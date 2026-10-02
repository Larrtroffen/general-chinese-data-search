# resdc.cn —— 资源环境栅格数据

- 去哪找：资源环境科学与数据平台 `https://www.resdc.cn/`；数据检索 `https://www.resdc.cn/DataSearch.aspx`；分类列表 `/Datalist1.aspx?FieldTyepID=<a,b>`；数据集详情 `/data.aspx?DATAID=<n>`；DOI 页 `/DOI/DOI.aspx?DOIID=<n>`。
- 什么时候用：要**中科院地理所口径**的中国空间栅格/矢量数据——土地利用（多期 1 km/30 m）、植被指数（NDVI/NPP）、土壤、气象插值、人口格网、行政区划边界、流域/分区边界；做空间分析、制图底图、区域面板。
- 怎么取：站点前置 **WebShield JS 会话校验**，`curl` 直连返回 405 B 的跳转页，需先取 token 并带 cookie 跟一次（本机验证可通）：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  curl -sS -c jar.txt -A "$UA" 'https://www.resdc.cn/' | grep -o 'WebShieldSessionVerify=[A-Za-z0-9]*'
  curl -sS -L -b jar.txt -c jar.txt -A "$UA" 'https://www.resdc.cn/?WebShieldSessionVerify=<token>'   # 后再取 / 即为真页
  ```
  真页为 ASP.NET WebForms（GB2312 编码），分类列表/详情/DOI 页为 HTML。**下载需登录**：详情页下载按钮跳 `/Login.aspx?ReturnUrl=…`。站内检索为 `DataSearch.aspx` 的 `__VIEWSTATE` POST 表单（脚本化需先取 viewstate）。
- 覆盖：中国（部分全球）· 土地利用/植被/土壤/气象/人口/区划等 · 多年份/多分辨率（1 km、30 m 等）· 栅格 + 矢量；更新随数据集。
- 门槛：浏览与元数据 **免费匿名**；**下载需注册登录**（多为实名，部分数据集要求邮箱申请/单位）。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA）——`https://www.resdc.cn/` 首次 → 200 但仅 405 B JS 挑战页（`self.location="/?WebShieldSessionVerify=H32V1xFzS0oXTKemQiHI"`）；按上文取 token 并带 cookie 跟随 → 200（154,835 B，标题「资源环境科学与数据平台」，含 `/DataSearch.aspx`、`/data.aspx?DATAID=…`、`/DOI/DOI.aspx?DOIID=…`、`/Login.aspx`、`/UserReg.aspx`）；`/data.aspx?DATAID=401` → 200（121,276 B）但下载链接为 `/Login.aspx?ReturnUrl=…`；`/DataSearch.aspx` → 200，检索表单为 POST + `__VIEWSTATE/__EVENTVALIDATION`。
- 上游：中国科学院地理科学与资源研究所（资源环境科学数据中心）。

## 细节

- 常用入口：数据出版 `/Datalist1.aspx?FieldTyepID=<类目对>`、`/DatalistHeitudi.aspx`（黑土地专题）、`/BookList.aspx`（专业图书）、`/LandsatSearch/`（遥感影像查询）、`/DOI/doiList.aspx`（数据论文）。
- DOI 页形如 `/DOI/DOI.aspx?DOIID=32`，数据集详情页 `/data.aspx?DATAID=<n>`；两者 ID 不同，别互串。
- 下载/申请流程与实名要求随数据集变化，部分全国栅格数据（如土地利用）需登录后在详情页点「数据下载」。

## 坑

1. **WebShield 会话校验**：不带 cookie 只能拿到 405 B 跳转页；脚本必须先握手，且 token 会话级、很快过期。
2. **编码为 GB2312**，解析响应要显式解码，否则中文乱码/报错。
3. 检索是 ASP.NET WebForms 的 `__VIEWSTATE` POST，不能简单拼 GET；想批量找数据集，优先用外部搜索引擎 `site:resdc.cn <关键词>`。
4. **CLCD（武汉大学 30 m 中国土地覆盖，Yang & Huang 2021, ESSD）不在本站**：其官方托管在 figshare（DOI 见 ESSD 论文 Data availability 段），本机 figshare API 返回 **403**（网络侧拦截），未取得记录号——要 CLCD 请走浏览器打开 figshare，或用 Google Dataset Search 定位。
5. 引用请区分「数据 DOI（`/DOI/DOI.aspx`）」与「数据集页」，正式发表需按站点要求填引用格式。
