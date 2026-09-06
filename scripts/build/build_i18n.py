#!/usr/bin/env python3
"""
Generate language variants of HTML pages for Iron Custom Motors.

Produces /ru/<path>/, /uk/<path>/, /pt/<path>/ for generic English source
pages. Project details are rendered directly in four languages by
build_project_pages.py.

Also adds proper hreflang block to every page.
"""

import json
import re
import shutil
from pathlib import Path
from copy import deepcopy

from bs4 import BeautifulSoup, FeatureNotFound, NavigableString

from build_output import write_html_if_changed
from blog_data import BLOG_POSTS
from brand_pages_data import BRAND_ORDER
from news_data import NEWS_ARTICLES
from localize_internal_links import is_language_switch_link, rewrite_href
from page_meta import PAGE_META, OG_LOCALES
from site_chrome import apply_form_next
from seo_meta import upsert_robots_image_preview

# --------- Paths ---------
SITE_ROOT = Path(__file__).resolve().parents[2]
BUILD_DIR = Path(__file__).resolve().parent
DOMAIN = "https://ironcustommotors.com"
LANGS = ["en", "ru", "uk", "pt"]
HREFLANG_CODES = {"en": "en", "ru": "ru", "uk": "uk", "pt": "pt-PT"}
TARGET_LANGS = ["ru", "uk", "pt"]  # generate these from EN source
LOCALIZED_URL_SKIP_PREFIXES = (
    f"{DOMAIN}/assets/",
    f"{DOMAIN}/photos/",
    f"{DOMAIN}/pricing/files/",
    f"{DOMAIN}/worker/",
)
GLOBAL_SCHEMA_IDS = {
    f"{DOMAIN}/#business",
    f"{DOMAIN}/#website",
    f"{DOMAIN}/#yaroslav-lutytskyi",
}
CUSTOM_LOCALIZED_URLS = {
    f"{DOMAIN}/motorcycle-tyre-service/": {
        "ru": f"{DOMAIN}/ru/shinomontazh-mototsiklov/",
        "uk": f"{DOMAIN}/uk/shynomontazh-mototsykliv/",
        "pt": f"{DOMAIN}/pt/montagem-de-pneus-mota/",
    },
}

try:
    BeautifulSoup("", "lxml")
    HTML_PARSER = "lxml"
except FeatureNotFound:
    HTML_PARSER = "html.parser"

# Pages to translate: (source_path_relative_to_site_root, page_id)
MAIN_PAGES = [
    ("index.html", ""),
    ("parts/index.html", "parts"),
    ("upgrades-tuning/index.html", "upgrades-tuning"),
    ("authorized-dealer/index.html", "authorized-dealer"),
    # motorcycle-service and custom are rendered directly in four languages by
    # build_service_custom_hubs.py from their approved multilingual copy files.
    # pre-purchase-inspection is generated directly in four languages by
    # build_pre_purchase_inspection.py because the page has rich service-page
    # structure, language-specific copy, and structured data.
    # pricing is handled by build_pricing.py (it has its own per-language generator)
    ("services/index.html", "services"),
    ("projects/index.html", "projects"),
    ("about/index.html", "about"),
    ("community/index.html", "community"),
    ("contact/index.html", "contact"),
    ("faq/index.html", "faq"),
    ("thank-you/index.html", "thank-you"),
    *[(f"{slug}/index.html", slug) for slug in BRAND_ORDER],
    ("blog/index.html", "blog"),
    *[
        (f"blog/{slug}/index.html", f"blog/{slug}")
        for slug in BLOG_POSTS
    ],
    ("news/index.html", "news"),
    *[
        (f"news/{slug}/index.html", f"news/{slug}")
        for slug in NEWS_ARTICLES
    ],
]

# --------- Load main I18N ---------
I18N = json.loads((BUILD_DIR / "i18n.json").read_text(encoding="utf-8"))


# --------- Helpers ---------

def make_hreflang_block(soup, page_id, project_name=None):
    """Build hreflang link tags pointing to all 4 language versions of this page."""
    # Path part after lang prefix (no leading slash, trailing slash)
    if project_name:
        path = f"projects/{project_name}/"
    elif page_id == "":
        path = ""
    else:
        path = f"{page_id}/"

    def url_for(lang):
        if lang == "en":
            return f"{DOMAIN}/{path}"
        return f"{DOMAIN}/{lang}/{path}"

    tags = []
    for lang in LANGS:
        tag = soup.new_tag("link")
        tag.attrs["rel"] = "alternate"
        tag.attrs["hreflang"] = HREFLANG_CODES[lang]
        tag.attrs["href"] = url_for(lang)
        tags.append(tag)
    # x-default points to English (default)
    xd = soup.new_tag("link")
    xd.attrs["rel"] = "alternate"
    xd.attrs["hreflang"] = "x-default"
    xd.attrs["href"] = url_for("en")
    tags.append(xd)
    return tags


def parse_html(markup: str) -> BeautifulSoup:
    return BeautifulSoup(markup, HTML_PARSER)


def replace_element_html(el, html_fragment: str):
    """Replace element contents with a translated HTML fragment."""
    fragment_soup = BeautifulSoup(html_fragment, "html.parser")
    container = fragment_soup
    el.clear()
    for child in list(container.children):
        el.append(child)


def normalize_h1_break_spacing(soup):
    """Keep h1 textContent readable when visual line breaks split words."""
    for h1 in soup.find_all("h1"):
        for br in h1.find_all("br"):
            prev = br.previous_sibling
            if prev is None:
                continue
            prev_text = prev.get_text() if hasattr(prev, "get_text") else str(prev)
            if prev_text and not prev_text[-1].isspace():
                br.insert_before(NavigableString(" "))


def localize_schema_url(value: str, lang: str) -> str:
    """Localize site URLs inside JSON-LD while preserving global IDs and assets."""
    if lang == "en" or not isinstance(value, str):
        return value
    if value in GLOBAL_SCHEMA_IDS:
        return value
    if value in CUSTOM_LOCALIZED_URLS:
        return CUSTOM_LOCALIZED_URLS[value].get(lang, value)
    if value == f"{DOMAIN}/#projects":
        return f"{DOMAIN}/{lang}/projects/"
    if value == f"{DOMAIN}/#reviews":
        return f"{DOMAIN}/{lang}/#reviews"
    if value == f"{DOMAIN}/":
        return f"{DOMAIN}/{lang}/"
    if any(value.startswith(prefix) for prefix in LOCALIZED_URL_SKIP_PREFIXES):
        return value
    if value.startswith(f"{DOMAIN}/{lang}/"):
        return value
    if any(value.startswith(f"{DOMAIN}/{other}/") for other in TARGET_LANGS):
        return value
    if value.startswith(f"{DOMAIN}/"):
        return value.replace(f"{DOMAIN}/", f"{DOMAIN}/{lang}/", 1)
    return value


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def schema_type_in(data: dict, schema_type: str) -> bool:
    value = data.get("@type")
    if isinstance(value, str):
        return value == schema_type
    if isinstance(value, list):
        return schema_type in value
    return False


def extract_inline_i18n(soup, lang: str) -> dict:
    """Read the per-page inline ICM_I18N_PAGE dictionary for one language."""
    for script in soup.find_all("script"):
        txt = script.string or ""
        m = re.search(r"window\.ICM_I18N_PAGE\s*=\s*(\{.*?\});", txt, re.DOTALL)
        if m:
            try:
                page_i18n = json.loads(m.group(1))
                return page_i18n.get(lang, {})
            except json.JSONDecodeError:
                return {}
    return {}


def sync_variable_faq_items(soup, translations: dict):
    """Add localized FAQ rows when a language has more questions than English."""
    faq_list = soup.select_one(".faq-list")
    if faq_list is None:
        return

    templates = faq_list.find_all("details", class_="faq-item", recursive=False)
    if not templates:
        return

    existing_indexes = set()
    for item in templates:
        question = item.find(class_="q")
        match = re.fullmatch(r"fq\.q(\d+)", question.get("data-i18n", "")) if question else None
        if match:
            existing_indexes.add(int(match.group(1)))

    desired_indexes = []
    for key in translations:
        match = re.fullmatch(r"fq\.q(\d+)", key)
        if match and f"fq.a{match.group(1)}" in translations:
            desired_indexes.append(int(match.group(1)))

    for index in sorted(desired_indexes):
        if index in existing_indexes:
            continue
        item = deepcopy(templates[-1])
        number = item.find(class_="num")
        question = item.find(class_="q")
        answer = item.find(class_="a")
        if number:
            number.string = f"{index:02d}"
        if question:
            question["data-i18n"] = f"fq.q{index}"
        if answer:
            answer["data-i18n"] = f"fq.a{index}"
        faq_list.append(item)


def translation_dict_for_soup(soup, lang: str) -> dict:
    page_dict = I18N.get(lang, {})
    extra_dict = extract_inline_i18n(soup, lang)
    return {**page_dict, **extra_dict}


def apply_translations(soup, lang: str) -> dict:
    """Apply data-i18n/data-i18n-html translations and return the merged dictionary."""
    full_dict = translation_dict_for_soup(soup, lang)

    for el in soup.find_all(attrs={"data-i18n": True}):
        key = el["data-i18n"]
        if key in full_dict:
            replace_element_html(el, full_dict[key])

    for el in soup.find_all(attrs={"data-i18n-html": True}):
        key = el["data-i18n-html"]
        if key in full_dict:
            replace_element_html(el, full_dict[key])

    for el in soup.find_all(attrs={"data-i18n-alt": True}):
        key = el["data-i18n-alt"]
        if key in full_dict:
            el["alt"] = full_dict[key]

    for el in soup.find_all(attrs={"data-i18n-title": True}):
        key = el["data-i18n-title"]
        if key in full_dict:
            el["title"] = full_dict[key]

    for el in soup.find_all(attrs={"data-i18n-aria-label": True}):
        key = el["data-i18n-aria-label"]
        if key in full_dict:
            el["aria-label"] = BeautifulSoup(full_dict[key], "html.parser").get_text(" ", strip=True)

    for attr, prefix in (
        ("data-i18n-proj-label", "proj.label"),
        ("data-i18n-proj-tag", "proj.tag"),
    ):
        for el in soup.find_all(attrs={attr: True}):
            key = f"{prefix}.{el[attr]}"
            if key in full_dict:
                replace_element_html(el, full_dict[key])

    return full_dict


def extract_breadcrumb_names(soup) -> list[str]:
    crumb = soup.find(class_="crumb")
    if crumb is None:
        return []
    names = []
    for child in crumb.find_all(["a", "span"], recursive=False):
        if "sep" in child.get("class", []):
            continue
        text = clean_text(child.get_text(" ", strip=True))
        if text:
            names.append(text)
    return names


def extract_faq_entities(soup) -> list[dict]:
    """Build FAQPage entities from the visible, already translated FAQ blocks."""
    entities = []
    seen = set()

    def add_pair(q_el, a_el):
        if q_el is None or a_el is None:
            return
        question = clean_text(q_el.get_text(" ", strip=True))
        answer = clean_text(a_el.get_text(" ", strip=True))
        key = (question, answer)
        if not question or not answer or key in seen:
            return
        seen.add(key)
        entities.append({
            "@type": "Question",
            "name": question,
            "acceptedAnswer": {"@type": "Answer", "text": answer},
        })

    for details in soup.find_all("details"):
        if "mobile-nav-group" in details.get("class", []):
            continue
        add_pair(
            details.find(class_="q") or details.find("summary"),
            details.find(class_="a") or details.find("p"),
        )

    for item in soup.select(".faq-item"):
        q_el = item.select_one(".faq-q [data-i18n], .faq-q span, .q")
        a_el = item.select_one(".faq-a p, .a")
        add_pair(q_el, a_el)

    return entities


def page_jsonld_context(soup, canonical_url: str, lang: str) -> dict:
    title = clean_text(soup.title.get_text(" ", strip=True)) if soup.title else ""
    description_el = soup.head.find("meta", attrs={"name": "description"}) if soup.head else None
    h1 = soup.find("h1")
    video_title = soup.select_one(".blog-video h2, .blog-video-section h2")
    video_description = soup.select_one(".blog-video p, .blog-video-section p")
    video_schema_name = ""
    video_schema_description = ""
    video_element = soup.select_one(".blog-video video, .blog-video-section video")
    if video_element:
        title_key = video_element.get("data-i18n-title", "")
        if title_key.endswith(".videoTitle"):
            key_prefix = title_key[:-len(".videoTitle")]
            translations = translation_dict_for_soup(soup, lang)
            video_schema_name = translations.get(f"{key_prefix}.videoSchemaName", "")
            video_schema_description = translations.get(f"{key_prefix}.videoSchemaDescription", "")
    return {
        "canonical_url": canonical_url,
        "lang": lang,
        "title": title,
        "description": description_el.get("content", "") if description_el else "",
        "h1": clean_text(h1.get_text(" ", strip=True)) if h1 else "",
        "video_title": video_schema_name or (
            clean_text(video_title.get_text(" ", strip=True)) if video_title else ""
        ),
        "video_description": video_schema_description or (
            clean_text(video_description.get_text(" ", strip=True)) if video_description else ""
        ),
        "breadcrumbs": extract_breadcrumb_names(soup),
        "faq_entities": extract_faq_entities(soup),
    }


def is_current_page_entity(data: dict, canonical_url: str) -> bool:
    if data.get("@id") == canonical_url or data.get("url") == canonical_url:
        return True
    main_entity = data.get("mainEntityOfPage")
    return isinstance(main_entity, dict) and main_entity.get("@id") == canonical_url


def enhance_jsonld_value(value, context: dict):
    if isinstance(value, list):
        return [enhance_jsonld_value(item, context) for item in value]
    if not isinstance(value, dict):
        return value

    data = {key: enhance_jsonld_value(val, context) for key, val in value.items()}

    if schema_type_in(data, "FAQPage") and context["faq_entities"]:
        data["mainEntity"] = context["faq_entities"]

    if schema_type_in(data, "BreadcrumbList") and context["breadcrumbs"]:
        items = data.get("itemListElement")
        if isinstance(items, list):
            for idx, item in enumerate(items):
                if isinstance(item, dict) and idx < len(context["breadcrumbs"]):
                    item["name"] = context["breadcrumbs"][idx]

    if schema_type_in(data, "VideoObject"):
        if context["video_title"]:
            data["name"] = context["video_title"]
        if context["video_description"] and "description" in data:
            data["description"] = context["video_description"]
        if "inLanguage" in data:
            data["inLanguage"] = context["lang"]

    if is_current_page_entity(data, context["canonical_url"]):
        if "inLanguage" in data:
            data["inLanguage"] = context["lang"]
        if schema_type_in(data, "NewsArticle") or schema_type_in(data, "BlogPosting") or schema_type_in(data, "Article") or schema_type_in(data, "TechArticle"):
            data["headline"] = context["h1"] or context["title"]
            if context["description"]:
                data["description"] = context["description"]
        elif schema_type_in(data, "Service") or schema_type_in(data, "CollectionPage") or schema_type_in(data, "WebPage") or schema_type_in(data, "AboutPage") or schema_type_in(data, "ContactPage") or schema_type_in(data, "CreativeWork"):
            if context["h1"]:
                data["name"] = context["h1"]
            if context["description"] and "description" in data:
                data["description"] = context["description"]
        elif schema_type_in(data, "Blog") or schema_type_in(data, "FAQPage"):
            if context["title"]:
                data["name"] = context["title"]
            if context["description"] and "description" in data:
                data["description"] = context["description"]

    return data


def localize_jsonld_value(value, lang: str):
    if isinstance(value, dict):
        return {key: localize_jsonld_value(val, lang) for key, val in value.items()}
    if isinstance(value, list):
        return [localize_jsonld_value(item, lang) for item in value]
    if isinstance(value, str):
        return localize_schema_url(value, lang)
    return value


def localize_jsonld_blocks(soup, lang: str, canonical_url: str):
    """Update JSON-LD URLs and visible page text for the current language."""
    context = page_jsonld_context(soup, canonical_url, lang)
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        raw = script.string or script.get_text()
        if not raw.strip():
            continue
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        localized = localize_jsonld_value(data, lang)
        enhanced = enhance_jsonld_value(localized, context)
        script.string = json.dumps(enhanced, ensure_ascii=False, separators=(",", ":"))


def absolutize_paths(soup):
    """Convert relative paths (../foo, ./foo) in head links/scripts to absolute /foo.
    Required so a page at /ru/motorcycle-service/ correctly resolves /photos, /assets."""
    for tag_name, attr in [("link", "href"), ("script", "src"), ("img", "src")]:
        for el in soup.find_all(tag_name):
            v = el.get(attr)
            if not v:
                continue
            if v.startswith(("../", "./")):
                # Replace leading ../ or ./ with /
                stripped = re.sub(r"^(\.\./)+|^\./", "", v)
                el[attr] = "/" + stripped


def replace_hreflang_block(soup, tags):
    """Replace hreflang links without moving their maintained head position."""
    existing = soup.head.find_all(
        "link",
        attrs={"rel": "alternate", "hreflang": True},
    )
    if existing:
        anchor = existing[0]
        for tag in tags:
            anchor.insert_before(tag)
        for element in existing:
            element.decompose()
        return
    for tag in tags:
        soup.head.append(tag)


def upsert_meta(soup, *, prop=None, name=None, content):
    """Find <meta property=... or name=...> and update its content, or create."""
    sel = {}
    if prop is not None:
        sel = {"property": prop}
    elif name is not None:
        sel = {"name": name}
    el = soup.head.find("meta", attrs=sel)
    if el is None:
        el = soup.new_tag("meta")
        if prop is not None:
            el.attrs["property"] = prop
        if name is not None:
            el.attrs["name"] = name
        soup.head.append(el)
    el.attrs["content"] = content


def localize_page(en_html: str, lang: str, page_id: str, *, project_name=None) -> str:
    """Take English HTML, produce a fully translated version for `lang`."""
    soup = parse_html(en_html)

    # 1. html lang attribute
    html = soup.find("html")
    if html is not None:
        html["lang"] = lang
        html["data-lang"] = lang

    # 2. Absolutize relative paths so the page works at /lang/path/
    absolutize_paths(soup)

    # 3. Translate elements with data-i18n / data-i18n-html
    extra_dict = extract_inline_i18n(soup, lang)
    sync_variable_faq_items(soup, extra_dict)
    apply_translations(soup, lang)

    # 4. Update title / description / OG / Twitter / canonical
    meta = PAGE_META.get(page_id, {}).get(lang, {})
    base_path = "" if page_id == "" else f"{page_id}/"
    if project_name:
        base_path = f"projects/{project_name}/"

    canonical_url = f"{DOMAIN}/{lang}/{base_path}" if lang != "en" else f"{DOMAIN}/{base_path}"

    # Title
    if "title" in meta:
        title_el = soup.title
        if title_el is None:
            title_el = soup.new_tag("title")
            soup.head.append(title_el)
        title_el.string = meta["title"]
    elif project_name:
        # Build title from project badge translation
        badge = extra_dict.get(f"proj.{project_name.replace('-', '_').replace('_', '-')}.badge", "")
        # Try both dash-form and underscore-form keys
        if not badge:
            badge_key = f"proj.{project_name}.badge"
            badge = extra_dict.get(badge_key, "")
        name = extra_dict.get(f"proj.{project_name}.name", project_name.title())
        if badge:
            title_text = f"{name} — {badge} | Iron Custom Motors"
        else:
            title_text = f"{name} | Iron Custom Motors"
        title_el = soup.title
        if title_el is None:
            title_el = soup.new_tag("title")
            soup.head.append(title_el)
        title_el.string = title_text
        meta = {"title": title_text}

    description = meta.get("description")
    if project_name and not description:
        # Use project tag translation as description
        description = extra_dict.get(f"proj.{project_name}.tag", "")
        # Pad to 140-160 chars with a localized brand tail for SEO
        BRAND_TAIL = {
            "en": "Custom build by Iron Custom Motors — Cascais workshop, Greater Lisbon.",
            "ru": "Кастом-сборка Iron Custom Motors — мастерская в Кашкайше, Большой Лиссабон.",
            "uk": "Кастом-збірка Iron Custom Motors — майстерня у Кашкайші, Великий Лісабон.",
            "pt": "Build custom da Iron Custom Motors — oficina em Cascais, Grande Lisboa.",
        }
        if description and len(description) < 140:
            tail = BRAND_TAIL.get(lang, BRAND_TAIL["en"])
            # Ensure tag ends with punctuation before concatenating
            sep = "" if description.endswith((".","!","?")) else "."
            description = f"{description}{sep} {tail}"
    if description:
        upsert_meta(soup, name="description", content=description)

    # OG
    og_title = meta.get("title", "")
    if og_title:
        upsert_meta(soup, prop="og:title", content=og_title)
    og_desc = meta.get("og_description") or description
    if og_desc:
        upsert_meta(soup, prop="og:description", content=og_desc)
    upsert_meta(soup, prop="og:url", content=canonical_url)
    upsert_meta(soup, prop="og:locale", content=OG_LOCALES[lang])

    # Twitter
    tw_title = meta.get("title", "")
    if tw_title:
        upsert_meta(soup, name="twitter:title", content=tw_title)
    tw_desc = meta.get("twitter_description") or og_desc or description
    if tw_desc:
        upsert_meta(soup, name="twitter:description", content=tw_desc)

    # Canonical
    can_el = soup.head.find("link", attrs={"rel": "canonical"})
    if can_el is None:
        can_el = soup.new_tag("link")
        can_el.attrs["rel"] = "canonical"
        soup.head.append(can_el)
    can_el["href"] = canonical_url

    # 5. Replace hreflang block
    replace_hreflang_block(soup, make_hreflang_block(soup, page_id, project_name))

    # 6. Localize JSON-LD URLs and visible text so structured data matches the page.
    localize_jsonld_blocks(soup, lang, canonical_url)

    # 7. Make h1 textContent readable for crawlers and assistive tech.
    normalize_h1_break_spacing(soup)

    # 8. Optional: update og:locale:alternate entries for English locale
    # (kept on home page only — handled via upsert above)
    upsert_robots_image_preview(soup)

    for anchor in soup.find_all("a", href=True):
        if not is_language_switch_link(anchor):
            anchor["href"] = rewrite_href(anchor["href"], lang)

    apply_form_next(soup, lang)

    return str(soup)


def update_en_page(en_html: str, page_id: str, project_name=None) -> str:
    """For English source page: sync visible copy, hreflang and JSON-LD."""
    soup = parse_html(en_html)
    apply_translations(soup, "en")
    replace_hreflang_block(soup, make_hreflang_block(soup, page_id, project_name))
    base_path = "" if page_id == "" else f"{page_id}/"
    if project_name:
        base_path = f"projects/{project_name}/"
    canonical_url = f"{DOMAIN}/{base_path}"
    localize_jsonld_blocks(soup, "en", canonical_url)
    normalize_h1_break_spacing(soup)
    # Also ensure og:locale:alternate covers all langs (for home page)
    if page_id == "" and project_name is None:
        # Remove existing alternates and add fresh
        for el in soup.head.find_all("meta", attrs={"property": "og:locale:alternate"}):
            el.decompose()
        for lang in ["ru", "uk", "pt"]:
            t = soup.new_tag("meta")
            t.attrs["property"] = "og:locale:alternate"
            t.attrs["content"] = OG_LOCALES[lang]
            soup.head.append(t)
    upsert_robots_image_preview(soup)
    apply_form_next(soup, "en")
    return str(soup)


def write_localized(out_path: Path, content: str):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    write_html_if_changed(out_path, content, preserve_body_shell=True)


# --------- Main run ---------

def main():
    output_pairs = []  # (target_path, content)

    all_pages = MAIN_PAGES

    for source_rel, page_id in all_pages:
        src = SITE_ROOT / source_rel
        if not src.exists():
            print(f"SKIP (missing): {source_rel}")
            continue

        en_html = src.read_text(encoding="utf-8")
        project_name = None

        # Localized versions
        for lang in TARGET_LANGS:
            translated = localize_page(en_html, lang, page_id, project_name=project_name)
            # Path: <lang>/<page>/index.html ; for home it's <lang>/index.html
            if page_id == "":
                out = SITE_ROOT / lang / "index.html"
            else:
                out = SITE_ROOT / lang / page_id / "index.html"
            output_pairs.append((out, translated))

        # Update English source: hreflang block
        updated_en = update_en_page(en_html, page_id, project_name=project_name)
        output_pairs.append((src, updated_en))

    # Write everything
    for path, content in output_pairs:
        path.parent.mkdir(parents=True, exist_ok=True)
        write_html_if_changed(path, content, preserve_body_shell=True)
        rel = path.relative_to(SITE_ROOT)
        print(f"wrote {rel}  ({len(content):,} bytes)")

    print(f"\n--- Done. Wrote {len(output_pairs)} files. ---")


if __name__ == "__main__":
    main()
