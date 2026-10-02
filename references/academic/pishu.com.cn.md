# pishu.com.cn —— 皮书系列全文数据库

皮书数据库（社科文献出版社）：皮书系列（蓝皮书/绿皮书）全文数据库；图书详情含内容简介与目录，全文需机构订阅。

- 去哪找：检索页 `https://www.pishu.com.cn/skwx_ps/search?query={关键词}&resourceType=all&field=All&search=1&SiteID=14&firstSublibID=`；图书详情 `https://www.pishu.com.cn/skwx_ps/bookDetail?SiteID=14&ID={数字ID}`
- 什么时候用：查皮书系列（蓝皮书/绿皮书）的书名/作者/出版时间/内容简介/目录/关键词；按 ID 直取单本详情
- 怎么搜：**编码陷阱（重要）**——URL 里的 query 若用 UTF-8 直接拼会变成乱码（如"åäº¬åçå»"）；**正确做法是用浏览器打开首页 → 在搜索框内 type 关键词 → 回车**，让站点自行处理编码。结果页为 JS 渲染，curl 拿不到条目；检索实际走 `POST /skwx_ps/search/list`（参数 `q/pi/ps/t/field/lang/classifyParam/sublibID/siteID=14`），GET 版返回 `hits: 0`、`ids: []` → 必须用 POST + 关键词做一遍 URL 编码。详情页直接可读
- 覆盖：皮书系列图书/报告/图表（蓝皮书、绿皮书）；详情页元数据+目录可读，全文需机构订阅
- 门槛：详情页免费可读；检索需浏览器（编码/JS）；全文需机构订阅
- 实测：2026-10-03，macOS + curl（desktop UA）：`GET https://www.pishu.com.cn/skwx_ps/bookDetail?SiteID=14&ID=16628350` → `HTTP 200 size=159689`，`<title>北京党的建设研究报告（2025）_皮书数据库</title>`；检索接口为 2026-10-01 会话实测（未复测）
- 上游：`https://www.pishu.com.cn/`

## 细节

- 排序：相关度/出版时间/更新时间；可切"图书/报告/图表"标签；分页有"上一页/下一页"。
- 已知 ID（北京党建蓝皮书系列）：2018 卷 10130536、2021 卷 12844187、2023 卷 14789938、2024 卷 15748504、2025 卷 16628350。
- 其余卷（如 2019/2020）在检索结果中按相关度排序时靠后，需翻页或在结果里按出版时间排序查找。
- 配套公众号「皮书说」（社科文献出版社官方）：新书"报告推荐"系列文章含书名/系列/出版信息；经搜狗微信可检索到（`references/wechat/weixin.sogou.com.md` 的流程取原文）。
