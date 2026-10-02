# provincial-yearbooks —— 各省统计年鉴在线入口与规律

省级统计年鉴（统计局口径）**没有全国统一入口**：除少数省外，各省统计局在五花八门的路径下发布，正文多为 frameset（`{年}/zk/indexch.htm`）或逐篇 HTML/图片。本卡给出实测入口与 URL 规律，并列出第三方聚合站。

- 去哪找：逐省入口见「细节 · 省级总表」；国家层年鉴（`stats.gov.cn`、`data.stats.gov.cn`）见 `../stats/`，本卡不重复。
- 什么时候用：要**某省**统计年鉴的官方表格（人口、GDP、分行业、分市县）；要知道年鉴正文是 HTML 还是扫描图片；要一个「按省找年鉴」的起步清单。
- 怎么搜：先按 `tjj.<省>.gov.cn` 或 `tj.<省>.gov.cn` 猜统计局域名，进「统计年鉴/统计资料/统计数据」栏目；年鉴路径**无统一规律**（`col/colNNNNN`、`cNNNNNN/pic_list.shtml`、`tjfw/tjcbw/tjnj`、`tjsj/sjkscx/tjnj`）；正文多为 frameset（`…/tjnjnew/{年}/zk/indexch.htm`、`…/tjnj/{年}/zk/indexch.htm`），表页是 `.htm` 或扫描 `.jpg`；拿不到时用第三方聚合再回官方核对。
- 覆盖：省级综合统计年鉴（多数 2000s 起可在线）；部分省另有**普查年鉴**（人口/经济）与**区域年鉴**（如北京区域统计年鉴）。年份随各省，最新多为 2025 卷（2024 年数据）。
- 门槛：官方站**免费**；第三方聚合站部分**需会员/付费**。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA，逐站 GET（状态见「省级总表」；其中上海 `/tjnj/`、江苏 `col85821`、广东 `/tjzl/`、四川 `c112132`、河南 `tjfw/tjcbw/tjnj/`、湖北 `tjsj/sjkscx/tjnj/` 为**直接请求**；浙江、山东两条为**首页取链接**，年鉴栏目 URL 未单独请求）。
- 上游：各省统计局官网；第三方 `tjcn.org`（中国统计信息网）、`tjnjw.com`（统计年鉴网）、`tjnj.net`→`tjnjdata.com`。

## 细节

### 省级总表（2026-10-03 实测）

| 省/市 | 年鉴入口 | 状态 | 正文形态 |
|---|---|---|---|
| 上海 | `https://tjj.sh.gov.cn/tjnj/`（首页 `/tjnj/index.html`） | ✅ 200 | 逐年页 `/tjnj/{YYYYMMDD}/{hash}.html`（2025 卷 `/tjnj/20260302/ab5e54f645fd4184b9e9c3aeef8a1c6c.html`） |
| 江苏 | `http://tj.jiangsu.gov.cn/col/col85821/index.html` | ✅ 200 | 栏目壳（1,468 B），正文另取 |
| 浙江 | `https://tjj.zj.gov.cn/`（首页未见年鉴直链） | ⚠️ 首页 200 | 年鉴栏目需站内找 |
| 广东 | 统计资料 `https://stats.gd.gov.cn/tjzl/index.html` | ✅ 200 | `/tjzl/` 为 569 B JS 跳转壳；年鉴另有 `https://stats.gd.gov.cn/gdtjnj/`（上游声明，未本机请求） |
| 山东 | `http://tjj.shandong.gov.cn/col/col6279/index.html`（统计数据查询） | ✅ 首页 200 | 栏目制；该栏目 URL 取自首页，未单独请求 |
| 四川 | `https://tjj.sc.gov.cn/scstjj/c112132/pic_list.shtml` | ✅ 200 | frameset：`https://tjj.sc.gov.cn/scstjj/tjnjnew/{年}/zk/indexch.htm`（2014–2025） |
| 北京 | 见 `../stats/tjj.beijing.gov.cn.md` | ✅ | 年鉴为**扫描图片**，逐表 `.jpg` |
| 河南 | `https://tjj.henan.gov.cn/tjfw/tjcbw/tjnj/` | ✅ 200 | 栏目制（普查年鉴 `/tjfw/tjsj/pcnj/`） |
| 湖北 | `https://tjj.hubei.gov.cn/tjsj/sjkscx/tjnj/` | ⚠️ 200 但 71 B | JS 跳转壳，需跟真实地址 |

### 第三方聚合（非官方，用作线索）

| 站 | 入口 | 说明 | 本机实测 |
|---|---|---|---|
| 中国统计信息网 | `http://www.tjcn.org/tjnj/index.html` | 统计年鉴下载（PDF/EXCEL），分省目录 `/tjnj/<省码>/<id>.html`；有会员/交易 | ✅ 200（GBK） |
| 统计年鉴网 | `http://www.tjnjw.com/niandu/diqunianjian-2025.html` | 「全国各地区 2025 统计年鉴汇总」，逐省/市/区县条目 | ✅ 200 |
| 统计年鉴下载站 | `https://tjnj.net/` → `https://www.tjnjdata.com/` | 1982–2026 全国省市年鉴 | ✅ 200（跳转） |

## 坑

1. **年鉴路径逐年/逐省漂移**，别套模板；先打统计局首页找「统计年鉴」链接再跟。
2. 正文有两类：**HTML 表格**（可直接解析）与**扫描图片**（北京年鉴；需 OCR）；湖北/广东的栏目页是 **JS 跳转壳**（几十~几百字节）。
3. 第三方聚合站**非官方**：版本、口径、更新时点都需回官方核对；部分内容要会员/付费。
4. `tjnj.net` 会 301 到 `tjnjdata.com`；`yrdcpcn.com` 等区域站也可能挂年鉴库，注意甄别来源。
5. 与 `../stats/` 分工：**全国口径/分省指标数值**走 `../stats/data.stats.gov.cn.md`；**省级年鉴原文**走本卡。
