# beijing.qianlong.com —— 千龙网市级/区级稿

北京市重点新闻网站，市级与区级经验稿的权威转载源（"169 个街乡"等口径多篇在此首发/转载）。

- 去哪找：站点 `https://beijing.qianlong.com/`；文章页 `https://beijing.qianlong.com/YYYY/MMDD/{id}.shtml`
- 什么时候用：找市级/区级经验稿、通报；原文被删时的转载页
- 怎么搜：站内检索不稳定 → `web_search site:beijing.qianlong.com {关键词}`、搜狗微信搜「千龙网」；命中后 curl 直读
- 覆盖：市级/区级稿件；示例含 2018-12-10
- 门槛：无
- 实测：2026-10-02，macOS + curl，文章页静态 HTML 直读（状态见 media/README 索引）
- 上游：<https://beijing.qianlong.com/>

## 细节

- 示例：`https://beijing.qianlong.com/2018/1210/2992421.shtml`（2018-12-10"169个街乡"报道）。
- 同名稿也会被中华网（`news.china.com`，见 `news.china.com.md`）转载，可互备。
- 取正文：

  ```bash
  curl -s -m 25 -A 'Mozilla/5.0 …' 'https://beijing.qianlong.com/2018/1210/2992421.shtml'
  ```

## 坑

- 分页稿（"16 区各有妙招"等 3 页长文）注意翻页链接 `/…_2.shtml`。
