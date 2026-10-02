# realestate —— 房地产指标与住房数据

- 去哪找：
  - **70 个大中城市住宅销售价格指数** → 走 `../stats/nbs-api-skills.md`（住宅价格指数 `cid=3eb43764c74741469b745c396cf002d1`、大中城市 `daCid=44016f1bffeb4ea49fe34e100c6415fb`）与 `../stats/data.stats.gov.cn.md`（下钻→取数流程），本卡不重复
  - **房地产开发投资 / 商品房销售** → 国家统计局「国家数据」`https://data.stats.gov.cn/dg/website/publicrelease/web/external/`（搜索接口 `…/external/query?search=…`）
  - **全国住房公积金年度报告**（住建部+财政部+人民银行）→ 住建部文章 `https://www.mohurd.gov.cn/tsgb/wjk/art/2025/art_309206552.html`（2024 年度）；文件库栏目 `https://www.mohurd.gov.cn/tsgb/wjk/index.html`；国务院政策文件库镜像 `https://www.gov.cn/zhengce/zhengceku/202506/content_7026110.htm`
  - **房企销售榜**：中指云 `https://www.cih-index.com/rank/company.html`、报告 `/report/detail/{id}.html`、新闻 `/news/{YYYY-MM-DD}/{id}.html`；克而瑞 `https://www.cric.com/`
  - 相邻口径：房地产市场与企业数据 `./fangchan.com.md`；建设统计年鉴 `./construction-realestate.md`；月度房地产投资与销售 `../stats/data.stats.gov.cn.md`
- 什么时候用：要 70 城房价指数、房地产开发投资/新开工/竣工/销售面积与销售额、**公积金缴存与贷款**、房企月度销售排名，做房地产周期、房贷与公积金政策、土地财政联动研究时。
- 怎么搜：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # ① 统计局关键词定位指标（拿 indic_id/cid，再按 ../stats/data.stats.gov.cn.md 用 stream/esData 取数）
  curl -sS -A "$UA" -H 'client: pc' -G --data-urlencode 'search=房地产开发投资' \
    --data-urlencode 'pagenum=1' --data-urlencode 'pageSize=15' \
    'https://data.stats.gov.cn/dg/website/publicrelease/web/external/query'
  # ② 住建部公积金年报：文章页解析 api-gateway 附件链（fileUrl 为页面加密串，不可猜）
  curl -sS -A "$UA" 'https://www.mohurd.gov.cn/tsgb/wjk/art/2025/art_309206552.html' | grep -o 'document/download?fileUrl=[^"]*'
  # ③ gov.cn 镜像：正文页 + 同目录 P0*.pdf
  curl -sS -A "$UA" 'https://www.gov.cn/zhengce/zhengceku/202506/content_7026110.htm' | grep -o 'href="\./P0[^"]*\.pdf"'
  ```
  结果形态：①②纯 JSON；③HTML 正文 + PDF 附件。公积金年报正文是文字报告（缴存/提取/贷款数据写在文中），**没有随附 xls**。
- 覆盖：70 城指数 = 月度（环比/同比/定基，见 `../stats/`）；房地产投资与销售 = 月度/年度、全国 + 分省；公积金年报 = 全国年度（住建部口径，2015 年起逐年）+ 各省/市年报；房企销售榜 = 月度/累计 TOP100/TOP200（中指、克而瑞两家）。
- 门槛：统计局、住建部、gov.cn 均 **免费免登录**；中指云榜单页有「登录/注册/试用」，CREIS 中指数据库与克而瑞 CRIC 数据库为**付费**产品。
- 实测：2026-10-03，macOS arm64，curl 8.x，桌面 UA，20 s 超时，同主机 ≥1.5 s 间隔：
  - `GET mohurd.gov.cn/tsgb/wjk/art/2025/art_309206552.html` → 200 14,138 B，title《住房城乡建设部　财政部　中国人民银行 关于印发〈全国住房公积金2024年 年度报告〉的通知》，正文含 `href="/api-gateway/jpaas-web-server/front/document/download?fileUrl=<加密串>&fileName=全国住房公积金2024年年度报告.pdf"` ✅
  - `GET mohurd.gov.cn/tsgb/wjk/index.html` → 200 1,957 B（**gzip 压缩，须 `--compressed`**），title「文件库及其他」，HTML 内无条目（列表 JS 渲染）⚠️
  - `GET gov.cn/zhengce/zhengceku/202506/content_7026110.htm` → 200 27,171 B，附件相对链 `./P020250601601759182303.pdf`；`HEAD https://www.gov.cn/zhengce/zhengceku/202506/P020250601601759182303.pdf` → 200 `application/pdf` ✅
  - `GET data.stats.gov.cn/…/external/query?search=房地产开发投资&pageSize=15`（`-H 'client: pc'`）→ 200，年度数据·全国·2025 = `82788.14` 亿元，`indic_id=81437724813c4a8285c1833ce31f01bb` ✅
  - 同接口 `search=商品房销售面积` → 200，「新建商品房销售面积 (万平方米)」全国 2024（`indic_id=6bb57c9d2b564dc2ac0313e2aaf7cd0c`）✅
  - 中指云 `GET www.cih-index.com/rank/land.html` → 200 120,715 B（含登录/注册/试用，榜单数字不在 HTML）⚠️；企业榜/报告/新闻 URL 来自检索命中（`/rank/company.html`、`/report/detail/109854.html`、`/news/2025-10-31/53752628.html`），未逐个打开
  - 克而瑞 `GET http://www.cricchina.com/research/` → 301 → `https://www.cric.com/` 200 4,777 B（Nuxt SPA + 阿里验证码，无内容）⚠️
- 上游：住房和城乡建设部 `mohurd.gov.cn`；财政部、中国人民银行（公积金年报联合发布方）；中国政府网 `gov.cn`；国家统计局 `data.stats.gov.cn`；中指研究院 `cih-index.com`；克而瑞 `cric.com`。

## 细节

### 全国住房公积金年度报告 —— 三条取法与 PDF 直链规律

| 渠道 | 页面形态 | 附件直链规律 |
|---|---|---|
| 住建部（首发） | `https://www.mohurd.gov.cn/tsgb/wjk/art/{YYYY}/art_{hash}.html` | `https://www.mohurd.gov.cn/api-gateway/jpaas-web-server/front/document/download?fileUrl=<页面加密串>&fileName=<URL编码的报告名>.pdf` |
| 国务院政策文件库（镜像） | `https://www.gov.cn/zhengce/zhengceku/{YYYYMM}/content_{id}.htm` | 同目录相对链 `./P0{20位}.pdf` → `https://www.gov.cn/zhengce/zhengceku/{YYYYMM}/P0{…}.pdf`（2022 年及更早：`…/{YYYY-MM}/{DD}/{id}/files/{hash}.pdf`） |
| 省级/市级（各省住建厅、公积金中心） | 各自「年度报告」栏目 | 例：北京公积金中心 `https://gjj.beijing.gov.cn/web/zwgk61/gjjndbb/`，直链 `…/{目录}/{时间戳}.pdf`；广东 `http://zfcxjst.gd.gov.cn/zfgl/zcwj/content/post_{id}.html`；云南 `zfcxjst.yn.gov.cn` |

- 覆盖年份：全国报告公开约自 2015 年度起逐年印发（2020 年度见 gov.cn `…/2022-06/28/5698068/files/5afdc2e23a004437a116c73450efacf9.pdf`，2024 年度 2025-06 印发）。**2026 年度（即 2025 年数据）报告截至本次实测尚未发布**，最新为 2024 年度。
- 报告含：缴存（实缴单位数、缴存职工数、缴存额）、提取（提取额与用途结构）、贷款（发放额/笔数、个贷率、回收）、增值收益、资产负债与支持保障性住房等。

### 房地产开发投资 / 商品房销售（国家统计局）

- 关键词定位：`GET …/external/query?search=<词>&pagenum=1&pageSize=15`，返回每条的 `indic_id`、`cid`、`treeinfo_globalid`、`dt`、`value`，可直接看到最新一期数值。
- 取数：用上面的 `cid` 走 `stream/esData`（POST JSON），流程与字段解释见 `../stats/data.stats.gov.cn.md`；分省用库码 `code=4/5/6`，房价指数用 `../stats/nbs-api-skills.md` 的常量。
- 常用检索词：`房地产开发投资`、`商品房销售面积`、`商品房销售额`、`房屋新开工面积`、`房地产开发企业到位资金`。

### 房企销售榜（商业库）

| 来源 | 入口 | 门槛 |
|---|---|---|
| 中指云 | 企业榜 `https://www.cih-index.com/rank/company.html`；月报 `https://www.cih-index.com/report/detail/{id}.html`；快讯 `https://www.cih-index.com/news/{YYYY-MM-DD}/{id}.html` | 榜单标题/解读免费，明细与 CREIS 库注册/付费 |
| 克而瑞 CRIC | 官网 `https://www.cric.com/`（SPA+验证码）；榜单 PDF `res1.cric.com/cricbiz/…pdf` | 数据库付费；榜单 PDF 常被转载（中房网 `fangchan.com`、东方财富研报 `pdf.dfcfw.com`） |
| 中房协 | `http://www.fangchan.com/data/`（见 `./fangchan.com.md`） | 报告免费、《中国房地产年鉴》付费 |

## 坑

1. **公积金年报没有 Excel**：缴存/贷款数字写在报告正文与附表中，要结构化只能自己抽；住建部文章页的附件是 PDF，且 `fileUrl` 是页面内的加密串——**只能从文章页解析，不能拼**。
2. **住建部列表页是 gzip + JS**：`/tsgb/wjk/index.html` 必须 `curl --compressed`，且 HTML 不含条目（列表异步加载），找历年报告用站内检索或搜索引擎定位 `art_{hash}.html`。
3. **gov.cn 附件是相对路径**：`./P0….pdf` 要按**文章所在年月目录**拼绝对链；2022 年前的目录层级不同（含 `{id}/files/`）。
4. **别把「70 城房价指数」与「商品房销售均价」混为一谈**：前者是国家统计局按城市编制的同质可比价格指数（走 `../stats/nbs-api-skills.md`），后者是销售额÷销售面积，口径完全不同。
5. 中指、克而瑞的月度榜单多在**次月初**发布，页面数字以图片/图表呈现，页面 HTML 抓不到数值；要数字走其数据库（付费）或媒体转载的 PDF/研报。
6. 房地产投资/销售的**月度累计口径**（统计局按月发布累计值）与年度库口径一致，但注意「1-本月累计」与「当月值」的区分，别把累计值当当月值。
7. 住房公积金是**属地管理**：全国报告只有全国合计，分城市数据要看各市公积金中心年报（栏目名多为「年度报告 / 信息披露 / 数据发布」）。
