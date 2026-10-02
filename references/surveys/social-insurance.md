# social-insurance —— 人社医保微观与统计

- 去哪找：人社部统计公报（主域被 JS 挑战，改用 IP 镜像）`http://114.255.111.180/SYrlzyhshbzb/zwgk/szrs/tjgb/`；国家医保局「统计数据」`https://www.nhsa.gov.cn/col/col7/index.html`、医保数智库 `https://www.nhsa.gov.cn/col/col257/index.html`；全国社保基金理事会财务报告 `https://www.ssf.gov.cn/portal/xxgk/fdzdgknr/cwbg/A00100308index_1.htm`。
- 什么时候用：要**参保人数、基金收支、社保卡持卡人数、医保待遇、养老金投资业绩**等社保/医保口径数据；做社会保障、医疗保险、养老金融实证或政策研究。
- 怎么搜：人社部走 IP 镜像直取列表与 PDF；医保局 col7 是静态 HTML 列表（公报全文 + 月度指标），数智库数据走 PDF 下载接口，站内检索用 jrobot；社保基金理事会年报为 HTML 全文。全部无 API、无需 key。
- 覆盖：人社部统计公报 2017–2025（年度）；国家医保局全国医疗保障事业发展统计公报 2018–2025 + 统计快报 + 逐月「基本医疗保险统筹基金和生育保险主要指标」（2023-08 起）；医保数智库数据集 1998–2025；社保基金年度报告 2011–2025、基本养老保险基金受托运营年度报告 2017–2025（缺 2020）。
- 门槛：全部**免费、无需登录**；人社部主域 `www.mohrss.gov.cn` 需浏览器（`EO_Bot_Ssid` JS cookie 挑战），IP 镜像可 `curl`。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA（`-L`、20s 超时）——`nhsa.gov.cn/` 200（120,005 B）、`/col/col7/index.html` 200（20,048 B，`<title>国家医疗保障局 统计数据`）、`/col/col7/...` 列表含 2018–2025 公报与逐月指标、jrobot 检索 200（44,023 B）、`art_257_21405.html` 200（13,105 B，附 PDF）；`ssf.gov.cn/portal/xxgk/fdzdgknr/cwbg/A00100308index_1.htm` 200（19,017 B）、年报正文 200（43,542 B）、`sbjjndbg/A0010030801index_1.htm` 200（15,528 B）、`yljjndbg/A0010030802index_1.htm` 200（14,018 B）；**`www.mohrss.gov.cn/` 200 但仅 986 B（JS 挑战）**，`114.255.111.180/…/tjgb/` 200（15,291 B，公报列表）、`…/tjgb/202506/W020250616518526345602.pdf` 200 `application/pdf`；`chinajob.mohrss.gov.cn` 200（46,171 B）。
- 上游：人力资源社会保障部 `https://www.mohrss.gov.cn/`；国家医疗保障局 `https://www.nhsa.gov.cn/`；全国社会保障基金理事会 `https://www.ssf.gov.cn/`。部委统计总表另见 [`../stats/ministry-stats.md`](../stats/ministry-stats.md)。

## 细节

### 一、人社部（MOHRSS）：绕开 JS 挑战

| 入口 | URL | 状态 |
|---|---|---|
| 统计公报列表（IP 镜像） | `http://114.255.111.180/SYrlzyhshbzb/zwgk/szrs/tjgb/` | ✅ 200 / 15 KB |
| 公报正文（同构） | `…/tjgb/{YYYYMM}/t{YYYYMMDD}_{id}.html` | ✅ 200 |
| 公报 PDF 附件 | `…/tjgb/{YYYYMM}/W0…pdf`（例 2024 年度 = `202506/W020250616518526345602.pdf`） | ✅ 200 `application/pdf` |
| 中国就业网·数据统计 | `https://chinajob.mohrss.gov.cn/` | ✅ 200 |
| 主域 | `https://www.mohrss.gov.cn/…` | ⚠️ 986 B JS 挑战 |

- 镜像 IP 另见 `114.255.111.133`（同站另一节点）；正文页 `<div id="insMainConTxt">` 内挂 `<iframe>` 之外，公报本体是**同目录 PDF 附件**（页面只给链接，不内嵌正文）。
- 列表页实测含 **2025、2024、2023、2022、2021、2020、2019、2018、2017** 年度《人力资源和社会保障事业发展统计公报》。
- 公报指标含：城镇新增就业、基本养老/失业/工伤保险参保人数、基金收支结余、**社会保障卡持卡人数**、职业培训与技工院校等。
- 社保卡数据（人社部口径，上游声明未本机核对）：2024 年 1 月底持卡 13.8 亿；2025 年底持卡 13.9 亿（覆盖 98.9% 人口）、电子社保卡领用 11.04 亿。逐月/逐年以公报与新闻稿为准。

### 二、国家医保局（NHSA）

| 内容 | URL | 形态 |
|---|---|---|
| 统计数据栏目 | `https://www.nhsa.gov.cn/col/col7/index.html` | 静态列表 HTML |
| 全国医疗保障事业发展统计公报 | `…/art/{y}/{m}/{d}/art_7_{id}.html` | 正文 HTML（无附件） |
| 医保数智库 | `https://www.nhsa.gov.cn/col/col257/index.html` | 数据集列表 |
| 数据下载 | `…/module/download/downfile.jsp?classid=0&filename=<hash>.pdf` | PDF |
| 站内检索（jrobot） | `https://www.nhsa.gov.cn/jrobot/search.do?webid=1&pg=10&p=1&tpl=1&category=&q=<词>` | HTML 结果页 |

- col7 实测涵盖：**2018–2025 年度统计公报**（2025 年度 2026-07-16 发布；2024 年度 2025-07-14；2023 年度 2024-07-25；2022 年度 2023-07-10；2020 年度 2021-06-08；2019 年度 2020-06-24；2018 年度 2019-06-30），另有年度「统计快报」与**逐月**《基本医疗保险统筹基金和生育保险主要指标》（2024 起标题、2023 年作「运行情况」）。
- 「医保数智库」数据集（`art_257_*`）：**2012 年–2025 年医保待遇享受相关数据**（`art/2026/7/13/art_257_21405.html`）、**1998 年–2025 年全国经济人口卫生医保相关数据**（`art/2026/7/6/art_257_21309.html`）；两篇均为 PDF 附件，页面注明数据源含《中国医疗保障统计年鉴》。
- jrobot 检索示例（2026-10-03 实测 200）：`…/jrobot/search.do?webid=1&pg=10&p=1&tpl=1&category=&q=统计公报`，结果含各年度公报与新闻稿（结果里的跳转是 `/jrobot/plugin/link/show.do?url=<编码后的真实 URL>`）。

### 三、全国社会保障基金理事会（SSF）

- 财务报告总栏目 `/portal/xxgk/fdzdgknr/cwbg/A00100308index_1.htm`，分三个子列表：

| 子栏目 | 索引 URL | 年份（实测列表） |
|---|---|---|
| 社保基金年度报告 | `…/cwbg/sbjjndbg/A0010030801index_1.htm` | 2011–2025 |
| 基本养老保险基金受托运营年度报告 | `…/cwbg/yljjndbg/A0010030802index_1.htm` | 2017–2025（缺 2020） |
| 财政拨入 | `…/cwbg/czbr/A0010030803index_1.htm` | 见站内 |

- 报告正文为 **HTML 全文**（如 2022 年度 43,542 B），无 PDF/xls 附件；条目 URL 形如 `…/webinfo/{y}/{m}/{16位数字}.htm`。
- 内容：社保基金会概况、基金规模、投资收益额与收益率、境内外投资配置等。

## 坑

1. **人社部主域有 JS cookie 挑战**（返回 ~986 B 空壳，需 `EO_Bot_Ssid`），换 UA 无效；用 IP 镜像 `114.255.111.180` 或区县人社局转载的 PDF，详见 [`../stats/ministry-stats.md`](../stats/ministry-stats.md)。
2. 人社部统计公报正文不内嵌，**必须先解析正文页找 PDF 链接**（HTML 里给的是相对/同目录 `W0…pdf`），再下载。
3. 医保局月度指标**口径随年份改名**（「统筹基金和生育保险主要指标」↔「运行情况」↔「基本医疗保险和生育保险主要指标」），按年检索别写死标题；公报是**纯文本 HTML**，年度间的表格结构不一致，解析要按年份分别处理。
4. 医保局 `/module/download/downfile.jsp` 的 `filename` 是**带随机前缀的 hash**（如 `ed003b38c92c4d0dae9213a5d748f486.pdf`），不能拼；须先从文章页取链接。
5. SSF 报告条目 URL 含 16 位数字 ID 且**历史条目跨了两套路径**（早期 `/portal/jjcw/sbjjndbg/…`，现行 `/portal/xxgk/fdzdgknr/cwbg/sbjjndbg/…`），按年拼接易失败，回列表页取链接。
6. 人社部/医保局数字**口径不同**（人社部=养老失业工伤保险，医保局=职工+居民基本医保），社保卡持卡人数以人社部公报为准，医保参保人数以医保局公报为准，勿混用。
7. 全国社保基金理事会 ≠ 全国社会保障基金（前者是机构名，后者是基金名）；「养老基金年度报告」指地方委托的基本养老保险基金受托运营，不要与社保基金年度报告混为一谈。
