# yytj.org.cn —— 医药工业统计数据与年报

- 去哪找：`https://www.yytj.org.cn/`；栏目 `/list.aspx?type={1|2|3|4|7}`；文章 `/article.aspx?id={N}`；企业直报 `/yytj/loginenter.aspx`；年报征订 `subscribeReportList.aspx`
- 什么时候用：要**医药工业**口径——统计调查制度、年度主营业务收入前 100 位企业（百强榜与解读）、医药工业出口交货值等；查《中国医药统计年报》目录与征订。
- 怎么搜：ASP.NET 查询串页面，直接改 `type` / `id`：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  curl -sS -A "$UA" 'https://www.yytj.org.cn/'                     # 首页：全部栏目 + 最新条目
  curl -sS -A "$UA" 'https://www.yytj.org.cn/article.aspx?id=585'  # 2026年医药工业统计调查制度
  ```
  结果形态：HTML（首页即完整栏目地图）；无公开 JSON API。
- 覆盖：制度文件（2024、2026 年统计调查制度）、百强榜单与解读、零散月度数据片段（如「2020年1-4月全国医药工业出口交货值」`id=556`）。
- 门槛：浏览免费；**企业直报需账号**（`loginenter.aspx`）；《中国医药统计年报》为**付费征订**（`subscribeReportList.aspx`）。
- 实测：2026-10-03 `https://www.yytj.org.cn/` → 200，50 KB，title「中国医药统计网」✅；同页可见「2024年度中国医药工业主营业务收入前100位企业解读」`article.aspx?id=601`、「2026年医药工业统计调查制度」`id=585`、「药品生产供应监测预警」`/monitor/`、直报入口 `/yytj/loginenter.aspx`。
- 上游：中国医药工业信息中心（页脚「沪ICP备16043204号-2」）。

## 细节

| 入口 | URL |
|---|---|
| 栏目列表 | `/list.aspx?type=1`（首页/要闻）、`2` 政策法规、`3` 相关下载、`4` 通知公告、`7` 新闻资讯 |
| 企业直报登录 | `/yytj/loginenter.aspx` |
| 药品生产供应监测预警 | `/monitor/` |
| 产业链供需信息平台 | `http://203.156.243.240:6002`（独立 IP 端口） |
| 《中国医药统计年报》征订 | `subscribeReportList.aspx` |

## 坑

1. 统计**数值**（分行业/分地区月度、年度）几乎都在付费年报与登录后的直报系统里，公开页只有制度、榜单与零散片段。
2. `id` 手工递增可遍历，但注意频率（≥1.5 s 间隔）。
3. `www.cpiic.org.cn`（网上常被当作医药工业信息中心站点）**域名已被他人占用，返回无关内容**，别再用。
