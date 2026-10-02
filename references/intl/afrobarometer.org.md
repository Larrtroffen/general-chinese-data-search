# afrobarometer.org —— 非洲晴雨表调查

- 去哪找：门户 `https://www.afrobarometer.org/`；数据总览 `https://www.afrobarometer.org/data/`；数据集 `…/data/data-sets/`；合并数据 `…/data/merged-data/`；使用政策 `…/data/data-usage-and-access-policy/`；在线分析 `…/online-data-analysis/`。
- 什么时候用：要**非洲 30+ 国公众**的政治态度与行为（民主支持、选举、腐败、治理、公民社会、生活条件、援助感知）；做非洲比较政治、治理评估、援助效果研究。
- 怎么取：
  - 官网 `/data/data-sets/` 逐轮（Round 1–10+）下载 SPSS/Stata；**须先注册并遵守数据使用与获取政策**。
  - 变量/问卷与抽样方法在 `/surveys-and-methods/*`（questionnaire、sampling、survey-manuals）。
  - 站是 WordPress：`/wp-json/wp/v2/pages?per_page=1` 等 REST 可用来检索页面/文档（实测可用），但不直接给数据文件。
- 覆盖：Round 1 (1999–2001) → 最近一轮；35+ 个非洲国家；个体级；约 2–3 年一轮（上游声明，未本机实测）。
- 门槛：免费；**下载需注册 + 同意数据使用政策**；在线分析工具免登录。
- 实测：2026-10-03，macOS arm64，curl 8.x：`https://www.afrobarometer.org/data/` → 200 / 72.5 KB；页内实测含 `/data/data-sets/`、`/data/merged-data/`、`/data/codebooks/`、`/data/data-usage-and-access-policy/`、`/geocoded-data/`、`/online-data-analysis/`、`/surveys-and-methods/*` 等链接；`/wp-json/wp/v2/pages?per_page=1` → 200 JSON。
- 上游：`https://www.afrobarometer.org/`。

## 坑

1. 数据下载**必须注册 + 填用途**，且禁止转售/再分发；引用格式官方有规定。
2. `/data/data-sets/` 的文件由表格/JS 渲染，curl 抓不到 `.sav`/`.zip` 直链（本机实测无）。
3. 各国轮次不齐（不是每轮全覆盖）；做面板前先下官方覆盖矩阵。
4. 各国"Summary of Results"简报是**聚合结果 PDF**，不是原始微观数据。
5. 地理编码数据（geocoded）有单独的访问限制，勿与常规数据混谈。
