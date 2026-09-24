"""Parser for schema_id `shopifyapp.v1` -- the Shopify App Store sitemap.

WHAT MOVES HERE IS AN APP BEING DELISTED, AND NOBODY ELSE IS WATCHING

The Internet Archive holds ZERO mementos of this sitemap. Snowflake's had 46,
Salesforce's 29. So unlike those, there is no backfill to mine and no history to
recover -- which is the argument for capturing rather than against it. Every week
unrecorded is gone, and nothing anywhere will be able to say which apps were on
sale in the meantime.

THE ENTITY IS THE SLUG, BECAUSE THERE IS NOTHING ELSE

Shopify's sitemap gives one thing per app: `https://apps.shopify.com/<slug>`.
There is no id, no vendor field, no date. The slug is both the key and the name,
which has one consequence worth stating: A RENAME IS INDISTINGUISHABLE FROM A
DEATH PLUS A BIRTH. Snowflake avoids this by carrying a stable listing id beside
the slug; here there is no such thing, so a sharp drop in one week paired with a
matching rise should be checked for renames before being read as churn.

`listed` is emitted once per app per capture and its absence later is the
delisting. Nothing else is available from the sitemap, and the detail pages are
~285 KB each -- 7.7 GB for a census -- so they are deliberately not fetched.
"""
import re

from wss import derive

PARSER_VERSION = "1"
SCHEMA_ID = "shopifyapp.v1"

# https://apps.shopify.com/<slug> -- the slug is lower kebab. Anything with a
# further path segment is a category or a collection page, not an app.
APP = re.compile(r"https://apps\.shopify\.com/([a-z0-9][a-z0-9-]*)</loc>")

# Sections of the store that share the app URL shape but are not apps.
NOT_APPS = {"browse", "categories", "collections", "search", "partners",
            "stories", "sitemap", "login", "signup"}


# Four sitemaps, four entity kinds. The kind comes from the URL rather than the
# body, because every one of these files is the same <urlset> shape and nothing
# inside says which it is.
KIND = {"sitemap_apps_en": "app", "sitemap_partners_en": "partner",
        "sitemap_categories_en": "category",
        "sitemap_category_features_en": "category_feature"}
PARTNER = re.compile(r"https://apps\.shopify\.com/partners/([^<?#]+)</loc>")
# Category and category-feature URLs. The feature ones carry a query string --
# ?feature_handles%5B%5D=cf.product_reviews... -- which an earlier `[^<?#]+`
# class excluded, so 2,612 entities silently parsed to zero. Worth knowing that
# Shopify LISTS these in a sitemap while its own robots forbids crawling them
# (Disallow: /*?*); they are usable as identifiers and must never be fetched.
PATHY = re.compile(r"<loc>https://apps\.shopify\.com/(categories/[^<]+)</loc>")


def parse(body: bytes, ctx: derive.ParseContext):
    text = body.decode("utf-8", "replace")
    url = getattr(ctx, "url", "") or ""
    kind = next((v for k, v in KIND.items() if k in url), "app")

    if kind == "app":
        found = (s for s in APP.findall(text) if s not in NOT_APPS)
    elif kind == "partner":
        found = PARTNER.findall(text)
    else:
        found = PATHY.findall(text)

    seen = set()
    for key in found:
        if key in seen:
            continue
        seen.add(key)
        # entity_id is namespaced by kind so a partner handle and an app slug
        # that happen to match cannot collide into one entity.
        yield derive.Observation(entity_id=f"{kind}:{key}", metric="listed",
                                 value=1, unit="count")
        yield derive.Observation(entity_id=f"{kind}:{key}", metric="kind", value=kind)


derive.register(SCHEMA_ID, parse, PARSER_VERSION)
