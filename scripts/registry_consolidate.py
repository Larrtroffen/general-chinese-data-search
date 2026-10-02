#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""registry_consolidate —— 把散落在其他目录的 registry CSV 合并进本仓库 registry/（按 tier+url 去重）。

用法：
  python3 scripts/registry_consolidate.py <外部目录> [<外部目录> ...]

规则：
- 只读外部目录里的 *.csv（表头须含 id,tier,url…字段）；
- 按 (tier, url) 去重合并进 registry/<同名文件>；已存在的行保留（本仓库优先）；
- 不删除外部文件（清理由调用方决定）。
"""
from __future__ import annotations

import csv
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = os.path.join(ROOT, 'registry')
FIELDS = ['id', 'tier', 'name', 'url', 'host', 'status', 'http_code', 'probe_date', 'note', 'ref']


def load(path):
    if not os.path.exists(path):
        return []
    with open(path, newline='', encoding='utf-8') as f:
        try:
            return list(csv.DictReader(f))
        except Exception:
            return []


def main():
    dirs = sys.argv[1:]
    if not dirs:
        print('usage: registry_consolidate.py <dir> [...]')
        return
    added_total = 0
    for d in dirs:
        for name in sorted(os.listdir(d)):
            if not name.endswith('.csv') or name == 'all.csv':
                continue
            src = os.path.join(d, name)
            dst = os.path.join(REG, name)
            srows = load(src)
            if not srows or 'url' not in (srows[0] or {}):
                continue
            drows = load(dst)
            seen = {(r.get('tier'), r.get('url')) for r in drows}
            ids = {r.get('id') for r in drows}
            added = 0
            for r in srows:
                key = (r.get('tier'), r.get('url'))
                if key in seen:
                    continue
                rid = r.get('id') or ''
                if rid in ids:
                    rid = rid + '~c%d' % added
                    r['id'] = rid
                seen.add(key)
                ids.add(rid)
                drows.append({k: r.get(k, '') for k in FIELDS})
                added += 1
            if added or not os.path.exists(dst):
                with open(dst, 'w', newline='', encoding='utf-8') as f:
                    w = csv.DictWriter(f, fieldnames=FIELDS)
                    w.writeheader()
                    w.writerows(sorted(drows, key=lambda x: (x.get('id') or '', x.get('url') or '')))
            print('%-40s +%d (total %d)' % (name, added, len(drows)))
            added_total += added
    print('TOTAL ADDED %d' % added_total)


if __name__ == '__main__':
    main()
