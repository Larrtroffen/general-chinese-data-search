# tourism —— 旅游统计与研究院口径

- 去哪找：
  - **中国旅游研究院（文化和旅游部数据中心）** `https://www.ctaweb.org.cn/`——报告栏目 `/yanjiuchengguo/`（研究成果）、`/xsjl/`（学术交流/报告发布）、`/gongzuodongtai/`（工作动态）、`/zhuantiyanjiu/`（专题研究）；**须强制 IPv4**（`curl -4`，见坑 1）
  - **文化和旅游部数据服务栏目**（数据报告：季度全国星级旅游饭店/旅行社统计调查报告、国内旅游数据）`https://sjfw.mct.gov.cn/site/dataservice/article`——Nuxt SPA，结构化取数走 `/api/`（详见 `../culture/market-stats.md`）
  - **各省文旅厅「统计信息」栏目**（抽查）：北京市文旅局 `https://whlyj.beijing.gov.cn/zwgk/zxgs/tjxx/`；湖南省文旅厅 `https://whhlyt.hunan.gov.cn/whhlyt/xxgk2019/xxgkml/tjxx/index.html`；江西省文旅厅 `https://dct.jiangxi.gov.cn/jxswhhlyt/col/tjxx/index.html`；陕西省文旅厅 `https://whhlyt.shaanxi.gov.cn/zfxxgk/fdzdgknr/tjxx/`
  - 全国口径的年度《文化和旅游发展统计公报》与季度国内出游数据见 `../culture/market-stats.md`（本卡不重复）
- 什么时候用：要**旅游市场研究报告/年度报告**（入境/国内/出境旅游发展、景区度假区、县域旅游、游客满意度）；要**分省月度或年度接待游客、旅游收入、A 级景区、星级饭店、旅行社**数据；要文化和旅游部数据中心口径的假日/季度出游解读。
- 怎么搜：省级「统计信息」多为 TRS/自建 CMS 的栏目列表（列表常 JS 渲染）+ 详情页，详情正文形态不一（PDF / HTML 表格 / PNG 图片）；研究院报告为「栏目列表 → 详情页」静态结构，改数字 ID 直取：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # 中国旅游研究院报告（务必 -4，IPv6 不通）
  curl -4 -sS -A "$UA" 'https://www.ctaweb.org.cn/gongzuodongtai/10505.html'
  # 北京市文旅局统计信息（尾斜杠；列表直接解析 PDF 链）
  curl -sS -A "$UA" 'https://whlyj.beijing.gov.cn/zwgk/zxgs/tjxx/'
  # 湖南统计信息（月度重点监测旅游区表；详情正文为 PNG）
  curl -sS -A "$UA" 'https://whhlyt.hunan.gov.cn/whhlyt/xxgk2019/xxgkml/tjxx/index.html'
  ```
  结果形态：**HTML 正文 + PDF（北京）/ PNG 图片（湖南）/ JS 渲染列表 + 登录或图片附件（江西、陕西）**；研究院为 HTML 正文、列表 JS 分页。
- 覆盖：中国旅游研究院「1+8」标志性成果（入境旅游发展年度报告已连续 14 年、国内旅游发展年度报告、出境满意度等）；部数据服务栏目按季度的星级饭店/旅行社统计调查报告与国内旅游数据；省级统计信息栏目的A级景区名录、星级饭店名单、月度重点监测旅游区统计表、假日旅游市场分析（各省起始年份不一，多为近 3–5 年滚动）。
- 门槛：**免费、免登录**（研究院、部数据服务、抽查各省均无需注册）；中国旅游研究院须走 IPv4（见坑 1）。
- 实测：2026-10-03，macOS arm64，curl 8.x，桌面 UA，20 s 超时，同主机 ≥1.5 s 间隔：
  - `curl -4 -skS https://www.ctaweb.org.cn/` → 200 / 71808 B；`-4` 后证书校验正常（`CN=ctaweb.org.cn`，2027-01-12 到期）；不加 `-4`（走 IPv6）→ 超时或 `certificate has expired`（000）。详情页 `…/gongzuodongtai/10505.html` → 200 / 22449 B，标题《中国入境旅游发展年度报告2025》出版发行（2026-05-20）；栏目 `/yanjiuchengguo/` → 200 / 20597 B（列表 JS「加载更多」）✅
  - `https://sjfw.mct.gov.cn/site/dataservice/article` → 200 / 51955 B（Nuxt SPA，含「2024年第三季度全国星级旅游饭店统计调查报告」等）⚠️ 列表 JS/`/api/` 渲染
  - 北京 `https://whlyj.beijing.gov.cn/zwgk/zxgs/tjxx`（无斜杠）→ 301 到 `/tjxx/` → 200 / 22654 B，列表含《2026年北京文化和旅游统计概览》PDF `./202609/P020260930389614168185.pdf`；该 PDF 直链 → 200 `application/pdf` 2.99 MB ✅
  - 湖南 `…/tjxx/index.html` → 200 / 36231 B；详情 `…/tjxx/202607/t20260714_34026232.html` → 200 / 29533 B，《2026年1-6月份重点监测旅游区情况统计表》，正文为 **PNG 图片**（`34026232/images/…png`）⚠️
  - 江西 `https://dct.jiangxi.gov.cn/jxswhhlyt/col/tjxx/index.html` → 200 / 182934 B（TRS，列表 JS 渲染，含「全省A级旅游景区名录」「江西省旅游星级饭店名单发布」）⚠️；陕西 `https://whhlyt.shaanxi.gov.cn/zfxxgk/fdzdgknr/tjxx/` → 200 / 38679 B（TRS `child-page.js`，列表 JS 渲染）⚠️
- 上游：中国旅游研究院（文化和旅游部数据中心）`ctaweb.org.cn`；文化和旅游部数据服务栏目 `sjfw.mct.gov.cn`；北京市文旅局 `whlyj.beijing.gov.cn`；湖南省文旅厅 `whhlyt.hunan.gov.cn`；江西省文旅厅 `dct.jiangxi.gov.cn`；陕西省文旅厅 `whhlyt.shaanxi.gov.cn`。

## 细节

### 一、源与入口（均为官方/省厅口径）

| 源 | 入口 | 口径 · 形态 |
|---|---|---|
| 中国旅游研究院（文化和旅游部数据中心） | `https://www.ctaweb.org.cn/` 各报告栏目 | 「1+8」年度报告、满意度/专题研究；**HTML 正文，列表 JS 分页** |
| 文化和旅游部数据服务栏目 | `https://sjfw.mct.gov.cn/site/dataservice/article` | 季度星级饭店/旅行社统计调查报告、国内旅游数据；**Nuxt SPA + `/api/`** |
| 北京市文旅局 · 统计信息 | `https://whlyj.beijing.gov.cn/zwgk/zxgs/tjxx/` | 年度《北京文化和旅游统计概览》；**静态列表 + PDF**，另有「历史数据查询」按年 |
| 湖南省文旅厅 · 统计信息 | `https://whhlyt.hunan.gov.cn/whhlyt/xxgk2019/xxgkml/tjxx/index.html` | 月度「重点监测旅游区情况统计表」等；**列表 JS，正文 PNG** |
| 江西省文旅厅 · 统计信息 | `https://dct.jiangxi.gov.cn/jxswhhlyt/col/tjxx/index.html` | A级景区名录、星级饭店名单、假日市场分析；**TRS，列表 JS** |
| 陕西省文旅厅 · 统计信息 | `https://whhlyt.shaanxi.gov.cn/zfxxgk/fdzdgknr/tjxx/` | 出游数据转载、A级景区名录、假期数据；**TRS，列表 JS** |

### 二、可直接拼的 URL 规律

- 中国旅游研究院报告详情：`https://www.ctaweb.org.cn/{栏目}/{数字ID}.html`（栏目如 `gongzuodongtai`/`yanjiuchengguo`/`xsjl`/`zhuantiyanjiu`）
- 北京统计 PDF：`https://whlyj.beijing.gov.cn/zwgk/zxgs/tjxx/{YYYYMM}/P0{17位}.pdf`（文件名不可猜，须从列表页解析）
- 湖南省厅详情：`https://whhlyt.hunan.gov.cn/whhlyt/xxgk2019/xxgkml/tjxx/{YYYYMM}/t{YYYYMMDD}_{id}.html`
- 江西省厅详情：`https://dct.jiangxi.gov.cn/jxswhhlyt/{分类}/{YYYYMM}/t{YYYYMMDD}_{id}.html`

### 三、省厅「统计信息」的常见栏目名（跨省找法）

不同省叫法不一：**统计信息**（湖南/江西/陕西/北京）、**数据发布**、**统计数据**、**规划计划总结**（浙江，无独立统计栏目）、**政务公开 > 法定主动公开内容**。检索式：「{省}文化和旅游厅 统计信息」「{省} 旅游统计 月报 / 国内旅游数据」，或到省统计局（`tjj.{省}.gov.cn`）找「旅游及相关产业增加值」「统计年鉴」。

## 坑

1. **中国旅游研究院 `ctaweb.org.cn` 必须强制 IPv4**：本机不加 `-4` 会走 IPv6（`240e:d9:c200:10b:85b8::8ce`）——该地址连接超时且边缘证书已过期，表现为 `curl: (60) certificate has expired` 或 20 s 超时（000）；`curl -4` 后 IPv4（`123.56.80.208`）证书正常、200。用浏览器或脚本抓时若失败，先确认走的是 IPv4。
2. **列表 JS 渲染**：研究院 `/yanjiuchengguo/`、江西、陕西的栏目列表都由 JS/TRS 模板异步填表，`curl` 只拿到空壳；改用站内检索、搜引擎结果页落详情，或对列表接口抓包。
3. **正文常是图片/PDF**：湖南统计表正文是 PNG；部分省厅把统计表做成图片或 Excel 附件——要结构化数字需 OCR 或找同期新闻稿文字版（多为「接待游客 X 万人次、旅游收入 Y 亿元」）。
4. **省厅统计 ≠ 省统计局统计**：省文旅厅栏目的接待游客/收入多为「第三方大数据/重点监测」口径，省统计局另有「旅游及相关产业增加值」等核算口径，两者**不可直接相加比对**，引用须注明来源与口径。
5. **「名录」不是流量数据**：A级景区名录、星级饭店名单是清单类，别当作客流/经营统计。
6. **中国旅游研究院 = 文化和旅游部数据中心**（同一机构两块牌子）：找「文化和旅游部数据中心」的国内出游/假日数据，落点就是 `ctaweb.org.cn` 与部数据服务栏目，不必再找独立域名。
7. 全国口径的年度统计公报与季度出游数据统一在 `../culture/market-stats.md`（文旅部财务司/统计信息栏目），跨源引用时别重复抓。
