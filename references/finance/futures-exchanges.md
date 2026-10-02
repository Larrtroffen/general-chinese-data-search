# futures-exchanges —— 期货交易所行情与持仓

- 去哪找：上期所 `https://www.shfe.com.cn/reports/tradedata/`；中金所 `http://www.cffex.com.cn/cn/scsj.html`；广期所 `http://www.gfex.com.cn/gfex/hqsj/redirect_firstChannel.shtml`；大商所 `http://www.dce.com.cn/`；郑商所 `http://www.czce.com.cn/`。
- 什么时候用：要**期货合约日行情**（开高低收/结算价/成交量/成交额/持仓量）、日成交持仓排名、仓单日报、周/月/年统计、历史行情下载；做商品/金融期货量价与持仓研究。
- 怎么搜：逐所不同——
  - **中金所（唯一免 JS 的 CSV 直链）**：`GET http://www.cffex.com.cn/sj/hqsj/rtj/{YYYYMM}/{DD}/{YYYYMMDD}_1.csv`（`_1`=日行情，`text/csv`，**GBK 编码**，含 `合约代码,昨结算,最高价,最低价,成交量,成交金额,持仓量,持仓变化,最新价,涨跌,前结算,涨跌1,涨跌2,Delta`）。
  - **上期所**：`/reports/tradedata/` 下按 `query_params` 取值——`kx`（日交易快讯）、`pm`（日交易排名）、`js_f`（每日结算参数）、`dailystock`（仓单日报）、`timeprice`（日间均价）；页面为客户度 SPA，`/data/dailydata/*.dat` 旧直链已失效（404）。
  - **广期所**：历史行情 `/gfex/lshq/lshqxz_new.shtml`、日行情、日成交持仓排名、仓单日报栏目（页面经 JS 渲染，需浏览器解析真实下载链接）。
  - **大商所 / 郑商所**：本机 curl 被 WAF 拦（见「坑」），需浏览器。
- 覆盖：五所主要期货/期权品种的日行情、成交持仓排名、仓单与结算参数、周月年统计、历史数据下载；日频（日终）。
- 门槛：免费；**中金所 CSV 免 JS**，上期所/广期所页面需浏览器解析，大商所/郑商所 WAF 拦 curl。
- 实测：2026-10-03，桌面 UA curl——中金所 `GET http://www.cffex.com.cn/sj/hqsj/rtj/202609/30/20260930_1.csv` → `200/54,380 B`、`text/csv`（GBK，正文含 `HO2610-C-2500,…`）；`GET http://www.cffex.com.cn/` `200/109,582 B`（跳 `/cn/index.html`）。上期所 `GET https://www.shfe.com.cn/` `200/198,931 B`；`GET /reports/tradedata/datadownload/` `200/122,231 B`；`GET /data/dailydata/kx/kx20260930.dat` → `404`；`tsite.shfe.com.cn` 不可达（curl `000`）。广期所 `GET http://www.gfex.com.cn/` `200/188,328 B`；`GET /gfex/lshq/lshqxz_new.shtml` `200/49,524 B`（无直链）。大商所 `https://www.dce.com.cn/` `000`（握手失败）、`http://www.dce.com.cn/` → `412`；郑商所 `http://www.czce.com.cn/` → `412`。
- 上游：各交易所官网（上海期货交易所 / 中国金融期货交易所 / 广州期货交易所 / 大连商品交易所 / 郑州商品交易所）。

## 细节

### 五所数据入口

| 交易所 | 数据栏目 | 状态 |
|---|---|---|
| 中金所 CFFEX | `/cn/scsj.html`（日/周/月统计、历史下载 `/cn/lssjxz.html`） | ✅ CSV 直链 |
| 上期所 SHFE | `/reports/tradedata/`（日周数据 / 月年数据 / 数据下载） | ⚠️ SPA，旧 `.dat` 失效 |
| 广期所 GFEX | `/gfex/hqsj/…`（日行情、日成交持仓排名、仓单日报、周/月行情） | ⚠️ 页面需浏览器 |
| 大商所 DCE | — | ❌ 412 |
| 郑商所 CZCE | — | ❌ 412 |

- 上期所 `query_params`：`kx` 日交易快讯 / `pm` 日交易排名 / `js_f` 每日结算参数 / `dailystock` 仓单日报 / `timeprice` 日间均价。
- 中金所路径模板：日行情 `rtj/YYYYMM/DD/YYYYMMDD_1.csv`；周/月统计见 `/cn/ztj.html`、`/cn/ytj.html`；交割数据 `/cn/jgsjtj.html`。

## 坑

1. **GBK 编码**：中金所 CSV 是 GBK，读入要 `encoding='gbk'`（或 `gb18030`），否则表头乱码。
2. **上期所改版为 SPA**：`www.shfe.com.cn/data/dailydata/…dat` 旧直链 `404`，`tsite.shfe.com.cn` 已不可达；取数改走页面内 JS 接口（需浏览器抓包）。
3. **大商所/郑商所被 WAF 拦**：`412`（郑商所）与 TLS 握手失败（大商所）——curl 硬刷无效，须真实浏览器；见 `../tools/agent-browser.md`。
4. 日行情非实时（日终/延时），实时行情需交易所**行情授权**；研究用日频数据足够。
5. 与中期协（`cfachina.org.md`）分工：全市场月度成交额看中期协 JSON；**逐合约日行情/持仓/仓单**看本卡交易所源。
