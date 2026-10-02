# bond-market-stats —— 债券市场统计补充入口

- 去哪找：
  - **上交所**：上证债券信息网 `https://bond.sse.com.cn/home/`——债券现券交易月报 `https://bond.sse.com.cn/data/statistics/monthly/bond/`、收益率曲线与债券估值（中证估值）`https://bond.sse.com.cn/market/indexv/ycav/`；主站债券成交概况 `https://www.sse.com.cn/market/bonddata/overview/monthly/`
  - **深交所**：市场数据·债券（成交概况 日/周/月/年）`https://www.szse.cn/market/bond/overview/monthly/index.html`、可转债转股统计 `https://www.szse.cn/market/bond/convertible/index.html`；专题统计导航 `https://www.szse.cn/market/subject/index.html`
  - **中国债券信息网（中债）统计月报**：`https://www.chinabond.com.cn/yjfx/yjfx_zzfx/zzfx_yb/index.html`；中债指数统计及分析月报 `https://www.chinabond.com.cn/zzsj/zzsj_zzjgcp/zzjgcp_cpdt/cpdt_zzzs/202511/t20251117_854837639.html`（近期条目按同栏目换 ID）
  - **财政部**：债务管理司月度《地方政府债券发行和债务余额情况》`http://zwgls.mof.gov.cn/tjsj/`（本层 `lgfv-platforms.md` 亦用）
  - 银行间：交易商协会 `nafmii.org.cn.md`（承销/发行 PDF）、上清所 `shclearing.com.cn.md`（清算/披露）、中国货币网 `../business/chinamoney.com.cn.md`（债券行情 `https://www.chinamoney.com.cn/chinese/mkdatabond/`）
- 什么时候用：要**交易所口径的债券统计**（成交笔数/金额、现券交易月报、可转债转股、中证债券估值）、**中债统计月报/指数月报**、地方债月度发行与余额、交易商协会债务融资工具统计；即 `../business/chinabond.com.cn.md`、`nafmii.org.cn.md` 之外的**补充入口**。
- 怎么搜：全是**栏目页 + 按年/月列表 + 文章页（HTML 表或 PDF）**的静态结构，改 URL 年月段即可；交易所成交表由 JS/接口渲染。
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  curl -sSL -A "$UA" 'https://bond.sse.com.cn/data/statistics/monthly/bond/'   # 上交所债券现券交易月报
  curl -sSL -A "$UA" 'https://www.sse.com.cn/market/bonddata/overview/monthly/'  # 上交所债券成交概况
  curl -sL  -A "$UA" 'https://www.szse.cn/market/bond/overview/monthly/index.html' # 深交所债券成交概况(月)
  curl -s   -A "$UA" 'http://zwgls.mof.gov.cn/tjsj/'                            # 财政部债务管理司月度列表
  ```
  结果形态：HTML 表 / 文章页；`chinabond` 月报列表**由 JS 载入，curl 只得壳页**（见坑 1）；深交所表由 `ShowReport/data` 接口出 JSON。
- 覆盖：上交所债券（现券交易月报、债券成交概况、中证估值/收益率曲线）；深交所债券（成交概况 日/周/月/年、可转债转股）；中债统计月报与中债指数月报；地方债月度发行与余额（债务管理司）；交易商协会债务融资工具发行/主承统计。年份以各栏目披露为准。
- 门槛：免费、免登录（本机实测）；`bond.sse.com.cn` 与 `www.sse.com.cn` 需桌面 UA +（部分）尾斜杠。
- 实测：2026-10-03，macOS arm64，curl 8.x，桌面 UA，20 s 超时：
  - `https://bond.sse.com.cn/home/` → `200/58,524`；`/data/statistics/monthly/bond/` → `200/21,311`（`<title>债券现券交易月报`）；`/market/indexv/ycav/` → `200/28,041`（`<title>收益率曲线和债券估值`）✅（无尾斜杠时 `301`）
  - `https://www.sse.com.cn/market/bonddata/overview/monthly/` → `200/27,432`（`<title>债券成交概况`）✅
  - `https://www.szse.cn/market/bond/overview/monthly/index.html` → `200/27,652`；`/market/bond/convertible/index.html`、`/market/bond/overview/{daily,weekly,yearly}/index.html` 均在专题统计导航内 ✅
  - `https://www.chinabond.com.cn/yjfx/yjfx_zzfx/zzfx_yb/index.html` → `200/38,039`（`<title>中国债券信息网-月报`），`index_N.html` 翻页可达 ⚠️（列表内容 JS 载入）
  - `http://zwgls.mof.gov.cn/tjsj/` → `200/12,330`，最新《2026年8月地方政府债券发行和债务余额情况》`./202609/t20260924_3998108.htm` ✅
  - `https://www.chinabond.com.cn/zzsj/` → `200/108,907`（`<title>中国债券信息网-中债数据`）✅
- 上游：`sse.com.cn` / `bond.sse.com.cn`（上海证券交易所）；`szse.cn`（深圳证券交易所）；`chinabond.com.cn`（中央国债登记结算有限责任公司）；`mof.gov.cn`（财政部债务管理司）。

## 细节

### 一、入口速查

| 主题 | URL | 形态 |
|---|---|---|
| 上交所债券现券交易月报 | `https://bond.sse.com.cn/data/statistics/monthly/bond/` | HTML 表（同比/环比 + 交易金额） |
| 上交所债券成交概况（月） | `https://www.sse.com.cn/market/bonddata/overview/monthly/` | HTML 表，另有日/周/年变体 |
| 上交所收益率曲线与债券估值 | `https://bond.sse.com.cn/market/indexv/ycav/` | 中证估值数据页 |
| 深交所债券成交概况（日/周/月/年） | `https://www.szse.cn/market/bond/overview/{daily,weekly,monthly,yearly}/index.html` | JS 渲染（`ShowReport/data`） |
| 深交所可转债转股统计 | `https://www.szse.cn/market/bond/convertible/index.html` | JS 渲染 |
| 中债统计月报 | `https://www.chinabond.com.cn/yjfx/yjfx_zzfx/zzfx_yb/index.html`（翻页 `index_N.html`） | 列表 JS 载入 |
| 中债指数月报 | 中债数据 `https://www.chinabond.com.cn/zzsj/` → 指数产品动态栏目 | 文章页 + PDF/xlsx 附件 |
| 地方债月度发行与余额 | `http://zwgls.mof.gov.cn/tjsj/` → `{YYYYMM}/t{YYYYMMDD}_{id}.htm` | HTML 表 |

### 二、深交所债券数据的取数接口

- 深交所市场统计统一走 `GET https://www.szse.cn/api/report/ShowReport/data?SHOWTYPE=JSON&CATALOGID=<表号>&TABKEY=tab1&PAGENO=1&random=…`（带 `Referer` 与桌面 UA）。
- 债券栏目页（`/market/bond/**`）的 `CATALOGID` **不在返回 HTML 里**，由页面脚本运行时装配——**本机未从 HTML 取到债券表号**，需在真实浏览器打开栏目页抓该请求的 `CATALOGID`（参数与响应结构见 `../business/szse.cn.md`）。
- 已知可用样例（非债券）：`CATALOGID=1803_sczm` = 证券类别统计（见 `../business/szse.cn.md`）。

### 三、口径区分（别互换）

| 口径 | 主管/机构 | 统计什么 |
|---|---|---|
| 交易所（上交所/深交所） | 证券交易所 | 场内现券成交、可转债转股、上市债券 |
| 中债（中央结算公司） | `chinabond.com.cn` | 银行间登记托管、中债估值/收益率曲线/指数、市场月报 |
| 上清所 | `shclearing.com.cn` | 银行间清算托管、发行披露 |
| 交易商协会 | `nafmii.org.cn` | 债务融资工具承销/发行统计 |
| 中国货币网 | `chinamoney.com.cn` | 银行间本币行情、债券做市/成交 |
| 财政部 | `zwgls.mof.gov.cn` | 地方政府债券发行与余额（政府债） |

## 坑

1. **中债月报列表是 JS 渲染**：`/yjfx/yjfx_zzfx/zzfx_yb/index.html` 与 `index_N.html` 本机 curl 只得壳页（页面正文条目由脚本注入），要条目需浏览器或抓其 XHR；同站 `yield.chinabond.com.cn` 取数接口亦未跑通（见 `../business/chinabond.com.cn.md` 坑 1）。
2. **上交所债券站需尾斜杠**：`bond.sse.com.cn/home`、`/data/statistics/monthly/bond`、`/market/indexv/ycav` 无尾斜杠均 `301`，脚本直写带 `/` 的地址省一跳。
3. **深交所债券 `CATALOGID` 本机没取到**：不要用猜的表号硬拉；缺失时回落到栏目页由浏览器抓包，或改用 `../business/cninfo.com.cn.md` 的公告数据、上交所 counterpart。
4. **上交所网站有两套域**：`bond.sse.com.cn`（债券专站：月报、中证估值）与 `www.sse.com.cn/market/bonddata/`（主站债券数据：成交概况）。同一指标两边都有，引用时注明出处页。
5. **交易商协会只有 PDF、无 JSON**（见 `nafmii.org.cn.md`）；需要结构化数字自行解析 PDF。
6. **「债券市场统计」不等于「债券发行明细」**：要逐只券的发行/存续信息去 `localgov-debt.md`（地方债）或 `chinabond`/交易所披露页；统计月报只给汇总。
7. 月度数据存在**发布时滞**（如 2026-10 实测债务管理司最新为 2026 年 8 月），引用时核对期次与发布日期。
