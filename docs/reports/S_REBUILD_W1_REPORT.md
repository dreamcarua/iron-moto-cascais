# S-REBUILD-W1 Delivery Report

Date: 2026-09-06 (Europe/Lisbon)

Baseline commit: `45405dd99797294dc229cf359391ddda4d6a6bf3`

Implementation commit: `42c5173246803626e7da06f99cfdb73e40d2d1ff`

Initial GitHub Pages workflow: `34060700603` (`success`, 46 seconds)

## Delivered Scope

The following eight hubs were rebuilt from approved four-language copy through
one shared source parser and renderer:

- `https://ironcustommotors.com/motorcycle-service/`
- `https://ironcustommotors.com/pt/motorcycle-service/`
- `https://ironcustommotors.com/ru/motorcycle-service/`
- `https://ironcustommotors.com/uk/motorcycle-service/`
- `https://ironcustommotors.com/custom/`
- `https://ironcustommotors.com/pt/custom/`
- `https://ironcustommotors.com/ru/custom/`
- `https://ironcustommotors.com/uk/custom/`

All eight production URLs returned HTTP 200 after deployment and matched the
repository output under cache-bypass requests. The four Pricing pages use the
approved 2026 title, metadata, eyebrow and H1. Only the four approved meta
description lines changed in the tyre-service source; semantic body comparison
against the baseline confirmed that their visible content is unchanged.

The two hub copy files were copied byte-for-byte from the amended owner inputs.
The input and repository hashes are:

```text
c16a33ae3c204084a9e5356c2bd0a3b7c9d99dcfd44b30752565cea49f38d28c  service_hub_copy_4lang.md
10790be1dab936791dd01b47bcfa9c3f1c73e12cc495275d2195a025a14f4292  custom_hub_copy_4lang.md
9414a8f95ab5ac910cc4c651c196ac2aecd1170389a413bd23db822598a854bd  2026-09-06_W1_metas-pricing_4lang.md
```

Source-specific validation checks the complete approved titles, descriptions,
H1s, section order, headings, paragraphs, descriptive links, localized
WhatsApp prefill and all FAQ question/answer pairs. Source-only notes and
placeholders do not appear in generated HTML. Each hub has one H1 and that H1
differs from its same-language homepage H1. Repository and generated output
contain no legacy `msr.*`/`cs.*` copy keys and no unresolved
`{{PROJECT_CUSTOM_LINKS}}` token.

## Hub Integration And Schema

The Custom project block is generated from the shared project registry between
the existing `PROJECT_CUSTOM_LINKS_START/END` markers. It contains, in
`PROJECT_TILES` order, Inspirium, Beckman, Unbreakable, Quanta-R, Burly,
Sturmvogel, Geometric, Joker, Hellboy, True Religion, Fighter, Cocktail,
Fetish and The First. All 14 links are language-local on every Custom variant.
All 14 project validators passed after the integration flag was enabled for
the complete portfolio.

Every hub graph contains `Service`, `FAQPage`, `BreadcrumbList`, `WebPage` and
the resolved shared `LocalBusiness` entity. The six visible FAQ items are
generated from the same parsed objects as the six schema questions and match
1:1 in every language. No `Offer` or `Product` entity appears on either family.
Every visible Service price is present in `pricing_data.py`; Custom contains no
euro amount. The amended Custom FAQ links electrical repairs on stock
motorcycles to the same-language Service hub.

Canonical URLs are self-referential, and every page carries mutual `en`,
`pt-PT`, `ru`, `uk` and `x-default` alternates. Header, mobile navigation,
footer, cookie controls and lead-modal chrome are rendered from the shared
same-language registry.

Google Rich Results Test crawled two deployed representatives successfully:

- EN Service result `ICpuxGmwcmItgg35JinkCg`: three valid items, no errors;
- PT Custom result `xR2ntFNq3QrtmJfydF3OeA`: three valid items, no errors.

Both results reported valid Breadcrumbs, Local business and Organization
items. `Service` and `FAQPage` remain present and locally validated even though
Google does not expose them as eligible result categories in this test UI.

## Lead Wiring And Responsive Delivery

The generated CTAs preserve the activated FormSubmit alias and the localized
absolute `_next` URL. WhatsApp uses `https://wa.me/351917961230` with the exact
source prefill, telephone uses `tel:+351917961230`, and the request CTA opens
the existing `leadForm` modal. The permanent SEO validator also confirms the
private FormSubmit action on every generated hub.

A production browser session using the reserved `?icm-leads-test=1` mode
opened the EN Service request modal and followed the WhatsApp CTA. The private
test counters recorded one `form_view` and one `whatsapp` event under
`/**test**/`; no form was submitted. The browser harness blocked the external
`tel:` protocol before dispatch, so a new end-to-end telephone event was not
claimed. The exact telephone href, delegated unchanged A-MEASURE handler and
production HTML were verified statically; the earlier A-MEASURE deployment
has independent production evidence for that event type. One ordinary
`form_view` on `/custom/` was emitted accidentally during the first live modal
check; it was not a submission or message.

At 390 px and 1440 px, both hub families had `scrollWidth == clientWidth`, six
FAQ items and one selected CSS-background hero resource. Cold requests selected
the registered 768 AVIF candidate at the mobile viewport and the 1920 AVIF
candidate at the desktop viewport, with no WebP/JPEG duplicate. The responsive
hero validator also passed all maintained viewport/DPR cases.

## Sitemap And Discovery

The sitemap remains at 236 URLs. Its baseline SHA-256 was
`4ef974f467c30c2e67efe7e276dbb6b03f93efd87959a3e72d7178673a9c31ae`;
the implementation SHA-256 is
`52aead525994703b941a5cca0f5dd94bc9589b651267a500fda767bf7e331956`.
Production and repository bytes match.

Exactly these 12 existing URLs received a new honest `lastmod`:

| URL | New `lastmod` |
|---|---|
| `https://ironcustommotors.com/motorcycle-service/` | `2026-09-06T22:09:31+01:00` |
| `https://ironcustommotors.com/ru/motorcycle-service/` | `2026-09-06T22:09:31+01:00` |
| `https://ironcustommotors.com/uk/motorcycle-service/` | `2026-09-06T22:09:32+01:00` |
| `https://ironcustommotors.com/pt/motorcycle-service/` | `2026-09-06T22:09:32+01:00` |
| `https://ironcustommotors.com/custom/` | `2026-09-06T22:09:32+01:00` |
| `https://ironcustommotors.com/ru/custom/` | `2026-09-06T22:09:32+01:00` |
| `https://ironcustommotors.com/uk/custom/` | `2026-09-06T22:09:32+01:00` |
| `https://ironcustommotors.com/pt/custom/` | `2026-09-06T22:09:32+01:00` |
| `https://ironcustommotors.com/pricing/` | `2026-09-06T22:05:47+01:00` |
| `https://ironcustommotors.com/pt/pricing/` | `2026-09-06T22:05:50+01:00` |
| `https://ironcustommotors.com/ru/pricing/` | `2026-09-06T22:05:53+01:00` |
| `https://ironcustommotors.com/uk/pricing/` | `2026-09-06T22:05:57+01:00` |

The tyre-service timestamps stayed byte-for-byte at their prior values:

```text
EN  2026-08-09T10:02:41+01:00
PT  2026-08-09T10:02:43+01:00
RU  2026-08-09T10:02:47+01:00
UK  2026-08-09T10:02:50+01:00
```

No other sitemap date changed. Generated and deployed `llms.txt` also match the
repository artifact.

## Verification

The focused family validator passed all eight hubs, four Pricing pages and four
tyre metadata variants. The canonical validation gates reported:

```text
SEO validation passed: 236 sitemap URL(s)
Brand page validation passed: 7 brand page set(s).
Harley Hub validation passed: 12 pages and all required integrations
Service/Custom hub validation passed: 8 hubs, 4 pricing pages, 4 tyre metas.
```

All 14 registered project validators reported success. The sitemap-wide SEO
pass found zero broken internal links and complete hreflang/chrome parity.
CSS-background hero preload checks passed 108 pages, picture-hero checks passed
36 pages across the five maintained viewport/DPR cases, and project navigation
checks passed all 236 indexable pages. `node --check`, Python compilation and
`git diff --check` passed.

The complete documented generator sequence, with pricing PDFs skipped as the
brief requires, was run again after the implementation commit and left
`git status --short` empty. The final documentation commit is followed by a
separate clean-clone rebuild gate from the canonical GitHub remote.

## Diff Scope And Deviations

Implementation commit `42c51732` contains 264 files: 240 generated HTML files
and 24 source, generator, data, documentation or discovery files. The
substantive page changes are exactly eight hubs, four Pricing pages and the
four tyre page heads. Retiring dead Custom hub i18n keys changed
`assets/main.js`, which required the documented site-wide common cache-bust
from `20260902b` to `20260906a`; 224 other generated HTML files therefore have
cache-reference-only output. The shared legal renderer was also made to own
its established `/photos/og.jpg` metadata explicitly so a deterministic full
rebuild no longer inherits the new Service hero. Their visible content did not
change. Homepage H1/copy, URLs, redirects, Workers, secrets, CI workflows,
FormSubmit configuration and sitemap membership were not changed.

The only acceptance limitation is the browser harness refusal to dispatch the
external telephone protocol noted above. No PDF was regenerated, as the task
explicitly excluded the macOS PDF step. No external system was changed apart
from the normal Git push, GitHub Pages deployment, two Google Rich Results
tests and reserved anonymous A-MEASURE acceptance events.
