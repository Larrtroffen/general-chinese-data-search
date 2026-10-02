# datacite.org —— 全球数据集 DOI 总检索

- 去哪找：Commons 检索台 `https://commons.datacite.org/`；**检索 API** `https://api.datacite.org/dois?query=<词>&resource-type-id=dataset`
- 什么时候用：**跨仓储找数据 DOI**——同一关键词在 Zenodo / Figshare / Dryad / ICPSR / 各 Dataverse 里一次搜完；用 `prefix=` 或 `client-id=` 锁定某个仓储或机构；核 DOI 元数据（作者、许可、关联论文）。也是 ICPSR 官网被 WAF 拦时的替代通道。
- 怎么搜：
  ```bash
  curl -s 'https://api.datacite.org/dois?query=china&resource-type-id=dataset&page%5Bsize%5D=2'
  # → {"data":[{"id":"10.6084/m9.figshare.34057325.v1","type":"dois",
  #     "attributes":{"doi":"10.6084/m9.figshare.34057325.v1",
  #       "creators":[{"givenName":"Tirmizhi Munkaila","familyName":"Abubakar",…}],
  #       "titles":[{"title":"Wastewater surveillance of tetr…"}],…}}],
  #    "meta":{"total":…,"page":1}}
  ```
  - 参数：`query`（Lucene 语法）、`resource-type-id`（`dataset` / `software` / `text`…）、`prefix`、`client-id`、`published`、`page[number]` / `page[size]`（**方括号要 URL 编码**）、`sort`。
  - 其他：`GET /api/clients?query=` 查注册机构（实测 `tsinghua.ngac` = China Geological Survey）；`GET /api/dois/{doi}` 取单条。
- 覆盖：DataCite 是全球 DOI 注册机构之一，覆盖数千家仓储的**数据集 / 软件 / 样本** DOI（期刊正文 DOI 在 Crossref，不在此）。
- 门槛：**免登录、无 key**（有速率限制；礼貌起见 ≤3 请求/主机、留间隔）。
- 实测：2026-10-03，macOS arm64，curl：`/dois?query=china&resource-type-id=dataset&page%5Bsize%5D=2` → **200**，8,570 B；`prefix=10.3886`（ICPSR）→ **200**，命中 `10.3886/icpsr03552.v2`；`/api/clients?query=china` → **200**。
- 上游：`https://datacite.org/`；检索台 `https://commons.datacite.org/`

## 细节

### 常用 DOI 前缀（记前缀就能直接收敛到某库）

| 前缀 | 仓储 |
|---|---|
| `10.3886` | ICPSR |
| `10.5281` | Zenodo |
| `10.6084` | Figshare |
| `10.5061` | Dryad |
| `10.7910` | Harvard Dataverse |
| `10.17616` | re3data 的仓储条目 DOI |

- `meta.total` 判量；`links.self` 回显解析后的查询，便于确认参数有没有被吃。

## 坑

- **方括号不编码 curl 直接报错**：`curl: (3) bad range in URL`。写 `page%5Bsize%5D`，或给 curl 加 `-g`。
- `query` 是全字段全文匹配，噪音大；务必配 `resource-type-id=` 或 `prefix=` 收敛。
- DataCite **不含**中文库（NBSDC / 国家数据中心多为 CSTR 标识）与期刊正文 DOI；中文源见 `nbsdc.cn.md`、`national-data-centers.md`。
