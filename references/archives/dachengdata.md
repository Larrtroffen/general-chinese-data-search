# dachengdata.com —— 大成故纸堆

商业综合性古旧资源数据库：古籍、古方志、家谱、晚清民国期刊、报纸、老照片、党史等。站点是 Java(Struts) 老站，**首页直跳登录页**，无机构账号进不去；但**帮助页把检索方式写得很清楚**，可以照此规划检索式，再去有权限的机构端口用。

- 去哪找：
  - 首页（**302 到登录**）：`https://www.dachengdata.com/` → `meta refresh` → `/search/toRealIndex.action` → **302** → `/searchSchoolUser/login`
  - 检索入口（登录后）：`https://www.dachengdata.com/search/toRealIndex.action`
  - 登录提交：`POST /searchSchoolUser/loginSubmit.action`（表单 `loginForm`）
  - 使用说明（**公开可读**）：`https://www.dachengdata.com/help/usage.jsp`
  - 关于本库（10 页图片介绍）：`https://www.dachengdata.com/about_us.jsp`（图 `/images/00.webp`…`/images/09.webp`）
  - 意见反馈/视频教程：`/tuijian/advice.jsp`、`/video.jsp`
- 什么时候用：
  - 找 **老刊 / 民国图书 / 晚清民国报纸 / 古方志 / 家谱 / 党史资料 / 老照片**，尤其是地方小刊小报这类公共平台覆盖薄的材料；
  - 做**家谱、方志**类检索时作为 `difangzhi.cn.md`、`shtong.md`、`bjdsdfz.cn.md` 的商业补充；
  - 需要**繁体关键词**检索（站点明确支持繁体）。
- 怎么搜：**检索方式（据官方 usage.jsp，逐字口径）**：
  - **全部**：在**题名、作者、出版者、来源等字段**中联合检索；
  - **题名 / 作者**：限定对应字段，适合精确查找；
  - **全文**：在**古籍全文库**中检索，**范围固定为古籍文献库**；
  - 关键词**支持繁体**；检索词不能为空；
  - **结果筛选**：可按**库别**（老刊、古籍、民国图书等）缩小；
  - **聚类导航**：左侧勾选作者或刊名后点「应用筛选」；聚类按**完整名称匹配**（避免同字误选）；
  - 已选条件显示在结果页。
  可复现入口（未登录只能到登录页）：
  ```bash
  curl -sSL -A '<桌面 Chrome UA>' 'https://www.dachengdata.com/'            # → 302 /searchSchoolUser/login
  curl -sSL -A '<桌面 Chrome UA>' 'https://www.dachengdata.com/help/usage.jsp'   # 200，检索说明（明文 HTML）
  ```
  登录后的检索/结果/全文/下载路径见 robots.txt（**均为 Disallow，勿抓**）：`/asearch/`（检索）、`/viewText/`、`/fullText/`、`/download/`、`/schoolDownload/`、`/bookNum.do`；接口 `/api/`、`/dwr/` 亦被禁。这些路径**存在但形态未验证**（登录墙内）。
- 覆盖：
  - 上游自述（`about_us.jsp` 第 2 页，官网原话）：*"大成故纸堆数据库，一个专门收录古旧资源的综合性数据库平台…包含并不限于**古籍、古方志、家谱以及晚清和民国期刊、报纸、老照片、党史**等多个方面的古旧文献类型"*；用途面向晚清史、民国史、近代文学史、教育学、中共党史、现代汉语、思想史、社会学、经济学、新闻、政治学、法律、哲学、科技史。**未给出册数/篇数**。
  - 粒度/年代/更新：未公开（需登录后看库别列表）。
- 门槛：
  - **机构用户登录**（`/searchSchoolUser/`，页面标题「大成故纸堆 · 用户登录」）——学校/机构账号或机构 IP；公网匿名只能看 `help/usage.jsp`、`about_us.jsp`。
  - 主域 `www.dachengdata.com` 根路径会跳到 **`http://www.dachengdata.com/searchSchoolUser/login`**（注意落回 http）。
  - `robots.txt` 明确 **Disallow `/api/`、`/dwr/`、`/download/`、`/fullText/`**，并对 GPTBot/ClaudeBot/Bytespider 等整站封禁 → **不要尝试绕过**，只记录入口与门槛。
  - 页面会**记录并显示你的访问 IP**（help 页可见「访问 IP 114.253.37.92」）。
- 实测：2026-10-03，macOS 27（arm64），curl 8.x，桌面 Chrome UA。① `GET https://www.dachengdata.com/` → **200 / 367 B**，`<title>大成故纸堆</title>`，正文只有 `meta refresh` + JS 跳 `/search/toRealIndex.action`。② `GET /search/toRealIndex.action` → **200**，最终 URL `http://www.dachengdata.com/searchSchoolUser/login`，21.7 KB，`<title>大成故纸堆 · 用户登录</title>`；表单 `action="/searchSchoolUser/loginSubmit.action"`。③ `GET /help/usage.jsp` → **200 / 8715 B**，`<title>使用说明 - 大成故纸堆</title>`，正文 518 字，检索方式如上。④ `GET /about_us.jsp` → **200 / 14160 B**，10 页图片版介绍；抓 `/images/00–02.webp` 读图拿到上面那段自述。⑤ `GET /robots.txt` → **200 / 1404 B**；`GET /sitemap.xml` → **200**，仅 4 条 URL（首页/检索/关于/帮助）。
- 上游：https://www.dachengdata.com/

## 细节

### 入口表

| 用途 | URL |
|---|---|
| 首页（**302 到登录**） | `https://www.dachengdata.com/` → `meta refresh` → `/search/toRealIndex.action` → **302** → `/searchSchoolUser/login` |
| 检索入口（登录后） | `https://www.dachengdata.com/search/toRealIndex.action` |
| 登录提交 | `POST /searchSchoolUser/loginSubmit.action`（表单 `loginForm`） |
| 使用说明（**公开可读**） | `https://www.dachengdata.com/help/usage.jsp` |
| 关于本库（10 页图片介绍） | `https://www.dachengdata.com/about_us.jsp`（图 `/images/00.webp`…`/images/09.webp`） |
| 意见反馈/视频教程 | `/tuijian/advice.jsp`、`/video.jsp` |

## 坑

1. 首页"看起来只有 200 B"不是坏了，是 `meta refresh` 壳；别据此判定"站点为空"。
2. 检索全在登录后，**没有可公网复现的检索 URL**；写检索方案时只能引用官方 usage.jsp 的字段口径。
3. robots 对 AI 爬虫整站封禁 + 记录访问 IP，**不做任何绕行**；有需求走机构采购。
4. 与免费的 `modernhistory.md`、`guji.nlc.cn.md`、`shuge.md` 有交集，先试免费源再考虑此库。
