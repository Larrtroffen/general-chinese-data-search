# europeansocialsurvey.org —— 欧洲社会调查

- 去哪找：门户 `https://www.europeansocialsurvey.org/`；数据页 `https://www.europeansocialsurvey.org/data`；**数据门户（SPA）** `https://ess.sikt.no/`；API 文档 `https://api.ess.sikt.no/docs`。
- 什么时候用：要**严格概率抽样、高质量翻译协议**的欧洲跨国态度/行为数据（政治信任、移民、福利、气候变化、健康、媒体使用、工作）；做欧洲跨国比较、方法学标杆。
- 怎么取：
  ```bash
  # 数据门户是 SPA，前端 env 指向后端；后端 REST + 独立 GraphQL
  curl -s 'https://ess.sikt.no/env.js'      # → VITE_API_URL='https://api.nsd.no/graphql'
  curl -s 'https://api.ess.sikt.no/'        # → {"status":"ok","serviceName":"ess-api"}
  curl -s 'https://api.ess.sikt.no/docs'    # → Redoc "ESS API Documentation"
  ```
  - 常规路径：`ess.sikt.no` 检索/浏览数据集 → 注册账号、接受条款 → 下载 SPSS/Stata/CSV。
  - 程序化：`api.ess.sikt.no`（REST，端点名见 `/docs`）+ `https://api.nsd.no/graphql`（POST）。
- 覆盖：2002–至今（Round 1–11+），约 30–40 个欧洲国家；个体级；两年一轮（上游声明，未本机实测）。
- 门槛：**注册（免费）后下载**；限学术/非商业用途并须按规范引用。
- 实测：2026-10-03，macOS arm64，curl 8.x：`https://www.europeansocialsurvey.org/data` → 200 / 127 KB；`https://ess.sikt.no/en/` → 200（SPA）；`https://api.ess.sikt.no/` → 200 `{"status":"ok","serviceName":"ess-api","serviceVersion":"8115374d"}`；`/docs` → 200（Redoc）；`/studies`、`/swagger` → **404**；`https://api.nsd.no/graphql` GET → 405、POST introspection `{__schema{queryType{name}}}` → 200。
- 上游：`https://www.europeansocialsurvey.org/`（ESS ERIC）；数据档案 NSD/Sikt。

## 坑

1. 官网数据页只是导航，**实体在 `ess.sikt.no`（SPA）**；curl 抓不到数据集列表，需浏览器或用 `api.ess.sikt.no` / NSD GraphQL。
2. REST 端点名未公开列出（`/studies` 404）；先读 `api.ess.sikt.no/docs`。
3. 下载需注册 + 学术用途声明，再分发受条款限制。
4. 国家覆盖是**轮次制**，某国缺席某轮很常见；别假设 30 国 × 11 轮齐整。
5. 变量在轮次间会修订（如移民模块改版），跨轮合并读官方 codebook。
