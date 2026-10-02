# ports-shipping —— 港口与水运运价指数统计

- 去哪找：
  - **交通运输部 综合规划司·统计数据**（港口货物/集装箱吞吐量，月度累计 + 年度）文章模板 `https://xxgk.mot.gov.cn/jigou/zhghs/{YYYYMM}/t{YYYYMMDD}_{id}.html`；正文附 **xlsx 附件**（相对 `./P0….xlsx`）；入口页 `https://www.mot.gov.cn/shuju/`
  - **上海航运交易所 运价指数** 单期查询 `https://www.sse.net.cn/index/singleIndex?indexType=scfi`（换 `indexType` 取不同指数）；数据中心（枚举全部指数）`https://www.sse.net.cn/datacenter`；多期查询 `https://www.sse.net.cn/index/scfilist`
  - **中国港口协会**（`port.org.cn` → 跳 `chinaports.org`）数据统计 `https://www.chinaports.org/site/term/48.html`（**转载镜像**）
  - **波罗的海交易所**（国际干散货/油轮指标）指数页 `https://www.balticexchange.com/en/data-services/market-information0/indices.html`；数据 API 门户 `https://api.balticexchange.com/`
- 什么时候用：要港口**货物吞吐量 / 集装箱吞吐量 / 外贸货物吞吐量**（全国·分省·主要港口，月度累计与同比、年度）；要 **SCFI（上海出口集装箱）·CCFI（中国出口集装箱）·SCFIS（结算）·CBFI（沿海散货）·CBCFI（沿海煤炭）·CTFI（进口原油）**等运价指数；要 **BDI / BCI / BPI / BSI** 等国际指数。
- 怎么搜：交通运输部走「栏目 → 年月目录 → 文章」，数字在 **xlsx 附件**；上交所指数**服务端直出 HTML 表**，URL 换参即取，多期为带 `_csrf` 的 POST 表单：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # ① 交通运输部月度港口吞吐量（正文附 xlsx）
  curl -sS -A "$UA" 'https://xxgk.mot.gov.cn/jigou/zhghs/202608/t20260824_4223063.html'
  curl -sS -A "$UA" -O 'https://xxgk.mot.gov.cn/jigou/zhghs/202608/P020260824329599922352.xlsx'
  # ② 上交所某一指数（单期，HTML 内已含数据表）
  curl -sS -A "$UA" 'https://www.sse.net.cn/index/singleIndex?indexType=scfi'
  ```
  结果形态：交通运输部 = HTML 正文 + **xlsx/xls 附件**（相对路径）；上交所 = **服务端渲染 HTML 表**（`?indexType=` 直取），多期走 POST 表单；中国港口协会 = HTML 正文（**数据为转载图片**）；波罗的海 = 需过 WAF / 订阅。
- 覆盖：交通运输部月度《{YYYY}年1-{M}月港口货物、集装箱吞吐量》（约次月底发布，含自年初累计、当月、同比，分省并列出沿海/内河主要港口）与**年度**《{YYYY}年港口货物、集装箱吞吐量》（约次年 1 月）；上交所 SCFI/CCFI 等每周五（节假日调整）15:00 发布，单期可查历史日期、多期可批量导出；波罗的海 BDI 系列**每日**（付费）。
- 门槛：交通运输部、上交所 **免费、免登录、无 key**；中国港口协会 **免费浏览**（附属资料下载多需会员登录）；波罗的海 **WAF 拦截 + API 需注册订阅**。
- 实测：2026-10-03，macOS arm64，curl 8.x，桌面 UA，20 s 超时，同主机 ≥1.5 s 间隔：
  - `GET xxgk.mot.gov.cn/jigou/zhghs/202608/t20260824_4223063.html` → **200**，23 KB，title《2026年1-7月港口货物、集装箱吞吐量》，正文含 xlsx 附件 `./P020260824329599922352.xlsx` ✅
  - `HEAD …/202608/P020260824329599922352.xlsx` → **200**，`application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`，79 248 B ✅
  - `GET xxgk.mot.gov.cn/jigou/zhghs/` → **200 但仅 6 B 空壳** ⚠️（栏目列表不在此路径）
  - `GET www.sse.net.cn/index/singleIndex?indexType=scfi` → **200**，36 KB，服务端含表：SCFI 综合指数 2026-09-24 = 3686.62、2026-09-30 = 3662.30 ✅
  - `GET www.sse.net.cn/datacenter` → **200**，23 KB，枚举全部 `indexType` ✅
  - `GET www.sse.net.cn/index/scfilist` → **200**，43 KB，多期查询表单（`startDate`/`endDate`/`SelLine` + `_csrf`）✅
  - `GET port.org.cn/` → **200**，最终 URL `https://www.chinaports.org/`（**跳转**）；`GET chinaports.org/site/term/48.html` → 200，35 KB，title「数据统计」✅；`GET chinaports.org/site/content/259847.html` → 200，32 KB，但**数据是转载自交通运输部 xlsx 的图片** `https://xxgk.mot.gov.cn/jigou/zhghs/202603/W020260326413674201718.png` ⚠️
  - `GET balticexchange.com/en/data-services/market-information0/indices.html` → **200 但 1 882 B，title「Challenge Validation」（WAF 挑战页）**；换桌面 UA + `Accept` 头仍同 ❌
- 上游：交通运输部 `mot.gov.cn`（`xxgk.mot.gov.cn`）；上海航运交易所 `sse.net.cn`；中国港口协会 `port.org.cn`（`chinaports.org`）；波罗的海交易所 `balticexchange.com`。

## 细节

### 上海航运交易所 `indexType`（取自 `/datacenter`，2026-10-03）

| `indexType` | 指数 | 频率 |
|---|---|---|
| `scfi` | 上海出口集装箱运价指数 | 周 |
| `scfis` | 上海出口集装箱结算运价指数 | 周 |
| `ccfi` | 中国出口集装箱运价指数 | 周 |
| `cbfi` / `cbcfi` / `cbofi` / `cbgfi` | 中国沿海（散货 / 煤炭 / 成品油 / 粮食）运价指数 | 周 |
| `cctfi_coastal` | 中国沿海集装箱运价指数 | 周 |
| `ctfi` | 中国进口原油运价指数 | 周 |
| `cdfi` | 中国进口干散货运价指数 | 周 |
| 其余 `cdi` `cicfi` `twfi` `seafi` `gcspi` `srfi` `ccri` `fdi` `brcvi` `brsti` `brtvi` | 各专项指数 | 见 `/datacenter` |

- 单期：`GET /index/singleIndex?indexType={code}`（HTML 直出）；页面内含 `name="date"` 查询框（`placeholder="2026-10-03"`），历史日期的 GET/POST 传参方式**未实测**。
- 多期：`GET /index/scfilist` 取得表单（含 `_csrf`），再 **POST** `startDate`/`endDate`/`SelLine`/`indexType`（表单字段名以页面为准）。
- 旧域 `www1.sse.net.cn/index/scfiAdvanceNew.jsp`（多期）、`www1.sse.net.cn/index/scfiintronew.jsp`（指数简介/发布日）仍可见；发新公式见 `indexIntro?indexName=scfi`。

### 交通运输部 URL 形态

| 内容 | 文章 URL | 附件 |
|---|---|---|
| 月度《{年}年1-{M}月港口货物、集装箱吞吐量》 | `https://xxgk.mot.gov.cn/jigou/zhghs/{YYYYMM}/t{YYYYMMDD}_{id}.html` | 同目录 `./P0….xlsx` |
| 年度《{年}年港口货物、集装箱吞吐量》 | 同上 | 同上 |
| 2024 及更早的文章 | `https://xxgk.mot.gov.cn/2020/jigou/zhghs/{YYYYMM}/t{YYYYMMDD}_{id}.html` | 同目录 |

- 附件为**相对路径**：`./P020260824329599922352.xlsx` → 绝对路径为「文章所在年月目录 + 文件名」，写成域名根路径会 404。
- 表格字段：港口（全国总计 / 沿海合计 / 内河合计 / 分省，下含主要港口）、**货物吞吐量（万吨）自年初累计 + 同比**、**集装箱吞吐量（万 TEU）自年初累计 + 同比**、**外贸货物吞吐量自年初累计 + 同比**；早期版本另有「本月」列。

### 中国港口协会

- `port.org.cn` 301/302 跳到 `https://www.chinaports.org/`；「数据统计」栏目 `https://www.chinaports.org/site/term/48.html`，文章 `/site/content/{id}.html`，转载交通运输部月度/年度港口数据，但正文数据以**图片**（`xxgk.mot.gov.cn/…/W*.png`）呈现——只能阅读，不能机读。
- 协会另出版《中国港口年鉴》《中国港口》杂志（增值/订阅）。

## 坑

1. **交通运输部栏目列表 URL 拍不到**：`/jigou/zhghs/` 返回 200 但是 6 B 空壳；找历史文章用站内检索（`https://xxgk.mot.gov.cn/` 检索框）或按 `{YYYYMM}/t{YYYYMMDD}_{id}.html` 由标题日期反推，配合搜索引擎 `site:xxgk.mot.gov.cn 港口货物 集装箱吞吐量`。
2. **港口吞吐量一定要取 xlsx**：文章正文的 HTML/图片是排版副本，字段口径与附件表可能不同；做面板一律用附件 xlsx。
3. **上交所数据是服务端渲染的**：`?indexType=` 页面直接含表，但**多期/历史批量**必须过 `scfilist` 的带 `_csrf` POST，纯 GET 拿不到完整历史；`_csrf` 在表单页 `<meta name="csrf-token">` / 隐藏域。
4. **不要把上交所运价指数与「港口吞吐量」混口径**：前者是运价（点/USD per TEU），后者是吞吐量（万吨/万 TEU）；指数是**周度发布**（周五 15:00，节假日顺延），不是每日。
5. **中国港口协会 ≠ 原始数据源**：其「数据统计」是交通运输部的转载（图片）；引用数字应落交通运输部文章/xlsx，署来源时写交通运输部综合规划司。
6. **波罗的海交易所本机进不去**：公开指数页被 WAF 挑战（`Challenge Validation`），数据 API `api.balticexchange.com` 需注册/订阅；国内要 BDI 序列可改用**上海航运交易所 `cdi`/`cdfi`** 或期货/资讯转引，但须注明转引与非官方。
7. **月度是累计值**：交通运输部月度表为「自年初累计」，要当月值需用相邻两月累计相减，且注意口径（如某月修正）。
