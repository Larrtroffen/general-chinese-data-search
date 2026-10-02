#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""站内 BFS 爬取（政府网站/机构网站语料收集）—— stdlib + curl，可断点续跑。

源自本机 32k 页政府站爬取实践（多进程分片 + 分页穷尽 + 主机限速）。
要点：
  - 只爬同一主机；每主机一个清单文件 index/<host>.jsonl，避免并发写同一文件撕裂。
  - 分页穷尽：从 list_N/index_N/list-N/裸数字.html 以及 ?page=N 型模板合成后续页（只从 n<=2 的页面展开）。
  - 优先级：任免/领导之窗/公报/公示/公告/年报 等高价值 URL 先爬。
  - TLS：政府站常见自签/证书错配 → 默认 curl -k（--strict-tls 关闭）。
  - robots.txt：默认遵守（Disallow 全站则拒爬）；--ignore-robots 跳过（需自行评估合规）。

用法：
  ./site_crawl.py --host www.bjdx.gov.cn --budget 50 --delay 0.7
  ./site_crawl.py --host www.bjchy.gov.cn --seeds https://www.bjchy.gov.cn/affair/file/qzffile/ --budget 30
  ./site_crawl.py --host www.bjdx.gov.cn --budget 500 --out-dir data/bjdx --index-dir data/bjdx/index

输出：
  <out-dir>/raw/<sha1[:16]>.<ext>      页面正文（html）或文档（pdf/doc/xls…，不解析）
  <index-dir>/<host>.jsonl             {url, path, status, ctype, title, links}
续跑：已爬 URL 从 index 读取跳过。
"""
from __future__ import annotations

import argparse
import hashlib
import heapq
import os
import re
import subprocess
import sys
import time
import urllib.parse
from collections import deque

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')

DOC_EXT = re.compile(r'\.(pdf|docx?|xlsx?|pptx?|rtf|wps|et|zip|rar)$', re.I)
SKIP_EXT = re.compile(r'\.(jpg|jpeg|png|gif|css|js|ico|svg|mp4|mp3|woff2?|ttf|eot)$', re.I)

BOOST = [('任免', 12), ('领导之窗', 12), ('领导', 6), ('公报', 4), ('公示', 4), ('公告', 4),
         ('选举', 6), ('镇长', 3), ('主任', 3), ('年度报告', 4), ('工作报告', 4),
         ('人大', 4), ('名单', 4), ('信息', 1)]
PAGE_QUERY = re.compile(r'[?&](page|p|PageNo|pageNo|pageNum|pageIndex|current|currentPage)', re.I)
PAGINATION = [
    (re.compile(r'list_(\d+)\.html?$', re.I), 40),
    (re.compile(r'list-(\d+)\.html?$', re.I), 30),
    (re.compile(r'index_(\d+)\.html?$', re.I), 30),
    (re.compile(r'/(\d+)\.html?$'), 15),
]


def curl(url, args, timeout=25):
    cmd = ['curl', '-s', '-m', str(timeout), '-L', '--max-redirs', '5', '-A', UA,
           '-w', '\n@@CT:%{http_code}|%{content_type}|%{size_download}']
    if not args.strict_tls:
        cmd += ['-k']
    cmd += [url]
    try:
        p = subprocess.run(cmd, capture_output=True, timeout=timeout + 15)
        raw = p.stdout
        mk = b'\n@@CT:'
        marker = raw.rfind(mk)
        if marker < 0:
            return -1, '', ''
        body = raw[:marker]
        code, ctype, _ = raw[marker + len(mk):].decode('utf-8', 'ignore').split('|')[:3]
        txt = decode_body(body, ctype)
        return int(code), ctype, txt
    except Exception:
        return -1, '', ''


def decode_body(body, ctype):
    m = re.search(rb'charset=["\']?([\w-]+)', body[:4000], re.I)
    cands = []
    if m:
        cands.append(m.group(1).decode('ascii', 'ignore').lower())
    if 'gb' in ctype.lower() or 'gb' in (cands[0] if cands else ''):
        cands += ['gb18030', 'utf-8']
    else:
        cands += ['utf-8', 'gb18030']
    for enc in cands:
        try:
            return body.decode(enc)
        except Exception:
            continue
    return body.decode('utf-8', 'ignore')


def fetch_robots(host, args):
    code, _, txt = curl('https://%s/robots.txt' % host, args, timeout=15)
    if code != 200 or not txt:
        code, _, txt = curl('http://%s/robots.txt' % host, args, timeout=15)
    if code != 200 or not txt:
        return None
    rules, applies = [], False
    for line in txt.splitlines():
        line = line.split('#')[0].strip()
        if not line:
            continue
        k, _, v = line.partition(':')
        k, v = k.strip().lower(), v.strip()
        if k == 'user-agent':
            applies = v in ('*', '')
        elif k == 'disallow' and applies and v:
            rules.append(v)
    return rules


def allowed(url, rules):
    if not rules:
        return True
    path = urllib.parse.urlparse(url).path or '/'
    return not any(path.startswith(r.rstrip('*')) for r in rules)


def score(url, depth):
    s = -depth
    for kw, w in BOOST:
        if kw in urllib.parse.unquote(url):
            s += w
    return s


def norm(url, host):
    """规范化为同主机绝对 http(s) URL；跨主机/非 http 返回 None。"""
    p = urllib.parse.urlparse(url)
    if p.scheme not in ('http', 'https'):
        return None
    if p.netloc.split(':')[0] != host:
        return None
    clean = urllib.parse.urlunparse((p.scheme, p.netloc, p.path or '/', p.params, p.query, ''))
    return clean


def extract_links(page, base, host):
    out = []
    for m in re.finditer(r'(?is)<(?:a|frame|iframe)[^>]+?(?:href|src)\s*=\s*["\']([^"\']+)["\']', page):
        u = urllib.parse.urljoin(base, m.group(1).strip())
        n = norm(u, host)
        if n and not SKIP_EXT.search(n):
            out.append(n)
    # 分页穷尽：静态模板 + 查询参数型
    for pat, cap in PAGINATION:
        mm = pat.search(urllib.parse.urlparse(base).path)
        if mm and int(mm.group(1)) <= 2:
            prefix = base[:mm.start(1)]
            suffix = base[mm.end(1):]
            for i in range(3, cap + 1):
                out.append(prefix + str(i) + suffix)
    if PAGE_QUERY.search(base):
        for i in range(3, 31):
            out.append(PAGE_QUERY.sub(lambda m: m.group(1) + '=' + str(i), base, count=1))
    return out


def load_seen(index_path):
    seen = set()
    if os.path.exists(index_path):
        with open(index_path, encoding='utf-8') as f:
            for line in f:
                try:
                    import json
                    d = json.loads(line)
                    if d.get('url'):
                        seen.add(d['url'])
                except Exception:
                    continue
    return seen


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--host', required=True)
    ap.add_argument('--seeds', default='')
    ap.add_argument('--budget', type=int, default=100, help='本次最多抓取页数')
    ap.add_argument('--delay', type=float, default=0.7)
    ap.add_argument('--depth', type=int, default=6)
    ap.add_argument('--timeout', type=int, default=25)
    ap.add_argument('--out-dir', default='data/raw_sites')
    ap.add_argument('--index-dir', default='data/raw_sites/index')
    ap.add_argument('--strict-tls', action='store_true')
    ap.add_argument('--ignore-robots', action='store_true')
    ap.add_argument('--keep-links', action='store_true', help='清单中记录链接列表（文件更大）')
    args = ap.parse_args()

    import json
    host = args.host
    os.makedirs(os.path.join(args.out_dir, 'raw'), exist_ok=True)
    os.makedirs(args.index_dir, exist_ok=True)
    index_path = os.path.join(args.index_dir, host + '.jsonl')

    rules = fetch_robots(host, args) if not args.ignore_robots else None
    if rules is None and not args.ignore_robots:
        print('robots.txt 不可得，继续（视为无限制）', file=sys.stderr)
    elif rules and not any(allowed(s, rules) for s in
                           ([args.seeds.split(',')[0]] if args.seeds else ['https://%s/' % host])):
        if not args.ignore_robots:
            print('robots.txt 禁止抓取本主机（Disallow 全站）；如确需抓取加 --ignore-robots（自行评估合规）', file=sys.stderr)
            return 2

    seen = load_seen(index_path)
    seeds = [s for s in args.seeds.split(',') if s] or ['https://%s/' % host, 'http://%s/' % host]
    heap, queued = [], set()
    for s in seeds:
        n = norm(s, host) or s
        heapq.heappush(heap, (-1000, 0, n))
        queued.add(n)

    done = 0
    f = open(index_path, 'a', encoding='utf-8')
    while heap and done < args.budget:
        neg, depth, url = heapq.heappop(heap)
        if url in seen or depth > args.depth:
            continue
        seen.add(url)
        code, ctype, page = curl(url, args)
        status = 'ok'
        path = ''
        if code != 200:
            status = 'http_%s' % code
            if code == -1:
                status = 'conn_fail'
                # 协议互换兜底（政府站常见 443 失败）
                alt = url.replace('https://', 'http://', 1) if url.startswith('https://') else url.replace('http://', 'https://', 1)
                code2, ctype2, page2 = curl(alt, args)
                if code2 == 200:
                    url, code, ctype, page, status = alt, code2, ctype2, page2, 'ok_alt_scheme'
        title = re.search(r'(?is)<title[^>]*>(.*?)</title>', page)
        title = re.sub(r'\s+', ' ', title.group(1)).strip()[:80] if title else ''
        is_doc = bool(DOC_EXT.search(urllib.parse.urlparse(url).path)) or 'pdf' in ctype.lower()
        if code == 200 and page:
            ext = '.pdf' if 'pdf' in ctype.lower() else ('.html' if 'html' in ctype.lower() or not is_doc else os.path.splitext(url)[1] or '.bin')
            h = hashlib.sha1(url.encode()).hexdigest()[:16]
            path = os.path.join(args.out_dir, 'raw', h + ext)
            with open(path, 'w', encoding='utf-8') as w:
                w.write(page)
        links = []
        if code == 200 and not is_doc and ('html' in ctype.lower() or '<a ' in page[:200000].lower()):
            links = extract_links(page, url, host)
            for u in links:
                if u not in seen and u not in queued and allowed(u, rules or []):
                    queued.add(u)
                    heapq.heappush(heap, (score(u, depth + 1), depth + 1, u))
        rec = {'url': url, 'path': path, 'status': status, 'ctype': ctype, 'title': title,
               'depth': depth, 'n_links': len(links)}
        if args.keep_links:
            rec['links'] = links
        f.write(json.dumps(rec, ensure_ascii=False) + '\n')
        f.flush()
        done += 1
        print('[%d/%d] %s %s %s' % (done, args.budget, status, title[:40], url[:110]), flush=True)
        time.sleep(args.delay)
    f.close()
    print('DONE pages=%d queued_left=%d index=%s' % (done, len(heap), index_path), flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
