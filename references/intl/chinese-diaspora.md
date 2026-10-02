# chinese-diaspora —— 华侨华人与国际移民统计

- 去哪找：**美国** 普查局 ACS API `https://api.census.gov/data/{年}/acs/acs5?get=...&for=...`（变量总表 `https://api.census.gov/data/2022/acs/acs5/groups/B02015.json`）；**加拿大** 统计局 WDS API `https://www150.statcan.gc.ca/t1/wds/rest/`（表清单 `/getAllCubesListLite`，批量包 `/n1/tbl/csv/{PID}-eng.zip`）；**全球** 联合国经社部国际移民存量 `https://www.un.org/development/desa/pd/content/international-migrant-stock`；**澳洲/新西兰** ABS `https://www.abs.gov.au/census/find-census-data`、Stats NZ `https://www.stats.govt.nz/`；**研究机构** 中国侨联 `http://www.chinaql.org/`、华侨大学 `https://www.hqu.edu.cn/`（暨南大学华侨华人研究院见「坑」）。
- 什么时候用：要**各国华人/华裔人口**（血统、出生地、族裔多口径）、移民存量与流向矩阵、华人的收入/学历/职业/语言分布；做海外华侨华人规模估算、离散地（diaspora）人口地理、移民融入研究。
- 怎么搜：**美国** ACS 数据接口需**免费 key**（`&key=`），但变量元数据（`/variables`、`/groups`）免 key；**加拿大** StatCan WDS 完全免 key（GET 列清单 + POST 取元数据/数据，或直接下整表 zip）；**联合国** 无 API，只有按主题直链 xlsx。
- 覆盖：**美国** ACS 1 年/5 年，2005– 至今（州/县/普查区/都会区；上游声明）；**加拿大** 人口普查 2021（族裔/出生地/移民），另有多套长期社会表；**联合国** 移民存量多轮（页上 2017/2019/2020/2024 版均可下，双年、按目的地×原籍国）；**澳洲** 历次普查；含血统与出生地两种「华人」口径。
- 门槛：US Census API 需免费 key；StatCan WDS、UN DESA xlsx、ABS 免 key；研究机构为普通网站。
- 实测：2026-10-03，macOS arm64 curl 8.x，桌面 UA、`--compressed`、20s 超时——`api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=state:06` → `200` 但正文为 **Missing Key** 页 ❌ 无 key；同主机 `.../groups/B02015.json` 与 `.../groups/B05006.json` 免 key `200 application/json` ✅；`www150.statcan.gc.ca/t1/wds/rest/getAllCubesListLite`（GET）`200`（8,271 张表、约 5 MB JSON），`.../getCubeMetadata`（POST `[{"productId":14100360}]`）`200`，`.../n1/tbl/csv/98100351-eng.zip` `200/301,395 B` ✅；UN DESA 页 `200`，`.../undesa_pd_2024_ims_stock_by_sex_destination_and_origin.xlsx` `200/6,005,287 B` ✅。
- 上游：U.S. Census Bureau（ACS）、Statistics Canada（WDS/Census of Population）、UN DESA Population Division（International Migrant Stock）、ABS、Stats NZ、中华全国归国华侨联合会（中国侨联）、华侨大学。

## 细节

### 美国 ACS（需免费 key）：华人两口径

```bash
KEY=你的密钥
# 亚裔细分：Chinese, except Taiwanese（B02015 Asian Alone by Selected Groups）
curl -s "https://api.census.gov/data/2022/acs/acs5?get=NAME,B02015_002E&for=state:*&key=$KEY"
# 外国出生人口：按出生地（B05006 Place of Birth for the Foreign-Born Population）
curl -s "https://api.census.gov/data/2022/acs/acs5?get=NAME,B05006_050E&for=state:*&key=$KEY"
```

| 变量 | 含义 |
|---|---|
| `B02015_002E` | 亚裔（单独）·Chinese, except Taiwanese |
| `B05006_049E` | 外国出生·亚洲·中国（含港澳台分项合计） |
| `B05006_050E` | 外国出生·中国（不含港澳台） |
| `B05006_051E` | 外国出生·香港 |
| `B05006_052E` | 外国出生·台湾 |

地理层级用 `for=` 指定（`state:*`、`county:*`、`metropolitan statistical area/micropolitan statistical area:*`），交叉用 `in=`。变量/分组元数据 `https://api.census.gov/data/{年}/acs/acs5/groups/{表号}.json`（免 key）。华人的收入/教育/语言看 `S0201`（Selected Population Profile）与 `B16004`（语言使用）。

### 加拿大 StatCan WDS（免 key）

```bash
# 1) 全表清单（JSON，约 8,271 张；本地 grep "Chinese"/"visible minority"/"place of birth"）
curl -s 'https://www150.statcan.gc.ca/t1/wds/rest/getAllCubesListLite'
# 2) 取某表元数据（POST JSON 数组）
curl -s -X POST -H 'Content-Type: application/json' \
  -d '[{"productId":98100351}]' 'https://www150.statcan.gc.ca/t1/wds/rest/getCubeMetadata'
# 3) 整表下载（CSV/SDMX zip；PID 去掉连字符）
curl -sLO 'https://www150.statcan.gc.ca/n1/tbl/csv/98100351-eng.zip'
```

华人相关常用表（Census 2021，`98-10-xxxx`）：

| PID | 内容 |
|---|---|
| `98100302` | 移民身份/移民期 × 出生地 × 公民身份 |
| `98100307` | 移民身份/移民期 × 出生地 |
| `98100308` | 可见少数族裔 × 移民身份 × 移民期 |
| `98100326` | 可见少数族裔 × 出生地 × 世代 |
| `98100337` | 可见少数族裔 × 族裔/文化出身 |
| `98100351` | 可见少数族裔 × 性别 × 年龄 |

WDS 亦支持 `getSeriesInfoFromCubePidCoord`（按坐标取序列）与 `getFullTableDownloadCSV`。

### 联合国 DESA 国际移民存量（无 API，xlsx 直链）

系列页 `https://www.un.org/development/desa/pd/content/international-migrant-stock`。2024 版直链：

- `.../undesa_pd_2024_ims_stock_by_sex_and_destination.xlsx`（按目的地）
- `.../undesa_pd_2024_ims_stock_by_sex_and_origin.xlsx`（按原籍）
- `.../undesa_pd_2024_ims_stock_by_sex_destination_and_origin.xlsx`（**原籍×目的地矩阵**，6 MB）

双年轮次；页上可直下 2017/2019/2020/2024 版（文件名含年份，规律同名）。中国（原籍）在各国存量以此矩阵取。

### 研究机构

- **中国侨联** `http://www.chinaql.org/`（200）：政策、侨情动态、华文教育；无结构化统计接口。
- **华侨大学** `https://www.hqu.edu.cn/`（200）：华侨华人研究；其华侨华人研究院子域 `hqhr.hqu.edu.cn` 本机 **DNS 无解析**。
- **暨南大学华侨华人研究院**：见「坑 4」。

## 坑

1. **「华人」三口径不可混**：美国的 *ancestry/ethnicity*（自报血统）、*race/Asian-alone*（种族细分，B02015）、*foreign-born place of birth*（出生地，B05006）给出的人数差异很大；做海外华人总量必须先声明口径。
2. **US Census API 已全面要求 key**：数据端点无 key 返回 `Missing Key` HTML（不是 401）；变量/分组元数据仍免 key。key 免费、即时申请。
3. StatCan WDS 是 **POST JSON 数组**（`[{"productId":…}]`），不是表单；`getAllCubesListLite` 返回约 5 MB，别每次全量拉，落盘后本地检索；整表 zip 的 PID 用**去掉连字符**的 8 位数（`98-10-0351-01` → `98100351`）。
4. **暨南大学华侨华人研究院** `https://hqhr.jnu.edu.cn/` 返回 200 但正文为 954 B 跳转页，重定向到 `auth7.jnu.edu.cn/wechat_auth/...`（微信/校内统一认证）——**需登录/仅浏览器**，无法直接抓取。
5. 联合国 DESA 移民存量是**双年**、且「stock」是在某时点的存量快照，不是年度流量；原籍×目的地矩阵可跨表核对中国维度。
6. ABS 出生地与血统两口径、Stats NZ API（`api.stats.govt.nz`）本机 `502`、门户站 200；跨国移民可比口径的同层卡片见 `worldbank.org.md`、`dbnomics.world.md`、`uis.unesco.org.md`。
