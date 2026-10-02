# microdata.stats.gov.cn —— 国家统计局微观数据申请

- 去哪找：微观数据实验室（「微观数据用户注册申请系统」）`https://microdata.stats.gov.cn/`；申请须知见国家统计局官网 `https://www.stats.gov.cn/zt_18555/zthd/sjtjr/d12kfr/tjzsqzs/202302/t20230216_1908892.html`；旧申请入口 `http://219.235.131.52/`（本机不通）。
- 什么时候用：要**国家统计局官方微观数据**——住户收支与生活状况调查、人口普查 / 1% 人口抽样、经济普查、农业普查、规模以上工业企业、企业跟踪调查等；需要官方抽样框与官方口径的实证。
- 怎么取：经国家统计局官网「统计服务—微观数据申请」在线提交申请 → 审核 → **联系实验室预约现场使用**（数据不落地，须到实验室/数据开发中心现场分析）。
- 覆盖：住户收支与生活状况调查已开放 **7 个年份**；首页数据资源另有第六次全国人口普查、2015 年 1% 人口抽样调查、第三/五次全国经济普查、第三次全国农业普查、2012–2016 规模以上工业企业财务状况调查、2014–2016 企业跟踪调查季度数据等（上游声明）。
- 门槛：**需注册 + 实名申请 + 审批**；**数据现场使用**（国家统计局微观数据实验室，及国家统计局—中国人民大学 / —北京大学数据开发中心）。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA：`https://microdata.stats.gov.cn/` → 200（682 B，Vue SPA，`microdata-reg`）；`https://microdata.stats.gov.cn/dataApplyReg` → 404；`http://219.235.131.52/` → **连接失败**。
- 上游：国家统计局 `https://www.stats.gov.cn/`。

## 细节

- SPA 前端路由（从前端 `app.js` 提取）：`/dataApplyReg`、`/dataChangeApplyReg`、`/labChangeReg`、`/labDetail`、`/microdata`、`/organizationListMore`、`/researchAgencyListMore`、`/researchAgencyReg`、`/resultListMore`、`/resultReg`、`/regResultQuery`、`/dataListMore`、`/feedBack`。
- 前端 bundle 内后端下载路径：`/tjmicrodatalab/download/reg/regExamine/`、`/tjmicrodatalab/unAuthDownload/`、`/tjRegDownload/ApprovalDownload/`；另有申请材料页 `/tjmicrodatalab/download/reg/application.html`、`/tjmicrodatalab/download/reg/instruction.html`（**直接请求返回 404/SPA 兜底**，须在站内点击）。前端 API 基址由 `VUE_APP_BASE_API` 注入。
- 实验室地址：国家统计局三里河东办公区 106 室；电话 010-68782405；邮箱 `wgsjsys@stats.gov.cn`；邮编 100826。
- 政策问答（官网 `…/hd/lyzx/zxgk/202502/t20250217_1958722.html`）：2018 年底成立微观数据实验室，已开放 7 个年份住户调查数据。

## 坑

- 前端是 SPA（`noscript` 提示需 JavaScript），**curl 拿不到数据列表**；直接请求 `/dataApplyReg` 返回 404（路由非服务端路径）。
- 微观数据**不可下载**，须现场使用；申请周期与到场安排要提前规划。
- 站点前置奇安信 WAF（DNS CNAME 到 `…qaxcloudwaf.com`）；`219.235.131.52` 旧入口本机连不上。
