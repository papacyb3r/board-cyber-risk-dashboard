#!/usr/bin/env python3
"""Build a self-contained HTML board dashboard of cyber risk indicators.

Usage: python build_dashboard.py kri_data.csv dashboard.html
All sample data is fictional.
"""
import csv
import html
import sys

STATUS = {
    "green": ("On target", "#1a7f4b"),
    "amber": ("Watch", "#b26a00"),
    "red": ("Action needed", "#b3261e"),
}


def status(v, target, red, higher_is_worse):
    if higher_is_worse:
        return "green" if v <= target else "amber" if v <= red else "red"
    return "green" if v >= target else "amber" if v >= red else "red"


def sparkline(values, colour, w=140, h=36):
    lo, hi = min(values), max(values)
    span = (hi - lo) or 1
    pts = []
    for i, v in enumerate(values):
        x = 4 + i * (w - 8) / (len(values) - 1)
        y = h - 4 - (v - lo) * (h - 8) / span
        pts.append((x, y))
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    x, y = pts[-1]
    return (f'<svg width="{w}" height="{h}" role="img" aria-label="Trend">'
            f'<polyline fill="none" stroke="{colour}" stroke-width="2" points="{line}"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="{colour}"/></svg>')


def fmt(v):
    return f"{v:g}"


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    with open(sys.argv[1], newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    periods = [c for c in rows[0] if c not in
               ("kri", "unit", "higher_is_worse", "target", "red")]
    cards, counts = [], {"green": 0, "amber": 0, "red": 0}
    for r in rows:
        vals = [float(r[p]) for p in periods]
        hw = r["higher_is_worse"].strip().lower() == "yes"
        s = status(vals[-1], float(r["target"]), float(r["red"]), hw)
        counts[s] += 1
        label, colour = STATUS[s]
        improving = (vals[-1] < vals[0]) if hw else (vals[-1] > vals[0])
        trend = "Improving" if improving else "Worsening"
        cards.append(
            f'<div class="card"><div class="name">{html.escape(r["kri"])}</div>'
            f'<div class="val">{fmt(vals[-1])}<span class="unit"> {html.escape(r["unit"])}</span></div>'
            f'<div class="badge" style="color:{colour};border-color:{colour}">'
            f'{label}</div>'
            f'{sparkline(vals, colour)}'
            f'<div class="meta">Target {fmt(float(r["target"]))} {html.escape(r["unit"])} &middot; '
            f'{trend} since {html.escape(periods[0])}</div></div>')
    summary = (f'{counts["green"]} on target &middot; {counts["amber"]} to watch '
               f'&middot; {counts["red"]} need action')
    page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cyber Risk Dashboard</title>
<style>
body{{font-family:system-ui,Segoe UI,Arial,sans-serif;margin:0;background:#f6f7f9;color:#1c2430}}
header{{background:#14213d;color:#fff;padding:24px 32px}}
header h1{{margin:0;font-size:22px}} header p{{margin:6px 0 0;opacity:.85}}
main{{padding:24px 32px;max-width:1100px;margin:auto}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:16px}}
.card{{background:#fff;border:1px solid #dde1e7;border-radius:10px;padding:16px}}
.name{{font-size:14px;color:#46515f;min-height:36px}}
.val{{font-size:32px;font-weight:600;margin:4px 0}} .unit{{font-size:14px;font-weight:400;color:#46515f}}
.badge{{display:inline-block;border:1px solid;border-radius:12px;padding:2px 10px;font-size:12px;font-weight:600;margin-bottom:8px}}
.meta{{font-size:12px;color:#46515f;margin-top:6px}}
footer{{padding:16px 32px;font-size:12px;color:#46515f;max-width:1100px;margin:auto}}
</style></head><body>
<header><h1>Cyber Risk Dashboard</h1><p>{summary} &middot; Latest period: {html.escape(periods[-1])}</p></header>
<main><div class="grid">{''.join(cards)}</div></main>
<footer>Illustrative sample data. Status is shown by label as well as colour. Thresholds are set per indicator in the CSV.</footer>
</body></html>"""
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write(page)
    print(f"Wrote {sys.argv[2]}: {summary.replace('&middot;', '|')}")


if __name__ == "__main__":
    main()
