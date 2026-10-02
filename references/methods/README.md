# methods/ —— 方法卡（跨站点流程，不是单一网站）

本层不放具体站点，放**跨站点的流程 / 检索方法**：当你要做的事是「怎么找」而不是「去哪个站」时，先来这一层。

## 文件一览

| 文件 | 来源 | 用途 | 状态 |
|---|---|---|---|
| `literature-delivery.md` | 自编（CALIS / NSTL / 国图 / ucdrs / CASHL 等站实测） | 从书名/篇名到全文：联合目录 → 文献传递 → 馆际互借的路由 | ✅ 本机实测 |
| `dataset-hubs.md` | 自编（天池 / 和鲸 / ScienceDB / ModelScope / HF-Mirror 实测） | 免费数据集市的 JSON 检索端点、参数、字段与许可 | ✅ 本机实测 |
| `microdata-access.md` | 自编（CFPS/CHARLS/CNSDA/北大 Dataverse/ICPSR 等实测） | 微观调查数据**申请路线图**（谁可申请/多久/是否要钱） | ✅ 入口实测 |
| `intl-data-apis.md` | 自编（World Bank/WHO/OECD/IMF/Eurostat/Comtrade 实测） | 国际统计库开放 API 速查（端点/参数/最小 curl） | ✅ 本机实测 |
| `officials-research.md` | 自编（单位门户 / 人大 / 组织部 / 年鉴 / 媒体 / 人物库实测） | 单位 → 领导之窗 → 人大任免 → 组织部公示 → 年鉴 → 媒体 → 人物库 | ✅ 本机实测 |
| `search-syntax.md` | 自编（综合引擎 + 站内检索实测） | 引擎操作符差异与站内高级检索参数（怎么拼 URL） | ✅ 本机实测 |
| `historical-web.md` | 自编（Wayback / CDX / archive.today / Common Crawl / 快照实测） | 旧页面、改版前正文、已删内容的回捞 | ⚠️ 部分可达 |
| `osint-china.md` | `UseOSINT/Skills`（MIT，commit `06243a5`） | 英文 OSINT 技能库里可迁移的中文检索法（只提炼方法，不引代码） | ⚠️ 上游声明 |
| `stat-yearbook-download.md` | 自编（国家统计局/3 省年鉴 + wget 配方实测） | 统计年鉴/公报的 URL 规律与**批量下载配方**（含命令） | ✅ 本机实测 |

## 选路

- 只有**书名/篇名/作者/ISBN/刊名年期**，要判断「能不能拿到全文、藏在哪个馆」 → `literature-delivery.md`。
- 要批量找**现成数据集**（CSV/JSON/图片/语料） → `dataset-hubs.md`；要官方统计口径则回 `../stats/`。
- 要还原**某单位 / 某街乡镇 / 某年的领导姓名、职务、任期**（或找任免 / 简历证据） → `officials-research.md`。
- 关键词拼不出、要用**引擎操作符或站内高级检索参数** → `search-syntax.md`。
- 页面已**改版 / 删除**、要找改版前正文或历史版本 → `historical-web.md`。
- 想借鉴**英文 OSINT 通用方法**（源分级、CDX 时间线、平台 ID 时间锚、图像地理定位） → `osint-china.md`。

## 相关

- 源清单总索引见 `../README.md`；领域层 `../gov/`、`../stats/`、`../media/`、`../academic/`、`../social/`、`../legal/`。
- 综合引擎逐 host 状态见 `../engines/README.md`；通用抓取 / 存档工具见 `../tools/`。
- 发现新方法 / 新源（复跑流程）见 `../meta/skills-discovery.md`。
