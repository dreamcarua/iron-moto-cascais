#!/usr/bin/env python3
"""Build every multilingual project page and legacy redirect from source data."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup
from PIL import Image

from build_output import write_html_if_changed, write_text_if_changed
from page_meta import OG_LOCALES
from project_pages_data import (
    PROJECT_CONFIGS,
    REDIRECT_CONFIGS,
    load_project,
    project_modified_iso,
)
from site_chrome import apply_global_i18n, patch_navigation_footer


SITE_ROOT = Path(__file__).resolve().parents[2]
DOMAIN = "https://ironcustommotors.com"
TEMPLATE_PATH = SITE_ROOT / "projects/joker/index.html"
LANGS = ["en", "ru", "uk", "pt"]
HREFLANG_CODES = {"en": "en", "ru": "ru", "uk": "uk", "pt": "pt-PT"}
CACHE_BUST = {
    "/assets/main.css": "20260906a",
    "/assets/main.js": "20260906a",
    "/assets/projects.css": "20260801a",
    "/assets/projects.js": "20260710b",
}

MARKDOWN_PROJECT_STYLE = """
.subpage picture.bg{position:absolute;inset:0;z-index:-1;display:block;filter:none;transform:none}
.subpage picture.bg img{width:100%;height:100%;object-fit:cover;object-position:center;filter:saturate(.85) contrast(1.05) brightness(.45)}
.generated-project-story{max-width:900px}
.generated-project-story h2{font-family:var(--font-display);font-size:clamp(26px,3vw,40px);font-weight:800;line-height:1.05;text-transform:uppercase;color:#fff;margin:44px 0 18px}
.generated-project-story h2:first-child{margin-top:0}
.generated-project-closing .lead{max-width:900px}
.generated-project-closing .lead p{margin:0;color:var(--text);font-size:clamp(17px,1.6vw,21px);line-height:1.65}
.generated-project-closing .lead a{color:var(--accent)}
.proj-gallery picture{display:block;width:100%;height:100%}
"""


def upsert_meta(
    soup: BeautifulSoup,
    *,
    name: str | None = None,
    prop: str | None = None,
    content: str,
) -> None:
    attrs = {"name": name} if name else {"property": prop}
    tag = soup.head.find("meta", attrs=attrs)
    if tag is None:
        tag = soup.new_tag("meta")
        tag.attrs.update(attrs)
        soup.head.append(tag)
    tag["content"] = content


def apply_cache_bust(soup: BeautifulSoup) -> None:
    found = set()
    for tag in soup.find_all(["link", "script"]):
        attr = "href" if tag.name == "link" else "src"
        ref = tag.get(attr, "")
        path = ref.split("?", 1)[0]
        if path not in CACHE_BUST:
            continue
        tag[attr] = f"{path}?v={CACHE_BUST[path]}"
        found.add(path)

    missing = set(CACHE_BUST) - found
    if missing:
        raise ValueError(f"Project template is missing cache-busted assets: {sorted(missing)}")


def image_dimensions(path: str) -> tuple[int, int]:
    with Image.open(SITE_ROOT / path.lstrip("/")) as image:
        return image.size


def localized_path(slug: str, lang: str) -> str:
    prefix = "" if lang == "en" else f"{lang}/"
    return f"{prefix}projects/{slug}/"


def page_url(slug: str, lang: str) -> str:
    return f"{DOMAIN}/{localized_path(slug, lang)}"


def replace_hreflangs(soup: BeautifulSoup, slug: str) -> None:
    for alternate in soup.head.find_all(
        "link", attrs={"rel": "alternate", "hreflang": True}
    ):
        alternate.decompose()

    anchor = soup.head.find("link", attrs={"rel": "canonical"})
    for lang in LANGS:
        alternate = soup.new_tag("link")
        alternate["rel"] = "alternate"
        alternate["hreflang"] = HREFLANG_CODES[lang]
        alternate["href"] = page_url(slug, lang)
        anchor.insert_after(alternate)
        anchor = alternate
    x_default = soup.new_tag("link")
    x_default["rel"] = "alternate"
    x_default["hreflang"] = "x-default"
    x_default["href"] = page_url(slug, "en")
    anchor.insert_after(x_default)


def picture_html(
    base: str,
    widths: list[int],
    *,
    alt: str,
    hero: bool = False,
    sizes: str | None = None,
) -> str:
    candidates = []
    for width in widths:
        dimensions = image_dimensions(f"{base}-{width}.webp")
        candidates.append((width, dimensions))
    largest_width, (largest_w, largest_h) = candidates[-1]
    srcset_avif = ", ".join(f"{base}-{width}.avif {width}w" for width, _ in candidates)
    srcset_webp = ", ".join(f"{base}-{width}.webp {width}w" for width, _ in candidates)
    has_jpeg_fallback = all(
        (SITE_ROOT / f"{base.lstrip('/')}-{width}.jpg").exists()
        for width, _ in candidates
    )
    fallback_extension = "jpg" if has_jpeg_fallback else "webp"
    fallback_srcset = ", ".join(
        f"{base}-{width}.{fallback_extension} {width}w" for width, _ in candidates
    )
    sizes = sizes or ("100vw" if hero else "(max-width:760px) 50vw, 25vw")
    picture_class = ' class="bg"' if hero else ""
    image_attrs = (
        ' decoding="async" fetchpriority="high"'
        if hero
        else ' decoding="async" loading="lazy"'
    )
    return f'''<picture{picture_class}>
<source srcset="{srcset_avif}" sizes="{sizes}" type="image/avif"/>
<source srcset="{srcset_webp}" sizes="{sizes}" type="image/webp"/>
<img alt="{html.escape(alt, quote=True)}"{image_attrs} height="{largest_h}" sizes="{sizes}" src="{base}-{largest_width}.{fallback_extension}" srcset="{fallback_srcset}" width="{largest_w}"/>
</picture>'''


def apply_exhibition_media(project: dict, lang: str, main) -> None:
    media = project.get("exhibition_media")
    sections = main.select('[data-project-exhibition="true"]')
    if media is None:
        if sections:
            raise ValueError(
                f"Project {project['slug']} {lang} has exhibition markup without media data"
            )
        return
    if len(sections) != 1:
        raise ValueError(
            f"Project {project['slug']} {lang} must have exactly one exhibition section"
        )

    story = sections[0].select_one(".container > .proj-story")
    if story is None:
        raise ValueError(f"Project {project['slug']} {lang} exhibition story is missing")
    picture = picture_html(
        media["base"],
        media["widths"],
        alt=media["alts"][lang],
        sizes="(max-width: 900px) calc(100vw - 40px), 42vw",
    )
    wrapper = BeautifulSoup(
        f'''<div class="project-exhibition-split">
<figure class="project-exhibition-media">{picture}</figure>
{story}
</div>''',
        "html.parser",
    ).div
    story.replace_with(wrapper)


def render_markdown_project_main(project: dict, lang: str) -> str:
    slug = project["slug"]
    content = project["content"][lang]
    ui = project["ui"][lang]
    prefix = "" if lang == "en" else f"/{lang}"
    hero = picture_html(
        project["hero_base"],
        [800, 1600, 2400],
        alt=content["hero_alt"],
        hero=True,
    )
    gallery = []
    for index, alt in enumerate(project["gallery_alts"][lang], start=1):
        image = picture_html(
            f"{project['gallery_base']}-{index:02d}",
            [800, 1600],
            alt=alt,
        )
        gallery.append(f'<div class="gtile">{image}</div>')

    return f'''<main>
<section class="subpage">
{hero}
<div class="container">
<div class="crumb"><a href="{prefix}/">{ui["home"]}</a><span class="sep">→</span><a href="{prefix}/projects/">{ui["projects"]}</a><span class="sep">→</span><span>{content["h1"]}</span></div>
<span class="proj-badge">{ui["badge"]}</span>
<h1 class="reveal">{content["h1"]}</h1>
<p class="tagline reveal"><em>{content["subtitle"]}</em></p>
<div class="proj-meta">
<div class="item"><span class="label">{ui["year_label"]}</span><span class="val">{project["year"]}</span></div>
<div class="item"><span class="label">{ui["category_label"]}</span><span class="val">{ui["category"]}</span></div>
<div class="item"><span class="label">{ui["where_label"]}</span><span class="val">{ui["where"]}</span></div>
</div>
</div>
</section>
<section class="sub-section">
<div class="container">
<article class="proj-story generated-project-story reveal">{content["body_html"]}</article>
</div>
</section>
<section class="sub-section">
<div class="container">
<div class="heading reveal">
<span class="h-eyebrow">{ui["gallery"]}</span>
<div><h2>{ui["gallery_title"]}</h2></div>
</div>
<div class="proj-gallery reveal-stagger">
{"".join(gallery)}
</div>
</div>
</section>
<section class="cta-back generated-project-closing">
<div class="container">
<div class="lead">{content["closing_html"]}</div>
</div>
</section>
</main>'''


def project_main(project: dict, lang: str) -> BeautifulSoup:
    if project["source_format"] == "localized_html":
        markup = project["content"][lang]["main_html"]
    else:
        markup = render_markdown_project_main(project, lang)
    fragment = BeautifulSoup(markup, "html.parser")
    if fragment.main is None:
        raise ValueError(f"Project {project['slug']} {lang} source has no main element")
    apply_exhibition_media(project, lang, fragment.main)
    return fragment.main


def project_meta(project: dict, lang: str, main) -> dict:
    content = project["content"][lang]
    if project["source_format"] == "localized_html":
        return content

    image_url = f"{DOMAIN}{project['hero_base']}-2400.webp"
    return {
        "title": content["title"],
        "description": content["description"],
        "og_title": content["title"],
        "og_description": content["description"],
        "og_image": image_url,
        "twitter_title": content["title"],
        "twitter_description": content["description"],
        "twitter_image": image_url,
        "h1": content["h1"],
        "breadcrumb_names": [
            project["ui"][lang]["home"],
            project["ui"][lang]["projects"],
            content["h1"],
        ],
    }


def hero_details(main) -> dict:
    hero = main.select_one(".subpage picture.bg img")
    avif = main.select_one('.subpage picture.bg source[type="image/avif"]')
    if hero is None or avif is None:
        raise ValueError("Project hero picture is incomplete")
    return {
        "src": hero.get("src", ""),
        "width": int(hero.get("width", 0)),
        "height": int(hero.get("height", 0)),
        "avif_srcset": avif.get("srcset", ""),
        "sizes": avif.get("sizes", "100vw"),
    }


def responsive_preload(soup: BeautifulSoup, details: dict) -> None:
    for preload in soup.head.find_all("link", attrs={"rel": "preload", "as": "image"}):
        preload.decompose()
    candidates = [part.strip().rsplit(" ", 1)[0] for part in details["avif_srcset"].split(",")]
    if not candidates:
        raise ValueError("Project hero has no AVIF preload candidate")
    href = candidates[len(candidates) // 2]
    preload = soup.new_tag("link")
    preload["rel"] = "preload"
    preload["as"] = "image"
    preload["href"] = href
    preload["type"] = "image/avif"
    preload["imagesrcset"] = details["avif_srcset"]
    preload["imagesizes"] = details["sizes"]
    first_stylesheet = soup.head.find("link", attrs={"rel": "stylesheet"})
    if first_stylesheet:
        first_stylesheet.insert_before(preload)
    else:
        soup.head.append(preload)


def faq_entities(main) -> list[dict]:
    entities = []
    for details in main.find_all("details"):
        question = details.find("summary")
        answer = details.find("p")
        if question and answer:
            entities.append(
                {
                    "@type": "Question",
                    "name": " ".join(question.get_text(" ", strip=True).split()),
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": " ".join(answer.get_text(" ", strip=True).split()),
                    },
                }
            )
    return entities


def schema_graph(project: dict, lang: str, meta: dict, main, hero: dict) -> dict:
    slug = project["slug"]
    current_url = page_url(slug, lang)
    image_url = f"{DOMAIN}{hero['src']}"
    breadcrumbs = meta["breadcrumb_names"]
    prefix = "" if lang == "en" else f"{lang}/"
    graph = [
        {
            "@type": "Article",
            "@id": f"{current_url}#article",
            "headline": meta["h1"],
            "description": meta["description"],
            "image": {"@id": f"{current_url}#primaryimage"},
            "datePublished": project["published_iso"],
            "dateModified": project_modified_iso(project, lang),
            "inLanguage": lang,
            "author": {"@id": f"{DOMAIN}/#business"},
            "publisher": {"@id": f"{DOMAIN}/#business"},
            "mainEntityOfPage": {"@id": current_url},
        },
        {
            "@type": "WebPage",
            "@id": current_url,
            "url": current_url,
            "name": meta["h1"],
            "description": meta["description"],
            "inLanguage": lang,
            "isPartOf": {"@id": f"{DOMAIN}/#website"},
            "primaryImageOfPage": {"@id": f"{current_url}#primaryimage"},
        },
        {
            "@type": "ImageObject",
            "@id": f"{current_url}#primaryimage",
            "url": image_url,
            "contentUrl": image_url,
            "width": hero["width"],
            "height": hero["height"],
        },
        {
            "@type": "LocalBusiness",
            "@id": f"{DOMAIN}/#business",
            "name": "Iron Custom Motors",
            "url": f"{DOMAIN}/{prefix}",
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
            "logo": {
                "@type": "ImageObject",
                "url": f"{DOMAIN}/photos/icon-512.png",
                "width": 512,
                "height": 512,
            },
        },
        {
            "@type": "BreadcrumbList",
            "@id": f"{current_url}#breadcrumb",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": breadcrumbs[0],
                    "item": f"{DOMAIN}/{prefix}",
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": breadcrumbs[1],
                    "item": f"{DOMAIN}/{prefix}projects/",
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": breadcrumbs[2],
                    "item": current_url,
                },
            ],
        },
    ]
    questions = faq_entities(main)
    if questions:
        graph.append(
            {
                "@type": "FAQPage",
                "@id": f"{current_url}#faq",
                "mainEntity": questions,
            }
        )
    return {"@context": "https://schema.org", "@graph": graph}


def remove_inline_project_i18n(soup: BeautifulSoup) -> None:
    for script in soup.find_all("script"):
        if "window.ICM_I18N_PAGE" in (script.string or ""):
            script.decompose()


def render_project(project: dict, lang: str, template_markup: str) -> Path:
    slug = project["slug"]
    soup = BeautifulSoup(template_markup, "html.parser")
    apply_cache_bust(soup)
    soup.html["lang"] = lang
    soup.html["data-lang"] = lang
    apply_global_i18n(soup, lang)

    main = project_main(project, lang)
    meta = project_meta(project, lang, main)
    hero = hero_details(main)
    for high in main.select('[fetchpriority="high"]'):
        del high["fetchpriority"]
    hero_img = main.select_one(".subpage picture.bg img")
    hero_img["fetchpriority"] = "high"
    hero_img.attrs.pop("loading", None)

    soup.main.replace_with(main)
    soup.title.string = meta["title"]
    upsert_meta(soup, name="description", content=meta["description"])
    upsert_meta(soup, prop="og:title", content=meta["og_title"])
    upsert_meta(soup, prop="og:description", content=meta["og_description"])
    upsert_meta(soup, prop="og:type", content="article")
    upsert_meta(soup, prop="og:url", content=page_url(slug, lang))
    upsert_meta(soup, prop="og:image", content=meta["og_image"])
    upsert_meta(soup, prop="og:locale", content=OG_LOCALES[lang])
    upsert_meta(soup, name="twitter:title", content=meta["twitter_title"])
    upsert_meta(soup, name="twitter:description", content=meta["twitter_description"])
    upsert_meta(soup, name="twitter:image", content=meta["twitter_image"])
    canonical = soup.head.find("link", attrs={"rel": "canonical"})
    canonical["href"] = page_url(slug, lang)
    replace_hreflangs(soup, slug)
    responsive_preload(soup, hero)

    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        script.decompose()
    schema = soup.new_tag("script")
    schema["type"] = "application/ld+json"
    schema.string = json.dumps(
        schema_graph(project, lang, meta, main, hero),
        ensure_ascii=False,
        separators=(",", ":"),
    )
    soup.head.append(schema)
    remove_inline_project_i18n(soup)

    if project["source_format"] == "markdown":
        style = soup.head.find("style")
        if "generated-project-story" not in (style.string or ""):
            style.string = (style.string or "") + MARKDOWN_PROJECT_STYLE

    output = SITE_ROOT / localized_path(slug, lang) / "index.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    generated = patch_navigation_footer(str(soup), lang)
    write_html_if_changed(output, generated)
    print(f"wrote {output.relative_to(SITE_ROOT)}")
    return output


def render_redirects() -> None:
    for old_slug, config in REDIRECT_CONFIGS.items():
        for lang in LANGS:
            prefix = "" if lang == "en" else f"/{lang}"
            target_path = f"{prefix}/projects/{config['target']}/"
            target_url = f"{DOMAIN}{target_path}"
            labels = config["labels"][lang]
            markup = f'''<!DOCTYPE html>

<html lang="{lang}">
<head>
<meta charset="utf-8"/>
<title>{labels["title"]}</title>
<link href="{target_url}" rel="canonical"/>
<meta content="0; url={target_path}" http-equiv="refresh"/>
<meta content="noindex, follow, max-image-preview:large" name="robots"/>
<script>window.location.replace("{target_path}");</script>
</head>
<body>
<p>{labels["message"]} <a href="{target_path}">{labels["target_name"]}</a>&hellip;</p>
</body>
</html>'''
            relative = Path("projects") / old_slug / "index.html"
            if lang != "en":
                relative = Path(lang) / relative
            output = SITE_ROOT / relative
            output.parent.mkdir(parents=True, exist_ok=True)
            write_text_if_changed(output, markup)
            print(f"wrote {relative}")


def main() -> None:
    template_markup = TEMPLATE_PATH.read_text(encoding="utf-8")
    for slug in PROJECT_CONFIGS:
        project = load_project(slug)
        if project["source_format"] == "markdown" and len(project["gallery_sources"]) != len(
            project["gallery_alts"]["en"]
        ):
            raise ValueError(f"Gallery source/alt count mismatch for {slug}")
        for lang in LANGS:
            render_project(project, lang, template_markup)
    render_redirects()
    print(
        f"Done. Wrote {len(PROJECT_CONFIGS) * len(LANGS)} project pages and "
        f"{len(REDIRECT_CONFIGS) * len(LANGS)} redirects."
    )


if __name__ == "__main__":
    main()
