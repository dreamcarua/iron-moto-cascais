# Iron Custom Motors Business Facts

This file is the single canonical documentation source for Iron Custom Motors
business facts. Other documentation must link here instead of copying these
values. Published site content and external listings must match this record
exactly.

The JSON block is machine-readable and is consumed by
`scripts/build/build_llms.py`. Do not change its structure without updating
that parser.

```json
{
  "tradingName": "Iron Custom Motors",
  "legalName": "Iron Custom Motors, Lda",
  "fullAddress": "R. António José da Silva 100 B, 2785-253 São Domingos de Rana, Cascais, Lisbon, Portugal",
  "phoneAndWhatsApp": "+351 917 961 230",
  "listingEmail": "Ironcustom.office@gmail.com",
  "openingHours": {
    "openDays": [
      "Tuesday",
      "Wednesday",
      "Thursday",
      "Friday",
      "Saturday"
    ],
    "opens": "10:00",
    "closes": "18:00",
    "closedDays": [
      "Sunday",
      "Monday"
    ],
    "timezone": "Europe/Lisbon"
  },
  "foundingYear": 2010,
  "foundingPlace": "Kharkiv, Ukraine",
  "founder": "Yaroslav Lutytskyi",
  "serviceLanguages": [
    {
      "code": "en",
      "name": "English"
    },
    {
      "code": "ru",
      "name": "Russian"
    },
    {
      "code": "uk",
      "name": "Ukrainian"
    },
    {
      "code": "pt",
      "name": "Portuguese"
    }
  ],
  "profiles": {
    "instagram": "https://www.instagram.com/ironcustommotors/",
    "facebook": "https://www.facebook.com/IronCustomMotors/",
    "youtube": "https://www.youtube.com/@IronCustomMotors"
  },
  "pricingSource": "scripts/build/pricing_data.py",
  "pricingUrl": "https://ironcustommotors.com/pricing/",
  "publishedKeyPrices": [
    {
      "name": "Other workshop work",
      "price": "50 EUR per hour"
    },
    {
      "name": "Pre-purchase inspection",
      "price": "150 EUR"
    },
    {
      "name": "Fault diagnostics",
      "price": "50–350 EUR"
    },
    {
      "name": "Scheduled maintenance",
      "price": "from 150 EUR"
    },
    {
      "name": "Ducati Desmo valve-clearance check",
      "price": "550 EUR"
    },
    {
      "name": "Ducati Desmo valve-clearance check and adjustment",
      "price": "1,200 EUR"
    },
    {
      "name": "Harley-Davidson scheduled maintenance",
      "price": "300 EUR"
    },
    {
      "name": "Tubeless conversion of one spoked wheel",
      "price": "100 EUR per wheel"
    }
  ],
  "pricingNote": "Published prices include applicable taxes and fees and are indicative unless explicitly stated as fixed. The final amount depends on the motorcycle and confirmed scope of work."
}
```

## Custom Build Policy

The owner confirmed these facts on 2026-09-06:

- The initial custom-project consultation is always free.
- The workshop accepts custom builds as complete projects; it does not accept
  standalone paint or wiring jobs. Electrical repairs on stock motorcycles
  belong to the service workflow.
- No prices are published for custom builds. Scope, budget and timeline are
  agreed for each complete project after the free consultation.

## Maintenance Rules

- Verify NAP, hours, founder, origin, service languages and profile URLs here
  before changing site copy or external listings.
- Treat [scripts/build/pricing_data.py](../scripts/build/pricing_data.py) as
  the implementation source of truth for the full current price list. Update
  this record when published key prices change there.
- Do not store credentials, API keys, account recovery details or other
  secrets in this file.
