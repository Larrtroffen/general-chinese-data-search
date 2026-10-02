# mcp-cnbs —— 国家统计局新版 API 的 MCP 服务

一个 Node MCP Server，把 NBS「国家数据」新版 JSON 接口 + 世界银行/IMF/OECD/BIS/FRED + NBS 普查/部委数据统一包成工具。**增量价值：它的 `api_introduce.md` 是中文版《国家统计局新版接口使用文档》，把 UUID/cid/时间分片讲得最透**（我们已有 `data.stats.gov.cn.md` 记端点和流程，这里只补文档级洞见）。

- 去哪找：`https://github.com/icen-ai/mcp-cnbs`；npm 包 `https://www.npmjs.com/package/mcp-cnbs`（v1.3.2）；接口文档 `raw.githubusercontent.com/icen-ai/mcp-cnbs/master/api_introduce.md`。
- 什么时候用：要**理解 NBS 新版 API 的 cid 时间分片 / 指标 ID 不稳定 / 口径字段**时；要一次性跨源（中国宏观 + World Bank/IMF/BIS/FRED）取数时；想用现成 MCP 而自己不想写抓取时。
- 怎么取（安装/接入，我们仓库不内置）：
  ```bash
  npx mcp-cnbs                      # stdio 模式
  npx mcp-cnbs --port 12345         # HTTP 模式
  # 免费公共实例（阿里云 ModelScope，无 FRED）：
  #   url = https://mcp.api-inference.modelscope.net/c2ca6ece4e9946/mcp
  ```
  客户端 JSON：`{"mcpServers":{"cnbs":{"command":"npx","args":["mcp-cnbs"]}}}`
- 覆盖：中国 NBS（月/季/年/分省，无鉴权）+ 6 个国际源；NBS 库码 `1/2/3/5/6/7`（月/季/年/分省季/分省年/其他普查）。时间格式 `2024YY`、季度 `2024A-D`、月 `202401MM`、区间 `2020YY-2024YY`；地区码 12 位补零（全国 `000000000000`）。
- 门槛：Node ≥18；中国 NBS 工具无鉴权，FRED 工具需免费 `FRED_API_KEY`（其余无 key）。npm 包 `package.json` 写 MIT，但**仓库根 `License` 文件实为 Apache-2.0**，许可口径不一致，正式分发前需核对。
- 实测：2026-10-02，macOS arm64，curl 8.x：`POST …/external/getEsDataByCidAndDt` → **404 Not Found**（`Server: dps`），确认该端点不存在，改用 `stream/esData` 正常返回北京 GDP；`GET …/external/query?search=CPI&pagenum=1&pageSize=15` → 200，`count=221`。**未安装 npm 包、未跑 MCP 工具**（只读研究，未执行第三方代码）。
- 上游：https://github.com/icen-ai/mcp-cnbs （npm: `mcp-cnbs`，文档 `api_introduce.md`）。

## 细节

### 主要工具名（按需调用）

`cnbs_search`、`cnbs_batch_search`、`cnbs_economic_snapshot`（10 大宏观指标快照）、`cnbs_compare`、`cnbs_fetch_nodes/metrics/series/end_nodes`、`cnbs_get_regions`（GB/T 2260）、`cnbs_get_categories`、`cnbs_get_guide`；分源工具有 `ext_world_bank`、`ext_imf`、`ext_oecd`、`ext_bis`、`ext_fred`、`ext_cn_census`（2020 人口/2018 经济/2016 农业普查）、`ext_cn_department`（财政部/工信/海关/央行等部委统计）、`ext_global_compare`。

### 传输/鉴权

stdio（`npx mcp-cnbs`）、HTTP（`--port`，端点 `/mcp`、`/sse`、`/message`）、SSE 三种；可用 `--auth-token` / `MCP_CNBS_AUTH_TOKEN` 开 Bearer 鉴权；Node ≥18。

### 工具调用范式（README 示例）

`cnbs_search(keyword="GDP")`；`cnbs_batch_search(keywords=["GDP","CPI","城镇化率","出生率"])`；`cnbs_compare(keyword="GDP", regions=["北京","上海","广东"], compareType="region")`；`cnbs_economic_snapshot()` 一次拿 GDP/CPI/PPI/PMI/失业率/工业增加值/社零/固投/进出口/M2。

### 关键洞见（读 `api_introduce.md` 得到）

1. **cid 有「时间分片」**：同一指标（如 CPI）按 5 年/制度变革切多个叶子 `cid`，节点上带 `sdate/edate`；取长历史须**分别请求各 cid 再本地拼接**。
2. **indicatorId 跨 cid 不稳定**，每个 cid 都要重新 `queryIndicatorsByCid` 建映射，不能缓存复用。
3. 指标返回带 **`i_mark`/`i_annotation` 统计口径说明**（计算方法、基期），引用口径时直接取。
4. 文档自称取数端点为 `POST /getEsDataByCidAndDt`——**实测该路径 404（下游 `dps` 返回 404 页）**，仍应用 `stream/esData`（见上「实测」）。

### 实测明细（2026-10-02，macOS arm64，curl 8.x）

- `POST …/external/getEsDataByCidAndDt` → **404 Not Found**（`Server: dps`），确认该端点不存在；改用 `stream/esData` 正常返回北京 GDP。
- `GET …/external/query?search=CPI&pagenum=1&pageSize=15` → 200，`count=221`，返回含 `explain/indic_id/da/dt/value`（全局关键词搜索可用，见 `nbs-api-skills.md`）。
- 未安装 npm 包、未跑 MCP 工具（只读研究，未执行第三方代码）。
