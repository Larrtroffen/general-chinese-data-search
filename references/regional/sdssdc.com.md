# sdssdc.com —— 山东社会科学数智服务平台

- 去哪找：`http://www.sdssdc.com/`（HTTPS 同样 200）。
- 什么时候用：要山东省级的**社会科学数据/年鉴/成果/人才/政策**；这是「山东省社会科学数据中心」的一站式数智门户。
- 怎么取：前端是 Vue3 SPA，数据全部走 `/api/*`；**实测所有匿名请求返回 401**（需登录 token），须在浏览器注册登录后使用。前端路由提示板块：`/sjpt/yearbookList`（年鉴）、`/sjpt/achievementList`（成果）、`/szskg`（数智社科）、`/cloudSearch`（云检索）、`/rczy`（人才资源）、`/zcxx`（政策信息）、`/cgzy`（成果资源）。
- 覆盖：山东社会科学年鉴、成果、人才、机构、政策与需求（上游声明：2017-07 启用）。
- 门槛：**注册登录**（山东省社会科学数据中心要求「集中注册登录和信息完善」）。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA：`http://www.sdssdc.com/` → 200（671 B SPA 壳，`<title>山东社会科学数智服务平台`）；`/api/sjpt/yearbookList`、`/api/sjpt/index`、`/api/index`、`/api/cloudSearch?keyword=经济`、`/api/sjpt/yearbookTable?…`、`/api/cgzy/achievementList?…` **均 → 401**（空 body）；`/prod-api/sjpt/yearbookList` → 500。
- 上游：`http://www.sdssdc.com/`；山东省社会科学数据中心启用报道（国际在线山东频道，2017-07-10）。

## 细节

- API 前缀已确认为 **`/api/`**（`/prod-api/` 是错前缀，返回 500）。401 说明端点存在但要求鉴权；登录态下的参数格式未验证。
- 站点是 Vue3 + chunk-vendors 打包，路由表在 `app.js`（`/js/app.js`），未从 bundle 挖到 API 绝对地址。

## 坑

1. **全站 API 需登录**，匿名 curl 一律 401——不要把它当公开数据源。
2. `/api/` 与 `/prod-api/` 只差一个前缀，行为却完全不同（401 vs 500），照抄时要核对。
3. 平台是**山东省级科研管理与数据门户**，覆盖面以山东为主，不含全国面板。
