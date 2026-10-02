# references/corpora —— 语料与文本数据源索引

本目录收录**以文本为数据**的语料库与语料仓储：现代汉语、古汉语/佛典、新闻与历时语料、中文 NLP 数据集聚合（GitHub / Hugging Face）、官方语料平台。原则：**优先官方或开放接口直接检索/下载**；商业或需授权的只作线索并标清门槛；语料本体不入库，只记录入口、参数、规模与许可。

## 文件一览

| 文件 | 来源 | 用途/何时用 | 状态 |
|---|---|---|---|
| `bcc.blcu.edu.cn.md` | 北京语言大学 BCC | 多领域**例句/索引**检索 + **匿名字/词频表**下载（口语/古汉语/文学/新闻/近代汉语/多领域） | ✅ 频表可取 |
| `ccl.pku.edu.cn.md` | 北京大学 CCL | 现代/古代汉语**索引行**，匿名 GET 直接检索（6 亿字符） | ✅ 检索可用 |
| `nclds.xmu.edu.cn.md` | 国家语委·教育教材语言资源中心（厦大） | 教材/报刊/网站/口语等 **8 分域库**；并记录"语料库在线"失效 | ⚠️ 取数需 POST |
| `rmrb-corpus.md` | 人民日报标注语料库（PFR）多版本 | 1998 人民日报**分词+词性标注**语料；官方 DOI + GitHub 镜像 | ✅ 入口已核 |
| `cluebenchmarks.md` | CLUE / FewCLUE / CLUECorpus2020 | 中文 NLP **评测基准** + **100GB** 预训练语料 | ⚠️ 语料需申请 |
| `chinese-nlp-corpora.md` | GitHub 聚合仓（nlp_chinese_corpus 等） | 维基/新闻/问答/翻译大规模中文语料 + 词表索引 | ✅ 仓库可达 |
| `ChineseDiachronicCorpus.md` | 中文历时语料库（刘焕勇） | **历时**语料：腾讯新闻 2009–2016 / 人民日报 1946–2003 / 参考消息 1957–2002 | ⚠️ 网盘分发 |
| `yuliao.people.cn.md` | 人民网语料社区 | **官方合规**《人民日报》等语料包（专题/行业） | ⚠️ 需登录 |
| `cbeta.md` | CBETA 中华电子佛典 | 汉文**大藏经全文** + API + XML 全集（佛典/宗教研究） | ✅ 在线/API 可用 |
| `hf-chinese-datasets.md` | Hugging Face（hf-mirror） | HF 生态**中文数据集**检索入口（语言标签/关键词） | ✅ 检索可用 |

## 选路

- **要带上下文的例句/索引行（语言学、词频、搭配）** → 现代汉语用 `ccl.pku.edu.cn.md`（匿名 GET 最省事）；要多领域/网络语料用 `bcc.blcu.edu.cn.md`；教材/教育语料用 `nclds.xmu.edu.cn.md`。
- **要现成的字频/词频表** → `bcc.blcu.edu.cn.md` 的 `/api/datasets`（匿名 zip 直下，12 张表）。
- **要中文 NLP 训练/评测数据** → 评测集与预训练大语料 `cluebenchmarks.md`；维基/新闻/问答/翻译聚合 `chinese-nlp-corpora.md`；HF 生态大池 `hf-chinese-datasets.md`。
- **要人民日报语料** → **标注**（分词/词性）用 `rmrb-corpus.md`；**未标注历时正文**用 `ChineseDiachronicCorpus.md`；**合规官方授权**用 `yuliao.people.cn.md`；**全量历年电子版抓取**见 `../media/people-daily-crawler.md`。
- **要古汉语/近代语料** → **佛典**用 `cbeta.md`；经史子集与古籍整包用 `../archives/daizhige.md`、`../archives/ctext.md`、`../archives/kanripo.md`。
- **要微信公众号/社交媒体语料（自采）** → 走本库 `../wechat/` 与 `../social/` 两层（`weixin.sogou.com.md`、`wechatspider.md`、`weibo.com.md`、`zhihu.com.md`、`xiaohongshu-mcp.md` 等），本层不重复。

## 相关

- 数据集市与 API：`../methods/dataset-hubs.md`（天池/和鲸/ScienceDB/ModelScope/HF-Mirror）。
- 古籍与档案：`../archives/`（daizhige、ctext、kanripo、guji.nlc.cn、sinica…）。
- 新闻与数字报：`../media/`（people-daily-crawler、epaper/、xinwenlianbo-archive）。
- 微信/社交自采：`../wechat/`、`../social/`。
- 抓取与清洗工具：`../tools/`。
- 跨层候选与进度：`../../CANDIDATES.md`。
- 所有状态码、接口与示例命令均为 2026-10-03 当日实测；未本机验证项已在各卡内标注。
