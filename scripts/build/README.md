# Build And Validation Commands

This is the only documentation file that owns build and validator commands.
Page-family ownership lives in `docs/CONTENT_TYPES.md`; current inventories and
cache-bust values live in `docs/PROJECT_STATE.md`.

Run commands from the repository root. Scripts resolve `SITE_ROOT` from their
location, but the pricing PDF generator also depends on macOS system fonts.

## Environment

Requirements:

- Python 3.10 or newer. The source uses PEP 604 union syntax.
- Node.js 14 or newer for `extract_i18n.js` and JavaScript syntax checks.
- Python packages from `requirements.txt`.
- macOS Arial files under `/System/Library/Fonts/Supplemental/` for
  `build_pricing_pdfs.py` and therefore for the complete rebuild.

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
test -f '/System/Library/Fonts/Supplemental/Arial.ttf'
test -f '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
test -f '/System/Library/Fonts/Supplemental/Arial Italic.ttf'
```

If PDF output is intentionally outside the task, the HTML generators do not
need those font files. Do not call an HTML-only run a “full rebuild.” The open
cross-platform PDF risk is tracked in `docs/OPEN_TASKS.md`.

## Script Ownership Inventory

Every executable or importable source file at the top level of `scripts/build/`
is listed below. “Broad SEO” means `validate_seo.py`; it does not imply exact
copy or business-semantic validation.

### Page And Artifact Generators

| Script | Maintained input | Direct output | Focused protection |
|---|---|---|---|
| `build_new_pages.py` | `new_pages_data.py`, existing chrome | English general hub pages | broad SEO |
| `build_authorized_dealer.py` | `authorized_dealer_data.py`, existing chrome | localized Authorized Dealer family | broad SEO; no dedicated validator |
| `build_brand_pages.py` | `brand_pages_data.py` | English registered brand pages | `validate_brand_pages.py` |
| `build_legal_pages.py` | `legal_pages_data.py`, service chrome | localized legal pages | broad SEO; no legal-copy validator |
| `build_news.py` | `news_data.py` | English news hub/articles | broad SEO and focused CSS-hero mode; no exact-copy validator |
| `build_blog.py` | `blog_data.py`, approved content files | English blog hub/articles | broad SEO and focused picture-hero mode; no exact-copy validator |
| `build_project_pages.py` | `project_pages_data.py`, approved project Markdown and localized project data | all localized project pages and noindex legacy redirects | `validate_project_pages.py` |
| `build_service_custom_hubs.py` | approved Service/Custom hub Markdown | localized Service and Custom hubs | `validate_service_custom_hubs.py` |
| `build_pre_purchase_inspection.py` | approved inspection Markdown | localized inspection pages | broad SEO; no exact-copy validator |
| `build_expat_hub.py` | approved expat Markdown | localized expat hub | broad SEO; no exact-copy validator |
| `build_harley_hub.py` | approved Harley Markdown, `harley_hub_data.py` | localized Harley family | `validate_harley_hub.py` |
| `build_pricing.py` | `pricing_data.py`, `i18n.json`, service chrome | localized pricing HTML | broad SEO plus Wave 1 metadata/price-parity checks in `validate_service_custom_hubs.py` |
| `build_pricing_pdfs.py` | `pricing_data.py`, macOS Arial fonts | localized pricing PDFs | internal PDF assertions only |
| `build_tyre_service.py` | approved tyre-service Markdown | localized tyre-service pages | broad SEO; no exact-copy validator |
| `build_i18n.py` | English sources, `page_meta.py`, `i18n.json` | generic localized page variants | broad SEO and family validators |
| `build_sitemap.py` | `PAGES`, language maps, article dates, Git history | `sitemap.xml` | broad SEO checks URL/file alignment, not date semantics |
| `build_llms.py` | sitemap/content registries, metadata, I18N labels, `BUSINESS_FACTS.md` | `llms.txt` | internal generator assertions and broad SEO coverage |
| `build_reviews_schema.py` | Reviews Worker, snapshot, curated reviews | snapshot and home review HTML/JSON-LD | broad SEO; no live-service validator |

### Post-Processors And Media Tools

| Script | Maintained input | Direct output | Focused protection |
|---|---|---|---|
| `nav_patch.py` | `site_chrome.py`, sitemap registry | navigation/footer on sitemap HTML | broad SEO chrome parity |
| `enhance_money_pages.py` | configured commercial page map | related/local blocks in owned pages | broad SEO only |
| `localize_internal_links.py` | `LOCALIZED_PATHS` | same-language links in localized HTML | broad SEO locality |
| `add_image_dims.py` | local image files | width/height on HTML images | broad SEO asset checks |
| `apply_seo_meta.py` | sitemap HTML, `seo_meta.py`, `hero_images.py` | robots/LCP/preload normalization and canonical-byte restoration when the final DOM matches tracked output | broad SEO and focused hero modes |
| `extract_i18n.js` | `assets/main.js` `I18N` | `i18n.json` | consumers and broad SEO pre-render checks |
| `optimize_hero_images.py` | a registered brand slug or local source image | responsive hero variants | family asset checks where implemented |
| `optimize_tyre_service_images.py` | tyre media sources and checksum manifest | tyre responsive variants and manifest | source checksum/idempotence logic |
| `import_project_images.py` | registered project config and source directory | responsive project hero/gallery media | project validator |
| `optimize_project_exhibition_images.py` | registered exhibition media config and one approved source image | responsive exhibition AVIF/WebP/JPEG variants | project validator |

Binary media tools are intentionally outside the full rebuild. Codec versions
can change encoded bytes without a source change; run them only when approved
source media changes and review the binary diff.

### Data And Shared Modules

| Module | Owner / consumers |
|---|---|
| `authorized_dealer_data.py` | Authorized Dealer copy, hero and partner registry |
| `blog_data.py` | blog registry, localized article content and media/schema inputs |
| `brand_pages_data.py` | brand registry, metadata and localized page content |
| `harley_hub_data.py` | Harley UI, media, feed and portfolio data |
| `legal_pages_data.py` | legal copy and update label |
| `new_pages_data.py` | general hubs and project listing registry |
| `news_data.py` | news registry and localized article content |
| `page_meta.py` | generic localized page metadata |
| `pricing_data.py` | shared HTML/PDF pricing data |
| `project_pages_data.py` | complete project/redirect registry, localized legacy data and Markdown parser |
| `build_output.py` | semantic/idempotent file writers |
| `hero_images.py` | hero discovery, responsive rendering and alignment helpers |
| `seo_meta.py` | shared SEO meta constants/helpers |
| `site_chrome.py` | canonical desktop/mobile navigation and footer renderer |

Content Markdown and JSON files under `scripts/build/content/` and
`scripts/build/*.json` are data, not standalone executables. Their owning
module is named above or in `docs/CONTENT_TYPES.md`.

### Validators

| Script | What it protects | Important exclusions |
|---|---|---|
| `validate_seo.py` | all built HTML FormSubmit-action privacy and localized `_next` redirects; noindex thank-you exclusion; cookie-free lead runtime; sitemap files; title/meta; canonical/hreflang; JSON parsing and breadcrumbs; localized JSON-LD URLs; local assets; cache-bust presence/consistency; LCP discovery; CSS hero alignment; Blog picture preload/source alignment and viewport/DPR candidate selection; navigation/footer structure; project-menu registry membership, localized URLs and order; same-language chrome-text parity; localized links; English `llms.txt` coverage; changelog commit references | Rich Results UI; schema recommended fields; global visible FAQ parity; Product/Offer semantics; real lastmod meaning; visual rendering; external services; measured performance |
| `validate_brand_pages.py` | brand registry and assets; generated variants; schema type presence; sitemap/deploy wiring; homepage and reciprocal links; forbidden brand claims | exact visible copy; global RRT warnings; browser interaction/performance |
| `validate_harley_hub.py` | exact maintained copy; visual tokens; hero media; schema families; language-local links; feed/portfolio and required integrations | live browser behavior; external RRT; performance benefit |
| `validate_project_pages.py` | every registered project: exact source copy; media; schema graph/dates/references; cache-bust; redirects; listing/sitemap and optional Custom/Harley integration | browser rendering; external RRT |

Scripts or data families without a dedicated validator rely on broad SEO plus
manual/source review. This is a known coverage boundary, not proof of failure.

## Full Safe Rebuild

Use this on macOS after structural source changes or as the reproducibility
gate. It excludes network-backed reviews and binary media optimization.

```bash
node scripts/build/extract_i18n.js
python3 scripts/build/build_new_pages.py
python3 scripts/build/build_authorized_dealer.py
python3 scripts/build/build_brand_pages.py
python3 scripts/build/build_legal_pages.py
python3 scripts/build/build_news.py
python3 scripts/build/build_blog.py
python3 scripts/build/build_project_pages.py
python3 scripts/build/build_pre_purchase_inspection.py
python3 scripts/build/build_expat_hub.py
python3 scripts/build/build_harley_hub.py
python3 scripts/build/build_pricing.py
python3 scripts/build/build_pricing_pdfs.py
python3 scripts/build/build_tyre_service.py
python3 scripts/build/build_service_custom_hubs.py
python3 scripts/build/build_i18n.py
python3 scripts/build/nav_patch.py
python3 scripts/build/enhance_money_pages.py
python3 scripts/build/localize_internal_links.py
python3 scripts/build/add_image_dims.py
python3 scripts/build/apply_seo_meta.py
python3 scripts/build/build_sitemap.py
python3 scripts/build/build_llms.py
python3 scripts/build/validate_seo.py
python3 scripts/build/validate_brand_pages.py
python3 scripts/build/validate_harley_hub.py
python3 scripts/build/validate_service_custom_hubs.py
for slug in $(python3 -c "import sys; sys.path.insert(0, 'scripts/build'); from project_pages_data import PROJECT_CONFIGS; print(' '.join(sorted(PROJECT_CONFIGS)))"); do
  python3 scripts/build/validate_project_pages.py "$slug"
done
```

Run `git status --short` afterward. A clean clone at the current commit must
remain clean after this sequence. If it does not, inspect the generated diff;
do not discard it blindly.

## Broad Verification

```bash
node --check assets/main.js
node --check assets/projects.js
node --check worker/reviews.js
python3 -m py_compile scripts/build/*.py
python3 scripts/build/validate_seo.py
python3 scripts/build/validate_brand_pages.py
python3 scripts/build/validate_harley_hub.py
for slug in $(python3 -c "import sys; sys.path.insert(0, 'scripts/build'); from project_pages_data import PROJECT_CONFIGS; print(' '.join(sorted(PROJECT_CONFIGS)))"); do
  python3 scripts/build/validate_project_pages.py "$slug"
done
git diff --check
```

## Shared Chrome And Translation Workflow

After changing `assets/main.js` I18N or shared chrome:

```bash
node scripts/build/extract_i18n.js
python3 scripts/build/build_i18n.py
python3 scripts/build/nav_patch.py
python3 scripts/build/localize_internal_links.py
python3 scripts/build/apply_seo_meta.py
python3 scripts/build/build_sitemap.py
python3 scripts/build/build_llms.py
python3 scripts/build/validate_seo.py
```

The lead-form modal is currently retained in checked-in HTML and copied by
page-family generators rather than rendered from a standalone form template.
Its FormSubmit `action` must use an activated private alias and must never
contain the recipient email address. `validate_seo.py` checks this rule across
all built HTML, including files outside the sitemap. `site_chrome.py` assigns
the absolute language-local `_next` URL when the modal is copied; generic
localization repeats that normalization in `build_i18n.py`.

If `assets/main.css` or `assets/main.js` changed, read the current main-asset
stamp from `docs/PROJECT_STATE.md`, choose the next date-letter value, update
the HTML references and every applicable generator constant, then run the broad
validator. Different asset families may keep independent stamps.

## Lead Measurement Workflow

Ownership:

- Worker/API/KV contract: `worker/leads/worker.mjs` and
  `worker/leads/wrangler.toml`;
- browser events and WhatsApp page attribution: `assets/main.js`;
- FormSubmit redirect destinations: `new_pages_data.py`,
  `build_new_pages.py`, `site_chrome.py` and `build_i18n.py`;
- private checkup report: `tools/leads_report.py`.

The Worker stores counters only. It never reads or stores IP addresses,
user-agent strings, form values or raw events. Its accepted `ref` field is
sanitized by the browser and discarded by the Worker. Worker deployment
changes Cloudflare account state and therefore requires owner approval.
Acceptance events use the reserved `/**test**/` page and separate `test:d:` KV
prefix. `/stats` and `tools/leads_report.py` exclude those counters by default;
`includeTests=1` is for explicit acceptance inspection only. To exercise the
real production UI without polluting operational totals, append
`?icm-leads-test=1` to the page URL; the browser payload then uses the reserved
test page while still following the normal delegated event path.

Local verification:

```bash
node --test worker/leads/worker.test.mjs
python3 tools/leads_report.py --help
python3 scripts/build/validate_seo.py
```

After the owner has provisioned the Worker secret, place the report credentials
in gitignored `.secrets/leads.env` as documented in `worker/leads/README.md`,
then run:

```bash
python3 tools/leads_report.py
```

The report writes `data/leads/<date>_leads.json` locally and prints the 7/28-day
type totals, top pages and language breakdown. Those JSON snapshots are
gitignored operational data.

## General Hub And Service Workflow

After changing a maintained general hub, inspection or tyre-service source:

```bash
node scripts/build/extract_i18n.js
python3 scripts/build/build_new_pages.py
python3 scripts/build/build_pre_purchase_inspection.py
python3 scripts/build/build_tyre_service.py
python3 scripts/build/build_service_custom_hubs.py
python3 scripts/build/build_i18n.py
python3 scripts/build/nav_patch.py
python3 scripts/build/enhance_money_pages.py
python3 scripts/build/localize_internal_links.py
python3 scripts/build/add_image_dims.py
python3 scripts/build/apply_seo_meta.py
python3 scripts/build/build_sitemap.py
python3 scripts/build/build_llms.py
python3 scripts/build/validate_service_custom_hubs.py
python3 scripts/build/validate_seo.py
```

Run only the owned generator(s) when a narrower task explicitly requires
unchanged sibling output, but retain every downstream shared step.

## Expat Hub Workflow

```bash
node scripts/build/extract_i18n.js
python3 scripts/build/build_new_pages.py
python3 scripts/build/build_pre_purchase_inspection.py
python3 scripts/build/build_expat_hub.py
python3 scripts/build/build_i18n.py
python3 scripts/build/nav_patch.py
python3 scripts/build/enhance_money_pages.py
python3 scripts/build/localize_internal_links.py
python3 scripts/build/add_image_dims.py
python3 scripts/build/apply_seo_meta.py
python3 scripts/build/build_sitemap.py
python3 scripts/build/build_llms.py
python3 scripts/build/validate_seo.py
```

If the expat hero source changed, run this before the page sequence:

```bash
python3 scripts/build/optimize_hero_images.py photos/services/english-speaking-motorcycle-workshop-main.jpg
```

## Brand Page Workflow

Set `SLUG` to an entry in `BRAND_CONFIG`. A new brand also requires approved
localized source data, a nav label when needed, a deploy copy entry, and hero
media.

```bash
SLUG=harley-service
node scripts/build/extract_i18n.js
python3 scripts/build/optimize_hero_images.py "$SLUG"
python3 scripts/build/build_brand_pages.py
python3 scripts/build/build_new_pages.py
python3 scripts/build/build_i18n.py
python3 scripts/build/nav_patch.py
python3 scripts/build/enhance_money_pages.py
python3 scripts/build/localize_internal_links.py
python3 scripts/build/apply_seo_meta.py
python3 scripts/build/build_sitemap.py
python3 scripts/build/build_llms.py
python3 scripts/build/validate_brand_pages.py "$SLUG"
python3 scripts/build/validate_seo.py
```

Skip the optimizer when the hero source did not change.

## Harley Hub Workflow

```bash
node scripts/build/extract_i18n.js
python3 scripts/build/build_brand_pages.py
python3 scripts/build/build_blog.py
python3 scripts/build/build_harley_hub.py
python3 scripts/build/build_i18n.py
python3 scripts/build/nav_patch.py
python3 scripts/build/localize_internal_links.py
python3 scripts/build/apply_seo_meta.py
python3 scripts/build/build_sitemap.py
python3 scripts/build/build_llms.py
python3 scripts/build/validate_harley_hub.py
python3 scripts/build/validate_brand_pages.py harley-service
python3 scripts/build/validate_seo.py
```

If a Harley hero source changed, run the optimizer for that exact source path
before the page sequence.

## Authorized Dealer Workflow

```bash
python3 scripts/build/build_authorized_dealer.py
python3 scripts/build/build_new_pages.py
python3 scripts/build/build_i18n.py
python3 scripts/build/nav_patch.py
python3 scripts/build/localize_internal_links.py
python3 scripts/build/apply_seo_meta.py
python3 scripts/build/build_sitemap.py
python3 scripts/build/build_llms.py
python3 scripts/build/validate_seo.py
```

If the hub hero changed:

```bash
python3 scripts/build/optimize_hero_images.py photos/authorized-dealer-main-1600.jpg
```

## Blog Workflow

```bash
python3 scripts/build/build_blog.py
python3 scripts/build/build_i18n.py
python3 scripts/build/nav_patch.py
python3 scripts/build/localize_internal_links.py
python3 scripts/build/apply_seo_meta.py
python3 scripts/build/build_sitemap.py
python3 scripts/build/build_llms.py
python3 scripts/build/validate_seo.py
```

New media must be processed and registered in `blog_data.py` before this
sequence. Binary image preparation is an explicit source-media task.

## News Workflow

For a registered article with supplied hero and gallery sources, import the
media first. The importer reads filenames, order and dimensions from
`NEWS_ARTICLES`, creates the maintained responsive AVIF/WebP/JPEG candidates,
and never edits generated HTML directly:

```bash
python3 scripts/build/import_news_images.py \
  workshop-bbq-party-august-2026 \
  "/absolute/path/to/source-media"
```

Then run the canonical generated-page sequence:

```bash
python3 scripts/build/build_news.py
python3 scripts/build/build_i18n.py
python3 scripts/build/nav_patch.py
python3 scripts/build/localize_internal_links.py
python3 scripts/build/apply_seo_meta.py
python3 scripts/build/build_sitemap.py
python3 scripts/build/build_llms.py
python3 scripts/build/validate_seo.py
```

New article content, media and `NEWS_ARTICLES` data must exist before this
sequence. Source-backed multilingual copy belongs in
`scripts/build/content/`; preserve the supplied file byte-for-byte and parse
placeholders into maintained renderer elements.

## Project Workflow

For a project registered in `PROJECT_CONFIGS` (the generator always refreshes
the complete registered project family and localized redirect set):

```bash
SLUG=<project-slug>
python3 scripts/build/build_project_pages.py
python3 scripts/build/build_new_pages.py
python3 scripts/build/build_harley_hub.py
python3 scripts/build/build_i18n.py
python3 scripts/build/nav_patch.py
python3 scripts/build/localize_internal_links.py
python3 scripts/build/apply_seo_meta.py
python3 scripts/build/build_sitemap.py
python3 scripts/build/build_llms.py
python3 scripts/build/validate_project_pages.py "$SLUG"
python3 scripts/build/validate_seo.py
```

For new approved source photos, import media before rendering:

```bash
SLUG=<project-slug>
SOURCE_DIR='/absolute/path/to/approved/project/photos'
python3 scripts/build/import_project_images.py "$SLUG" "$SOURCE_DIR"
```

The importer always writes AVIF and WebP variants. It also writes JPEG
fallbacks when the project config enables `jpeg_fallback`. Binary media remains
outside the Full Safe Rebuild and must be reviewed and committed with the
approved source-media task.

For an optional exhibition split registered in `PROJECT_EXHIBITION_MEDIA`,
optimize its one approved source photo before rendering:

```bash
SLUG=<registered-project-slug>
SOURCE_IMAGE='/absolute/path/to/approved/exhibition-photo.jpg'
python3 scripts/build/optimize_project_exhibition_images.py "$SLUG" "$SOURCE_IMAGE"
```

The exhibition optimizer always writes the registered responsive widths in
AVIF, WebP and JPEG. Like other binary media tools, it stays outside the Full
Safe Rebuild to avoid codec-version churn.

Migrated project hero optimization uses the explicit source path accepted by
`optimize_hero_images.py`. Do not run all binary optimizers during an idle
rebuild.

## Pricing Workflow

This workflow requires the macOS fonts listed under **Environment**.

```bash
python3 scripts/build/build_pricing.py
python3 scripts/build/build_pricing_pdfs.py
python3 scripts/build/nav_patch.py
python3 scripts/build/localize_internal_links.py
python3 scripts/build/apply_seo_meta.py
python3 scripts/build/build_sitemap.py
python3 scripts/build/build_llms.py
python3 scripts/build/validate_seo.py
```

## Discovery Index Workflow

Do not hand-edit `llms.txt`.

```bash
python3 scripts/build/build_sitemap.py
python3 scripts/build/build_llms.py
python3 scripts/build/validate_seo.py
```

## Reviews Workflow

This calls the public Reviews Worker and requires outbound network access.

```bash
python3 scripts/build/build_reviews_schema.py
python3 scripts/build/validate_seo.py
```

Expected source ownership:

- aggregate rating/count: Worker response saved to
  `assets/reviews-snapshot.json`;
- visible cards and JSON-LD reviews: `assets/reviews-curated.json` according to
  `displayCount`.

An unchanged Worker response and curated source should leave tracked output
unchanged. The scheduled automation is defined in
`.github/workflows/reviews-refresh.yml`. It pushes only changed tracked review
output. Its `committed` job output conditionally calls the reusable Pages
workflow only after a commit was pushed. A no-change refresh skips that job,
creates no Pages run and cannot interrupt an in-progress deployment.

## Focused CSS Hero Validation

```bash
python3 scripts/build/validate_seo.py --check-css-hero-preloads
```

## Focused Blog Picture Hero Validation

```bash
python3 scripts/build/validate_seo.py --check-picture-hero-preloads
```

This mode requires one responsive AVIF preload per Blog article hero, exact
`imagesrcset`/`imagesizes` parity with the rendered AVIF source, one
`fetchpriority="high"` element, no high-priority lazy image, and matching
candidate selection at 390px/DPR3, 390px/DPR2, 768px/DPR2, 1280px/DPR1 and
1440px/DPR1.

## Focused Project Navigation Validation

```bash
python3 scripts/build/validate_seo.py --check-project-navigation
```

This mode requires every project in `new_pages_data.py` `PROJECT_TILES` to
appear in that exact order in both the desktop and mobile project menus on
every sitemap page, with the URL localized to the page language.

## Dates And Cache-Bust

`build_sitemap.py` uses explicit article dates and semantic Git history. It
must not stamp unchanged pages with build time. Structured-data publication
and modification dates follow the same rule.

Asset references use `?v=YYYYMMDDx`. Current values live only in
`docs/PROJECT_STATE.md`. A changed asset requires a new value everywhere that
asset is referenced; an unchanged asset retains its value.
