# surveys/ —— 中国大型调查与微观数据

本层收录中国主要**学术抽样调查/追踪调查**（CFPS、CGSS、CHARLS、CLHLS、CLDS、CHFS、CEPS、CIEFR-HS、CHIP/CHNS/CSS）与**微观数据平台/申请入口**（CNSDA、CFDB、国家统计局微观数据、IPUMS），并补入**教育/心理学专项**（清华 CCSS、PISA/TIMSS/PIRLS、教育部教育统计、心理科学数据中心），另收**人口与流动人口专项**（人发中心调查数据、CMDS、老龄抽样调查）与**人社/医保统计**（人社部公报、国家医保局、全国社保基金理事会），并补入**招聘平台就业大数据**（智联招聘、BOSS 直聘、猎聘、前程无忧的行业报告），面向社科与教育心理实证研究的数据获取。

## 文件一览

| 文件 | 来源 | 用途 | 状态 |
|---|---|---|---|
| `cfps.md` | 北京大学 ISSS | 家庭户 + 个人两级双年追踪面板（2010 起） | ✅ 需申请审核 |
| `cgss.md` | 中国人民大学 NSRC | 全国年度综合性社会调查横截面（2003 起） | ✅ 经 CNSDA |
| `charls.md` | 北大国家发展研究院 / 武大 | 45 岁及以上中老年人健康与养老追踪（2011 起） | ✅ 需注册 |
| `clhls.md` | 北大健康老龄与发展研究中心 | 65+ 老人健康长寿追踪（1998 起，含认知） | ✅ 需申请审核 |
| `clds.md` | 中山大学社科调查中心 | 劳动力/家庭/社区双年追踪 | ⚠️ 官网不通 |
| `chfs.md` | 西南财经大学 | 家庭金融与资产微观调查（2011 起） | ✅ 需统一认证 |
| `ceps.md` | 中国人民大学 NSRC | 初中队列教育追踪调查（2013–14 基线） | ✅ 经 CNSDA |
| `ciefr-hs.md` | 北京大学 CIEFR | 家庭教育支出全国追踪（2017 起） | ✅ 需机构邮箱 |
| `tsinghua-ccss.md` | 清华大学教育研究院 | 大学生学情与发展院校调查 | ⚠️ 非公开·院校委托 |
| `pisa-timss-pirls.md` | OECD / IEA | PISA·TIMSS·PIRLS 中国参与地区测评数据 | ✅ 免费直下 |
| `edu-stat-public.md` | 教育部 | 教育事业发展统计公报与教育统计数据 | ✅ 免费 |
| `chip-chns-css.md` | 中外合作 / UNC / 社科院 | 收入分配·健康营养·社会状况三类经典调查 | ✅ 可申请 |
| `psych-data.md` | 中科院心理所 / ScienceDB | 心理学数据、预注册与存缴入口 | ✅ 检索免登录 |
| `cnsda.org.md` | 中国社会调查数据资料库 | 社科调查项目元数据的一站式检索入口 | ⚠️ 证书过期 |
| `cfdb.md` | 浙江大学社科研究基础平台 | 中国家庭大数据库（CFD/CRHPS，2011–2017） | ✅ 邮件申请 |
| `microdata.stats.gov.cn.md` | 国家统计局 | 官方微观数据注册申请与现场使用 | ✅ 需现场用 |
| `ipums.org.md` | 明尼苏达人口中心 | 中国人口普查微数据（1982/1990/2000） | ✅ 需注册 |
| `population-surveys.md` | 人发中心 / 卫健委 / 老龄科研中心 | 人口与流动人口专项调查（CMDS、生育/家庭、老龄） | ✅ 部分需申请 |
| `social-insurance.md` | 人社部 / 国家医保局 / 社保基金理事会 | 社保医保统计公报与基金年报 | ✅ 免费免登录 |
| `employment-data.md` | 智联招聘 / BOSS 直聘 / 猎聘 / 前程无忧 | 招聘平台就业与薪酬报告（PDF / JSON 入口） | ⚠️ 部分需浏览器 |

## 选路

- **先查某个调查有没有数据、有哪些年份** → 直接去 `cnsda.org.md` 用 `Projects[title]=` 检索（免登录、可解析 HTML），再进对应项目页。
- **做家庭/个人长期追踪（收入、教育、健康、代际）** → `cfps.md`（家庭+个人双年面板，北大平台申请）或 `charls.md`（45+ 中老年健康养老）。
- **做社会态度/阶层/劳动就业的年度横截面** → `cgss.md`（经 CNSDA / 人大 CSSD 下载）。
- **做家庭资产、负债、金融行为** → `chfs.md`（西财申请入口）；要 2011–2017 农村家庭追踪与城镇对比 → `cfdb.md`。
- **做教育产出与不平等** → `ceps.md`（初中同期群追踪）。
- **要官方普查/住户调查的个体级数据** → `microdata.stats.gov.cn.md`（国家统计局，**须现场使用**）；要可下载的中国普查微数据 → `ipums.org.md`（1982/1990/2000，跨国可比）。
- **老牌专题调查（收入分配 CHIP、健康营养 CHNS、社会状况 CSS）** → `chip-chns-css.md`，注意其最新波次距今较远。
- **找不到 CLDS/CHIP 等官网** → 优先用 `cnsda.org.md` 的项目页（`clds.md` 的 `css.sysu.edu.cn` 本机不通）。
- **家庭教育支出 / 课外补习 / 入园 / 教育负担** → `ciefr-hs.md`（北大 CIEFR，须机构邮箱在 PKU 平台申请）。
- **大学生学情（学习投入 / NSSE / 院校质量）** → `tsinghua-ccss.md`（院校委托参与，数据非公开；个人需课题合作）。
- **国际测评（PISA / TIMSS / PIRLS）中国参与地区** → `pisa-timss-pirls.md`（免注册直下；注意 PISA「中国」是省市联合体，TIMSS/PIRLS 无内地）。
- **教育年度数字（在校生 / 毛入学率 / 生师比 / 分省）** → `edu-stat-public.md`（教育部公报 + 统计数据模块，免费）。
- **高龄老人（65+ / 百岁）健康、认知与长寿** → `clhls.md`（1998 起，PKU 平台申请）；45+ 全国队列见 `charls.md`。
- **心理学数据 / 预注册 / 论文数据存缴** → `psych-data.md`（心理科学数据中心匿名 JSON 接口、ScienceDB、OSF/PsyArXiv、ICPSR）。
- **流动人口/农民工个体级数据（CMDS）** → `population-surveys.md`（国家人口健康科学数据中心 JSON 检索后申请下载；原免费通道 2023-09 已关）。
- **生育/家庭/托育专项与人口预测汇总** → `population-surveys.md`（人发中心「调查数据」目录 + PADIS-INT 人口预测）。
- **老年人口生活状况（60+，五年一次）** → `population-surveys.md`（老龄科研中心，填表邮件申请）。
- **参保人数 / 基金收支 / 社保卡持卡数（人社口径）** → `social-insurance.md`（人社部统计公报，走 IP 镜像绕 JS 挑战）。
- **医保参保 / 待遇 / 基金（医保局口径）** → `social-insurance.md`（col7 公报 + 逐月指标 + 数智库 PDF）。
- **社保基金与养老金投资业绩** → `social-insurance.md`（社保基金理事会年度报告，HTML 全文）。
- **招聘平台口径的就业景气 / 招聘薪酬 / 应届生就业力 / 跳槽指数** → `employment-data.md`：前程无忧报告 PDF 按年直链可下（2021–2025）；智联报告中心被 WAF、BOSS 直聘接口 IP 风控，余转第三方转载。
- **商业平台报告站内找不到** → 检索「平台名 + 报告名 + 年份」转第三方聚合站（三个皮匠 / 发现报告 / 报告汇），注意为转载、须核原始 PDF 出处。

## 相关

- 宏观统计与年鉴数据源（NBS 接口、统计公报、统计年鉴）：[`../stats/README.md`](../stats/README.md)。
- 数据集市（天池/和鲸/ScienceDB/ModelScope/HF-Mirror，带 JSON 检索接口）：[`../methods/dataset-hubs.md`](../methods/dataset-hubs.md) —— 与官方调查口径互补，但许可与质量需逐条核。
- 教育统计口径与部委统计总表：[`../stats/ministry-stats.md`](../stats/ministry-stats.md)；高校 / 科研机构名录与资质核实：[`../gov/edu-research-institutions.md`](../gov/edu-research-institutions.md)。
- 人口普查汇总与个体级数据：[`../health/stats.gov.cn-census.md`](../health/stats.gov.cn-census.md) 与 `microdata.stats.gov.cn.md`、`ipums.org.md`；社保/医保部委口径见本层 `social-insurance.md`。
- 心理学预注册与社科数据档案：[`../repos/osf.io.md`](../repos/osf.io.md)、[`../repos/icpsr.umich.edu.md`](../repos/icpsr.umich.edu.md)。
- 官方就业 / 失业统计口径（城镇调查失业率、就业人员）见 [`../stats/README.md`](../stats/README.md)，人社 / 医保数字见本层 `social-insurance.md`；招聘平台自报数据见本层 `employment-data.md`，口径不同勿混用。
- 上游总表与用法：仓库根 `SKILL.md`。

## 通用注意

- 本层各源多为**申请制**：免费但需注册、实名、签数据使用协议，甚至审核/现场使用；引用时须按各自规定标注数据来源。
- 中文官方/调查站抓取建议 ≥1.5s 间隔、桌面 UA；`cnsda.org` 证书过期需 `-k`，其元数据检索免登录但**无 JSON API**。
- 调查数据年份/样本量以项目官网与 CNSDA 元数据为准；本层卡片中凡未本机核对者均标注「上游声明」。
- 招聘平台报告（`employment-data.md`）为**平台自有用户样本**（非概率抽样），只能作市场侧补充，勿当劳动力市场代表值或与官方统计混用。
