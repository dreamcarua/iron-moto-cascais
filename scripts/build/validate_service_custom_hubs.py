#!/usr/bin/env python3
"""Validate the copy-driven Service/Custom hubs and Wave 1 metadata contract."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from bs4 import BeautifulSoup

from build_service_custom_hubs import (
    DOMAIN,
    HREFLANG_CODES,
    HUBS,
    LANGS,
    canonical_path,
    canonical_url,
    markdown_plain,
    output_path,
    parse_copy,
    split_hero_actions,
)
from new_pages_data import PROJECT_TILES
from pricing_data import LABELS
from site_chrome import THANK_YOU_URLS, localized_href


SITE_ROOT = Path(__file__).resolve().parents[2]
TYRE_PATHS = {
    "en": "motorcycle-tyre-service/index.html",
    "pt": "pt/montagem-de-pneus-mota/index.html",
    "ru": "ru/shinomontazh-mototsiklov/index.html",
    "uk": "uk/shynomontazh-mototsykliv/index.html",
}
TYRE_METAS = {
    "en": 'Motorcycle tyre fitting and wheel balancing in Cascais: labour from 40 € per wheel, wheels up to 30" and 400 mm, spoked, vintage, Harley and custom.',
    "pt": 'Montagem de pneus de mota e equilibragem em Cascais: mão de obra desde 40 € por roda, jantes até 30" e 400 mm, raios, clássicas, Harley e custom.',
    "ru": 'Шиномонтаж мотоциклов и балансировка в Кашкайше: работа от 40 € за колесо, диски до 30" и 400 мм, спицы, классика, Harley и кастом. Любые бренды шин.',
    "uk": 'Шиномонтаж мотоциклів і балансування в Кашкайші: робота від 40 € за колесо, диски до 30" і 400 мм, спиці, класика, Harley і кастом. Будь-які бренди шин.',
}
PRICING_NUMBERS = {
    int(value)
    for value in re.findall(
        r"\d[\d ]*",
        (SITE_ROOT / "scripts/build/pricing_data.py").read_text(encoding="utf-8"),
    )
    if value.replace(" ", "").isdigit()
}


def clean_text(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    return re.sub(r"\s+([.,;:!?])", r"\1", value)


def text_of(node) -> str:
    return clean_text(node.get_text(" ", strip=True)) if node else ""


def schema_nodes(soup: BeautifulSoup) -> list[dict]:
    nodes: list[dict] = []
    for script in soup.find_all("script", type="application/ld+json"):
        data = json.loads(script.string or "{}")
        if isinstance(data, dict) and isinstance(data.get("@graph"), list):
            nodes.extend(item for item in data["@graph"] if isinstance(item, dict))
        elif isinstance(data, dict):
            nodes.append(data)
    return nodes


def nodes_of_type(nodes: list[dict], schema_type: str) -> list[dict]:
    matches = []
    for node in nodes:
        types = node.get("@type", [])
        if isinstance(types, str):
            types = [types]
        if schema_type in types:
            matches.append(node)
    return matches


def assert_copy_lines(container, source: str, context: str, issues: list[str]) -> None:
    rendered = text_of(container)
    for raw in source.splitlines():
        line = raw.strip()
        if not line or line == "{{PROJECT_CUSTOM_LINKS}}":
            continue
        expected = markdown_plain(line.removeprefix("- "))
        if expected not in rendered:
            issues.append(f"{context}: copy line missing: {expected}")


def validate_hub(slug: str, lang: str, content: dict, issues: list[str]) -> None:
    path = output_path(slug, lang)
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "lxml")
    label = str(path.relative_to(SITE_ROOT))

    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    description = soup.find("meta", attrs={"name": "description"})
    canonical = soup.find("link", rel="canonical")
    if title != content["seo_title"]:
        issues.append(f"{label}: title differs from approved copy")
    if not description or description.get("content") != content["meta_description"]:
        issues.append(f"{label}: meta description differs from approved copy")
    if not canonical or canonical.get("href") != canonical_url(slug, lang):
        issues.append(f"{label}: self-canonical mismatch")

    alternates = {
        link.get("hreflang"): link.get("href")
        for link in soup.find_all("link", rel="alternate")
        if link.get("hreflang")
    }
    expected_alternates = {
        **{HREFLANG_CODES[item]: canonical_url(slug, item) for item in LANGS},
        "x-default": canonical_url(slug, "en"),
    }
    if alternates != expected_alternates:
        issues.append(f"{label}: hreflang cluster mismatch")

    h1s = soup.find_all("h1")
    if len(h1s) != 1 or text_of(h1s[0]) != content["h1"]:
        issues.append(f"{label}: expected one exact approved H1")
    home_path = SITE_ROOT / ("index.html" if lang == "en" else f"{lang}/index.html")
    home_h1 = BeautifulSoup(home_path.read_text(encoding="utf-8"), "lxml").find("h1")
    if h1s and text_of(h1s[0]) == text_of(home_h1):
        issues.append(f"{label}: hub H1 duplicates the homepage H1")

    main = soup.find("main", attrs={"data-copy-driven-hub": slug})
    if not main:
        issues.append(f"{label}: copy-driven hub marker missing")
        return
    raw_main = str(main)
    if re.search(r"\b(?:msr|cs)\.", raw_main) or "{{PROJECT_CUSTOM_LINKS}}" in raw_main:
        issues.append(f"{label}: legacy i18n key or project placeholder remains")
    if soup.select_one(".money-local, .money-related"):
        issues.append(f"{label}: generic money-page enhancer duplicated hub-owned copy")

    hero = main.select_one(".hub-hero")
    eyebrow = hero.select_one(".h-eyebrow") if hero else None
    if text_of(eyebrow) != content["eyebrow"]:
        issues.append(f"{label}: hero eyebrow differs from approved copy")
    hero_body, hero_actions = split_hero_actions(content["hero"])
    assert_copy_lines(hero.select_one(".lead") if hero else None, hero_body, f"{label} hero", issues)

    actions = hero.select(".hub-actions a") if hero else []
    if len(actions) != 3:
        issues.append(f"{label}: expected three hero CTAs")
    else:
        if [text_of(item) for item in actions] != [item[0] for item in hero_actions]:
            issues.append(f"{label}: hero CTA labels differ from approved copy")
        whatsapp = next((item for item in actions if urlsplit(item.get("href", "")).netloc == "wa.me"), None)
        if not whatsapp:
            issues.append(f"{label}: WhatsApp CTA missing")
        else:
            query = parse_qs(urlsplit(whatsapp["href"]).query)
            if query.get("text") != [content["whatsapp_prefill"]]:
                issues.append(f"{label}: WhatsApp prefill mismatch")
        source_has_tel = any(item[1] == "tel:+351917961230" for item in hero_actions)
        if source_has_tel and not any(item.get("href") == "tel:+351917961230" for item in actions):
            issues.append(f"{label}: telephone CTA missing")
        if not any(item.get("href") == "#contact" and item.has_attr("data-cta") for item in actions):
            issues.append(f"{label}: lead-form CTA wiring missing")

    modal = soup.select_one("#modal")
    form = soup.select_one("form#leadForm")
    if modal is None or form is None:
        issues.append(f"{label}: shared lead-form modal missing")
    else:
        if form.get("action") != "https://formsubmit.co/c29ab5a6818b2926388e8978888304a2":
            issues.append(f"{label}: lead form does not use the private FormSubmit alias")
        next_inputs = form.select('input[name="_next"]')
        if len(next_inputs) != 1 or next_inputs[0].get("value") != THANK_YOU_URLS[lang]:
            issues.append(f"{label}: lead form has no exact localized _next destination")

    for section in content["sections"]:
        node = main.select_one(f'[data-copy-section="{section["number"]}"]')
        if not node:
            issues.append(f"{label}: section {section['number']} missing")
            continue
        expected_heading = f"{section['number']} · {section['title']}"
        if text_of(node.find("h2")) != expected_heading:
            issues.append(f"{label}: section {section['number']} heading mismatch")
        assert_copy_lines(node.select_one(".hub-copy"), section["body"], f"{label} section {section['number']}", issues)

    cta = main.select_one('[data-copy-section="cta"]')
    if text_of(cta.find("h2") if cta else None) != content["cta"]["title"]:
        issues.append(f"{label}: closing CTA heading mismatch")
    assert_copy_lines(cta.select_one(".hub-copy") if cta else None, content["cta"]["body"], f"{label} CTA", issues)

    related = main.select_one('[data-copy-section="related"]')
    if text_of(related.find("h2") if related else None) != content["related"]["title"]:
        issues.append(f"{label}: related-path heading mismatch")
    source_related = []
    for line in content["related"]["body"].splitlines():
        match = re.match(r"^-\s+\[([^]]+)\]\(([^)]+)\)\s*$", line.strip())
        if match:
            source_related.append((match.group(1), localized_href(match.group(2), lang)))
    rendered_related = [
        (text_of(anchor.select_one(".related-card-label")), anchor.get("href"))
        for anchor in (related.select("a.related-card") if related else [])
    ]
    if rendered_related != source_related:
        issues.append(f"{label}: related paths differ from approved copy")

    visible_faq = []
    for detail in main.select('[data-copy-section="faq"] details'):
        visible_faq.append(
            (
                text_of(detail.find("summary").find("span")),
                text_of(detail.select_one(".answer")),
            )
        )
    expected_faq = [
        (markdown_plain(item["question"]), markdown_plain(item["answer"]))
        for item in content["faq"]
    ]
    if visible_faq != expected_faq:
        issues.append(f"{label}: visible FAQ is not the approved six-item source")

    nodes = schema_nodes(soup)
    for required in ("LocalBusiness", "Service", "FAQPage", "BreadcrumbList"):
        if len(nodes_of_type(nodes, required)) != 1:
            issues.append(f"{label}: expected one {required} schema node")
    if nodes_of_type(nodes, "Offer") or nodes_of_type(nodes, "Product"):
        issues.append(f"{label}: Offer/Product schema is prohibited")
    business_ids = {node.get("@id") for node in nodes_of_type(nodes, "LocalBusiness")}
    service_nodes = nodes_of_type(nodes, "Service")
    if service_nodes and service_nodes[0].get("provider", {}).get("@id") not in business_ids:
        issues.append(f"{label}: Service publisher/provider @id does not resolve")
    faq_nodes = nodes_of_type(nodes, "FAQPage")
    if faq_nodes:
        schema_faq = [
            (item.get("name"), item.get("acceptedAnswer", {}).get("text"))
            for item in faq_nodes[0].get("mainEntity", [])
        ]
        if schema_faq != expected_faq:
            issues.append(f"{label}: FAQPage does not match visible FAQ 1:1")

    if slug == "custom":
        projects = main.select("[data-project-custom-links] a")
        expected_projects = [
            (tile["label"][lang] + " →", localized_href(f'/projects/{tile["slug"]}/', lang))
            for tile in PROJECT_TILES
        ]
        if [(text_of(item), item.get("href")) for item in projects] != expected_projects:
            issues.append(f"{label}: custom project list is not all 14 projects in registry order")
        if "€" in text_of(main):
            issues.append(f"{label}: custom hub must not publish custom-build prices")
    else:
        for amount in re.findall(
            r"(?<![\w-])(\d[\d ]*(?:[–/-]\s*\d[\d ]*)*)\s*€",
            text_of(main),
        ):
            for value in re.findall(r"\d[\d ]*", amount):
                number = int(value.replace(" ", ""))
                if number not in PRICING_NUMBERS:
                    issues.append(
                        f"{label}: service price anchor {number} is absent from pricing_data.py"
                    )


def validate_pricing_and_tyre(issues: list[str]) -> None:
    for lang in LANGS:
        pricing_path = SITE_ROOT / ("pricing/index.html" if lang == "en" else f"{lang}/pricing/index.html")
        soup = BeautifulSoup(pricing_path.read_text(encoding="utf-8"), "lxml")
        label = str(pricing_path.relative_to(SITE_ROOT))
        expected = LABELS[lang]
        checks = {
            "title": soup.title.string.strip() if soup.title and soup.title.string else "",
            "description": (soup.find("meta", attrs={"name": "description"}) or {}).get("content", ""),
            "eyebrow": text_of(soup.select_one(".proj-badge")),
            "h1": text_of(soup.find("h1")),
        }
        expected_checks = {
            "title": expected["page_title"],
            "description": expected["page_description"],
            "eyebrow": expected["eyebrow"],
            "h1": clean_text(re.sub(r"<br\s*/?>", " ", expected["h1"])),
        }
        for key, actual in checks.items():
            if actual != expected_checks[key]:
                issues.append(f"{label}: pricing {key} mismatch")
        head_text = clean_text(str(soup.head))
        if "2025" in soup.title.get_text() or "2025" in text_of(soup.find("h1")):
            issues.append(f"{label}: 2025 remains in pricing title/H1")
        if expected["page_title"] not in head_text or expected["page_description"] not in head_text:
            issues.append(f"{label}: derived head fields do not use pricing title/meta")

        tyre_path = SITE_ROOT / TYRE_PATHS[lang]
        tyre_soup = BeautifulSoup(tyre_path.read_text(encoding="utf-8"), "lxml")
        meta = tyre_soup.find("meta", attrs={"name": "description"})
        if not meta or meta.get("content") != TYRE_METAS[lang]:
            issues.append(f"{tyre_path.relative_to(SITE_ROOT)}: tyre meta refinement mismatch")


def main() -> int:
    issues: list[str] = []
    for slug in HUBS:
        parsed = parse_copy(slug)
        for lang in LANGS:
            validate_hub(slug, lang, parsed[lang], issues)
    validate_pricing_and_tyre(issues)

    if issues:
        print("Service/Custom hub validation failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("Service/Custom hub validation passed: 8 hubs, 4 pricing pages, 4 tyre metas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
