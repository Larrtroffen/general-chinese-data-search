# news.china.com —— 中华网转载通道

转载各类央媒/北京媒体稿，PC 页可直接抓，常作"原文被删/不可达"时的替代引文源。

- 去哪找：站点 `https://news.china.com/`；文章页 `https://news.china.com/zw/news/13000776/YYYYMMDD/{id}.html`
- 什么时候用：原文被删/不可达时的替代引文；与千龙网等原稿互备
- 怎么搜：`web_search`：`site:news.china.com {关键词}`；或从千龙网原稿标题反查其中华网转载页
- 覆盖：央媒/北京媒体稿转载；示例含 2018-12-09、2019-01-02
- 门槛：无
- 实测：2026-10-02，macOS + curl，文章页静态 HTML 直读（状态见 media/README 索引）
- 上游：<https://news.china.com/>

## 细节

- 示例（2018-12-09 BTV 稿）：`https://news.china.com/zw/news/13000776/20181209/34634904.html`。
- 分页稿带 `_2.html`、`_3.html` 后缀（如 2019-01-02"16区各有妙招"三页稿）。
- 取正文：

  ```bash
  curl -s -m 25 -A 'Mozilla/5.0 …' 'https://news.china.com/zw/news/13000776/20181209/34634904.html'
  ```

## 坑

- 该站偶发 JS 壳页，需确认正文节点存在。
