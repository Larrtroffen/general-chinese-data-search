#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""通用抓取助手：curl 封装（UA 预设 / cookie jar / 重试 / 状态码探测）。

只用标准库 + 系统 curl（本机 python3 无 requests）。

用法：
  fetch.py URL                          # 抓正文到 stdout
  fetch.py URL --out page.html          # 存文件（自动建父目录）
  fetch.py URL --probe                  # 只打印状态行: code size time url
  fetch.py URL --jar jar.txt            # 带 cookie jar（-b/-c）
  fetch.py URL --referer REF            # 带 Referer
  fetch.py URL --ua iphone|desktop|none # UA 预设（默认 desktop）
  fetch.py URL --retry 3                # 非 2xx 或超时重试（指数退避）
  fetch.py URL -H 'X-Foo: bar'          # 附加请求头（可多次）

退出码：0 成功；1 curl 失败或重试后仍非 2xx；2 参数错误。
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time

UA_IPHONE = ('Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) '
             'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1')
UA_DESKTOP = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
UA_NONE = ''

PRESETS = {'iphone': UA_IPHONE, 'desktop': UA_DESKTOP, 'none': UA_NONE}


def build_cmd(url, args):
    """返回 (cmd, tmp_out) —— tmp_out 为 None 表示 body 走 stdout。"""
    cmd = ['curl', '-s', '--compressed', '-m', str(args.timeout), '-L', '--max-redirs', '5']
    ua = PRESETS[args.ua]
    if ua:
        cmd += ['-A', ua]
    if args.jar:
        cmd += ['-b', args.jar, '-c', args.jar]
    if args.referer:
        cmd += ['-H', 'Referer: ' + args.referer]
    for h in args.header or []:
        cmd += ['-H', h]
    if args.probe:
        fmt = '%{http_code} %{size_download} %{time_total} %{content_type}'
        cmd += ['-o', '/dev/null', '-w', fmt]
    cmd += [url]
    return cmd


def run_once(cmd, url):
    p = subprocess.run(cmd, capture_output=True)
    out = p.stdout.decode('utf-8', 'ignore')
    if cmd[0] == 'curl' and '-w' in cmd and cmd[-1] == url:
        # probe 模式：stdout 即状态行
        return p.returncode, out.strip()
    return p.returncode, out


def probe_result(cmd, url):
    p = subprocess.run(cmd, capture_output=True)
    line = p.stdout.decode('utf-8', 'ignore').strip()
    code = line.split(' ', 1)[0] if line else '000'
    return code, line


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('url')
    ap.add_argument('--out')
    ap.add_argument('--probe', action='store_true', help='只打印: code size time content_type url')
    ap.add_argument('--jar')
    ap.add_argument('--referer')
    ap.add_argument('--ua', choices=['iphone', 'desktop', 'none'], default='desktop')
    ap.add_argument('--timeout', type=int, default=25)
    ap.add_argument('--retry', type=int, default=2, help='总尝试次数（默认 2）')
    ap.add_argument('-H', '--header', action='append')
    args = ap.parse_args()

    ok_probe = None
    for attempt in range(max(1, args.retry)):
        cmd = build_cmd(args.url, args)
        if args.probe:
            code, line = probe_result(cmd, args.url)
            ok_probe = line
            if code.startswith('2') or code.startswith('3'):
                print(line, args.url)
                return 0
        else:
            rc, out = run_once(cmd, args.url)
            if rc == 0 and out:
                if args.out:
                    d = os.path.dirname(os.path.abspath(args.out))
                    os.makedirs(d, exist_ok=True)
                    with open(args.out, 'w', encoding='utf-8') as f:
                        f.write(out)
                    print(f'saved {len(out)} chars -> {args.out}', file=sys.stderr)
                else:
                    sys.stdout.write(out)
                return 0
        if attempt < max(1, args.retry) - 1:
            time.sleep(2 * (attempt + 1))
    if ok_probe is not None:
        print(ok_probe, args.url)
        return 1
    print(f'FAILED: {args.url}', file=sys.stderr)
    return 1


if __name__ == '__main__':
    sys.exit(main())
