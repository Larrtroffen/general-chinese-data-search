# bjdj.gov.cn —— 北京组工网文章

- 去哪找：文章页 `https://www.bjdj.gov.cn/article/{NNNNN}.html`（如 `/article/22309.html`、`/article/19322.html`）；站点首页 `https://www.bjdj.gov.cn/`。
- 什么时候用：要北京市委组织部/党建系统（吹哨报到、组工动态）的官方发布原文。
- 怎么搜：站点**没有可用的站内搜索接口**（页面为静态 HTML），三条路——
  1. 搜狗微信搜公众号「北京组工」（账号名/文章标题）；
  2. `web_search` 用 `site:bjdj.gov.cn {关键词}`（工具被限流时退化为搜索引擎直查）；
  3. 已知文章 ID 递增试探：2018 年文章 ID 约在 19000–23000 区间，可小范围枚举。
- 覆盖：北京市党建/组织系统文章；内容与「北京组工」公众号基本同源。
- 门槛：免费，curl 直读。
- 实测：原卡未记录日期（本机 curl）；`curl` 直读可取全文（见下命令）。
- 上游：北京市委组织部 `https://www.bjdj.gov.cn/`。

## 细节

```bash
curl -s -m 25 -A 'Mozilla/5.0 …Chrome…' 'https://www.bjdj.gov.cn/article/22309.html' | iconv -f gb18030 -t utf-8
```

- 页面为静态 HTML，正文在 `<div class="article-content">`（以实际页面结构为准），可直接全文抓取。
- `http://` 与 `https://` 均可；部分老文章仅 http 存活。
- 同站镜像内容也出现在人民网·中国共产党新闻网、共产党员网 12371.cn（转载路径）；12371 站内检索可用（见 `12371.cn.md`）。
- 「北京组工」公众号文章与网站文章基本同源；微信抓不到正文时，用标题在站内/站外搜网站版全文。
