# Data shape

*Generated 2026-09-24T16:44:05Z by `wss schema` from the derived rows. Do not hand-edit — regenerate after any derive.*

**You should not need to download anything to read this.**

- **27,071 observations** across 1 partition(s), in **1 series**
  - `shopify.appstore.listings` — 27,071 rows, **27071 entities**
- Raw: 1 file(s), 289,148 bytes on disk, 1 capture date(s), 2026-09-24 → 2026-09-24

## Sources

| source | cadence | endpoints | storage | personal data | licence |
| --- | --- | ---: | --- | --- | --- |
| `shopify.appstore.listings` | weekly | 1 | git | none | NOT ESTABLISHED (checked 2026-09-25). apps.shopify.com/robot |

## Columns

```
series_id, entity_id, observed_at, captured_at, metric, value, unit, source_id, raw_ref, parser_version
```

`entity_id` looks like: **shopify.appstore.listings** `011bq-product-swatcher`, `1-all-in-one-image-optimizer`, `1-click-auto-ai-seo-llms-txt`

## Metrics

| metric | series | rows | entities | type | unit | distinct | range / samples |
| --- | --- | ---: | ---: | --- | --- | ---: | --- |
| `listed` | shopify.appstore.listings | 27,071 | 27071 | bool | count | 1 | `1` |

## Partitions

- `derived/observations/2026-09.csv.gz`
