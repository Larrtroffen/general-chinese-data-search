# re3data.org —— 数据仓储目录与资质核对

- 去哪找：检索台 `https://www.re3data.org/search?query=<词>`；**API 全量** `https://www.re3data.org/api/v1/repositories`；单库 `https://www.re3data.org/api/v1/repository/<id>`
- 什么时候用：**不知道数据该去哪个库找**时，先按学科 / 内容类型筛出候选仓储；核一家仓储的资质（有无 DOI、是否开放、许可、保存政策、收录起始年）；给论文挑投稿数据仓储。
- 怎么取：
  ```bash
  curl -s 'https://www.re3data.org/api/v1/repositories'                    # 全量列表（XML）
  curl -s 'https://www.re3data.org/api/v1/repository/r3d100000001'         # 单库详情（RDF/XML）
  # 列表：<list><repository><id>r3d100000001</id>
  #        <doi>https://doi.org/10.17616/R31NJCHT</doi>
  #        <name>Odum Institute Archive Dataverse</name>
  #        <link href="/api/v1/repository/r3d100000001" rel="self"/></repository>…</list>
  ```
  - 详情是 `r3d:re3data`（schema 2.2）命名空间的完整描述：学科分类、内容类型、DOI/CSTR 支持、许可、数据访问政策、收录起始年、机构信息。
- 覆盖：**3,531** 家研究数据仓储（2026-10-03 全量 XML 计数），全球、全学科；每家带 re3data DOI（`10.17616/…`）。
- 门槛：**免登录、无 key**。
- 实测：2026-10-03，macOS arm64，curl：`/api/v1/repositories` → **200**，`text/xml`，1,025,781 B，`grep -c '<repository>'` = **3531**；`/api/v1/repository/r3d100000001` → **200**，9,289 B（含 `r3d:re3data` schema 2.2 头）。
- 上游：`https://www.re3data.org/`（DataCite 与 GFZ 等联合运营）

## 坑

- **API 不支持服务端查询**：实测 `?query=china` 与 `?query=social science` 返回**同一份 1,025,781 B 全量列表**，`query=` 被忽略。筛选要么在网页检索台做，要么本地过滤全量 XML。
- v1 API **只有 XML / RDF，没有 JSON**；解析用 `xmlstarlet` 或 `python -c 'import xml.etree.ElementTree …'`。
- 它只是**目录（关于仓储的元数据）**，不存数据本体；找到目标仓储后回到该仓储自己的检索接口。
