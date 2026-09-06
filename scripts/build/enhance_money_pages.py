#!/usr/bin/env python3
"""Add reusable local SEO and related-page blocks to commercial service pages."""

import json
import re
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup, FeatureNotFound

from build_output import write_html_if_changed
from brand_pages_data import BRAND_NAME, BRAND_NAV_KEYS, BRAND_ORDER

SITE_ROOT = Path(__file__).resolve().parents[2]
BUILD_DIR = Path(__file__).resolve().parent
TARGET_LANGS = ["en", "ru", "uk", "pt"]

try:
    BeautifulSoup("", "lxml")
    HTML_PARSER = "lxml"
except FeatureNotFound:
    HTML_PARSER = "html.parser"

GLOBAL_I18N = json.loads((BUILD_DIR / "i18n.json").read_text(encoding="utf-8"))

COMMON_I18N = {
    "en": {
        "seo.localEyebrow": "Local service area",
        "seo.localTitle": "Serving Cascais, Lisbon <em>and Greater Lisbon.</em>",
        "seo.localLead": "Iron Custom Motors is based in São Domingos de Rana, Cascais. We work with riders from Cascais, Estoril, Oeiras, Sintra, Lisbon and the wider Greater Lisbon area.",
        "seo.area1t": "Cascais workshop",
        "seo.area1d": "A real workshop and client lounge, not a remote parts counter. Book service, drop off the bike, or visit to discuss a project.",
        "seo.area2t": "Multilingual process",
        "seo.area2d": "English, Russian, Ukrainian and Portuguese communication with written estimates and clear next steps. See our <a href=\"/english-speaking-motorcycle-workshop/\">expat service hub</a>.",
        "seo.area3t": "One accountable path",
        "seo.area3d": "Diagnostics, parts sourcing, installation, upgrades and follow-up happen under one workshop standard.",
        "seo.relatedEyebrow": "Related workshop paths",
        "seo.relatedTitle": "Continue through the <em>same service system.</em>",
        "seo.relatedLead": "These pages connect the most common next steps: service, parts, upgrades, pricing, brand-specific help and the rider lounge.",
        "seo.relatedText": "Open the related page for details, process, pricing context and booking options.",
        "seo.otherBrandsTitle": "Other brands we service.",
        "seo.otherBrandsLead": "Compare the same workshop process across our brand-specific service pages.",
        "seo.otherBrandText": "Open the brand page for model-specific service details, diagnostics, parts and booking context.",
    },
    "ru": {
        "seo.localEyebrow": "Локальная зона сервиса",
        "seo.localTitle": "Работаем для Cascais, Lisbon <em>и Большого Лиссабона.</em>",
        "seo.localLead": "Iron Custom Motors находится в São Domingos de Rana, Cascais. Мы работаем с райдерами из Cascais, Estoril, Oeiras, Sintra, Lisbon и всего Greater Lisbon.",
        "seo.area1t": "Мастерская в Cascais",
        "seo.area1d": "Реальная мастерская и клиентский lounge, а не удалённая стойка запчастей. Можно записаться на сервис, оставить мотоцикл или приехать обсудить проект.",
        "seo.area2t": "Процесс на вашем языке",
        "seo.area2d": "Английский, русский, украинский и португальский, письменные сметы и понятные следующие шаги. Смотрите <a href=\"/english-speaking-motorcycle-workshop/\">страницу для экспатов</a>.",
        "seo.area3t": "Одна точка ответственности",
        "seo.area3d": "Диагностика, подбор запчастей, установка, апгрейды и сопровождение идут по одному стандарту мастерской.",
        "seo.relatedEyebrow": "Связанные направления",
        "seo.relatedTitle": "Двигайтесь дальше в <em>той же системе сервиса.</em>",
        "seo.relatedLead": "Эти страницы связывают самые частые следующие шаги: сервис, запчасти, апгрейды, цены, брендовые страницы и rider lounge.",
        "seo.relatedText": "Откройте связанную страницу, чтобы посмотреть детали, процесс, контекст цены и варианты записи.",
        "seo.otherBrandsTitle": "Другие марки, которые обслуживаем.",
        "seo.otherBrandsLead": "Сравните тот же процесс мастерской на брендовых страницах сервиса.",
        "seo.otherBrandText": "Откройте страницу бренда, чтобы увидеть сервисные детали по моделям, диагностике, запчастям и записи.",
    },
    "uk": {
        "seo.localEyebrow": "Локальна зона сервісу",
        "seo.localTitle": "Працюємо для Cascais, Lisbon <em>і Великого Лісабона.</em>",
        "seo.localLead": "Iron Custom Motors знаходиться у São Domingos de Rana, Cascais. Ми працюємо з райдерами з Cascais, Estoril, Oeiras, Sintra, Lisbon і всього Greater Lisbon.",
        "seo.area1t": "Майстерня у Cascais",
        "seo.area1d": "Реальна майстерня і клієнтський lounge, а не віддалена стійка запчастин. Можна записатися на сервіс, залишити мотоцикл або приїхати обговорити проєкт.",
        "seo.area2t": "Процес вашою мовою",
        "seo.area2d": "Англійська, російська, українська і португальська, письмові кошториси і зрозумілі наступні кроки. Дивіться <a href=\"/english-speaking-motorcycle-workshop/\">сторінку для експатів</a>.",
        "seo.area3t": "Одна точка відповідальності",
        "seo.area3d": "Діагностика, підбір запчастин, встановлення, апґрейди і супровід ідуть за одним стандартом майстерні.",
        "seo.relatedEyebrow": "Пов'язані напрямки",
        "seo.relatedTitle": "Рухайтесь далі у <em>тій самій системі сервісу.</em>",
        "seo.relatedLead": "Ці сторінки пов'язують найчастіші наступні кроки: сервіс, запчастини, апґрейди, ціни, брендові сторінки і rider lounge.",
        "seo.relatedText": "Відкрийте пов'язану сторінку, щоб побачити деталі, процес, контекст ціни і варіанти запису.",
        "seo.otherBrandsTitle": "Інші марки, які обслуговуємо.",
        "seo.otherBrandsLead": "Порівняйте той самий процес майстерні на брендових сторінках сервісу.",
        "seo.otherBrandText": "Відкрийте сторінку бренду, щоб побачити сервісні деталі за моделями, діагностикою, запчастинами й записом.",
    },
    "pt": {
        "seo.localEyebrow": "Área local de serviço",
        "seo.localTitle": "Servimos Cascais, Lisboa <em>e a Grande Lisboa.</em>",
        "seo.localLead": "A Iron Custom Motors fica em São Domingos de Rana, Cascais. Trabalhamos com riders de Cascais, Estoril, Oeiras, Sintra, Lisboa e toda a Grande Lisboa.",
        "seo.area1t": "Oficina em Cascais",
        "seo.area1d": "Uma oficina real com lounge para clientes, não um balcão remoto de peças. Marque serviço, deixe a moto ou visite para discutir um projeto.",
        "seo.area2t": "Processo multilingue",
        "seo.area2d": "Comunicação em inglês, russo, ucraniano e português, com orçamentos escritos e próximos passos claros. Veja a <a href=\"/english-speaking-motorcycle-workshop/\">página para expatriados</a>.",
        "seo.area3t": "Uma rota responsável",
        "seo.area3d": "Diagnóstico, sourcing de peças, instalação, upgrades e acompanhamento seguem o mesmo padrão de oficina.",
        "seo.relatedEyebrow": "Caminhos relacionados",
        "seo.relatedTitle": "Continue no <em>mesmo sistema de serviço.</em>",
        "seo.relatedLead": "Estas páginas ligam os próximos passos mais comuns: serviço, peças, upgrades, preços, ajuda por marca e rider lounge.",
        "seo.relatedText": "Abra a página relacionada para detalhes, processo, contexto de preço e opções de marcação.",
        "seo.otherBrandsTitle": "Outras marcas que servimos.",
        "seo.otherBrandsLead": "Compare o mesmo processo de oficina nas nossas páginas de serviço por marca.",
        "seo.otherBrandText": "Abra a página da marca para detalhes de serviço por modelo, diagnóstico, peças e marcação.",
    },
}

PAGES = {
    "parts": {
        "path": "parts/index.html",
        "related": [
            ("services.s1.title", "/motorcycle-service/", "Motorcycle service & repair"),
            ("services.s3.title", "/upgrades-tuning/", "Upgrades & tuning"),
            ("nav.pricing", "/pricing/", "Pricing"),
            ("nav.community", "/community/", "Community"),
        ],
    },
    "upgrades-tuning": {
        "path": "upgrades-tuning/index.html",
        "related": [
            ("services.s1.title", "/motorcycle-service/", "Motorcycle service & repair"),
            ("services.s2.title", "/parts/", "Parts & consumables"),
            ("services.s4.title", "/custom/", "Custom & special projects"),
            ("nav.pricing", "/pricing/", "Pricing"),
        ],
    },
}

def parse_html(markup: str) -> BeautifulSoup:
    return BeautifulSoup(markup, HTML_PARSER)


def replace_html(el, html: str):
    fragment = BeautifulSoup(html, "html.parser")
    container = fragment
    el.clear()
    for child in list(container.children):
        el.append(child)


def load_inline_i18n(soup) -> tuple[dict, object]:
    for script in soup.find_all("script"):
        text = script.string or ""
        match = re.search(r"window\.ICM_I18N_PAGE\s*=\s*(\{.*?\});", text, re.DOTALL)
        if not match:
            continue
        return json.loads(match.group(1)), script
    data = {lang: {} for lang in TARGET_LANGS}
    script = soup.new_tag("script")
    script.string = "window.ICM_I18N_PAGE = {};".format(json.dumps(data, ensure_ascii=False))
    soup.head.append(script)
    return data, script


def merge_i18n(page_i18n: dict):
    for lang in TARGET_LANGS:
        page_i18n.setdefault(lang, {})
        page_i18n[lang].update(COMMON_I18N[lang])


def sync_en_text(soup):
    full = {**GLOBAL_I18N["en"], **COMMON_I18N["en"]}
    for el in soup.find_all(attrs={"data-i18n": True}):
        key = el["data-i18n"]
        if key in full:
            replace_html(el, full[key])


def insert_css(soup):
    style = soup.find("style")
    if style is None or ".trust-row" in (style.string or ""):
        return
    style.string = (style.string or "") + """
.trust-row{display:grid;grid-template-columns:30px 1fr;gap:26px;padding:24px 0;border-bottom:1px solid var(--border);align-items:start;transition:padding-left .25s var(--ease)}
.trust-row:hover{padding-left:10px}
.trust-row .bullet{width:14px;height:14px;background:var(--accent);clip-path:polygon(0 0, 100% 0, 100% 70%, 70% 100%, 0 100%);margin-top:6px}
.trust-row h4{margin-bottom:8px;color:#fff;font-size:clamp(16px,1.4vw,20px)}
.trust-row p{font-size:15px;color:var(--text-dim);max-width:64ch}
.proc-row{display:grid;grid-template-columns:80px 1fr;gap:30px;padding:24px 0;border-bottom:1px solid var(--border);align-items:start}
.proc-row .num{font-family:var(--font-display);font-weight:800;font-size:28px;color:var(--accent);line-height:1}
.proc-row h4{margin-bottom:6px;color:#fff;font-size:clamp(16px,1.4vw,20px)}
.proc-row h4 a{color:#fff;text-decoration:none}
.proc-row h4 a:hover{color:var(--accent)}
.proc-row p{font-size:14px;color:var(--text-dim);max-width:60ch}
.related-card-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:24px}
.related-card{position:relative;display:flex;min-height:128px;flex-direction:column;justify-content:space-between;gap:18px;padding:20px 18px;border:1px solid var(--border);border-radius:16px;background:var(--surface);color:#fff;text-decoration:none;overflow:hidden;transition:transform .25s var(--ease),border-color .25s var(--ease),background .25s var(--ease)}
.related-card::after{content:"";position:absolute;inset:0;background:radial-gradient(circle at 80% 10%,rgba(255,87,34,.16),transparent 52%);opacity:0;transition:opacity .25s var(--ease);pointer-events:none}
.related-card:hover,.related-card:focus-visible{transform:translateY(-4px);border-color:var(--accent);background:var(--surface-2);outline:none}
.related-card:hover::after,.related-card:focus-visible::after{opacity:1}
.related-card-label{position:relative;z-index:1;font-family:var(--font-display);font-weight:800;text-transform:uppercase;font-size:clamp(17px,1.35vw,22px);line-height:1;color:#fff}
.related-card-text{position:relative;z-index:1;font-size:13px;line-height:1.45;color:var(--text-dim);max-width:26ch}
.related-card-arrow{position:relative;z-index:1;align-self:flex-start;font-family:var(--font-ui);font-weight:700;color:var(--accent);letter-spacing:.08em}
.related-subhead{margin:36px 0 14px;padding-top:20px;border-top:1px solid var(--border)}
.related-subhead h3{font-family:var(--font-display);font-weight:800;text-transform:uppercase;font-size:clamp(20px,2vw,30px);line-height:1;color:#fff;margin-bottom:8px}
.related-subhead p{font-size:14px;color:var(--text-dim);max-width:62ch}
.brand-pill-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.brand-pill{display:flex;min-height:58px;align-items:center;justify-content:space-between;gap:14px;padding:15px 16px;border:1px solid var(--border);border-radius:14px;background:rgba(255,255,255,.035);font-family:var(--font-ui);font-weight:700;text-transform:uppercase;letter-spacing:.08em;font-size:13px;color:#fff;text-decoration:none;transition:transform .25s var(--ease),border-color .25s var(--ease),background .25s var(--ease),color .25s var(--ease)}
.brand-pill::after{content:"→";color:var(--accent);font-size:16px;line-height:1}
.brand-pill:hover,.brand-pill:focus-visible{transform:translateY(-3px);border-color:var(--accent);background:rgba(255,87,34,.08);color:var(--accent);outline:none}
@media (max-width:900px){.related-card-grid,.brand-pill-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:760px){.proc-row{grid-template-columns:50px 1fr;gap:18px}.proc-row .num{font-size:24px}.related-card-grid,.brand-pill-grid{grid-template-columns:1fr}.related-card{min-height:112px}.trust-row{grid-template-columns:20px 1fr;gap:16px}}
"""


def related_rows(links):
    rows = []
    for idx, (key, href, fallback) in enumerate(links, start=1):
        label = GLOBAL_I18N["en"].get(key, fallback)
        rows.append(f'''<article class="proc-row">
<span class="num">{idx:02d}</span>
<div>
<h4><a data-i18n="{key}" href="{href}">{label}</a></h4>
<p data-i18n="seo.relatedText">{COMMON_I18N["en"]["seo.relatedText"]}</p>
</div>
</article>''')
    return "\n".join(rows)


def other_brand_rows(slug: Optional[str], start: int) -> str:
    if slug not in BRAND_ORDER:
        return ""

    rows = [
        f'''<div class="related-subhead">
<h3 data-i18n="seo.otherBrandsTitle">{COMMON_I18N["en"]["seo.otherBrandsTitle"]}</h3>
<p data-i18n="seo.otherBrandsLead">{COMMON_I18N["en"]["seo.otherBrandsLead"]}</p>
</div>'''
    ]
    for idx, other_slug in enumerate((item for item in BRAND_ORDER if item != slug), start=start):
        rows.append(f'''<article class="proc-row">
<span class="num">{idx:02d}</span>
<div>
<h4><a data-i18n="{BRAND_NAV_KEYS[other_slug]}" href="/{other_slug}/">{BRAND_NAME[other_slug]}</a></h4>
<p data-i18n="seo.otherBrandText">{COMMON_I18N["en"]["seo.otherBrandText"]}</p>
</div>
</article>''')
    return "\n".join(rows)


def brand_related_cards(links):
    cards = []
    for key, href, fallback in links:
        label = GLOBAL_I18N["en"].get(key, fallback)
        cards.append(f'''<a class="related-card" href="{href}">
<span class="related-card-label" data-i18n="{key}">{label}</span>
<span class="related-card-text" data-i18n="seo.relatedText">{COMMON_I18N["en"]["seo.relatedText"]}</span>
<span aria-hidden="true" class="related-card-arrow">→</span>
</a>''')
    return "\n".join(cards)


def other_brand_cards(slug: Optional[str]) -> str:
    if slug not in BRAND_ORDER:
        return ""

    cards = [
        f'''<div class="related-subhead">
<h3 data-i18n="seo.otherBrandsTitle">{COMMON_I18N["en"]["seo.otherBrandsTitle"]}</h3>
<p data-i18n="seo.otherBrandsLead">{COMMON_I18N["en"]["seo.otherBrandsLead"]}</p>
</div>'''
    ]
    cards.append('<div class="brand-pill-grid">')
    cards.extend(
        f'''<a class="brand-pill" data-i18n="{BRAND_NAV_KEYS[other_slug]}" href="/{other_slug}/">{BRAND_NAME[other_slug]}</a>'''
        for other_slug in (item for item in BRAND_ORDER if item != slug)
    )
    cards.append("</div>")
    return "\n".join(cards)


def enhancement_html(links, slug: Optional[str] = None):
    if slug in BRAND_ORDER:
        related_content = f'''<div class="related-card-grid">
{brand_related_cards(links)}
</div>
{other_brand_cards(slug)}'''
        related_wrapper_attrs = 'class="reveal-stagger"'
    else:
        related_content = f'''{related_rows(links)}
{other_brand_rows(slug, len(links) + 1)}'''
        related_wrapper_attrs = 'class="reveal-stagger" style="max-width:900px"'

    return f'''<section class="sub-section" data-enhancement="money-local">
<div class="container">
<div class="heading reveal">
<span class="h-eyebrow" data-i18n="seo.localEyebrow">{COMMON_I18N["en"]["seo.localEyebrow"]}</span>
<div>
<h2 data-i18n="seo.localTitle">{COMMON_I18N["en"]["seo.localTitle"]}</h2>
<p class="lead" data-i18n="seo.localLead">{COMMON_I18N["en"]["seo.localLead"]}</p>
</div>
</div>
<div class="reveal-stagger">
<div class="trust-row"><span class="bullet"></span><div><h4 data-i18n="seo.area1t">{COMMON_I18N["en"]["seo.area1t"]}</h4><p data-i18n="seo.area1d">{COMMON_I18N["en"]["seo.area1d"]}</p></div></div>
<div class="trust-row"><span class="bullet"></span><div><h4 data-i18n="seo.area2t">{COMMON_I18N["en"]["seo.area2t"]}</h4><p data-i18n="seo.area2d">{COMMON_I18N["en"]["seo.area2d"]}</p></div></div>
<div class="trust-row"><span class="bullet"></span><div><h4 data-i18n="seo.area3t">{COMMON_I18N["en"]["seo.area3t"]}</h4><p data-i18n="seo.area3d">{COMMON_I18N["en"]["seo.area3d"]}</p></div></div>
</div>
</div>
</section>
<section class="sub-section" data-enhancement="money-related">
<div class="container">
<div class="heading reveal">
<span class="h-eyebrow" data-i18n="seo.relatedEyebrow">{COMMON_I18N["en"]["seo.relatedEyebrow"]}</span>
<div>
<h2 data-i18n="seo.relatedTitle">{COMMON_I18N["en"]["seo.relatedTitle"]}</h2>
<p class="lead" data-i18n="seo.relatedLead">{COMMON_I18N["en"]["seo.relatedLead"]}</p>
</div>
</div>
<div {related_wrapper_attrs}>
{related_content}
</div>
</div>
</section>'''


def process_page(slug: str, config: dict) -> bool:
    path = SITE_ROOT / config["path"]
    if not path.exists():
        print(f"  SKIP missing: {config['path']}")
        return False

    soup = parse_html(path.read_text(encoding="utf-8"))
    for old in soup.find_all(attrs={"data-enhancement": re.compile(r"^money-")}):
        old.decompose()

    insert_css(soup)
    page_i18n, script = load_inline_i18n(soup)
    merge_i18n(page_i18n)
    script.string = f"window.ICM_I18N_PAGE = {json.dumps(page_i18n, ensure_ascii=False)};"

    target = soup.find("section", class_="cross-link") or soup.find("section", class_="cta-back")
    if target is None:
        print(f"  SKIP no insertion point: {config['path']}")
        return False

    fragment = parse_html(enhancement_html(config["related"], slug))
    new_sections = [child for child in (fragment.body or fragment).children if getattr(child, "name", None)]
    for section in reversed(new_sections):
        target.insert_before(section)

    sync_en_text(soup)
    write_html_if_changed(path, str(soup))
    print(f"  enhanced: {config['path']}")
    return True


def main():
    changed = 0
    for slug, config in PAGES.items():
        if process_page(slug, config):
            changed += 1
    print(f"\nDone. {changed}/{len(PAGES)} money pages enhanced.")


if __name__ == "__main__":
    main()
