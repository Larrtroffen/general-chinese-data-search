# xepaper.com —— 密云报等数字报

密云报等区报的数字报托管平台，页面为静态 HTML，可直接 curl。

- 去哪找：站点 `https://xepaper.com/`；文章页 `https://xepaper.com/myb/html/YYYY-MM/DD/content_B_N.htm`
- 什么时候用：按日期取密云等区报逐期报道（如密云区吹哨报到配套文件）
- 怎么取：无站内搜索 → 已知日期构造版面目录 `https://xepaper.com/myb/html/YYYY-MM/DD/node_N.htm` 解析文章链接；已知内容线索则用搜狗微信/搜索引擎搜"密云报 + 关键词"再回本站取原文
- 覆盖：密云报等区报（各频道标识不同）；示例含 2018-09/10
- 门槛：无
- 实测：2026-10-02，macOS + curl，文章页静态 HTML 直读（状态见 epaper/README 索引）
- 上游：<https://xepaper.com/>

## 细节

- URL 规则：`myb` = 密云报频道标识；`YYYY-MM` = 年月；`DD` = 日；`B` = 版面号；`N` = 该版第 N 篇文章。
- 示例：`https://xepaper.com/myb/html/2018-09/26/content_1_1.htm`（2018-09-26 第 1 版第 1 篇）、`https://xepaper.com/myb/html/2018-10/23/content_2_1.htm`。
- 密云区吹哨报到配套文件（《工作办法》先行试行单位名单等）即出自密云报 2018-09-26。
- 取正文：

  ```bash
  curl -s -m 25 -A 'Mozilla/5.0 …' 'https://xepaper.com/myb/html/2018-09/26/content_1_1.htm' | iconv -f gb18030 -t utf-8
  ```

## 坑

- 正文在页面主体 `<div class="…content…">`，按实际结构提取。
- 该站其他频道（其他区报）频道标识不同，先访问 `xepaper.com` 首页看频道目录。
