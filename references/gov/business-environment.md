# business-environment —— 营商环境评价与民企500强

- 去哪找：
  - 国家发改委「优化营商环境」专栏 `https://www.ndrc.gov.cn/xwdt/ztzl/xhyshj/`（子栏 `dfdt/` 地方动态）
  - 发改委政策文件库 JSON 接口 `https://fwfx.ndrc.gov.cn/api/query`
  - 《中国营商环境发展报告（2026）》发布页 `https://www.ndrc.gov.cn/xwdt/tzgg/202605/t20260508_1405105.html`（PDF `./P020260508388323173734.pdf`）；2025 版 `https://www.ndrc.gov.cn/xwdt/tzgg/202504/t20250430_1397515.html`（PDF `P020250430371376827216.pdf`）
  - 全国工商联 中国民营企业 500 强专题 `https://www.acfic.org.cn/ztzlhz/500q2026/`；历年 2025 版 `https://www.acfic.org.cn/ztzlhz/2025_500q/`
  - 全国工商联「持续优化营商环境 助力民企高质量发展」专题 `https://www.acfic.org.cn/ztzlhz/youhua_zhuli/`
  - 世界银行 B-READY `https://www.worldbank.org/en/businessready`；数据 API `https://api.worldbank.org/v2/country/all/indicator/IC.BRE.BE.OS?format=json`
- 什么时候用：
  - 关键词：营商环境 评价 / 营商环境 报告 / 优化营商环境条例 → **官方评价口径与年度报告**。
  - 关键词：民营企业 500 强 / 制造业 500 强 / 服务业 100 强 → **年度榜单名单、营收门槛、区域与行业分布**。
  - 关键词：万家民营企业评营商环境 → **民营企业主观评价（分省/分城市满意度）**。
  - 关键词：营商环境 某省/某市 行动方案 → **地方专栏与政策清单**。
  - 关键词：B-READY / 营商环境 国际排名 → **世界银行新评估体系**（注意中国未入评）。
  - 不适用：企业工商登记 → `gsxt.md`；信用红黑名单/双公示 → `credit-china.md`；城市信用监测排名 → `city-credit.md`。
- 怎么搜：
  - **发改委政策文件检索（JSON）**：`GET https://fwfx.ndrc.gov.cn/api/query?qt=<关键词>&tab=all&page=1&pageSize=20&siteCode=bm04000fgk&key=CAB549A94CF659904A7D6B0E8FC8A7E9&timeOption=0&sort=dateDesc` → `{"ok":true,"data":{"totalHits":N,"resultList":[…]}}`。参数表见「细节」，结果上限 500 条（前端声明）。
  - **榜单/名单**：进专题页 → 「会议发布」列表 → 榜单条目页；名单本体多为**单张 JPG**（无 HTML 表格、无 PDF/Excel），需 OCR。
  - **B-READY**：`data.worldbank.org` 指标页，或 API `IC.BRE.BE.OS` 及各支柱分项 `IC.BRE.BE.P1…P10`。
  - 结果形态：HTML（专栏/公告）+ PDF（报告与名单）+ JPG（榜单）+ JSON（发改委文件库、World Bank API）。
- 覆盖：发改委营商环境专栏按省更新地方动态（最新 2026-09）；《中国营商环境发展报告》2018–2026 年度（2026 版 2026-05 发布）；民营企业 500 强 2010–2026 年度；万家民营企业评营商环境 2019–2025 年度；B-READY 2024/2025 两版（50 → 100+ 经济体）。
- 门槛：免费、免登录、无验证码（发改委 / 工商联 / 世界银行均直连）。
- 实测：2026-10-03，macOS arm64，curl 8.x，桌面 UA，20 s 超时。发改委文件库 API `qt=营商环境` → `200`，`ok=true`，`totalHits=253`；营商环境专栏 `200`（标题「优化营商环境」，含 `dfdt/` 子栏，最新条目 2026-09）；2026 报告公告页 `200`（正文含 PDF 相对链接）；2025 报告 PDF → `206`，头 4 字节 `%PDF-1.7`（可下）；工商联 500 强专题 `200`、榜单条目页 `200`（32 KB，正文只有 `<img src="./W020260922444542877116.jpg">`）；工商联优化营商环境专题 `200`；World Bank API `country/CN/indicator/IC.BRE.BE.OS` → `200` 但 `value` 全为 `null`，`country/all…&date=2024` → 50 个经济体有值、**不含 CHN**（含 `HKG`）。
- 上游：<https://www.ndrc.gov.cn/>；<https://www.acfic.org.cn/>；<https://www.worldbank.org/en/businessready>

## 细节

### 发改委文件库接口参数（`https://fwfx.ndrc.gov.cn/api/query`，GET）

| 参数 | 取值 | 说明 |
|---|---|---|
| `qt` | 关键词（UTF-8 URL 编码） | 必填 |
| `tab` | `all` / `fzggwl` / `gfxwj` / `gg` / `ghwb` / `tz` / `zcjd` / `qt` | 文件类型 |
| `page` / `pageSize` | `1` / `20` | 前端默认 20 |
| `siteCode` | `bm04000fgk` | 发改委文件库站点码（固定） |
| `key` | `CAB549A94CF659904A7D6B0E8FC8A7E9` | 前端硬编码（页面源码可见） |
| `startDateStr` / `endDateStr` | `YYYY-MM-DD` | 年份区间 |
| `timeOption` | `0` / `2` | 0=不限；2=按年份 |
| `sort` | `dateDesc` / `weight` | 时间 / 相关度 |

记录字段：`title`、`url`、`summary`、`docDate`（YYYY-MM-DD）、`dreDate`（epoch ms）、`indexDate`、`domainSite`。

### 年度报告与专题路径

| 资源 | URL |
|---|---|
| 发改委「优化营商环境」专栏 | `https://www.ndrc.gov.cn/xwdt/ztzl/xhyshj/` |
| 　└ 地方动态 | `https://www.ndrc.gov.cn/xwdt/ztzl/xhyshj/dfdt/` |
| 《中国营商环境发展报告（2026）》 | `…/xwdt/tzgg/202605/t20260508_1405105.html` + `…/202605/P020260508388323173734.pdf` |
| 《中国营商环境发展报告（2025）》 | `…/xwdt/tzgg/202504/t20250430_1397515.html` + `…/202504/P020250430371376827216.pdf` |
| 《中国营商环境报告2020》（发改委法规司） | `https://www.ndrc.gov.cn/fzggw/jgsj/fgs/sjdt/202010/t20201019_1248411.html` |
| 民企 500 强 2026 | `https://www.acfic.org.cn/ztzlhz/500q2026/` |
| 民企 500 强 2025 | `https://www.acfic.org.cn/ztzlhz/2025_500q/` |
| 2026 榜单条目（500 强 / 制造业 500 强 / 服务业 100 强） | `…/500q2026/hyfb_500q2026/202609/t20260922_331490.html`、`…331491.html`、`…331492.html` |
| 工商联「持续优化营商环境」专题 | `https://www.acfic.org.cn/ztzlhz/youhua_zhuli/`（成效 `achievement_yhzl/`、案例 `cases_yhzl/`、动态 `news_yhzl/`） |
| 工商联「优化营商环境」栏目 | `https://www.acfic.org.cn/lqfw/czyz/yhyshj/` |
| 万家民营企业评营商环境 2023 结论 | `…/youhua_zhuli/achievement_yhzl/202409/t20240918_314152.html` |

### 省级专栏（抽查 2 省）

| 省 | 入口 |
|---|---|
| 浙江 | 省经济信息中心「营商环境」`https://zjic.zj.gov.cn/ywdhx/yshj/`；省发改委 `https://fzggw.zj.gov.cn/`（如《复制推广国家营商环境创新试点改革举措任务清单》`…/art/2023/1/19/art_1229248116_58935536.html`） |
| 上海 | 市政府「营造超一流营商环境」专题 `https://cdn.shanghai.gov.cn/yzcylyshj/index.html`（政策文件 `yshjzcwj/`、政策解读 `yshjzcjd/`）；《上海市加快打造国际一流营商环境行动方案（2026年）》`https://www.shanghai.gov.cn/nw12344/20260104/0b80134b5fa944eea6c12e586bfec06e.html` |

### 世界银行 B-READY

- 入口 `https://www.worldbank.org/en/businessready`；方法论 `/methodology`；覆盖经济体 `/about-us/covered-economies`。
- 数据：`https://data.worldbank.org/indicator/IC.BRE.BE.OS?locations=CN`；API `https://api.worldbank.org/v2/country/all/indicator/IC.BRE.BE.OS?format=json&per_page=1000&date=2024`。
- 指标族：`IC.BRE.BE.{OS,P1…P10}`（Business Entry 总评 + 各支柱）。
- **中国未入评**：B-READY 2024 仅 50 个经济体（名单含 `HKG`，无 `CHN`）。

## 坑

1. **民企 500 强榜单是图片**：条目页正文只有一张 JPG（`W020260922444542877116.jpg`），无表格、无附件；要结构化名单得 OCR，或退用《调研分析报告》的文字结论。
2. **专题路径逐年改名**：2026 = `/ztzlhz/500q2026/`，2025 = `/ztzlhz/2025_500q/`，无统一模板 → 从首页/栏目页解析当年链接。
3. **报告 PDF 时间戳不可猜**：`P020260508388323173734.pdf` 必须从公告页 HTML 取。
4. **B-READY 无中国数据**：世行 2021 年停发《营商环境报告》(Doing Business)，B-READY 至今未评中国；「国际排名」只能引历史 DB 排名（2020 年第 31 位）或中国官方评价口径。
5. **发改委文件库只返回最新 500 条**，且 `key` 为前端硬编码、改版可能失效。
6. gov.cn 无独立「营商环境」专题（`/zhuanti/yshj/` → 404）；国家层面政策原文改用 `gov.cn.md` 的 `search-gov/data` 接口。
