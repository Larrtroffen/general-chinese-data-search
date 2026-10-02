# data.cma.cn —— 气象观测数据检索

- 去哪找：中国气象数据网 `http://data.cma.cn/`；站点为 SPA（Vue），路由 `/advanced-search`、`/data-service`、`/search`、`/vis/live-data`、`/user/data`；用户接口前缀 `/api/user/`。
- 什么时候用：要**中国气象局**口径的气象观测/再分析/模式数据——地面站、高空、雷达、卫星、辐射、农业气象；做气候统计、极端天气、气象-经济交叉研究；对应《中国气象年鉴》/气象公报的数字底稿。
- 怎么搜：站点是前端渲染，**数据检索与下单在页面里**，未发现可匿名直取的检索 JSON；已知匿名可探的用户接口：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  curl -sS -o /dev/null -w '%{http_code}\n' -A "$UA" 'http://data.cma.cn/api/user/getUserInfoByToken'   # → 401
  ```
  前端 bundle `assets/js/index-*.js` 暴露 `/api/user/{login,getUserInfoByToken,forgetPasswd,image}`、`/mobile/data`、`/mobile/search` 等；数据检索/下载接口在登录态下才可用（**未本机验证**）。
- 覆盖：全国 + 全球交换站 · 1951–至今（视数据集）· 站点/格点 · 逐时/逐日/逐月；含 CMORPH、CRA-40 再分析、雷达拼图、卫星等。
- 门槛：**实名注册登录**（部分数据免费、部分按需申请/收费；数据服务与 API 面向注册用户）。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA）——`http://data.cma.cn/` → 200（534 B SPA 壳，`<div id="app">` + `/assets/js/index-ze_rRBJb.js`）；拉取该 bundle（539 KB）挖出上述路由与 `/api/user/*` 端点；`GET http://data.cma.cn/api/user/getUserInfoByToken` → **401**（空响应，确认需令牌）。
- 上游：中国气象局国家气象信息中心；另有国家气象科学数据中心（同一门户）。

## 细节

- 与中国气象局的其他数据口区别：`data.cma.cn` 面向科研用户的登记下载；国家气候中心 `cmdp.ncc-cma.net`（[`ncc-cma.net.md`](ncc-cma.net.md)）给的是环流指数与气候监测产品；空间栅格底图另见 [`../stats/geodata.md`](../stats/geodata.md)。
- 站点有移动端路由 `/mobile/data`、`/mobile/search`（移动页更轻，可能更好抓，**未实测**）。

## 坑

1. **纯 SPA + 登录墙**：curl 只能拿到壳页；检索/下载必须在浏览器里登录（实名）后进行，脚本化成本高。
2. `/api/user/getUserInfoByToken` 无令牌返回 **401 且空 body**，别把空响应当「服务不可用」。
3. 数据集有「免费/收费/申请」三类，同一门户里待遇不同；引用要注明数据集全名与版本。
4. 站点近年改版（旧 `data.cma.cn/data/cdcdetail/...` 路径已变），写死 URL 易失效；以 `data.cma.cn` 首页最新路由为准。
5. 气象数据的**起止年份与站点数**逐数据集不同，别按「1951–至今」一概而论。
