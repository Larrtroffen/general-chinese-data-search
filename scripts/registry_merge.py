#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""registry_merge —— 汇总 registry/*.csv → registry/all.csv（并打印各层计数）。

用法：python3 scripts/registry_merge.py
"""
from __future__ import annotations

import csv
import glob
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = os.path.join(ROOT, 'registry')


def main():
    rows = []
    counts = {}
    for path in sorted(glob.glob(os.path.join(REG, '*.csv'))):
        name = os.path.basename(path)
        if name == 'all.csv':
            continue
        with open(path, newline='', encoding='utf-8') as f:
            rs = list(csv.DictReader(f))
        counts[name[:-4]] = len(rs)
        rows.extend(rs)
    seen = set()
    dedup = []
    for r in rows:
        key = (r.get('tier'), r.get('url'))
        if key in seen:
            continue
        seen.add(key)
        dedup.append(r)
    fields = ['id', 'tier', 'name', 'url', 'host', 'status', 'http_code', 'probe_date', 'note', 'ref']
    with open(os.path.join(REG, 'all.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in dedup:
            w.writerow({k: r.get(k, '') for k in fields})
    for k in sorted(counts):
        print('%-22s %5d' % (k, counts[k]))
    print('%-22s %5d (dedup)' % ('TOTAL', len(dedup)))
    hosts = {r.get('host') for r in dedup if r.get('host')}
    print('%-22s %5d' % ('UNIQUE HOSTS', len(hosts)))


if __name__ == '__main__':
    main()
