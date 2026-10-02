# chinanpo.mca.gov.cn —— 社会组织登记与年检查询

- 去哪找：
  - 平台首页（含全国查询搜索框）：`https://chinanpo.mca.gov.cn/`
  - **全国社会组织信用信息公示平台（检索结果页）**：`https://xxgs.chinanpo.mca.gov.cn/gsxt/newList`
  - 组织详情：`https://xxgs.chinanpo.mca.gov.cn/gsxt/newDetails…`（列表项进入）
  - 严重违法失信名单：`https://xxgs.chinanpo.mca.gov.cn/gsxt/yzwfsxmdList`
  - 已取缔非法社会组织名单：`https://xxgs.chinanpo.mca.gov.cn/gsxt/banillegalorg`
  - 政策法规库：`https://zcfg.chinanpo.mca.gov.cn/api-k/pages/knowledgefrontend/kl_index_new.html`
  - 社会组织总数：`https://xxgs.chinanpo.mca.gov.cn/gsxt/shzzCount`
- 什么时候用：
  - 关键词：社会组织名称 / 统一社会信用代码 → **登记证书信息、法定代表人、业务主管单位、状态**。
  - 关键词：组织名 → **年检/年报**情况、是否被列入**严重违法失信名单**。
  - 关键词：组织名 → 是否为**已取缔的非法社会组织**（"山寨社团"甄别）。
  - 用途：核查基金会/协会/学会的**合法性与年检状态**、判断"某协会"真伪。
  - 不适用：企业（去 `gsxt.md`）；民办学校/医院等的**办学/执业许可**（去对应行业主管部门）。
- 怎么搜：
  - **① 网页检索（推荐）**：首页搜索框输入"社会组织名称/统一社会信用代码"，点击搜索后跳转 `https://xxgs.chinanpo.mca.gov.cn/gsxt/newList?b=<b>`。`b` 的生成方式**完全由首页 JS 给出**（`searchOrgData()`）：
    ```js
    var param = { o: 组织名称, u: 统一社会信用代码, t: 类型, s: 状态 };
    var b = btoa(encodeURIComponent(JSON.stringify(param)));   // 注意：先 encodeURIComponent 再 base64
    // 不带条件时直接用：https://xxgs.chinanpo.mca.gov.cn/gsxt/newList
    ```
    示例（`{o:"基金会",u:"",t:"",s:""}`）：`https://xxgs.chinanpo.mca.gov.cn/gsxt/newList?b=JTdCJTIybyUyMiUzQSUyMiVFNSU5RiVCQSVFOSU4NyU5MSVFNCVCQyU5QSUyMiUyQyUyMnUlMjIlM0ElMjIlMjIlMkMlMjJ0JTIyJTNBJTIyJTIyJTJDJTIycyUyMiUzQSUyMiUyMiU3RA==`
  - **② 列表数据接口（由前端 JS 反查，未直连成功）**：`POST https://xxgs.chinanpo.mca.gov.cn/api/biz/ma/shzzgsxt/a/gridQuery.html`，参数 `pageNo=1&pageSize=10&paramsValue=<名称或统一社会信用代码>&aaae0105=<类型 t>&aaae0127=<状态 s>&a=&b=&c=`（滑块验证码 related `valuea/valueb/valuec`）。参数映射（列表页 JS 解析 URL 里的 `b`）：`paramsValue = u || o`，`aaae0105 = t`，`aaae0127 = s`。同族接口：`biz/ma/shzzgsxt/a/getAssociate.html`（联想）、`getTotal.html`（统计）、`gsptLogSave.html`（埋点）。
  - 结果形态：JSON（`code=200` 时 `result.data` = 记录数组，`result.totalCount` = 总数）。直连实测返回 3 059 B 的 SPA 壳（text/html），即请求未命中后端 → **需浏览器会话**。
- 覆盖：全国民政部门登记的社会团体、基金会、民办非企业单位（社会服务机构）+ 已取缔非法组织；登记信息为当前状态，年报/年检按年度，严重违法失信名单为当前有效期名单；粒度=单组织级 + 单条年报/处罚记录；动态更新（登记机关录入后同步）。
- 门槛：免费、**无需登录/注册**；有前端**滑块验证码**与 WAF（响应头 `Server: WAF`，回不下发 `https_waf_cookie`）；触发高频查询时可能要求验证码。
- 实测：2026-10-03，macOS，curl 8.x，Chrome 126 UA。`GET https://chinanpo.mca.gov.cn/` → **200**，50 680 B，`<title>中国社会组织政务服务平台</title>`（首页 JS 含 `searchOrgPath="https://xxgs.chinanpo.mca.gov.cn"` 与 `searchOrgData()` 的 `b` 构造）；`GET https://xxgs.chinanpo.mca.gov.cn/gsxt/newList` 及带 `?b=` → **200**，3 059 B（Vue SPA 壳，结果由 XHR 渲染）；`GET …/gsxt/js/app.ffa5e75f.js` → **200**，145 897 B（`baseURL:"/api"`，路由 `/newList`、`/newDetails`、`/yzwfsxmdList`、`/shzzCount`）；`GET …/gsxt/js/chunk-40d645cc.3fe2b715.js` → **200**，54 886 B（反查到 `gridQuery.html`/`getAssociate.html`/`getTotal.html` 及 `queryParams` 字段）；`POST/POST …/api/biz/ma/shzzgsxt/a/gridQuery.html` → **200**，3 031 B SPA 壳（未命中后端）。
- 上游：<https://chinanpo.mca.gov.cn/>、<https://xxgs.chinanpo.mca.gov.cn/gsxt/newList>、<https://xxgs.chinanpo.mca.gov.cn/gsxt/yzwfsxmdList>、<https://xxgs.chinanpo.mca.gov.cn/gsxt/banillegalorg>

## 细节

民政部主办的**社会组织**（社会团体/基金会/民办非企业单位/社会服务机构）登记管理与信用公示平台：含全国社会组织信用信息公示平台（登记信息、年检年报）、严重违法失信名单、已取缔非法社会组织名单。

检索参数与接口分别由首页内联 JS `searchOrgData()`、`/gsxt/js/app.ffa5e75f.js`、`/gsxt/js/chunk-40d645cc.3fe2b715.js` 反查（chunk 文件名由 app.js 的 webpack 映射表得到）。

## 坑

1. 直连 `/api/biz/ma/shzzgsxt/a/gridQuery.html`（GET/POST，带 Referer/Origin/XHR 头）返回 200 的 SPA 壳，非数据 → 需浏览器会话。
2. 滑块验证码 `slideCaptcha`（前端自实现 base64 编解码 + `valuea/valueb/valuec` 校验）。
3. WAF 存在（`Server: WAF`），高频查询要求验证码。
