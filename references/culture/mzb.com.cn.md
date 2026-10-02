# mzb.com.cn —— 民族宗教资讯检索

- 去哪找：**中国民族宗教网**（中国民族报社主办，国家民委直属）`https://www.mzb.com.cn/`；检索入口 `http://www.mzb.com.cn/search/search`（TRS WAS5，实际由 `/was5/web/search` 处理）。
- 什么时候用：要**民族/宗教领域的新闻报道与深度文**（民族政策解读、民族文化、宗教中国化、边疆发展、人物报道）；要按关键词回看某议题的历史报道；作为国家民委/宗教口径的**媒体侧**补充（正式引用回 `neac.gov.cn.md` / `sara.gov.cn.md`）。
- 怎么搜：TRS WAS5 GET 检索页，**须先取首页 Cookie（JSESSIONID）**，否则 302；再带搜索表单内置的 `token`/`channelid`：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
  curl -sS -A "$UA" --compressed -c /tmp/mzb.jar -b /tmp/mzb.jar -o /dev/null 'http://www.mzb.com.cn/'
  curl -sSL -A "$UA" --compressed -c /tmp/mzb.jar -b /tmp/mzb.jar \
    -H 'Referer: http://www.mzb.com.cn/' \
    'http://www.mzb.com.cn/search/search?token=84.1611214997343.84&channelid=259355&orderby=RELEVANCE&searchword=%E4%BD%9B%E6%95%99'
  # → 200，HTML，正文含「找到相关新闻168篇」
  ```
  结果形态：**服务端渲染 HTML**（标题 + 摘要 + 发布时间）；`searchword` 为关键词（URL 编码），`orderby=RELEVANCE`（另有按时间），`channelid` 缺省会报「未指定任何操作的频道 1001」。分页在结果页内以 WAS5 链接翻。
- 覆盖：民族与宗教两线的日常稿源（时政、文化、宗教团体、地方民族工作、人物），更新按日；粒度=单篇稿件，正文为静态 HTML 详情页。
- 门槛：**免费、免登录**；非纯 stateless——必须持 Cookie，`token` 随首页刷新而变化。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA——`GET https://www.mzb.com.cn/` → **200**（32 KB，`<title>首页 - 中国民族宗教网</title>`）；无 Cookie 直连 `/search/search?…` → **302**（192 B，tengine）；带首页 Cookie 后 `searchword=佛教` → **200**，正文「找到相关新闻168篇」，命中年份跨 2026-08～2026-09；浏览器直连同 URL 亦可（标题 `TRS WAS 5`）。
- 上游：<http://www.mzb.com.cn/>（中国民族报社）；检索由 TRS WAS5（`/was5/web/search`）提供。

## 细节

- 首页检索表单隐藏字段（`view-source` 可见）：`token=84.1611214997343.84`、`channelid=259355`、`orderby=RELEVANCE`，可见字段 `searchword`。
- WAS5 结果页支持「任何地方 / 标题 / 正文」与「按相关度 / 按时间」；对应参数名页面内可见。
- 站内另有会员登录表单 `POST /servlet/Login`（读稿无需登录）。

## 坑

1. **不持 Cookie 必 302**：直接打 `/search/search` 会被 tengine 跳回，需先请求首页取 `JSESSIONID`（`/was5` 路径）。
2. `token` 值随首页刷新变动，硬编码会随改版失效；稳定做法是每次先抓首页再拼参数。
3. `channelid` 写错返回「提示编号 1001 未指定任何操作的频道」，不是站点故障。
4. 作为**媒体转载**源，文责在报文单位；学术引用应回溯国家级原文（国家民委、国家宗教事务局）。
