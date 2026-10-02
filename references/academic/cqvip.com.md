# cqvip.com —— 中文期刊论文检索

维普期刊全文库新版官网。**检索结果页为服务端渲染，curl 直取第 1 页（20 条）的题名/作者/刊名/机构/摘要可用，无需登录、无验证码；翻页与全文下载受限。**

- 去哪找：`https://www.cqvip.com/`；检索 `https://www.cqvip.com/search?k={关键词}`；详情 `https://www.cqvip.com/doc/journal/{id}?sign=…&expireTime=…`
- 什么时候用：要中文期刊论文列表/摘要/机构/核心收录；`k` 关键词足够精确时优先用（最省的匿名通道之一）；详情页可拿题名/摘要/参考文献元数据
- 怎么搜：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  curl -s -m 20 -A "$UA" -o q.html \
    'https://www.cqvip.com/search?k=%E5%9F%BA%E5%B1%82%E6%B2%BB%E7%90%86'   # k=关键词，URL 编码
  ```
  `k` 为关键词（实测即普通检索，支持词串）。返回约 480KB HTML，含 20 个结果块；解析选择器见下「细节」。
- 覆盖：维普中文期刊全文库；检索元数据/摘要（含核心收录）免费，全文/下载需会员或机构订阅；结果页为服务端渲染
- 门槛：检索元数据免费、无需登录；翻页受限（`p`/`page` 参数无效）；详情 `sign` 有时效；下载全文需登录/会员/机构订阅
- 实测：2026-10-02，macOS + curl 8.x：
  - `GET https://www.cqvip.com/` → `HTTP 200`
  - `GET https://www.cqvip.com/search?k=基层治理` → `HTTP 200 size=483882`，`<title>文献检索结果-维普官网</title>`，正则命中 `xy-start b-c-fff item` **20** 个，首条：《数字技术嵌入、基层治理演化与共同体构建——基于P县国家智能社会治理实验基地的案例研究》（石文杰、马华，《管理世界》北大核心 CSSCI CSTPCD 2026年第1期 125-139）
  - `GET /search?k=基层治理&p=2` → 200，首条与第 1 页相同（分页无效）
  - `GET https://www.cqvip.com/doc/journal/7202756460?sign=…` → `HTTP 200 size=75408`，title 含完整题名+`-文献详情-维普官网`
  - `GET https://qikan.cqvip.com/Qikan/Search/Index?key=基层治理` → `HTTP 412`
- 上游：`https://www.cqvip.com/`

## 细节

### 可用性矩阵

| 入口 | 状态 | 现象 |
|---|---|---|
| `https://www.cqvip.com/` | ✅ | HTTP 200 |
| `GET /search?k={关键词}` | ✅ | 200，HTML 内含**服务端渲染的 20 条结果**（题名/作者/刊/年卷期/页码/机构/摘要/核心收录） |
| `GET /search?k={kw}&p=2` / `&page=2` | ❌ | 200 但**仍是第 1 页**（参数被忽略；只有第 1 页在 HTML 里，后续页走站内 XHR） |
| `GET /doc/journal/{id}?sign=…&expireTime=…` | ✅ | 200，题名/摘要/参考文献元数据；下载按钮为"会员"门禁 |
| 旧站 `https://qikan.cqvip.com/Qikan/Search/Index?key=…` | ❌ | `HTTP 412` 反爬拒绝 |
| 下载全文 PDF/CAJ | ❌→登录 | 详情页下载入口需登录/会员/机构订阅 |

### 解析要点（实测选择器）

- 结果块：`<div class="xy-start b-c-fff item">`（每页 20 个）。
- 题名：块内 `class="title font-size18 FW600"`（或 `sl detail-left-title f-c-root`）。
- 每块文本含：`【期刊论文】` 类型、作者（多个）、`《刊名》`、核心收录（`北大核心 CSSCI CSTPCD`）、`年 第X期 起页-止页，共N页`、`机构：`、`摘要：`。
- 详情链接：块内 `href="/doc/journal/{resourceId}?sign=…&expireTime=…&resourceId=…&type=1"`（sign/expireTime 由服务端在结果页下发，可直接复用）。
- 尚可的纯文本提取：剥 `<script>/<style>` 再剥标签，即得每条的可读字段。

```python
import re, html
h = open('q.html', encoding='utf-8').read()
items = re.findall(r'<div class="xy-start b-c-fff item".*?(?=<div class="xy-start b-c-fff item"|$)', h, re.S)
for it in items:
    t = html.unescape(re.sub(r'\s+',' ', re.sub(r'<[^>]+>',' ', re.sub(r'<script.*?</script>','',it,flags=re.S)))).strip()
    print(t[:200])
```

## 坑

- **只出第 1 页**：`p`/`page` 参数无效；要更深结果需在浏览器里滚动/点翻页（站内 XHR），或先用更精确的 `k` 词。
- 详情页的 `sign` 有时效（`expireTime` 时间戳），结果页给的链接当场可用，隔天会失效——需要时重新检索。
- `qikan.cqvip.com` 老站已 412，别再走。
- 全文/下载为会员或机构订阅权限，检索元数据与摘要免费。
