#!/usr/bin/env python3
"""How long a Shopify app stays listed, against the same measure on Snowflake."""
import json, pathlib, sys
import plate
from plate import INK, INK2, MUTED, RULE, GRID, FAINT

W, H = 880, 590
SHOP, SNOW = "#2f6f5e", "#8a8880"
# Snowflake's curve, from wss-snowflake-marketplace/public/survival-2026-09-24.json.
# Carried as a handful of points because the comparison is the finding and a
# second repo's full curve is not this repo's to restate.
SNOW_PTS = [(90, .932), (180, .875), (365, .782), (547, .699), (730, .615)]


def main():
    here = pathlib.Path(__file__).resolve()
    src = sys.argv[1] if len(sys.argv) > 1 else str(sorted((here.parents[1] / "public").glob("backfill-*.json"))[-1])
    d = json.load(open(src)); km = d["km"]
    def at(day): return next((s for t, s in reversed(km) if t <= day), 1.0)

    s = plate.open_svg(W, H,
        f"Shopify apps outlast Snowflake data listings at every horizon",
        subtitle=f"Kaplan-Meier, {d['n']:,} apps with an observed arrival across {d['snapshots']} "
                 f"snapshots. {d['deaths']:,} delistings, {d['n']-d['deaths']:,} right-censored.")
    f, y = plate.frame(W, 88,
        who="Anyone choosing which marketplace to build a business or a pipeline on",
        decide="How much delisting risk a third-party dependency carries, by marketplace",
        wrong="The two curves cross, or sit on top of each other")
    s += f

    x0, x1 = 84, W - 168
    top, bot = y + 34, H - 128
    XMAX = 800
    def px(t): return x0 + (x1 - x0) * min(t, XMAX) / XMAX
    def py(v): return bot - (bot - top) * (v - .5) / .5     # zoomed to 50-100%
    for v in (.5, .6, .7, .8, .9, 1.0):
        gy = py(v)
        s.append(f'<line x1="{x0}" y1="{gy:.1f}" x2="{x1}" y2="{gy:.1f}" stroke="{GRID}"/>')
        s.append(plate.txt(x0 - 9, gy + 3.5, f"{int(v*100)}", size=10.5, fill=MUTED, anchor="end"))
    for t in (0, 365, 730):
        gx = px(t)
        s.append(f'<line x1="{gx:.1f}" y1="{top}" x2="{gx:.1f}" y2="{bot}" stroke="{GRID}"/>')
        s.append(plate.txt(gx, bot + 17, f"{t:,}", size=10.5, fill=MUTED, anchor="middle"))
    s.append(plate.txt(x0 - 9, top - 26, "% still listed", size=10, fill=MUTED, anchor="end"))
    s.append(plate.txt(x0 - 9, top - 15, "(axis starts at 50)", size=9, fill=MUTED, anchor="end"))
    s.append(plate.txt((x0 + x1) / 2, bot + 36, "days since first seen", size=10.5, fill=MUTED, anchor="middle"))

    horizon = km[-1][0]
    end = min(XMAX, horizon)
    pts = []; pv = 1.0
    for t, v in km:
        if t > end: break
        pts += [f"{px(t):.1f},{py(pv):.1f}", f"{px(t):.1f},{py(v):.1f}"]; pv = v
    pts.append(f"{px(end):.1f},{py(pv):.1f}")
    sn = " ".join(f"{px(t):.1f},{py(v):.1f}" for t, v in SNOW_PTS)
    s.append(f'<polyline points="{sn}" fill="none" stroke="{SNOW}" stroke-width="2" stroke-dasharray="5 4"/>')
    s.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{SHOP}" stroke-width="2.6"/>')
    s += plate.halo(px(730) + 8, py(.615) + 4, "Snowflake listings", size=11, fill=MUTED)
    s += plate.halo(px(end) + 8, py(pv) + 4, "Shopify apps", size=11.5, fill=SHOP)
    # The cliff near the right edge is an ARTEFACT, not an event. Every departure
    # inside the 254-day archive gap is dated to the same midpoint, so they land
    # as one drop. Marked rather than truncated: hiding it would make the curve
    # look better resolved than it is.
    cliff = max((km[i] for i in range(1, len(km))
                 if km[i-1][1] - km[i][1] > 0.02 and km[i][0] > 600), default=None)
    if cliff:
        cx = px(cliff[0])
        s.append(f'<line x1="{cx:.1f}" y1="{top}" x2="{cx:.1f}" y2="{bot}" stroke="#b4472e" '
                 f'stroke-width="1.2" stroke-dasharray="3 3"/>')
        s += plate.halo(cx - 9, top + 14, "gap artefact — not an event", size=10,
                        fill="#b4472e", anchor="end")

    lx = x1 + 26
    s.append(plate.txt(lx, top + 2, "STILL LISTED", size=9, fill=MUTED, weight="700", spacing="0.9"))
    for i, m in enumerate((90, 365, 730)):
        yy = top + 26 + i * 54
        s += plate.halo(lx, yy, f"{100*at(m):.1f}%", size=16, fill=SHOP)
        s.append(plate.txt(lx, yy + 15, f"at {m:,} days", size=10, fill=MUTED))
        s.append(plate.txt(lx, yy + 28, f"Snowflake {100*dict(SNOW_PTS)[m]:.1f}%", size=10, fill=MUTED))

    s.append(f'<line x1="28" y1="{H-80:.1f}" x2="{W-28}" y2="{H-80:.1f}" stroke="{RULE}"/>')
    s += plate.wrap(28, H - 64,
        f"Shopify sitemap, {d['snapshots']} snapshots {d['span'][0]} to {d['span'][1]}, from the "
        f"Internet Archive plus one live capture. THERE IS A {d['gap_days']}-DAY HOLE in the middle: "
        f"the Archive's last usable capture is 2026-01-13 and the first live one is 2026-09-25, so an "
        f"app that arrived and left inside that window is invisible, and a departure within it can only "
        f"be dated to its midpoint. Snowflake's curve is drawn from wss-snowflake-marketplace at the "
        f"same five horizons.",
        size=10, fill=MUTED, chars=132, leading=13)
    s.append("</svg>")
    out = here.parent / "charts" / "survival.svg"
    out.write_text("\n".join(s), encoding="utf-8")
    print(f"  wrote {out.name}  S(365)={100*at(365):.1f}% S(730)={100*at(730):.1f}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
