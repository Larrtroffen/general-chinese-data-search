# osf.io —— 研究项目与预注册检索

- 去哪找：门户 `https://osf.io/`；检索台 `https://osf.io/search?q=<词>`；**API** `https://api.osf.io/v2/nodes/?filter[title]=<词>`
- 什么时候用：找**心理学 / 社科预注册与重复研究**、课题组项目页、预印本（PsyArXiv / SocArXiv）、OSF 托管的原始数据与问卷；核论文里的 OSF 链接指向什么。
- 怎么搜：
  ```bash
  curl -s 'https://api.osf.io/v2/nodes/?filter%5Btitle%5D=china&page%5Bsize%5D=2'
  curl -s 'https://api.osf.io/v2/registrations/?filter%5Btitle%5D=china&page%5Bsize%5D=2'
  # → JSON:API {"data":[{"id":"kp9jx","type":"nodes",
  #      "attributes":{"title":"Ruptured Intracranial Aneurysms … in China","description":…},
  #      "links":{…}}],"links":{"next":…}}
  ```
  - 支持 `filter[title]`、`filter[description]`、`filter[date_created]`、`filter[public]`、`page[size]` / `page[number]`、`sort`；`registrations` / `preprints` / `files` 同理。
  - **`filter[q]` 不存在**：实测 → **400** `'q' is not a valid field for this endpoint`。免费全文检索只能走网页或 SHARE。
- 覆盖：OSF 项目（nodes）/ 注册（预注册）/ 预印本 / 文件 / 用户；心理学与社科为主，条目含标题、摘要、贡献者、关联 DOI。
- 门槛：浏览与 API **免登录**；发帖 / 上传需账号。
- 实测：2026-10-03，macOS arm64，curl：`/v2/nodes/?filter[title]=china&page[size]=2` → **200**，18,686 B（首条 `kp9jx`，川大华西的动脉瘤队列研究）；`/v2/registrations/?filter[title]=china` → **200**，686 B；`/v2/search/?q=china` → **404**；`/v2/nodes/?filter[q]=china` → **400**。
- 上游：`https://osf.io/`（COS 运营，API v2，JSON:API 规范）

## 坑

- 网页 `https://osf.io/search/` 的全文检索由 **SHARE** 驱动（`share.osf.io/api/v2/search/creativeworks/_search`）；本机 20s 超时未通（上游声明，未本机实测）。
- 高价值内容多在 `registrations`（预注册）而非 `nodes`（普通项目），两者要**分别查**。
- JSON:API 格式：结果在 `data[]`，翻页连接在 `links.next`，别按扁平数组解析。
