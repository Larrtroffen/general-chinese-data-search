# rmrb-corpus —— 人民日报标注语料库（公开版本）

- 去哪找（官方一手）：北京大学开放研究数据平台 **现代汉语多级加工语料库**，`https://opendata.pku.edu.cn/dataset.xhtml?persistentId=doi:10.18170/DVN/SEYRX5`（DOI `10.18170/DVN/SEYRX5`），下载件 `5-199801基本标注语料库-2003年版规范-20170612.rar`。
- 去哪找（镜像/衍生，免注册）：
  - `https://github.com/chenhui-bupt/PeopleDaily1998` —— 仓内 `199801.zip`（20.3 MB），1998 年人民日报标注语料。
  - `https://github.com/howl-anderson/tools_for_corpus_of_people_daily` —— 处理工具集（Apache-2.0，含正则在"官方注册自取"的说明）。
  - 百度 AI Studio 数据集 `datasetdetail/190121` —— "人民日报 新闻数据集 1998-2022"（第三方整理，口径需核）。
- 什么时候用：要**经典分词/词性标注语料**做中文 NLP 训练或评测（1998 年人民日报 = 中文分词/词性/NER 的事实标准训练集）；要一个**带人工标注**的小规模高质量语料；复现老论文。
- 怎么取：
  ```bash
  # 镜像直取（免注册，20 MB）
  curl -L -o 199801.zip 'https://raw.githubusercontent.com/chenhui-bupt/PeopleDaily1998/master/199801.zip'
  # 或克隆工具仓
  git clone --depth 1 https://github.com/howl-anderson/tools_for_corpus_of_people_daily
  ```
  官方版需在 `opendata.pku.edu.cn` **注册账号后**下载（语料为版权材料，官方按注册用户分发）。
- 覆盖：**PFR 语料库 1.0** = 1998 年人民日报语料，**600 多万字节**，由北京大学计算语言学研究所 + 富士通研究开发中心制作，**已做分词 + 词性标注**；含 `199801`（1998 年 1 月起）逐日文件。人民网语料社区另有 1998–2022 电子版整理（非标注）。
- 门槛：**镜像免注册**（GitHub zip）；**官方版需注册** `opendata.pku.edu.cn` 账号；语料为版权材料，仓库均**不直接分发原始语料**则另说（`chenhui-bupt` 仓内含 zip）。
- 实测：2026-10-03，macOS arm64：`GET opendata.pku.edu.cn/dataset.xhtml?persistentId=doi:10.18170/DVN/SEYRX5` → **200**，页面标题「Corpus of Multi-level Processing for Modern Chinese - Comprehensive Language Knowledge Base」；`gh api repos/chenhui-bupt/PeopleDaily1998` → 仓库含 `199801.zip`(20,305,578 B) + `README.md`；`gh api repos/howl-anderson/tools_for_corpus_of_people_daily` → `license=Apache-2.0`、`pushed_at=2023-07-06`。
- 上游：北京大学计算语言学研究所（ICL/PKU）· 富士通研究开发中心；`https://github.com/chenhui-bupt/PeopleDaily1998`。

## 细节

### 版本对照

| 版本 | 范围 | 标注 | 入口 | 门槛 |
|---|---|---|---|---|
| PFR 1.0（199801，2003 版规范） | 1998 年人民日报，600 万+ 字节 | 分词 + 词性 | `opendata.pku.edu.cn` DOI `10.18170/DVN/SEYRX5` | 注册 |
| PeopleDaily1998 镜像 | 同上（`199801.zip` 20 MB） | 同上 | GitHub `chenhui-bupt/PeopleDaily1998` | 免注册 |
| 1998-2022 新闻数据集 | 人民日报电子版正文 | 无标注 | 百度 AI Studio `datasetdetail/190121` | 登录（第三方） |

工具仓 `tools_for_corpus_of_people_daily` 已把 199801 的**标注规范坑**写清（姓名拆分 `王/nrf 小明/nrg` 需合并、全角转半角、词性 `t/nr/ns/nt` ↔ DATE/PERSON/GPE/ORG），并附 ConLL/BILUO 转换脚本。

## 坑

1. **版权**：人民日报语料是版权材料，官方仅对注册用户开放；镜像仓按各自 README 说明使用，商用前自行评估。
2. `199801.zip` 是**分词+词性**的标注文本（每行一词带 `/词性`），**不是**原始新闻全文；要全文另见 `people-daily-crawler`（`../media/`）或人民网语料社区。
3. Wiki/博客里的 "人民日报语料" 版本混杂（1998 全年版 / 1–4 月版 / 199801 单月版），**先确认月份与标注规范再引用**。
4. 百度网盘的衍生版（如 `ChineseDiachronicCorpus`）含 1946–2003 人民日报，与本卡的"标注语料"不是同一物（前者为未标注历时正文），勿混用。
