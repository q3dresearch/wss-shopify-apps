#!/usr/bin/env python3
"""Reviews against age, alive and dead. Rating was tested as a fourth axis and dropped."""
import json, math, pathlib, sys
import plate
from plate import INK, INK2, MUTED, RULE, GRID, FAINT

W, H = 880, 620
LIVE, DEAD = "#2f6f5e", "#b4472e"


def main():
    here = pathlib.Path(__file__).resolve()
    src = sys.argv[1] if len(sys.argv) > 1 else str(sorted((here.parents[1] / "public").glob("rating-sample-*.json"))[-1])
    d = json.load(open(src))
    live = [o for o in d if o["fate"] == "live"]; dead = [o for o in d if o["fate"] == "dead"]
    lr = [o for o in live if o["rating"] is not None]; dr = [o for o in dead if o["rating"] is not None]
    pl, pd = 100*len(lr)/len(live), 100*len(dr)/len(dead)

    s = plate.open_svg(W, H,
        f"Having any review at all separates them. The score does not.",
        subtitle=f"{len(live)} live and {len(dead)} delisted apps sampled at a fixed seed. Rated: "
                 f"{pl:.0f}% of live against {pd:.0f}% of dead — but the median rating is 5.0 in both.")
    f, y = plate.frame(W, 88,
        who="Anyone using a store rating to judge whether an app is a safe dependency",
        decide="Which signal to trust — the score, the review count, or neither",
        wrong="Dead apps carry visibly lower ratings than live ones")
    s += f

    x0, x1 = 84, W - 250
    top, bot = y + 34, H - 168
    XMIN, XMAX = 1, 1000
    def px(v): return x0 + (x1-x0) * (math.log10(max(v, XMIN)) / math.log10(XMAX))
    ages = [o["age"] for o in lr+dr] or [1]
    AMAX = max(ages) * 1.08
    def py(a): return bot - (bot-top) * a / AMAX
    for v in (1, 10, 100, 1000):
        gx = px(v)
        s.append(f'<line x1="{gx:.1f}" y1="{top}" x2="{gx:.1f}" y2="{bot}" stroke="{GRID}"/>')
        s.append(f'<text x="{gx:.1f}" y="{bot+18}" font-size="10.5" fill="{MUTED}" text-anchor="middle" '
                 f'style="font-variant-numeric: tabular-nums">10<tspan dy="-5" font-size="7.5">'
                 f'{int(math.log10(v))}</tspan></text>')
    for a in (0, 365, 730, 1095):
        if a > AMAX: continue
        gy = py(a)
        s.append(f'<line x1="{x0}" y1="{gy:.1f}" x2="{x1}" y2="{gy:.1f}" stroke="{GRID}"/>')
        s.append(plate.txt(x0-9, gy+3.5, f"{a:,}", size=10.5, fill=MUTED, anchor="end"))
    s.append(plate.txt(x0-9, top-14, "days observed", size=10, fill=MUTED, anchor="end"))
    s.append(plate.txt((x0+x1)/2, bot+38, "reviews", size=10.5, fill=MUTED, anchor="middle"))

    for grp, col in ((lr, LIVE), (dr, DEAD)):
        for o in grp:
            s.append(f'<circle cx="{px(o["reviews"]):.1f}" cy="{py(o["age"]):.1f}" r="5.5" '
                     f'fill="{col}" fill-opacity="0.55" stroke="{plate.SURFACE}" stroke-width="1.1"/>')

    lx = x1 + 26
    s.append(plate.txt(lx, top+2, "OF THOSE SAMPLED", size=9, fill=MUTED, weight="700", spacing="0.8"))
    for i,(lab,n,tot,col,pct) in enumerate((("still listed",len(lr),len(live),LIVE,pl),
                                            ("delisted",len(dr),len(dead),DEAD,pd))):
        yy = top + 26 + i*76
        s.append(f'<rect x="{lx}" y="{yy-10:.1f}" width="12" height="12" rx="2" fill="{col}"/>')
        s += plate.halo(lx+19, yy, lab, size=12, fill=INK)
        s += plate.halo(lx, yy+22, f"{pct:.0f}% rated", size=15, fill=col)
        s.append(plate.txt(lx, yy+37, f"{n} of {tot}", size=10, fill=MUTED))

    s += plate.halo(x0, bot+62,
        "Rating was tested as a fourth axis and dropped: median 5.0 on both sides.",
        size=12, fill=INK)
    s += plate.wrap(x0, bot+80,
        "A y-axis that does not vary is a wasted axis, so it is named here rather than drawn.",
        size=10.5, fill=MUTED, chars=96, leading=13)

    s.append(f'<line x1="28" y1="{H-72:.1f}" x2="{W-28}" y2="{H-72:.1f}" stroke="{RULE}"/>')
    s += plate.wrap(28, H-56,
        f"Shopify, 2026-09-25, random.seed(20260925). Live ratings read from the page today; DEAD ones "
        f"from each app's last Internet Archive capture, so they predate the delisting by an unknown "
        f"margin. THE DEAD SAMPLE IS DOUBLY FILTERED: 19 of 70 have no archived page at all, and only "
        f"13 carry a rating — so 'dead apps are less often rated' is partly a statement about Archive "
        f"coverage. n=25 and n=13 is thin; read it as directional.",
        size=10, fill=MUTED, chars=132, leading=13)
    s.append("</svg>")
    out = here.parent / "charts" / "what-predicts-death.svg"
    out.write_text("\n".join(s), encoding="utf-8")
    print(f"  wrote {out.name}  live {pl:.0f}% rated vs dead {pd:.0f}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
