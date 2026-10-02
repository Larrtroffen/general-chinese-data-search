# comtrade.un.org —— 联合国商品贸易统计

- 去哪找：门户 `https://comtradeplus.un.org/`；**免 key 预览接口** `https://comtradeapi.un.org/public/v1/preview/{type}/{freq}/{clCode}`；参考表 `https://comtradeapi.un.org/files/v1/app/reference/`。
- 什么时候用：要**双边、分商品**的进出口额与数量（HS 编码粒度）；算贸易依存度、贸易战/关税影响、产业链上下游；需要"报告国 × 伙伴国 × 商品 × 流向"四维取数。
- 怎么搜：免费层只有 `public/v1/preview/...`；正式 `/data/v1/get/...` 需订阅 key。
  ```bash
  # ① 免 key 预览：报告国 156(中国) 2022 年 HS 第 85 章进口
  curl -s 'https://comtradeapi.un.org/public/v1/preview/C/A/HS?reporterCode=156&period=2022&cmdCode=85&flowCode=M'
  # ② 免 key 参考表（报告国/伙伴/商品/流向字典）
  curl -s 'https://comtradeapi.un.org/files/v1/app/reference/Reporters.json'
  # ③ 正式接口（无 key → 401）
  #   curl -H 'Ocp-Apim-Subscription-Key: <KEY>' \
  #     'https://comtradeapi.un.org/data/v1/get/C/A/HS?reporterCode=156&period=2022&cmdCode=85&flowCode=M'
  ```
  - 路径骨架 `/{type}/{freq}/{clCode}`：`type`=C(商品)/S(服务)，`freq`=A(年)/M(月)，`clCode`=HS/SITC/BEC/EB02…
  - 常用参数：`reporterCode`（M49 数字码，中国=156）、`partnerCode`（0=世界）、`period`（年或 `YYYYMM`）、`cmdCode`（HS 码，逗号可多值）、`flowCode`（M 进口 / X 出口 / RX 再出口 / RM 再进口）、`customsCode`、`motCode`。
  - 返回 JSON：顶层 `count`，`data[]` 每行含 `refYear/period/reporterCode/flowCode/partnerCode/cmdCode/primaryValue/netWgt/qty` 等。
- 覆盖：年度自 1962 年起、月度视报告国约 2010 年代起；~200 个报告经济体；HS 2/4/6 位 + SITC + BEC；更新到最近申报月份（各国滞后不等）。
- 门槛：**preview 全免**（单次结果有行数上限）；完整接口在 `comtradeplus.un.org` 免费注册取 `subscription-key`（配额以上游为准）。
- 实测：2026-10-03，macOS arm64，curl 8.x：`public/v1/preview/C/A/HS?reporterCode=156&period=2022&cmdCode=85&flowCode=M` → 200 / 181 KB，`count=205`；`files/v1/app/reference/Reporters.json` → 200 / 80 KB；`data/v1/get/C/A/HS?...` 无 key → **401** `Access denied due to missing subscription key`。
- 上游：`https://comtradeplus.un.org/`；开发者门户 `https://comtradedeveloper.un.org/`（上游声明，注册取 key 流程未本机实测）。

## 细节

### 常用 M49 报告国码

| 国家/地区 | 码 | 国家 | 码 |
|---|---|---|---|
| 中国 | 156 | 美国 | 842 |
| 日本 | 392 | 德国 | 276 |
| 印度 | 699 | 越南 | 704 |
| 中国香港 | 344 | 中国台湾（Other Asia, nes） | 490 |

完整表走 `files/v1/app/reference/Reporters.json`（含 `reporterCodeIsoAlpha3`）。

### 参考表清单

`https://comtradeapi.un.org/files/v1/app/reference/` 下：`Reporters.json`、`partnerAreas.json`、`HS.json`、`SITC.json`、`BEC.json`、`flowCodes.json`、`customsCodes.json`、`motCodes.json`。

## 坑

1. `partnerCode=0` 是"世界"合计；与逐伙伴相加口径可能不同，别重复计数。
2. `reporterCode` 是 **M49 数字码**不是 ISO3；`customsCode=C00`（全部海关）、`motCode=0` 为默认值。
3. 台湾在 Comtrade 记为 `490`（Other Asia, nes），与 ISO `TWN` 不同——做面板要手工映射。
4. preview 有结果上限，拉全行业/全伙伴面板会被截断；大批量須申请 key 或用 bulk 文件（上游声明）。
5. `type=S` 服务贸易的国别覆盖远少于货物贸易。
