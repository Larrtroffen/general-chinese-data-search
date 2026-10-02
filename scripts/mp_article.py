#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""微信文章正文抓取（mp.weixin.qq.com /s 链接 → Markdown + JSON）。

适用：搜狗 /link 解析出的签名链接（src=11&timestamp=…&signature=…，有效期分钟级），
也适用于永久链接（__biz=…&mid=…&idx=…&sn=…）。

用法：
  ./mp_article.py fetch 'https://mp.weixin.qq.com/s?src=11&timestamp=…' [--out-dir articles]
  ./mp_article.py batch --in crawl.jsonl --out-dir articles [--limit 50]
        # 从 sogou_wechat.py 的 item 记录中取 link 字段逐篇抓

产出：articles/<date>_<slug>.md（front matter: title/account/date/url/msg_link）+ 同名 .json。
状态：ok / deleted（已删除）/ blocked（风控页）/ error。

注意：签名链接有时效，必须拿到后立刻抓；批量时保持 ≥1s 间隔。
"""
from __future__ import annotations

import argparse
import html as htmllib
import json
import os
import re
import subprocess
import sys
import time

UA_IPHONE = ('Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) '
             'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1')

DELETED = ['该内容已被发布者删除', '内容已被发布者删除', '该内容已被删除',
           '此内容因违规无法查看', '此内容发送失败无法查看', '该公众号已迁移']


def curl(url, timeout=25):
    cmd = ['curl', '-s', '-m', str(timeout), '-A', UA_IPHONE, '-H', 'Referer: https://weixin.sogou.com/', url]
    p = subprocess.run(cmd, capture_output=True)
    return p.stdout.decode('utf-8', 'ignore')


def jsv(page, name):
    """取 var NAME = ...; 的值；兼容 JS 字符串拼接（"a" || "b" || ""）。"""
    m = re.search(r'(?:^|[;\s])var %s = ([^\n]*)' % re.escape(name), page, re.M)
    if not m:
        return ''
    rhs = m.group(1).strip()
    if rhs.endswith(';'):
        rhs = rhs[:-1]
    parts = re.findall(r'"((?:[^"\\]|\\.)*)"', rhs)
    if not parts:
        return ''
    val = ''.join(parts)
    return htmllib.unescape(val.replace('\\"', '"').replace("\\'", "'"))


def html_to_text(frag):
    frag = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', '', frag)
    frag = re.sub(r'(?i)<br\s*/?>', '\n', frag)
    frag = re.sub(r'(?i)</(p|section|div|li|h[1-6]|blockquote)>', '\n\n', frag)
    frag = re.sub(r'(?i)<li[^>]*>', '- ', frag)
    txt = re.sub(r'<[^>]+>', '', frag)
    txt = htmllib.unescape(txt)
    txt = re.sub(r'[ \t\u00a0\u200b]+', ' ', txt)
    txt = re.sub(r'\n{3,}', '\n\n', txt)
    return txt.strip()


def parse(page):
    """返回 dict：title/account/date/link/content/images/status/source_url。"""
    out = {'status': 'ok'}
    if any(k in page for k in DELETED) and 'js_content' not in page:
        out['status'] = 'deleted'
    if 'environment' in page[:500] or '请输入验证码' in page[:2000] or '访问过于频繁' in page:
        out['status'] = 'blocked'

    out['title'] = jsv(page, 'msg_title')
    if not out['title']:
        m = re.search(r'(?s)<h1[^>]*id="activity-name"[^>]*>(.*?)</h1>', page)
        if m:
            out['title'] = html_to_text(m.group(1))
    out['account'] = jsv(page, 'nickname')
    if not out['account']:
        m = re.search(r'(?s)<a[^>]*id="js_name"[^>]*>(.*?)</a>', page)
        if m:
            out['account'] = html_to_text(m.group(1))
    ct = jsv(page, 'ct')
    out['date'] = time.strftime('%Y-%m-%d', time.localtime(int(ct))) if ct.isdigit() else ''
    out['msg_link'] = jsv(page, 'msg_link')          # 永久链接（__biz/…）；签名链接页常为空
    out['source_url'] = jsv(page, 'msg_source_url')  # 阅读原文
    # 文章身份三要素（biz, mid, idx）—— 唯一标识，胜过 标题+日期 去重
    for k in ('biz', 'mid', 'idx', 'sn'):
        out[k] = jsv(page, k)
    if not out['msg_link'] and out['biz'] and out['mid'] and out['sn']:
        out['msg_link'] = 'https://mp.weixin.qq.com/s?__biz=%s&mid=%s&idx=%s&sn=%s' % (
            out['biz'], out['mid'], out['idx'] or '1', out['sn'])

    m = re.search(r'(?s)<div[^>]*id="js_content"[^>]*>(.*?)</div>\s*(?:<script|<div[^>]*id="js_sg_bar")', page)
    if not m:
        m = re.search(r'(?s)<div[^>]*id="js_content"[^>]*>(.*?)</div>', page)
    body_raw = m.group(1) if m else ''
    out['content'] = html_to_text(body_raw)
    out['images'] = re.findall(r'data-src="([^"]+)"', body_raw)
    if out['status'] == 'ok' and not out['content']:
        out['status'] = 'error'
    return out


def slugify(s, n=40):
    s = re.sub(r'[\\/:*?"<>|\s]+', '_', s or 'untitled')
    return s[:n].strip('_')


def save(url, rec, out_dir, raw=False):
    os.makedirs(out_dir, exist_ok=True)
    name = '%s_%s' % (rec.get('date') or 'nodedate', slugify(rec.get('title')))
    md_path = os.path.join(out_dir, name + '.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('---\n')
        for k in ('title', 'account', 'date', 'url', 'msg_link', 'source_url', 'status'):
            if rec.get(k):
                f.write('%s: %s\n' % (k, rec[k]))
        f.write('---\n\n')
        f.write(rec.get('content') or '')
        if rec.get('images'):
            f.write('\n\n## 图片\n')
            for u in rec['images']:
                f.write('- %s\n' % u)
    with open(os.path.join(out_dir, name + '.json'), 'w', encoding='utf-8') as f:
        json.dump(rec, f, ensure_ascii=False, indent=1)
    return md_path


def fetch_one(url, args):
    page = curl(url, timeout=args.timeout)
    if not page:
        return {'status': 'error', 'url': url, 'title': '', 'content': ''}
    rec = parse(page)
    rec['url'] = url
    if args.raw:
        os.makedirs(args.out_dir, exist_ok=True)
        rawp = os.path.join(args.out_dir, slugify(url.split('signature=')[-1][:16]) + '.html')
        with open(rawp, 'w', encoding='utf-8') as f:
            f.write(page)
    return rec


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)

    f = sub.add_parser('fetch')
    f.add_argument('url')
    f.add_argument('--out-dir', default='articles')
    f.add_argument('--timeout', type=int, default=25)
    f.add_argument('--raw', action='store_true')
    f.add_argument('--json', action='store_true', help='结果打到 stdout（JSON）')

    b = sub.add_parser('batch')
    b.add_argument('--in', dest='inp', required=True, help='JSONL：含 link 字段（sogou_wechat.py 输出）')
    b.add_argument('--out-dir', default='articles')
    b.add_argument('--limit', type=int, default=0)
    b.add_argument('--gap', type=float, default=1.2)
    b.add_argument('--timeout', type=int, default=25)
    b.add_argument('--raw', action='store_true')

    args = ap.parse_args()
    if args.cmd == 'fetch':
        rec = fetch_one(args.url, args)
        if args.json:
            print(json.dumps(rec, ensure_ascii=False))
        else:
            p = save(args.url, rec, args.out_dir)
            print('%s -> %s (%d chars)' % (rec['status'], p, len(rec.get('content') or '')), file=sys.stderr)
        return 0 if rec['status'] == 'ok' else 1

    todo = []
    seen = set()
    with open(args.inp, encoding='utf-8') as fh:
        for line in fh:
            try:
                d = json.loads(line)
            except Exception:
                continue
            link = d.get('link')
            if not link or link in seen:
                continue
            seen.add(link)
            todo.append(link)
    if args.limit:
        todo = todo[:args.limit]
    print('todo=%d' % len(todo), flush=True)
    ok = bad = 0
    for i, url in enumerate(todo, 1):
        rec = fetch_one(url, args)
        rec['url'] = url
        if rec['status'] == 'ok':
            save(url, rec, args.out_dir)
            ok += 1
        else:
            bad += 1
            print('  [%s] %s' % (rec['status'], url[:110]), flush=True)
        if i % 10 == 0 or i == len(todo):
            print('  %d/%d ok=%d bad=%d' % (i, len(todo), ok, bad), flush=True)
        time.sleep(args.gap)
    print('DONE ok=%d bad=%d' % (ok, bad), flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
