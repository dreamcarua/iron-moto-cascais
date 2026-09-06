#!/usr/bin/env python3
"""Generate sitemap.xml with all language versions and xhtml:link alternates.

Sitemap lastmod values must be stable content dates, not build dates. Blog and
news articles use their registered publish/modified dates. Other pages use the
last Git commit whose served HTML changed semantically, ignoring shared chrome
and generated boilerplate that should not trigger crawler recrawl priority.
"""

from __future__ import annotations

from datetime import datetime, time
import re
import subprocess
from pathlib import Path
from functools import lru_cache
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape as xml_escape

from bs4 import BeautifulSoup, FeatureNotFound, NavigableString

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover - Python < 3.9 fallback
    ZoneInfo = None

from brand_pages_data import BRAND_ORDER
from blog_data import BLOG_POSTS
from news_data import NEWS_ARTICLES
from project_pages_data import PROJECT_CONFIGS, project_modified_iso

DOMAIN = "https://ironcustommotors.com"
SITE_ROOT = Path(__file__).resolve().parents[2]
LISBON_TZ = ZoneInfo("Europe/Lisbon") if ZoneInfo else None
try:
    BeautifulSoup("", "lxml")
    HTML_PARSER = "lxml"
except FeatureNotFound:
    HTML_PARSER = "html.parser"
COMMITTED_LASTMOD_BY_URL = {}
PROJECT_PRIORITIES = {
    "inspirium": "0.8",
    "beckman": "0.8",
    "unbreakable": "0.8",
    "quanta-r": "0.75",
    "burly": "0.75",
}
BLOG_PRIORITIES = {
    "harley-davidson-full-service-done-right": "0.9",
    "royal-enfield-bear-650-scrambler-build": "0.9",
    "tubeless-conversion-spoked-wheels": "0.9",
}
NEWS_PRIORITIES = {
    "ericeira-kustom-fest-2026": "0.9",
    "opens-new-workshop-in-cascais": "0.8",
}

# (path, changefreq, priority)
PAGES = [
    ("", "weekly", "1.0"),
    ("motorcycle-service/", "monthly", "0.9"),
    ("parts/", "monthly", "0.9"),
    ("upgrades-tuning/", "monthly", "0.85"),
    ("custom/", "monthly", "0.8"),
    ("harley/", "weekly", "0.95"),
    ("harley-tuning/", "monthly", "0.9"),
    ("harley-custom/", "monthly", "0.9"),
    ("pre-purchase-inspection/", "monthly", "0.95"),
    ("english-speaking-motorcycle-workshop/", "monthly", "0.9"),
    ("authorized-dealer/", "weekly", "0.9"),
    ("authorized-dealer/c-way/", "monthly", "0.88"),
    ("pricing/", "monthly", "0.9"),
    ("services/", "weekly", "0.95"),
    ("projects/", "monthly", "0.85"),
    ("about/", "monthly", "0.7"),
    ("community/", "monthly", "0.75"),
    ("contact/", "monthly", "0.8"),
    ("faq/", "monthly", "0.75"),
    ("privacy/", "yearly", "0.3"),
    ("cookies/", "yearly", "0.3"),
    ("terms/", "yearly", "0.3"),
    *[(f"{slug}/", "monthly", "0.9") for slug in BRAND_ORDER],
    ("motorcycle-tyre-service/", "monthly", "0.95"),
    ("blog/", "weekly", "0.85"),
    *[
        (f"blog/{slug}/", "monthly", BLOG_PRIORITIES.get(slug, "0.82"))
        for slug in BLOG_POSTS
    ],
    ("news/", "weekly", "0.9"),
    *[
        (f"news/{slug}/", "yearly", NEWS_PRIORITIES.get(slug, "0.85"))
        for slug in sorted(
            NEWS_ARTICLES,
            key=lambda item: NEWS_ARTICLES[item].get("sitemapOrder", 999),
        )
    ],
    *[
        (f"projects/{slug}/", "yearly", PROJECT_PRIORITIES.get(slug, "0.7"))
        for slug in PROJECT_CONFIGS
    ],
]

LANGS = ["en", "ru", "uk", "pt"]
HREFLANG_CODES = {"en": "en", "ru": "ru", "uk": "uk", "pt": "pt-PT"}
CUSTOM_LOCALIZED_PATHS = {
    "motorcycle-tyre-service/": {
        "en": "motorcycle-tyre-service/",
        "ru": "ru/shinomontazh-mototsiklov/",
        "uk": "uk/shynomontazh-mototsykliv/",
        "pt": "pt/montagem-de-pneus-mota/",
    }
}


def run_git(args):
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=SITE_ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""
    return result.stdout


def normalize_iso(value):
    value = str(value).strip()
    if "T" in value:
        if len(value) >= 5 and value[-5] in ("+", "-") and value[-3] != ":":
            return f"{value[:-2]}:{value[-2:]}"
        return value

    if LISBON_TZ:
        dt = datetime.combine(datetime.fromisoformat(value).date(), time(10, 0), tzinfo=LISBON_TZ)
        return dt.isoformat(timespec="seconds")

    month = int(value[5:7])
    offset = "+01:00" if 4 <= month <= 10 else "+00:00"
    return f"{value}T10:00:00{offset}"


def article_lastmod(article):
    return normalize_iso(article.get("modifiedISO") or article["publishedISO"])


EXPLICIT_LASTMOD = {
    **{
        f"blog/{slug}/": article_lastmod(article)
        for slug, article in BLOG_POSTS.items()
    },
    **{
        f"news/{slug}/": article_lastmod(article)
        for slug, article in NEWS_ARTICLES.items()
    },
}
PROJECT_LASTMOD = {
    f"projects/{slug}/": {
        lang: normalize_iso(project_modified_iso(project, lang))
        for lang in LANGS
    }
    for slug, project in PROJECT_CONFIGS.items()
}
EXPLICIT_LASTMOD["blog/"] = max(
    article_lastmod(article)
    for article in BLOG_POSTS.values()
)
EXPLICIT_LASTMOD["news/"] = max(
    article_lastmod(article)
    for article in NEWS_ARTICLES.values()
)
def url_for(lang, path):
    if path in CUSTOM_LOCALIZED_PATHS:
        return f"{DOMAIN}/{CUSTOM_LOCALIZED_PATHS[path][lang]}"
    if lang == "en":
        return f"{DOMAIN}/{path}"
    return f"{DOMAIN}/{lang}/{path}"


def relative_url_path(lang, path):
    if path in CUSTOM_LOCALIZED_PATHS:
        return CUSTOM_LOCALIZED_PATHS[path][lang]
    if lang == "en":
        return path
    return f"{lang}/{path}"


def html_file_for(lang, path):
    url_path = relative_url_path(lang, path).strip("/")
    if not url_path:
        return SITE_ROOT / "index.html"
    return SITE_ROOT / url_path / "index.html"


def clean_text(value):
    return re.sub(r"\s+", " ", str(value)).strip()


def stable_attr_value(value):
    if isinstance(value, list):
        return " ".join(str(item) for item in value)
    return str(value)


def semantic_html(html, include_head=True):
    soup = BeautifulSoup(html, HTML_PARSER)
    title = clean_text(soup.title.get_text(" ", strip=True)) if soup.title else ""
    description = ""
    for meta in soup.find_all("meta"):
        if str(meta.get("name", "")).lower() == "description":
            description = clean_text(meta.get("content", ""))
            break

    target = soup.find("main") or soup
    for node in target.find_all(["script", "style"]):
        node.decompose()

    pieces = [f"title:{title}", f"description:{description}"] if include_head else []
    tracked_attrs = ("href", "src", "srcset", "alt", "title", "aria-label", "id")
    for node in target.descendants:
        if isinstance(node, NavigableString):
            text = clean_text(node)
            if text:
                pieces.append(f"text:{text}")
            continue
        if not getattr(node, "name", None):
            continue
        attrs = [
            f"{attr}={stable_attr_value(node[attr])}"
            for attr in tracked_attrs
            if node.has_attr(attr)
        ]
        pieces.append(f"tag:{node.name}:{'|'.join(attrs)}")
    return "\n".join(pieces)


def git_file_at(commit, rel_path):
    return run_git(["show", f"{commit}:{rel_path}"])


def fs_lastmod(path):
    dt = datetime.fromtimestamp(path.stat().st_mtime).astimezone()
    return dt.isoformat(timespec="seconds")


@lru_cache(maxsize=None)
def semantic_git_lastmod(rel_path):
    file_path = SITE_ROOT / rel_path
    if not file_path.exists():
        raise FileNotFoundError(f"Cannot determine sitemap lastmod; missing page file: {rel_path}")

    current = semantic_html(file_path.read_text(encoding="utf-8"))
    head_html = git_file_at("HEAD", rel_path)
    if head_html and semantic_html(head_html) != current:
        return fs_lastmod(file_path)

    log = run_git(["log", "--follow", "--format=%H%x00%cI", "--", rel_path])
    if not log.strip():
        return fs_lastmod(file_path)

    candidate = None
    for line in log.splitlines():
        if "\x00" not in line:
            continue
        commit, commit_date = line.split("\x00", 1)
        historical = git_file_at(commit, rel_path)
        if not historical:
            continue
        if semantic_html(historical) == current:
            candidate = normalize_iso(commit_date)
            continue
        if candidate:
            break

    return candidate or fs_lastmod(file_path)


def lastmod_for(lang, path):
    if path in PROJECT_LASTMOD:
        return PROJECT_LASTMOD[path][lang]
    if path in EXPLICIT_LASTMOD and path not in {"blog/", "news/"}:
        return EXPLICIT_LASTMOD[path]
    html_file = html_file_for(lang, path)
    rel_path = html_file.relative_to(SITE_ROOT).as_posix()
    head_html = git_file_at("HEAD", rel_path)
    if head_html:
        current_html = html_file.read_text(encoding="utf-8")
        current = semantic_html(current_html)
        committed = COMMITTED_LASTMOD_BY_URL.get(url_for(lang, path))
        if semantic_html(head_html) == current:
            if committed:
                return committed
        # Titles and descriptions affect discovery, but they do not change the
        # user-visible page body. Preserve honest lastmod for head-only edits.
        if semantic_html(head_html, include_head=False) == semantic_html(
            current_html, include_head=False
        ):
            if committed:
                return committed
    if path in EXPLICIT_LASTMOD:
        return EXPLICIT_LASTMOD[path]
    return semantic_git_lastmod(rel_path)


def committed_sitemap_lastmods():
    xml_text = run_git(["show", "HEAD:sitemap.xml"])
    if not xml_text:
        return {}
    root = ET.fromstring(xml_text)
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return {
        node.find("sm:loc", namespace).text: node.find("sm:lastmod", namespace).text
        for node in root.findall("sm:url", namespace)
    }


def build_url_entry(lang, path, changefreq, priority):
    primary = url_for(lang, path)
    parts = [f"  <url>"]
    parts.append(f"    <loc>{xml_escape(primary)}</loc>")
    parts.append(f"    <lastmod>{lastmod_for(lang, path)}</lastmod>")
    parts.append(f"    <changefreq>{changefreq}</changefreq>")
    parts.append(f"    <priority>{priority}</priority>")
    # Alternates pointing to all language versions, including self
    for alt in LANGS:
        parts.append(
            f'    <xhtml:link rel="alternate" hreflang="{HREFLANG_CODES[alt]}" href="{xml_escape(url_for(alt, path))}"/>'
        )
    parts.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{xml_escape(url_for("en", path))}"/>')
    parts.append(f"  </url>")
    return "\n".join(parts)


def main():
    global COMMITTED_LASTMOD_BY_URL
    COMMITTED_LASTMOD_BY_URL = committed_sitemap_lastmods()
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for path, freq, pri in PAGES:
        for lang in LANGS:
            lines.append(build_url_entry(lang, path, freq, pri))
    lines.append("</urlset>")
    out = SITE_ROOT / "sitemap.xml"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out} ({len(PAGES)} pages × {len(LANGS)} langs = {len(PAGES) * len(LANGS)} URLs)")


if __name__ == "__main__":
    main()
