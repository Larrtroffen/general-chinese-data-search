#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""registry_stats —— 统计 registry/ 现状：总行数、唯一主机、各表计数、状态分布。

用法：
  python3 scripts/registry_stats.py            # 打印
  python3 scripts/registry_stats.py --write    # 同时写 registry/STATS.md
"""
from __future__ import annotations

import argparse
import collections
import csv
import glob
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = os.path.join(ROOT, 'registry')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()

    rows_all = []
    per_file = {}
    for path in sorted(glob.glob(os.path.join(REG, '*.csv'))):
        name = os.path.basename(path)
        if name == 'all.csv':
            continue
        with open(path, newline='', encoding='utf-8') as f:
            rows = list(csv.DictReader(f))
        per_file[name] = len(rows)
        rows_all.extend(rows)

    seen = set()
    dedup = []
    for r in rows_all:
        k = (r.get('tier'), r.get('url'))
        if k in seen:
            continue
        seen.add(k)
        dedup.append(r)

    hosts = {r.get('host') for r in dedup if r.get('host')}
    status = collections.Counter((r.get('status') or 'unknown') for r in dedup)
    # 归一化状态：probed-2xx / probed-3xx / probed-4xx / probed-5xx / probed-000 / unprobed / declared
    norm = collections.Counter()
    for r in dedup:
        s = (r.get('status') or '').strip()
        if s.startswith('probed-'):
            code = r.get('http_code') or '000'
            norm['probed-' + (code[:1] + 'xx' if code[:1] in '12345' else '000')] += 1
        elif s:
            norm[s] += 1
        else:
            norm['unknown'] += 1
    tiers = collections.Counter((r.get('tier') or '?') for r in dedup)

    lines = []
    lines.append('# registry STATS —— 源注册表统计（自动生成）')
    lines.append('')
    lines.append('- 数据行（去重后）：**%d**' % len(dedup))
    lines.append('- 唯一主机：**%d**' % len(hosts))
    lines.append('- 分表：')
    for k in sorted(per_file):
        lines.append('  - `%s`：%d 行' % (k, per_file[k]))
    lines.append('')
    lines.append('## 状态分布（去重后）')
    for k, v in norm.most_common():
        lines.append('- %s：%d' % (k, v))
    lines.append('')
    lines.append('## 各层计数（去重后）')
    for k, v in tiers.most_common():
        lines.append('- %s：%d' % (k, v))
    out = '\n'.join(lines) + '\n'
    print(out)
    if args.write:
        with open(os.path.join(REG, 'STATS.md'), 'w', encoding='utf-8') as f:
            f.write(out)
        print('written registry/STATS.md')


if __name__ == '__main__':
    main()
