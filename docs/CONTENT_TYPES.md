# Content Types And Implementation Ownership

This file owns repeatable page-family workflows and stable implementation
patterns. It intentionally contains no build command blocks and no current
inventory counts. Use `docs/PROJECT_STATE.md` for current quantities and
`scripts/build/README.md` for executable commands.

## Rules For Every Indexable Family

- Preserve every language registered in `build_sitemap.py` `LANGS`.
- Prefer maintained source data and shared renderers over manual generated-HTML
  edits.
- Register new paths in `build_sitemap.py` `PAGES`,
  `localize_internal_links.py` `LOCALIZED_PATHS`, the appropriate i18n source
  registry, and `.github/workflows/pages.yml` when a new deploy folder exists.
- Keep canonical, mutual hreflang, localized internal links and JSON-LD aligned.
- Every indexable page must include at least `BreadcrumbList`.
- Use absolute local asset paths and explicit image dimensions.
- Use real content dates with timezone for sitemap and structured data. Never
  replace unchanged page dates with build or deploy time.
- Keep visible FAQ content and `FAQPage` entities identical through source data.
- CSS-background hero preloads and rendered backgrounds must select the same
  responsive resource. Shared behavior belongs in `hero_images.py` and
  `apply_seo_meta.py`.
- Shared article CTAs use the existing article button classes; shared service
  card grids use the established service-grid patterns. Do not introduce
  page-specific duplicates for the same component.
- Generated inline CSS uses the typography variables from `assets/main.css`,
  not hardcoded font-family names.
- Run the family workflow named in `scripts/build/README.md`, then the broad
  verification workflow, before delivery.

## Brand Service Pages

Source and registry:

- `scripts/build/brand_pages_data.py`: `BRAND_ORDER`, `BRAND_CONFIG`,
  `BRAND_HEAD`, `PAGE_I18N`.
- `assets/main.js`: navigation labels when a new label key is required.
- Hero sources under `photos/`; variants under `photos/optimized/`.

Renderer and protection:

- `build_brand_pages.py` renders the English sources.
- `build_new_pages.py` consumes the brand registry for shared hubs.
- `site_chrome.py` consumes the registry for desktop/mobile navigation and the
  footer.
- `validate_brand_pages.py` protects registry wiring, generated variants,
  hero assets, schema families, deployment and reciprocal links.

Stable rules:

- Use independent-workshop wording for every brand registered in
  `BRAND_ORDER`.
- Keep reciprocal “Other brands” links and related workshop-path cards within
  the current language.
- Keep the homepage brand strip synchronized with `BRAND_ORDER`.
- Preserve approved model names, technical claims, prices and contact facts.
- A text or hero refresh changes source data, not just generated HTML.

Commands: `scripts/build/README.md`, **Brand page workflow**.

## General Hubs And Service Pages

Ownership:

- General hubs: `new_pages_data.py` + `build_new_pages.py`.
- Copy-driven Service/Custom hubs:
  `content/service_hub_copy_4lang.md` and
  `content/custom_hub_copy_4lang.md` +
  `build_service_custom_hubs.py`; exact family checks live in
  `validate_service_custom_hubs.py`.
- Pre-purchase inspection:
  `content/pre_purchase_inspection_copy_4lang.md` +
  `build_pre_purchase_inspection.py`.
- Tyre service: `content/tyre_service_copy_4lang.md` +
  `build_tyre_service.py`; media refresh is owned by
  `optimize_tyre_service_images.py` and its checksum manifest.
- English-speaking expat hub: `content/expat_hub_copy_4lang.md` +
  `build_expat_hub.py`.
- Shared commercial enhancements: `enhance_money_pages.py`.

Stable Service/Custom hub rules:

- Both hubs use the same parser and renderer and are rendered directly in all
  four languages. They are not outputs of the generic `build_i18n.py` flow.
- The approved copy owns each hub's local-area and related-path sections.
  `enhance_money_pages.py` must not add either generic block to these pages.
- Service price anchors must already exist in `pricing_data.py`; no new price
  may be introduced only in hub copy. Custom-build prices are not published.
- Project links come from all `PROJECT_CONFIGS` entries with
  `integrations.custom`, in `PROJECT_TILES` order and with same-language URLs.
- A literal Google rating may be used only without a hard-coded review count.
  Recheck that literal when the review snapshot rating changes.
- The confirmed custom-build policy is maintained in
  [BUSINESS_FACTS.md](BUSINESS_FACTS.md#custom-build-policy); do not duplicate
  it as a second documentation source.

Schema normally follows `Service` + `FAQPage` + `BreadcrumbList`; collection
hubs use the established collection pattern. Use the actual source family as
the authority rather than applying this shorthand blindly.

The expat hub routes to existing commercial pages, remains footer-only and
contextual-link-only, and must not become a header-navigation item without an
explicit owner decision.

Commands: `scripts/build/README.md`, **General hub and service workflow** and
**Expat hub workflow**.

## Harley Hub Family

Ownership:

- Approved multilingual copy:
  `content/harley_hub_phase1_4lang.md`.
- Supplemental UI, media and project summaries: `harley_hub_data.py`.
- Renderer: `build_harley_hub.py`.
- Focused validator: `validate_harley_hub.py`.
- Hero sources: `photos/harley/`.

Stable rules:

- The hub routes riders among service, tuning, custom work and parts; it does
  not replace the independent service spoke.
- Feed membership comes from a blog post's maintained `topics` metadata.
- Portfolio cards reuse existing project assets and fact-based project copy.
- Preserve the validator-owned typography, spacing and dark hero treatment.
- Hub schema uses a collection/web-page pattern; service spokes include
  `Service`; visible FAQs mirror `FAQPage`; all include breadcrumbs.
- Do not add `Product` or `Offer` without approved numeric pricing.

Commands: `scripts/build/README.md`, **Harley Hub workflow**.

## Authorized Dealer Family

Ownership:

- `authorized_dealer_data.py` owns the hub and future partner registry.
- `build_authorized_dealer.py` renders the hub and maintained direct partner
  subpages.
- `site_chrome.py` owns shared navigation and footer placement.

This family is an official parts/accessories channel and must stay separate
from independent motorcycle-brand service pages.

For C-Way and future priced partner catalogs:

- Every visible product position has one complete `Product` with an `Offer`.
- Never emit a second partial `Product` for the same item inside a service or
  catalog graph. Cross-references use the canonical product `@id`.
- Visible names, prices, currency, availability and schema must remain aligned.
- Product media stays local and responsive.

Current partner inventory belongs only in `docs/PROJECT_STATE.md`.

Commands: `scripts/build/README.md`, **Authorized Dealer workflow**.

## Blog

Ownership:

- `blog_data.py` `BLOG_POSTS`: slugs, topics, dates, metadata, localized copy,
  media and schema inputs.
- Long approved copy may live under `scripts/build/content/` and be parsed by
  `blog_data.py`.
- `build_blog.py`: hub and article rendering.
- `build_i18n.py`, `build_sitemap.py` and `localize_internal_links.py` derive
  Blog article membership from `BLOG_POSTS`; a new registered post must not
  require a second hand-maintained slug list.

Stable rules:

- Preserve the reviewed copy and maintained internal links.
- Hero is the LCP resource: responsive local AVIF/WebP, explicit dimensions,
  eager/high-priority discovery and no lazy loading.
- The article hero preload is one AVIF link with `imagesrcset` and
  `imagesizes` matching the first AVIF `<source>`. Keep `fetchpriority="high"`
  only on the hero `<img>` so preload and paint resolve through one candidate
  selection contract.
- Other article images are lazy unless their position requires otherwise.
- Native video uses the supplied source/poster and matching `VideoObject`; do
  not substitute an iframe when self-hosted media is required.
- When a self-hosted video is declared deferred, keep the MP4 URL in
  `data-src` with `preload="none"` and attach it only on the first deliberate
  player activation. The poster and dimensioned aspect-ratio wrapper must
  render before that activation without downloading the MP4.
- Portrait native video uses the common centered `9 / 16` wrapper, constrained
  to 420 px at desktop widths and to the article column on mobile. Do not apply
  the landscape width/aspect override unless the registered video is actually
  landscape.
- `BlogPosting`, `VideoObject` when present, `FAQPage` when present and
  `BreadcrumbList` must match visible content and real dates.
- Every `VideoObject` must have a non-empty `uploadDate` using the real video
  or article publication time in full ISO-8601 form with timezone.
  `validate_seo.py` enforces this contract across every sitemap page.
- Referenced author/provider/publisher entities need maintained names; article
  publisher data includes the maintained logo where required.

Commands: `scripts/build/README.md`, **Blog workflow**.

## News

Ownership:

- `news_data.py` `NEWS_ARTICLES`.
- `build_news.py` renders the hub and articles.

News articles currently use the responsive CSS-background hero pattern, not
the Blog `<picture>` pattern. Keep their preload and CSS candidates aligned
through `hero_images.py` and `apply_seo_meta.py`. Other stable rules mirror
Blog for responsive local media, real dates, localized links and
schema-to-visible-content alignment. `NewsArticle` is used for event and
workshop news. Event names used in machine indexes should be concise;
marketing subtitles belong in descriptions.

Approved multilingual delivery files belong under `scripts/build/content/`
and are parsed by the registered article data rather than copied into generated
HTML by hand. When a delivery includes a gallery, register its source order,
dimensions and localized ALT pattern in `NEWS_ARTICLES`; the common renderer
owns the responsive AVIF/WebP/JPEG `<picture>` markup and the contained
horizontal scroll-snap layout. Import registered hero and gallery sources with
`import_news_images.py`, then use the complete News Workflow.

Commands: `scripts/build/README.md`, **News workflow**.

## Projects

Ownership:

- `project_pages_data.py` is the complete project and redirect registry.
- Fighter, Cocktail, Fetish and The First use approved Markdown under
  `content/projects/`; the 10 migrated project pages use
  `content/projects/legacy_projects_4lang.json`, which preserves their reviewed
  localized main content and media structure.
- `build_project_pages.py` renders every indexable project variant and all 8
  localized noindex redirects directly. Project details are not outputs of the
  generic `build_i18n.py` flow.
- `import_project_images.py` owns newly approved data-driven project media.
- `optimize_project_exhibition_images.py` owns responsive media for optional
  registered exhibition split sections.
- `validate_project_pages.py` protects every registered project and redirect.
- Portfolio cards and project names: `new_pages_data.py` `PROJECT_TILES`.
- Desktop and mobile project navigation: `site_chrome.py`, derived from
  `PROJECT_TILES` in the same order as the portfolio listing.

Stable rules:

- New projects use the registered data-driven Markdown flow. Extend
  `MARKDOWN_PROJECT_CONFIGS`; do not add a project-specific renderer or build
  script. Listing and shared navigation membership come from `PROJECT_TILES`;
  sitemap and localized-path membership derive from `PROJECT_CONFIGS`.
- A project with `integrations.custom` is added to the four `/custom/` pages by
  `build_service_custom_hubs.py`; do not patch those generated pages manually. Harley
  portfolio copy and order remain explicit in `harley_hub_data.py` because not
  every project is a Harley project. `validate_project_pages.py` enforces the
  declared Custom and Harley integrations.
- Contextual project-to-project relationships belong in
  `reciprocal_projects`. The project validator requires same-language links in
  both directions without duplicating visible copy in generated HTML.
- Generated project HTML must not contain `window.ICM_I18N_PAGE`; localized
  project copy belongs in the registered source data.
- Because project details bypass `build_i18n.py`, `build_project_pages.py` must
  apply `site_chrome.py` `GLOBAL_I18N` for the selected language before it
  writes shared chrome. `validate_seo.py` compares translated chrome text on
  every indexable page with the same-language homepage baseline.
- Hero media is responsive and eager, with a responsive AVIF preload matching
  its `<picture>` source. New registered media uses AVIF/WebP with JPEG fallback
  when `jpeg_fallback` is enabled. Only the hero image uses
  `fetchpriority="high"`; gallery media remains dimensioned and lazy.
- Optional exhibition split sections are marked in maintained project source
  with `data-project-exhibition="true"` and configured once in
  `PROJECT_EXHIBITION_MEDIA`. The common project renderer supplies the
  localized responsive AVIF/WebP/JPEG picture; generated HTML is never edited
  per language. Exhibition media is dimensioned and lazy and never competes
  with the hero for high priority.
- Listing card names, tags and project detail claims must not contradict each
  other.
- Adding a project to `PROJECT_TILES` must add it to both project menus without
  a second inventory edit. `validate_seo.py --check-project-navigation`
  protects exact registry membership, localized URLs and order on every
  sitemap page.
- A detail-only project content change updates only that project's localized
  sitemap dates. The `/projects/` listing date changes only when its visible
  listing content changes; shared chrome changes never move `lastmod`.
- Every project uses the same Article/WebPage/ImageObject/LocalBusiness and
  localized BreadcrumbList graph. Article publisher and author use an `@id`
  reference to the complete LocalBusiness entity with maintained name and
  logo. Dates are full ISO-8601 values with timezone.
- The old `nezlamniy` and `quanta` paths are localized noindex redirects in all
  four languages and stay out of the sitemap.
- No `Product`/`Offer` is emitted without approved commerce data.

Commands: `scripts/build/README.md`, **Project workflow**.

## Pricing

Ownership:

- `pricing_data.py`: page and PDF data.
- `build_pricing.py`: localized HTML.
- `build_pricing_pdfs.py`: downloadable PDFs.

Edit the shared data first and regenerate both representations. Keep visible
prices, `OfferCatalog` and linked PDFs aligned. The current PDF portability
limit is documented in `docs/OPEN_TASKS.md`.

Additional fixed services in a pricing section belong in the section's
`additional_services` data. The HTML renderer, `OfferCatalog` builder and PDF
renderer consume that same list so a published price cannot exist in only one
representation.

Commands: `scripts/build/README.md`, **Pricing workflow**.

## Shared Navigation And I18N

Ownership:

- Labels: `assets/main.js` `I18N`.
- Extracted build snapshot: `scripts/build/i18n.json`, produced by
  `extract_i18n.js`.
- Canonical chrome: `site_chrome.py`.
- Sitemap-wide application: `nav_patch.py`.
- Generic localized output: `build_i18n.py`.
- Same-language link rewriting: `localize_internal_links.py`.

Do not hand-maintain separate desktop and mobile menu inventories. Shared
rendering must preserve parent-link behavior, dropdown/accordion children,
language locality and footer parity.

Commands: `scripts/build/README.md`, **Shared chrome and translation workflow**.

## AI Discovery Index

Ownership:

- `build_llms.py` reads `build_sitemap.py` `PAGES`, maintained content
  registries, short names from existing navigation/content sources, published
  metadata and `docs/BUSINESS_FACTS.md`.
- `llms.txt` is generated output and must not be hand-edited.

Every English sitemap URL must appear once in the generated index. Link names
are stable human page names, not marketing H1 text. Business facts remain
machine-readable and source-backed.

Commands: `scripts/build/README.md`, **Discovery index workflow**.

## Reviews

Ownership:

- Live aggregate snapshot: `assets/reviews-snapshot.json`.
- Editorial visible cards: `assets/reviews-curated.json`, including
  `displayCount`.
- Renderer/schema updater: `build_reviews_schema.py`.
- Runtime source: public Cloudflare Worker configured in `assets/main.js`.
- Worker implementation and cache behavior: `worker/reviews.js` and
  `worker/README.md`.

`AggregateRating` uses the live rating/count snapshot. Visible cards and
JSON-LD `Review` items come from the curated file and match one-for-one. Never
derive aggregate `reviewCount` from the visible-card count. Do not expose the
Google Places key client-side.

Commands: `scripts/build/README.md`, **Reviews workflow**.

## Anonymous Lead Measurement

Ownership:

- Browser transport, delegated WhatsApp/telephone tracking and localized
  WhatsApp page attribution: `assets/main.js`.
- Lead Worker and KV data model: `worker/leads/`.
- FormSubmit language-local success destinations: the shared modal source in
  `index.html`, normalization in `site_chrome.py` / `build_i18n.py`, and the
  generated `thank-you` entry in `new_pages_data.py` / `build_new_pages.py`.
- Private checkup report: `tools/leads_report.py`; local JSON output under
  `data/leads/` is intentionally gitignored.

The four event types are `whatsapp`, `tel`, `form_submit` and `form_view`.
Payloads contain only event type, query-free path, path-derived language and a
sanitized referrer source. KV retains daily counters, not raw events. Thank-you
pages are `noindex` utility output and must never enter the sitemap or discovery
index. Cloudflare Web Analytics is owner-managed through edge injection and is
not added to repository HTML.

Synthetic acceptance events must use the reserved `/**test**/` page. The
Worker stores them below a separate `test:d:` KV prefix. Normal `/stats`
responses and `tools/leads_report.py` exclude that prefix; use
`includeTests=1` only for explicit acceptance inspection.

Commands: `scripts/build/README.md`, **Lead Measurement Workflow**.

## Media Optimization

Binary optimization is intentionally outside the canonical full rebuild to
avoid codec-version churn. Run a media tool only after its source image changes
and review the binary diff deliberately.

- General/brand/legacy hero variants: `optimize_hero_images.py`.
- Tyre-service variants: `optimize_tyre_service_images.py`.
- Data-driven project import: `import_project_images.py`.
- Registered project exhibition media: `optimize_project_exhibition_images.py`.
- HTML dimensions: `add_image_dims.py` after generated markup changes.

## Task Completion

Use `docs/TASK_BRIEF_TEMPLATE.md` for substantial intake. At completion:

- update `docs/PROJECT_STATE.md` only if current state changed;
- update `docs/OPEN_TASKS.md` for new or resolved risks;
- add chronology to `docs/CODEX_CHANGELOG.md` for meaningful implementation;
- run the exact family and broad commands from `scripts/build/README.md`;
- commit, push and verify production unless the owner explicitly limits
  delivery.
