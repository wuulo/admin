"""Etsy Ads CSV analysis for wuulo.

Reads the Etsy Ads daily export (Shop Manager > Marketing > Etsy Ads > Download stats)
and prints all-time totals, campaign periods, a monthly table, order days and
recent-window summaries.

Usage:
    python etsy-ads-analysis.py [path/to/etsy_ads_stats_*.csv]

With no argument it looks for the CSV in the parent folder of this script
(etsy/2026.11.01_stats/). Output of the 31 Oct 2026 run is in
etsy-ads-analysis-output.txt next to this file.
"""
import csv
import glob
import os
import sys
from collections import OrderedDict
from datetime import datetime


def find_csv():
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = glob.glob(os.path.join(here, "..", "etsy_ads_stats_*.csv"))
    if not candidates:
        sys.exit("No etsy_ads_stats_*.csv found in the parent folder; pass the path as an argument.")
    return sorted(candidates)[-1]


path = sys.argv[1] if len(sys.argv) > 1 else find_csv()

rows = []
with open(path, newline="", encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        rows.append(dict(
            date=datetime.strptime(row["Date (ET)"], "%b %d, %Y"),
            views=int(row["Views"]),
            clicks=int(row["Clicks"]),
            orders=int(row["Orders"]),
            revenue=float(row["Revenue (USD)"]),
            spend=float(row["Spend (USD)"]),
            budget=float(row["Ending budget (USD)"]),
        ))


def agg(rs):
    v = sum(x["views"] for x in rs)
    c = sum(x["clicks"] for x in rs)
    o = sum(x["orders"] for x in rs)
    rev = sum(x["revenue"] for x in rs)
    sp = sum(x["spend"] for x in rs)
    active = sum(1 for x in rs if x["spend"] > 0)
    return dict(views=v, clicks=c, orders=o, revenue=rev, spend=sp, active_days=active,
                ctr=(c / v * 100) if v else 0, cpc=(sp / c) if c else 0,
                conv=(o / c * 100) if c else 0, roas=(rev / sp) if sp else 0,
                cpo=(sp / o) if o else None)


def show(label, a):
    cpo = f"${a['cpo']:.2f}" if a["cpo"] is not None else "n/a"
    print(f"{label:<28} days_active={a['active_days']:>3}  views={a['views']:>6}  clicks={a['clicks']:>4}  "
          f"CTR={a['ctr']:.2f}%  spend=${a['spend']:>7.2f}  CPC=${a['cpc']:.2f}  orders={a['orders']}  "
          f"conv={a['conv']:.2f}%  revenue=${a['revenue']:.2f}  ROAS={a['roas']:.2f}  cost/order={cpo}")


print(f"Source: {os.path.basename(path)}  ({rows[0]['date']:%Y-%m-%d} .. {rows[-1]['date']:%Y-%m-%d})")
print("\n=== ALL TIME ===")
show("all time", agg(rows))

print("\n=== CAMPAIGN PERIODS (gaps of >5 zero-spend days split periods) ===")
periods, cur, gap = [], [], 0
for x in rows:
    if x["spend"] > 0 or x["views"] > 0:
        if gap > 5 and cur:
            periods.append(cur)
            cur = []
        cur.append(x)
        gap = 0
    else:
        gap += 1
        if cur:
            cur.append(x)
if cur:
    periods.append(cur)
for p in periods:
    while p and p[-1]["spend"] == 0 and p[-1]["views"] == 0:
        p.pop()
    if not p:
        continue
    budgets = sorted(set(x["budget"] for x in p if x["budget"] > 0))
    show(f"{p[0]['date']:%Y-%m-%d}..{p[-1]['date']:%Y-%m-%d}", agg(p))
    print(f"{'':<28} daily budgets seen: {budgets}")

print("\n=== BY MONTH (months with spend) ===")
months = OrderedDict()
for x in rows:
    months.setdefault(x["date"].strftime("%Y-%m"), []).append(x)
for k, rs in months.items():
    a = agg(rs)
    if a["spend"] > 0:
        show(k, a)

print("\n=== ORDER DAYS ===")
for x in rows:
    if x["orders"]:
        print(f"{x['date']:%Y-%m-%d}: orders={x['orders']} revenue=${x['revenue']:.2f} "
              f"spend that day=${x['spend']:.2f} clicks={x['clicks']}")

print("\n=== RECENT WINDOWS ===")
show("last 30 days", agg(rows[-30:]))
show("last 60 days", agg(rows[-60:]))

o = sum(x["orders"] for x in rows)
rev = sum(x["revenue"] for x in rows)
print(f"\n=== AVG ORDER VALUE (ads) ===\norders={o} revenue=${rev:.2f} AOV=${(rev / o) if o else 0:.2f}")
