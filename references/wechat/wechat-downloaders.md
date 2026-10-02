# wechat-downloaders —— 已有链接落地为本地文件

三个**单篇（部分整号）落地成文件**的工具合集（qiye45 / jackwener / gxcsoccer）。共同前提：**你已经有一个 mp.weixin.qq.com 链接**；
都不能按关键词检索、都不能自己列号内文章。与 `mp.weixin.qq.com.md`（裸 curl 正文）的区别是**抗风控细节 + 多格式落地 + 图片本地化**。

- 去哪找：
  - https://github.com/qiye45/wechatDownload （9.6k★，**无 LICENSE**）
  - https://github.com/jackwener/wechat-article-to-markdown （PyPI 同名 v0.1.0，1k★，**无 LICENSE**）
  - https://github.com/gxcsoccer/wechat-article-crawler （MIT，13★）
- 什么时候用：**已有链接要落地成 HTML/MHTML/MD/PDF/DOCX/CSV 或图片本地化**时；
  或要一份**「自己写正文抓取器」的抗风控参考实现**（第三个工具的要点可直接抄）。
- 怎么取：三个工具各有一套最小用法（GUI 三步 / `uv tool install` / `pip install crawl4ai`）——详见「细节」。
- 覆盖：单篇为主；qiye45 支持**整号批量**（历史消息、合集 `appmsgalbum`、评论及回复、图片/视频/音频，可按时间段/阅读量筛，**能导出阅读量/点赞/分享/评论数**）。
- 门槛：无 key；qiye45 需人工把链接在微信客户端打开取密钥；jackwener/gxcsoccer 吃公开 URL
- 实测：2026-10-02——`curl` 探活 qiye45 的远程 MCP 兜底端点（见「细节」，返回 200 与 2 个工具）；`git clone --depth 1` gxcsoccer 仓库成功（未安装 crawl4ai、未跑脚本）；jackwener 查 PyPI 元数据存在。**三个工具均未实际下载文件 / 未装 GUI**。
- 上游：https://github.com/qiye45/wechatDownload ｜ https://github.com/jackwener/wechat-article-to-markdown ｜ https://github.com/gxcsoccer/wechat-article-crawler

## 细节

### 1) qiye45/wechatDownload —— 桌面 GUI 整号批量下载（Win/macOS）

- 去哪找：https://github.com/qiye45/wechatDownload （**无 LICENSE：只作品路参考**）；Release 提供 `wechatDownload4.7.zip`（5.0 仅 tag 无附件）；Skill 目录 `skills/wechat-article-downloader/SKILL.md`；随手带一个**远程 MCP 兜底端点** `https://changfengbox.top/api/mcp`。
- 怎么取（GUI 三步）：① 复制该号任意一篇文章链接到软件 → 点「获取公众号 id」；② 把软件生成的链接**发到微信「文件传输助手」并用微信内置浏览器打开** → 自动抓密钥；③ 设置格式/时间段后下载。
- MCP/Skill 用法（`http://127.0.0.1:4545/mcp`，需在软件里勾「启动MCP」）：`single_article_download{url}`、`get_public_account_id{}`、`batch_download_articles{}`、`export_article_data{}`（本地）；远程兜底只有两个工具 `wechat{url,config}`、`wechat_collection{url,config}`。
- 门槛：核心一步**必须人工把链接在微信客户端里打开**（拿密钥）；无 LICENSE。
- 实测：`curl -sS -X POST https://changfengbox.top/api/mcp -H 'Content-Type: application/json' -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'` → **200**，返回 2 个工具：`wechat`（参数 `url,config`；描述「一键下载公众号文章/网易新闻/今日头条/360图书馆等文章链接。config 支持：HTML、MD、PDF、WORD、TXT、MHTML、文件开头添加日期」）、`wechat_collection`（参数 `url,config`，「下载微信公众号合集（appmsgalbum）」）。**未运行 GUI、未下载文件**。
- 坑：远程 MCP 会把链接交给第三方 `changfengbox.top`（敏感场景别用）。

### 2) jackwener/wechat-article-to-markdown —— CLI 单篇转 Markdown（含图片本地化）

- 去哪找：repo https://github.com/jackwener/wechat-article-to-markdown ；PyPI 包同名（v0.1.0，**无 LICENSE：只作品路参考**，1k★）；Skill 安装走 Skills CLI 或手工放 skills 目录（ClawHub 方式已废弃）。
- 什么时候用：要**干净 Markdown + 图片落地**喂 AI/知识库：输出 `./output/<标题>/<标题>.md` + `images/*`。
- 怎么取：`uv tool install wechat-article-to-markdown` → `wechat-article-to-markdown "https://mp.weixin.qq.com/s/xxxx"`；自带 Camoufox 反检测、并发下图、代码块提取（图片/SVG 渲染的代码无法还原）。
- 门槛：无 key；只吃公开 `mp.weixin.qq.com` URL。
- 实测：2026-10-02 **未安装未运行**；`curl https://pypi.org/pypi/wechat-article-to-markdown/json` → 存在，version `0.1.0`。
- 坑：单篇；上游声明「高频会触发反爬」。

### 3) gxcsoccer/wechat-article-crawler —— crawl4ai 方案的技术要点（**推荐直接抄这些要点**）

- 去哪找：https://github.com/gxcsoccer/wechat-article-crawler （MIT，13★）；`SKILL.md` + `scripts/crawl_wechat.py`。
- 什么时候用：我们要**自己写正文抓取器**时的最佳参考实现（比直接用它的脚本更有价值）。
- 要点（原文）：① UA 里带 `MicroMessenger/8.0.43`，否则被「请用微信打开」拦；② `wait_for="css:#js_content"` 等正文渲染完；③ 懒加载图 `data-src` → 注入 JS 复制到 `src`；④ `JsonCssExtractionStrategy` 选择器：标题 `#activity-name`、作者 `#js_name`、时间 `#publish_time`、正文 `#js_content`；⑤ Markdown 生成后清洗 SVG 占位图/data-URI；⑥ `mmbiz.qpic.cn` 图**防盗链**，下图必须带正确 `Referer`（`--download-images`）。
- 怎么取：`pip install crawl4ai aiohttp && crawl4ai-setup` → `python scripts/crawl_wechat.py <URL> [--download-images] [--save-markdown] [--output-dir DIR]`。
- 实测：2026-10-02 `git clone --depth 1 https://github.com/gxcsoccer/wechat-article-crawler` → 成功；读 `SKILL.md`(MIT) 与 `scripts/crawl_wechat.py` 目录项；**未安装 crawl4ai、未跑脚本**。

## 坑

- 三个工具都**只处理已知链接**（不能搜、不能列号内文章）。
- 高频会触发验证码/IP 封；临时分享链接会过期。
