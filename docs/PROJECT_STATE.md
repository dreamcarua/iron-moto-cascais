# Iron Custom Motors Website: Project State

Last updated: 2026-09-06

This is the only documentation file that owns current inventories, counts,
deployed public identifiers and cache-bust values. Operating rules live in
`AGENTS.md`; page ownership lives in `docs/CONTENT_TYPES.md`; commands live in
`scripts/build/README.md`.

## Status And Evidence

- Status: **confirmed** for the deployed site and both Worker services.
- Evidence date: 2026-09-06 (Europe/Lisbon).
- Repository evidence: S-REBUILD-W1 implementation commit `42c51732`,
  A-MEASURE commits `fae3a7ce`, `173d62e1` and
  `a286b68a`, M-REPO commits `88a44503` and `599a0429`, automated
  review-snapshot refresh commit `6f28a412`, N-BBQ implementation commit
  `f4d4dd07` and merged deployment state `93b4f460`, the automated
  review-snapshot refresh commit
  `1e2e9e6c`, F-HASH implementation commit `5c010b49`,
  B-TAPE implementation commit `6c24e8ef`,
  V-UPLOADDATE implementation commit `39e44293`, R9
  implementation commit `800c4c68`, the automated
  review-snapshot refresh commit `7e834826`, B-TUBELESS implementation commit
  `fb4429e9` and schema
  resolution follow-up commit `44e202ee`,
  P-THE-FIRST implementation commit `06e04fff`,
  P-FETISH implementation commit `a0da49fd`, CWAY-VAT
  size follow-up commit `8447160b`, CWAY-VAT
  implementation commit `560e3891`, EXPO-V2
  implementation commit `aa23075c`, NAV+EXPO
  implementation commit `6a2bdff7`, P-COCKTAIL implementation commit
  `e3ef595c`, the earlier C8 implementation commits `ce25a7c2` and `f42fb5d0`,
  and C8-FIX implementation commit `52316a26`.
- Inventory method: import the maintained Python registries, parse
  `sitemap.xml`, and enumerate tracked `*.html` files.
- Cache-bust method: scan asset references in every sitemap HTML file.
- Production evidence: S-REBUILD-W1 GitHub Pages workflow `34060700603`,
  cache-bypass checks on all eight rebuilt Service/Custom hubs, four Pricing
  pages, four tyre-service pages, `llms.txt` and `sitemap.xml`; responsive
  browser checks at 390 px and 1440 px found zero document overflow and one
  responsive CSS hero candidate. Google Rich Results results
  `ICpuxGmwcmItgg35JinkCg` for EN Service and
  `xR2ntFNq3QrtmJfydF3OeA` for PT Custom each reported three valid items and
  no errors. A-MEASURE GitHub Pages workflows `33665877221` and
  `33666134112`, production HTTP checks on all four noindex thank-you pages,
  all four localized contact forms, the shared JavaScript and `sitemap.xml`,
  and browser checks of all four event types and all four WhatsApp languages.
  The first Pages run exposed a missing root `thank-you` directory in the
  artifact allowlist; commit `a286b68a` corrected it and the second run
  deployed all four utility pages. N-BBQ GitHub Pages workflow `32704971695`,
  cache-bypass checks on all four new News pages, the four News hubs, the
  twelve existing News articles, `llms.txt` and `sitemap.xml`; responsive
  browser checks at 390 px and 1440 px found no document overflow and selected
  the 768 AVIF and 1920 AVIF CSS hero candidates respectively. Google Rich
  Results result `YVVmMMh-Ri99Utdpst9nbA` detected four valid items, including
  valid Article, Breadcrumb and Local business items. F-HASH GitHub Pages
  workflow `32566489805`,
  cache-bypass checks on all 120 pages that contain the lead form and the
  production sitemap; every deployed FormSubmit action uses the activated
  private alias, none exposes an email address, and the complete normalized
  form markup matches the repository. B-TAPE GitHub Pages workflow `31874899365`,
  cache-bypass checks on the four new Blog pages, four Blog hubs, four
  reciprocal tubeless-conversion pages, `llms.txt` and `sitemap.xml`; the
  self-hosted portrait MP4 and poster returned HTTP 200, and browser resource
  inventories at 390 px and 1440 px contained one responsive hero and the
  poster but no MP4 before interaction. V-UPLOADDATE GitHub Pages workflow
  `31781405314`,
  cache-bypass schema checks on all 12 affected Blog pages and the production
  sitemap; R9 GitHub Pages workflow `31390002213`, cache-bypass
  checks on all four home pages, `assets/reviews-curated.json` and
  `sitemap.xml`; B-TUBELESS GitHub Pages workflow `31306394300`,
  cache-bypass checks on the four article pages, four Blog hubs, four pricing
  pages, four tyre-service pages, `llms.txt` and `sitemap.xml`; both media
  endpoints returned HTTP 200 and the production article graphs resolve
  publisher `@id` to the complete `LocalBusiness` entity. Earlier completed
  evidence includes P-THE-FIRST GitHub Pages workflow `30883611614`,
  cache-bypass checks on the four The First pages, all twelve integration
  pages, eight reciprocal Cocktail/Fetish pages, `llms.txt` and `sitemap.xml`;
  P-FETISH GitHub Pages workflow `30852768505`,
  cache-bypass checks on the four Fetish pages, all twelve integration pages,
  reciprocal Cocktail links, `llms.txt` and `sitemap.xml`; CWAY-VAT size
  follow-up workflow `30716569527`,
  CWAY-VAT GitHub Pages workflow `30715488709`,
  cache-bypass checks on all four C-Way pages and the production sitemap,
  EXPO-V2 GitHub Pages workflow `30713880464`,
  cache-bypass checks on all 12 exhibition pages and four project listings,
  byte-identical production project CSS and sitemap, and Google Rich Results
  result `QtK8FJYbOvDZFu-k-TWBng` with four valid items, no errors and no
  warnings. Earlier evidence remains in the task reports and changelog.
- Reproducibility evidence: the documented Full Safe Rebuild with the PDF step
  intentionally skipped and all four validator groups passed after
  S-REBUILD-W1 commit `42c51732`, leaving empty `git status --short`; verified
  2026-09-06. The current
  `sitemap.xml` SHA-256 is
  `52aead525994703b941a5cca0f5dd94bc9589b651267a500fda767bf7e331956`.
  The earlier repository audit baseline was documentation commit `d08a3297`.
- A-MEASURE evidence: the owner authorized Cloudflare deployment and completed
  Wrangler OAuth for the Vg account on 2026-09-02. `icm-leads` is deployed with
  its KV binding and private stats secret. Production acceptance exercised all
  four event types through the live client and stored them only under the
  reserved `/**test**/` page; ordinary stats and `tools/leads_report.py`
  excluded them. No-token stats returned 401, both production origins passed
  CORS preflight, and a foreign origin returned 403 without an allow-origin
  header. One owner-confirmed FormSubmit request labeled
  `TEST A-MEASURE — ignore` redirected to `/thank-you/`. `icm-reviews` was
  redeployed from the repository and returned 200 with the correct CORS header
  for both production and the current GitHub Pages preview origin. The static
  production review widget remained operational with its checked-in snapshot
  and nine curated cards.

## Repository And Production

| Item | Current value |
|---|---|
| Production | `https://ironcustommotors.com/` |
| Repository | `https://github.com/PhilipGrishin/iron-moto-cascais` |
| Git remote | `https://github.com/PhilipGrishin/iron-moto-cascais.git` |
| Production branch | `main` |
| Hosting | GitHub Pages, checked-in static output |
| DNS/CDN | Cloudflare |
| Server-side framework | None |
| CMS | None |

Pushing `main` triggers `.github/workflows/pages.yml`. GitHub does not run the
site generators during deployment; the workflow packages checked-in output.
The repository was transferred to the owner's `PhilipGrishin` account on
2026-08-24. The owner confirmed that the domain, DNS and GitHub Pages settings
were reconfigured for the new repository and verified in production. The old
repository URL currently redirects, but it is not a supported canonical URL.

## Current Inventory

| Inventory | Current value | Canonical evidence |
|---|---:|---|
| Supported languages | 4 | `build_sitemap.py` `LANGS` |
| English path patterns | 59 | `build_sitemap.py` `PAGES` |
| Indexable sitemap URLs | 236 | parsed `sitemap.xml` `<url>` entries |
| Tracked HTML files | 249 | filesystem enumeration |
| Indexable HTML files | 236 | sitemap-to-file resolution |
| Non-indexed HTML files | 13 | `404.html`, 8 localized project redirect stubs and 4 `thank-you` pages |
| Sitemap lastmod tags | 236 | parsed `sitemap.xml` |
| Unique sitemap lastmod values | 58 | parsed `sitemap.xml` |
| Registered brand service pages | 7 | `BRAND_ORDER` / `BRAND_CONFIG` |
| Project detail pages | 14 | `PROJECT_TILES` |
| Data-driven project definitions | 14 | `PROJECT_CONFIGS` |
| Blog posts | 9 | `BLOG_POSTS` |
| News articles | 4 | `NEWS_ARTICLES` |
| Harley Hub English page patterns | 3 | `harley_hub_data.py` `PAGE_CONFIG` |
| Generated general/utility localized entries | 7 | `build_new_pages.py` / `new_pages_data.py` |
| Authorized Dealer English page patterns | 2 | `build_authorized_dealer.py` |
| Legal English page patterns | 3 | `LEGAL_PAGES` |

Language roots:

- English: `/`
- Portuguese: `/pt/`
- Russian: `/ru/`
- Ukrainian: `/uk/`

The tyre-service family intentionally uses localized slugs. Read them from
`build_sitemap.py` `LANG_PATHS`; do not infer them from the English slug.

Registry alignment on the evidence date:

| Registry | Entries | Relationship |
|---|---:|---|
| `build_sitemap.py` `PAGES` | 59 | canonical English indexable paths |
| `localize_internal_links.py` `LOCALIZED_PATHS` | 59 | matches `PAGES` after normalization |
| `build_i18n.py` `MAIN_PAGES` | 33 | English sources localized by the generic i18n flow |
| `project_pages_data.py` `PROJECT_CONFIGS` | 14 | project details rendered directly in four languages |

There is no active `EN_PAGES` registry. The canonical English page registry is
`build_sitemap.py` `PAGES`.

## Current Cache-Bust Values

| Assets | Value | Scope |
|---|---|---|
| `assets/main.css`, `assets/main.js` | `20260906a` | every sitemap page |
| `assets/projects.css` | `20260801a` | project detail pages |
| `assets/projects.js` | `20260710b` | project detail pages |

Different asset families may legally use different values. Each individual
asset must use one value site-wide. Change a value only when that asset changes.

## Current Page Families

### General And Commercial Pages

`/`, `/services/`, `/motorcycle-service/`, `/parts/`,
`/upgrades-tuning/`, `/custom/`, `/pre-purchase-inspection/`,
`/motorcycle-tyre-service/`, `/pricing/`, `/projects/`, `/about/`,
`/community/`, `/contact/`, `/faq/`,
`/english-speaking-motorcycle-workshop/`, `/authorized-dealer/`,
`/blog/`, `/news/`, `/privacy/`, `/cookies/`, and `/terms/`.

The expat workshop page is intentionally footer-only and contextual-link-only;
it is not a top-navigation item.

The Service and Custom hubs are copy-driven four-language families owned by
`scripts/build/content/service_hub_copy_4lang.md`,
`scripts/build/content/custom_hub_copy_4lang.md` and the shared
`build_service_custom_hubs.py` renderer. Their current pages use distinct
search-intent H1s, six source-matched FAQ items, localized lead CTAs and the
`Service`/`FAQPage`/`BreadcrumbList` graph. The Custom hub lists all 14
registered projects in `PROJECT_TILES` order. Pricing titles, descriptions,
eyebrows and H1s identify the 2026 price list; the tyre-service family received
metadata-only refinements with unchanged visible content.

### Harley Hub

- `/harley/`
- `/harley-tuning/`
- `/harley-custom/`

The existing `/harley-service/` page is the independent service spoke. Blog
feed membership comes from `BLOG_POSTS[*].topics`.

### Brand Service Pages

The current ordered inventory is the brands registered in `BRAND_ORDER`.
These are independent workshop pages, not authorized motorcycle-brand dealer
pages.

### Authorized Dealer

- `/authorized-dealer/`
- `/authorized-dealer/c-way/`

This is a separate official parts/accessories channel. The C-Way page currently
contains 6 visible priced configurations and 6 matching `Product`/`Offer`
entities, with no partial duplicate products. Each visible configuration price
repeats the existing VAT-exclusion wording in the page language; the summary
price note and schema tax fields remain unchanged. The page-scoped suffix is
17 px in every language, approximately 31% larger than its original 13 px
release size.

### Projects

- `/projects/inspirium/`
- `/projects/beckman/`
- `/projects/unbreakable/`
- `/projects/quanta-r/`
- `/projects/burly/`
- `/projects/sturmvogel/`
- `/projects/geometric/`
- `/projects/joker/`
- `/projects/hellboy/`
- `/projects/true-religion/`
- `/projects/fighter/`
- `/projects/cocktail/`
- `/projects/fetish/`
- `/projects/the-first/`

All 14 project details are data-driven and rendered through
`build_project_pages.py`. Fighter, Cocktail, Fetish and The First use approved
Markdown; the 10
migrated projects use the versioned localized source at
`content/projects/legacy_projects_4lang.json`. Generated project HTML contains
no `window.ICM_I18N_PAGE` copy block.

Sturmvogel, Beckman and Hell Boy are confirmed in the permanent workshop
exhibition beside the rider lounge. Their four-language project pages use the
registered responsive exhibition split: photo on the left and text on the
right at desktop widths, then photo above text on mobile. The media uses
dimensioned lazy AVIF/WebP with JPEG fallback and localized approved ALT text.
The Hell Boy listing year is `2025` in every language.

Localized noindex redirects, intentionally excluded from the sitemap:

- `/projects/nezlamniy/` -> `/projects/unbreakable/`
- `/projects/quanta/` -> `/projects/quanta-r/`

The same redirect relationship exists under `/ru/`, `/uk/` and `/pt/`.

### Blog

- `/blog/revtech-110-oil-service-engine-gearbox-drive/`
- `/blog/motorcycle-brake-pad-replacement-cascais/`
- `/blog/front-fork-service-motorcycle-cascais/`
- `/blog/motorcycle-tyre-fitting-specialist-cascais/`
- `/blog/royal-enfield-bear-650-fork-oil-case-study/`
- `/blog/harley-davidson-full-service-done-right/`
- `/blog/royal-enfield-bear-650-scrambler-build/`
- `/blog/tubeless-conversion-spoked-wheels/`
- `/blog/tubeless-sealing-tape-failure/`

### News

- `/news/workshop-bbq-party-august-2026/`
- `/news/ericeira-kustom-fest-2026/`
- `/news/opens-new-workshop-in-cascais/`
- `/news/lisbon-motorcycle-film-fest-2026-beckman/`

## Current Delivery And Discovery State

- All 136 pages that contain the lead form submit to FormSubmit through the
  activated private action alias. No built HTML exposes the delivery inbox in
  a FormSubmit action, and the SEO validator enforces this contract across all
  built HTML files, including non-sitemap output. The 132 indexable form pages
  redirect to their language-local noindex `thank-you` page; those four utility
  pages contain the same shared modal and remain outside `sitemap.xml`.
- A-MEASURE's checked-in client sends only four anonymous lead-intent types:
  `whatsapp`, `tel`, `form_submit` and `form_view`. The payload contains the
  query-free path, path-derived language and a sanitized referrer hostname;
  it contains no form values or browser identifiers. The new Worker stores KV
  counters only and does not read or store IP addresses or user-agent strings.
  The production Worker endpoint is deployed. Reserved `/**test**/` events use
  a separate `test:d:` KV prefix and are excluded from normal stats and checkup
  reports. Appending `?icm-leads-test=1` to a production page exercises the
  normal browser event path while assigning the reserved test page.
- The four home pages render 9 curated Google-review cards and the matching
  9 JSON-LD `Review` items from `assets/reviews-curated.json`. Their
  `AggregateRating` remains independently sourced from the Worker snapshot and
  is currently `5.0` from `25` reviews. The curated source SHA-256 is
  `aaad7c6c40839b4174653524fcc7749e17714792b033b861e011d57cdf708190`.
- Every sitemap page has canonical, mutual hreflang and Schema.org JSON-LD with
  at least `BreadcrumbList`.
- All 44 `VideoObject` entities across sitemap pages have a non-empty
  `uploadDate`. The SEO validator checks this required field recursively in
  every JSON-LD graph.
- Every sitemap page has an early hero discovery hint.
- CSS-background heroes use matching responsive preload/background candidates
  at the maintained viewport boundaries.
- Blog article `<picture>` heroes use one AVIF preload whose `imagesrcset` and
  `imagesizes` mirror the rendered AVIF source; the hero `<img>` is the only
  `fetchpriority="high"` element on those pages.
- The tubeless-conversion video article keeps the self-hosted MP4 out of the
  initial request graph: its poster is visible immediately and the MP4 source
  is attached only on the first player click. Its visible price, the four
  pricing pages, `OfferCatalog` entries and four generated PDFs all state
  `100 EUR` per wheel.
- The sealing-tape failure case uses the same deferred self-hosted media
  contract with a centered portrait `9 / 16` player. The four new pages have
  five localized FAQ items, and the preceding tubeless-conversion article
  links back to the case in every language.
- News article heroes remain in the CSS-background family protected by the
  responsive CSS hero contract; they are not `<picture>` heroes.
- Registered News galleries use AVIF/WebP/JPEG candidates with explicit
  dimensions and native lazy loading inside a contained horizontal scroll-snap
  region. The BBQ article is the first registered News page using this shared
  gallery path.
- Project heroes retain responsive `<picture>` delivery. Migrated projects,
  Cocktail, Fetish and The First use AVIF/WebP sources with a JPEG fallback;
  Fighter retains its registered AVIF/WebP media set. Every project page has one responsive AVIF
  preload and exactly one `fetchpriority="high"` hero image.
- Registered project exhibition media is rendered through the common project
  generator from `PROJECT_EXHIBITION_MEDIA`; its picture stays lazy and never
  receives high fetch priority.
- Project detail chrome is pre-rendered from the same `GLOBAL_I18N` source as
  the matching language homepage. Sitemap-wide validation compares cookie,
  booking, WhatsApp, header/mobile and footer chrome strings against that
  same-language baseline.
- The desktop and mobile Projects menus derive from `PROJECT_TILES`, the same
  ordered registry as `/projects/`. Sitemap-wide validation protects all 14
  localized project links on every indexable page.
- `llms.txt` is generated from the English page registry, maintained page-name
  sources, metadata and `docs/BUSINESS_FACTS.md`.
- `robots.txt` advertises both `sitemap.xml` and `llms.txt`.
- `sitemap.xml` uses stable, per-page content dates rather than deployment time.

Open performance caveats and external verification limits are in
`docs/OPEN_TASKS.md`.

## External Services And Public Identifiers

| Service | Current public identifier or endpoint |
|---|---|
| Reviews Worker | `https://icm-reviews.vg-ab6.workers.dev/` |
| Lead Worker | `https://icm-leads.vg-ab6.workers.dev/` |
| Cloudflare Web Analytics | owner-managed edge injection; no repository HTML snippet |
| FormSubmit delivery inbox | `Ironcustom.office@gmail.com` |
| FormSubmit action alias | `https://formsubmit.co/c29ab5a6818b2926388e8978888304a2` |

The Google Places API key is a Cloudflare Worker secret and must never appear
in client files or documentation. Account-only risks and verification limits
live in `docs/OPEN_TASKS.md`; variable names live in `.env.example`.

## Current Build Ownership

The exhaustive script/input/output/validator inventory and every executable
command sequence live in `scripts/build/README.md`. Page-family ownership and
stable implementation rules live in `docs/CONTENT_TYPES.md`.

The full documented rebuild currently requires macOS because
`build_pricing_pdfs.py` uses macOS system Arial paths. This is an open
portability risk, not a cross-platform guarantee.

## Corrections Recorded By The FINAL Audit

- **Previous statement:** `HANDOFF.md` contained stale counts and should be
  treated as a current-state conflict.
  **Correction (2026-07-31):** C1 already converted `HANDOFF.md` into a thin
  historical entry point with no competing inventory. Evidence: file review.
- **Previous statement:** all build scripts were path-portable and Python 3.8+
  was sufficient.
  **Correction (2026-07-31):** source syntax requires Python 3.10+, and the PDF
  generator has macOS-only font paths. Evidence: source inspection and a clean
  environment build audit.
- **Previous statement:** one cache-bust value described the whole site.
  **Correction (2026-07-31):** main and project asset families have independent
  values, recorded above. Evidence: sitemap HTML asset scan.
- **Previous terminology:** `EN_PAGES` was treated as a current registry in a
  prior task report.
  **Correction (2026-07-31):** no such registry exists; `PAGES` is canonical.

## Recovery Answer

For a new session: this repository is the production static marketing site for
Iron Custom Motors. Its current inventory is above. Both Workers and the
cookie-free A-MEASURE client are deployed and production-verified. Other
unresolved performance, portability, CDN and external-account work is in
`docs/OPEN_TASKS.md`. Read the affected family in `docs/CONTENT_TYPES.md`, then
use only `scripts/build/README.md` for commands.
