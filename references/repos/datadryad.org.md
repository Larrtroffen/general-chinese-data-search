# datadryad.org —— 论文配套数据的 DOI 仓储

- 去哪找：门户 `https://datadryad.org/`；检索页 `https://datadryad.org/search?q=<词>`；**检索 API** `https://datadryad.org/api/v2/search?q=<词>&per_page=10`
- 什么时候用：找**期刊论文的配套原始数据**（生态 / 进化 / 生物为主，也有社科）；核论文 data availability 声明指向哪里；要 `10.5061/dryad.*` 这类 DOI。
- 怎么搜：
  ```bash
  curl -s 'https://datadryad.org/api/v2/search?q=china&per_page=2'
  # → {"count":2,"total":3949,
  #    "_links":{"next":{"href":"/api/v2/search?page=2&per_page=2&q=china"}},
  #    "_embedded":{"stash:datasets":[{"_links":{"self":{"href":"/api/v2/datasets/doi%3A10.5061%2Fdryad.4qrfj6qgm"},
  #       "stash:versions":{…},"stash:version":{…},…},…}]}}
  ```
  - 参数：`q`、`page`、`per_page`。`total` 判量、`_embedded["stash:datasets"]` 是结果数组、`_links.next` 翻页。
  - 取单数据集：`GET /api/v2/datasets/{URL编码DOI}`——`:` 与 `/` 都要编码（`doi%3A10.5061%2Fdryad.…`）；版本链 `…/versions`，具体版本 `/api/v2/versions/{id}`。
- 覆盖：Dryad 成立于 2008，以期刊 / 机构投稿为主；条目 = 数据集 + 文件清单 + 关联论文 + 许可（多为 CC0）。
- 门槛：检索与元数据 **免登录**；下载公开数据集免登录。
- 实测：2026-10-03，macOS arm64，curl：`/api/v2/search?q=china&per_page=2` → **200**，15,103 B，`total=3949`；`/api/v2/datasets/doi%3A10.5061%2Fdryad.4qrfj6qgm` → **200**，7,314 B，`_links` 里含 `stash:download`。
- 上游：`https://datadryad.org/`（非营利 Dryad，California Digital Library 托管）

## 坑

- DOI 必须 URL 编码后再放进路径；直接写 `doi:10.5061/dryad.xxx` 会 404。
- 生态 / 进化是主体，**社科数据少**——社科优先 Harvard Dataverse / ICPSR。
- `q` 的匹配面较窄（标题 / 作者 / 摘要类字段），找不全时配合 DataCite `prefix=10.5061` 交叉查。
