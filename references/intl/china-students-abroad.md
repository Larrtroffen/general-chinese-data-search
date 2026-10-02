# china-students-abroad —— 中国学生出国留学统计

- 去哪找：**美国** IIE Open Doors `https://opendoorsdata.org/`（人用页 `https://www.iie.org/research-initiatives/open-doors/`）、国土安全部 **SEVIS by the Numbers** `https://www.ice.gov/doclib/sevis/btn/`；**加拿大** IRCC 开放数据 `https://open.canada.ca/data/api/3/action/package_search?q=study+permit+holders`（直链见「细节」）；**英国** HESA `https://www.hesa.ac.uk/data-and-analysis/students`（目录镜像 `https://ckan.publishing.service.gov.uk/api/3/action/package_show?id=44864962-e4ad-46e6-8f10-71b40126cefb`）；**澳大利亚** ABS `https://www.abs.gov.au/census/find-census-data`；**中国口径** 教育部 `http://www.moe.gov.cn/jyb_xxgk/xxgk/neirong/tongji/jytj_lxsj/`。
- 什么时候用：要**中国在某一国的留学生人数/占比/学历层次/专业/院校分布**；做国际学生流动、留学目的地变迁、中美/中英/中加/中澳教育贸易；要按国籍（country of citizenship）或出生地拆分的官方统计。
- 怎么搜：四类入口门槛不同——**美国** Open Doors 全年报在 Cloudflare 后，仅浏览器；SEVIS 是年度 PDF。**加拿大** IRCC 走 open.canada.ca 的 CKAN API，再顺 `ircc.canada.ca/opendata-donneesouvertes/data/` 直链拿 CSV/XLSX（免 key）。**英国** HESA 站与 CSV 均被 WAF 挡（403），只能浏览器。**澳洲** ABS 走网站数据包/社区档案。**中国** MOE 是政府信息公开 HTML，无接口。
- 覆盖：**美国** 1949– 至今（Open Doors 年报，1949 起；SEVIS 2011– ；两者为上游声明，本机被挡未核）；**加拿大** 2015– 至今（IRCC 月度，按国籍/省/学历层次）；**英国** 2014/15– 至今（HESA 学年表，上游声明）；**澳洲** 每次人口普查（2006/2011/2016/2021，出生地/血统）；**中国** 出国留学人员统计止于 **2019 年度**（此后 MOE 不再发布明细，仅公报总量）。
- 门槛：IRCC/开放数据 免 key；ABS、MOE 免 key；HESA 与 Open Doors 被 WAF 挡、仅浏览器；UNESCO UIS 见 `uis.unesco.org.md`（批量需 token）。
- 实测：2026-10-03，macOS arm64 curl 8.x，桌面 UA、`--compressed`、20s 超时——`opendoorsdata.org` `403`（含 `/wp-json/` 亦被 `__cf_chl_rt_tk` 挑战）❌；`www.ice.gov/doclib/sevis/btn/25_0605_2024-sevis-btn.pdf` `200/1,391,792 B application/pdf` ✅；`open.canada.ca/data/api/3/action/package_search?q=study+permit+holders` `200` 命中 75 数据集，`ircc.canada.ca/.../ODP-TR-Study-IS_CITZ.csv` `200/1,293,348 B` ✅；`hesa.ac.uk/data-and-analysis/students` `403`、`hesa.ac.uk/.../table-28.csv` `403` ❌；`www.abs.gov.au/census/find-census-data` `200`、`api.data.abs.gov.au` **DNS 无解析** ❌；`moe.gov.cn/jyb_sjzl/sjzl_fztjgb/` `200`、`moe.gov.cn/.../202607/t20260706_1442870.html`（2025 年公报）`200`。
- 上游：IIE/Open Doors（美国国务院教育与文化事务局资助）、US ICE SEVP、IRCC/open.canada.ca、HESA、ABS、中华人民共和国教育部；教育口径跨国可比另见 `uis.unesco.org.md`。

## 细节

### 加拿大 IRCC：按国籍的中国留学生（免 key，直链）

```bash
# 找数据集（CKAN，JSON）
curl -s 'https://open.canada.ca/data/api/3/action/package_search?q=study+permit+holders&rows=5'
# 直取 CSV（按国籍 citizenship；1.29 MB）
curl -sLO 'https://www.ircc.canada.ca/opendata-donneesouvertes/data/ODP-TR-Study-IS_CITZ.csv'
```

| 文件 | 维度 |
|---|---|
| `ODP-TR-Study-IS_CITZ.csv` | 学签持有人 按 国籍 × 年/月 |
| `ODP-TR-Study-IS_PT_study.csv` | 按 省/地区 × 学历层次 |
| `ODP-TR-Study-IS_PT_gender.csv` | 按 省/地区 × 性别 |
| `ODP-TR-Study-DLI_name_PT_Admin_type.csv` | 按 指定学习机构（DLI） |
| `EN_ODP_annual-TR-Study-IS_CITZ_year_end.xlsx` | 12-31 存量 按 国籍 |

月更；CSV 为**取整值**、精确计算用 XLSX。

### 美国

- **Open Doors**：`https://opendoorsdata.org/data/international-students/`（Cloudflare 挑战，浏览器打开）。年报（每年 11 月）含 `Place of Origin`（中国居首）、`Academic Level`、`Field of Study`、`Leading Institutions`；国别明细为 xlsx/PDF。
- **SEVIS by the Numbers**（ICE/SEVP）：年度 PDF，`https://www.ice.gov/doclib/sevis/btn/{YY}_{MMDD}_{年}-sevis-btn.pdf`（年→文件名映射每年变，从 `https://www.ice.gov/news/releases/` 顺链最稳）。按国籍/州/院校给 F-1/M-1 在册数，与 Open Doors 口径不同（SEVIS 为 SEVIS 系统在册快照）。

### 英国 HESA

- 站与 CSV 均为 WAF 403；`data.gov.uk` 的 CKAN 目录可 API 读到资源清单（table-28 = 非英籍学生按院校×居住国，chart-6 = 首年非英籍按居住国），但 CSV 直链同样 403。**仅浏览器**（可下后本地复用）。

### 澳大利亚 ABS

- `https://www.abs.gov.au/census/find-census-data/datapacks` 与 `/community-profiles/2021/...` 免 key 直下；按**出生地（China）**与**血统（Chinese ancestry）**两种口径，二者差异大。
- ABS SDMX API `api.data.abs.gov.au` 本机 DNS 无解析，未取；如需结构化 API 换网再试。

### 中国 MOE

- 明细系列止于 **2019 年度**：`http://www.moe.gov.cn/jyb_xwfb/gzdt_gzdt/s5987/202012/t20201214_505447.html`（此后仅《全国教育事业发展统计公报》总量，无出国/回国明细）。
- 公报索引 `http://www.moe.gov.cn/jyb_sjzl/sjzl_fztjgb/`；教育统计数据（全国基本情况）`http://www.moe.gov.cn/jyb_sjzl/moe_560/{年}/quanguo/`。

## 坑

1. **口径互不可比**：Open Doors（学年注册）≠ SEVIS（SEVIS 在册快照）≠ IRCC（年末有效学签）≠ HESA（学年注册）≠ ABS（人口普查出生地/血统）。做中国出国人数时间序列前先统一「存量/流量」「学年/日历年」「国籍/出生地」。
2. Open Doors 与 HESA 均为 **Cloudflare/WAF 挡爬**，本机 curl 403；HESA 的 `data.gov.uk` 目录能读到资源名但 CSV 仍 403。
3. IRCC CSV 是**取整值**，逐机构精确数请用对应 XLSX；文件名里含空格（如 `EN_ODP-TR-Work-IMP CITZ.xlsx`），URL 需编码。
4. MOE 的「年度出国、来华留学数据」栏目实为政策通知混排，**不要**当统计库；真正时间序列看 `jyb_xwfb/gzdt_gzdt/s5987/` 下的年度条目。
5. ABS 的**出生地**与**血统**两口径对「华人」定义不同，混用会得出不同结论。
6. 教育口径跨国可比（在校生/流动率）回 `uis.unesco.org.md`（UIS 批量需 token）。
