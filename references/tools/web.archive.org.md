# web.archive.org —— 网页存档回捞（间歇可达）

用于回捞已下线/改版的 2018 年页面（区报数字报、政府网旧栏目）。本机多次实测结论：**时好时坏**，按不可靠通道处理。

- 去哪找：`https://web.archive.org/` ；快照定位 `https://archive.org/wayback/available?url={url}&timestamp={YYYYMMDD}` ；CDX 批量枚举 `http://web.archive.org/cdx/search/cdx?url={host}&output=json&…`
- 什么时候用：目标页已下线/改版，需要历史快照；枚举某域名的历史抓取清单
- 怎么用：`curl -s -m 20 'https://archive.org/wayback/available?url=bjdx.gov.cn&timestamp=20180601'`（JSON）；CDX `curl -s -m 25 'http://web.archive.org/cdx/search/cdx?url=www.bjdx.gov.cn&output=json&limit=50&fl=timestamp,original,statuscode'`（`&showNumPages=true` 先探规模）。结果形态：JSON / HTML；本机时通时断
- 覆盖：Internet Archive 网页快照；年代依存档情况而定；粒度 = URL 快照
- 门槛：无 key；但需能连通 `web.archive.org`（本机 2026-10-01/02 不可达）
- 实测：2026-09-28 首页 200、CDX 一度 "Temporarily Offline" 后恢复、`available` 返回快照 JSON；2026-10-01 子代理报告不可达；2026-10-02 `available`/CDX 均 20–25 s 超时（HTTP 000）
- 上游：Internet Archive（站点自身，无 repo/Skill 出处）

## 细节

### 多次实测记录（本机）

| 日期 | 探测 | 结果 |
|---|---|---|
| 2026-09-28 | `https://web.archive.org/` | ✅ 200（145KB） |
| 2026-09-28 | `http://web.archive.org/cdx/search/cdx?url=renda.bjshy.gov.cn*&output=json&limit=8&collapse=urlkey&fl=timestamp,original,statuscode` | ⚠️ 首次返回 "Temporarily Offline"；`&showNumPages=true` 通；复测 CDX 恢复、返回真实行 |
| 2026-09-28 | `https://archive.org/wayback/available?url=bjdx.gov.cn&timestamp=20180601` | ✅ 返回快照 JSON |
| 2026-10-01 | 子代理汇总报告 | ❌ 不可达 |
| 2026-10-02 | `available?url=bjdx.gov.cn&timestamp=20180601` / CDX | ❌ 均 20–25s 超时（HTTP 000） |

### 可用时的两种调用

```bash
# 1) 找某 URL 在某时点的最近快照（JSON）
curl -s -m 20 'https://archive.org/wayback/available?url=bjdx.gov.cn&timestamp=20180601'
# → {"archived_snapshots":{"closest":{"available":true,"url":"http://web.archive.org/web/2018…","timestamp":"2018…"}}}

# 2) CDX 批量枚举（某域名历史抓取清单；collapse=urlkey 去重）
curl -s -m 25 'http://web.archive.org/cdx/search/cdx?url=www.bjdx.gov.cn&output=json&limit=50&fl=timestamp,original,statuscode'
# showNumPages=true 可先探规模
```

### 替代路径

1. 站内自存档：政府网旧栏目有时仍在线（改版未删文件），用 `web_search`/搜狗微信的标题反查现链。
2. 文库/转载站：实施方案、报告类文本常被 51jzrc/人人文库/豆丁 等转载（见 `../gov/beijing-districts.md` 与 `../media/README.md`）。
3. 区报数字报 PDF 老 URL 规则直连试取（见 `../media/epaper/`）。
4. 换网络环境（代理/移动网络）后再试 Wayback。

## 坑

- **处置**：不要因为一次超时就写死「不可用」；先给 1–2 次 20s 超时的机会，通了就立即用（CDX 枚举 + `available` 定位），不通就换替代路径。反之亦然：历史上曾可用 ≠ 现在可用。
