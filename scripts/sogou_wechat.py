#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""搜狗微信检索 + 现取现解析（stdlib + curl，可断点续跑）。

搜狗结果页里的 /link?url=… token 时效极短（分钟级），必须在抓到搜索页后**立即**解析。
本脚本的 search 子命令在翻页过程中对命中条目直接解析，产出 mp.weixin.qq.com 签名链接。

子命令：
  search   按检索式清单翻页抓取；对目标年份/dd 条目立即解析链接
  resolve  对已存结果 JSONL 中缺 link 的条目重解析（跨页/标题回查）

用法：
  ./sogou_wechat.py search queries.txt --out crawl.jsonl --resolve 2018
  ./sogou_wechat.py search queries.txt --out crawl.jsonl --shard 0/3 --resolve all
  ./sogou_wechat.py resolve --in crawl.jsonl --out relinks.jsonl

检索式文件：每行一条（UTF-8）。断点：JSONL 中 `{"_kind":"query_done","query":…}` 标记已完成的检索式。

输出记录：
  {"_kind":"item","date":"2018-06-01","title":…,"account":…,"query":…,"page":N,
   "href":"/link?url=…","link":"https://mp.weixin.qq.com/s?…","status":"ok|nofind|antispider|page_fail"}
  {"_kind":"query_done","query":…}
"""
from __future__ import annotations

import argparse
import html
import json
import os
import random
import re
import subprocess
import sys
import time
import urllib.parse

UA_IPHONE = ('Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) '
             'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1')
SEARCH = 'https://weixin.sogou.com/weixinwap'
HOMEPAGE = 'https://weixin.sogou.com/'
WARM_QUERY = '北京 街乡吹哨 部门报到'


def curl(url, jar, referer=None, timeout=30):
    cmd = ['curl', '-s', '-i', '-m', str(timeout), '-A', UA_IPHONE, '-b', jar, '-c', jar]
    if referer:
        cmd += ['-H', 'Referer: ' + referer]
    cmd += [url]
    p = subprocess.run(cmd, capture_output=True)
    return p.stdout.decode('utf-8', 'ignore')


def search_url(query, page=1):
    u = SEARCH + '?type=2&ie=utf8&query=' + urllib.parse.quote(query)
    if page > 1:
        u += '&page=%d' % page
    return u


def parse_items(body):
    """解析结果页 <li id="sogou_vr_*">：href/title/account/date。"""
    out = []
    i = body.find('<div class="results"')
    if i < 0:
        return out
    for li in re.findall(r'<li id="sogou_vr_\d+_box_\d+".*?</li>', body[i:], re.S):
        m = re.search(r'<h4>\s*<a href="([^"]+)"[^>]*>\s*<div>(.*?)</div>', li, re.S)
        if not m:
            continue
        href = html.unescape(m.group(1))
        title = html.unescape(re.sub(r'<[^>]+>', '', m.group(2))).strip()
        am = re.search(r'data-sourcename="([^"]*)"', li)
        account = html.unescape(am.group(1)) if am else ''
        dm = re.search(r'data-lastModified="(\d+)"', li)
        date = time.strftime('%Y-%m-%d', time.localtime(int(dm.group(1)))) if dm else ''
        out.append({'href': href, 'title': title, 'account': account, 'date': date})
    return out


def extract_link(resp):
    """从 /link 返回页的逐段 JS 拼接出 mp.weixin.qq.com 签名链接。"""
    frags = re.findall(r"url \+= '([^']*)';", resp)
    if not frags:
        return None
    target = ''.join(frags)
    return target if target.startswith('https://mp.weixin.qq.com') else None


def reset_jar(jar):
    if os.path.exists(jar):
        os.remove(jar)


def warm(jar):
    reset_jar(jar)
    curl(search_url(WARM_QUERY), jar, referer=HOMEPAGE)


def fetch_page(query, page, jar, retry=3, verbose=True):
    """抓一页；空页/无结果返回 []；被反爬重试耗尽返回 None。"""
    for k in range(retry):
        r = curl(search_url(query, page), jar, referer=HOMEPAGE)
        body = r.split('\r\n\r\n', 1)[-1]
        if 'antispider' not in r[:1500] and ('sogou_vr_' in body or '没有找到相关的微信文章' in body):
            return parse_items(body)
        wait = 45 + 30 * k
        if verbose:
            print('  [page blocked] %s p%d, wait %ds' % (query, page, wait), flush=True)
        time.sleep(wait)
        warm(jar)
    return None


def resolve(href, query, page, jar):
    """解析单条 href → (link, status)。status ∈ ok/nofind/antispider。"""
    url = 'https://weixin.sogou.com' + html.unescape(href).replace(' ', '%20')
    r = curl(url, jar, referer=search_url(query, page))
    head, _, b = r.partition('\r\n\r\n')
    if 'antispider' in head or 'antispider' in b[:2000]:
        return None, 'antispider'
    link = extract_link(b)
    return (link, 'ok') if link else (None, 'nofind')


def find_href(query, title, jar):
    """条目索引漂移时跨页/按标题回查 href。返回 (href, page) 或 (None, None)。"""
    for pg in (1, 2, 3):
        items = fetch_page(query, pg, jar, verbose=False)
        if not items:
            continue
        for it in items:
            if it['title'] == title or it['title'][:14] == title[:14]:
                return it['href'], pg
    q2 = title[:30]
    for pg in (1, 2):
        items = fetch_page(q2, pg, jar, verbose=False)
        if not items:
            continue
        for it in items:
            if it['title'] == title or it['title'][:12] == title[:12]:
                return it['href'], pg
    return None, None


def load_queries(path):
    with open(path, encoding='utf-8') as f:
        return [ln.strip() for ln in f if ln.strip() and not ln.startswith('#')]


def load_done(path):
    done = set()
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            for line in f:
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                if d.get('_kind') == 'query_done':
                    done.add(d['query'])
    return done


def cmd_search(args):
    queries = load_queries(args.queries)
    if args.shard:
        i, n = (int(x) for x in args.shard.split('/'))
        queries = [q for k, q in enumerate(queries) if k % n == i]
    done = load_done(args.out)
    todo = [q for q in queries if q not in done]
    print('queries=%d done=%d todo=%d shard=%s' % (len(queries), len(done), len(todo), args.shard or '-'), flush=True)
    jar = args.jar or 'sogou_jar.txt'
    with open(args.out, 'a', encoding='utf-8') as f:
        n_items = n_hit = n_links = 0
        for qi, q in enumerate(todo, 1):
            seen = set()
            for page in range(1, args.pages + 1):
                items = fetch_page(q, page, jar, verbose=args.verbose)
                if items is None:
                    break
                if not items:
                    break  # 空页=翻到底
                new = [it for it in items if (it['title'], it['date']) not in seen]
                if not new:
                    break  # 整页重复=翻到底
                for it in new:
                    seen.add((it['title'], it['date']))
                    n_items += 1
                    hit = args.resolve == 'all' or (args.resolve == '2018' and it['date'].startswith('2018'))
                    link, st = ('', 'skipped')
                    if hit:
                        n_hit += 1
                        link, st = resolve(it['href'], q, page, jar)
                        if link:
                            n_links += 1
                    rec = {'_kind': 'item', 'date': it['date'], 'title': it['title'], 'account': it['account'],
                           'query': q, 'page': page, 'href': it['href'], 'link': link or '', 'status': st}
                    f.write(json.dumps(rec, ensure_ascii=False) + '\n')
                f.flush()
                if len(new) < 3 and page >= 2:
                    break
                time.sleep(args.gap_min + random.random() * (args.gap_max - args.gap_min))
            f.write(json.dumps({'_kind': 'query_done', 'query': q}, ensure_ascii=False) + '\n')
            f.flush()
            if qi % 10 == 0:
                print('  %d/%d items=%d target=%d links=%d' % (qi, len(todo), n_items, n_hit, n_links), flush=True)
    print('DONE items=%d target=%d links=%d' % (n_items, n_hit, n_links), flush=True)
    return 0


def cmd_resolve(args):
    rows = []
    with open(args.inp, encoding='utf-8') as f:
        for line in f:
            try:
                d = json.loads(line)
            except Exception:
                continue
            if d.get('_kind') == 'item' and not d.get('link'):
                rows.append(d)
    seen = set()
    todo = []
    for d in rows:
        k = (d.get('date'), d.get('title'), d.get('account'))
        if k in seen:
            continue
        seen.add(k)
        todo.append(d)
    print('missing=%d uniq=%d' % (len(rows), len(todo)), flush=True)
    jar = args.jar or 'sogou_jar.txt'
    warm(jar)
    ok = fail = 0
    with open(args.out, 'a', encoding='utf-8') as f:
        for i, d in enumerate(todo, 1):
            q, page = d.get('query', ''), int(d.get('page', 1))
            href = d.get('href')
            items = fetch_page(q, page, jar, verbose=False) if q else None
            if items:
                by_title = {it['title']: it['href'] for it in items}
                href = by_title.get(d['title']) or href
            if not href or args.recheck:
                href2, pg2 = find_href(q, d['title'], jar)
                if href2:
                    href, page = href2, pg2
            link, st = (None, 'nofind')
            if href:
                link, st = resolve(href, q, page, jar)
            rec = {'_kind': 'item', 'date': d.get('date'), 'title': d.get('title'), 'account': d.get('account'),
                   'query': q, 'page': page, 'href': href or '', 'link': link or '', 'status': st}
            f.write(json.dumps(rec, ensure_ascii=False) + '\n')
            f.flush()
            ok += 1 if link else 0
            fail += 0 if link else 1
            if i % 20 == 0:
                print('  %d/%d ok=%d fail=%d' % (i, len(todo), ok, fail), flush=True)
            time.sleep(args.gap_min + random.random() * (args.gap_max - args.gap_min))
    print('DONE ok=%d fail=%d' % (ok, fail), flush=True)
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)

    s = sub.add_parser('search', help='检索式清单 → 结果 JSONL（可选现取现解析）')
    s.add_argument('queries')
    s.add_argument('--out', required=True)
    s.add_argument('--jar', help='cookie jar 文件（默认 sogou_jar.txt；分片时每分片一个）')
    s.add_argument('--shard', help='i/n，例如 0/3；检索式按 i %% n == i 取模')
    s.add_argument('--pages', type=int, default=10, help='每检索式最大翻页数（搜狗上限 10）')
    s.add_argument('--resolve', choices=['none', '2018', 'all'], default='2018')
    s.add_argument('--gap-min', type=float, default=0.6)
    s.add_argument('--gap-max', type=float, default=1.2)
    s.add_argument('--verbose', action='store_true')
    s.set_defaults(func=cmd_search)

    r = sub.add_parser('resolve', help='结果 JSONL 中缺 link 的条目重解析')
    r.add_argument('--in', dest='inp', required=True)
    r.add_argument('--out', required=True)
    r.add_argument('--jar')
    r.add_argument('--recheck', action='store_true', help='即使有 href 也重新按标题回查')
    r.add_argument('--gap-min', type=float, default=0.8)
    r.add_argument('--gap-max', type=float, default=1.6)
    r.set_defaults(func=cmd_resolve)

    args = ap.parse_args()
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
