# CNSDA —— 社科调查数据的检索与存档

- 去哪找：`https://www.cnsda.org/index.php`；检索页 `https://www.cnsda.org/index.php?r=projects/index`；项目页 `https://www.cnsda.org/index.php?r=projects/view&id=<ID>`。
- 什么时候用：要**一站式检索国内大型社科调查**（CGSS、CEPS、CLDS、CHIP、CFPS、CSS…）的元数据与数据申请入口；查某调查的年份、分类、负责机构、引用备注。
- 怎么搜：免登录 GET 检索，参数进查询串——`Projects[title]=<关键词>`、`Projects[cid]=<分类ID>`、`Projects[collection_date]=<执行时间>`、`Projects[geographic_coverage]=<地理区域>`，另有 `language`。
  ```bash
  curl -sk -A "$UA" 'https://www.cnsda.org/index.php?r=projects/index&Projects%5Btitle%5D=%E7%BB%BC%E5%90%88%E7%A4%BE%E4%BC%9A%E8%B0%83%E6%9F%A5'
  # → 「共14条，当前页显示第1-5条」；每页 5 条；项目链 ?r=projects/view&id=<ID>
  ```
- 覆盖：国内外社科调查项目元数据（社会变迁、人口、健康、劳动、收入、支出、家庭、教育、老年、宗教、私营企业、企业管理等分类），结果 5 条/页分页。
- 门槛：检索/元数据**免费免登录**；下载数据须按各项目自身要求注册/申请。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA：检索「综合社会调查」→ 200（14,790 B，共 14 条）；项目页 `…&id=75023529`（CLDS）→ 200（10,732 B）；**站点 TLS 证书过期**，本机须 `curl -k`。
- 上游：中国社会调查数据资料库（CNSDA）。

## 细节

- 高级搜索表单字段（实测页面源码）：`Projects[cid]`（分类列表：社会经济、家庭、劳动、收入、健康、老年、教育社会学、中国宗教…）、`Projects[collection_date]`、`Projects[geographic_coverage]`、`Projects[title]`；表单 `action="/index.php?r=projects/index"`、`method="get"`。
- 项目页字段：摘要、项目编号、DOI、网址、建立/更新时间、是否外部数据、简称、负责机构/负责人、资金来源、系列名称、引用备注、项目分类。
- 姊妹站 `cnsda.ruc.edu.cn` 本机不可达；人大新平台 `https://cssd.ruc.edu.cn/` 正承接 CGSS/CEPS/CLASS 等数据集（见 `cgss.md`）。

## 坑

- TLS 证书过期（`curl` 报 `ssl_verify_result=10`），脚本必须 `-k`/`--insecure`，否则连不上；浏览器需手动信任。
- 每页仅 5 条，翻页靠查询串；**无 JSON API，只能解析 HTML**。
- 元数据由项目方自报，部分条目更新滞后（如 CLDS 项目页停留在 2015）。
