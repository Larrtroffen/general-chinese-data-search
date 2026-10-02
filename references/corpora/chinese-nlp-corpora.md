# chinese-nlp-corpora —— 中文 NLP 语料聚合仓

- 去哪找：
  - `https://github.com/brightmart/nlp_chinese_corpus` —— 大规模中文 NLP 语料（维基/新闻/问答/翻译），**MIT**，9,920★。
  - `https://github.com/liuhuanyong/ChineseNLPCorpus` —— 中文 NLP 语料集合（语义词、领域共时/历时、评测），448★。
  - `https://github.com/qianzhengyang/AllDataPackages` —— 中文分词/词表/停用词/事件词表/问答/知识图谱/文本语料打包索引。
- 什么时候用：**手头没有语料，先来这里找"有没有人整过"**——预训练原始语料、词表/停用词、问答对、分词标注、知识图谱；比逐个爬站省事；也是找**中文词向量/语言模型配套语料**的入口。
- 怎么取：
  ```bash
  # 元数据/目录（不下载大数据）
  gh api repos/brightmart/nlp_chinese_corpus --jq '[.stargazers_count,.license.spdx_id,.pushed_at]|@tsv'
  gh api repos/brightmart/nlp_chinese_corpus/contents --jq '.[]|[.name,.type,.size]|@tsv'
  # 语料本体：读各仓 README 里的 Google Drive / 百度网盘 / 外部链接（仓内一般只放说明与图片）
  gh api repos/brightmart/nlp_chinese_corpus/readme --jq .content | base64 -d
  ```
- 覆盖（`nlp_chinese_corpus` 一期目标，README 实测）：
  - `wiki2019zh` **104 万**中文维基词条（json，1.6G / 压缩 519M）；
  - `news2016zh` **250 万**篇新闻（含关键词、描述）；
  - `baike2018qa` **150 万**带问题类型的问答；
  - `webtext2019zh` **410 万**社区问答 json；
  - `translation2019zh` **520 万**中英句对。
- 门槛：**GitHub 免登录**；语料本体经**网盘/Google Drive**（须自行下载，部分链接可能失效）；许可逐仓核（`nlp_chinese_corpus` = MIT，仅覆盖其处理成果，原始来源另有权利）。
- 实测：2026-10-03，macOS arm64：`gh api repos/brightmart/nlp_chinese_corpus` → 9,920★、`license=MIT`、`pushed 2026-02-06`，顶层 `README.md`(20 KB)+`resources/`(图片)；`gh api …/liuhuanyong/ChineseNLPCorpus` → 448★、`pushed 2018-12-16`，顶层仅 `README.md`+`newspaper_spider/`（多为外链索引）；`…/qianzhengyang/AllDataPackages` → 173★。
- 上游：`brightmart`（ALBERT_zh 作者）等社区维护者。

## 细节

### 聚合仓对比

| 仓库 | 侧重 | stars | 更新 | 形态 |
|---|---|---|---|---|
| `brightmart/nlp_chinese_corpus` | 大规模预训练语料（维基/新闻/QA/翻译） | 9,920 | 2026-02 | README + 网盘外链 |
| `liuhuanyong/ChineseNLPCorpus` | 词表 + 共时/历时/评测语料索引 | 448 | 2018-12 | README 索引 |
| `qianzhengyang/AllDataPackages` | 词表/停用词/事件/知识图谱/问答打包 | 173 | — | README 索引 |

## 坑

1. 多数聚合仓**只放 README 与网盘链接**，仓里没有语料本体；网盘链接会**失效**，先点开验活再规划。
2. "MIT" 只覆盖**处理成果/代码**，原始语料（维基、新闻、社区问答）仍受各自条款约束——正式引用回源核。
3. 历时语料另见本层 `ChineseDiachronicCorpus.md`；人民日报标注语料见 `rmrb-corpus.md`，勿与通用新闻语料混用。
4. 语料年份偏老（2016–2019），做"当前"研究要先确认时效。
