#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""registry_probe —— 对 registry/*.csv 中的行做批量探活，回填 status/http_code/probe_date。

- 每主机 1 次请求（`curl -o /dev/null -w '%{http_code}'`），并发默认 8，超时默认 12s；
- 默认只探 `unprobed` 或 probe_date 超过 N 天的行（--stale-days，默认 90）；
- 支持 --limit 控制本轮总量；--tier 限定层。

用法：
  python3 scripts/registry_probe.py --workers 8 --limit 500
  python3 scripts/registry_probe.py --tier gov --stale-days 0   # 强制全量重测 gov
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import glob
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = os.path.join(ROOT, 'registry')
UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')


def probe(url: str, timeout: int):
    cmd = ['curl', '-s', '-k', '-L', '--max-redirs', '3', '-o', '/dev/null',
           '-m', str(timeout), '-A', UA, '-w', '%{http_code}', url]
    try:
        p = subprocess.run(cmd, capture_output=True, timeout=timeout + 8)
        code = p.stdout.decode('utf-8', 'ignore').strip() or '000'
        return code
    except Exception:
        return '000'


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--tier', default='')
    ap.add_argument('--workers', type=int, default=8)
    ap.add_argument('--timeout', type=int, default=12)
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--stale-days', type=int, default=90)
    ap.add_argument('--include-github', action='store_true',
                    help='默认跳过 host=github.com 的行（爬虫仓索引，避免对 GitHub 打上千请求）')
    args = ap.parse_args()

    today = dt.date.today().isoformat()
    cutoff = (dt.date.today() - dt.timedelta(days=args.stale_days)).isoformat()
    files = sorted(glob.glob(os.path.join(REG, '*.csv')))
    if args.tier:
        files = [f for f in files if os.path.basename(f).startswith(args.tier + '.')]

    total_probed = 0
    host_cache = {}
    for path in files:
        with open(path, newline='', encoding='utf-8') as f:
            rows = list(csv.DictReader(f))
        if not rows:
            continue
        targets = []
        for r in rows:
            if r.get('host', '') == 'github.com' and not args.include_github:
                continue
            if r.get('status', '').startswith('probed') and (r.get('probe_date') or '') >= cutoff:
                continue
            targets.append(r)
        if args.limit and total_probed + len(targets) > args.limit:
            targets = targets[:max(0, args.limit - total_probed)]
        if not targets:
            continue
        # 同主机只探一次（媒体/机构表存在同主机多行）
        uniq = {}
        for r in targets:
            uniq.setdefault(r.get('host') or r['url'], r['url'])
        print('%s: %d rows / %d hosts' % (os.path.basename(path), len(targets), len(uniq)), flush=True)
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = {ex.submit(probe, u, args.timeout): h for h, u in uniq.items()}
            for fut in as_completed(futs):
                h = futs[fut]
                code = fut.result()
                host_cache[h] = code
        for r in targets:
            h = r.get('host') or r['url']
            code = host_cache.get(h, '000')
            r['http_code'] = code
            r['probe_date'] = today
            r['status'] = 'probed-000' if code == '000' else ('probed-%sxx' % code[0] if code[:1] in '12345' else 'probed-' + code)
        fields = list(rows[0].keys())
        with open(path, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
        total_probed += len(targets)
        print('  done. total=%d' % total_probed, flush=True)
    print('PROBED %d rows' % total_probed)


if __name__ == '__main__':
    main()
