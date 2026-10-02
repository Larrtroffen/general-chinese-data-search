# officials-research —— 官员/干部检索方法卡

- 去哪找：单位门户「领导之窗 / 机构领导」页；人大任免公报（[`gov/renshi-sources.md`](../gov/renshi-sources.md) §5 中国人大网、各区人大）；组织部「任前公示」（[`gov/renshi-sources.md`](../gov/renshi-sources.md) §3 人民网「任前公示」栏、地方；[`party/bjdj.gov.cn.md`](../party/bjdj.gov.cn.md)）；年鉴 / 政府工作报告 / 信息公开年报（[`gov/beijing-xxgk.md`](../gov/beijing-xxgk.md)、[`stats/tjj.beijing.gov.cn.md`](../stats/tjj.beijing.gov.cn.md)、[`archives/`](../archives/README.md)）；地方媒体（[`media/`](../media/README.md)、2018 老稿走 [`wechat/weixin.sogou.com.md`](../wechat/weixin.sogou.com.md)）；人物库（[`archives/cbdb.md`](../archives/cbdb.md)、中研院各库）。
- 什么时候用：给定「某单位 / 某街乡镇 / 某年」要还原**正职（及副职）姓名、职务、任期**；或找**简历 / 任免**证据。
- 怎么搜：按可靠性降序走，命中即停 —— ① 定单位规范名与层级 → ② 单位「领导之窗」页 → ③ 人大任免公报 → ④ 组织部任前公示 → ⑤ 年鉴 / 政府工作报告 / 信息公开年报 → ⑥ 地方媒体报道 → ⑦ 人物库对档。**交叉验证**：任前公示（拟任）→ 人大任命（正式）→ 领导之窗（在任）三者互证，日期不一致时以**人大公报日期**为任期起点。逐站 URL 规律与词表见「细节」。
- 覆盖：单位层级（区门户 → 街道/部门）；时间（在任 / 历史任期 / 某年断面）；人物（古代、近代、民国、日治台湾）。
- 门槛：多为公开网页 + 搜索引擎；部分站前端 JS / 瑞数 / Cloudflare 反爬需浏览器；人物库 CBDB 需下载 SQLite。
- 实测：2026-10-03，macOS 27（arm64），curl 8.x（`-sSk -L -m 20`，桌面 Chrome UA，单主机 ≤3 请求、间隔 ≥1.5 s）。
- 上游：各级政府 / 人大 / 组织部站点、CBDB、中研院各库（入口见「细节」）。

> 产出纪律：每条结论尽量落到「官方口径 + 日期 + URL」。

## 细节

### 一、通用流程（按可靠性降序走，命中即停）

1. **先定单位规范名与层级**
   - 街乡镇名录/代码：[`stats/mca.gov.cn.md`](../stats/mca.gov.cn.md)、[`stats/xzqh.org.md`](../stats/xzqh.org.md)、[`stats/data_location.md`](../stats/data_location.md)。
   - 注意**后缀变体**（见 §三）——名录里可能是「XX地区」，政府站里写作「XX街道办事处/地区办事处」。
2. **单位「领导之窗 / 机构领导」页**（最直接）：见 §四 URL 规律。区门户 → 机构职能/街道 → XX街道办事处 → **领导介绍/领导班子**。
   - 典型字段：姓名 + 职务（工委书记 / 办事处主任 …）+ 出生年月/学历/分工 + 简历。**只反映当前在任**，历史任期要靠下面第 3–6 步。
3. **人大任免公报**（有日期、有任免动作，权威）
   - 国家层面：[`gov/renshi-sources.md`](../gov/renshi-sources.md) §5 中国人大网任免专栏（2007→今，静态可爬）。
   - 区级人大：[`gov/beijing-districts.md`](../gov/beijing-districts.md)（`chyrd` 朝阳人大、`renda.bjft` 丰台人大、`renda.bjtzh` 通州人大、`www.dcrd.gov.cn` 东城人大…）。
   - 检索式：`{区}人大常委会 任命名单` / `{单位} 主任 任命` / `第X届人大常委会第X次会议`。
4. **组织部「任前公示」**（含拟任职务、出生年月、现职，**信息最全**）
   - 聚合入口（免登录、跨省）：[`gov/renshi-sources.md`](../gov/renshi-sources.md) §3 人民网「任前公示」栏。
   - 地方：江苏/安徽/山东见 `gov/renshi-sources.md` §7–§10；北京市级见 [`party/bjdj.gov.cn.md`](../party/bjdj.gov.cn.md)。
   - 检索式：`{单位|区} 干部任前公示` / `拟任 {职务}` / `省管干部 公示`。
5. **年鉴 / 政府工作报告 / 信息公开年报**（给「某年」断面名单）
   - 年报树：[`gov/beijing-xxgk.md`](../gov/beijing-xxgk.md)；统计年鉴：[`stats/tjj.beijing.gov.cn.md`](../stats/tjj.beijing.gov.cn.md)；方志/年鉴：[`archives/`](../archives/README.md)（`difangzhi.cn`、`bjsfzg.bjdsdfz.cn`）。
   - 政府工作报告常在门户「政务公开」栏；检索式：`{区} 政府工作报告 {年} 街道` / `{单位} 年鉴`。
6. **地方媒体报道**（补正式名单外的动态、任免新闻）
   - [`media/bjnews.com.cn.md`](../media/bjnews.com.cn.md)、[`media/beijing.qianlong.com.md`](../media/beijing.qianlong.com.md)、[`media/people.com.cn.md`](../media/people.com.cn.md)、[`media/xinhuanet.com.md`](../media/xinhuanet.com.md)。
   - **2018 老稿主通道仍是搜狗微信**（[`wechat/weixin.sogou.com.md`](../wechat/weixin.sogou.com.md)）：公众号「北京组工」「XX 街道」等 + 年份词放量。
7. **人物库对档**（把姓名对到权威 ID / 补履历）
   - 历史人物（唐–清）：[`archives/cbdb.md`](../archives/cbdb.md) CBDB（`c_personid`、官職履历、任官地点）。
   - 台湾/民国人物（见 §五）。

> **交叉验证纪律**：任前公示（拟任）→ 人大任命（正式）→ 领导之窗（在任）三者相互印证；三者日期不一致时以**人大公报日期**为任期起点。

### 二、关键词与变体词表

| 维度 | 词表 |
|---|---|
| 正职 | 书记、党工委/党委书记、主任、工委主任、办事处主任、镇长、乡长、局长、部长、院长、理事长、管委会主任、总队长 |
| 副职 | 副书记、副主任、副镇长、副乡长、副局长、委员、党组成员 |
| 代/兼/主持 | 代区长、代市长、代理主任、代镇长、兼任、主持工作、主持全面工作、负责人、临时负责、牵头 |
| 挂职/交流 | 挂职、挂任、下派、选派、交流任职、援派、驻村第一书记 |
| 任免动作 | 任免、任命、免去、辞去、辞职、决定任命、拟任、拟提名、拟推荐、职务调整、职务任免、不再担任 |
| 公示 | 任前公示、任职前公示、干部任前公示、省管干部、市管干部、区管干部、公示公告、公示通告 |
| 人大 | 人大常委会、任命名单、免职名单、决定任免的名单、第X届人大常委会第X次会议、公告 |
| 简历 | 简历、个人基本信息、分工、分管、领导介绍、领导班子、领导之窗 |

**组合技巧**：`{单位全名} + {职务词}`；`{区} + 人大常委会 + {年}`；`{单位} + 任前公示`；把「正职词」与「任免动作」组合（如 `主任 免去`、`镇长 拟任`）能同时锁定更替的两端。

### 三、单位名后缀变体（同一实体多种写法，必须逐一试）

- 街道办事处 ↔ **地区办事处** ↔ 管理委员会/管委会 ↔ 地区工委 ↔ 街道工委 ↔ 人民政府（镇/乡）↔ 「XX 地区」。
- 例：名录「三间房地区」→ 站内「三间房地区办事处 / 三间房街道办事处 / 三间房乡」。
- 简称/别字：街道名去「街道」二字、区名「北京市 XX 区」↔「XX 区」。
- 行政区划 ≠ 功能区：开发区/管委会（如中关村、CBD）与属地街道是两套班子，别混。

### 四、「领导之窗」类页面 URL 规律（本机实测）

| 层级 | 常见路径 | 实测例（✅ 2026-10-03） |
|---|---|---|
| 区门户 | `/{xxgk\|zwgk}/ldzc.{html\|/}`（领导之窗） | `https://www.bjxch.gov.cn/xxgk/ldzc.html` ✅ 79 KB |
| 区门户 | `/{xxgk\|zwgk}/ldfg/{...}`（领导分工） | 搜索所得：`pudong.gov.cn/zwgk/ldfg-{街道拼音}ldfg/index.html` |
| 街道（挂区门户） | `/{xxgk\|zwgk}/jgzn/{街道缩写}/{街道拼音}dbsc/ldjs.html` | `https://www.bjxch.gov.cn/xxgk/jgzn/qjd/asljdbsc/ldjs.html` ✅ 47 KB（含「工委书记/办事处主任/职 务/个人基本信息」） |
| 街道（机构专页） | `/jgzy/zzfjdbsc/{街道拼音}jdbsc/ldbz` | `http://www.panyu.gov.cn/jgzy/zzfjdbsc/fzqrmzfsqjdbsc/ldbz` ✅ 43 KB |
| 街道（机构） | `/gzjg/jz/{街道缩写}dbsc/ldbz` | 搜索所得：`hp.gov.cn/gzjg/jz/dsjdbsc/ldbz` |
| 部门站 | `/{部门}/ldbz/`、`/ldjs/`、`/jggk/`（机构概况） | 命名规律：`ldzc`=领导之窗、`ldjs`=领导介绍、`ldbz`=领导班子、`ldfg`=领导分工 |

**技法**：先定门户，再按上表猜路径后**逐一 curl 探测**（`curl -sSk -L -m 20 -A '<桌面UA>'`）；页面里有「工委书记/主任」文本即命中；旧版页面可能只在 `{门户}/zfxxgk/` 下。

**快照回捞（找历史在任名单）**：领导之窗只显当前班子 → 用 Wayback 取历年快照对比。
- 工具卡：[`tools/web.archive.org.md`](../tools/web.archive.org.md)（**间歇可达**；本机 2026-10-03 实测 CDX `http`/`https` 均 **超时 000**，不可用 → 换 Bing/搜狗缓存、或媒体存档）。
- 若可达时的模板：`http://web.archive.org/cdx/search/cdx?url=<host>/<path>&output=json&filter=statuscode:200`，再按时间戳取 `https://web.archive.org/web/<ts>/<url>`。

### 五、人物库

| 库 | 入口 | 覆盖 | 实测/门槛 |
|---|---|---|---|
| **CBDB 中国历代人物传记资料库** | 见 [`archives/cbdb.md`](../archives/cbdb.md)（SQLite，HF 下载，`hf-mirror.com` 可达） | 唐–清为主，数十万人；官職履历 + 关系 | ✅ 已有专卡；引用即可 |
| **臺灣「人名權威檔」（中研院史語所·人物傳記資料庫）** | `https://newarchive.ihp.sinica.edu.tw/sncaccgi/sncacFtp` | 歷史人物傳記權威檔（姓名/生卒/異名/籍貫/傳略/出身/關連） | ✅ 2026-10-03 → 200（标题《人名權威-人物傳記資料庫》）；免费 |
| **臺灣總督府職員錄系統**（中研院臺史所） | `https://who.ith.sinica.edu.tw/`（進階查詢 `/search2adv.html`） | 日治時期臺灣總督府職員：姓名/單位/官職/職等/本籍（同名錄可查**在任年**） | ✅ 2026-10-03 → 200（首页 63 KB；進階查詢页 200） |
| 近現代人物資訊整合系統（中研院近史所） | `https://mhdb.mh.sinica.edu.tw/` | 近現代（民國）人物 | ❌ 本机 2026-10-03 **超时 000**，本机不可达 |
| 國家檔案資訊網·政治檔案人名索引 | `https://aa.archives.gov.tw/ELK/Politic?cnid=109771` | 政治檔案當事人姓名索引（80 万+ 笔） | 搜索所得，未 curl |

> 用途：人名消歧（同一人多名/异体字）与控制身份；古/近代人物用 CBDB，日治台湾用总督府职员录，民国人物优先近现代整合系统（待网络可达）。

### 实测

2026-10-03，macOS 27（arm64），curl 8.x（`-sSk -L -m 20`，桌面 Chrome UA，单主机 ≤3 请求、间隔 ≥1.5 s）。本文 `✅/❌/⚠️` 均取自当日本机请求；标「搜索所得」者为搜索引擎结果、未 curl 复测（仅作入口线索，用前先探测）。

## 坑

- 领导之窗 / 年鉴**只给断面**，不写任期起止 → 任期必须靠**人大任免公报日期**（`gov/renshi-sources.md` §5）锚定。
- 省委组织部/地方政府站大量**前端 JS 或瑞数/Cloudflare**：curl 拿不到就上浏览器（`tools/agent-browser.md`、`tools/playwright-cli.md`、`tools/scrapling.md`）；不可达照实记录，勿猜。
- 「搜不到」≠「没有」：人民网站内检索索引只约 2021 至今（见 `media/people.com.cn.md`），2018 老稿走搜狗微信 + 数字报。
- 编码/HTTPS 混杂（GBK、只 http、自签证书）见 `gov/beijing-districts.md` 坑表；一律 `-sSk -L` + `iconv -f gb18030` 兜底。
- 站群“站内检索”多需签名/会把出口 IP 拉黑（`api.so-gov.cn`）→ 改 `web_search site:` + 搜狗微信。
