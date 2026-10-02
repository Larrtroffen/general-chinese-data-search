# csteelnews.com —— 钢铁行业指数与行情

- 去哪找：`http://www.csteelnews.com/`；数据资讯 `/sjzx/`；行业指数 `/sjzx/hyzh/`；钢市分析 `/sjzx/gsfx/`
- 什么时候用：中国铁矿石价格指数（CIOPI）日度值、钢市行情分析、重点企业对标挖潜成本、协会会员大会与统计发布转载。
- 怎么搜：TRS 静态站，日期分目录：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  curl -sS -A "$UA" 'http://www.csteelnews.com/sjzx/hyzh/'                            # 行业指数列表
  curl -sS -A "$UA" 'http://www.csteelnews.com/sjzx/hyzh/202212/t20221230_70229.html' # 12月30日 CIOPI
  ```
  结果形态：HTML 列表 + 正文；无 API、无附件。
- 覆盖：指数与行情按日/按周发布；实测列表最新条目为 2022-12（栏目更新状态需复核）。
- 门槛：免费、无需登录。
- 实测：2026-10-03 `http://www.csteelnews.com/` → 200，114 KB；`/sjzx/` → 200，45 KB，title「中国钢铁新闻网」，含「数据资讯 / 行业指数 / 钢市分析」三子栏与带日期详情的指数条目 ✅。
- 上游：中国钢铁工业协会主管、中国冶金报社主办。

## 坑

1. 「行业指数」列表实测停在 2022-12（页面缓存或栏目停更），当期指数回 `chinaisa.org.cn.md` 的「钢材价格指数」或交易所/钢厂渠道。
2. 数据以正文形式出现，做时间序列要自行解析正文日期与数值。
3. 站点为旧版 TRS 站，页面编码与结构不统一，抓取时同时试 UTF-8 与 GB18030。
