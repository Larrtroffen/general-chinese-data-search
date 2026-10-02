# data.stats.gov.cn —— 国家数据指标数值 API

- 去哪找：接口基址 `BASE = https://data.stats.gov.cn/dg/website/publicrelease/web/external/`；前端 `https://data.stats.gov.cn/dg/website/page.html#/pc/national/home`；旧接口 `https://data.stats.gov.cn/easyquery.htm?cn=A01`（**已 403，勿用**）。
- 什么时候用：要抓**分省/全国/主要城市**的月度、季度、年度指标数值（GDP、CPI、人口…），是省市经济数据最省事的通道。
- 怎么搜：**新接口 4 步**（根目录 → 逐级下钻到 leaf 得 `cid` → `queryIndicatorsByCid` 取 `indicatorId` → `POST stream/esData` 取数），详见下「取数流程」。
  ```bash
  BASE='https://data.stats.gov.cn/dg/website/publicrelease/web/external'
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'

  # ① 拿根目录 id（code=6 分省年度）
  curl -s -A "$UA" "$BASE/new/queryIndexTreeAsync?pid=&code=6"
  # → data[0]._id = c4d82af16c3d4f0cb4f09d4af7d5888e  (分省年度数据)
  ```
- 覆盖：库码 `code=1…14`（月度/季度/年度/分省/主要城市/港澳台/国际…，见下）；粒度=指标×地区×月/季/年。
- 门槛：免费，无需登录；新接口**不校验 Referer/Origin/Cookie**（实测不带 Referer 直接 POST 也通），UA 用桌面 Chrome 即可。
- 实测：2026-10-02，macOS（arm64），curl 8.x：`easyquery.htm` 403（UrlACL）；`queryIndexTreeAsync` code=1–14 逐一探明库码；`stream/esData` 取到北京 GDP 五整年（44350.7 → 52073.4 亿元），并核对新 SPA 前端实际发出的 `dts`/`das` 格式（浏览器捕获）。
- 上游：国家统计局「国家数据」`https://data.stats.gov.cn/`。

## 细节

### 现状（本机实测）

2024 年前后网站改版：**旧 `easyquery.htm` 接口已被 WAF 封禁**（本项目自 2026-10-02 实测）。

| 路径 | 状态 | 现象 |
|---|---|---|
| `https://data.stats.gov.cn/` | ✅ 302 | → `/dg/website/page.html#/pc/national/home`（新 SPA） |
| `https://data.stats.gov.cn/easyquery.htm?cn=A01` | ❌ 403 | 403 页含 `reason:UrlACL`、`Client IP: …`；带 Referer/UA 仍 403 |
| `http://data.stats.gov.cn/easyquery.htm?...` | ❌ 301→403 | 301 跳 https 后 403 |
| `https://data.stats.gov.cn/dg/website/page.html` | ✅ 200 | 新前端（Vue「dsf」平台） |
| `https://data.stats.gov.cn/dg/website/publicrelease/web/external/new/queryIndexTreeAsync?pid=&code=6` | ✅ 200 | 返回 JSON，指标树 |

**结论：不要再用 easyquery.htm，改用新接口。**

### 接口基址

```
BASE = https://data.stats.gov.cn/dg/website/publicrelease/web/external/
```

### 可用性矩阵

| 接口 | 方法 | 用途 | 现象 |
|---|---|---|---|
| `new/queryIndexTreeAsync?pid={父id}&code={库码}` | GET | 指标分类树（逐级下钻） | ✅ 200 JSON |
| `new/queryIndicatorsByCid?cid={cid}&dt={年段}&name=` | GET | 取某分类下的指标清单（含 indicatorId） | ✅ 200 JSON |
| `getDaCatalogTreeByIndicatorCid?indicatorCid={cid}` | GET | 地区（DA）维度树 | ✅ 200 JSON |
| `getDasByDaCatalogId?daCid={id}` | GET | 地区清单（省/市 + 12 位代码） | ✅ 200 JSON |
| `stream/esData` | POST | **取数主接口**（JSON body） | ✅ 200 JSON |
| `queryAllPblIbs?type=year\|month\|session` | GET | 统计出版物（年报/月报/季报）书目 | ✅ 200 JSON |
| `new/queryCMSArticles?code=zxfb&pagenum=1&pageSize=10` | GET | 最新发布（新闻稿） | ✅ 200 JSON |
| `queryAgendaByDate?startDate=…&endDate=…` | GET | 数据发布日程 | ✅ 200 JSON |

### 库码 `code` 含义（`queryIndexTreeAsync?pid=&code=N` 实测）

```
1  月度数据        2  季度数据        3  年度数据
4  分省月度数据     5  分省季度数据     6  分省年度数据
7  主要城市月度价格  8  主要城市年度数据
9  港澳台月度数据   10 港澳台年度数据
11 （空，未返回）    12 三大经济体月度数据
13 国际市场月度商品价格  14 主要国家年度数据
```

### 取数流程（4 步）

以「分省年度数据 → 国民经济核算 → 地区生产总值 → 北京市 2021–2025」为例：

```bash
BASE='https://data.stats.gov.cn/dg/website/publicrelease/web/external'
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'

# ① 拿根目录 id（code=6 分省年度）
curl -s -A "$UA" "$BASE/new/queryIndexTreeAsync?pid=&code=6"
# → data[0]._id = c4d82af16c3d4f0cb4f09d4af7d5888e  (分省年度数据)

# ② 逐级下钻，直到节点 type=catalog 且 isLeaf=true（该节点 _id 即 cid）
curl -s -A "$UA" "$BASE/new/queryIndexTreeAsync?pid=c4d82af16c3d4f0cb4f09d4af7d5888e&code=6"
# → 国民经济核算 da5ccb68e9de4671ad967247fe427c91
curl -s -A "$UA" "$BASE/new/queryIndexTreeAsync?pid=da5ccb68e9de4671ad967247fe427c91&code=6"
# → 地区生产总值 6f8fbd415cbc40ffa7ecb7fd917f2598 (isLeaf=true) → 这就是 cid

# ③ 取指标清单
curl -s -A "$UA" "$BASE/new/queryIndicatorsByCid?cid=6f8fbd415cbc40ffa7ecb7fd917f2598&dt=2021-2025&name="
# → data.list[]._id 即 indicatorId；d 段用 2021-2025（年度）/ 2025-2026（月度）

# ④ 取数
curl -s -A "$UA" -H 'Content-Type: application/json' -X POST \
  --data-binary '{"cid":"6f8fbd415cbc40ffa7ecb7fd917f2598",
   "indicatorIds":["aff57de5ee994283974705914fbed246","615ce248396a4a5fa52bca05f0633e95"],
   "daCatalogId":"","das":[{"text":"北京市","value":"110000000000"}],
   "showType":"1","dts":["2021YY-2025YY"],
   "rootId":"c4d82af16c3d4f0cb4f09d4af7d5888e"}' \
  "$BASE/stream/esData"
```

### `stream/esData` 请求体字段

| 字段 | 说明 |
|---|---|
| `cid` | 指标分类 id（第②步的 cid，与 `queryIndicatorsByCid` 的 cid 同值） |
| `indicatorIds` | 指标 id 数组，取自 `queryIndicatorsByCid` 的 `list[]._id` |
| `daCatalogId` | 地区维度分类 id，直接给空串即可 |
| `das` | 地区数组：`[{"text":"北京市","value":"110000000000"}]`，`value` 为 **12 位补零**区划码（北京 `110000000000`、石家庄 `130100000000`） |
| `showType` | 固定 `"1"` |
| `dts` | 时间区间数组：年度 `"2021YY-2025YY"`；月度 `"202509MM-202609MM"`（实测两种格式） |
| `rootId` | 该库根目录 id（第①步） |

### 返回字段路径

```
data[]                      每个时间点一块
  .code        如 "2025YY" / "202509MM"
  .name        如 "2025年"
  .values[]    指标值列表
     ._id          indicatorId
     .i_showname   指标名（如 "地区生产总值 (亿元) "）
     .value        数值（字符串，可能为空串）
     .du_name      单位（"亿元"）
     .da / .da_name  地区码 / 地区名
```

**实测样例（北京市地区生产总值，亿元）**：2021 `44350.7`、2022 `45222.4`、2023 `47353.7`、2024 `49670.2`、2025 `52073.4`。

### 地区清单怎么拿

```bash
# 分省：全部地区
curl -s -A "$UA" "$BASE/getDaCatalogTreeByIndicatorCid?indicatorCid=6f8fbd415cbc40ffa7ecb7fd917f2598"
# → data[]._id；其中「全部地区」= a10dceae75d245008bf4b9a0e6fe1d55
curl -s -A "$UA" "$BASE/getDasByDaCatalogId?daCid=a10dceae75d245008bf4b9a0e6fe1d55"
# → data[].name_value(12位码) / show_name(北京市)

# 主要城市（code=8）：daCid = 5772e42228f948149cf5d6a11d07bce1，北京=110000000000
curl -s -A "$UA" "$BASE/getDasByDaCatalogId?daCid=5772e42228f948149cf5d6a11d07bce1"
```

## 坑

1. **旧 `easyquery.htm` 全站 403（UrlACL）**，网上大量教程失效；本文件所述新接口是唯一可用路径。
2. `pid=` 为空时返回的是**根节点数组**（层数因库而异）；一定要用返回的 `_id` 继续下钻，不要凭空拼 id。
3. `queryIndexTreeAsync` 的 `code` 必须与目标库一致（用 code=6 却传 code=3 的 id 会返回空 `data`）。
4. `dt` 参数只影响指标清单的年份过滤（年度 `2021-2025`、月度 `2025-2026`），取数时间范围由 `dts` 决定。
5. `value` 为空串 = 该指标该地区该年无值（例如「年度数据」全国库里查北京市本级指标会为空）；**分省数据必须用 code=4/5/6**。
6. 前端是 SPA（`#/pc/national/...`），curl 直接抓页面拿不到数据；但**接口本身是纯 JSON**，可脱离浏览器使用。
7. 礼貌抓取：接口无明确频控，但仍建议 ≤3 请求/秒并串行；批量抓取前先用 1 个指标试跑通流程。
