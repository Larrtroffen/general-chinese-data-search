# references/legal —— 法律/法规/裁判文书 数据源索引

本目录收录**法律、行政法规、部门规章、党内法规、司法解释、裁判文书/案例**的检索入口与抓取方法。原则：能用**官方一手源**（全国人大、中国政府网）就不用商业库；免费离线语料/镜像用于批量与离线；商业库只作补充（多需 Token/登录）。

## 文件一览

| 文件 | 来源 | 用途 | 状态 |
|---|---|---|---|
| `flk.npc.gov.cn.md` | 国家法律法规数据库（全国人大） | **法律/行政法规/监察法规/地方性法规/司法解释**全文检索 + Word/PDF 原件下载（官方、免登录） | ✅ 接口可用 |
| `chinese-law-corpus.md` | lttxzmj/chinese-law-corpus（CC0） | **法条逐条离线语料**（446 部/2.6 万条）+ 278 指导案例 + 445 公报案例；jsDelivr 免鉴权 JSON；配套 MCP | ✅ CDN 可取 |
| `lawtext-laws.md` | lawtext/laws + law-flk-vol1/2 | **flk 全量离线镜像**：markdown 正文 2548 篇（含已废止）+ 官方 docx 原件 2517 份 | ✅ 取件可用 |
| `legal-cn-mcp-hub.md` | hygiene-12/legal-cn-mcp-hub | **人民法院案例库 rmfyalk 逆向 API**（案例检索/详情/统计/枚举）+ flk 连接器 | ⚠️ 需 token |
| `cn-law-hub.md` | ZongziForu/cn-law-hub | **10 个官方源**一站式 Skill（法规/规章/条约/政策/党内法规/税务/环保/法院） | ✅ 各源可达 |
| `yuandian-law-search.md` | cat-xierluo/legal-skills（元典） | **付费备选**：法规/案例语义+关键词、企业画像（35 端点）、幻觉检测 | ⚠️ 需付费 Key |
| `gov.cn.md`（在 `../gov/`） | 中国政府网 | 国务院/中办**政策文件**、国务院公报检索（JSON API）；国家规章库入口 | ✅ 检索可用 |
| `npc-gov-regulations.md` | 聚合索引 | **部门规章 / 党中央文件 / 党内法规**三分工表 + 共产党员网 JSONP 接口 | ✅ 可检索 |
| `wenshu.court.gov.cn.md` | 中国裁判文书网 | 裁判文书检索 | ❌ 匿名不可用 |
| `court-open.md` | **法院公开三站**：中国执行信息公开网 / 人民法院公告网 / 全国企业破产重整案件信息网 | **失信被执行人、被执行人、限高、终本、法院公告、破产重整案件**；含从页面 JS 反查的接口与字段 | ⚠️ 部分验证 |
| `pkulaw.com.md` | 北大法宝 | 法律/行政法规/地方性法规/规章/司法解释/裁判文书（商业库） | ⚠️ 需 Token |
| `standards-cn.md` | **标准体系五站**：std.samr / openstd / hbba / dbba / ttbz + 部委 | **国家标准/行业标准/地方标准/团体标准**的标准号↔名称、状态、全文在线；国标元数据与行/地标有 JSON 接口 | ⚠️ 部分受限 |

## 选路

- **要法条逐条原文 / 离线入库（RAG、citation）** → `chinese-law-corpus.md`（逐条 JSON，CC0，最省事）或 `lawtext-laws.md`（flk 全量 markdown / docx 原件，含已废止）。
- **要免费官方全文（法条/司法解释原件下载）** → `flk.npc.gov.cn.md`（免登录，可下 Word/PDF）。
- **要案例（指导性/参考性，含裁判要点与正文）** → `legal-cn-mcp-hub.md` 的 **rmfyalk 逆向 API（需 token）**；无 token 时退回官网人工浏览（见 `wenshu.court.gov.cn.md` 替代通道）。
- **要失信被执行人 / 限高 / 被执行人 / 终本 / 法院公告 / 破产重整案件** → `court-open.md`（三站合一；`rmfygg` 的公告列表资源接口已定位（需 `JSESSIONID`+`p_auth`，本机空集），`zxgk` 接口参数已反查但受瑞数 WAF + 验证码限制，`pccz` 表单可用但结果需 JS 渲染）。
- **要跨多官方源（规章/条约/政策/党内法规/税务/环保）** → `cn-law-hub.md`。
- **要国务院/中办文件、公报** → `../gov/gov.cn.md`；**部门规章/党内法规** → `npc-gov-regulations.md`。
- **免费源不够（语义检索/权威案例/企业画像/幻觉检测）** → `yuandian-law-search.md`（付费，需 Key）或 `pkulaw.com.md`（需 Token）。
- **要标准号↔名称、现行/废止状态、标准全文（国标/行标/地标/团标）** → `standards-cn.md`（国标元数据与行/地标有 JSON 接口；国标全文在线预览免登录、下载可能弹验证码；团标前台受 WAF）。
- **裁判文书网本身** → `wenshu.court.gov.cn.md`（匿名不可用，仅记替代通道）。

## 相关

- 政策文件/规章库入口：`../gov/gov.cn.md`；企业工商登记 `../gov/gsxt.md`；信用红黑名单 `../gov/credit-china.md`。
- 人物/官员检索方法：`../methods/officials-research.md`。
- 商业古籍/论文库：`../academic/`。
- 抓取与清洗工具：`../tools/`。
- 跨库候选清单与进度：`../../CANDIDATES.md`。
- 一个网站/仓库一个文件；跨库聚合/分工放 `npc-gov-regulations.md`。
- 所有状态码、字段名、示例命令均为当日实际请求验证；未验证项在各自文件内标注（如 rmfyalk 带 token 路径、元典带 Key 路径）。
- 离线语料/镜像（`chinese-law-corpus`、`lawtext-laws`）只记录取用 URL 与结构，**不把语料副本搬入本仓库**；无 license 的仓库只记链接与用法。
