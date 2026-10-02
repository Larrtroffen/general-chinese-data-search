# business/ —— 企业与市场数据源

本层收录「企业主体—证券—市场」三类研究与尽调常用的数据源：上市/挂牌公司公告年报、交易所市场统计、
监管处罚、债券与货币市场行情、海关进出口统计、企业认定名单、招投标与政府采购公告，以及高校科研常用的商业数据库入口。

## 文件一览

| 文件 | 来源 | 用途/何时用 | 状态 |
|---|---|---|---|
| `cninfo.com.cn.md` | 巨潮资讯网（深交所指定披露平台） | **沪深北+港股公告/年报全文检索**：代码表、公告检索、全文检索、PDF 直链规律 | ✅ 免登录 JSON |
| `szse.cn.md` | 深圳证券交易所 | 深市公告列表 + 市场统计报表（含 Excel 导出标识） | ✅ JSON 接口 |
| `sse.com.cn.md` | 上海证券交易所 | 沪市公告/定期报告栏目、市场统计栏目；JSONP 取数域 | ⚠️ 公告接口参数未跑通 |
| `bse.cn.md` | 北京证券交易所 | 北交所信息披露与市场数据 | ⚠️ 需浏览器（JS 挑战） |
| `neeq.com.cn.md` | 全国中小企业股份转让系统 | 新三板挂牌公司名录/公告/行情 | ⚠️ 需浏览器（JS 挑战） |
| `csrc.gov.cn.md` | 中国证监会 | 证券/期货市场统计（周/月报）、上市公司行业分类、行政处罚 | ⚠️ 处罚列表 JS 渲染 |
| `chinabond.com.cn.md` | 中国债券信息网 / 中债估值 | 债券市场统计、中债收益率曲线与估值 | ⚠️ 取数接口未跑通 |
| `customs.gov.cn.md` | 海关总署 | 进出口月度统计：总值/国别/商品类章/贸易方式 | ⚠️ WAF，需浏览器 |
| `chinamoney.com.cn.md` | 中国货币网（外汇交易中心） | 人民币汇率中间价、Shibor/LPR、货币市场行情 | ✅ 匿名 JSON 接口 |
| `commercial-databases.md` | CSMAR / CNRDS / CEIC / Wind | 商科面板数据总卡：定位、覆盖、订阅与申请门槛 | ⚠️ 需订阅 |
| `enterprise-certifications.md` | 高企认定工作网 / 工信部培育平台 | 高新技术企业、专精特新"小巨人"公示名单入口 | ⚠️ 名单分散/本机不可达 |
| `procurement.md` | 中国招标投标公共服务平台 / 省级交易平台 / 千里马·采招·比地 | **招标与政采公告的历史回溯与批量取数**：省级三种血统、商业网回溯年限、分页/时间窗语料化 | ⚠️ 多数需浏览器 |
| `tender-corpus.md` | CnOpenData / Hugging Face / 知了标讯 | 现成招标公告数据集：学术付费库、开源 NLP 微调集、接口化数据源 | ⚠️ 付费/需镜像 |
| `bid-docs.md` | 全军武器装备采购信息网 / 国铁采购平台 / 中招联合 / 中国采购与招标网 / 剑鱼标讯 | **带附件的公告源**（招标文件/需求书 PDF·zip）：军队、铁路、代理机构、聚合站的列表与附件规律 | ⚠️ weain 详情需登录 |

## 选路

- **要上市公司公告/年报原文** → 首选 `cninfo.com.cn.md`：`hisAnnouncement/query`（按公司+日期）或 `fulltextSearch/full`（跨公司关键词），PDF 走 `static.cninfo.com.cn/finalpage/…`。它是本层**唯一全套免登录 JSON** 的公告源。
- **要交易所官方口径与市场统计** → 深市走 `szse.cn.md`（公告 + `ShowReport` 报表）；沪市走 `sse.com.cn.md`（栏目页可读，批量公告回退 cninfo）；北交所/新三板分别见 `bse.cn.md`、`neeq.com.cn.md`（官网需浏览器，样本批量取用 cninfo 绕行）。
- **要证券/期货市场统计与处罚** → `csrc.gov.cn.md`：统计栏目服务端渲染可直接抓；行政处罚列表 JS 渲染、检索端点匿名返回 0，需浏览器。
- **要债券/利率/汇率** → 收益率曲线看 `chinabond.com.cn.md`（页面可读、取数接口未跑通）；汇率与货币市场行情走 `chinamoney.com.cn.md`（`RefRateHis` 匿名 JSON）。
- **要进出口贸易统计** → `customs.gov.cn.md`：月报/快讯栏目 + 在线查询平台，官网有 WAF，需浏览器过挑战。
- **要清洗好的结构化面板**（财务附注、治理、ESG、宏观长序列） → `commercial-databases.md`：先确认本校/机构是否已购（图书馆导航），再决定用 CSMAR/CNRDS/CEIC/Wind；**先用免费源（`../stats/`、cninfo 公告）再上商业库**。
- **要企业政策认定名单** → `enterprise-certifications.md`：高企分省分批公示、专精特新部省两级公示，名单多在附件，注意留档。
- **要招标/政采公告的历史回溯与批量语料** → `procurement.md`：优先有 JSON 的入口（北京 `POST /elasticsearch/search`、千里马 `search.qianlima.com/api/v1/website/search`）循环分页，再按「关键词 × 年」细分绕上限；国家级口径与其接口字段见 `../gov/ccgp-ggzy.md`（本层不重复）。商业网（千里马/采招/比地）历史库与 API 需付费。
- **要现成招标数据集而非自采** → `tender-corpus.md`：学术面板走 CnOpenData（2013 年起、含原始文档），NLP 语料走 Hugging Face（国内须用 `hf-mirror.com` 镜像）。
- **要军队/铁路/代理机构的公告原文与附件** → `bid-docs.md`：weain（`/api/front/list/cggg/list` 匿名 JSON）与国铁（`POST /proxy/portal/elasticSearch/queryDataToEs`）给标题/日期，**招标文件附件在详情页**（weain 详情需登录；国铁附件走 `forwardFile/downloadFileForCommon`）。

**通用结论**

- 公告取数的**主通道是 cninfo**（免登录、可翻页、直出 PDF），交易所官网更多是官方栏目结构与统计口径；两者互为旁证。
- 本层多个官网有反爬：北交所/新三板为**创宇盾 `C3VK` JS 挑战**（302 重定向环），海关为**加速乐 `__jsluid`（412）**，工信部为 `__jsluid_s`——均**须真实浏览器**，别用 curl 硬刷（会封 IP）。
- 注意实体类型区分：`../gov/gsxt.md`（工商登记）≠ 交易所披露（`cninfo`）≠ 监管处罚（`csrc`）；研究样本构建常需三者交叉。
- 抓取建议：桌面 UA、同主机 ≥1.5s 间隔；公告 PDF 走 `static.cninfo.com.cn`。

## 相关

- 宏观统计数值与年鉴：`../stats/`（国家统计局、`data.stats.gov.cn.md`、`akshare.md`）。
- 企业工商登记、信用红黑名单：`../gov/gsxt.md`、`../gov/credit-china.md`。
- 裁判文书、失信、破产：`../legal/court-open.md`。
- 免费数据集市（天池/和鲸/ScienceDB/ModelScope/HF-Mirror）：`../methods/dataset-hubs.md`。
- 交易所公告与政府信息公开总入口：`../gov/`。
- 招投标/政府采购公告的检索接口与字段（ccgp 检索参数、ggzy `getTradList`）：`../gov/ccgp-ggzy.md`（`procurement.md` 只讲历史回溯与批量，不重复）。
- 军队/铁路/代理机构公告与附件规律：`bid-docs.md`；北京公共资源交易与各区门户：`procurement.md`、`../gov/beijing-xxgk.md`。
