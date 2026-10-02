# tw-statistics —— 台湾主计总处与政府资料开放平台

- 去哪找：
  - **中华民国统计资讯网 / 行政院主计总处** `https://www.stat.gov.tw/`——统计资料查询 `https://www.stat.gov.tw/cl.aspx?n=3563`、主计总处查询系统 `…/cl.aspx?n=3654`；**统计年鉴** `https://www.stat.gov.tw/News.aspx?n=3093&sms=11160`
  - **总体统计资料库** `https://nstatdb.dgbas.gov.tw/dgbasall/webMain.aspx?sys=100&funid=defjsp`；**县市指标查询系统** `https://winstacity.dgbas.gov.tw/DgbasWeb/ZWeb/StateFile_ZWeb.aspx`
  - **政府资料开放平台（data.gov.tw）** `https://data.gov.tw/`——**目录检索 API** `POST https://data.gov.tw/api/front/dataset/list`、**全库目录 CSV** `https://data.gov.tw/api/front/dataset/export?format=csv`、**Open Data API v2** `POST https://data.gov.tw/api/v2/rest/dataset`（需 key）
- 什么时候用：要台湾官方口径的**经济成长率／CPI／失业率／薪资／工业生产／外销订单／进出口／人口**等重要经社指标；要**按指标/期间查询的时间序列**（总体统计资料库）；要**县市层级指标**；要台湾各部会**开放数据集清单与下载链**；写台湾经济、两岸贸易、产业分析时。
- 怎么搜：**数值**走「总体统计资料库」（网页查询 + CSV/Excel 导出，见坑 1）；**目录/元数据**走 data.gov.tw 的 `api/front/dataset/list`（POST JSON）；**批量目录**直接下 CSV。结果形态：data.gov.tw = **JSON** 与 **CSV**；主计总处 = **HTML 表格 + CSV/Excel 导出**（网页渲染）。
- 覆盖：data.gov.tw 目录检索 `search_count` 约 **5.2 万**条资源，覆盖中央与地方机关（含主计总处、内政部、经济部、央行等），字段含机关、服务分类、更新频率、格式、下载网址。主计总处总体统计资料库覆盖物价、国民所得、就业失业、薪资生产力、家庭收支、社会指标、普查等；统计年鉴按年出版。
- 门槛：data.gov.tw 的**前端检索 API 与目录 CSV 免 key、免登录**；`api/v2/rest/dataset` **需申请 API Key**（`Authorization` 头）。主计总处站点免费但**有 Cloudflare 人机校验，需真实浏览器**（见坑 1）。
- 实测：2026-10-03，macOS arm64：
  - `curl` 桌面 UA：`https://data.gov.tw/` → `200/240105`；`GET https://data.gov.tw/api/front/dataset/export?format=csv` → `200` `text/html; charset=UTF-8`，`13948406` 字节 CSV（**UTF-8 BOM**，表头「資料集識別碼,資料集名稱,資料提供屬性,服務分類,品質檢測,檔案格式,資料下載網址,編碼格式,…」）✅
  - `POST https://data.gov.tw/api/front/dataset/list`，体 `{"q":"人口","page":1,"size":2}` → `200 application/json`，`{"success":true,"code":200,"payload":{"search_count":52442,"search_result":[{"agency_name":"地政司","category_name":"公共資訊","charge":"免費","check_freq_name":"每日","changed":{…},…}]}}` ✅；同端点 **GET → 405**（`allow: POST`）
  - `POST https://data.gov.tw/api/v2/rest/dataset`（体 `{"q":"人口"}`）→ `200` 但 `{"success":false,"error":{"error_type":"ER0001:API Key錯誤","message":"…HTTP 標頭沒設定 Authorization Key"}}`；`GET` → `405` ⚠️
  - `https://www.stat.gov.tw/` `curl` → `403` Cloudflare `Just a moment...`；`http://` 同 `403`；reader 取数 `HTTP 403` ⚠️；**无头 Chromium 打开 → 正常渲染**，标题《中華民國統計資訊網》，页内链出 `n=3563`（統計資料查詢）、`n=3654`（主計總處查詢系統）、`n=3442`（總體統計資料庫）、`n=3093`（統計年鑑）✅
  - `https://nstatdb.dgbas.gov.tw/dgbasall/webMain.aspx?sys=100&funid=defjsp` 浏览器打开 → 标题《總體統計資料庫》，含「單表查詢／跨表查詢／視覺圖」✅；`https://statdb.dgbas.gov.tw/pxweb/Dialog/statfile9.asp` → 浏览器 `ERR_CONNECTION_CLOSED`、curl `000` ❌（该 PX-Web 主机本机不可用）
  - `https://www.dgbas.gov.tw/`、`https://ebook.dgbas.gov.tw/` → `403` Cloudflare ⚠️
- 上游：行政院主計總處 `dgbas.gov.tw` / 中華民國統計資訊網 `stat.gov.tw` / `nstatdb.dgbas.gov.tw` / `winstacity.dgbas.gov.tw`；政府資料開放平臺 `data.gov.tw`。

## 细节

### 一、data.gov.tw（政府资料开放平台）

| 用途 | 端点 | 方法 | 关键参数/体 | 实测 |
|---|---|---|---|---|
| 目录检索 | `https://data.gov.tw/api/front/dataset/list` | POST | JSON：`{"q":"关键词","page":1,"size":N}`；返回 `payload.search_count` + `payload.search_result[]` | ✅ 200 JSON，免 key |
| 全库目录 | `https://data.gov.tw/api/front/dataset/export?format=csv` | GET | `format=csv` | ✅ 200，约 13.9 MB CSV |
| Open Data API v2 | `https://data.gov.tw/api/v2/rest/dataset` | POST | 需 `Authorization`（API Key） | ⚠️ 无 key 报 `ER0001:API Key錯誤` |

```bash
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
# 1) 关键词检索数据集（POST，免 key）
curl -s -A "$UA" -X POST -H 'Content-Type: application/json' \
  -d '{"q":"人口","page":1,"size":10}' 'https://data.gov.tw/api/front/dataset/list'
# 2) 一次拿全库目录（CSV，含下载网址）
curl -s -A "$UA" 'https://data.gov.tw/api/front/dataset/export?format=csv' -o data.gov.tw.csv
```

- `search_result[]` 常用字段：`agency_name`（机关）、`category_name`/`category_dataset_name`（分类）、`changed`（更新时点）、`charge`（免费/付费）、`check_freq_name`（更新频率）、`content`（描述）、下载资源信息。
- 数据集详情页 `https://data.gov.tw/dataset/{id}`；机关浏览 `https://data.gov.tw/datasets/...`。

### 二、主计总处与中华民国统计资讯网

| 用途 | 入口 | 形态 |
|---|---|---|
| 统计资讯网主站 | `https://www.stat.gov.tw/` | HTML（**Cloudflare 校验，需浏览器**） |
| 统计资料查询 | `https://www.stat.gov.tw/cl.aspx?n=3563` | 目录页 |
| **总体统计资料库** | `https://nstatdb.dgbas.gov.tw/dgbasall/webMain.aspx?sys=100&funid=defjsp` | 单表/跨表查询，可导出 CSV/Excel |
| 县市指标查询系统 | `https://winstacity.dgbas.gov.tw/DgbasWeb/ZWeb/StateFile_ZWeb.aspx` | 县市层级指标 |
| 统计年鉴 | `https://www.stat.gov.tw/News.aspx?n=3093&sms=11160` | 按年 PDF/网页 |
| 統計調查查詢 | `https://enterprise.dgbas.gov.tw/STATSVY/manager/indexn.jsp` | 调查名录 |

- 旧 PX-Web 入口 `https://statdb.dgbas.gov.tw/pxweb2007/Dialog/statfile9.asp` **本机不可达**（见坑 2），现行为 `nstatdb.dgbas.gov.tw` 的 webMain 应用。

## 坑

1. **主计总处主站全系被 Cloudflare 拦**：`www.stat.gov.tw`、`www.dgbas.gov.tw`、`ebook.dgbas.gov.tw`、`statdb.dgbas.gov.tw` 用 `curl`/reader 均 `403 Just a moment...`（换 HTTP 亦同），**只能真实/无头浏览器**打开；写脚本抓取须用带 JS 引擎的客户端，或改用 data.gov.tw（同一机关数据集多以开放格式托管于此）。
2. **`statdb.dgbas.gov.tw` 主机本机连接被断开**（浏览器 `ERR_CONNECTION_CLOSED`、curl `000`），旧 PX-Web 深链不要用；统计资料库改走 `nstatdb.dgbas.gov.tw/dgbasall/webMain.aspx`。
3. **data.gov.tw 前端 API 与 v2 API 是两套**：前端 `/api/front/...` 免 key（但多为 **POST**，GET 报 405）；正式 `/api/v2/rest/dataset` 必须 `Authorization` API Key（需注册申请），无 key 会以 `success:false` + `ER0001` 返回而**不是** 401/403。
4. **目录 CSV 体量大**（约 13.9 MB），且以 `text/html` 类型返回（实际 CSV，带 UTF-8 BOM），解析时须按 BOM+逗号处理，勿以 `Content-Type` 判断。
5. **`search_count` 是资源计数而非去重数据集数**：关键词检索命中数会显著大于实际数据集条数，引用时勿直接当「数据集总量」。
6. 数据来自各部会，**口径/更新频率不一**；跨数据集比较前先看 `check_freq_name` 与 `changed`，数值类指标优先回主计总处总体统计资料库核对。
