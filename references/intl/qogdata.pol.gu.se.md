# qogdata.pol.gu.se —— QoG 政府质量标准数据集

- 去哪找：门户 `https://www.qogdata.pol.gu.se/`；数据目录 `https://www.qogdata.pol.gu.se/data/`；**标准时间序列直链** `https://www.qogdata.pol.gu.se/data/qog_std_ts_jan25.csv`。
- 什么时候用：要**一次性拿到上千个已清洗、已对齐的跨国治理/政治/社会变量**（含 Freedom House、Polity、V-Dem、WGI、CPI、PTS 等的派生列）；"先广撒网再挑变量"的探索阶段；省去逐库对齐与合并。
- 怎么取：
  ```bash
  # 标准时间序列整表直下（无需注册）
  curl -sLO 'https://www.qogdata.pol.gu.se/data/qog_std_ts_jan25.csv'
  # 同一目录还有交叉截面/基础版/专家版，如 qog_std_cs_jan25.csv、qog_bas_ts_jan25.csv、qog_std_ts_jan25.dta
  ```
  - 三个 ID 列：`cname`（国名）、`ccodecow`（COW 码）、`ccodealp`（ISO3）、`ccodealp_year`（含年际更名的 alpha 码）；列名前缀即原始来源。
- 覆盖：`qog_std_ts_jan25` 为 2025-01 版，覆盖 ~200 国家/地区，年度；每年 1 月更新一版（上游声明，未本机实测）。
- 门槛：免费、**无注册、无 key**。
- 实测：2026-10-03，macOS arm64，curl 8.x：`https://www.qogdata.pol.gu.se/data/qog_std_ts_jan25.csv` → **200 / 61.5 MB**（7.6 s）；表头实测含 `cname_qog,cname,year,ccodecow,ccodealp,ccodealp_year,ccode_qog,cname_year,ccode,aid_cpnc,aii_acc,…`，并实测含 Freedom House 变量 `fh_cl,fh_pr,fh_status,fh_rol,fh_aor,fh_ep,fh_fog,fh_pair,fh_ppp,fh_feb`。
- 上游：Quality of Government Institute, University of Gothenburg `https://www.qogdata.pol.gu.se/`。

## 细节

### 为什么值得单独收一张卡

它是"**变量超市**"：一张表里同时有 Freedom House、Polity、V-Dem、世行 WGI、透明国际 CPI、PTS 恐怖主义、AidData 援助、CIRI 人权等。当你要回答"某治理概念有哪些现成度量"时，先 grep 它的表头，比自己逐个库找快一个数量级。**但其值是二次转引**，正式分析回原库核对。

## 坑

1. 文件极大（61 MB、上万列），Excel 打不开；pandas 用 `usecols=` 只读所需列。
2. 版本号绑在文件名（`jan25`）；换版要重核列名——变量会增删改名。
3. 同一概念**常有多列**（不同来源/口径/年份），务必读官方 codebook 的变量来源表再选，别按名字猜。
4. 做面板优先用 `ccodealp_year`（处理了更名/分裂），而非 `ccodealp`。
5. 二次转引可能有版本滞后；关键数字回原机构核。
