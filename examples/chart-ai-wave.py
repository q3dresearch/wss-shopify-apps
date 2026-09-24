#!/usr/bin/env python3
"""AI apps are arriving five times faster and dying faster."""
import json, pathlib, sys
import plate
from plate import INK, INK2, MUTED, RULE, GRID, FAINT

W, H = 880, 648
AI, OTHER = "#b4472e", "#2f6f5e"


def main():
    here = pathlib.Path(__file__).resolve()
    src = sys.argv[1] if len(sys.argv) > 1 else str(sorted((here.parents[1] / "public").glob("niches-*.json"))[-1])
    d = json.load(open(src)); tl = d["timeline"]; coh = d["cohorts"]
    sh0, sh1 = 100*tl[0]["ai"]/tl[0]["n"], 100*tl[-1]["ai"]/tl[-1]["n"]

    s = plate.open_svg(W, H,
        f"AI apps went from {sh0:.1f}% of the store to {sh1:.1f}% — and they die faster",
        subtitle=f"Apps whose slug carries an `ai` token, against all others. "
                 f"{d['timeline'][0]['date']} to {d['timeline'][-1]['date']}.")
    f, y = plate.frame(W, 88,
        who="Anyone deciding whether to build, buy or depend on an AI app on Shopify",
        decide="Whether the AI surge is durable supply or a wave that clears",
        wrong="The survival gap disappears once arrival year is held constant")
    s += f

    # LEFT: share over time. RIGHT: survival gap by cohort. Two panels, one claim.
    lx0, lx1 = 78, 430
    rx0, rx1 = 520, W - 150
    top, bot = y + 42, H - 190

    s.append(plate.txt(lx0, top - 16, "SHARE OF THE STORE", size=9, fill=MUTED, weight="700", spacing="0.8"))
    mx = max(100*t["ai"]/t["n"] for t in tl)
    def lpx(i): return lx0 + (lx1 - lx0) * i / (len(tl) - 1)
    def lpy(v): return bot - (bot - top) * v / (mx * 1.12)
    for v in (0, 2, 4, 6):
        gy = lpy(v)
        s.append(f'<line x1="{lx0}" y1="{gy:.1f}" x2="{lx1}" y2="{gy:.1f}" stroke="{GRID}"/>')
        s.append(plate.txt(lx0 - 8, gy + 3.5, f"{v}", size=10, fill=MUTED, anchor="end"))
    pts = " ".join(f"{lpx(i):.1f},{lpy(100*t['ai']/t['n']):.1f}" for i, t in enumerate(tl))
    s.append(f'<polyline points="{pts}" fill="none" stroke="{AI}" stroke-width="2.6"/>')
    for i in (0, len(tl) - 1):
        t = tl[i]
        s.append(f'<circle cx="{lpx(i):.1f}" cy="{lpy(100*t["ai"]/t["n"]):.1f}" r="4" fill="{AI}"/>')
    s += plate.halo(lx0 + 4, lpy(sh0) - 10, f"{sh0:.1f}%  ({tl[0]['ai']} apps)", size=10.5, fill=AI)
    s += plate.halo(lx1, lpy(sh1) - 12, f"{sh1:.1f}%  ({tl[-1]['ai']:,} apps)", size=11.5, fill=AI, anchor="end")
    s.append(plate.txt(lx0, bot + 17, tl[0]["date"][:7], size=10, fill=MUTED))
    s.append(plate.txt(lx1, bot + 17, tl[-1]["date"][:7], size=10, fill=MUTED, anchor="end"))

    s.append(plate.txt(rx0, top - 16, "STILL LISTED AT ONE YEAR, BY ARRIVAL YEAR",
                       size=9, fill=MUTED, weight="700", spacing="0.8"))
    bw = 46
    for j, c in enumerate(coh):
        gx = rx0 + 40 + j * 150
        for k, (lab, v, n, col) in enumerate((("AI", c["ai"], c["ai_n"], AI),
                                              ("other", c["other"], c["other_n"], OTHER))):
            bx = gx + k * (bw + 12)
            h = (bot - top) * (v - .5) / .5
            s.append(f'<rect x="{bx}" y="{bot-h:.1f}" width="{bw}" height="{h:.1f}" rx="3" '
                     f'fill="{col}" fill-opacity="0.9"/>')
            s += plate.halo(bx + bw/2, bot - h - 8, f"{100*v:.0f}%", size=12, fill=col, anchor="middle")
            s.append(plate.txt(bx + bw/2, bot + 15, lab, size=9.5, fill=MUTED, anchor="middle"))
            s.append(plate.txt(bx + bw/2, bot + 27, f"n={n:,}", size=8.5, fill=MUTED, anchor="middle"))
        s += plate.halo(gx + bw + 6, bot + 43, f"arrived {c['year']}", size=10.5, fill=INK2, anchor="middle")
    s.append(plate.txt(rx0, bot + 3, "50", size=9.5, fill=MUTED, anchor="end"))

    s += plate.halo(78, bot + 72,
        f"AI apps: {100*d['ai_s365']:.1f}% at one year and {100*d['ai_s730']:.1f}% at two, "
        f"against {100*d['other_s365']:.1f}% and {100*d['other_s730']:.1f}% for everything else.",
        size=12, fill=INK)

    s.append(f'<line x1="28" y1="{H-72:.1f}" x2="{W-28}" y2="{H-72:.1f}" stroke="{RULE}"/>')
    s += plate.wrap(28, H - 56,
        "Shopify sitemap, 55 snapshots 2023-06-20 to 2026-09-25, Internet Archive plus one live "
        "capture. An app counts as AI if `ai` is a whole hyphen-separated token in its slug, which "
        "catches `ai-product-description` and not `hair` or `email`. 2023 is omitted from the right "
        "panel: only 5 AI apps arrived that year. The gap holds INSIDE each cohort, so it is not "
        "explained by AI apps being younger.",
        size=10, fill=MUTED, chars=132, leading=13)
    s.append("</svg>")
    out = here.parent / "charts" / "ai-wave.svg"
    out.write_text("\n".join(s), encoding="utf-8")
    print(f"  wrote {out.name}  share {sh0:.1f}%->{sh1:.1f}%, S365 {100*d['ai_s365']:.1f} vs {100*d['other_s365']:.1f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
