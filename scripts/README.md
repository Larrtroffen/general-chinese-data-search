# scripts —— 可复用操作脚本

全部脚本：**只用 Python 标准库 + 系统 `curl`**（本机 python3 无 requests/bs4/lxml），
`python3 scripts/<x>.py --help` 即用，无需安装依赖。默认写入当前工作目录下的相对路径。

| 脚本 | 用途 | 典型场景 |
|---|---|---|
| `sogou_wechat.py` | 搜狗微信 wap 检索＋`/link` **现取现解析**（断点续跑、分片） | 按单位/年份批量检索公众号文章，产出链接 |
| `mp_article.py` | 微信文章正文抓取（签名链接→Markdown/JSON） | 把解析出的链接落成可读语料 |
| `bjgov_search.py` | 首都之窗统一搜索 JSON 接口（区政府门户检索的实际后端） | 北京市/区政府站内检索，抓政策/新闻/问答 |
| `site_crawl.py` | 站内 BFS 爬取（分页穷尽、主机限速、robots、断点） | 政府网站全站语料（任免/领导之窗/年报） |
| `fetch.py` | 单请求抓取/探活（UA 预设、cookie jar、重试） | 手工取页面、复现文档里的 curl |
| `probe.py` | 批量 URL 探活（并发） | 维护源 list 时的可达性体检 |
| `registry_extract.py` | 从 `references/` 卡片抽 URL → `registry/*.csv` | 卡片反哺源表 |
| `registry_probe.py` | 批量探活 `registry/*.csv` 并回填状态（同主机去重、跳过 github） | 源表状态维护 |
| `registry_merge.py` | 汇总 `registry/*.csv` → `registry/all.csv` | 计数与总表 |
| `registry_consolidate.py` | 把散落 CSV 合并进 `registry/`（按 tier+url 去重） | 多批次枚举合流 |
| `registry_stats.py` | 统计（行数/唯一主机/状态分布）→ 打印或写 `registry/STATS.md` | 验收与汇报 |

## 常用命令

```bash
# 1) 搜狗微信：检索式清单 → 结果 JSONL（命中 2018 的条目即时解析出签名链接）
python3 scripts/sogou_wechat.py search queries.txt --out crawl.jsonl --resolve 2018
python3 scripts/sogou_wechat.py search queries.txt --out crawl.jsonl --shard 1/3 --jar jar1.txt
python3 scripts/sogou_wechat.py resolve --in crawl.jsonl --out relinks.jsonl   # 补解失败链接

# 2) 微信正文（拿到签名链接后立刻抓，链接约 8 分钟过期）
python3 scripts/mp_article.py fetch 'https://mp.weixin.qq.com/s?src=11&timestamp=…' --out-dir articles
python3 scripts/mp_article.py batch --in crawl.jsonl --out-dir articles --limit 50

# 3) 首都之窗统一搜索
python3 scripts/bjgov_search.py 吹哨报到 --page-size 20 --out hits.jsonl
python3 scripts/bjgov_search.py 任免 --filter bjchy.gov.cn

# 4) 站内爬取（先小 budget 试跑，再放大）
python3 scripts/site_crawl.py --host www.bjdx.gov.cn --budget 20 --delay 0.7
python3 scripts/site_crawl.py --host www.bjchy.gov.cn --seeds http://www.bjchy.gov.cn/affair/file/qzffile/ --budget 100

# 5) 探活
python3 scripts/probe.py urls.txt --out status.csv --workers 4
```

## 约定

- **JSONL 断点**：`sogou_wechat.py` 以 `{"_kind":"query_done","query":…}` 标记完成；`site_crawl.py` 以
  `<host>.jsonl` 中已爬 URL 为断点。中途被杀（任务超时）可直接重跑。
- **并发/分片**：搜狗按 `--shard i/n` 拆检索式，每分片独立 cookie jar；站点爬取按主机分文件，避免多进程写同一文件撕裂。
- **礼貌**：搜狗批量 0.6–1.8s/请求、3–4 分片实测数千请求无反爬；政府站 `site_crawl.py` 默认 0.7s、单进程。
  TLS 有问题的政府站默认 `curl -k`（`--strict-tls` 关闭）。

## 输出约定（便于跨脚本串联）

- 搜狗 item：`{_kind,date,title,account,query,page,href,link,status}`；`status ∈ ok/nofind/antispider/page_fail/skipped`。
- 微信正文：`.md`（front matter: title/account/date/url/msg_link/status）+ `.json`（含 `biz/mid/idx/sn` 唯一标识与 `images`）。
- 站爬清单：`{url,path,status,ctype,title,depth,n_links}`；正文按 `sha1(url)[:16]` 命名落 `raw/`。
