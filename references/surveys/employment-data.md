# employment-data —— 招聘平台就业与薪酬报告

- 去哪找：智联招聘报告中心（大数据研究报告）`https://rd5.zhaopin.com/report/industry/nologin`，报告详情 `https://rd5.zhaopin.com/report/industry/detail/nologin?reportId=<id>`；BOSS 直聘文章列表 `https://www.zhipin.com/web/common/geo/article-list.html`，数据接口 `https://www.zhipin.com/wapi/moment/pc/longText/geo/list`，白皮书 PDF `https://z.zhipin.com/H5/html/pdf/white_paper.pdf`；前程无忧人力资源调研中心 `https://research.51job.com/`，报告 PDF 按年直链 `https://research.51job.com/pdf/resource/{YYYY}/resource.pdf` 与 `…/pdf/resign/{YYYY}/total1.pdf`；猎聘无公开报告中心，公司 IR 入口 `https://ir.liepin.com/`。
- 什么时候用：要**招聘平台自有口径**的就业市场景气、招聘/应届薪酬、应届生就业力、人才流动与紧缺岗位、白领跳槽指数、AI 对劳动力市场影响等；官方统计（国家统计局 / 人社部）之外的市场侧补充口径，或需要可直接引用的行业报告 PDF。
- 怎么搜：智联进 `rd5` 报告中心列表、按 `reportId` 看详情（**WAF 安全验证，需浏览器**）；BOSS 直聘 `article-list.html` 正文由 JS 渲染，数据走 `GET /wapi/moment/pc/longText/geo/list?page=&pageSize=` 返回 JSON（IP 风控）；前程无忧**无报告索引页**，按年份拼 PDF 直链（`resource`=人力资源白皮书、`resign`=离职与调薪调研报告）；猎聘报告经微信公众号/新闻稿发布，检索转第三方聚合站。结果形态：PDF / HTML / JSON 混合。
- 覆盖：前程无忧 `resource.pdf` **2021–2025**（2026 未出），`resign` 2022·2023·2025·2026（实测）；智联、BOSS 直聘、猎聘为**历年零散发布**（校招就业力、年度/季度薪酬、跳槽指数、平台治理公报等），站内无统一年度清单，年份以发布方为准。粒度：行业 / 城市 / 职能 / 学历 / 经验 / 薪酬；更新：年度 + 季度（薪酬、招聘趋势）。
- 门槛：前程无忧 PDF **免费直下**（无登录）；智联报告中心 `nologin` 路径免登录但**被 WAF 安全验证拦 curl**；BOSS 直聘浏览免费、接口需可信 IP（返回 `code 35`）；猎聘无统一下载入口，第三方聚合站多需注册/付费。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA、`-L`、20s 超时——`https://www.zhaopin.com/` 200（979,662 B）；`rd5.zhaopin.com/report/industry/nologin` 404（`text/plain` 9 B），改 `…/report/industry/list/nologin`、`…/report/industry/detail/nologin?reportId=1` 均 200 但正文为「Security Verification」安全验证页（2,177 B），`research.zhaopin.com/` 403；`https://www.zhipin.com/web/common/geo/article-list.html` 200（15,462 B，`<title>Geo文章列表-BOSS直聘`，正文仅「加载中…」），`GET /wapi/moment/pc/longText/geo/list?page=1&pageSize=10` 200 `application/json` 返回 `{"code":35,"message":"您的IP地址存在异常行为."}`，`z.zhipin.com/H5/html/pdf/white_paper.pdf` 200 `application/pdf`；`https://www.liepin.com/` 200（376,051 B），`/report/`、`/statistic/`、`/research/`、`/news/` 及 `m.liepin.com/report/` 均 404（返回 SPA 壳 4,933 B），`https://ir.liepin.com/` 200（3,482 B）、`/knowledge/` 200（33,937 B）；`https://research.51job.com/` 200（8,783 B）、`/salary.php` 200（14,068 B）、`/talentdate.php` 200（9,887 B），`/result.php` 正文「研究成果 页面正在建设中」，HEAD `pdf/resource/{2021,2022,2023,2024,2025}/resource.pdf` 200 `application/pdf`、`pdf/resource/2026/resource.pdf` 302、`pdf/resign/{2023,2025,2026}/total1.pdf`、`pdf/resign/2022/consume1.pdf`、`pdf/jifen/reward.pdf` 均 200（仅探测，未下载本体）。
- 上游：智联招聘 `https://www.zhaopin.com/`；BOSS 直聘 `https://www.zhipin.com/`；猎聘 `https://www.liepin.com/`；前程无忧人力资源调研中心 `https://research.51job.com/`。

## 细节

### 各平台入口与形态（2026-10-03 实测）

| 平台 | 入口 | 形态 | 可用性 |
|---|---|---|---|
| 智联招聘 | `rd5.zhaopin.com/report/industry/nologin` | HTML 列表 + `reportId` 详情（网页/PDF） | ⚠️ WAF 安全验证 |
| BOSS 直聘 | `www.zhipin.com/web/common/geo/article-list.html` | JS 渲染列表 + JSON `/wapi/moment/pc/longText/geo/list` | ⚠️ IP 风控（`code 35`） |
| 猎聘 | 无公开入口 | 公众号 / 新闻稿；第三方聚合收录 | ❌ 无统一报告中心 |
| 前程无忧 | `research.51job.com/` | 服务页 HTML + 报告 PDF 直链 | ✅ PDF 可下 |

### 前程无忧 PDF 直链规律（按年份可枚举）

| 报告 | URL 模板 | 实测存在年份 |
|---|---|---|
| 人力资源白皮书 | `https://research.51job.com/pdf/resource/{YYYY}/resource.pdf` | 2021·2022·2023·2024·2025（2026 → 302） |
| 离职与调薪调研报告 | `https://research.51job.com/pdf/resign/{YYYY}/total1.pdf` | 2023·2025·2026（2022 为 `…/2022/consume1.pdf`；2024 未测） |
| 积分兑换说明 | `https://research.51job.com/pdf/jifen/reward.pdf` | 固定单文件 |

- 子栏目页：`salary.php`（薪酬数据服务，**付费定制**）、`talentdate.php`（人才数据服务）、`government.php` / `company.php`（政府 / 企业案例）、`result.php`（研究成果，标注「建设中」）、`about.php`。
- 平台报告清单不在站内，PDF 直链靠年份拼；缺失年份会 302 回首页，需逐个试。

### 各平台报告主题（上游声明，未本机逐篇核对）

- **智联招聘**：大学生就业力调研报告（年度）、《中国企业招聘薪酬报告》（季度）、白领跳槽指数、新质产业/新质生产力人才需求、AI 大模型对劳动力市场潜在影响、城市大数据分析等。
- **BOSS 直聘**：人才资本趋势报告（年度）、人才吸引力报告（季度）、平台治理与服务公报、就业市场景气 / 新发职位观察等。
- **猎聘（猎聘大数据研究院）**：季度招聘调研报告、中高端人才就业观察、留学归国人才全景报告、高校毕业生就业数据报告、紧缺岗位薪资报告等。

## 坑

1. **智联 `rd5` 是 WAF 站**：`nologin` 路径虽标「免登录」，curl 仍拿不到内容（安全验证页），UA 无效；须浏览器或转第三方全文（三个皮匠 / 报告汇 / 搜弘文库等，注意其为转载）。
2. **BOSS 直聘接口有 IP 风控**：`/wapi/moment/pc/longText/geo/list` 返回 `{"code":35,"message":"您的IP地址存在异常行为."}`——需浏览器上下文且非常用数据中心 IP，列表页正文为空壳，纯 curl 不可得。
3. **前程无忧无报告索引页**（`result.php` 建设中）：只能按 `{YYYY}` 拼 PDF 直链，年份缺失 302；`resource`.pdf 与 `resign`.pdf 目录名、文件名都不同，勿互套。
4. **口径非概率抽样**：这些是平台**自有用户样本**（求职者/企业非随机），不等于劳动力市场总体；引用须标平台名与发布年份，勿当官方统计代表值。
5. **猎聘无 web 报告中心**：重点报告多在微信公众号「猎聘大数据研究院」+ 新闻稿发布，站内不留档；需要时检索 `猎聘 + 报告名 + 年份` 再核原始 PDF 出处。
6. **版权与时效**：报告版权归各平台，PDF 直链可能改路径或下线；重要报告及时留存并记录获取日。官方劳动力口径另见 [`../stats/README.md`](../stats/README.md)（国家统计局调查失业率等），人社/医保口径见本层 [`social-insurance.md`](social-insurance.md)。
