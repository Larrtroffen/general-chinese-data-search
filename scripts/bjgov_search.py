#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""首都之窗统一搜索（北京市政府门户站内检索 JSON 接口）—— 抓取政策文件/新闻/问答。

原理：区级门户（如朝阳 bjchy.gov.cn）的「政策文件检索」表单实际提交到首都之窗统一搜索；
其前端搜索页 https://www.beijing.gov.cn/so/s 调用本脚本所用 JSON 接口。

接口：
  POST https://www.beijing.gov.cn/so/ss/query/s
  body: qt=<关键词>&page=N&pageSize=M&siteCode=<站点码>
  响应 JSON: {ok, totalHits, resultDocs:[{data:{title,url,docDate,summary,siteLabel,dbName,fileType},...}]}
  示例字段：resultDocs[].data.url / title / docDate / summary / dbName

限制（实测）：
  - siteCode 会被后端忽略为“全站聚合”时需按 URL 域名自行过滤（用 --filter）。
  - 多词 qt 可能 0 结果，优先单关键词（多词拆开分别检索）。
  - 同源接口 api.so-gov.cn/query/s 对批量/高频请求会封出口 IP（code -101）；本脚本默认走
    www.beijing.gov.cn，且请保持低频、单关键词，不要轮询 siteCode。

用法：
  ./bjgov_search.py 吹哨报到                          # 打印前 20 条
  ./bjgov_search.py 吹哨报到 --page 2 --page-size 40
  ./bjgov_search.py 吹哨报到 --filter bjchy.gov.cn --out hits.jsonl
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import urllib.parse

DEFAULT_ENDPOINT = 'https://www.beijing.gov.cn/so/ss/query/s'
DEFAULT_SITE = '1100000088'  # 首都之窗站码（取 /so/s 页隐藏域实测值）


def post_search(endpoint, qt, page, page_size, site_code, timeout=25):
    body = urllib.parse.urlencode({'qt': qt, 'page': page, 'pageSize': page_size, 'siteCode': site_code})
    cmd = ['curl', '-s', '-m', str(timeout), '-X', 'POST', endpoint,
           '-H', 'Referer: https://www.beijing.gov.cn/so/s', '--data', body]
    p = subprocess.run(cmd, capture_output=True)
    txt = p.stdout.decode('utf-8', 'ignore')
    try:
        return json.loads(txt)
    except Exception:
        return {'ok': False, 'msg': 'non-json response: ' + txt[:200]}


def rows_from(resp, host_filter=None):
    out = []
    for doc in resp.get('resultDocs') or []:
        d = doc.get('data') or {}
        url = d.get('url') or ''
        if host_filter and host_filter not in url:
            continue
        out.append({
            'title': (d.get('title') or '').replace('<em>', '').replace('</em>', ''),
            'url': url,
            'date': d.get('docDate') or '',
            'site': (d.get('siteLabel') or {}).get('value', '') if isinstance(d.get('siteLabel'), dict) else '',
            'db': d.get('dbName') or '',
            'summary': (d.get('summary') or '')[:200],
        })
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('qt', help='关键词（建议单关键词）')
    ap.add_argument('--page', type=int, default=1)
    ap.add_argument('--page-size', type=int, default=20)
    ap.add_argument('--site-code', default=DEFAULT_SITE)
    ap.add_argument('--endpoint', default=DEFAULT_ENDPOINT)
    ap.add_argument('--filter', help='仅保留 url 含该子串的结果（如 bjchy.gov.cn）')
    ap.add_argument('--out', help='结果写 JSONL')
    ap.add_argument('--timeout', type=int, default=25)
    args = ap.parse_args()

    resp = post_search(args.endpoint, args.qt, args.page, args.page_size, args.site_code, args.timeout)
    if not resp.get('ok'):
        print('ERROR: %s' % resp.get('msg'), file=sys.stderr)
        return 1
    rows = rows_from(resp, args.filter)
    print('totalHits=%s currentHits=%s rows=%d' % (resp.get('totalHits'), resp.get('currentHits'), len(rows)))
    for r in rows:
        print('%s  %s' % (r['date'], r['title'][:60]))
        print('    ' + r['url'])
    if args.out:
        with open(args.out, 'w', encoding='utf-8') as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + '\n')
        print('saved -> %s' % args.out, file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
