# dataverse.harvard.edu —— 社科数据集与 DOI 检索

- 去哪找：门户 `https://dataverse.harvard.edu/`；带词检索页 `https://dataverse.harvard.edu/dataverse/harvard?q=<词>`；**检索 API** `https://dataverse.harvard.edu/api/search?q=<词>&type=dataset&per_page=10`
- 什么时候用：找**中国主题的社科微观数据**（调查、选举、卫生行为、人口）、论文配套数据与复现包；要能正式引用的 `doi:10.7910/DVN/...`；找跨国调查（ANES / CCES 等）的原始数据。
- 怎么搜：
  ```bash
  curl -s 'https://dataverse.harvard.edu/api/search?q=china&type=dataset&per_page=2'
  # → {"status":"OK","data":{"q":"china","total_count":6201,"items":[
  #     {"name":"China (2013): Routine Behavioral Tracking (RBT) …","type":"dataset",
  #      "url":"https://doi.org/10.7910/DVN/FRRXHL","global_id":"doi:10.7910/DVN/FRRXHL",
  #      "description":"The purpose of the behavioral tracking survey …"}]}}
  ```
  - 参数：`q`（支持 `title:` / `authorName:` / `dsPersistentId:` 等字段前缀与布尔）、`type`（`dataset` / `file` / `dataverse`）、`subtree`（限定子库 alias）、`per_page` / `start`、`sort` / `order`、`fq`（分面）。先用 `data.total_count` 判量。
  - 取单库元数据：`GET /api/datasets/:persistentId?persistentId=doi:10.7910/DVN/FRRXHL`（含文件清单 `latestVersion.files`、许可、字段说明）；连通性探针 `GET /api/info/version`。
- 覆盖：全学科仓储，社科最厚（政治学 / 社会学 / 经济 / 公共健康）；条目分「数据集 / 文件 / 子库」三层；中国相关命中 **6,201** 条（2026-10-03）。
- 门槛：检索与元数据 API **免登录**；下载部分数据集需登录或接受使用条款；发布 / 建库需 Dataverse 账号。
- 实测：2026-10-03，macOS arm64，curl（桌面 UA，同主机 ≥1.5s 间隔）：`/api/search?q=china&type=dataset&per_page=2` → **200**，5,028 B，`total_count=6201`，首条 `doi:10.7910/DVN/FRRXHL`；`/api/info/version` → **200**，`{"version":"6.10.1","build":"iqss-4"}`；`:persistentId` → **200**，10,935 B。
- 上游：`https://dataverse.harvard.edu/`（哈佛 IQSS 运营，Dataverse 开源软件）

## 细节

| 端点 | 用途 | 匿名 |
|---|---|---|
| `GET /api/search?q=&type=dataset` | 全库检索（也可搜 file 层） | ✅ 实测 |
| `GET /api/datasets/:persistentId?persistentId=<doi>` | 单数据集元数据 + 文件表 | ✅ 实测 |
| `GET /api/info/version` | 版本 / 连通性探针 | ✅ 实测 |
| `GET /api/dataverses/{alias}/contents` | 某子库（机构库）内容 | 上游声明，未本机实测 |

- `items[].global_id` 是结果的稳定标识，`url` 是 DOI 短链。
- 同一套 API 通用于全球 Dataverse 实例，换 host 即可（如 `dataverse.ucla.edu`）。

## 坑

- `q` 是 Lucene 语法：含 `-` `:` `(` 的词要么加引号要么转义，否则会被当操作符解析出怪异结果。
- Harvard Dataverse 只是**一个实例**；不少机构数据在各校自己的 Dataverse。跨库检索用 DataCite（见 `datacite.org.md`）更全。
- 检索结果里的 `description` 可能很长，批量时用 `fields` 之类的裁剪参数（上游声明，未本机实测）或本地截断。
