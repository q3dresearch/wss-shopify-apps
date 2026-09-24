#!/usr/bin/env python3
"""Archive coverage of each marketplace's index, measured 2026-09-25."""
import pathlib, sys
import plate
from plate import INK, INK2, MUTED, RULE, GRID, FAINT

W, H = 880, 566
ALERT, SERIES = "#b4472e", "#2f6f5e"
# Measured with the Internet Archive CDX API, 2026-09-25. "usable" counts
# mementos over 50 KB, the ones large enough to carry listings.
ROWS = [("Snowflake Marketplace", 46, 31, False),
        ("Salesforce AppExchange", 29, 28, False),
        ("Atlassian Marketplace", 23, 23, False),
        ("Databricks Marketplace", 3, 2, False),
        ("Microsoft Edge add-ons", 2, 2, False),
        ("Shopify App Store", 0, 0, True)]


def main():
    here = pathlib.Path(__file__).resolve()
    s = plate.open_svg(W, H,
        "Nobody has kept a copy of the Shopify App Store",
        subtitle="Internet Archive mementos of each marketplace's own index, measured 2026-09-25. "
                 "Shaded bars are captures large enough to carry listings.")
    f, y = plate.frame(W, 88,
        who="Anyone choosing which marketplace to start capturing",
        decide="Whether to pick the one with history to mine, or the one with none",
        wrong="Shopify turns out to have mementos under another URL — then it is not unwatched")
    s += f

    x0, x1 = 226, W - 210
    top = y + 30
    rowh = 40
    mx = max(r[1] for r in ROWS) or 1
    for i, (lab, n, usable, hero) in enumerate(ROWS):
        ry = top + i * rowh
        col = ALERT if hero else SERIES
        bw = (x1 - x0) * n / mx
        if n:
            s.append(f'<rect x="{x0}" y="{ry:.1f}" width="{bw:.1f}" height="17" rx="3" '
                     f'fill="{col}" fill-opacity="0.30"/>')
            s.append(f'<rect x="{x0}" y="{ry:.1f}" width="{(x1-x0)*usable/mx:.1f}" height="17" rx="3" '
                     f'fill="{col}" fill-opacity="0.95"/>')
            s += plate.halo(x0 + bw + 9, ry + 13, f"{n}", size=12.5, fill=INK2)
        else:
            # A zero must be VISIBLE. An empty row reads as a missing row.
            s.append(f'<line x1="{x0}" y1="{ry+8.5:.1f}" x2="{x0+13:.1f}" y2="{ry+8.5:.1f}" '
                     f'stroke="{ALERT}" stroke-width="3"/>')
            s += plate.halo(x0 + 20, ry + 13, "zero mementos — no copy exists anywhere",
                            size=12.5, fill=ALERT)
        s.append(plate.txt(x0 - 12, ry + 13, lab, size=11.5,
                           fill=INK if hero else MUTED, anchor="end",
                           weight="600" if hero else "normal"))
    bot = top + len(ROWS) * rowh
    s += plate.wrap(x0 - 12, bot + 14,
        "An absent archive is the strongest reason to capture, not the weakest. The five above are "
        "partly held by somebody else. This one is not held at all, so every week unrecorded is gone.",
        size=11, fill=INK2, chars=86, leading=14)

    s.append(f'<line x1="28" y1="{H-72:.1f}" x2="{W-28}" y2="{H-72:.1f}" stroke="{RULE}"/>')
    s += plate.wrap(28, H - 56,
        "Internet Archive CDX, collapsed on digest, 2026-09-25. Counted against each marketplace's own "
        "listing index -- sitemap_apps_en.xml for Shopify, sitemap.xml for the others, "
        "sitemap-listings.xml for Atlassian. A zero here is a measured absence, not an unqueried one: "
        "CDX answered 200 with an empty result.",
        size=10, fill=MUTED, chars=132, leading=13)
    s.append("</svg>")
    out = here.parent / "charts" / "nobody-is-watching.svg"
    out.write_text("\n".join(s), encoding="utf-8")
    print(f"  wrote {out.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
