# chinabuddhism.com.cn —— 佛教协会资讯与发布

- 去哪找：**中国佛教协会官网**`https://www.chinabuddhism.com.cn/`（亦 `https://chinabuddhism.com.cn/`）；栏目 `/web/list.html?classid=<栏目号>`（新闻中心 `510`、下载专区 `534`）；信息查询 `/web/myxxcx.html`；JSON 接口在 `/web/*`。
- 什么时候用：要**中国佛教协会的新闻、公告、规章制度、期刊目录**；要佛教中国化、佛教团体治理、藏传/南传佛教工作等协会口径稿件；要协会发布活动的原始链接（寺庙/佛学院相关）作佐证。
- 怎么搜：站点有 **Alibaba WAF（`denied by http_custom`）**，curl 直连 403，**必须用真实浏览器**（无头 Chromium 可过）。过检后页面同源 `fetch` 可用下列 JSON：
  ```js
  // 在 chinabuddhism.com.cn 页面上下文内
  await fetch('/web/getColumnListByParentId/0').then(r=>r.json())  // 栏目树（columnId/columnNameZh/path）
  await fetch('/web/publishList').then(r=>r.json())               // 发布位/专栏（{total,rows:[{id,bannerName,category,publishTime}]}）
  await fetch('/web/config').then(r=>r.json())                    // 站点配置（名称/地址/备案）
  ```
  结果形态：**JSON**；栏目内容页 `/web/list.html?classid=…`、详情页 `/web/details/<id>` 为 HTML。
- 覆盖：协会新闻与专题、制度法规、本会期刊、下载专区、信息查询；更新随官网发稿（2026 年在更）。粒度=单篇。
- 门槛：**免费、免登录、无 key**；但**有 WAF**——CLI 直连 403，须浏览器会话。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA + Chromium 无头——`curl https://www.chinabuddhism.com.cn/` → **403**（`X-Tengine-Error: denied by http_custom`，Alibaba WAF）；Chromium 打开 → **200**，`<title>中国佛教协会官网</title>`，正文含「深入推进我国佛教中国化五年工作规划纲要」「中国佛教协会第十一届理事会…」等；页面 XHR 实测 `GET /web/getColumnListByParentId/0`、`/web/news/list/1/14`、`/web/config`、`/web/mourningFilter`、`/web/publishList`；同源 `fetch /web/getColumnListByParentId/0` → 200 JSON（栏目含「首页/Home」「新闻中心/News」等）；`fetch /web/config` → 200，`{"code":200,"data":{"name":"中国佛教协会","add":"北京市西城区阜成门内大街25号",…}}`。
- 上游：<https://www.chinabuddhism.com.cn/>（中国佛教协会）。

## 细节

- 已确证接口：`/web/getColumnListByParentId/{parentId}`（`0`=顶级栏目）、`/web/publishList`、`/web/config`、`/web/mourningFilter`。
- `/web/news/list/{classId}/{pageSize}` 首页会调用，但本机同源复现返回 `[]`（疑需页面上下文或额外参数），取栏目内容以 HTML 页 `/web/list.html?classid=…` 为准。
- 导航：`/web/myjs.html`（本会介绍）、`/web/list.html?classid=510`（新闻）、`/web/ListInfo_fg.html`（制度法规）、`/web/zt.html`（专题）、`/web/qk.html`（期刊）、`/web/list.html?classid=534`（下载）、`/web/myxxcx.html`（信息查询）。

## 坑

1. **WAF 硬拦 CLI**：403 自定义页（`denied by http_custom`），本卡所有取数须走浏览器；换 UA 无效。
2. 「信息查询」页本机未展开出可检索实体（佛教场所/教职人员）；国家级宗教场所检索仍回 `sara.gov.cn.md`。
3. 协会为**宗教团体**，稿件为团体口径；正式引用涉及宗教政策请核国家宗教事务局/中央统战部原文。
4. `/web/news/list` 无参数会抛 500 数字转换异常，勿以此为站点故障。
