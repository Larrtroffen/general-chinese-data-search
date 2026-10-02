# bjsfzg.bjdsdfz.cn —— 北京市数字方志馆

北京市方志馆数字平台：志书、数字年鉴（市级）、馆藏查询。

- 去哪找：
  - 站点：`https://bjsfzg.bjdsdfz.cn/`
  - 检索页（志鉴检索）：`https://bjsfzg.bjdsdfz.cn/znjs?keyword={关键词}`（GET 带 keyword 即触发）
  - 底层接口：`api.GET('/content/search', {siteId, keyword, page, size:20, …})`，走 `https://bjsfzg.bjdsdfz.cn/dfz-api/dfz-toolbox/tp/public/`
- 什么时候用：查北京市级数字年鉴（《北京年鉴》）、民国年鉴、馆藏方志检索。
- 怎么搜：`GET /znjs?keyword={关键词}` 触发检索；**结果为 AJAX 渲染**：curl 拿不到条目，需真实浏览器打开该 URL 等 3–5s 后读 `#searchList`。
- 覆盖：数字年鉴《北京年鉴》2012–2021 各卷（`/bjnj/{id}.jhtml`）、民国年鉴（`/mgnj/…`）；**无区级年鉴**（《北京朝阳年鉴》等不在此站，见 `bjdsdfz.cn.md`）。
- 门槛：首页/栏目页是静态 HTML + 少量 JS，curl 可抓；**检索必须浏览器**。年鉴单卷页嵌 pdfjs 阅读器，**PDF 端点有登录判定**（两站共用同一套 dfz-pdfjs 体系，详见 `bjdsdfz.cn.md` 的说明）。
- 实测：（本卡未记录实测日期）馆藏内容为实测核对：数字年鉴《北京年鉴》2012–2021 各卷、民国年鉴在册；无区级年鉴。
- 上游：`https://bjsfzg.bjdsdfz.cn/`

## 细节

### 馆藏内容（实测）

- 数字年鉴：《北京年鉴》2012–2021 各卷（`/bjnj/{id}.jhtml`）、民国年鉴（`/mgnj/…`）。
- **无区级年鉴**（《北京朝阳年鉴》等不在此站，见 `bjdsdfz.cn.md`）。
- 首页/栏目页是静态 HTML + 少量 JS，curl 可抓；检索必须浏览器。
