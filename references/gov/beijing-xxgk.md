# 北京政府信息公开年报 —— 街乡镇正职线索树

- 去哪找：
  - 年报树根模板：`https://<区门户>/zfxxgk/zfxxgknb/{Y}/`（`{Y}`=4 位年；各区实际路径见 `## 细节` 模板表）
  - 可直取样例（密云）：`https://www.bjmy.gov.cn/zwgk/zfxxgk/zfxxgknb/gknb2017/201802/t20180223_195744.html`
  - 大兴街乡镇子树：`https://www.bjdx.gov.cn/bjsdxqrmzf/zwfw/zfxxgk/dxqzf69/{Y}n/xzjd/`
  - 怀柔街乡镇子树：`https://www.bjhr.gov.cn/zfxxgkzl/gknb/{Y}nb/zxjd{Y}/`
  - 石景山统栏入口：`https://www.bjsjs.gov.cn/gongkai/`
  - 失效/迁移的区：改从各区门户首页/`gongkai` 栏目重新定位（见 `## 细节` 状态表）。
- 什么时候用：要**逐街乡镇政府正职（镇长/乡长/主任）姓名**线索——年报正文常年列「本单位行政正职情况」；或按「区 × 年 × 街乡镇」穷尽枚举年报附件。
- 怎么搜：
  - **爬取器**：`python run/crawl_gknb.py --years 2017 2018 2019 [--report]`
    - 入口 = 各区**年报树根**（见 `## 细节`），逐页解析 `<a href>`，把 `DOC_RE`（`doc/docx/pdf/rtf/xls/xlsx`）与 `PAGE_RE`（`html/htm/shtml`）链接**完整落盘**，不做姓名过滤；
    - 深度展开：从年报页继续抓子页/附件，链接文本含 `镇|乡|街道|地区|报告|gknb|nb` 时纳入；
    - 输出经 `crawl.store()` 落 `data/index/pages.<host>.jsonl`（**按主机分片**，避免并发 append 撕裂行）。
  - **抽取器**：`python run/harvest_gknb.py` → `out/gknb_hits.jsonl`
    - 正则 `(地区办事处主任|街道办事处主任|办事处主任|镇长|乡长)[：:，,、\s]{0,3}([\u4e00-\u9fa5]{2,3})`，再按百家姓 + 停用字过滤。
    - 注意：会产出「任组长」这类误命中（见 `gknb_hits.jsonl`），**下游须人工/规则复核**。
  - 探测命令：`curl -sSk -L -m 20 -A "$UA" -o /dev/null -w '%{http_code} %{url_effective}\n' '<url>'`（模板变量 `{Y}`=4 位年，`{Y2}`=2 位年）。
- 覆盖：北京各区门户「政府信息公开年报」栏目（`gknb`），按「区 × 年 × 街乡镇」；年报正文多为静态 HTML，部分区为 Office/PDF 附件；近年各年度（列表实测含 2017–2019）。
- 门槛：免费、免登录；**路径漂移严重**，脚本里的树根是 2026-09-28 会话快照，运行前须先探测；顺义 robots `Disallow: /`（见 `beijing-districts.md`）。
- 实测：2026-10-02，macOS（arm64），curl（`-sSk -L -m 20`，桌面 UA）。密云、大兴、怀柔、石景山树根 200；房山/门头沟/通州/平谷/昌平/海淀/丰台/顺义/东城/西城等 10+ 区 404 或迁移（明细见 `## 细节`）；密云样例正文 200 / `text/html; charset=utf-8`，`<title>高岭镇_2017年_…`。URL 模板与抽取逻辑来自 `run/crawl_gknb.py`、`run/harvest_gknb.py`；`out/gknb_hits.jsonl`（生成于前序会话）本轮仅读取其内容，未重跑流水线。
- 上游：北京各区门户 gknb 栏目（见 `## 细节` 模板表）；本地脚本 `run/crawl_gknb.py`、`run/harvest_gknb.py`

## 细节

证据来源：`run/crawl_gknb.py`、`run/harvest_gknb.py`（不含本仓库时，URL 模板仍可复用），产出 `out/gknb_hits.jsonl`（24 条命中）、`out/crawl_report.md`。

### 年报树 URL 模板与本次实测（2026-10-02，macOS + curl）

| 区 | 树根模板（HTTPS） | 本次状态 | 现象 |
|---|---|---|---|
| 密云区 | `https://www.bjmy.gov.cn/zwgk/zfxxgk/zfxxgknb/gknb{Y}/` | ✅ 200（gknb2018/，utf-8） | 可用；文章形态 `.../gknb2017/201802/t20180223_195744.html` |
| 大兴区 | `https://www.bjdx.gov.cn/bjsdxqrmzf/zwfw/zfxxgk/dxqzf69/{Y}n/`（另有 `/{Y}n/xzjd/` 街乡镇子树） | ✅ 200（2017n、2018n，utf-8） | 可用 |
| 怀柔区 | `https://www.bjhr.gov.cn/zfxxgkzl/gknb/{Y}nb/` | ✅ 200（2018nb，utf-8） | 另有 `/{Y}nb/zxjd{Y}/` 街乡镇子树 |
| 石景山区 | `https://www.bjsjs.gov.cn/gongkai/` | ✅ 200 | 统栏入口，非按年目录 |
| 房山区 | `https://www.bjfsh.gov.cn/zfxxgk/zfxxgknb/{Y}/` | ❌ 404；基目录 403 | 路径已漂移 |
| 门头沟区 | `https://www.bjmtg.gov.cn/zfxxgk/zfxxgknb/{Y}/` | ⚠️ 301 回首页 | 目录失效 |
| 通州区 | `https://www.bjtzh.gov.cn/zfxxgk/zfxxgknb/{Y}/` | ❌ 404（年目录与基目录均 404） | |
| 平谷区 | `https://www.bjpg.gov.cn/zfxxgk/zfxxgknb/{Y}/` | ❌ 404（错误页 charset=iso-8859-1） | |
| 昌平区 | `https://www.bjchp.gov.cn/cpqzf/xxgkzl/zfxxgknb82/{Y}43/`、`…/{Y}64/` | ❌ 404（201843、201764 均 404） | 路径已漂移 |
| 海淀区 | `https://www.bjhd.gov.cn/zfxxgk/zfxxgknb/{Y}/` | ❌ 301 → `https://zyk.bjhd.gov.cn/jbdt/zfxxgknb/{Y}/` → 404 | 已迁资源库域名 |
| 丰台区 | `https://www.bjft.gov.cn/zfxxgk/zfxxgknb/{Y}/` | ❌ 404 | |
| 顺义区 | `https://www.bjshy.gov.cn/web/zwgk/zfxxgk/zfxxgknb/{Y}/` | ❌ 404 | |
| 东城区 | `https://www.bjdch.gov.cn/zfxxgk/zfxxgknb/{Y}/` | ❌ 404 | |
| 西城区 | `https://www.bjxch.gov.cn/zfxxgk/zfxxgknb/{Y}/` | ❌ 404 | |
| 朝阳区 | `https://www.bjchy.gov.cn/zfxxgk/zfxxgknb/{Y}/` | 未复测（该域 HTTPS 不可用，须 http） | 见 `bjchy.gov.cn.md` |
| 延庆区 | `https://www.bjyq.gov.cn/zfxxgk/zfxxgknb/{Y}/` | 未复测（该域只服务 http） | 见 `beijing-districts.md` |

> **结论：路径漂移严重**。脚本里的树根是 2026-09-28 会话时的快照，2026-10-02 复测已有 10+ 区返回 404/迁移。使用时**先探测树根**，失效的改从各区门户首页/`gongkai` 栏目重新定位，或退回搜狗微信按「区名 + 街道 + 政府信息公开年报/工作报告」检索。

### 附件类型与页面形态

- 年报正文多为**静态 HTML**（密云样例 200 / `text/html; charset=utf-8`，`<title>高岭镇_2017年_…`），可直接取。
- 部分区把年报做成**Office/PDF 附件**，脚本按扩展名下载：`.doc/.docx/.pdf/.rtf/.xls/.xlsx`（`crawl.py` 的 `DOCTYPES`、`crawl_gknb.py` 的 `DOC_RE`）。
- 民政口径的对照：`out/crawl_report.md` 统计全站落盘 5326 页（含 PDF 627），其中 `www.bjdch.gov.cn` 177 PDF、`www.bjxch.gov.cn` 175 PDF、`www.bjdx.gov.cn` 58 PDF——东城/西城/大兴的年报附件占比最高。

### 已确认命中样例（`out/gknb_hits.jsonl`，24 条）

| host | 年份 | 条数 |
|---|---|---|
| www.bjmy.gov.cn | 2017 / 2018 / 2019 | 6 / 3 / 8 |
| www.bjdx.gov.cn | 2017 / 2019 | 3 / 1 |
| www.bjchp.gov.cn | 2017 / 2018 | 1 / 2 |

真实 URL 样例（可用于回归）：

```
https://www.bjmy.gov.cn/zwgk/zfxxgk/zfxxgknb/gknb2017/201802/t20180223_195744.html
https://www.bjmy.gov.cn/zwgk/zfxxgk/zfxxgknb/gknb2017/201803/t20180309_195741.html
```

## 坑

1. **树根会漂移**：不要在代码里硬编码年目录并假设长期有效；每次运行先做状态探测，失效即重新定位。
2. **HTTPS 不可用域**：朝阳（443 握手失败）、延庆（20s 超时）只服务 http；用 `-sSk` 且改 http。
3. **编码**：门户 UTF-8 为主；错误页偶见 `iso-8859-1`；朝阳系页面为 GB2312/GBK，需 `iconv -f gb18030`。
4. **抽取噪声**：「任组长」等非人名会入库 → 必须复核，勿直接当人名清单。
5. **附件解析**：macOS 环境无 `requests/bs4/lxml`，正文/附件解析走 stdlib + `curl` 子进程；`.doc` 老格式难解析，优先 `.pdf/.docx`。
6. **robots**：见 `beijing-districts.md`（顺义 `Disallow: /`）。
