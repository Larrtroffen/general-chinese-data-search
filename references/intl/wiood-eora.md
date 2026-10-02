# wiood-eora —— 全球投入产出与价值链数据

- 去哪找：**WIOD**（格罗宁根 GGDC）`https://www.rug.nl/ggdc/valuechain/wiod/`，2016 版页 `…/wiod-2016-release`，文件托管在 DataverseNL `https://dataverse.nl/dataverse/GGDC`；**Eora** `https://worldmrio.com/`（Eora26 `…/eora26/`；Eora2 见 `https://eora.org`）；**EXIOBASE** `https://exiobase.eu/`（数据发布在 Zenodo，站内指向 `https://zenodo.org/records/15689391`）；**ADB MRIO** `https://kidb.adb.org/globalization/current`（现值）/`…/globalization/constant`（不变价）；**OECD TiVA** 见同层 `oecd.org.md`（门户 `https://data-explorer.oecd.org/`）。
- 什么时候用：要全球/区域**投入产出表（ICIO / MRIO）**、增加值贸易（TiVA）、全球价值链（GVC）分解、隐含碳/资源足迹；按「国家 × 部门 × 最终使用」做 Leontief、SDA、贸易增加值分解。
- 怎么取：这几家都是**打包文件下载**（Excel / R / Stata / zip），不是检索接口；文件 id/版本随发布变化，先从落地页解析再下。
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # ① WIOD 2016：DataverseNL 直链（文件 id 见「细节」表）
  curl -sLO -A "$UA" 'https://dataverse.nl/api/access/datafile/199104'   # WIOT Tables Excel
  curl -sLO -A "$UA" 'https://dataverse.nl/api/access/datafile/199103'   # WIOT Tables Stata
  # ② ADB MRIO：id 从 /globalization/current 页的 mrio-file 链接解析
  curl -sLO -A "$UA" 'https://kidb.adb.org/download/mrio-file/5'         # ADB-MRIO-2007.xlsx
  # ③ Eora26：站点「Download Data」→ 需登录（/login.jsp）
  # ④ EXIOBASE：Zenodo 记录页取 zip（本机被 403 拦，见「坑」）
  ```
  结果形态：xlsx / zip / `.dta` / `.RData`；WIOD·ADB·EXIOBASE 直链，Eora 需注册登录。
- 覆盖：WIOD 2016 版页载「28 个 EU 国 + 15 个主要国家、2000–2014」；Eora26 免费学术版 **1990–2017**（许可页所载，见「细节」）；ADB MRIO 提供 62/72 经济体版本（kidb 页所载），2025 版更新至约 2023–2024（上游声明）；EXIOBASE 覆盖/部门以 Zenodo 记录页为准（本机 403，未核）。
- 门槛：**WIOD / ADB MRIO / EXIOBASE / OECD TiVA 免费直下**；**Eora26 免费仅限学术**（须注册登录，商业用途到 `https://worldmrio.com/store/` 购买）；GTAP 等商业 IO 库需付费授权（不在本卡）。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA、`-L`、20 s）——`rug.nl/ggdc/valuechain/wiod/` `200/42,790 B`；`…/wiod-2016-release` `200/49,352 B`，页内 DataverseNL 直链 `dataverse.nl/api/access/datafile/199087–199104`（见「细节」）。`dataverse.nl/api/access/datafile/199104` → **200 但为「Making sure you're not a bot!」拦截页**（本机 curl 未过 bot 校验；链接结构有效）。`worldmrio.com/` `200/24,594 B`、`/eora26/` `200/25,623 B`，下载入口 `…/login.jsp`；`/licensing.jsp` 明示「1990–2017 学术免费 / academic use」。`exiobase.eu/` `200/41,693 B`（仅指向 Zenodo，无自托管直链）；`zenodo.org/records/15689391` → **403**。`kidb.adb.org/globalization/current` `200/94,568 B`；`kidb.adb.org/download/mrio-file/5` → `206 application/xlsx`（`ADB-MRIO-2007.xlsx`）。❌ `mrio.adbx.online` **NXDOMAIN**（旧入口已下线）；`www.adb.org`、`data.adb.org` → **403 Cloudflare**。OECD：`sdmx.oecd.org/public/rest/v1/dataflow/all?format=json-structure-2.0.0` `200`（命中 5 条 `OECD.STI.PIE` TiVA 2025 数据流），但数据端点本机 `500/403`（见「坑」6）。
- 上游：WIOD `https://www.rug.nl/ggdc/valuechain/wiod/`（Groningen Growth and Development Centre）；Eora `https://worldmrio.com/`；EXIOBASE `https://exiobase.eu/`；ADB MRIO `https://kidb.adb.org/globalization/current`；OECD TiVA 见 `oecd.org.md`。

## 细节

### 各库入口与文件规律（2026-10-03 实测）

| 库 | 入口 | 取数方式 |
|---|---|---|
| WIOD 2016 | `https://www.rug.nl/ggdc/valuechain/wiod/wiod-2016-release` | DataverseNL `api/access/datafile/{id}` 直链 |
| Eora26 | `https://worldmrio.com/eora26/` | 交互页「Download Data」→ 登录后下载；学术免费 |
| EXIOBASE | `https://exiobase.eu/` | 指向 Zenodo 记录页（zip） |
| ADB MRIO | `https://kidb.adb.org/globalization/current`、`…/constant` | `https://kidb.adb.org/download/mrio-file/{id}` → xlsx |
| OECD TiVA | `https://data-explorer.oecd.org/`（SDMX 见 `oecd.org.md`） | SDMX REST / data-explorer 导出 |

### WIOD 2016 DataverseNL 文件 id（从 2016 版页解析所得）

| id | 内容 |
|---|---|
| 199104 / 199103 / 199101 | WIOT Tables —— Excel / Stata / R |
| 199088 | WIOD Socio-Economic Accounts 2016 |
| 199087 | Note on the Construction of WIOTs in Previous Year's Prices |
| 199095–199102 | 各国 SUT / 投入数据 / 汇率等 Excel 附表 |

- 数据集 DOI 前缀 `doi:10.34894/…`，Dataverse 集合页 `https://dataverse.nl/dataverse/GGDC`；**文件 id 会随重发变，务必回 2016 版页重解析**。

### ADB MRIO / kidb

- 落地页 `/globalization/current` 的 HTML 里内嵌一个 JSON（`href`、`filename`、`historical_year`、`file_update_date`），逐个 `download/mrio-file/{id}` 即为 xlsx；另有 SDMX 端点 `kidb.adb.org/api/v3/sdmx/data/…`（本机对示例 `EO_NA/A.NGDP_XDC.PHI` 返回 404，未打通）。

### Eora26 许可要点（`/licensing.jsp`）

- 免费学术范围 = 在校学生/教研人员、用于课程作业或同行评审论文；**不得转载超过 200 条原始数据**；>2017 年数据、商业用途走 store 购买，Eora2 联系 `info@worldmrio.com`。

## 坑

1. **旧入口全部失效**：`http://www.wiod.org/...` 301 到 `rug.nl` 同名页；ADB 旧站 `mrio.adbx.online` 已 **NXDOMAIN**；别再按教程里的旧 URL 拼。
2. **`adb.org` / `data.adb.org` 本机 403（Cloudflare）**：ADB MRIO 数据改从 `kidb.adb.org` 取；不要把 403 当成数据下线。
3. **DataverseNL 有 bot 校验**：本机 curl 直下 `datafile/{id}` 会拿到拦截页（页面标题 `Making sure you're not a bot!`），需浏览器过验证或换网络；链接本身有效。
4. **Zenodo 本机 403**：EXIOBASE 的唯一官方分发在 Zenodo，本机被拦；换网络/浏览器可下，或查论文附件镜像。
5. **Eora 需注册登录**，`data-id`/文件名拼不出直链；Eora26 与 Eora1/Eora2 是不同产品，引用要写清版本与年份上限（免费版止于 2017）。
6. **OECD TiVA 2025 数据流本机取不到数**：`sdmx.oecd.org/public/rest/v1/dataflow/all?format=json-structure-2.0.0` 能列出 `OECD.STI.PIE,DSD_TIVA_MAINLV@DF_MAINLV,1.1`（等 5 条，维度序 `MEASURE.REF_AREA.ACTIVITY.COUNTERPART_AREA.UNIT_MEASURE.FREQ`），但 `/public/rest/…/data/…` 返回 **500**、`/sti-public/…/data/…` 返回 **403**，且 data-explorer 的 TiVA 页当时也报「something went wrong」（2026-10-03）——疑上游临时状态；取数方法仍按 `oecd.org.md`。
7. **单位/价格口径**：WIOD·ADB 有现值（current）与不变价（constant）两套；ADB 不变价以 2010 年为基（kidb 页）；引用前确认价格基年与货币单位。
8. 各库「国家数 × 部门数」差异大（WIOD 43×56、Eora26 189×26、ADB 62/72、EXIOBASE 分区域版），**跨库合并先做部门/国家 concordance**，不能直接对齐。
