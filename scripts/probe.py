#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量探活：给一批 URL，输出 状态码/大小/耗时 —— 用于维护「源 list」的可达性。

用法：
  ./probe.py urls.txt                       # 每行一个 URL（# 注释）
  ./probe.py urls.txt --out status.csv --workers 4
  ./probe.py urls.txt --ua iphone --timeout 15

输出：CSV: url,http_code,size_bytes,time_s,content_type（同时打印到 stdout）。
"""
from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

UA_IPHONE = ('Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) '
             'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1')
UA_DESKTOP = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
PRESETS = {'iphone': UA_IPHONE, 'desktop': UA_DESKTOP, 'none': ''}


def probe(url, ua, timeout):
    cmd = ['curl', '-s', '-o', '/dev/null', '-m', str(timeout), '-L', '--max-redirs', '5',
           '-w', '%{http_code},%{size_download},%{time_total},%{content_type}']
    if ua:
        cmd += ['-A', ua]
    cmd += [url]
    try:
        p = subprocess.run(cmd, capture_output=True, timeout=timeout + 10)
        parts = p.stdout.decode('utf-8', 'ignore').strip().split(',')
        while len(parts) < 4:
            parts.append('')
        return [url] + parts[:4]
    except Exception as e:
        return [url, '000', '0', '', 'ERR:%s' % type(e).__name__]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('urls')
    ap.add_argument('--out')
    ap.add_argument('--workers', type=int, default=4)
    ap.add_argument('--timeout', type=int, default=15)
    ap.add_argument('--ua', choices=list(PRESETS), default='desktop')
    args = ap.parse_args()

    with open(args.urls, encoding='utf-8') as f:
        urls = [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith('#')]

    rows = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(probe, u, PRESETS[args.ua], args.timeout): u for u in urls}
        for fut in as_completed(futs):
            r = fut.result()
            rows.append(r)
            print(' '.join(r), flush=True)
    rows.sort(key=lambda r: urls.index(r[0]))

    if args.out:
        with open(args.out, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(['url', 'http_code', 'size_bytes', 'time_s', 'content_type'])
            w.writerows(rows)
        print('saved ->', args.out, file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
