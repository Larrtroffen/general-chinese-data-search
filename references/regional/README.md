# regional/ —— 区域与地方研究数据

本层收录**地方（省市）与跨省域**的社科研究数据入口：省级社科院数据平台、高校社科数据平台、地方研究机构与区域（长三角/粤港澳）数据、各省统计年鉴在线入口，以及**港澳台本地官方统计源**（香港统计处与资料一线通、澳门统计暨普查局与数据平台、台湾主计总处与政府资料开放平台）。查全国口径请回 `../stats/`；查政府开放数据平台请到 `../gov/`；查微观调查申请请到 `../surveys/`。

## 文件一览

| 文件 | 来源 | 用途/何时用 | 状态 |
|---|---|---|---|
| `sass.org.cn.md` | 上海社会科学院 | 上海地方智库成果、信息研究所数据实验室、院图书馆 | ✅ 本机实测 |
| `jsass.org.cn.md` | 江苏省社会科学院 | 江苏智库平台 + 院内可用商业数据库清单 | ✅ 本机实测 |
| `gdass.org.md` | 广东省社会科学院 | 广东省级智库与「智慧社科平台」线索 | ❌ 本机不可达 |
| `sky.zj.gov.cn.md` | 浙江省社会科学院 | 浙江社科院机构/成果；dictCode 栏目制 | ✅ 本机实测 |
| `sass.cn.md` | 四川省社会科学院 | 四川社科院（含文献信息中心）；仅 http | ✅ 本机实测 |
| `sdass.net.cn.md` | 山东社会科学院 | 山东社科院与智库联盟入口 | ✅ 本机实测 |
| `sdssdc.com.md` | 山东省社会科学数据中心 | 山东社会科学数智平台（年鉴/成果/人才）；API 需登录 | ✅ 本机实测 |
| `rdr.fudan.edu.cn.md` | 复旦大学 | 复旦社会科学数据平台（数据空间/变量检索） | ✅ 本机实测 |
| `tcdc.sem.tsinghua.edu.cn.md` | 清华大学 | 中国经济社会数据研究中心（微观数据开发） | ✅ 本机实测 |
| `econpub.xmu.edu.cn.md` | 厦门大学 | 经济学科研究共享平台（数据集/代码） | ✅ 本机实测 |
| `university-ss-data.md` | 多校 | 高校社科数据平台总表（武大/南大/人大/北大/中山…） | ⚠️ 部分上游声明 |
| `local-research-platforms.md` | 穗/深/京/沪 | 地方社科研究平台与院内数据中心总表 | ✅ 本机实测 |
| `regional-data-cn.md` | 长三角/粤港澳 | 区域数据入口（统计局指数、区域年鉴） | ✅ 本机实测 |
| `provincial-yearbooks.md` | 各省统计局 | 省级统计年鉴在线入口与 URL 规律 | ✅ 本机实测 |
| `county-portals.md` | 县级政府/统计局 | 县级官网与统计局入口规律、公报定位四步法 | ✅ 本机实测 |
| `hk-statistics.md` | 香港统计处/资料一线通 | 香港官方统计（C&SD 網上統計表 JSON API）、data.gov.hk CKAN、香港年報 | ✅ 本机实测 |
| `mo-statistics.md` | 澳门统计暨普查局/数据平台 | 澳门时间序列（REST/SOAP API）、统计年鉴、开放数据目录 | ✅ 本机实测 |
| `tw-statistics.md` | 台湾主计总处/data.gov.tw | 台湾重要经社指标、统计年鉴、开放数据目录（前端 API/CSV） | ✅ 本机实测 |

## 选路

- 要**某省社科数据/年鉴/成果**且该省有数据中心 → 山东走 `sdssdc.com.md`（需登录）；其余省社科院多为机构站，数据转 `provincial-yearbooks.md` 或 `../surveys/`。
- 要**省级统计年鉴原文** → `provincial-yearbooks.md`（先按 `tjj.<省>.gov.cn` 猜域名）；要全国/分省指标数值 → `../stats/data.stats.gov.cn.md`；要北京年鉴（扫描图片）→ `../stats/tjj.beijing.gov.cn.md`。
- 要**高校的社科数据集/变量** → 先看 `university-ss-data.md` 对照表；复旦 `rdr.fudan.edu.cn.md`、清华 `tcdc.sem.tsinghua.edu.cn.md`、厦大 `econpub.xmu.edu.cn.md` 各有专卡。
- 要**省级社科院的研究资源/院内数据库清单** → 上海 `sass.org.cn.md`、江苏 `jsass.org.cn.md`、浙江 `sky.zj.gov.cn.md`、四川 `sass.cn.md`、山东 `sdass.net.cn.md`；广东 `gdass.org.md` 本机不可达。
- 要**地方（市）研究机构或开放数据评估** → `local-research-platforms.md`（广州社科院数据中心、开放数林等）；要**政府开放数据平台本体** → `../gov/gov_opendata.md`。
- 要**长三角/粤港澳跨区域指标** → `regional-data-cn.md`（区域指数、大湾区年鉴附表）。
- 要**家庭/劳动力等微观调查**（CFDB/CHFS/CLDS 等）→ 统一走 `../surveys/`，本层只做交叉引用。
- 要**香港官方统计数值/开放数据** → `hk-statistics.md`：数值走 C&SD 網上統計表 JSON API，数据集目录走 data.gov.hk 的 CKAN API；要香港年度叙述 → 香港年報。
- 要**澳门官方时间序列/开放数据** → `mo-statistics.md`：数值走 DSEC `TimeSeriesApi`（REST）或 `TimeSeriesDatabase.asmx`（SOAP），数据集目录走 `api.data.gov.mo`。
- 要**台湾重要经社指标/开放数据** → `tw-statistics.md`：指标走总体统计资料库（`nstatdb.dgbas.gov.tw`，主计总处主站需浏览器过 Cloudflare），目录走 data.gov.tw 前端 API/CSV（免 key）。

## 相关

- 统计与区划：[`../stats/`](../stats/README.md)（`data.stats.gov.cn.md` 全国/分省指标、`tjj.beijing.gov.cn.md` 北京年鉴、`ministry-stats.md` 部委口径）。
- 微观调查：[`../surveys/`](../surveys/README.md)（CFPS/CGSS/CHARLS/CHFS/CFDB/CLDS 的申请与取数）。
- 政府开放数据平台：[`../gov/gov_opendata.md`](../gov/gov_opendata.md)（13 省级 + 27 地市开放数据门户）。
- 地方志/省情：[`../archives/local-gazetteers-cn.md`](../archives/local-gazetteers-cn.md)（31 省级方志站总表）。
- 学术文献与皮书：[`../academic/`](../academic/README.md)（`ncpssd.org.md` 全国哲社期刊库、`pishu.com.cn.md` 皮书）。
- 卡片写法与索引规范：[`../meta/style.md`](../meta/style.md)。
