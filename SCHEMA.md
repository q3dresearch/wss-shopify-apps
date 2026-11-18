# Data shape

*Generated 2026-11-18T14:32:45Z by `wss schema` from the derived rows. Do not hand-edit — regenerate after any derive.*

**You should not need to download anything to read this.**

- **892,448 observations** across 3 partition(s), in **1 series**
  - `shopify.appstore.listings` — 892,448 rows, **55838 entities**
- Raw: 34 file(s), 4,193,366 bytes on disk, 9 capture date(s), 2026-09-24 → 2026-11-18

## Sources

| source | cadence | endpoints | storage | personal data | licence |
| --- | --- | ---: | --- | --- | --- |
| `shopify.appstore.listings` | weekly | 4 | git | none | NOT ESTABLISHED (checked 2026-09-25). apps.shopify.com/robot |

## Columns

```
series_id, entity_id, observed_at, captured_at, metric, value, unit, source_id, raw_ref, parser_version
```

`entity_id` looks like: **shopify.appstore.listings** `app:011bq-product-swatcher`, `app:0rto-cod-form-upsells-otp`, `app:1-all-in-one-image-optimizer`

## Metrics

| metric | series | rows | entities | type | unit | distinct | range / samples |
| --- | --- | ---: | ---: | --- | --- | ---: | --- |
| `kind` | shopify.appstore.listings | 446,224 | 55838 | text |  | 4 | `app`, `category`, `category_feature` |
| `listed` | shopify.appstore.listings | 446,224 | 55838 | bool | count | 1 | `1` |

## Partitions

- `derived/observations/2026-09.csv.gz`
- `derived/observations/2026-10.csv.gz`
- `derived/observations/2026-11.csv.gz`
