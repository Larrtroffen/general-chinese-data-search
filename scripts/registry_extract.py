#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""registry_extract —— 从 references/ 各来源卡抽取 URL，生成/刷新 registry/<tier>.csv。

规则：
- 每个卡文件 → 一行或多行（URL 去重后；每行 = 一个源）。
- tier 取卡文件所在的层名（references/<tier>/…）；id = "<tier>:<host>"，同主机多 URL 取第一个为主、其余加路径摘要。
- 只填 name/url/host/status=unprobed/note/ref；已存在且 ref 相同的行不重复生成（幂等）。
- 不覆盖 registry/crawlers.csv 等“手写表”；只维护以 ref 指向卡片的行。

用法：
  python3 scripts/registry_extract.py            # 全部层
  python3 scripts/registry_extract.py gov stats  # 指定层
"""
from __future__ import annotations

import csv
import glob
import os
import re
import sys
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, 'references')
REG = os.path.join(ROOT, 'registry')

URL_RE = re.compile(r'https?://[^\s<>"`\)\]]+')
SKIP_HOSTS = {
    'github.com', 'raw.githubusercontent.com', 'githubusercontent.com', 'gitee.com',
    'api.github.com', 'docs.github.com', 'zenodo.org', 'dataverse.harvard.edu',
    'huggingface.co', 'hf-mirror.com', 'pypi.org', 'npmjs.com', 'npmjs.org',
    'doi.org', 'img.shields.io', 'creativecommons.org', 'opensource.org',
}
FIELDS = ['id', 'tier', 'name', 'url', 'host', 'status', 'http_code', 'probe_date', 'note', 'ref']


def clean_url(u: str) -> str:
    u = u.rstrip('.,;:、。，；：」』】）)]')
    u = u.replace('&amp;', '&')
    return u


def load(path):
    rows = []
    if os.path.exists(path):
        with open(path, newline='', encoding='utf-8') as f:
            rows = list(csv.DictReader(f))
    return rows


def main():
    want = set(sys.argv[1:])
    os.makedirs(REG, exist_ok=True)
    tiers = sorted(d for d in os.listdir(REF) if os.path.isdir(os.path.join(REF, d)))
    report = []
    for tier in tiers:
        if want and tier not in want:
            continue
        csv_path = os.path.join(REG, tier + '.csv')
        rows = load(csv_path)
        seen = {(r['id'], r['url']) for r in rows}
        added = 0
        for md in sorted(glob.glob(os.path.join(REF, tier, '**', '*.md'), recursive=True)):
            if os.path.basename(md) == 'README.md':
                continue
            rel = os.path.relpath(md, ROOT)
            txt = open(md, encoding='utf-8').read()
            title = re.search(r'^# (.+)$', txt, re.M)
            name = (title.group(1).split(' —— ')[0].strip() if title else os.path.basename(md))
            urls = []
            for m in URL_RE.finditer(txt):
                u = clean_url(m.group(0).split('#')[0])
                if u not in urls:
                    urls.append(u)
            for i, u in enumerate(urls):
                host = urlparse(u).netloc.split(':')[0].lower()
                if host in SKIP_HOSTS or host.endswith(tuple('.' + h for h in SKIP_HOSTS)):
                    continue
                rid = '%s:%s' % (tier, host)
                if i > 0:
                    rid += '~%d' % i
                if (rid, u) in seen:
                    continue
                seen.add((rid, u))
                rows.append({
                    'id': rid, 'tier': tier, 'name': name, 'url': u, 'host': host,
                    'status': 'unprobed', 'http_code': '', 'probe_date': '',
                    'note': '卡片抽取', 'ref': rel,
                })
                added += 1
        # 按 id 排序后写回
        rows.sort(key=lambda r: (r['id'], r['url']))
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            w.writeheader()
            w.writerows(rows)
        report.append((tier, len(rows), added))
    print('tier                total  added')
    total = 0
    for tier, n, a in report:
        print('%-20s %5d %6d' % (tier, n, a))
        total += n
    print('%-20s %5d' % ('TOTAL', total))


if __name__ == '__main__':
    main()
