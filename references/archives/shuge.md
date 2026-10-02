# shuge.org —— 书格 公共版权古籍 PDF

自由开放的数字图书馆，专收**公共版权领域**的古籍善本（参照伯尔尼公约），提供高清 PDF 下载。站点是 WordPress；真正的宝藏是它的**公开存储服务器 `shuge.hanjihebi.com`**——一个 OpenList 实例，**列目录与文件搜索全部匿名开放**，可以直接按文件名检索全站 PDF 并取原文件。

- 去哪找：
  - 首页 / 分类：`https://www.shuge.org/` ；分类 `https://www.shuge.org/collection/<类>/`（经部 `jing`、史部 `shi`、子部 `ji`、集部 `literature`、丛书 `cong`、类书 `leishu`、稿钞本 `manuscript`、碑拓 `rubbings`、舆图 `map`、影像 `photographs`、绘画 `painting`、书法 `calligraphy`、**CC0授权** 等 20+ 类）
  - **站内搜索（HTML）**：`https://www.shuge.org/?s=<关键词>`（WordPress 原生搜索）
  - 书页（详情+下载入口）：`https://www.shuge.org/view/<slug>/`
  - **全站存储（公开目录）**：`https://shuge.hanjihebi.com/`（OpenList；页脚称「公开目录/全站资源」）
  - **存储文件搜索 API**：`POST https://shuge.hanjihebi.com/api/fs/search`
  - 存储列目录 API：`POST https://shuge.hanjihebi.com/api/fs/list`
  - 原文件直下：`https://shuge.hanjihebi.com/d/<path>`
  - 其余（下载短链、网盘页、子站）见「细节」。
- 什么时候用：
  - 要**整本古籍的 PDF**（原色/黑白、高清+、含分卷书签），而且**不想登录、不想走网盘**——走 `hanjihebi` 存储直下；
  - 知道书名/版本名但不知道在哪：先用存储的 `fs/search` 按关键词扫全站文件名；
  - 需要**成体系的专题**：宋刻本、永乐大典零本、中国古代木刻画史、中医典籍、CC0授权 等专题系列。
- 怎么搜：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'

  # 1) 站内检索（HTML，标题形如「「论语」的搜索结果 – 书格」）
  curl -sSL -A "$UA" 'https://www.shuge.org/?s=%E8%AE%BA%E8%AF%AD' | grep -oE 'https://www\.shuge\.org/view/[^"]*'

  # 2) 存储：文件级搜索（推荐！直接命中 PDF 文件与所在目录）
  curl -sS -A "$UA" -H 'Content-Type: application/json' -H 'Referer: https://shuge.hanjihebi.com/' \
    -X POST 'https://shuge.hanjihebi.com/api/fs/search' \
    -d '{"parent":"/","keywords":"论语","scope":0,"page":1,"per_page":20,"password":""}'
  #   → {"code":200,"data":{"content":[{"parent":"/书格网站资源/哲学经学/十三经注疏.三百三十五卷",
  #      "name":"十三经注疏.10.论语注疏.明嘉靖时期李元阳福建刻…pdf","is_dir":false,"size":281270623,"type":0}]}}

  # 3) 存储：列目录（path 逐层展开目录树）
  curl -sS -A "$UA" -H 'Content-Type: application/json' -H 'Referer: https://shuge.hanjihebi.com/' \
    -X POST 'https://shuge.hanjihebi.com/api/fs/list' \
    -d '{"path":"/","password":"","page":1,"per_page":100,"refresh":false}'
  #   → 顶层：Readme.md、书格网站资源/、卷轴画/、压缩包/ …

  # 4) 原文件直下（路径需 URL-encode；支持 Range）
  curl -sSI -A "$UA" 'https://shuge.hanjihebi.com/d/%E4%B9%A6%E6%A0%BC%E7%BD%91%E7%AB%99%E8%B5%84%E6%BA%90/…/<file>.pdf'
  #   → HTTP/2 200，content-type: application/pdf，content-disposition: attachment
  ```
  **结果形态**：`shuge.org` 是 HTML（WordPress）；`hanjihebi.com` 是 **OpenList JSON**（`{"code":200,"message":"success","data":{content:[…]}}`，字段 `name/parent/is_dir/size/modified/type`）。网盘选择页 `f.shuge.org/dl/…` 的按钮是**前端 JS 用 URL 查询参数拼出来的**（`pan/ay/hb/g/o` 是各网盘的签名参数），curl 只能拿到空壳 → 要网盘链接就用浏览器。
- 覆盖：
  - 内容：**公共版权古籍善本**为主（书名+版本+繁简书目信息+高清 PDF），另有绘画/书法/碑拓/舆图/老照片。
  - 规模：`/api/fs/list` 顶层有「**书格网站资源**」「卷轴画」「压缩包」等目录；单文件常为 100 MB–1 GB 级（实测《古逸丛书03.论语》545 MB）；按主题分档（经史子集/丛书/类书/专题系列）。
  - 更新：站点持续更新（书页有「更新记录」，如"2021-02-20 更新为高清+无水印版本"）；存储目录 `modified` 一路到 2026-04。
  - 每条书页标注**文件格式/大小/分卷书签**与**来源馆**（提要常引用日、美等馆藏，如 `dl.ndl.go.jp`、`digital.archives.go.jp`、普林斯顿、大都会等）。
- 门槛：
  - **免费、无需注册**。`?s=` 检索、`/view/` 书页、`hanjihebi` 存储 API 与 `/d/` 直下均匿名可用（实测）；API **不需要 Referer**（带不带都 200），示例里带 Referer 只是跟浏览器一致。
  - 网盘下载（百度/夸克/豆包等）需**对应网盘账号**，但**可绕开**——直接去 `hanjihebi` 存储取原文件。
  - **版权/使用边界（站点 `Readme.md` 原文口径）**：分享内容**限定为公共版权领域书籍**（参照标准伯尔尼公约）；资源来源于世界各图书馆/机构的公开内容，部分经重新编辑整理；**不会在已发布资源上声明新版权，不加水印、不做文件加密**，"鼓励大家自由再加工、再创造、再发布"；**建议再发布时保留文献来源链接**（署名/溯源是道德要求，非强制许可条款）；站点设有 **CC0授权** 分类页（`/collection/…`，菜单可见）。⚠️ 使用边界：仍应**核对单本书的原始馆藏权利声明**（个别馆藏可能另有条件）；商用前自行确认底本权利状态。
- 实测：2026-10-03，macOS 27（arm64），curl 8.x，桌面 Chrome UA。① `GET https://www.shuge.org/` → **200 / 138 KB**，WordPress 站；分类链接 20+ 条。② `GET https://www.shuge.org/?s=论语` → **200 / 75 KB**，`<title>「论语」的搜索结果 – 书格</title>`，命中 `/view/lun_yu_zhu_shu/`、`/view/lun_yu_ji_shuo/` 等。③ `GET /view/lun_yu_zhu_shu/` → 200 / 180 KB，`<title>论语注疏 – 书格</title>`；正文给出「文件格式 PDF 高清+ / 原色 1.02G / 黑白 62.2M」；下载按钮 `<a href='https://s.shuge.org/lyzss'>下载链接</a>`。④ `GET https://s.shuge.org/lyzss` → **302** → `https://f.shuge.org/dl/4/?n=论语注疏…&pan=…&ay=…`；跟随 → **200 / 4.8 KB**，`<title>请选择网盘下载</title>`（按钮由 `script.js` 渲染）。⑤ `GET https://shuge.hanjihebi.com/` → **200**，`<title>书格存储</title>`，`<meta name="generator" content="OpenList">`。⑥ `POST /api/fs/list {"path":"/","per_page":10}` → **200**，返回 `Readme.md`、`书格网站资源`(dir)、`卷轴画`(dir)、`压缩包`(dir)。⑦ `POST /api/fs/search {"keywords":"论语"}` → **200**，命中 `/书格网站资源/哲学经学/十三经注疏.三百三十五卷/十三经注疏.10.论语注疏…pdf`(281 MB)、`/书格网站资源/综合类/古逸丛书…/古逸丛书03.论语…pdf`(545 MB)。⑧ `GET /d/Readme.md` → 200，拿到版权说明全文。⑨ `HEAD /d/古逸丛书03.论语…pdf` → **HTTP/2 200**，`content-type: application/pdf`，`content-length: 545524176`，`content-disposition: attachment`。
- 上游：https://www.shuge.org/ ；存储 https://shuge.hanjihebi.com/ ；Readme https://shuge.hanjihebi.com/d/Readme.md

## 细节

### 入口表

| 用途 | URL |
|---|---|
| 首页 / 分类 | `https://www.shuge.org/` ；分类 `https://www.shuge.org/collection/<类>/` |
| **站内搜索（HTML）** | `https://www.shuge.org/?s=<关键词>` |
| 书页（详情+下载入口） | `https://www.shuge.org/view/<slug>/`，例 `/view/lun_yu_zhu_shu/` |
| 下载短链 | `https://s.shuge.org/<短码>`（例 `https://s.shuge.org/lyzss`）→ **302** → `https://f.shuge.org/dl/4/?n=…&d=…&pan=…&ay=…&hb=…&o=…`（网盘选择页） |
| **全站存储（公开目录）** | `https://shuge.hanjihebi.com/`（OpenList） |
| 存储列目录 API | `POST https://shuge.hanjihebi.com/api/fs/list` |
| **存储文件搜索 API** | `POST https://shuge.hanjihebi.com/api/fs/search` |
| 原文件直下 | `https://shuge.hanjihebi.com/d/<path>` |
| 相关子站 | `https://tools.hanjihebi.com/`；硬盘直递 `https://www.shuge.org/foryou/disk_express/` |

## 坑

1. **下载短链会失效**（书页评论里常见"链接不能直接下载了，劳您补一下"），但 `hanjihebi` 存储里通常还有 → 优先用存储路径。
2. `s.shuge.org` 只是跳转，真正的网盘参数在 `f.shuge.org/dl/…?pan=…` 查询串里，**JS 渲染**，别指望 curl 拿到网盘直链。
3. `/api/fs/list`、`/api/fs/search` 需要 `path`/`parent` 用**中文原样路径**（UTF-8），不要先 percent-encode（`/d/` 直下才需要 encode）。
4. 大文件（几百 MB–1 GB）走 `/d/` 支持 Range，可断点续传；请控制并发，站点挂在 Cloudflare 后面。
5. 存储目录与站点书页**不是一一命名**，用 `fs/search` 的关键词可能命中同一书的多版本；下载前用书页确认版本。
