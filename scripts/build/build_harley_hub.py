#!/usr/bin/env python3
"""Build the Harley Hub, Harley tuning and Harley custom pages in four languages."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

from build_output import write_html_if_changed
from blog_data import BLOG_POSTS
from harley_hub_data import (
    HREFLANG_CODES,
    LANGUAGE_HEADINGS,
    PAGE_CONFIG,
    PORTFOLIO,
    PORTFOLIO_ORDER,
    UI,
)
from hero_images import hero_preload_links, optimized_hero_url
from site_chrome import chrome_fragments


SITE_ROOT = Path(__file__).resolve().parents[2]
BUILD_DIR = Path(__file__).resolve().parent
COPY_FILE = BUILD_DIR / "content" / "harley_hub_phase1_4lang.md"
DOMAIN = "https://ironcustommotors.com"
LANGS = ("en", "pt", "ru", "uk")
OG_LOCALES = {
    "en": "en_GB",
    "pt": "pt_PT",
    "ru": "ru_RU",
    "uk": "uk_UA",
}

PAGE_CSS = """
.harley-hero{position:relative;display:grid;min-height:min(620px,68vh);align-items:end;overflow:hidden;border-bottom:1px solid var(--border);background:#050505}
.harley-hero-media,.harley-hero-media img,.harley-hero-shade{position:absolute;inset:0;width:100%;height:100%}
.harley-hero-media img{object-fit:cover;object-position:center;filter:saturate(.85) contrast(1.05) brightness(.5)}
.harley-hero-shade{background:linear-gradient(180deg,rgba(10,10,10,.45) 0%,rgba(10,10,10,.6) 50%,rgba(10,10,10,.96) 100%)}
.harley-hero .container{position:relative;z-index:2;padding-top:140px;padding-bottom:50px}
.harley-hero .crumb{margin-bottom:18px}
.harley-hero h1{max-width:900px;color:#fff;font-family:var(--font-display);font-size:clamp(30px,4vw,52px);font-weight:800;line-height:.92;letter-spacing:0;text-transform:uppercase}
.harley-section{padding:clamp(34px,4vw,48px) 0;border-bottom:1px solid var(--border);background:#0a0a0a}
.harley-section:nth-of-type(even){background:#0d0d0d}
.harley-section .section-heading{display:grid;grid-template-columns:minmax(220px,.7fr) minmax(0,1.3fr);gap:36px;margin-bottom:24px}
.harley-section h2{max-width:760px;color:#fff;font-family:var(--font-display);font-size:clamp(24px,3.2vw,44px);font-weight:800;line-height:.95;letter-spacing:0;text-transform:uppercase}
.harley-copy{max-width:820px;margin-left:auto}
.harley-copy p{margin:0 0 15px;color:var(--text-dim);font-size:clamp(15px,1.05vw,17px);line-height:1.65}
.harley-copy p:last-child{margin-bottom:0}
.harley-copy strong{color:#fff}
.harley-copy a{color:var(--accent);text-underline-offset:4px}
.harley-section-wide .harley-copy{max-width:none;margin-left:0}
.harley-intro .harley-copy{max-width:940px;margin:0}
.harley-intro .harley-copy p{color:#d5d5d5;font-size:clamp(17px,1.45vw,21px);line-height:1.55}
.harley-step{padding:15px 0;border-bottom:1px solid var(--border)}
.hub-service-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin-top:22px}
.hub-service-tile{position:relative;display:flex;min-height:170px;flex-direction:column;justify-content:space-between;gap:18px;padding:22px;border:1px solid var(--border);border-radius:8px;background:#111;color:#fff;text-decoration:none;transition:transform .2s ease,border-color .2s ease,background .2s ease}
.hub-service-tile:hover,.hub-service-tile:focus-visible{transform:translateY(-3px);border-color:var(--accent);background:#151515;outline:none}
.hub-service-tile h3{max-width:21ch;color:#fff;font-family:var(--font-display);font-size:clamp(20px,2vw,28px);font-weight:800;line-height:1;text-transform:uppercase}
.hub-service-tile p{max-width:48ch;margin:0;color:var(--text-dim);font-size:14px;line-height:1.55}
.hub-service-tile .tile-arrow{color:var(--accent);font-size:22px}
.harley-feed{display:grid;gap:16px;margin-top:24px}
.harley-feed-card{display:grid;grid-template-columns:minmax(300px,.95fr) minmax(0,1.05fr);min-height:300px;overflow:hidden;border:1px solid var(--border);border-radius:8px;background:#101010;color:#fff;text-decoration:none}
.harley-feed-card picture,.harley-feed-card img{width:100%;height:100%}
.harley-feed-card img{display:block;object-fit:cover}
.harley-feed-body{display:flex;flex-direction:column;justify-content:center;padding:26px}
.harley-feed-date{margin-bottom:10px;color:var(--accent);font-family:var(--font-ui);font-size:12px;font-weight:700;text-transform:uppercase}
.harley-feed-card h3{margin-bottom:12px;color:#fff;font-family:var(--font-display);font-size:clamp(22px,2.4vw,32px);font-weight:800;line-height:1;text-transform:uppercase}
.harley-feed-card p{margin:0 0 16px;color:var(--text-dim);font-size:14px;line-height:1.55}
.harley-more{color:var(--accent);font-family:var(--font-ui);font-size:13px;font-weight:750;text-transform:uppercase}
.portfolio-list{display:grid;gap:18px;margin-top:24px}
.portfolio-row{display:grid;grid-template-columns:minmax(380px,1.08fr) minmax(0,.92fr);min-height:330px;overflow:hidden;border:1px solid var(--border);border-radius:8px;background:#101010}
.portfolio-row picture,.portfolio-row img{width:100%;height:100%}
.portfolio-row img{display:block;object-fit:cover}
.portfolio-body{display:flex;flex-direction:column;align-items:flex-start;justify-content:center;padding:28px}
.portfolio-body h3{margin-bottom:14px;color:#fff;font-family:var(--font-display);font-size:clamp(22px,2.4vw,32px);font-weight:800;line-height:.95;text-transform:uppercase}
.portfolio-body p{margin:0 0 20px;color:var(--text-dim);font-size:15px;line-height:1.6}
.harley-faq{max-width:820px;margin-left:auto}
.harley-faq details{border-top:1px solid var(--border)}
.harley-faq details:last-child{border-bottom:1px solid var(--border)}
.harley-faq summary{display:flex;cursor:pointer;align-items:center;justify-content:space-between;gap:20px;padding:18px 0;color:#fff;font-family:var(--font-ui);font-size:clamp(15px,1.3vw,18px);font-weight:700;list-style:none}
.harley-faq summary::-webkit-details-marker{display:none}
.harley-faq summary::after{content:"+";flex:none;color:var(--accent);font-size:22px}
.harley-faq details[open] summary::after{content:"−"}
.harley-faq .answer{padding:0 38px 18px 0;color:var(--text-dim);font-size:15px;line-height:1.6}
.harley-faq .answer a{color:var(--accent)}
.harley-cta{text-align:center}
.harley-cta .section-heading{display:block;margin-bottom:18px}
.harley-cta h2{margin:0 auto}
.harley-cta .harley-copy{margin:0 auto}
.inline-arrow-link{display:inline-flex;align-items:center;justify-content:center;min-width:28px;color:var(--accent);font-weight:800;text-decoration:none}
@media(max-width:900px){
  .harley-section .section-heading{grid-template-columns:1fr;gap:14px}
  .harley-copy,.harley-faq{margin-left:0}
  .harley-feed-card,.portfolio-row{grid-template-columns:1fr}
  .harley-feed-card picture{aspect-ratio:16/10}
  .portfolio-row picture{aspect-ratio:4/3}
}
@media(max-width:680px){
  .harley-hero{min-height:58vh}
  .harley-hero .container{padding-top:120px;padding-bottom:36px}
  .harley-hero h1{font-size:clamp(28px,8vw,40px)}
  .harley-section{padding:32px 0}
  .harley-section .section-heading{margin-bottom:20px}
  .hub-service-grid{grid-template-columns:1fr}
  .hub-service-tile{min-height:150px;padding:20px}
  .harley-feed-body,.portfolio-body{padding:22px}
  .harley-faq summary{padding:16px 0}
}
"""


def detect_cache_bust() -> str:
    text = (SITE_ROOT / "index.html").read_text(encoding="utf-8")
    match = re.search(r"/assets/main\.css\?v=([a-zA-Z0-9]+)", text)
    return match.group(1) if match else "20260906a"


def canonical_path(slug: str, lang: str) -> str:
    if lang == "en":
        return f"/{slug}/"
    return f"/{lang}/{slug}/"


def canonical_url(slug: str, lang: str) -> str:
    return DOMAIN + canonical_path(slug, lang)


def home_url(lang: str) -> str:
    return f"{DOMAIN}/" if lang == "en" else f"{DOMAIN}/{lang}/"


def localized_href(href: str, lang: str) -> str:
    if not href or not href.startswith("/") or href.startswith(("/photos/", "/assets/")):
        return href
    if re.match(r"^/(pt|ru|uk)(/|$)", href):
        return href
    if lang == "en":
        return href
    if href == "/":
        return f"/{lang}/"
    return f"/{lang}{href}"


def split_pages(source: str) -> dict[str, str]:
    matches = list(re.finditer(r"^# PAGE ([ABC])\b.*$", source, flags=re.MULTILINE))
    pages = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(source)
        pages[match.group(1)] = source[match.end():end].strip()
    missing = set(PAGE_CONFIG) - set(pages)
    if missing:
        raise ValueError(f"Missing Harley source pages: {', '.join(sorted(missing))}")
    return pages


def split_languages(page_source: str) -> dict[str, str]:
    heading_pattern = "|".join(re.escape(value) for value in LANGUAGE_HEADINGS)
    matches = list(re.finditer(rf"^## ({heading_pattern})\s*$", page_source, flags=re.MULTILINE))
    blocks = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(page_source)
        blocks[LANGUAGE_HEADINGS[match.group(1)]] = page_source[match.end():end].strip().removesuffix("---").strip()
    missing = set(LANGS) - set(blocks)
    if missing:
        raise ValueError(f"Missing Harley language blocks: {', '.join(sorted(missing))}")
    return blocks


def extract_field(block: str, labels: tuple[str, ...]) -> str:
    for label in labels:
        match = re.search(rf"^\*\*{re.escape(label)}:\*\*\s*(.+?)\s*$", block, flags=re.MULTILINE)
        if match:
            return match.group(1).strip()
    raise ValueError(f"Missing field: {' / '.join(labels)}")


def stash_token(tokens: list[str], value: str) -> str:
    tokens.append(value)
    return f"@@ICM_HARLEY_{len(tokens) - 1}@@"


def inline_markdown(value: str, lang: str) -> str:
    tokens: list[str] = []

    def markdown_link(match: re.Match[str]) -> str:
        label, href = match.group(1), localized_href(match.group(2), lang)
        rendered = f'<a href="{html.escape(href, quote=True)}">{html.escape(label, quote=False)}</a>'
        return stash_token(tokens, rendered)

    def path_link(match: re.Match[str]) -> str:
        href = localized_href(match.group(1), lang)
        rendered = f'<a href="{html.escape(href, quote=True)}">{html.escape(match.group(1), quote=False)}</a>'
        return stash_token(tokens, rendered)

    def arrow_link(match: re.Match[str]) -> str:
        href = localized_href(match.group(1), lang)
        rendered = (
            f'<a aria-label="{html.escape(href, quote=True)}" class="inline-arrow-link" '
            f'href="{html.escape(href, quote=True)}">→</a>'
        )
        return stash_token(tokens, rendered)

    value = re.sub(r"\[([^\]]+)\]\((/[^)]+)\)", markdown_link, value)
    value = re.sub(r"\[→\s*(/[^\]]+)\]", arrow_link, value)
    value = re.sub(r"\[(/[^\]]+)\]", path_link, value)
    value = re.sub(
        r"\*\*(.+?)\*\*",
        lambda match: stash_token(tokens, f"<strong>{inline_markdown(match.group(1), lang)}</strong>"),
        value,
    )
    value = re.sub(
        r"(?<!\*)\*(.+?)\*(?!\*)",
        lambda match: stash_token(tokens, f"<em>{inline_markdown(match.group(1), lang)}</em>"),
        value,
    )
    value = html.escape(value, quote=False)
    return re.sub(
        r"@@ICM_HARLEY_(\d+)@@",
        lambda match: tokens[int(match.group(1))],
        value,
    )


def parse_blocks(raw: str, lang: str) -> list[dict[str, str]]:
    blocks = []
    paragraph: list[str] = []

    def flush() -> None:
        if paragraph:
            value = " ".join(part.strip() for part in paragraph).strip()
            blocks.append({"type": "p", "html": inline_markdown(value, lang)})
            paragraph.clear()

    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped:
            flush()
            continue
        if stripped == "[PORTFOLIO: cards slot]":
            flush()
            blocks.append({"type": "portfolio"})
            continue
        if re.match(r"^\*\*\d+\.", stripped):
            flush()
            blocks.append({"type": "step", "html": inline_markdown(stripped, lang)})
            continue
        paragraph.append(stripped)
    flush()
    return blocks


def parse_faq(raw: str, lang: str) -> list[dict[str, str]]:
    items = []
    current_question = None
    answer_lines: list[str] = []

    def flush() -> None:
        nonlocal current_question
        if current_question is None:
            return
        answer = " ".join(line.strip() for line in answer_lines if line.strip()).strip()
        items.append(
            {
                "question": current_question,
                "answer_html": inline_markdown(answer, lang),
            }
        )
        current_question = None
        answer_lines.clear()

    for line in raw.splitlines():
        stripped = line.strip()
        question = re.fullmatch(r"\*\*(.+?)\*\*", stripped)
        if question:
            flush()
            current_question = question.group(1).strip()
        elif current_question is not None:
            answer_lines.append(stripped)
    flush()
    if not items:
        raise ValueError("Harley FAQ has no parsed questions")
    return items


def parse_language(block: str, lang: str) -> dict:
    title = extract_field(block, ("SEO Title",))
    description = extract_field(block, ("Meta", "Meta Description"))
    source_slug = extract_field(block, ("Slug",))
    h1_match = re.search(r"^# (?!PAGE )(.+?)\s*$", block, flags=re.MULTILINE)
    if not h1_match:
        raise ValueError("Missing Harley page H1")
    h1 = h1_match.group(1).strip()
    body = block[h1_match.end():].strip()

    image_match = re.search(
        r'^\[IMAGE:.*?ALT:\s*(?:"([^"]+)"|«([^»]+)»|(.+?))\]\s*$',
        body,
        flags=re.MULTILINE,
    )
    if not image_match:
        raise ValueError(f"Missing Harley hero slot for {lang}")
    hero_alt = next(value for value in image_match.groups() if value).strip().strip('"').strip("»").strip("«")
    body = (body[:image_match.start()] + body[image_match.end():]).strip()

    section_matches = list(re.finditer(r"^## (.+?)\s*$", body, flags=re.MULTILINE))
    preamble = body[:section_matches[0].start()].strip() if section_matches else body
    sections = []
    for index, match in enumerate(section_matches):
        end = section_matches[index + 1].start() if index + 1 < len(section_matches) else len(body)
        section_raw = body[match.end():end].strip()
        section = {
            "title": match.group(1).strip(),
            "raw": section_raw,
            "blocks": parse_blocks(section_raw, lang),
        }
        if match.group(1).strip() in ("FAQ", "Perguntas frequentes"):
            section["faq"] = parse_faq(section_raw, lang)
        sections.append(section)

    return {
        "title": title,
        "description": description,
        "source_slug": source_slug,
        "h1": h1,
        "hero_alt": hero_alt,
        "preamble": parse_blocks(preamble, lang),
        "sections": sections,
    }


def load_copy() -> dict[str, dict[str, dict]]:
    source = COPY_FILE.read_text(encoding="utf-8")
    parsed = {}
    for page_code, page_source in split_pages(source).items():
        config = PAGE_CONFIG[page_code]
        parsed[config["key"]] = {
            lang: parse_language(block, lang)
            for lang, block in split_languages(page_source).items()
        }
        for lang, page in parsed[config["key"]].items():
            expected = canonical_path(config["slug"], lang)
            if page["source_slug"] != expected:
                raise ValueError(
                    f"Unexpected source slug for {config['key']} {lang}: "
                    f"{page['source_slug']} (expected {expected})"
                )
    return parsed


def render_picture(
    source: str,
    dims: tuple[int, int],
    alt: str,
    *,
    sizes: str,
    eager: bool = False,
    class_name: str | None = None,
) -> str:
    width, height = dims
    candidates = []
    for requested_width in (768, 1280, 1920):
        actual_width = min(requested_width, width)
        if candidates and candidates[-1][1] == actual_width:
            continue
        candidates.append((requested_width, actual_width))
    srcset = lambda ext: ", ".join(
        f"{optimized_hero_url(source, requested_width, ext)} {actual_width}w"
        for requested_width, actual_width in candidates
    )
    class_attr = f' class="{class_name}"' if class_name else ""
    loading = "" if eager else ' loading="lazy"'
    priority = ' fetchpriority="high"' if eager else ""
    return f'''<picture{class_attr}>
<source sizes="{sizes}" srcset="{srcset("avif")}" type="image/avif"/>
<source sizes="{sizes}" srcset="{srcset("webp")}" type="image/webp"/>
<img alt="{html.escape(alt, quote=True)}" decoding="async"{priority} height="{height}" sizes="{sizes}" src="{optimized_hero_url(source, 1280, "jpg")}" srcset="{srcset("jpg")}" width="{width}"{loading}/>
</picture>'''


def render_blocks(blocks: list[dict[str, str]]) -> str:
    rendered = []
    for block in blocks:
        if block["type"] == "portfolio":
            rendered.append("<!-- PORTFOLIO_SLOT -->")
        else:
            class_attr = ' class="harley-step"' if block["type"] == "step" else ""
            rendered.append(f"<p{class_attr}>{block['html']}</p>")
    return "\n".join(rendered)


def parse_hub_tiles(raw: str, lang: str) -> list[dict[str, str]]:
    tiles = []
    for paragraph in [item.strip() for item in raw.split("\n\n") if item.strip()]:
        match = re.fullmatch(r"\*\*(.+?)\*\*\s*(.*?)\s*\[→\s*(/[^\]]+)\]", paragraph, flags=re.DOTALL)
        if not match:
            raise ValueError(f"Cannot parse Harley hub tile: {paragraph[:80]}")
        tiles.append(
            {
                "title": match.group(1).strip(),
                "description": " ".join(match.group(2).split()),
                "href": localized_href(match.group(3), lang),
            }
        )
    if len(tiles) != 4:
        raise ValueError(f"Expected 4 Harley hub tiles, got {len(tiles)}")
    return tiles


def render_hub_tiles(raw: str, lang: str) -> str:
    cards = []
    for tile in parse_hub_tiles(raw, lang):
        cards.append(
            f'''<a class="hub-service-tile" href="{html.escape(tile["href"], quote=True)}">
<h3>{inline_markdown(tile["title"], lang)}</h3>
<p>{inline_markdown(tile["description"], lang)}</p>
<span aria-hidden="true" class="tile-arrow">→</span>
</a>'''
        )
    return '<div class="hub-service-grid">\n' + "\n".join(cards) + "\n</div>"


def article_hero(post: dict) -> str:
    if post.get("heroImage"):
        return post["heroImage"]
    return f"{post['imageBase']}-{post['imageHero']:02d}-1600.jpg"


def article_hero_dims(post: dict) -> tuple[int, int]:
    if post.get("heroImageDims"):
        return tuple(post["heroImageDims"])
    return tuple(post["imageDims"][post["imageHero"]])


def render_harley_feed(lang: str) -> str:
    posts = [
        (slug, post)
        for slug, post in BLOG_POSTS.items()
        if "harley" in {str(topic).lower() for topic in post.get("topics", ())}
    ]
    posts.sort(key=lambda item: item[1]["publishedISO"], reverse=True)
    if not posts:
        return f'<p class="harley-feed-empty">{html.escape(UI[lang]["noPosts"])}</p>'

    cards = []
    for slug, post in posts:
        body = post["body"][lang]
        href = localized_href(f"/blog/{slug}/", lang)
        image = article_hero(post)
        picture = render_picture(
            image,
            article_hero_dims(post),
            body["heroAlt"],
            sizes="(max-width: 900px) 100vw, 48vw",
        )
        cards.append(
            f'''<a class="harley-feed-card" href="{href}">
{picture}
<div class="harley-feed-body">
<div class="harley-feed-date">{html.escape(body["publishedLabel"])}</div>
<h3>{html.escape(body["h1Crumb"])}</h3>
<p>{html.escape(post["meta"][lang]["excerpt"])}</p>
<span class="harley-more">{html.escape(UI[lang]["readMore"])} →</span>
</div>
</a>'''
        )
    return '<div class="harley-feed">\n' + "\n".join(cards) + "\n</div>"


def render_portfolio(lang: str) -> str:
    rows = []
    for slug in PORTFOLIO_ORDER:
        item = PORTFOLIO[slug]
        href = localized_href(f"/projects/{slug}/", lang)
        picture = render_picture(
            item["image"],
            item["dims"],
            item["name"],
            sizes="(max-width: 900px) 100vw, 54vw",
        )
        rows.append(
            f'''<article class="portfolio-row">
{picture}
<div class="portfolio-body">
<h3>{html.escape(item["name"])}</h3>
<p>{html.escape(item["copy"][lang])}</p>
<a class="btn btn-ghost" href="{href}">{html.escape(UI[lang]["viewProject"])} →</a>
</div>
</article>'''
        )
    return '<div class="portfolio-list">\n' + "\n".join(rows) + "\n</div>"


def plain_text(value: str) -> str:
    return " ".join(BeautifulSoup(value, "html.parser").get_text(" ", strip=True).split())


def faq_items(page: dict) -> list[dict[str, str]]:
    for section in page["sections"]:
        if section.get("faq"):
            return section["faq"]
    raise ValueError("Missing FAQ section")


def schema_graph(config: dict, page: dict, lang: str) -> dict:
    canonical = canonical_url(config["slug"], lang)
    page_id = canonical + "#webpage"
    localized_home = home_url(lang)
    business_id = DOMAIN + "/#business"
    business = {
        "@type": ["LocalBusiness", "MotorcycleRepair"],
        "@id": business_id,
        "name": "Iron Custom Motors",
        "url": localized_home,
        "logo": DOMAIN + "/photos/icon-512.png",
        "image": DOMAIN + "/photos/og.jpg",
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
    business_reference = {
        "@id": business_id,
        "name": "Iron Custom Motors",
    }
    webpage_type = ["CollectionPage", "WebPage"] if config["key"] == "hub" else "WebPage"
    webpage = {
        "@type": webpage_type,
        "@id": page_id,
        "url": canonical,
        "name": page["h1"],
        "description": page["description"],
        "inLanguage": HREFLANG_CODES[lang],
        "isPartOf": {
            "@id": DOMAIN + "/#website",
            "name": "Iron Custom Motors",
        },
        "about": business_reference,
    }

    graph = [business, webpage]
    if config["schema_type"] == "Service":
        service_name = (
            UI[lang]["serviceTypeTuning"]
            if config["key"] == "tuning"
            else UI[lang]["serviceTypeCustom"]
        )
        service = {
            "@type": "Service",
            "@id": canonical + "#service",
            "name": service_name,
            "serviceType": service_name,
            "description": page["description"],
            "url": canonical,
            "provider": business_reference,
            "areaServed": {
                "@type": "Place",
                "name": "Cascais and Greater Lisbon",
            },
            "mainEntityOfPage": {
                "@id": page_id,
                "name": page["h1"],
            },
        }
        webpage["mainEntity"] = {
            "@id": service["@id"],
            "name": service_name,
        }
        graph.append(service)

    faq = {
        "@type": "FAQPage",
        "@id": canonical + "#faq",
        "name": f"{page['h1']} FAQ",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item["question"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": plain_text(item["answer_html"]),
                },
            }
            for item in faq_items(page)
        ],
    }
    graph.append(faq)

    breadcrumbs = [
        {
            "@type": "ListItem",
            "position": 1,
            "name": UI[lang]["home"],
            "item": home_url(lang),
        }
    ]
    if config["key"] != "hub":
        breadcrumbs.append(
            {
                "@type": "ListItem",
                "position": 2,
                "name": UI[lang]["hub"],
                "item": canonical_url("harley", lang),
            }
        )
    breadcrumbs.append(
        {
            "@type": "ListItem",
            "position": len(breadcrumbs) + 1,
            "name": page["h1"],
            "item": canonical,
        }
    )
    graph.append(
        {
            "@type": "BreadcrumbList",
            "@id": canonical + "#breadcrumb",
            "name": f"{page['h1']} breadcrumb",
            "itemListElement": breadcrumbs,
        }
    )
    return {"@context": "https://schema.org", "@graph": graph}


def breadcrumb_html(config: dict, page: dict, lang: str) -> str:
    parts = [f'<a href="{localized_href("/", lang)}">{html.escape(UI[lang]["home"])}</a>']
    if config["key"] != "hub":
        parts.extend(
            [
                '<span class="sep">→</span>',
                f'<a href="{localized_href("/harley/", lang)}">{html.escape(UI[lang]["hub"])}</a>',
            ]
        )
    parts.extend(
        [
            '<span class="sep">→</span>',
            f"<span>{html.escape(page['h1'])}</span>",
        ]
    )
    return '<div class="crumb">' + "".join(parts) + "</div>"


def head_html(config: dict, page: dict, lang: str) -> str:
    canonical = canonical_url(config["slug"], lang)
    alternate_links = "\n".join(
        f'<link rel="alternate" hreflang="{HREFLANG_CODES[item_lang]}" href="{canonical_url(config["slug"], item_lang)}"/>'
        for item_lang in LANGS
    )
    alternate_links += (
        f'\n<link rel="alternate" hreflang="x-default" '
        f'href="{canonical_url(config["slug"], "en")}"/>'
    )
    hero_width, hero_height = config["hero_dims"]
    og_width = min(hero_width, 1920)
    og_height = round(hero_height * og_width / hero_width)
    og_image = DOMAIN + optimized_hero_url(config["hero"], 1920, "webp")
    cache_bust = detect_cache_bust()
    schema = json.dumps(schema_graph(config, page, lang), ensure_ascii=False, separators=(",", ":"))
    return f'''<!DOCTYPE html>
<html data-lang="{lang}" lang="{lang}">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1, viewport-fit=cover" name="viewport"/>
<meta content="#0a0a0a" name="theme-color"/>
<meta content="max-image-preview:large" name="robots"/>
<title>{html.escape(page["title"])}</title>
<meta content="{html.escape(page["description"], quote=True)}" name="description"/>
<link href="{canonical}" rel="canonical"/>
{alternate_links}
<meta content="{html.escape(page["title"], quote=True)}" property="og:title"/>
<meta content="{html.escape(page["description"], quote=True)}" property="og:description"/>
<meta content="website" property="og:type"/>
<meta content="{canonical}" property="og:url"/>
<meta content="Iron Custom Motors" property="og:site_name"/>
<meta content="{og_image}" property="og:image"/>
<meta content="{og_width}" property="og:image:width"/>
<meta content="{og_height}" property="og:image:height"/>
<meta content="{html.escape(page["hero_alt"], quote=True)}" property="og:image:alt"/>
<meta content="{OG_LOCALES[lang]}" property="og:locale"/>
<meta content="summary_large_image" name="twitter:card"/>
<meta content="{html.escape(page["title"], quote=True)}" name="twitter:title"/>
<meta content="{html.escape(page["description"], quote=True)}" name="twitter:description"/>
<meta content="{og_image}" name="twitter:image"/>
<link href="/photos/favicon.ico" rel="icon" sizes="any"/>
<link href="/photos/favicon-32.png" rel="icon" sizes="32x32" type="image/png"/>
<link href="/photos/apple-touch-icon.png" rel="apple-touch-icon" sizes="180x180"/>
<link href="/photos/site.webmanifest" rel="manifest"/>
{hero_preload_links(config["hero"])}
<link href="https://fonts.googleapis.com" rel="preconnect"/>
<link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
<link href="https://fonts.googleapis.com/css2?family=Saira:wght@300;400;500;600;700;800;900&amp;family=Saira+Condensed:wght@400;600;700;800;900&amp;family=Roboto+Condensed:wght@400;500;600;700;800;900&amp;family=Inter:wght@300;400;500;600;700&amp;display=swap" rel="stylesheet"/>
<link href="/assets/main.css?v={cache_bust}" rel="stylesheet"/>
<style>{PAGE_CSS}</style>
<script type="application/ld+json">{schema}</script>
<script>window.ICM_I18N_PAGE = {{}};</script>
</head>'''


def render_faq(section: dict) -> str:
    rows = []
    for item in section["faq"]:
        rows.append(
            f'''<details>
<summary>{html.escape(item["question"])}</summary>
<div class="answer">{item["answer_html"]}</div>
</details>'''
        )
    return '<div class="harley-faq">\n' + "\n".join(rows) + "\n</div>"


def render_section(
    config: dict,
    page: dict,
    section: dict,
    section_index: int,
    lang: str,
) -> str:
    section_class = "harley-section"
    if (
        (config["key"] == "hub" and section_index in (0, 1))
        or (
            config["key"] == "custom"
            and any(block["type"] == "portfolio" for block in section["blocks"])
        )
    ):
        section_class += " harley-section-wide"
    if section_index == len(page["sections"]) - 1:
        section_class += " harley-cta"

    content = render_blocks(section["blocks"])
    if section.get("faq"):
        content = render_faq(section)
    elif config["key"] == "hub" and section_index == 0:
        content = render_hub_tiles(section["raw"], lang)
    elif config["key"] == "hub" and section_index == 1:
        content += render_harley_feed(lang)
    elif config["key"] == "custom" and "<!-- PORTFOLIO_SLOT -->" in content:
        content = content.replace("<!-- PORTFOLIO_SLOT -->", render_portfolio(lang))

    return f'''<section class="{section_class}">
<div class="container">
<div class="section-heading"><h2>{html.escape(section["title"])}</h2></div>
<div class="harley-copy">{content}</div>
</div>
</section>'''


def render_page(config: dict, page: dict, lang: str) -> str:
    before, after = chrome_fragments(lang, detect_cache_bust())
    hero = render_picture(
        config["hero"],
        config["hero_dims"],
        page["hero_alt"],
        sizes="100vw",
        eager=True,
        class_name="harley-hero-media",
    )
    intro = ""
    if page["preamble"]:
        intro = f'''<section class="harley-section harley-intro">
<div class="container"><div class="harley-copy">{render_blocks(page["preamble"])}</div></div>
</section>'''
    sections = "\n".join(
        render_section(config, page, section, index, lang)
        for index, section in enumerate(page["sections"])
    )
    main = f'''<main>
<section class="harley-hero">
{hero}
<div aria-hidden="true" class="harley-hero-shade"></div>
<div class="container">
{breadcrumb_html(config, page, lang)}
<h1>{html.escape(page["h1"])}</h1>
</div>
</section>
{intro}
{sections}
</main>'''
    return head_html(config, page, lang) + "\n<body>\n" + before + "\n" + main + "\n" + after + "\n</body>\n</html>\n"


def output_path(slug: str, lang: str) -> Path:
    if lang == "en":
        return SITE_ROOT / slug / "index.html"
    return SITE_ROOT / lang / slug / "index.html"


def main() -> int:
    copy = load_copy()
    generated = []
    for config in PAGE_CONFIG.values():
        for lang in LANGS:
            page = copy[config["key"]][lang]
            target = output_path(config["slug"], lang)
            target.parent.mkdir(parents=True, exist_ok=True)
            write_html_if_changed(
                target,
                render_page(config, page, lang),
                preserve_body_shell=True,
                merge_page_i18n=True,
                preserve_downstream_head=True,
            )
            generated.append(target.relative_to(SITE_ROOT).as_posix())
    print(f"Generated {len(generated)} Harley Hub pages")
    for path in generated:
        print(f"  {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
