# Data shape

*Generated 2026-09-30T11:21:19Z by `wss schema` from the derived rows. Do not hand-edit — regenerate after any derive.*

**You should not need to download anything to read this.**

- **243,166 observations** across 1 partition(s), in **1 series**
  - `shopify.appstore.listings` — 243,166 rows, **47752 entities**
- Raw: 7 file(s), 996,553 bytes on disk, 2 capture date(s), 2026-09-24 → 2026-09-30

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
| `kind` | shopify.appstore.listings | 121,583 | 47752 | text |  | 4 | `app`, `category`, `category_feature` |
| `listed` | shopify.appstore.listings | 121,583 | 47752 | bool | count | 1 | `1` |

## Partitions

- `derived/observations/2026-09.csv.gz`
