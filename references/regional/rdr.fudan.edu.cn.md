# rdr.fudan.edu.cn —— 复旦大学社会科学数据平台

- 去哪找：`https://rdr.fudan.edu.cn/datahome/`；数据空间 `/datahome/open/datahome/54`；高级智能检索 `/datahome/open/advanceSmartSearch`；变量检索 `/datahome/open/variableSearch`；数据资源 `/datahome/open/dataResource`；数字资源 `/datahome/open/digital`。
- 什么时候用：要复旦及合作方发布的**社科数据集/变量级检索**；要按变量/题项找数据；要复旦数据空间里共享的研究数据。
- 怎么搜：前端是 Vue3 SPA（所有路由都返回同一 1.9 KB 外壳，数据由 JS 拉取），**人用入口即上面的路由 URL**；登录走**复旦大学统一身份认证**（`id.fudan.edu.cn/idp/authCenter/authenticate`）与上海教育云（`sog-seman.cloud.sh.edu.cn/oauth/v1/authorize`）。
- 覆盖：复旦社科数据仓储（re3data 有「Fudan University Social Science Data Repository」记录，上游声明）；含数据空间、变量检索、数字资源板块。
- 门槛：浏览可能免登录；**下载/申请需复旦统一身份认证**（校外受限）。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA：`https://rdr.fudan.edu.cn/datahome/` → 200（1,908 B，`<title>复旦大学社会科学数据平台`，入口脚本 `/datahome/assets/js/index-2c7f71a7.js`）；`/datahome/open/advanceSmartSearch`、`/datahome/open/variableSearch`、`/datahome/open/dataResource`、`/datahome/open/datahome/54` **均 → 200（同一 1,908 B SPA 壳）**。**旧域名 `dvn.fudan.edu.cn` → 502**（http/https 均 502 Bad Gateway）。
- 上游：`https://rdr.fudan.edu.cn/datahome/`；re3data `r3d100012775`（上游声明）。

## 细节

- 前端 bundle 里可见的后端/第三方地址：`https://id.fudan.edu.cn/idp/authCenter/authenticate`（复旦 IdP）、`https://sog-seman.cloud.sh.edu.cn/oauth/v1/authorize`（上海教育云）、`https://i-huiyuan.shec.edu.cn/home`。
- 路由全集（从 `index-*.js` 提取）：`/open/home`、`/open/aboutUs`、`/open/advanceSmartSearch`、`/open/variableSearch`、`/open/dataResource`、`/open/digital`、`/open/news`、`/open/attainment`、`/open/fileAnalysis` 等；数据管理侧有 `/dataManager/dataSpace`、`/application/applyList`。

## 坑

1. **旧域名 `dvn.fudan.edu.cn` 已 502**，不要再引用；现行入口是 `rdr.fudan.edu.cn/datahome/`。
2. 全站是 SPA，curl 只能拿壳，**没有可匿名直连的 JSON 检索 API**（未从 bundle 挖到后端地址；调用在懒加载 chunk）。
3. 校外账号能否申请下载未验证；入库/下载大概率要复旦身份。
