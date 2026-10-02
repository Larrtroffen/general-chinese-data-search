# repos/ —— 数据仓储与数据集检索

本层放**研究数据的仓储 / 集市 / 目录**：当你要找的是「**数据本体**」而不是文献、也不是官方统计口径时，从这里选路。重点是各库的 **检索 API / URL 模板**——国际库多数有开放 JSON API，中文库走国家科学数据中心体系。

## 文件一览

| 文件 | 来源 | 用途 | 状态 |
|---|---|---|---|
| `dataverse.harvard.edu.md` | Harvard Dataverse | 社科数据集与 DOI 检索（`/api/search`） | ✅ 本机实测 |
| `zenodo.org.md` | Zenodo（CERN） | 全学科开放仓储与 DOI（`/api/records`） | ✅ 本机实测 |
| `datadryad.org.md` | Dryad | 论文配套数据的 DOI 仓储（`/api/v2/search`） | ✅ 本机实测 |
| `datacite.org.md` | DataCite | 全球数据集 DOI 总检索（按 prefix 收敛） | ✅ 本机实测 |
| `re3data.org.md` | re3data | 数据仓储目录（3,531 家，选仓储用） | ✅ 本机实测 |
| `osf.io.md` | OSF / COS | 研究项目与预注册检索（`filter[title]`） | ✅ 本机实测 |
| `figshare.com.md` | Figshare | 全学科成果与附件仓储 | ⚠️ 仅浏览器可达 |
| `kaggle.com.md` | Kaggle | 竞赛与社区数据集市场 | ✅ 本机实测 |
| `icpsr.umich.edu.md` | ICPSR | 社科数据档案与变量级检索 | ⚠️ 官网不可达 |
| `gesis.org.md` | GESIS | 德国社科数据与变量检索 | ⚠️ 仅浏览器可达 |
| `hf-mirror.com.md` | HF-Mirror | Hugging Face 数据集镜像检索 | ✅ 本机实测 |
| `nbsdc.cn.md` | 国家基础学科公共科学数据中心 | 基础学科数据与 CSTR 检索 | ✅ 本机实测 |
| `escience.org.cn.md` | 中国科技资源共享网 | 科技资源与数据中心总入口 | ✅ 本机实测 |
| `national-data-centers.md` | 自编（逐站探测） | 国家科学数据中心 20 家入口总表 | ✅ 本机实测 |
| `science-data-apis.md` | 自编（逐站实测） | 七大科学数据中心检索接口（天文/海洋/空间/极地/微生物/基因组/地球系统） | ✅ 本机实测 |
| `bio-global-apis.md` | 自编（逐站实测） | 国际科研数据接口（GBIF / NASA CMR / WorldClim） | ✅ 本机实测 |
| `csdata.org.md` | 中国科学数据（SciEngine） | 数据论文与配套数据集 | ⚠️ 部分可达 |

## 选路

- **不知道数据藏在哪家** → 先 `datacite.org.md` 跨库搜 DOI，再用 `prefix=` / `client-id=` 收回具体仓储。
- 找**社科 / 调查 / 微观数据** → `dataverse.harvard.edu.md`、`icpsr.umich.edu.md`、`gesis.org.md`；心理学预注册另有 `osf.io.md`。
- 找**论文配套数据**（data availability 声明指向哪） → `datadryad.org.md`、`figshare.com.md`、`zenodo.org.md`。
- 找**中文 / 国内权威数据** → `nbsdc.cn.md`；按学科定位则先 `national-data-centers.md`（再进该中心站内检索），要 curl 直连的检索接口看 `science-data-apis.md`（微生物 / 基因组 / 地球系统有 JSON API）；总入口 `escience.org.cn.md`。
- 找**物种分布 / 全球气候栅格 / 卫星对地观测** → `bio-global-apis.md`（GBIF / WorldClim / NASA CMR，均免 key 检索）。
- 找**AI 语料 / 竞赛数据集** → `hf-mirror.com.md`、`kaggle.com.md`；中文数据集市（天池 / 和鲸 / ScienceDB / ModelScope）见 `../methods/dataset-hubs.md`。
- **要先挑仓储、或核仓储资质** → `re3data.org.md`。
- 要的是**数据论文**（用论文发表数据集） → `csdata.org.md`。

## 相关

- 官方统计口径（GDP / 人口 / 年鉴等）见 `../stats/`；机构与单位信息见 `../gov/`。
- 免费数据集市与中文平台见 `../methods/dataset-hubs.md`；检索语法见 `../methods/search-syntax.md`。
- 文献与全文获取见 `../academic/`、`../methods/literature-delivery.md`；抓取 / 存档工具见 `../tools/`。
- 源清单总索引见 `../README.md`。
