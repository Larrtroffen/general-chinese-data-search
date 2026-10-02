# gov/ —— 中国政府站群与权威登记库索引

本层收录中国政府侧的数据源：中央政策文件与公报、部委/省市级政策发布站点、政府开放数据平台、
企业/社会组织/事业单位等主体的官方登记与信用库、招投标与政府采购公告、国家级人才计划名单与
职称评审/职业资格考试公示、北京 16 区门户站群与政府信息公开年报通道。用于**名录核对、主体尽调、
任免检索、人才履历核查、政策原文与官方口径引文**。

## 文件一览

| 文件 | 来源 | 用途 | 状态 |
|---|---|---|---|
| `gov.cn.md` | 中国政府网（www.gov.cn） | 政策文件库/国务院公报检索 JSON API、国家规章库入口 | ✅ 检索 API 可用 |
| `china-policy-sites.md` | changwu/china-policy-sites | 80 部委 + 省/地市/直辖市政策发布站点 URL 总表 | ⚠️ 部分省份未完成 |
| `gov_opendata.md` | LuMitchell/gov_opendata | 13 省级 + 27 地市开放数据平台入口清单 | ⚠️ 停更、多有下线 |
| `gov-policy-mcp.md` | 三个第三方政策检索封装 | gov.cn 接口参数与站点白名单参考 | ⚠️ 未运行其代码 |
| `credit-china.md` | 信用中国（creditchina.gov.cn） | 法人/自然人信用信息、红黑名单、双公示 | ⚠️ 瑞数+加速乐 WAF |
| `city-credit.md` | 全国城市信用状况监测平台 + 各地信用网 | 城市综合信用指数月排名、社会信用体系政策、示范区名单 | ⚠️ 官方平台 WAF |
| `business-environment.md` | 发改委 + 全国工商联 + 世界银行 | 营商环境评价/报告、民企500强榜单、万家民企评营商环境 | ⚠️ 榜单为图片 |
| `gsxt.md` | 国家企业信用信息公示系统 | 企业/个体/农合工商登记、年报、异常与失信名单 | ⚠️ 加速乐挑战，须浏览器 |
| `ccgp-ggzy.md` | 中国政府采购网 / 全国公共资源交易平台 | 招投标与政府采购公告检索 | ✅ ggzy JSON 接口可用 |
| `chinanpo.md` | 中国社会组织政务服务平台（民政部） | 社会组织登记、年检、违法失信名单 | ⚠️ 检索需浏览器会话 |
| `ip-cnipa.md` | 国家知识产权局系（cnipa.gov.cn） | 专利/商标检索与公告入口 | ⚠️ 官网可达；检索库需登录 |
| `sydj.md` | 机关赋码和事业单位登记管理平台 | 事业单位法人登记与年度报告公示 | ✅ 免登录可直连 |
| `edu-research-institutions.md` | 教育部/学信网/中科院/社科院/中国科协/卫健委 | 高校名单（Excel）、院校库、科研机构、医疗机构名录 | ⚠️ 部分库需浏览器 |
| `renshi-sources.md` | 中央 + 地方组织部/人大网等 | 按「单位+年份」定位任免与任前公示 | ⚠️ 地方栏目多为 JS |
| `talent-programs.md` | 国家自然科学基金 / 教育部 / 人社部 / 中国博士后网 | 杰青优青、长江学者、特贴、博士后人名名单 | ✅ NSFC 清单 + 基金门户 API |
| `professional-titles.md` | 粤/苏/浙人社厅 + 人社部考试中心/技能评价网 | 职称评审公示、职业资格与技能证书查询 | ✅ 浙江 zcps JSON 接口可用 |
| `beijing.gov.cn.md` | 首都之窗（北京市政府门户） | 市级政策解读、部门动态、统一搜索 JSON 接口 | ✅ 搜索接口可用 |
| `beijing-districts.md` | 北京 16 区门户及人大/区委/融媒子站 | 区级名录核查、任免检索、新闻直取 | ✅ 门户可达（朝阳/延庆仅 http） |
| `beijing-xxgk.md` | 北京各区门户 gknb 年报栏目 | 区×年×街乡镇年报树、正职姓名线索 | ⚠️ 路径漂移严重 |
| `beijing-bureaus.md` | 首都之窗信息公开索引 + 各委办局/群团/党派官网 | 市级机构官网与信息公开栏目总表（委办局·群团·民主党派·工商联） | ✅ 委办局全可达 |
| `beijing-street-town.md` | 北京 16 区门户街乡镇栏目目录 | 按「区×街道/乡镇」定位该单位官网栏目（三种形态） | ✅ 各街镇栏目 200 |
| `bjchy.gov.cn.md` | 朝阳区政府网 | 区级新闻直取（GBK，仅 http） | ✅ 正文可直取 |
| `bjdx.gov.cn.md` | 大兴区政府网 | 区级新闻直取、id 可枚举 | ✅ 正文可直取 |
| `defense-documents.md` | 国防部 / 国新办 / 财政部 | 国防白皮书、涉军发布、国防支出预算决算 | ⚠️ 国新办需浏览器 |
| `veterans-affairs.md` | 退役军人事务部 / 中国双拥网 | 双拥模范名单、模范退役军人、烈士纪念设施 | ✅ 部分可抓 |
| `disclosure-channels.md` | 首都之窗/各委办局/市区审计·应急·规自·住建 | **易漏文件的 10 类政务栏目**：依申请公开、公报、规范性文件、意见征集、听证、审计、事故调查、巡视、规划公示、征收 | ✅ 多数 200 |

## 选路

- 要**政策文件原文/公报** → `gov.cn.md` 的 `search-gov/data` JSON API；机关入口白名单看 `china-policy-sites.md`；现成 MCP 封装见 `gov-policy-mcp.md`。
- 要**数据集本体**（开放数据门户） → `gov_opendata.md`；要政策文本 → `gov.cn.md` / `china-policy-sites.md`。
- 要**企业工商登记** → `gsxt.md`（须浏览器）；要**信用红黑名单/双公示** → `credit-china.md`；要**诉讼执行** → `../legal/court-open.md`。
- 要**营商环境评价/年度报告、民营企业500强榜单、万家民企评营商环境** → `business-environment.md`（发改委文件库有 JSON 接口；500强榜单本体为图片需 OCR）。
- 要**城市信用监测月排名 / 社会信用体系政策 / 示范区名单** → `city-credit.md`（官方平台 WAF，走地方信用站镜像）。
- 要**社会组织/基金会/协会真伪** → `chinanpo.md`；要**事业单位是否存在** → `sydj.md`。
- 要**招投标/政府采购公告** → `ccgp-ggzy.md`（批量走 ggzy JSON 接口）。
- 要**专利/商标** → `ip-cnipa.md`。
- 要**人才计划名单**（杰青/优青、长江学者、万人计划、政府特殊津贴、博士后基金） → `talent-programs.md`；NSFC 走各科学部资助清单，博士后务必走 `/website/` 深链。
- 要**职称评审公示 / 职业资格与技能证书** → `professional-titles.md`（浙江走 `zcps` JSON 接口，江苏走 jpage XML，广东走 `zwgk/gsgg/`）。
- 要**任免/任前公示** → `renshi-sources.md`（跨省首选人民网聚合栏）；北京市级 → `../party/bjdj.gov.cn.md`。
- 要**北京区级新闻/名单线索** → `beijing-districts.md`、`bjchy.gov.cn.md`、`bjdx.gov.cn.md`；街乡镇单位栏目 → `beijing-street-town.md`；年报树 → `beijing-xxgk.md`；市级口径 → `beijing.gov.cn.md`。
- 要**北京市级某委办局/群团/民主党派/工商联的官网与信息公开栏目** → `beijing-bureaus.md`（50+ 机构域名总表）；区级机构 → `beijing-districts.md`、`beijing-street-town.md`。

**通用结论**

- **区级门户站内检索基本不可直连**：多为 JS 异步 + `api.so-gov.cn` 后端，且 siteCode 扫描会封出口 IP；改用**搜狗微信 / `web_search site:`**（见 `../engines/`）。
- **HTTPS 不通用**：朝阳、延庆只服务 http；丰台人大等自签证书 → 统一 `curl -sSk`。
- **编码混杂**：门户多为 UTF-8，朝阳系（chynews/chyrd/bjchy）为 GB2312/GBK → `iconv -f gb18030`。
- **路径会漂移**：年报树根等深链长期有效假设不成立，运行前先探测。
- 政协/人大子站命名规律：`<区简称>rd.<区域>`（如 `renda.bjft.gov.cn`）、`<区简称>qw.<区域>`（如 `hdqw.bjhd.gov.cn`），可据此猜域名后再探测。
- **北京街镇无独立官网**：街镇级 `<街道>.bjXX.gov.cn` 子域名已全部下线；单位栏目一律在区网「机构职能/政务公开」目录下的拼音缩写/数字 id 栏目里，映射与坑见 `beijing-street-town.md`。
- **部委官方库常带门**：人社部主域为 JS cookie 挑战 → 走 IP 镜像 `114.255.111.180`；NSFC 基金门户 `/api/*` 响应为 `DES-ECB`（key 见 `talent-programs.md`）需先解密；地方平台（如浙江 zcps）接口要会话 cookie，无 cookie 返回 HTTP 200 的 `非法请求 404！`。

## 相关

- 党内法规/部门规章：`../legal/npc-gov-regulations.md`；裁判文书/失信/破产：`../legal/court-open.md`。
- 信用与营商环境：`credit-china.md`（单主体信用）、`city-credit.md`（城市信用排名）、`business-environment.md`（营商环境评价与民企榜单）。
- 北京组工/党建：`../party/bjdj.gov.cn.md`。
- 统计与区划代码：`../stats/`（民政部区划代码、统计用区划代码）。
- 检索通道（搜狗微信 / 360 / 搜狗）：`../engines/`。
- 人物名录分工：院士/国家荣誉/英烈 → `../archives/person-databases.md`；计划性人才名单 → `talent-programs.md`；干部任免 → `renshi-sources.md`。
