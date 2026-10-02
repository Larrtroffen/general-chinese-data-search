# zenodo.org —— 全学科开放仓储与 DOI 记录

- 去哪找：门户 `https://zenodo.org/`；检索页 `https://zenodo.org/search?q=<词>`；**检索 API** `https://zenodo.org/api/records?q=<词>&size=10`
- 什么时候用：找带 `10.5281/zenodo.*` DOI 的**数据集 / 软件 / 图像 / 预印本**；欧洲项目（Horizon 等）的产出；代码与论文补充材料的长期存档记录；用 DOI 做正式引用。
- 怎么搜：
  ```bash
  curl -s -A 'curl/8.7.1' 'https://zenodo.org/api/records?q=china&size=2&sort=mostrecent'
  # → {"hits":{"total":…,"hits":[{"id":16448450,"doi":"10.5281/zenodo.16448450",
  #     "conceptdoi":"10.5281/zenodo.16448449","doi_url":"https://doi.org/10.5281/zenodo.16448450",
  #     "metadata":{…},"links":{…}}]}}
  ```
  - 参数：`q`（支持 `resource_type:dataset` / `access_right:open` / `communities:` / `creators.name:` 等前缀）、`size`、`page`、`sort`（`mostrecent` / `bestmatch`）。响应在 `hits.hits[]`，总量在 `hits.total`。
  - 取单条：`GET /api/records/{id}`；换引用格式加 `Accept: application/vnd.citationstyles.csl+json`（上游声明，未本机实测）。
- 覆盖：全学科、全球；Zenodo 由 CERN 运营（2013 起）；条目含数据集 / 软件 / 图像 / 论文 / 预印本，每条带 DOI 与 `conceptdoi`（版本族锚点）。
- 门槛：检索与元数据 API **免登录**；公开记录下载免登录；上传需账号（ORCID 可登）。
- 实测：2026-10-03，macOS arm64，`curl -A 'curl/8.7.1' 'https://zenodo.org/api/records?q=china&size=1&sort=mostrecent'` → **200**，12,448 B，`hits.hits[0].doi=10.5281/zenodo.16448450`。
- 上游：`https://zenodo.org/`（CERN 运营，InvenioRDM）

## 坑

- **桌面浏览器 UA 会被 WAF 403**：返回 `403 Forbidden … Access to this resource has been restricted due to unusual traffic from your network`（实测同一 URL 桌面 UA 403、`curl/8.7.1` UA 200）。脚本里别伪装浏览器，用默认 curl UA 反而通。
- 换到 `/api/communities` 等其它路径时同样按上条规律试两次 UA。
- `q` 里 `:` 是字段前缀语法；中文关键词直接写即可（无需转义）。
