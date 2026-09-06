#!/usr/bin/env python3
"""Build the copy-driven Motorcycle Service and Custom hubs in four languages."""

from __future__ import annotations

import html
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import quote, urlsplit

from build_output import write_html_if_changed
from hero_images import hero_background_css, hero_preload_links
from new_pages_data import PROJECT_TILES
from project_pages_data import PROJECT_CONFIGS
from site_chrome import chrome_fragments, localized_href


SITE_ROOT = Path(__file__).resolve().parents[2]
BUILD_DIR = Path(__file__).resolve().parent
DOMAIN = "https://ironcustommotors.com"
LANGS = ("en", "ru", "uk", "pt")
HREFLANG_CODES = {"en": "en", "ru": "ru", "uk": "uk", "pt": "pt-PT"}
EXPECTED_SOURCE_SHA256 = {
    "motorcycle-service": "c16a33ae3c204084a9e5356c2bd0a3b7c9d99dcfd44b30752565cea49f38d28c",
    "custom": "10790be1dab936791dd01b47bcfa9c3f1c73e12cc495275d2195a025a14f4292",
}

HUBS = {
    "motorcycle-service": {
        "copy": BUILD_DIR / "content" / "service_hub_copy_4lang.md",
        "hero": "/photos/service-action-1600.jpg",
        "section_count": 5,
        "service_type": {
            "en": "Motorcycle service, diagnostics and repair",
            "pt": "Revisão, diagnóstico e reparação de motas",
            "ru": "Сервис, диагностика и ремонт мотоциклов",
            "uk": "Сервіс, діагностика та ремонт мотоциклів",
        },
    },
    "custom": {
        "copy": BUILD_DIR / "content" / "custom_hub_copy_4lang.md",
        "hero": "/photos/why-engine-1600.jpg",
        "section_count": 6,
        "service_type": {
            "en": "Complete custom motorcycle projects",
            "pt": "Projetos completos de motas custom",
            "ru": "Полные проекты кастом-мотоциклов",
            "uk": "Повні проєкти кастом-мотоциклів",
        },
    },
}

UI = {
    "en": {"home": "Home", "services": "Services", "faq": "FAQ"},
    "pt": {"home": "Início", "services": "Serviços", "faq": "FAQ"},
    "ru": {"home": "Главная", "services": "Услуги", "faq": "FAQ"},
    "uk": {"home": "Головна", "services": "Послуги", "faq": "FAQ"},
}


def detect_cache_bust() -> str:
    source = (SITE_ROOT / "index.html").read_text(encoding="utf-8")
    match = re.search(r"/assets/main\.css\?v=([a-zA-Z0-9]+)", source)
    return match.group(1) if match else "20260906a"


def canonical_path(slug: str, lang: str) -> str:
    prefix = "" if lang == "en" else f"/{lang}"
    return f"{prefix}/{slug}/"


def canonical_url(slug: str, lang: str) -> str:
    return DOMAIN + canonical_path(slug, lang)


def output_path(slug: str, lang: str) -> Path:
    return SITE_ROOT / canonical_path(slug, lang).strip("/") / "index.html"


def split_language_blocks(markdown: str) -> dict[str, str]:
    header_to_lang = {
        "ENGLISH": "en",
        "PORTUGUÊS (pt-PT)": "pt",
        "РУССКИЙ": "ru",
        "УКРАЇНСЬКА": "uk",
    }
    matches = list(re.finditer(r"^## (.+?)\s*$", markdown, flags=re.MULTILINE))
    blocks: dict[str, str] = {}
    for index, match in enumerate(matches):
        lang = header_to_lang.get(match.group(1).strip())
        if not lang:
            continue
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        blocks[lang] = markdown[match.end():end].strip()
    missing = set(LANGS) - set(blocks)
    if missing:
        raise ValueError(f"Missing hub copy blocks: {', '.join(sorted(missing))}")
    return blocks


def extract_field(block: str, label: str) -> str:
    match = re.search(
        rf"^\*\*{re.escape(label)}:\*\*\s*(.*?)\s*$",
        block,
        flags=re.MULTILINE,
    )
    if not match:
        raise ValueError(f"Missing field: {label}")
    return match.group(1).strip().strip("`")


def heading_slice(block: str, heading: str, next_pattern: str) -> str:
    match = re.search(rf"^###\s+{heading}\s*$", block, flags=re.MULTILINE)
    if not match:
        raise ValueError(f"Missing heading: {heading}")
    following = re.search(next_pattern, block[match.end():], flags=re.MULTILINE)
    end = match.end() + following.start() if following else len(block)
    return block[match.end():end].strip()


def extract_sections(block: str, expected_count: int) -> list[dict[str, str]]:
    matches = list(
        re.finditer(r"^###\s+(\d{2})\s+·\s+(.+?)\s*$", block, flags=re.MULTILINE)
    )
    sections: list[dict[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(block)
        next_special = re.search(r"^###\s+(?:CTA\s+—|FAQ\s*$)", block[match.end():end], flags=re.MULTILINE)
        if next_special:
            end = match.end() + next_special.start()
        sections.append(
            {
                "number": match.group(1),
                "title": match.group(2).strip(),
                "body": block[match.end():end].strip(),
            }
        )
    if len(sections) != expected_count:
        raise ValueError(f"Expected {expected_count} hub sections, got {len(sections)}")
    return sections


def extract_named_section(block: str, heading_pattern: str, end_pattern: str) -> dict[str, str]:
    match = re.search(rf"^###\s+({heading_pattern})\s*$", block, flags=re.MULTILINE)
    if not match:
        raise ValueError(f"Missing section matching: {heading_pattern}")
    following = re.search(end_pattern, block[match.end():], flags=re.MULTILINE)
    end = match.end() + following.start() if following else len(block)
    return {"title": match.group(1).strip(), "body": block[match.end():end].strip()}


def extract_faq(block: str) -> list[dict[str, str]]:
    raw = heading_slice(block, "FAQ", r"^## ")
    items = []
    for line in raw.splitlines():
        match = re.match(r"^-\s+\*\*(.+?)\*\*\s+(.+?)\s*$", line.strip())
        if match:
            items.append({"question": match.group(1).strip(), "answer": match.group(2).strip()})
    if len(items) != 6:
        raise ValueError(f"Expected 6 FAQ items, got {len(items)}")
    return items


def parse_copy(slug: str) -> dict[str, dict]:
    config = HUBS[slug]
    source_bytes = config["copy"].read_bytes()
    actual_hash = hashlib.sha256(source_bytes).hexdigest()
    expected_hash = EXPECTED_SOURCE_SHA256[slug]
    if actual_hash != expected_hash:
        raise ValueError(
            f"{config['copy'].name}: SHA-256 {actual_hash} != approved {expected_hash}"
        )
    blocks = split_language_blocks(source_bytes.decode("utf-8"))
    parsed: dict[str, dict] = {}
    for lang, block in blocks.items():
        cta = extract_named_section(block, r"CTA\s+—\s+.+?", r"^###\s+")
        cta["title"] = re.sub(r"^CTA\s+—\s+", "", cta["title"])
        related = extract_named_section(
            block,
            r"(?:Related paths|Caminhos relacionados|Смежные страницы|Суміжні сторінки)",
            r"^###\s+FAQ\s*$",
        )
        content = {
            "seo_title": extract_field(block, "SEO Title"),
            "meta_description": extract_field(block, "Meta"),
            "source_slug": extract_field(block, "Slug"),
            "eyebrow": extract_field(block, "Eyebrow"),
            "h1": extract_field(block, "H1"),
            "whatsapp_prefill": extract_field(block, "WhatsApp prefill").rstrip(),
            "hero": heading_slice(block, "Hero intro", r"^###\s+01\s+·"),
            "sections": extract_sections(block, config["section_count"]),
            "cta": cta,
            "related": related,
            "faq": extract_faq(block),
        }
        expected = canonical_path(slug, lang)
        if content["source_slug"] != expected:
            raise ValueError(f"{slug}/{lang}: slug {content['source_slug']} != {expected}")
        parsed[lang] = content
    return parsed


def markdown_plain(value: str) -> str:
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = value.replace("**", "")
    return re.sub(r"\s+", " ", value).strip()


def _bold_html(value: str) -> str:
    parts = re.split(r"(\*\*.+?\*\*)", value)
    rendered = []
    for part in parts:
        if part.startswith("**") and part.endswith("**"):
            rendered.append(f"<strong>{html.escape(part[2:-2], quote=False)}</strong>")
        else:
            rendered.append(html.escape(part, quote=False))
    return "".join(rendered)


def link_attributes(href: str, lang: str, prefill: str) -> tuple[str, str]:
    parsed = urlsplit(href)
    if parsed.netloc in {"wa.me", "www.wa.me"}:
        target = f"https://wa.me/351917961230?text={quote(prefill, safe='')}"
        return target, ' data-wa="" rel="noopener" target="_blank"'

    localized = localized_href(href, lang)
    if urlsplit(localized).path.rstrip("/").endswith("/contact"):
        return "#contact", ' data-cta="book"'
    if parsed.scheme in {"http", "https"} and "ironcustommotors.com" not in parsed.netloc:
        return localized, ' rel="noopener" target="_blank"'
    return localized, ""


def inline_markdown(value: str, lang: str, prefill: str) -> str:
    rendered = []
    position = 0
    for match in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", value):
        rendered.append(_bold_html(value[position:match.start()]))
        label = _bold_html(match.group(1))
        href, attrs = link_attributes(match.group(2), lang, prefill)
        rendered.append(f'<a href="{html.escape(href, quote=True)}"{attrs}>{label}</a>')
        position = match.end()
    rendered.append(_bold_html(value[position:]))
    return "".join(rendered)


def split_hero_actions(markdown: str) -> tuple[str, list[tuple[str, str]]]:
    lines = [line.rstrip() for line in markdown.splitlines()]
    if not lines:
        return "", []
    matches = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", lines[-1])
    if len(matches) < 2:
        return markdown.strip(), []
    return "\n".join(lines[:-1]).strip(), matches


def render_action(label: str, href: str, lang: str, prefill: str, primary: bool) -> str:
    target, attrs = link_attributes(href, lang, prefill)
    class_name = "btn btn-primary" if primary else "btn btn-ghost"
    return (
        f'<a class="{class_name}" href="{html.escape(target, quote=True)}"{attrs}>'
        f"{html.escape(label, quote=False)}</a>"
    )


def render_flow(markdown: str, lang: str, prefill: str) -> str:
    output = []
    list_items: list[str] = []

    def flush_list() -> None:
        nonlocal list_items
        if list_items:
            output.append(
                '<ul class="hub-list">'
                + "".join(
                    f"<li>{inline_markdown(item, lang, prefill)}</li>" for item in list_items
                )
                + "</ul>"
            )
            list_items = []

    for raw_line in markdown.splitlines():
        line = raw_line.strip()
        if not line:
            flush_list()
            continue
        if line == "{{PROJECT_CUSTOM_LINKS}}":
            flush_list()
            output.append(render_project_links(lang))
        elif line.startswith("- "):
            list_items.append(line[2:].strip())
        elif line.startswith("**"):
            flush_list()
            output.append(f'<article class="hub-copy-card"><p>{inline_markdown(line, lang, prefill)}</p></article>')
        else:
            flush_list()
            output.append(f"<p>{inline_markdown(line, lang, prefill)}</p>")
    flush_list()
    return "\n".join(output)


def render_project_links(lang: str) -> str:
    links = []
    for tile in PROJECT_TILES:
        config = PROJECT_CONFIGS.get(tile["slug"])
        if config and config.get("integrations", {}).get("custom"):
            href = localized_href(f'/projects/{tile["slug"]}/', lang)
            links.append(
                f'<a class="btn btn-ghost" href="{href}">'
                f'{html.escape(tile["label"][lang], quote=False)} →</a>'
            )
    if len(links) != len(PROJECT_TILES):
        raise ValueError(
            f"Custom integration has {len(links)} projects; expected {len(PROJECT_TILES)}"
        )
    return (
        '<div class="hub-project-grid" data-project-custom-links="">\n'
        '<!-- PROJECT_CUSTOM_LINKS_START -->\n'
        + "\n".join(links)
        + "\n<!-- PROJECT_CUSTOM_LINKS_END -->\n</div>"
    )


def render_related(section: dict[str, str], lang: str, prefill: str) -> str:
    cards = []
    has_harley_custom = False
    for line in section["body"].splitlines():
        match = re.match(r"^-\s+\[([^\]]+)\]\(([^)]+)\)\s*$", line.strip())
        if not match:
            continue
        href, attrs = link_attributes(match.group(2), lang, prefill)
        classes = "related-card"
        if urlsplit(href).path.rstrip("/").endswith("/harley-custom"):
            classes += " custom-harley-link"
            has_harley_custom = True
        cards.append(
            f'<a class="{classes}" href="{html.escape(href, quote=True)}"{attrs}>'
            f'<span class="related-card-label">{html.escape(match.group(1), quote=False)}</span>'
            '<span aria-hidden="true" class="related-card-arrow">→</span></a>'
        )
    if len(cards) != 5:
        raise ValueError(f"Expected 5 related paths, got {len(cards)}")
    grid_classes = "related-card-grid"
    if has_harley_custom:
        grid_classes += " custom-harley-link"
    return f"""
<section class="hub-section hub-related" data-copy-section="related">
<div class="container">
<div class="hub-heading"><h2>{html.escape(section['title'], quote=False)}</h2></div>
<div class="{grid_classes}">{''.join(cards)}</div>
</div>
</section>"""


def render_faq(items: list[dict[str, str]], lang: str, prefill: str) -> str:
    details = []
    for item in items:
        details.append(
            "<details>"
            f"<summary><span>{inline_markdown(item['question'], lang, prefill)}</span>"
            '<span aria-hidden="true" class="chev">⌄</span></summary>'
            f'<div class="answer"><p>{inline_markdown(item["answer"], lang, prefill)}</p></div>'
            "</details>"
        )
    return f"""
<section class="hub-section hub-faq" data-copy-section="faq" id="faq">
<div class="container">
<div class="hub-heading"><h2>{UI[lang]['faq']}</h2></div>
<div class="hub-faq-list">{''.join(details)}</div>
</div>
</section>"""


def business_entity(lang: str) -> dict:
    return {
        "@type": ["LocalBusiness", "MotorcycleRepair"],
        "@id": f"{DOMAIN}/#business",
        "name": "Iron Custom Motors",
        "url": DOMAIN + localized_href("/", lang),
        "logo": {
            "@type": "ImageObject",
            "url": f"{DOMAIN}/photos/icon-512.png",
            "width": 512,
            "height": 512,
        },
        "image": f"{DOMAIN}/photos/og.jpg",
        "telephone": "+351917961230",
        "priceRange": "€€",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "R. António José da Silva 100 B",
            "addressLocality": "São Domingos de Rana",
            "addressRegion": "Lisbon",
            "postalCode": "2785-253",
            "addressCountry": "PT",
        },
    }


def schema_graph(slug: str, content: dict, lang: str) -> dict:
    canonical = canonical_url(slug, lang)
    service_id = canonical + "#service"
    webpage_id = canonical + "#webpage"
    faq_id = canonical + "#faq"
    business_ref = {"@id": f"{DOMAIN}/#business", "name": "Iron Custom Motors"}
    service = {
        "@type": "Service",
        "@id": service_id,
        "name": content["h1"],
        "serviceType": HUBS[slug]["service_type"][lang],
        "description": content["meta_description"],
        "url": canonical,
        "provider": business_ref,
        "areaServed": [
            {"@type": "City", "name": name}
            for name in ("Cascais", "Estoril", "Oeiras", "Sintra", "Lisbon")
        ],
        "mainEntityOfPage": {"@id": webpage_id, "name": content["h1"]},
    }
    webpage = {
        "@type": "WebPage",
        "@id": webpage_id,
        "url": canonical,
        "name": content["h1"],
        "description": content["meta_description"],
        "inLanguage": HREFLANG_CODES[lang],
        "about": business_ref,
        "mainEntity": {"@id": service_id, "name": content["h1"]},
    }
    faq = {
        "@type": "FAQPage",
        "@id": faq_id,
        "mainEntity": [
            {
                "@type": "Question",
                "name": markdown_plain(item["question"]),
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": markdown_plain(item["answer"]),
                },
            }
            for item in content["faq"]
        ],
    }
    breadcrumbs = {
        "@type": "BreadcrumbList",
        "@id": canonical + "#breadcrumb",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": UI[lang]["home"],
                "item": DOMAIN + localized_href("/", lang),
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": content["h1"],
                "item": canonical,
            },
        ],
    }
    return {
        "@context": "https://schema.org",
        "@graph": [business_entity(lang), webpage, service, faq, breadcrumbs],
    }


def head_html(slug: str, content: dict, lang: str) -> str:
    config = HUBS[slug]
    canonical = canonical_url(slug, lang)
    alternates = "\n".join(
        f'<link rel="alternate" hreflang="{HREFLANG_CODES[code]}" href="{canonical_url(slug, code)}"/>'
        for code in LANGS
    )
    graph = json.dumps(schema_graph(slug, content, lang), ensure_ascii=False)
    og_locale = {"en": "en_US", "ru": "ru_RU", "uk": "uk_UA", "pt": "pt_PT"}[lang]
    hero_url = config["hero"]
    cache_bust = detect_cache_bust()
    return f"""<!DOCTYPE html>
<html data-lang="{lang}" lang="{lang}">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1, viewport-fit=cover" name="viewport"/>
<meta content="#0a0a0a" name="theme-color"/>
<meta content="max-image-preview:large" name="robots"/>
<title>{html.escape(content['seo_title'])}</title>
<meta content="{html.escape(content['meta_description'], quote=True)}" name="description"/>
<link href="{canonical}" rel="canonical"/>
{alternates}
<link rel="alternate" hreflang="x-default" href="{canonical_url(slug, 'en')}"/>
<meta content="{html.escape(content['seo_title'], quote=True)}" property="og:title"/>
<meta content="{html.escape(content['meta_description'], quote=True)}" property="og:description"/>
<meta content="website" property="og:type"/>
<meta content="{canonical}" property="og:url"/>
<meta content="Iron Custom Motors" property="og:site_name"/>
<meta content="{DOMAIN}{hero_url}" property="og:image"/>
<meta content="{og_locale}" property="og:locale"/>
<meta content="summary_large_image" name="twitter:card"/>
<meta content="{html.escape(content['seo_title'], quote=True)}" name="twitter:title"/>
<meta content="{html.escape(content['meta_description'], quote=True)}" name="twitter:description"/>
<meta content="{DOMAIN}{hero_url}" name="twitter:image"/>
<link href="/photos/favicon.ico" rel="icon" sizes="any"/>
<link href="/photos/favicon-32.png" rel="icon" sizes="32x32" type="image/png"/>
<link href="/photos/apple-touch-icon.png" rel="apple-touch-icon" sizes="180x180"/>
<link href="/photos/site.webmanifest" rel="manifest"/>
<link href="https://fonts.googleapis.com" rel="preconnect"/>
<link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
{hero_preload_links(hero_url)}
<link href="https://fonts.googleapis.com/css2?family=Saira:wght@300;400;500;600;700;800;900&amp;family=Saira+Condensed:wght@400;600;700;800;900&amp;family=Roboto+Condensed:wght@400;500;600;700;800;900&amp;family=Inter:wght@300;400;500;600;700&amp;display=swap" rel="stylesheet"/>
<link href="/assets/main.css?v={cache_bust}" rel="stylesheet"/>
<style>{page_css(hero_url)}</style>
<script type="application/ld+json">{graph}</script>
</head>"""


def page_css(hero_url: str) -> str:
    return """.hub-hero{position:relative;isolation:isolate;overflow:hidden;min-height:78vh;padding:150px 0 84px;background:#080808}
.hub-hero::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,rgba(8,8,8,.95),rgba(8,8,8,.72) 55%,rgba(8,8,8,.3)),linear-gradient(180deg,rgba(8,8,8,.18),#080808 96%)}
.hub-hero-bg{position:absolute;inset:0;z-index:-2;background-size:cover;background-position:center;filter:saturate(.88) contrast(1.06) brightness(.62);""" + hero_background_css(hero_url, 768) + """}
@media (min-width:768px){.hub-hero-bg{""" + hero_background_css(hero_url, 1280) + """}}
@media (min-width:1280px){.hub-hero-bg{""" + hero_background_css(hero_url, 1920) + """}}
.hub-hero h1{max-width:min(1040px,82vw,calc(100vw - 40px));margin:18px 0 24px;font-family:var(--font-display);font-size:clamp(32px,5vw,68px);font-weight:900;line-height:.9;text-transform:uppercase;color:#fff;overflow-wrap:anywhere}
.hub-hero .lead{max-width:min(940px,78vw,calc(100vw - 40px));font-size:clamp(18px,1.4vw,23px);line-height:1.62;color:var(--text)}
.hub-hero .lead p{margin:0 0 16px}.hub-actions{display:flex;align-items:center;flex-wrap:wrap;gap:14px;margin-top:28px}.hub-actions .btn{white-space:normal}
.hub-section{padding:clamp(44px,6vw,78px) 0;background:#080808;border-top:1px solid var(--border)}
.hub-heading{display:grid;grid-template-columns:minmax(0,1fr);gap:18px;margin-bottom:30px}.hub-heading h2{max-width:min(980px,82vw,calc(100vw - 40px));margin:0;font-family:var(--font-display);font-size:clamp(27px,4vw,52px);font-weight:900;line-height:.94;text-transform:uppercase;color:#fff;overflow-wrap:anywhere}.hub-heading .num{color:var(--accent)}
.hub-copy{display:grid;gap:14px;max-width:1120px}.hub-copy>p,.hub-copy-card p{margin:0;font-size:clamp(16px,1.25vw,20px);line-height:1.67;color:var(--text)}
.hub-copy a,.hub-faq a{color:var(--accent);text-decoration:none;border-bottom:1px solid rgba(255,87,34,.5)}.hub-copy strong,.hub-faq strong{color:#fff}
.hub-copy-card{padding:20px 22px;border:1px solid var(--border);border-radius:var(--radius-lg);background:var(--surface)}
.hub-project-grid{display:flex;flex-wrap:wrap;gap:10px;margin:6px 0}.hub-project-grid .btn{min-height:42px;padding:11px 15px}
.hub-cta{background:#101010;text-align:center}.hub-cta .container{max-width:980px}.hub-cta .hub-copy{margin:0 auto}.hub-cta .hub-actions{justify-content:center}
.related-card-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}.related-card{position:relative;display:flex;min-height:128px;flex-direction:column;justify-content:space-between;gap:18px;padding:20px 18px;border:1px solid var(--border);border-radius:16px;background:var(--surface);color:#fff;text-decoration:none;overflow:hidden;transition:transform .25s var(--ease),border-color .25s var(--ease),background .25s var(--ease)}.related-card:hover,.related-card:focus-visible{transform:translateY(-4px);border-color:var(--accent);background:var(--surface-2);outline:none}.related-card-label{position:relative;z-index:1;font-family:var(--font-display);font-weight:800;text-transform:uppercase;font-size:clamp(17px,1.35vw,22px);line-height:1;color:#fff}.related-card-arrow{color:var(--accent);font-weight:800}
.hub-faq-list{display:grid;gap:12px}.hub-faq-list details{border:1px solid var(--border);border-radius:var(--radius-lg);background:var(--surface);overflow:hidden}.hub-faq-list summary{display:flex;gap:18px;align-items:flex-start;justify-content:space-between;cursor:pointer;padding:22px 24px;list-style:none;font-family:var(--font-display);font-size:clamp(18px,1.6vw,24px);font-weight:800;line-height:1.1;text-transform:uppercase;color:#fff}.hub-faq-list summary::-webkit-details-marker{display:none}.hub-faq-list .chev{color:var(--accent);transition:transform .2s var(--ease)}.hub-faq-list details[open] .chev{transform:rotate(180deg)}.hub-faq-list .answer{padding:0 24px 24px;color:var(--text-dim);font-size:16px;line-height:1.65}.hub-faq-list .answer p{margin:0}
@media (max-width:900px){.related-card-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:640px){.hub-hero{min-height:auto;padding:124px 0 62px}.hub-hero h1{max-width:calc(100vw - 40px);font-size:clamp(29px,9vw,39px);line-height:.94}.hub-hero .lead{max-width:calc(100vw - 40px)}.hub-actions{display:grid;grid-template-columns:1fr}.hub-actions .btn{width:100%;justify-content:center;text-align:center}.hub-section{padding:38px 0}.hub-heading{margin-bottom:24px}.related-card-grid{grid-template-columns:1fr}.related-card{min-height:108px}.hub-copy-card{padding:18px}}
"""


def render_page(slug: str, content: dict, lang: str) -> str:
    before, after = chrome_fragments(lang, detect_cache_bust())
    hero_body, hero_actions = split_hero_actions(content["hero"])
    if len(hero_actions) != 3:
        raise ValueError(f"{slug}/{lang}: expected three hero actions, got {len(hero_actions)}")
    hero_action_html = "".join(
        render_action(label, href, lang, content["whatsapp_prefill"], index == 0)
        for index, (label, href) in enumerate(hero_actions)
    )
    sections = "".join(
        f"""
<section class="hub-section" data-copy-section="{section['number']}" id="section-{section['number']}">
<div class="container">
<div class="hub-heading"><h2><span class="num">{section['number']} ·</span> {html.escape(section['title'], quote=False)}</h2></div>
<div class="hub-copy">{render_flow(section['body'], lang, content['whatsapp_prefill'])}</div>
</div>
</section>"""
        for section in content["sections"]
    )
    return head_html(slug, content, lang) + f"""
<body>
{before}
<main data-copy-driven-hub="{slug}">
<section class="hub-hero">
<div aria-hidden="true" class="hub-hero-bg" data-lcp-responsive-background=""></div>
<div class="container">
<div class="crumb"><a href="{localized_href('/', lang)}">{UI[lang]['home']}</a><span class="sep">→</span><a href="{localized_href('/services/', lang)}">{UI[lang]['services']}</a><span class="sep">→</span><span>{html.escape(content['h1'], quote=False)}</span></div>
<span class="h-eyebrow">{html.escape(content['eyebrow'], quote=False)}</span>
<h1>{html.escape(content['h1'], quote=False)}</h1>
<div class="lead">{render_flow(hero_body, lang, content['whatsapp_prefill'])}</div>
<div class="hub-actions">{hero_action_html}</div>
</div>
</section>
{sections}
<section class="hub-section hub-cta" data-copy-section="cta">
<div class="container">
<div class="hub-heading"><h2>{html.escape(content['cta']['title'], quote=False)}</h2></div>
<div class="hub-copy">{render_flow(content['cta']['body'], lang, content['whatsapp_prefill'])}</div>
</div>
</section>
{render_related(content['related'], lang, content['whatsapp_prefill'])}
{render_faq(content['faq'], lang, content['whatsapp_prefill'])}
</main>
{after}
</body>
</html>"""


def main() -> int:
    for slug in HUBS:
        content = parse_copy(slug)
        for lang in LANGS:
            target = output_path(slug, lang)
            target.parent.mkdir(parents=True, exist_ok=True)
            write_html_if_changed(
                target,
                render_page(slug, content[lang], lang),
                preserve_body_shell=False,
            )
            print(f"wrote {target.relative_to(SITE_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
