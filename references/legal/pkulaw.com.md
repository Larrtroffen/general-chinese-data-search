# pkulaw.com —— 北大法宝

商业法律法规数据库：查法规、地方规范性文件、裁判文书等。本任务用它找《实施方案》类党委文件，结论见下。

- 去哪找：
  - 站点：`https://www.pkulaw.com/…`（未登录态只返回 JS 壳，约 29KB，无检索结果）
  - MCP 网关：`https://apim-gateway.pkulaw.com/`
  - 已装 skill：`~/.agents/skills/pkulaw-mcp-installer`（只做 MCP 配置写入，不含 Token；安装后需重启运行时加载 MCP）
- 什么时候用：需要法律/行政法规/地方性法规/规章/司法解释/裁判文书（商业库）检索时；**党委文件（市委/区委实施方案）基本不收录**，"试点单位名单"类附件更不可期。
- 怎么搜：走 MCP 网关，须**持有 `PKULAW_AUTH_TOKEN`**（控制台签发）；若必须试党委文件，优先 25 积分的 `pkulaw-law-keyword` 检索"街乡吹哨 部门报到"，预期命中 0 或仅新闻类收录。
- 覆盖：法律/行政法规/地方性法规/规章/司法解释/裁判文书为主。
- 门槛：需 `PKULAW_AUTH_TOKEN`（MCP 网关）；官方网关 `GET https://apim-gateway.pkulaw.com/` 可达（HTTP 200），但无 Token 不可用。
- 实测：本机实测（无具体日期记录）：`https://www.pkulaw.com/…` 未登录态只返回 JS 壳（约 29KB），无检索结果；`https://apim-gateway.pkulaw.com/` HTTP 200 可达但需 `PKULAW_AUTH_TOKEN`。
- 上游：`https://www.pkulaw.com/` ｜ MCP 安装说明：`~/.agents/skills/pkulaw-mcp-installer`

## 细节

### 替代路径（党委文件）

1. 文库站点流传稿：360 搜索"…实施方案 参考版"（豆丁/道客巴巴等，均为编辑修改稿、无附件）。
2. 政府信息公开申请（市委组织部/市委社会工委）。
3. 区档案馆查阅 2018 年 3-4 月试点部署文件。
