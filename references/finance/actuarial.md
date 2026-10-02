# actuarial —— 精算与保险研究数据入口

- 去哪找：
  - 中国精算师协会 `https://www.e-caa.org.cn/`——**研究资源**：专业研究 `/dataUpload/professional`、经验分析 `/dataUpload/empirical`；**专栏刊物** `/systemNews/19`（专栏观点 / 精算刊物）；通知公告 `/systemNews/10`。
  - 中国保险保障基金有限责任公司 `https://www.cisf.cn/cisf/index/index.shtml`——**基金规模** `/cisf/jjcj/jjgm/index.shtml`、缴纳公司名单 `/cisf/jjcj/jngsmd/index.shtml`、缴纳公示 `/cisf/jjcj/jngs/index.shtml`、风险评估报告 `/cisf/fxjc/fxpgbg/index.shtml`、**保险消费者信心指数** `/cisf/fxjc/xfzxxzs/index.shtml`、一周观察 `/cisf/fxjc/yzgc/index.shtml`、处置案例 `/cisf/fxcz/czal/index.shtml`。
  - 中国保险学会 `http://www.isc-org.cn/`——**《保险研究》下载** `/zkfwbxyj/index.jhtml`（分年卷 `/{YYYY}ndbxyj/index.jhtml`）、《保险理论与实践》下载 `/bxllysj/index.jhtml`、舆情报告 `/yqbg/index.jhtml`、课题研究 `/ktyj/index.jhtml` 与课题发布 `/ktfb/index.jhtml`、保险史志 `/bxsz/index.jhtml`。
  - 行业统计与公司披露见同层 `insurance.md`；监管口径见 `nfra.gov.cn.md`。
- 什么时候用：要**精算职业资格与考试信息、精算研究资料/经验分析、保险保障基金规模与缴纳名单、保险消费者信心指数、赔付/风险评估报告**，或要**保险学术论文（《保险研究》）、行业舆情与课题报告、保险史**时。
- 怎么搜：三站三种形态——精算师协会是 **JSON 接口**，保险保障基金是**静态 `.shtml` 列表**，保险学会是**分年 `.jhtml` 目录**。
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # ① 精算师协会：栏目列表 JSON（newsType 见下表）
  curl -sSL -A "$UA" -X POST 'https://www.e-caa.org.cn/dataUpload/listInformation' \
    -H 'Referer: https://www.e-caa.org.cn/dataUpload/professional' \
    --data 'pageNo=1&pageSize=12&newsType=12'
  # ② 保险保障基金：静态列表 → 文章   （注意必须 https）
  curl -sSL -A "$UA" 'https://www.cisf.cn/cisf/fxjc/xfzxxzs/index.shtml'
  # ③ 保险学会：《保险研究》某年卷
  curl -sSL -A "$UA" 'http://www.isc-org.cn/2024ndbxyj/index.jhtml'
  ```
  结果形态：精算师协会 = JSON（`{page,total,records,rows[]}`）；保险保障基金 = HTML 文章页（`/cisf/{YYYY-MM}/{DD}/article_{时间戳}.shtml`）；保险学会 = HTML 目录 + 文章页。
- 覆盖：精算师协会 = 协会动态/考试/研究资源/专栏刊物等分类（内容按 `newsType` 分栏，部分栏目当前为空）；保险保障基金 = 基金规模、缴纳单位、季度消费者信心指数（实测 2023Q3–2024Q4）、风险评估与处置案例；保险学会 = 《保险研究》1980 年卷起（下载页列 1980–2026 年卷）、《保险理论与实践》、舆情报告、历年课题立项名单。
- 门槛：三站浏览均**免费**；精算师协会接口免登录；保险学会站有注册/登录入口，**部分期刊下载是否限会员本机未实测**。保险保障基金无需登录。
- 实测：2026-10-03，macOS arm64，桌面 UA、20 s 超时、同主机 ≥1.5 s 间隔：
  - `https://www.e-caa.org.cn/` → `200/29,110 B`（title 中国精算师协会）；`http://` 同域 → `502`（**只走 https**）；`/dataUpload/professional` → `200/17,695`、`/dataUpload/empirical` → `200/17,377` ✅
  - `POST /dataUpload/listInformation`（`newsType=4`）→ `200` JSON `records:16`、`rows[]` 含 `informationId/informationTitle/informationUrl`；`newsType=12/13/19/20/22` → `200` `records:0`（栏目当前无内容）⚠️
  - `https://www.cisf.cn/cisf/index/index.shtml` → `200/69,890 B`（title 中国保险保障基金有限责任公司）；`/cisf/jjcj/jjgm/index.shtml` → `200/56,524`；`/cisf/fxjc/xfzxxzs/index.shtml` → `200/59,565`，条目如「2024年四季度中国保险消费者信心指数72.5」`/cisf/2025-04/23/article_2025042310581181608.shtml` → `200/63,289`；`/cisf/jjcj/jngsmd/index.shtml` → `200/57,984` ✅
  - `http://www.isc-org.cn/` → `200/19,694 B`（title 中国保险学会）；`/zkfwbxyj/index.jhtml` → `200/19,010`（年卷链接 1980–2026）；`/2024ndbxyj/index.jhtml` → `200/19,959`（含分页 `index_2.jhtml`）；`/yqbg/index.jhtml` → `200/13,409` ✅
- 上游：`e-caa.org.cn`（中国精算师协会）；`cisf.cn`（中国保险保障基金有限责任公司）；`isc-org.cn`（中国保险学会）。

## 细节

### 一、精算师协会 `/dataUpload/listInformation`（POST，form-urlencoded）

参数 `pageNo`、`pageSize`、`newsType`；返回 `{page,total,records,rows[]}`，`rows[]` 字段含 `informationId` `informationTitle` `informationUrl` `informationType` `auditTime` `publishTime` `informationIntro` `informationContent`（HTML）。

| newsType | 栏目 |
|---|---|
| `1` | 人才培养·考试新信息 |
| `4` | 协会动态 |
| `11` | 行业要闻 |
| `12` / `13` | 研究资源·专业研究 / 经验分析（实测空） |
| `14` / `15` | 国际交流·交流合作 / 会晤交流 |
| `17` / `23` | 会员支持·职位信息 / 会员通知 / 会员动态 |
| `19` / `22` | 专栏刊物·专栏观点（19）/ 精算刊物（22）（实测空） |
| `20` / `21` | 动态要闻·专业标准 / 行业规范 |

（`newsType` 映射自栏目页脚本；`12/13/19/20/22` 本机实测 `records:0`。）

### 二、保险保障基金栏目速查（`cisf.cn`）

| 主题 | 路径 | 形态 |
|---|---|---|
| 基金规模 | `/cisf/jjcj/jjgm/index.shtml` | 列表 |
| 缴纳公司名单 | `/cisf/jjcj/jngsmd/index.shtml` | 列表 |
| 缴纳公示 | `/cisf/jjcj/jngs/index.shtml` | 列表 |
| 风险评估报告 | `/cisf/fxjc/fxpgbg/index.shtml` | 列表 |
| 保险消费者信心指数 | `/cisf/fxjc/xfzxxzs/index.shtml` | 季度文章（指数值在标题） |
| 一周观察 | `/cisf/fxjc/yzgc/index.shtml` | 列表 |
| 处置案例 | `/cisf/fxcz/czal/index.shtml` | 列表 |
| 法律法规 | `/cisf/fxcz/flfg/index.shtml` | 列表 |

- 文章 URL 形态：`/cisf/{YYYY-MM}/{DD}/article_{YYYYMMDDHHMMSS}{序号}.shtml`；英文站 `http://www.cisf.cn:8088/cisfeng/`。

### 三、保险学会期刊目录

- 《保险研究》下载总入口 `/zkfwbxyj/index.jhtml` → 年卷 `/{YYYY}ndbxyj/index.jhtml`（页面列出 1980–2026），年卷内用 `index_2.jhtml`… 翻页。
- 《保险理论与实践》下载 `/bxllysj/index.jhtml`；投稿系统分别在 `https://bxyj.cbpt.cnki.net`、`https://bxls.cbpt.cnki.net`。

## 坑

1. **精算师协会只认 https**：`http://www.e-caa.org.cn/` 本机 `502`，改 `https://` 即 `200`。
2. **研究资源/专栏刊物栏目本机为空**（`listInformation` 返回 `records:0`）：接口正常，是内容未发布；别据此判断"接口坏了"，先用 `newsType=4` 验证连通性。
3. **保险保障基金文章时间戳不可猜**，必须从栏目列表页解析 `article_*.shtml` 全链。
4. **保险学会期刊下载可能需登录**：站点有注册/登录，本机未验证匿名能否下载全文——引用前实测；目录页本身免登录可看。
5. 中国保险学会的**舆情报告/课题名单是 `<a>` 列表页**，条目年份跨度大，抓取时按 `index_N.jhtml` 翻页；首页导航未见站点检索入口，别指望搜索框。
6. 这些源偏向**研究/指数/基金**，公司级财务与偿付能力数据在 `insurance.md`（披露平台）与 `nfra.gov.cn.md`，别混用。
