# cia.org.cn —— 中国信息年鉴在线指标

- 去哪找：`http://www.cia.org.cn/data/data_index.htm`（全国信息化基础数据指标）；同目录 `dq_index.htm`（各地区）、`gj_index.htm`（国际信息化统计数据指标）；订阅入口 `/dingyue_shuju.html`
- 什么时候用：要**信息化 / 电子信息产业口径**的长序列：电子信息产业、通信业、广播电视业、计算机与网络、科研与信息化人才五大类近 60 个指标。
- 怎么搜：静态页面直取：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  curl -sS -A "$UA" 'http://www.cia.org.cn/data/data_index.htm'
  curl -sS -A "$UA" 'http://www.cia.org.cn/data/dq_index.htm'
  ```
- 覆盖：1998 年至今；全国 / 各省、自治区、直辖市、计划单列市 / 国际组织与各国；年度粒度，五大类近 60 指标（页面自述）。
- 门槛：指标入口页免费；完整数据订阅入口为 `/dingyue_shuju.html`（**是否付费未验证**）。
- 实测：2026-10-03 `data_index.htm` → 200，42.5 KB；`dq_index.htm` → 200，41.2 KB；两页均为同一「中国信息年鉴 信息化基础数据」框架（含三类入口链接），title「中国信息年鉴」✅。
- 上游：中国信息年鉴（`www.cia.org.cn`）。

## 坑

1. 三个入口页共用同一模板，**指标表在页内继续跳转**，不要以为三个 URL 内容不同。
2. 完整表格大概率在订阅后（`dingyue_shuju.html`），公开页给的是指标索引；取不到时走 `../stats/cnki-data.md` 的年鉴库。
3. 页面为老式静态站，编码需 UTF-8/GB18030 双试。
