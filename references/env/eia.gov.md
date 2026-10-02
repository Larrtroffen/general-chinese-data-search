# eia.gov —— 美国与国际能源 API

- 去哪找：开放数据门户 `https://www.eia.gov/opendata/`；**API v2 根** `https://api.eia.gov/v2/`；注册取 key `https://www.eia.gov/opendata/register.php`；批量文件 `https://www.eia.gov/opendata/bulkfiles.php`。
- 什么时候用：要**免费、可脚本**的能源时间序列——美国石油/天然气/电力/煤炭/可再生能源价格与产量，以及 **EIA 国际能源数据**（各国一次能源、发电、CO₂ 排放）；做能源市场、跨国能源结构、与中国能源数据对标。
- 怎么搜：全部 GET，返回 JSON，`api_key` 为查询参数：
  ```bash
  # 无 key → 明确报错，可用于探活
  curl -sS 'https://api.eia.gov/v2/'                       # 403 {"error":{"code":"API_KEY_MISSING",...}}
  # DEMO_KEY 可直接试通（限流）
  curl -sS -g 'https://api.eia.gov/v2/petroleum/pri/spt/data/?frequency=monthly&api_key=DEMO_KEY' | head -c 300
  ```
  常用参数：`frequency=monthly|annual`、`data[0]=value`、`facets[series][]=<序列码>`、`start=`/`end=`、`length=`、`offset=`；返回 `{"response":{"total":…,"data":[…]}}`。注意 URL 里的 `[]` 要用 `curl -g` 关闭 glob。
- 覆盖：美国全能源系列（1970s–至今，月/年）+ 国际能源（Annual Energy Outlook / International，年）；粒度到州/部门/品种；另有 bulk 文件（zip/csv）。
- 门槛：**免费**（注册取个人 key；`DEMO_KEY` 可临时用但限流）。
- 实测：2026-10-03，macOS arm64，curl 8.x——`https://api.eia.gov/v2/` → **403** `application/json`，`{"error":{"code":"API_KEY_MISSING","message":"…register for one at …/register.php"}}`；`https://api.eia.gov/v2/petroleum/pri/spt/data/?frequency=monthly&api_key=DEMO_KEY` → **200**，`application/json`，1,274,032 B，`{"response":{"total":"4387",…}}`；`https://www.eia.gov/opendata/` → 200（72,064 B）。
- 上游：U.S. Energy Information Administration（美国能源部统计机构）。

## 细节

- v2 路径结构：`/v2/<领域>/<数据族>/<子项>/data/`，例如 `/v2/petroleum/pri/spt/data/`、`/v2/electricity/retail-sales/data/`、`/v2/international/data/`；领域与序列码可在门户的「API」页用浏览器浏览。
- 路线与序列码检索：门户 `https://www.eia.gov/opendata/browser/`（浏览器）；批量历史可走 bulkfiles 的 zip。

## 坑

1. v2 需要 `api_key`；**无 key 一律 403**（错误码 `API_KEY_MISSING`），别误判为站点故障。`DEMO_KEY` 能用但限流，正式用请自行注册。
2. URL 含 `[]`，`curl` 默认把方括号当 glob 会失败（本机见到 `000` 无输出）；加 `-g`。
3. `total` 是字符串，`data` 数组默认只回一页，长序列要配 `length`/`offset` 分页。
4. 美国之外的部分国家数据来自 EIA 汇编，**更新滞后**于各国官方（如中国数据不如 [`nea.gov.cn.md`](nea.gov.cn.md) 及时），跨国对比注意年份口径。
5. 门户 `eia.gov` 偶发 Cloudflare 挑战（本机个别请求出现 `Just a moment...`），但 `api.eia.gov` 稳定返 JSON。
