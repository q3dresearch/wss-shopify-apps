# Data shape

*Generated 2026-10-14T10:35:49Z by `wss schema` from the derived rows. Do not hand-edit — regenerate after any derive.*

**You should not need to download anything to read this.**

- **437,110 observations** across 2 partition(s), in **1 series**
  - `shopify.appstore.listings` — 437,110 rows, **49806 entities**
- Raw: 15 file(s), 2,003,900 bytes on disk, 4 capture date(s), 2026-09-24 → 2026-10-14

## Sources

| source | cadence | endpoints | storage | personal data | licence |
| --- | --- | ---: | --- | --- | --- |
| `shopify.appstore.listings` | weekly | 4 | git | none | NOT ESTABLISHED (checked 2026-09-25). apps.shopify.com/robot |

## Columns

```
series_id, entity_id, observed_at, captured_at, metric, value, unit, source_id, raw_ref, parser_version
```

`entity_id` looks like: **shopify.appstore.listings** `app:011bq-product-swatcher`, `app:1-all-in-one-image-optimizer`, `app:1-click-auto-ai-seo-llms-txt`

## Metrics

| metric | series | rows | entities | type | unit | distinct | range / samples |
| --- | --- | ---: | ---: | --- | --- | ---: | --- |
| `kind` | shopify.appstore.listings | 218,555 | 49806 | text |  | 4 | `app`, `category`, `category_feature` |
| `listed` | shopify.appstore.listings | 218,555 | 49806 | bool | count | 1 | `1` |

## Partitions

- `derived/observations/2026-09.csv.gz`
- `derived/observations/2026-10.csv.gz`
