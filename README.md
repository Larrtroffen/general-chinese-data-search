# general-chinese-data-search —— 中文公开资料源库（Agent Skill）

面向**中文公开资料检索**的 Agent Skill：把「去哪儿找、怎么找」整理成 **25 个分层、400+ 张来源卡**，
外加一组**零依赖脚本**（标准库 + 系统 `curl`）。不搬运数据本体——只维护**来源与方法**。

> 适用场景：查政策文件/公报、翻单位名录与人事任免、检索微信公众号文章、抓政府网站语料、
> 找统计口径与调查数据、翻方志档案与民国文献、定位各类"可能藏文件"的政务栏目与文档分享站。

## 怎么用

1. **作为 Agent Skill**：把整个目录放进 `~/.agents/skills/`（或支持 Agent Skills 的客户端技能目录），
   入口是 `SKILL.md`；各层索引在 `references/<层>/README.md`。
2. **当资料清单直接查**：从 `references/README.md`（总索引）或根目录 `CANDIDATES.md`（待收编候选池）看起。
3. **脚本**（`scripts/`，无需安装依赖）：
   ```bash
   python3 scripts/sogou_wechat.py search queries.txt --out crawl.jsonl --resolve 2018
   python3 scripts/mp_article.py batch --in crawl.jsonl --out-dir articles
   python3 scripts/bjgov_search.py 吹哨报到 --filter bjchy.gov.cn
   python3 scripts/site_crawl.py --host www.bjdx.gov.cn --budget 20
   python3 scripts/probe.py urls.txt --out status.csv
   ```

## 目录结构

```
registry/         ← 全量源注册表（CSV：一条一行 = 一个源；all.csv 为总表）
references/       ← 精讲来源卡（25 层；每层有 README.md 索引）
scripts/          ← 零依赖脚本（检索/抓取/探活/注册表维护）
SKILL.md          ← Agent Skill 入口（顶层工作流 + 分层总表）
CANDIDATES.md     ← 待收编候选池
```

| 层 | 内容 |
|---|---|
| `engines/` | 综合搜索引擎（头条/必应/神马/百度移动/360/搜狗） |
| `wechat/` | 微信生态：搜狗微信、正文抓取、客户端按号全量 |
| `gov/` | 政府网站：中央·北京站群（52 委办局）·区/街乡镇·公开渠道十类·人才/国防/营商 |
| `party/` | 党建与党史 |
| `stats/` | 统计与区划、部委统计、地理数据、迁徙、农业、县域、投入产出 |
| `business/` | 企业与市场：公告/交易所/债券/海关/招投标/商业库 |
| `finance/` | 金融与财税：央行/外汇/监管/支付/银行/保险/财政/地方债城投 |
| `health/` | 健康与人口：疾控/卫健/药监/GBD/人口普查 |
| `surveys/` | 调查与微观数据：CFPS/CGSS/CHARLS/CHFS…与申请路线 |
| `repos/` | 数据仓储：Dataverse/Zenodo/ICPSR/国家科学数据中心 |
| `intl/` | 国际组织/跨国调查/IFI 项目库/报告全文库/留学生华侨 |
| `industry/` | 行业与协会、国资、交通港航、房地产、文旅体育 |
| `regional/` | 区域与地方：省级社科院/高校平台/港澳台统计/县级入口 |
| `env/` | 环境·能源·碳：碳核算、空气质量、环评、执法督察 |
| `civil/` | 公益与志愿服务 |
| `culture/` | 文化·民族·宗教·语言·遗产 |
| `media/` | 媒体与数字报、地方融媒、文库站、论坛附件区 |
| `academic/` | 学术文献：CNKI 套件、NSTL、预印本、海外馆藏（含 JACAR/胡佛/欧洲敦煌） |
| `corpora/` | 语料与文本数据 |
| `legal/` | 法律、标准、案例、文书 |
| `archives/` | 方志·档案·古籍·民国文献·历史地图 |
| `social/` | 社交平台与问政渠道 |
| `tools/` | 抓取/OCR/存档等工具 |
| `methods/` | 跨源方法卡：文献传递、检索语法、历史回捞、官员检索、数据 API |
| `meta/` | 元资源：中国应用 MCP 索引、发现机制、写作规范 |

每张来源卡字段固定：`去哪找 · 什么时候用 · 怎么搜/怎么取 · 覆盖 · 门槛 · 实测 · 上游`（规范见 `references/meta/style.md`）。

## 维护

- **规模**：注册表 **18,030 行 / 12,772 唯一主机**（一条 = 一个可定位的源）；其中**探活存活 12,110 条（2xx/3xx）**、失效 4,809、GitHub 仓库声明 1,416（爬虫索引）。覆盖：中央党政群团 225 · 省级+地市 367 · 区县 ~3,100 · 北京全量 870 · 高校 2,912 · 医院 ~1,100 · 国企官网 1,094 · 媒体/数字报/出版社 ~1,700 · 馆藏机构 719 · 开放数据与统计 657 · 海外/港台机构 457 · 爬虫仓库 1,416 · 既有卡片抽取 3,891。**远超 5000 条目标**。
- **状态纪律**：✅/⚠️/❌ 均来自**本机实测**（卡内注明日期）；未探测的写「未验证」。
- **定期体检**：`scripts/registry_probe.py` 批量探活注册表；`scripts/probe.py` 体检单批 URL；每季度按 `references/meta/skills-discovery.md` 复跑发现新源，追加到 `CANDIDATES.md`。
- 实测状态是**时间快照**（多为 2026-10）：站点会改版/下线，引用前先复测。

## 声明

- 仅收录**公开可访问**的入口、检索方法与元信息；**不包含**受版权保护的数据/文献本体。
- 部分卡片涉及需登录/订阅或反爬严格的站点，均如实标注门槛；请遵守各站服务条款与当地法律。
- 引用的第三方仓库/工具版权归其作者；本库只写链接与用法，不复制其代码。
