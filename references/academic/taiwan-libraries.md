# taiwan-libraries —— 台湾学位论文、华艺与国图数字资源

- 去哪找：
  - 台湾博硕士论文：`https://ndltd.ncl.edu.tw/`（免費检索/书目，全文需免费注册）
  - 华艺线上图书馆：`https://www.airitilibrary.com/` → 现 302 到 `https://www.airitilibrary.cn/`
  - 国图「臺灣記憶」：`https://tm.ncl.edu.tw/`（古籍/图像/地图，免费）
- 什么时候用：要**台湾视角**的中文文献时——找某题目的台湾硕博论文（清代台湾、日治时期、战后台湾史…）、要台湾期刊论文的题录、或要台湾老照片/古地图/方志图像。
- 怎么搜：三源各一句话——
  - **臺灣記憶**：GET 就够 `https://tm.ncl.edu.tw/search_result?lang=chn&query_words=<词>`；
  - **博硕士论文**：CGI 检索式 `qs0=<词>`，支持字段限定（如 `"清代".ti`），URL 里带会话号 `ccd`，**逐条记录另有免会话的永久链接**；
  - **华艺**：本机探到的只有机构认证页，**无公开检索入口**，需单位 IP/账号。
- 覆盖：NDLTD 为全国性硕博论文库（台湾教育部/国图体系，含摘要/目次/参考文献，实测命中含 102 学年度论文）；臺灣記憶为国家图书馆的图像/古籍/地图类数字馆藏（栏目：典藏資源、大事記要、共建共享資源）；华艺为全文数据库（期刊/学位论文，机构认证）。
- 门槛：NDLTD 检索免费免登录、**全文 PDF 需免费注册登录**；臺灣記憶免费免登录；华艺 = **单位 IP / 机构账号**（本机链路直接跳机构认证页）。
- 实测：2026-10-03（无头 Chromium）：NDLTD `qs0="清代".ti` → **904 筆**；永久链接 `https://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/login?o=dnclcdr&s=id%3D%22102NKNU5642017%22.&searchmode=basic` → **curl 200 / 128,533 B**，标题=论文名。臺灣記憶 `search_result?lang=chn&query_words=臺灣府` → 200 / 63,230 B。`airitilibrary.com` → 302 → `airitilibrary.cn/Institution/InstitutionalCertification`（机构认证）。
- 上游：<https://ndltd.ncl.edu.tw/>、<https://tm.ncl.edu.tw/>、<https://www.airitilibrary.com/>

## 细节

### 1. 臺灣博碩士論文知識加值系統（ndltd.ncl.edu.tw）

| 用途 | URL / 端点 | 形态 |
|---|---|---|
| 首页入口 | `https://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/login?o=dwebmge` | ⚠️ 首页是 JS 跳转 + F5 BIG-IP cookie 挑战，**必须能跑 JS**（浏览器 ✅，curl 拿不到内容） |
| 检索 | `POST https://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/ccd=<sid>/search`，字段 `qs0=<检索式>` | HTML 结果页；表单里 `qs0` 是唯一检索输入框，method 是 **POST** |
| 结果页 | `…/ccd=<sid>/search#result` | HTML，含「檢索策略：… 檢索結果共 N 筆資料」 |
| 单条记录 | `…/ccd=<sid>/record?r1=<序号>&h1=0` | HTML（会话内定位） |
| **永久链接** | `https://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/login?o=dnclcdr&s=id%3D%22<论文编号>%22.&searchmode=basic` | ✅ **免会话、可 curl**（`s` 值形如 `id="102NKNU5642017".`，编号 = 学年度+校代码+系所+序号）；约 128 KB，`<title>`=论文名 |
| 电子全文 | 记录页「電子全文」页签 | ❌ 触发 `nclconfirmlogin(...請先入登入您的會員帳號)`，**需免费注册登录** |

- 检索式支持字段限定后缀：`"清代".ti`（题名）、并可「在搜寻的结果范围内查询」逐字段收窄（題名/研究生/校院/系所/指導教授/關鍵詞/摘要…）。
- 结果默认按相关度排序，可切表格式/条列式。

### 2. 華藝線上圖書館（airitilibrary.com → .cn）

- 实测链路：`GET https://www.airitilibrary.com/` → **302** → `https://www.airitilibrary.cn` → **302** → `/Institution/InstitutionalCertification` → 200。
- 认证页要求「机构认证 / 帐号密码 / 快速登入」，页面即显示来访 IP（如 `IP:114.253.37.92`）——**按 IP 判定机构**。
- 本机未探到可匿名访问的检索 URL；页面自述「全新平台即将登场」。**个人免费不可用**，走单位 IP 或机构账号。

### 3. 臺灣記憶 Taiwan Memory（tm.ncl.edu.tw）

| 用途 | URL | 形态 |
|---|---|---|
| 首页 | `https://tm.ncl.edu.tw/` → 302 → `/index` | ✅ 200 / 48,329 B（标题《臺灣記憶 Taiwan Memory》） |
| 检索 | `https://tm.ncl.edu.tw/search_result?lang=chn&query_words=<词>` | ✅ 200 / 63,230 B，HTML |
| 范围切换 | 同上 + `search_go_type_article`（典藏資源）/`search_go_type_twm`（大事記要）/`search_go_type_partner`（共建共享） | 复选框参数 |
| 进阶 | 结果页内 `AND/OR/NOT` + 字段（中文題名…） | HTML |

- 首页那行 `<form id="form_do_search" … action="/search_result">` 在 HTML 里被注释掉了（改由 JS 提交），但**GET 参数照旧可用**。

## 坑

1. NDLTD 首页有 **F5 BIG-IP 反爬 cookie 挑战** + JS 跳转，纯 `curl` 只会拿到一段脚本；要么用浏览器，要么**直接走永久链接**（`o=dnclcdr&s=id="…".&searchmode=basic`，实测 curl 200 / ~128 KB）。偶尔会返一个约 3.3 KB 的 F5 JS 壳，**带 cookie jar 重试一次即得全文**（`f5_cspm` cookie 会留在会话里）。
2. NDLTD 的 `ccd=` 是**会话号**，`/search`、`/record` 一类 URL 不可跨会话复用；要引用就给永久链接。
3. 华艺已从 `.com` 跳 `.cn` 并强制机构认证，**别把它当免费源**；引用题录前先确认是否有机构权限。
4. 臺灣記憶的检索词建议用繁体；图片二次利用需看「申請授權說明」页。
