#!/usr/bin/env python3
"""
Generate the shared general and utility hub pages.

Each page:
- Uses the same chrome (head + header + footer + modal) as motorcycle-service/
- Has its own body (sections, JSON-LD), and inline ICM_I18N_PAGE with all 4 langs.
- Uses absolute paths (/assets, /photos) so the same chrome works in /xx/ subtrees.

After running this, run build_i18n.py to produce /ru/, /uk/, /pt/ versions.
"""

import html as html_lib
import json
import re
from pathlib import Path

from build_output import write_html_if_changed
from brand_pages_data import BRAND_NAME, BRAND_NAV_KEYS, BRAND_ORDER
from hero_images import hero_background_css, optimized_hero_url
from new_pages_data import PAGE_HEAD_META, PAGE_I18N, PROJECT_TILES, FAQ_QA
from site_chrome import (
    render_contact_modal,
    render_pre_body_chrome,
    render_site_footer,
)

SITE_ROOT = Path(__file__).resolve().parents[2]
BUILD_DIR = Path(__file__).resolve().parent
DOMAIN = "https://ironcustommotors.com"
CACHE_BUST = "20260906a"  # bump on each change to main.css/main.js
GLOBAL_I18N = json.loads((BUILD_DIR / "i18n.json").read_text(encoding="utf-8"))

# ---------- shared chrome fragments ----------

ARROW_SVG = '<svg fill="none" height="18" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="18"><path d="M5 12h14M13 6l6 6-6 6"></path></svg>'

SHARED_STYLES = """.subpage{padding:160px 0 100px;background:#0a0a0a;position:relative;overflow:hidden;isolation:isolate}
.subpage::before{content:"";position:absolute;top:-30%;right:-15%;width:600px;height:600px;background:radial-gradient(circle,rgba(255,87,34,.20),transparent 60%);pointer-events:none;z-index:1}
.subpage::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,10,10,.45) 0%,rgba(10,10,10,.6) 50%,rgba(10,10,10,.96) 100%);z-index:0;pointer-events:none}
.subpage .container{position:relative;z-index:1}
.crumb{display:flex;align-items:center;gap:10px;font-family:var(--font-ui);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--text-mute);margin-bottom:24px}
.crumb a{color:var(--text-dim)}
.crumb a:hover{color:var(--accent)}
.crumb .sep{color:var(--accent)}
.subpage h1{font-family:var(--font-display);font-weight:800;line-height:.92;letter-spacing:-.01em;text-transform:uppercase;font-size:clamp(30px,4vw,52px);color:#fff;max-width:18ch;margin-bottom:24px}
.subpage h1 .accent{color:var(--accent)}
.subpage .lead{max-width:60ch;color:var(--text-dim)}
.subpage-cta{display:flex;gap:14px;flex-wrap:wrap;margin-top:36px}
.sub-section{padding:var(--gap) 0;background:#0a0a0a;border-top:1px solid var(--border)}
.sub-section .heading{margin-bottom:60px;display:grid;grid-template-columns:1fr 1.4fr;gap:60px;align-items:end;padding-bottom:30px;border-bottom:1px solid var(--border)}
.sub-section .heading h2{margin:0;font-family:var(--font-display);font-weight:800;text-transform:uppercase;font-size:clamp(24px,3.2vw,44px);line-height:.95;letter-spacing:-.005em;color:#fff}
.sub-section .heading h2 em{color:var(--accent);font-style:italic}
.sub-section .heading p.lead{margin-top:18px}
.sub-intro p{font-family:var(--font-ui);font-weight:400;font-size:clamp(18px,1.6vw,22px);line-height:1.55;color:var(--text);max-width:64ch;margin-bottom:18px}
.sub-intro p:last-child{color:var(--text-dim);font-size:clamp(15px,1.2vw,18px)}
.cta-back{padding:var(--gap) 0;background:#0a0a0a;text-align:center;border-top:1px solid var(--border)}
.cta-back .container{max-width:760px}
.cta-back h2{margin-bottom:18px;font-family:var(--font-display);font-weight:800;text-transform:uppercase;font-size:clamp(24px,3.2vw,42px);line-height:.95;color:#fff}
.cta-back .lead{margin:0 auto 30px;max-width:54ch}
.cta-back .btns{display:flex;justify-content:center;gap:14px;flex-wrap:wrap}
@media (max-width:1100px){.sub-section .heading{grid-template-columns:1fr;gap:24px}}
@media (max-width:760px){.subpage{padding-top:130px}}"""


def head(
    page_id,
    lang,
    extra_styles="",
    json_ld_blocks=None,
    hreflang=True,
    og_image=None,
    robots="max-image-preview:large",
):
    """Build the <head> section for a page."""
    meta = PAGE_HEAD_META[page_id][lang]
    canonical = f"{DOMAIN}/{page_id}/"
    og_locale = {"en": "en_US", "ru": "ru_RU", "uk": "uk_UA", "pt": "pt_PT"}[lang]
    og_img = og_image or f"{DOMAIN}/photos/og.jpg"

    json_ld_html = ""
    if json_ld_blocks:
        for block in json_ld_blocks:
            json_ld_html += f'<script type="application/ld+json">{json.dumps(block, ensure_ascii=False)}</script>\n'

    hreflang_html = ""
    if hreflang:
        urls = [
            ("en", f"{DOMAIN}/{page_id}/"),
            ("ru", f"{DOMAIN}/ru/{page_id}/"),
            ("uk", f"{DOMAIN}/uk/{page_id}/"),
            ("pt", f"{DOMAIN}/pt/{page_id}/"),
        ]
        hreflang_html = "".join(
            f'<link rel="alternate" hreflang="{lg}" href="{u}"/>' for lg, u in urls
        )
        hreflang_html += f'<link rel="alternate" hreflang="x-default" href="{DOMAIN}/{page_id}/"/>'

    # Inline ICM_I18N_PAGE JSON with all 4 langs for this page
    i18n_json = json.dumps(PAGE_I18N[page_id], ensure_ascii=False)

    return f'''<!DOCTYPE html>
<html data-lang="{lang}" lang="{lang}">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1, viewport-fit=cover" name="viewport"/>
<meta content="#0a0a0a" name="theme-color"/>
<meta content="{robots}" name="robots"/>
<title>{meta["title"]}</title>
<meta content="{meta["description"]}" name="description"/>
<link href="{canonical}" rel="canonical"/>
<meta content="{meta["title"]}" property="og:title"/>
<meta content="{meta["description"]}" property="og:description"/>
<meta content="website" property="og:type"/>
<meta content="{canonical}" property="og:url"/>
<meta content="Iron Custom Motors" property="og:site_name"/>
<meta content="{og_img}" property="og:image"/>
<meta content="1200" property="og:image:width"/>
<meta content="630" property="og:image:height"/>
<meta content="{og_locale}" property="og:locale"/>
<meta content="summary_large_image" name="twitter:card"/>
<meta content="{meta["title"]}" name="twitter:title"/>
<meta content="{meta["description"]}" name="twitter:description"/>
<meta content="{og_img}" name="twitter:image"/>
<link href="/photos/favicon.ico" rel="icon" sizes="any"/>
<link href="/photos/favicon-32.png" rel="icon" sizes="32x32" type="image/png"/>
<link href="/photos/apple-touch-icon.png" rel="apple-touch-icon" sizes="180x180"/>
<link href="/photos/site.webmanifest" rel="manifest"/>
<link href="https://fonts.googleapis.com" rel="preconnect"/>
<link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
<link href="https://fonts.googleapis.com/css2?family=Saira:wght@300;400;500;600;700;800;900&amp;family=Saira+Condensed:wght@400;600;700;800;900&amp;family=Roboto+Condensed:wght@400;500;600;700;800;900&amp;family=Inter:wght@300;400;500;600;700&amp;display=swap" rel="stylesheet"/>
<link href="/assets/main.css?v={CACHE_BUST}" rel="stylesheet"/>
<style>
{SHARED_STYLES}
{extra_styles}
</style>
{json_ld_html}<script>window.ICM_I18N_PAGE = {i18n_json};</script>
{hreflang_html}
</head>'''


def header_html():
    return render_pre_body_chrome("en")


def footer_html():
    return render_site_footer("en")


MODAL_HTML = render_contact_modal("en")


def end_html():
    return f'{MODAL_HTML}\n<script defer="" src="/assets/main.js?v={CACHE_BUST}"></script>\n</body>\n</html>'


def breadcrumb_jsonld(crumb_name, url):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{DOMAIN}/"},
            {"@type": "ListItem", "position": 2, "name": crumb_name, "item": url},
        ],
    }


def schema_text(value):
    """Return readable plain text for JSON-LD from visible HTML-capable copy."""
    text = re.sub(r"<[^>]+>", "", value or "")
    return re.sub(r"\s+", " ", html_lib.unescape(text)).strip()


def hero_srcset(source_url, ext):
    return ", ".join(
        f"{optimized_hero_url(source_url, width, ext)} {width}w"
        for width in (768, 1280, 1920)
    )


def hero_picture(source_url, alt_text, alt_key, class_name="abt-hero-media", fetchpriority="high"):
    priority_attr = f' fetchpriority="{fetchpriority}"' if fetchpriority else ""
    return f'''<picture class="{class_name}">
<source srcset="{hero_srcset(source_url, "avif")}" sizes="100vw" type="image/avif"/>
<source srcset="{hero_srcset(source_url, "webp")}" sizes="100vw" type="image/webp"/>
<img alt="{html_lib.escape(alt_text, quote=True)}" data-i18n-alt="{alt_key}" decoding="async"{priority_attr} height="1440" sizes="100vw" src="{optimized_hero_url(source_url, 1920, "jpg")}" srcset="{hero_srcset(source_url, "jpg")}" width="1920"/>
</picture>'''


def optional_lead(en, key):
    value = en.get(key, "")
    if not value:
        return ""
    return f'<p class="lead" data-i18n-html="{key}">{value}</p>'


def optional_paragraph(en, key):
    value = en.get(key, "")
    if not value:
        return ""
    return f'<p data-i18n-html="{key}">{value}</p>'


# =========================================================================
# /thank-you/ — noindex FormSubmit destination
# =========================================================================

def render_thank_you():
    page_id = "thank-you"
    page_url = f"{DOMAIN}/{page_id}/"
    en = PAGE_I18N[page_id]["en"]
    json_ld = [
        {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "@id": page_url,
            "name": en["thanks.crumb"],
            "url": page_url,
            "isPartOf": {"@id": f"{DOMAIN}/#website"},
            "about": {"@id": f"{DOMAIN}/#business"},
        },
        breadcrumb_jsonld(en["thanks.crumb"], page_url),
    ]
    extra_css = """.thanks-page{min-height:72vh;display:flex;align-items:center;padding:150px 0 90px;background:#0a0a0a}
.thanks-card{max-width:760px;padding:clamp(28px,5vw,58px);border:1px solid var(--border);border-radius:var(--radius-lg);background:var(--surface)}
.thanks-card h1{max-width:none;margin:14px 0 18px}
.thanks-card .lead{font-size:clamp(17px,2vw,21px)}
.thanks-card .subpage-cta{margin-top:30px}"""
    body = f'''<main>
<section class="subpage thanks-page">
<div class="container">
<div class="thanks-card">
<div class="crumb"><a data-i18n="thanks.breadHome" href="/">{en["thanks.breadHome"]}</a><span class="sep">→</span><span data-i18n="thanks.crumb">{en["thanks.crumb"]}</span></div>
<span class="h-eyebrow" data-i18n="thanks.eyebrow">{en["thanks.eyebrow"]}</span>
<h1 data-i18n="thanks.h1">{en["thanks.h1"]}</h1>
<p class="lead" data-i18n="thanks.text">{en["thanks.text"]}</p>
<div class="subpage-cta">
<a class="btn btn-primary" data-wa="" href="https://wa.me/351917961230" rel="noopener" target="_blank"><span data-i18n="thanks.whatsapp">{en["thanks.whatsapp"]}</span>{ARROW_SVG}</a>
<a class="btn btn-ghost" data-i18n="thanks.home" href="/">{en["thanks.home"]}</a>
</div>
</div>
</div>
</section>
</main>'''
    page_html = (
        head(
            page_id,
            "en",
            extra_styles=extra_css,
            json_ld_blocks=json_ld,
            robots="noindex,follow",
        )
        + "\n<body>\n"
        + header_html()
        + body
        + footer_html()
        + end_html()
    )
    out = SITE_ROOT / page_id / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    write_html_if_changed(
        out,
        page_html,
        preserve_body_shell=True,
        merge_page_i18n=True,
        preserve_downstream_head=True,
    )
    return out


# =========================================================================
# /services/ — hub
# =========================================================================

def render_services():
    page_id = "services"
    page_url = f"{DOMAIN}/{page_id}/"
    en = PAGE_I18N[page_id]["en"]
    brand_service_links = "\n".join(
        f'<a class="brand-service-link" data-i18n="{BRAND_NAV_KEYS[slug]}" href="/{slug}/">{BRAND_NAME[slug]}</a>'
        for slug in BRAND_ORDER
    )

    json_ld = [
        {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": "All motorcycle services under one roof.",
            "url": page_url,
            "isPartOf": {"@id": f"{DOMAIN}/#website"},
            "about": {"@id": f"{DOMAIN}/#business"},
            "hasPart": [
                {"@type": "Service", "name": "Motorcycle service & repair", "url": f"{DOMAIN}/motorcycle-service/"},
                {"@type": "Service", "name": "Motorcycle parts & consumables", "url": f"{DOMAIN}/parts/"},
                {"@type": "Service", "name": "Upgrades & tuning", "url": f"{DOMAIN}/upgrades-tuning/"},
                {"@type": "Service", "name": "Custom & special projects", "url": f"{DOMAIN}/custom/"},
                {"@type": "Service", "name": "Motorcycle tyre fitting & wheel balancing", "url": f"{DOMAIN}/motorcycle-tyre-service/"},
                {"@type": "Service", "name": "Pre-purchase inspection", "url": f"{DOMAIN}/pre-purchase-inspection/"},
            ],
        },
        breadcrumb_jsonld("Services", page_url),
    ]

    extra_css = """.subpage.svc{padding:140px 0 80px}
.subpage.svc .bg{position:absolute;inset:0;z-index:-1;background-size:cover;background-position:center;filter:saturate(.85) contrast(1.05) brightness(.5);""" + hero_background_css('/photos/service-action-1600.jpg') + """}
.svc-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:24px;margin-top:40px}
.svc-card{position:relative;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-lg);padding:34px 30px;display:flex;flex-direction:column;gap:14px;transition:border-color .25s var(--ease),transform .25s var(--ease)}
.svc-card:hover{border-color:var(--accent);transform:translateY(-2px)}
.svc-card .num{font-family:var(--font-display);font-weight:800;font-size:48px;color:var(--accent);line-height:1;margin-bottom:6px}
.svc-card h3{font-family:var(--font-display);font-weight:800;text-transform:uppercase;font-size:clamp(20px,2vw,28px);line-height:1.05;color:#fff}
.svc-card p{font-size:15px;color:var(--text-dim);max-width:46ch}
.svc-card .cta{margin-top:auto;display:inline-flex;align-items:center;gap:8px;font-family:var(--font-ui);font-weight:600;font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--accent)}
.svc-card .cta:hover{transform:translateX(3px)}
.brand-service-list{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px;margin-top:28px}
.brand-service-link{display:flex;align-items:center;justify-content:center;min-height:76px;padding:18px 16px;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-lg);font-family:var(--font-display);font-weight:800;text-transform:uppercase;font-size:clamp(18px,1.7vw,24px);line-height:1;color:#fff;text-align:center;transition:border-color .25s var(--ease),transform .25s var(--ease),color .25s var(--ease)}
.brand-service-link:hover{border-color:var(--accent);color:var(--accent);transform:translateY(-2px)}
/* Whole-card click handling is done in main.js (CARD_PATTERNS) */
.price-strip{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:36px 0 0}
.price-strip .ph-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-lg);padding:22px 20px}
.price-strip .ph-card .v{font-family:var(--font-display);font-weight:800;color:var(--accent);font-size:34px;line-height:1}
.price-strip .ph-card .t{font-size:13px;color:var(--text-dim);margin-top:8px}
@media (max-width:900px){.svc-grid{grid-template-columns:1fr}.brand-service-list{grid-template-columns:repeat(2,1fr)}.price-strip{grid-template-columns:repeat(2,1fr)}}
@media (max-width:560px){.brand-service-list{grid-template-columns:1fr}}"""

    body = f'''<main>
<section class="subpage svc">
<div aria-hidden="true" class="bg"></div>
<div class="container">
<div class="crumb"><a data-i18n="svc.breadHome" href="/">Home</a><span class="sep">→</span><span data-i18n="svc.h1Crumb">Services</span></div>
<div class="h-eyebrow" data-i18n="svc.eyebrow" style="margin-bottom:18px">{en["svc.eyebrow"]}</div>
<h1 data-i18n="svc.h1">{en["svc.h1"]}</h1>
<p class="lead" data-i18n="svc.sub">{en["svc.sub"]}</p>
<div class="subpage-cta">
<a class="btn btn-primary" data-wa="" href="https://wa.me/351917961230" rel="noopener" target="_blank"><span data-i18n="svc.btnWA">{en["svc.btnWA"]}</span>{ARROW_SVG}</a>
<a class="btn btn-ghost" data-i18n="svc.btnSend" href="/contact/">{en["svc.btnSend"]}</a>
</div>
</div>
</section>
<section class="sub-section">
<div class="container">
<div class="heading">
<span class="h-eyebrow" data-i18n="svc.listEyebrow">{en["svc.listEyebrow"]}</span>
<div>
<h2 data-i18n="svc.listTitle">{en["svc.listTitle"]}</h2>
<p class="lead" data-i18n="svc.listLead">{en["svc.listLead"]}</p>
</div>
</div>
<div class="svc-grid">
<article class="svc-card">
<div class="num">01</div>
<h3 data-i18n="svc.s1t">{en["svc.s1t"]}</h3>
<p data-i18n="svc.s1d">{en["svc.s1d"]}</p>
<a class="cta" data-i18n="svc.s1cta" href="/motorcycle-service/">{en["svc.s1cta"]}</a>
</article>
<article class="svc-card">
<div class="num">02</div>
<h3 data-i18n="svc.s2t">{en["svc.s2t"]}</h3>
<p data-i18n="svc.s2d">{en["svc.s2d"]}</p>
<a class="cta" data-i18n="svc.s2cta" href="/parts/">{en["svc.s2cta"]}</a>
</article>
<article class="svc-card">
<div class="num">03</div>
<h3 data-i18n="svc.s3t">{en["svc.s3t"]}</h3>
<p data-i18n="svc.s3d">{en["svc.s3d"]}</p>
<a class="cta" data-i18n="svc.s3cta" href="/upgrades-tuning/">{en["svc.s3cta"]}</a>
</article>
<article class="svc-card">
<div class="num">04</div>
<h3 data-i18n="svc.s4t">{en["svc.s4t"]}</h3>
<p data-i18n="svc.s4d">{en["svc.s4d"]}</p>
<a class="cta" data-i18n="svc.s4cta" href="/custom/">{en["svc.s4cta"]}</a>
</article>
<article class="svc-card">
<div class="num">05</div>
<h3 data-i18n="svc.s6t">{en["svc.s6t"]}</h3>
<p data-i18n="svc.s6d">{en["svc.s6d"]}</p>
<a class="cta" data-i18n="svc.s6cta" href="/motorcycle-tyre-service/">{en["svc.s6cta"]}</a>
</article>
<article class="svc-card">
<div class="num">06</div>
<h3 data-i18n="svc.s5t">{en["svc.s5t"]}</h3>
<p data-i18n="svc.s5d">{en["svc.s5d"]}</p>
<a class="cta" data-i18n="svc.s5cta" href="/pre-purchase-inspection/">{en["svc.s5cta"]}</a>
</article>
</div>
<div class="brand-service-list" aria-label="Brand service pages">
{brand_service_links}
</div>
</div>
</section>
<section class="sub-section">
<div class="container">
<div class="heading">
<span class="h-eyebrow" data-i18n="svc.priceEyebrow">{en["svc.priceEyebrow"]}</span>
<div>
<h2 data-i18n="svc.priceTitle">{en["svc.priceTitle"]}</h2>
<p class="lead" data-i18n="svc.priceLead">{en["svc.priceLead"]}</p>
</div>
</div>
<div class="price-strip">
<div class="ph-card"><div class="v" data-i18n="svc.priceCardAv">{en["svc.priceCardAv"]}</div><div class="t" data-i18n="svc.priceCardA">{en["svc.priceCardA"]}</div></div>
<div class="ph-card"><div class="v" data-i18n="svc.priceCardBv">{en["svc.priceCardBv"]}</div><div class="t" data-i18n="svc.priceCardB">{en["svc.priceCardB"]}</div></div>
<div class="ph-card"><div class="v" data-i18n="svc.priceCardCv">{en["svc.priceCardCv"]}</div><div class="t" data-i18n="svc.priceCardC">{en["svc.priceCardC"]}</div></div>
<div class="ph-card"><div class="v" data-i18n="svc.priceCardDv">{en["svc.priceCardDv"]}</div><div class="t" data-i18n="svc.priceCardD">{en["svc.priceCardD"]}</div></div>
</div>
<div style="margin-top:30px"><a class="btn btn-primary" data-i18n="svc.priceCta" href="/pricing/">{en["svc.priceCta"]}</a></div>
</div>
</section>
<section class="cta-back">
<div class="container">
<span class="h-eyebrow" data-i18n="svc.ctaEyebrow">{en["svc.ctaEyebrow"]}</span>
<h2 data-i18n="svc.ctaTitle">{en["svc.ctaTitle"]}</h2>
<p class="lead" data-i18n="svc.ctaText">{en["svc.ctaText"]}</p>
<div class="btns">
<a class="btn btn-primary" data-wa="" href="https://wa.me/351917961230" rel="noopener" target="_blank"><span data-i18n="svc.btnWA">{en["svc.btnWA"]}</span>{ARROW_SVG}</a>
<a class="btn btn-ghost" data-i18n="svc.btnBack" href="/">{en["svc.btnBack"]}</a>
</div>
</div>
</section>
</main>'''

    html = head(page_id, "en", extra_styles=extra_css, json_ld_blocks=json_ld) + "\n<body>\n" + header_html() + body + footer_html() + end_html()
    out = SITE_ROOT / page_id / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    write_html_if_changed(out, html, preserve_body_shell=True, merge_page_i18n=True, preserve_downstream_head=True)
    return out


# =========================================================================
# /projects/ — gallery
# =========================================================================

def render_projects():
    page_id = "projects"
    page_url = f"{DOMAIN}/{page_id}/"
    en = PAGE_I18N[page_id]["en"]

    # ItemList JSON-LD for the gallery
    items = []
    for i, p in enumerate(PROJECT_TILES, start=1):
        items.append({
            "@type": "ListItem",
            "position": i,
            "url": f"{DOMAIN}/projects/{p['slug']}/",
            "name": p["label"]["en"],
        })
    json_ld = [
        {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": "Custom motorcycles we built.",
            "url": page_url,
            "isPartOf": {"@id": f"{DOMAIN}/#website"},
            "mainEntity": {
                "@type": "ItemList",
                "numberOfItems": len(items),
                "itemListElement": items,
            },
        },
        breadcrumb_jsonld("Projects", page_url),
    ]

    extra_css = """.subpage.prj{padding:140px 0 80px}
.subpage.prj .bg{position:absolute;inset:0;z-index:-1;background-size:cover;background-position:center;filter:saturate(.85) contrast(1.05) brightness(.45);""" + hero_background_css('/photos/projects/inspirium-hero-1600.jpg') + """}
.awards-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:30px}
.award{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-lg);padding:30px 26px}
.award .num{font-family:var(--font-display);font-weight:800;color:var(--accent);font-size:36px;line-height:1;margin-bottom:14px}
.award h3{font-family:var(--font-display);font-weight:800;text-transform:uppercase;font-size:20px;color:#fff;margin-bottom:10px}
.award p{font-size:14px;color:var(--text-dim)}
.prj-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:30px}
.prj-tile{position:relative;display:block;aspect-ratio:4/3;border-radius:var(--radius-lg);overflow:hidden;background:#111;text-decoration:none}
.prj-tile picture{display:block;width:100%;height:100%}
.prj-tile img{width:100%;height:100%;object-fit:cover;transition:transform .5s var(--ease)}
.prj-tile:hover img{transform:scale(1.04)}
.prj-tile::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 40%,rgba(0,0,0,.82) 100%);pointer-events:none}
.prj-tile .meta{position:absolute;left:18px;right:18px;bottom:16px;z-index:2;color:#fff}
.prj-tile .meta .y{font-family:var(--font-ui);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--text-mute);margin-bottom:4px}
.prj-tile .meta .n{font-family:var(--font-display);font-weight:800;text-transform:uppercase;font-size:22px;line-height:1}
.prj-tile .meta .tag{display:inline-block;margin-top:6px;font-family:var(--font-ui);font-size:10px;color:var(--accent);letter-spacing:.1em;text-transform:uppercase}
@media (max-width:1100px){.awards-grid{grid-template-columns:1fr}.prj-grid{grid-template-columns:repeat(2,1fr)}}
@media (max-width:640px){.prj-grid{grid-template-columns:1fr}}"""

    # Build project tiles HTML
    tiles_html = ""
    for p in PROJECT_TILES:
        image = f'''<img alt="{p["label"]["en"]}" loading="lazy" src="{p["img"]}" width="{p.get("img_width", 800)}" height="{p.get("img_height", 600)}"/>'''
        if p.get("img_avif"):
            image = f'''<picture>
<source srcset="{p["img_avif"]}" type="image/avif"/>
<source srcset="{p.get("img_webp", p["img"])}" type="image/webp"/>
{image}
</picture>'''
        tiles_html += f'''<a class="prj-tile" href="/projects/{p["slug"]}/">
{image}
<div class="meta">
<div class="y">{p["year"]}</div>
<div class="n" data-i18n-proj-label="{p["slug"]}">{p["label"]["en"]}</div>
<div class="tag" data-i18n-proj-tag="{p["slug"]}">{p["tag"]["en"]}</div>
</div>
</a>
'''

    body = f'''<main>
<section class="subpage prj">
<div aria-hidden="true" class="bg"></div>
<div class="container">
<div class="crumb"><a data-i18n="prj.breadHome" href="/">Home</a><span class="sep">→</span><span data-i18n="prj.h1Crumb">Projects</span></div>
<div class="h-eyebrow" data-i18n="prj.eyebrow" style="margin-bottom:18px">{en["prj.eyebrow"]}</div>
<h1 data-i18n="prj.h1">{en["prj.h1"]}</h1>
<p class="lead" data-i18n="prj.sub">{en["prj.sub"]}</p>
<div class="subpage-cta">
<a class="btn btn-primary" data-wa="" href="https://wa.me/351917961230" rel="noopener" target="_blank"><span data-i18n="prj.btnWA">{en["prj.btnWA"]}</span>{ARROW_SVG}</a>
<a class="btn btn-ghost" data-i18n="prj.btnSend" href="/contact/">{en["prj.btnSend"]}</a>
</div>
</div>
</section>
<section class="sub-section">
<div class="container">
<div class="heading">
<span class="h-eyebrow" data-i18n="prj.awardsEyebrow">{en["prj.awardsEyebrow"]}</span>
<div>
<h2 data-i18n="prj.awardsTitle">{en["prj.awardsTitle"]}</h2>
<p class="lead" data-i18n="prj.awardsLead">{en["prj.awardsLead"]}</p>
</div>
</div>
<div class="awards-grid">
<div class="award"><div class="num">01</div><h3 data-i18n="prj.a1t">{en["prj.a1t"]}</h3><p data-i18n="prj.a1d">{en["prj.a1d"]}</p></div>
<div class="award"><div class="num">02</div><h3 data-i18n="prj.a2t">{en["prj.a2t"]}</h3><p data-i18n="prj.a2d">{en["prj.a2d"]}</p></div>
<div class="award"><div class="num">03</div><h3 data-i18n="prj.a3t">{en["prj.a3t"]}</h3><p data-i18n="prj.a3d">{en["prj.a3d"]}</p></div>
</div>
</div>
</section>
<section class="sub-section">
<div class="container">
<div class="heading">
<span class="h-eyebrow" data-i18n="prj.galleryEyebrow">{en["prj.galleryEyebrow"]}</span>
<div>
<h2 data-i18n="prj.galleryTitle">{en["prj.galleryTitle"]}</h2>
<p class="lead" data-i18n="prj.galleryLead">{en["prj.galleryLead"]}</p>
</div>
</div>
<div class="prj-grid">
{tiles_html}
</div>
</div>
</section>
<section class="cta-back">
<div class="container">
<span class="h-eyebrow" data-i18n="prj.ctaEyebrow">{en["prj.ctaEyebrow"]}</span>
<h2 data-i18n="prj.ctaTitle">{en["prj.ctaTitle"]}</h2>
<p class="lead" data-i18n="prj.ctaText">{en["prj.ctaText"]}</p>
<div class="btns">
<a class="btn btn-primary" data-wa="" href="https://wa.me/351917961230" rel="noopener" target="_blank"><span data-i18n="prj.btnWA">{en["prj.btnWA"]}</span>{ARROW_SVG}</a>
<a class="btn btn-ghost" data-i18n="prj.btnBack" href="/">{en["prj.btnBack"]}</a>
</div>
</div>
</section>
</main>'''

    # Inject project tile labels into ICM_I18N_PAGE for other langs
    for lang in ["ru", "uk", "pt"]:
        for p in PROJECT_TILES:
            PAGE_I18N[page_id][lang][f"proj.label.{p['slug']}"] = p["label"][lang]
            PAGE_I18N[page_id][lang][f"proj.tag.{p['slug']}"] = p["tag"][lang]
    # Also for EN (so the data attribute resolves consistently)
    for p in PROJECT_TILES:
        PAGE_I18N[page_id]["en"][f"proj.label.{p['slug']}"] = p["label"]["en"]
        PAGE_I18N[page_id]["en"][f"proj.tag.{p['slug']}"] = p["tag"]["en"]

    html = head(page_id, "en", extra_styles=extra_css, json_ld_blocks=json_ld) + "\n<body>\n" + header_html() + body + footer_html() + end_html()
    out = SITE_ROOT / page_id / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    write_html_if_changed(out, html, preserve_body_shell=True, merge_page_i18n=True, preserve_downstream_head=True)
    return out


# =========================================================================
# /about/ — about page
# =========================================================================

def render_about():
    page_id = "about"
    page_url = f"{DOMAIN}/{page_id}/"
    en = PAGE_I18N[page_id]["en"]
    hero_image = "/photos/about-hero.jpg"

    faq_entities = [
        {
            "@type": "Question",
            "name": schema_text(en[f"abt.faq{idx}q"]),
            "acceptedAnswer": {
                "@type": "Answer",
                "text": schema_text(en[f"abt.faq{idx}a"]),
            },
        }
        for idx in range(1, 7)
    ]

    json_ld = [
        {
            "@context": "https://schema.org",
            "@type": "AboutPage",
            "@id": f"{page_url}#about",
            "name": schema_text(en["abt.h1"]),
            "description": PAGE_HEAD_META[page_id]["en"]["description"],
            "url": page_url,
            "inLanguage": "en",
            "mainEntity": {"@id": f"{DOMAIN}/#business"},
            "isPartOf": {"@id": f"{DOMAIN}/#website"},
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "@id": f"{page_url}#company-faq",
            "url": page_url,
            "inLanguage": "en",
            "mainEntity": faq_entities,
        },
        breadcrumb_jsonld("About", page_url),
        {
            "@context": "https://schema.org",
            "@type": "Person",
            "@id": f"{DOMAIN}/#yaroslav-lutytskyi",
            "name": "Yaroslav Lutytskyi",
            "worksFor": {"@id": f"{DOMAIN}/#business"},
            "founderOf": {"@id": f"{DOMAIN}/#business"},
        },
    ]

    value_cards = "\n".join(
        f'''<div class="value-card"><div class="num">{idx:02d}</div><h3 data-i18n="abt.v{idx}t">{en[f"abt.v{idx}t"]}</h3><p data-i18n="abt.v{idx}d">{en[f"abt.v{idx}d"]}</p></div>'''
        for idx in range(1, 5)
    )
    award_rows = "\n".join(
        f'''<div class="award-row"><div class="y" data-i18n="abt.a{idx}y">{en[f"abt.a{idx}y"]}</div><div><h4 data-i18n-html="abt.a{idx}t">{en[f"abt.a{idx}t"]}</h4><p data-i18n-html="abt.a{idx}d">{en[f"abt.a{idx}d"]}</p></div></div>'''
        for idx in range(1, 4)
    )
    timeline_rows = "\n".join(
        f'''<div class="timeline-row"><div class="y" data-i18n="abt.tl{idx}y">{en[f"abt.tl{idx}y"]}</div><div><h4 data-i18n-html="abt.tl{idx}t">{en[f"abt.tl{idx}t"]}</h4>{optional_paragraph(en, f"abt.tl{idx}d")}</div></div>'''
        for idx in range(1, 7)
    )
    faq_items = "\n".join(
        f'''<details class="company-faq-item"><summary data-i18n="abt.faq{idx}q">{en[f"abt.faq{idx}q"]}</summary><p data-i18n-html="abt.faq{idx}a">{en[f"abt.faq{idx}a"]}</p></details>'''
        for idx in range(1, 7)
    )
    values_lead_html = optional_lead(en, "abt.valuesLead")
    awards_lead_html = optional_lead(en, "abt.awardsLead")
    timeline_lead_html = optional_lead(en, "abt.timelineLead")
    faq_lead_html = optional_lead(en, "abt.faqLead")

    extra_css = """.subpage.abt{padding:140px 0 90px;min-height:760px;display:flex;align-items:center}
.subpage.abt::after{background:linear-gradient(90deg,rgba(10,10,10,.82) 0%,rgba(10,10,10,.70) 42%,rgba(10,10,10,.42) 100%),linear-gradient(180deg,rgba(10,10,10,.08) 0%,rgba(10,10,10,.20) 48%,rgba(10,10,10,.88) 100%)}
.subpage.abt .bg{position:absolute;inset:0;z-index:0;background:radial-gradient(circle at 86% 18%,rgba(255,87,34,.20),transparent 36%);pointer-events:none}
.abt-hero-media{position:absolute;inset:0;z-index:0;display:block;overflow:hidden;background:#050505}
.abt-hero-media img{display:block;width:100%;height:100%;object-fit:cover;object-position:center;filter:saturate(.92) contrast(1.04) brightness(.82)}
.values-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:20px;margin-top:30px}
.value-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-lg);padding:28px 26px}
.value-card .num{font-family:var(--font-display);font-weight:800;color:var(--accent);font-size:30px;line-height:1;margin-bottom:10px}
.value-card h3{font-family:var(--font-display);font-weight:800;text-transform:uppercase;font-size:22px;color:#fff;margin-bottom:8px}
.value-card p{font-size:15px;color:var(--text-dim);max-width:46ch}
.awards-list{display:grid;grid-template-columns:1fr;gap:14px;margin-top:30px}
.award-row{display:grid;grid-template-columns:160px 1fr;gap:30px;padding:24px 0;border-bottom:1px solid var(--border);align-items:start;transition:padding-left .25s var(--ease)}
.award-row:hover{padding-left:10px}
.award-row .y{font-family:var(--font-ui);font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent)}
.award-row h4{font-family:var(--font-display);font-weight:800;text-transform:uppercase;font-size:clamp(18px,1.6vw,22px);color:#fff;margin-bottom:6px}
.award-row p{font-size:15px;color:var(--text-dim);max-width:64ch}
.timeline-list{display:grid;grid-template-columns:1fr;gap:0;margin-top:30px}
.timeline-row{display:grid;grid-template-columns:130px 1fr;gap:34px;padding:26px 0;border-bottom:1px solid var(--border);align-items:start}
.timeline-row .y{font-family:var(--font-display);font-weight:800;color:var(--accent);font-size:34px;line-height:1}
.timeline-row h4{font-family:var(--font-display);font-weight:800;text-transform:uppercase;font-size:clamp(18px,1.8vw,24px);color:#fff;margin-bottom:6px}
.timeline-row p{font-size:15px;color:var(--text-dim);max-width:66ch}
.company-faq-list{display:grid;grid-template-columns:1fr;gap:14px;margin-top:30px}
.company-faq-item{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-lg);padding:0 24px;overflow:hidden}
.company-faq-item summary{cursor:pointer;list-style:none;padding:22px 0;font-family:var(--font-display);font-weight:800;text-transform:uppercase;font-size:clamp(18px,1.8vw,24px);line-height:1.08;color:#fff}
.company-faq-item summary::-webkit-details-marker{display:none}
.company-faq-item p{padding:0 0 22px;font-size:16px;color:var(--text-dim);max-width:72ch}
.company-faq-item[open]{border-color:rgba(255,87,34,.45)}
.loc-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-lg);padding:34px 30px;margin-top:30px}
.loc-card h3{font-family:var(--font-display);font-weight:800;text-transform:uppercase;font-size:24px;color:#fff;margin-bottom:14px}
.loc-card p{font-size:16px;color:var(--text-dim);margin-bottom:10px}
.loc-card .cta-row{margin-top:18px;display:flex;gap:12px;flex-wrap:wrap}
@media (max-width:900px){.values-grid{grid-template-columns:1fr}.award-row,.timeline-row{grid-template-columns:1fr;gap:8px}}"""

    body = f'''<main>
<section class="subpage abt">
{hero_picture(hero_image, en["abt.heroAlt"], "abt.heroAlt")}
<div aria-hidden="true" class="bg"></div>
<div class="container">
<div class="crumb"><a data-i18n="abt.breadHome" href="/">Home</a><span class="sep">→</span><span data-i18n="abt.h1Crumb">About</span></div>
<div class="h-eyebrow" data-i18n="abt.eyebrow" style="margin-bottom:18px">{en["abt.eyebrow"]}</div>
<h1 data-i18n-html="abt.h1">{en["abt.h1"]}</h1>
<p class="lead" data-i18n="abt.sub">{en["abt.sub"]}</p>
<div class="subpage-cta">
<a class="btn btn-primary" data-wa="" href="https://wa.me/351917961230" rel="noopener" target="_blank"><span data-i18n="abt.btnWA">{en["abt.btnWA"]}</span>{ARROW_SVG}</a>
<a class="btn btn-ghost" data-i18n="abt.btnSend" href="/contact/">{en["abt.btnSend"]}</a>
</div>
</div>
</section>
<section class="sub-section sub-intro">
<div class="container">
<div class="heading">
<span class="h-eyebrow" data-i18n="abt.storyEyebrow">{en["abt.storyEyebrow"]}</span>
<div><h2 data-i18n-html="abt.storyTitle">{en["abt.storyTitle"]}</h2></div>
</div>
<div>
<p data-i18n-html="abt.storyP1">{en["abt.storyP1"]}</p>
<p data-i18n-html="abt.storyP2">{en["abt.storyP2"]}</p>
<p data-i18n-html="abt.storyP3">{en["abt.storyP3"]}</p>
</div>
</div>
</section>
<section class="sub-section">
<div class="container">
<div class="heading">
<span class="h-eyebrow" data-i18n="abt.valuesEyebrow">{en["abt.valuesEyebrow"]}</span>
<div>
<h2 data-i18n-html="abt.valuesTitle">{en["abt.valuesTitle"]}</h2>
{values_lead_html}
</div>
</div>
<div class="values-grid">
{value_cards}
</div>
</div>
</section>
<section class="sub-section">
<div class="container">
<div class="heading">
<span class="h-eyebrow" data-i18n="abt.awardsEyebrow">{en["abt.awardsEyebrow"]}</span>
<div>
<h2 data-i18n-html="abt.awardsTitle">{en["abt.awardsTitle"]}</h2>
{awards_lead_html}
</div>
</div>
<div class="awards-list">
{award_rows}
</div>
</div>
</section>
<section class="sub-section">
<div class="container">
<div class="heading">
<span class="h-eyebrow" data-i18n="abt.timelineEyebrow">{en["abt.timelineEyebrow"]}</span>
<div>
<h2 data-i18n-html="abt.timelineTitle">{en["abt.timelineTitle"]}</h2>
{timeline_lead_html}
</div>
</div>
<div class="timeline-list">
{timeline_rows}
</div>
</div>
</section>
<section class="sub-section">
<div class="container">
<div class="heading">
<span class="h-eyebrow" data-i18n="abt.faqEyebrow">{en["abt.faqEyebrow"]}</span>
<div>
<h2 data-i18n-html="abt.faqTitle">{en["abt.faqTitle"]}</h2>
{faq_lead_html}
</div>
</div>
<div class="company-faq-list">
{faq_items}
</div>
</div>
</section>
<section class="sub-section">
<div class="container">
<div class="heading">
<span class="h-eyebrow" data-i18n="abt.locEyebrow">{en["abt.locEyebrow"]}</span>
<div>
<h2 data-i18n-html="abt.locTitle">{en["abt.locTitle"]}</h2>
<p class="lead" data-i18n="abt.locLead">{en["abt.locLead"]}</p>
</div>
</div>
<div class="loc-card">
<h3 data-i18n="abt.locAddress">{en["abt.locAddress"]}</h3>
<p data-i18n="abt.locHours">{en["abt.locHours"]}</p>
<div class="cta-row">
<a class="btn btn-primary" data-i18n="abt.locCta" href="/contact/">{en["abt.locCta"]}</a>
<a class="btn btn-ghost" href="https://maps.google.com/?q=R.+Ant%C3%B3nio+Jos%C3%A9+da+Silva+100+B+S%C3%A3o+Domingos+de+Rana" rel="noopener" target="_blank">Google Maps →</a>
</div>
</div>
</div>
</section>
<section class="cta-back">
<div class="container">
<span class="h-eyebrow" data-i18n="abt.ctaEyebrow">{en["abt.ctaEyebrow"]}</span>
<h2 data-i18n="abt.ctaTitle">{en["abt.ctaTitle"]}</h2>
<p class="lead" data-i18n="abt.ctaText">{en["abt.ctaText"]}</p>
<div class="btns">
<a class="btn btn-primary" data-wa="" href="https://wa.me/351917961230" rel="noopener" target="_blank"><span data-i18n="abt.btnWA">{en["abt.btnWA"]}</span>{ARROW_SVG}</a>
<a class="btn btn-ghost" data-i18n="abt.btnBack" href="/">{en["abt.btnBack"]}</a>
</div>
</div>
</section>
</main>'''

    html = head(page_id, "en", extra_styles=extra_css, json_ld_blocks=json_ld) + "\n<body>\n" + header_html() + body + footer_html() + end_html()
    out = SITE_ROOT / page_id / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    write_html_if_changed(out, html, preserve_body_shell=True, merge_page_i18n=True, preserve_downstream_head=True)
    return out


# =========================================================================
# /community/ — rider lounge and local motorcycle community
# =========================================================================

def render_community():
    page_id = "community"
    page_url = f"{DOMAIN}/{page_id}/"
    en = {**GLOBAL_I18N["en"], **PAGE_I18N[page_id]["en"]}

    json_ld = [
        {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "@id": page_url,
            "name": "More than a service. A place for riders, stories and motorcycle culture.",
            "description": PAGE_HEAD_META[page_id]["en"]["description"],
            "url": page_url,
            "isPartOf": {"@id": f"{DOMAIN}/#website"},
            "about": [
                {"@id": f"{DOMAIN}/#business"},
                {
                    "@type": "Place",
                    "name": "Iron Custom Motors rider lounge",
                    "address": "R. António José da Silva 100 B, 2785-253 São Domingos de Rana, Cascais, Portugal",
                },
            ],
        },
        breadcrumb_jsonld("Community", page_url),
    ]

    extra_css = """.subpage.comm{padding:140px 0 80px}
.subpage.comm .bg{position:absolute;inset:0;z-index:-1;background-size:cover;background-position:center;filter:saturate(.9) contrast(1.05) brightness(.46);""" + hero_background_css('/photos/lounge-1600.jpg') + """}
.comm-media{display:grid;grid-template-columns:1.1fr .9fr;gap:24px;margin-top:36px;align-items:stretch}
.comm-photo{border-radius:var(--radius-lg);overflow:hidden;border:1px solid var(--border);min-height:360px;background:#111}
.comm-photo img{width:100%;height:100%;object-fit:cover;display:block}
.comm-note{display:flex;flex-direction:column;justify-content:center;padding:34px 30px;border:1px solid var(--border);border-radius:var(--radius-lg);background:var(--surface)}
.comm-note h3{font-family:var(--font-display);font-weight:800;text-transform:uppercase;font-size:clamp(24px,3vw,40px);line-height:.98;color:#fff;margin-bottom:16px}
.comm-note h3 em{color:var(--accent);font-style:italic}
.comm-note p{color:var(--text-dim);font-size:16px;line-height:1.6}
.comm-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:16px;margin-top:30px}
.comm-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-lg);padding:24px 22px;min-height:190px}
.comm-card .num{font-family:var(--font-display);font-weight:800;color:var(--accent);font-size:28px;line-height:1;margin-bottom:12px}
.comm-card h3{font-family:var(--font-display);font-weight:800;text-transform:uppercase;font-size:20px;line-height:1.05;color:#fff;margin-bottom:10px}
.comm-card p{font-size:14px;color:var(--text-dim);line-height:1.55}
.comm-local{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:30px;align-items:stretch}
.comm-local .panel{border:1px solid var(--border);border-radius:var(--radius-lg);padding:30px 28px;background:var(--surface)}
.comm-local .panel h3{font-family:var(--font-display);font-weight:800;text-transform:uppercase;font-size:28px;color:#fff;margin-bottom:12px}
.comm-local .panel p{font-size:16px;color:var(--text-dim);line-height:1.6}
.comm-local .panel .cta-row{display:flex;gap:12px;flex-wrap:wrap;margin-top:22px}
.comm-local .photo{border-radius:var(--radius-lg);overflow:hidden;border:1px solid var(--border);background:#111}
.comm-local .photo img{width:100%;height:100%;object-fit:cover;display:block;min-height:360px}
@media (max-width:1200px){.comm-grid{grid-template-columns:repeat(3,1fr)}}
@media (max-width:900px){.comm-media,.comm-local{grid-template-columns:1fr}.comm-grid{grid-template-columns:1fr 1fr}}
@media (max-width:640px){.comm-grid{grid-template-columns:1fr}.comm-photo{min-height:260px}}"""

    cards = []
    for idx in range(1, 6):
        cards.append(f'''<article class="comm-card">
<div class="num">{idx:02d}</div>
<h3 data-i18n="community.f{idx}.t">{en[f"community.f{idx}.t"]}</h3>
<p data-i18n="community.f{idx}.d">{en[f"community.f{idx}.d"]}</p>
</article>''')

    body = f'''<main>
<section class="subpage comm">
<div aria-hidden="true" class="bg"></div>
<div class="container">
<div class="crumb"><a data-i18n="comm.breadHome" href="/">Home</a><span class="sep">→</span><span data-i18n="comm.h1Crumb">Community</span></div>
<div class="h-eyebrow" data-i18n="community.eyebrow" style="margin-bottom:18px">{en["community.eyebrow"]}</div>
<h1 data-i18n="community.title">{en["community.title"]}</h1>
<p class="lead" data-i18n="community.sub">{en["community.sub"]}</p>
<div class="subpage-cta">
<a class="btn btn-primary" data-i18n="comm.btnContact" href="/contact/">{en["comm.btnContact"]}</a>
<a class="btn btn-ghost" data-i18n="comm.btnProjects" href="/projects/">{en["comm.btnProjects"]}</a>
</div>
</div>
</section>
<section class="sub-section sub-intro">
<div class="container">
<div class="heading">
<span class="h-eyebrow" data-i18n="comm.storyEyebrow">{en["comm.storyEyebrow"]}</span>
<div>
<h2 data-i18n="comm.storyTitle">{en["comm.storyTitle"]}</h2>
<p class="lead" data-i18n="community.heroSub">{en["community.heroSub"]}</p>
</div>
</div>
<div class="comm-media">
<div class="comm-photo"><img alt="Iron Custom Motors rider lounge with championship motorcycle culture" loading="lazy" src="/photos/lounge-detail-1600.jpg" width="1600" height="1067"/></div>
<div class="comm-note">
<h3 data-i18n="community.heroTitle">{en["community.heroTitle"]}</h3>
<p data-i18n="community.introP1">{en["community.introP1"]}</p>
</div>
</div>
<p data-i18n="community.introP2" style="margin-top:28px">{en["community.introP2"]}</p>
<p data-i18n="community.introP3">{en["community.introP3"]}</p>
</div>
</section>
<section class="sub-section">
<div class="container">
<div class="heading">
<span class="h-eyebrow" data-i18n="comm.findEyebrow">{en["comm.findEyebrow"]}</span>
<div>
<h2 data-i18n="community.findTitle">{en["community.findTitle"]}</h2>
<p class="lead" data-i18n="comm.findLead">{en["comm.findLead"]}</p>
</div>
</div>
<div class="comm-grid">
{''.join(cards)}
</div>
</div>
</section>
<section class="sub-section">
<div class="container">
<div class="heading">
<span class="h-eyebrow" data-i18n="comm.localEyebrow">{en["comm.localEyebrow"]}</span>
<div>
<h2 data-i18n="comm.localTitle">{en["comm.localTitle"]}</h2>
<p class="lead" data-i18n="comm.localLead">{en["comm.localLead"]}</p>
</div>
</div>
<div class="comm-local">
<div class="panel">
<h3 data-i18n="community.promiseTitle">{en["community.promiseTitle"]}</h3>
<p data-i18n="community.promiseSub">{en["community.promiseSub"]}</p>
<div class="cta-row">
<a class="btn btn-primary" data-wa="" href="https://wa.me/351917961230" rel="noopener" target="_blank"><span data-i18n="comm.btnWA">{en["comm.btnWA"]}</span>{ARROW_SVG}</a>
<a class="btn btn-ghost" data-i18n="comm.btnProjects" href="/projects/">{en["comm.btnProjects"]}</a>
</div>
</div>
<div class="photo"><img alt="Inspirium Bonneville motorcycle displayed by Iron Custom Motors" loading="lazy" src="/photos/projects/inspirium-hero-1600.jpg" width="1600" height="1067"/></div>
</div>
</div>
</section>
<section class="cta-back">
<div class="container">
<span class="h-eyebrow" data-i18n="comm.ctaEyebrow">{en["comm.ctaEyebrow"]}</span>
<h2 data-i18n="comm.ctaTitle">{en["comm.ctaTitle"]}</h2>
<p class="lead" data-i18n="comm.ctaText">{en["comm.ctaText"]}</p>
<div class="btns">
<a class="btn btn-primary" data-i18n="comm.btnContact" href="/contact/">{en["comm.btnContact"]}</a>
<a class="btn btn-ghost" data-i18n="comm.btnBack" href="/">{en["comm.btnBack"]}</a>
</div>
</div>
</section>
</main>'''

    html = head(page_id, "en", extra_styles=extra_css, json_ld_blocks=json_ld) + "\n<body>\n" + header_html() + body + footer_html() + end_html()
    out = SITE_ROOT / page_id / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    write_html_if_changed(out, html, preserve_body_shell=True, merge_page_i18n=True, preserve_downstream_head=True)
    return out


# =========================================================================
# /contact/ — contacts + form anchor
# =========================================================================

def render_contact():
    page_id = "contact"
    page_url = f"{DOMAIN}/{page_id}/"
    en = PAGE_I18N[page_id]["en"]

    json_ld = [
        {
            "@context": "https://schema.org",
            "@type": "ContactPage",
            "name": "Get in touch.",
            "url": page_url,
            "isPartOf": {"@id": f"{DOMAIN}/#website"},
            "mainEntity": {"@id": f"{DOMAIN}/#business"},
        },
        breadcrumb_jsonld("Contact", page_url),
    ]

    extra_css = """.subpage.ctc{padding:140px 0 80px}
.subpage.ctc .bg{position:absolute;inset:0;z-index:-1;background-size:cover;background-position:center;filter:saturate(.85) contrast(1.05) brightness(.45);""" + hero_background_css('/photos/exterior-1600.jpg') + """}
.ctc-cards{display:grid;grid-template-columns:repeat(2,1fr);gap:20px;margin-top:30px}
.ctc-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-lg);padding:30px 28px;display:flex;flex-direction:column;gap:10px}
.ctc-card .icon{width:36px;height:36px;color:var(--accent);margin-bottom:8px}
.ctc-card h3{font-family:var(--font-display);font-weight:800;text-transform:uppercase;font-size:22px;color:#fff}
.ctc-card p{font-size:15px;color:var(--text-dim)}
.ctc-card .cta{margin-top:auto;display:inline-flex;align-items:center;gap:8px;font-family:var(--font-ui);font-weight:600;font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--accent)}
/* Whole-card click handling is done in main.js (CARD_PATTERNS) */
.hours-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-lg);padding:30px 28px;margin-top:30px;max-width:640px}
.hours-card .row{font-family:var(--font-ui);font-size:18px;color:#fff;padding:6px 0}
.hours-card .row:last-of-type{color:var(--text-dim)}
.hours-card .note{margin-top:16px;font-size:14px;color:var(--text-dim);font-style:italic}
.map-wrap{margin-top:30px;border-radius:var(--radius-lg);overflow:hidden;border:1px solid var(--border);aspect-ratio:16/8;background:#0a0a0a}
.map-wrap iframe{width:100%;height:100%;border:0;display:block}
@media (max-width:900px){.ctc-cards{grid-template-columns:1fr}.map-wrap{aspect-ratio:4/5}}"""

    map_q = "R.+Ant%C3%B3nio+Jos%C3%A9+da+Silva+100+B+S%C3%A3o+Domingos+de+Rana+Cascais"

    body = f'''<main>
<section class="subpage ctc">
<div aria-hidden="true" class="bg"></div>
<div class="container">
<div class="crumb"><a data-i18n="ctc.breadHome" href="/">Home</a><span class="sep">→</span><span data-i18n="ctc.h1Crumb">Contact</span></div>
<div class="h-eyebrow" data-i18n="ctc.eyebrow" style="margin-bottom:18px">{en["ctc.eyebrow"]}</div>
<h1 data-i18n="ctc.h1">{en["ctc.h1"]}</h1>
<p class="lead" data-i18n="ctc.sub">{en["ctc.sub"]}</p>
<div class="subpage-cta">
<a class="btn btn-primary" data-wa="" href="https://wa.me/351917961230" rel="noopener" target="_blank"><span data-i18n="ctc.btnWA">{en["ctc.btnWA"]}</span>{ARROW_SVG}</a>
</div>
</div>
</section>
<section class="sub-section">
<div class="container">
<div class="heading">
<span class="h-eyebrow" data-i18n="ctc.cardsEyebrow">{en["ctc.cardsEyebrow"]}</span>
<div><h2 data-i18n="ctc.cardsTitle">{en["ctc.cardsTitle"]}</h2></div>
</div>
<div class="ctc-cards">
<div class="ctc-card">
<svg class="icon" fill="currentColor" viewbox="0 0 24 24"><path d="M17.5 14.4c-.3-.2-1.7-.8-1.9-.9-.3-.1-.5-.2-.7.2-.2.3-.8 1-1 1.2-.2.2-.4.2-.6.1-1-.5-2.2-1.1-3.1-2.5-.7-1.2-.4-1.1.4-1.7.1-.1.2-.3.3-.5.1-.2 0-.4 0-.5-.1-.1-.7-1.6-.9-2.2-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.2.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.7-.7 1.9-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.4zM12 2C6.5 2 2 6.5 2 12c0 2 .6 3.8 1.6 5.4L2 22l4.7-1.6c1.5.9 3.4 1.6 5.3 1.6 5.5 0 10-4.5 10-10S17.5 2 12 2z"></path></svg>
<h3 data-i18n="ctc.c1t">{en["ctc.c1t"]}</h3>
<p data-i18n="ctc.c1d">{en["ctc.c1d"]}</p>
<a class="cta" data-wa="" data-i18n="ctc.c1cta" href="https://wa.me/351917961230" rel="noopener" target="_blank">{en["ctc.c1cta"]}</a>
</div>
<div class="ctc-card">
<svg class="icon" fill="none" stroke="currentColor" stroke-width="1.8" viewbox="0 0 24 24"><path d="M5 4h4l2 5-3 2c1 2 3 4 5 5l2-3 5 2v4c0 1-1 2-2 2-9 0-15-6-15-15 0-1 1-2 2-2z"></path></svg>
<h3 data-i18n="ctc.c2t">{en["ctc.c2t"]}</h3>
<p data-i18n="ctc.c2d">{en["ctc.c2d"]}</p>
<a class="cta" data-i18n="ctc.c2cta" href="tel:+351917961230">{en["ctc.c2cta"]}</a>
</div>
<div class="ctc-card">
<svg class="icon" fill="none" stroke="currentColor" stroke-width="1.8" viewbox="0 0 24 24"><rect height="14" rx="2" width="18" x="3" y="5"></rect><path d="M3 7l9 6 9-6"></path></svg>
<h3 data-i18n="ctc.c3t">{en["ctc.c3t"]}</h3>
<p data-i18n="ctc.c3d">{en["ctc.c3d"]}</p>
<a class="cta" data-i18n="ctc.c3cta" href="mailto:Ironcustom.office@gmail.com">{en["ctc.c3cta"]}</a>
</div>
<div class="ctc-card">
<svg class="icon" fill="none" stroke="currentColor" stroke-width="1.8" viewbox="0 0 24 24"><path d="M12 22s8-7 8-13a8 8 0 10-16 0c0 6 8 13 8 13z"></path><circle cx="12" cy="9" r="3"></circle></svg>
<h3 data-i18n="ctc.c4t">{en["ctc.c4t"]}</h3>
<p data-i18n="ctc.c4d">{en["ctc.c4d"]}</p>
<a class="cta" data-i18n="ctc.c4cta" href="https://maps.google.com/?q={map_q}" rel="noopener" target="_blank">{en["ctc.c4cta"]}</a>
</div>
</div>
</div>
</section>
<section class="sub-section">
<div class="container">
<div class="heading">
<span class="h-eyebrow" data-i18n="ctc.hoursEyebrow">{en["ctc.hoursEyebrow"]}</span>
<div><h2 data-i18n="ctc.hoursTitle">{en["ctc.hoursTitle"]}</h2></div>
</div>
<div class="hours-card">
<div class="row" data-i18n="ctc.hours1">{en["ctc.hours1"]}</div>
<div class="row" data-i18n="ctc.hours2">{en["ctc.hours2"]}</div>
<div class="note" data-i18n="ctc.hoursNote">{en["ctc.hoursNote"]}</div>
</div>
</div>
</section>
<section class="sub-section">
<div class="container">
<div class="heading">
<span class="h-eyebrow" data-i18n="ctc.mapEyebrow">{en["ctc.mapEyebrow"]}</span>
<div>
<h2 data-i18n="ctc.mapTitle">{en["ctc.mapTitle"]}</h2>
<p class="lead" data-i18n="ctc.mapAddress">{en["ctc.mapAddress"]}</p>
</div>
</div>
<div class="map-wrap">
<iframe allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q={map_q}&amp;output=embed" title="Iron Custom Motors workshop map"></iframe>
</div>
<div style="margin-top:18px"><a class="btn btn-ghost" data-i18n="ctc.mapCta" href="https://maps.google.com/?q={map_q}" rel="noopener" target="_blank">{en["ctc.mapCta"]}</a></div>
</div>
</section>
<section class="sub-section">
<div class="container">
<div class="heading">
<span class="h-eyebrow" data-i18n="ctc.formEyebrow">{en["ctc.formEyebrow"]}</span>
<div>
<h2 data-i18n="ctc.formTitle">{en["ctc.formTitle"]}</h2>
<p class="lead" data-i18n="ctc.formLead">{en["ctc.formLead"]}</p>
</div>
</div>
<div><a class="btn btn-primary" data-cta="book" data-i18n="ctc.formCta" href="#contact">{en["ctc.formCta"]}</a></div>
</div>
</section>
<section class="cta-back">
<div class="container">
<h2 data-i18n="ctc.ctaTitle">{en["ctc.ctaTitle"]}</h2>
<p class="lead" data-i18n="ctc.ctaText">{en["ctc.ctaText"]}</p>
<div class="btns">
<a class="btn btn-primary" data-wa="" href="https://wa.me/351917961230" rel="noopener" target="_blank"><span data-i18n="ctc.btnWA">{en["ctc.btnWA"]}</span>{ARROW_SVG}</a>
<a class="btn btn-ghost" data-i18n="ctc.btnBack" href="/">{en["ctc.btnBack"]}</a>
</div>
</div>
</section>
</main>'''

    html = head(page_id, "en", extra_styles=extra_css, json_ld_blocks=json_ld) + "\n<body>\n" + header_html() + body + footer_html() + end_html()
    out = SITE_ROOT / page_id / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    write_html_if_changed(out, html, preserve_body_shell=True, merge_page_i18n=True, preserve_downstream_head=True)
    return out


# =========================================================================
# /faq/ — FAQ
# =========================================================================

def render_faq():
    page_id = "faq"
    page_url = f"{DOMAIN}/{page_id}/"
    en = PAGE_I18N[page_id]["en"]
    faqs = FAQ_QA["en"]

    # FAQPage schema using EN questions
    faq_main_entity = [
        {"@type": "Question", "name": q["q"],
         "acceptedAnswer": {"@type": "Answer", "text": q["a"]}}
        for q in faqs
    ]

    json_ld = [
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "url": page_url,
            "mainEntity": faq_main_entity,
        },
        breadcrumb_jsonld("FAQ", page_url),
    ]

    extra_css = """.subpage.fq{padding:140px 0 80px}
.subpage.fq .bg{position:absolute;inset:0;z-index:-1;background-size:cover;background-position:center;filter:saturate(.85) contrast(1.05) brightness(.5);""" + hero_background_css('/photos/service-action-1600.jpg') + """}
.faq-list{display:grid;grid-template-columns:1fr;gap:14px;margin-top:30px}
.faq-item{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-lg);overflow:hidden}
.faq-item summary{cursor:pointer;list-style:none;padding:22px 26px;display:flex;align-items:flex-start;gap:18px;font-family:var(--font-display);font-weight:700;text-transform:uppercase;font-size:clamp(16px,1.4vw,20px);color:#fff;line-height:1.25;letter-spacing:.01em;transition:color .2s var(--ease)}
.faq-item summary:hover{color:var(--accent)}
.faq-item summary::-webkit-details-marker{display:none}
.faq-item .num{font-family:var(--font-display);font-weight:800;color:var(--accent);font-size:22px;min-width:36px;line-height:1}
.faq-item .q{flex:1}
.faq-item .chev{margin-left:14px;color:var(--text-dim);transition:transform .25s var(--ease);flex-shrink:0}
.faq-item[open] .chev{transform:rotate(180deg)}
.faq-item .a{padding:0 26px 22px 26px;color:var(--text-dim);font-size:15px;line-height:1.6;max-width:80ch;padding-left:80px}
@media (max-width:760px){.faq-item .a{padding-left:26px}}"""

    # Build FAQ items HTML (EN). For other langs, fill via ICM_I18N_PAGE keys.
    # Add the available fq.qN / fq.aN keys for each language.
    for lang in ["en", "ru", "uk", "pt"]:
        lang_faqs = FAQ_QA[lang]
        for i, qa in enumerate(lang_faqs, start=1):
            PAGE_I18N[page_id][lang][f"fq.q{i}"] = qa["q"]
            PAGE_I18N[page_id][lang][f"fq.a{i}"] = qa["a"]

    items_html = ""
    for i, qa in enumerate(faqs, start=1):
        items_html += f'''<details class="faq-item">
<summary>
<span class="num">{i:02d}</span>
<span class="q" data-i18n="fq.q{i}">{qa["q"]}</span>
<svg class="chev" fill="none" height="18" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="18"><path d="M6 9l6 6 6-6"></path></svg>
</summary>
<div class="a" data-i18n="fq.a{i}">{qa["a"]}</div>
</details>
'''

    body = f'''<main>
<section class="subpage fq">
<div aria-hidden="true" class="bg"></div>
<div class="container">
<div class="crumb"><a data-i18n="fq.breadHome" href="/">Home</a><span class="sep">→</span><span data-i18n="fq.h1Crumb">FAQ</span></div>
<div class="h-eyebrow" data-i18n="fq.eyebrow" style="margin-bottom:18px">{en["fq.eyebrow"]}</div>
<h1 data-i18n="fq.h1">{en["fq.h1"]}</h1>
<p class="lead" data-i18n="fq.sub">{en["fq.sub"]}</p>
<div class="subpage-cta">
<a class="btn btn-primary" data-wa="" href="https://wa.me/351917961230" rel="noopener" target="_blank"><span data-i18n="fq.btnWA">{en["fq.btnWA"]}</span>{ARROW_SVG}</a>
<a class="btn btn-ghost" data-i18n="fq.btnSend" href="/contact/">{en["fq.btnSend"]}</a>
</div>
</div>
</section>
<section class="sub-section">
<div class="container">
<div class="heading">
<span class="h-eyebrow" data-i18n="fq.listEyebrow">{en["fq.listEyebrow"]}</span>
<div>
<h2 data-i18n="fq.listTitle">{en["fq.listTitle"]}</h2>
<p class="lead" data-i18n="fq.listLead">{en["fq.listLead"]}</p>
</div>
</div>
<div class="faq-list">
{items_html}
</div>
</div>
</section>
<section class="cta-back">
<div class="container">
<span class="h-eyebrow" data-i18n="fq.ctaEyebrow">{en["fq.ctaEyebrow"]}</span>
<h2 data-i18n="fq.ctaTitle">{en["fq.ctaTitle"]}</h2>
<p class="lead" data-i18n="fq.ctaText">{en["fq.ctaText"]}</p>
<div class="btns">
<a class="btn btn-primary" data-wa="" href="https://wa.me/351917961230" rel="noopener" target="_blank"><span data-i18n="fq.btnWA">{en["fq.btnWA"]}</span>{ARROW_SVG}</a>
<a class="btn btn-ghost" data-i18n="fq.btnBack" href="/">{en["fq.btnBack"]}</a>
</div>
</div>
</section>
</main>'''

    html = head(page_id, "en", extra_styles=extra_css, json_ld_blocks=json_ld) + "\n<body>\n" + header_html() + body + footer_html() + end_html()
    out = SITE_ROOT / page_id / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    write_html_if_changed(out, html, preserve_body_shell=True, merge_page_i18n=True, preserve_downstream_head=True)
    return out


def main():
    outs = [
        render_thank_you(),
        render_services(),
        render_projects(),
        render_about(),
        render_community(),
        render_contact(),
        render_faq(),
    ]
    for o in outs:
        size = o.stat().st_size
        print(f"  wrote {o.relative_to(SITE_ROOT)} ({size} bytes)")
    print(f"Done. {len(outs)} EN pages written.")


if __name__ == "__main__":
    main()
