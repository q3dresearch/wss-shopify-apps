# Data shape

*Generated 2026-11-25T16:02:09Z by `wss schema` from the derived rows. Do not hand-edit — regenerate after any derive.*

**You should not need to download anything to read this.**

- **977,026 observations** across 3 partition(s), in **1 series**
  - `shopify.appstore.listings` — 977,026 rows, **56866 entities**
- Raw: 38 file(s), 4,618,685 bytes on disk, 10 capture date(s), 2026-09-24 → 2026-11-25

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
| `kind` | shopify.appstore.listings | 488,513 | 56866 | text |  | 4 | `app`, `category`, `category_feature` |
| `listed` | shopify.appstore.listings | 488,513 | 56866 | bool | count | 1 | `1` |

## Partitions

- `derived/observations/2026-09.csv.gz`
- `derived/observations/2026-10.csv.gz`
- `derived/observations/2026-11.csv.gz`
