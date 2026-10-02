# cluebenchmarks —— 中文 NLP 评测集与预训练语料

- 去哪找：官网 `https://www.cluebenchmarks.com/`（榜单/数据集说明）；仓库 `https://github.com/CLUEbenchmark/CLUE`（测评基准）、`https://github.com/CLUEbenchmark/FewCLUE`（小样本基准）、`https://github.com/CLUEbenchmark/CLUECorpus2020`（100GB 预训练语料）。
- 什么时候用：要**中文 NLP 评测数据集**（分类/相似度/推理/阅读理解）做 baseline 或对比；要**中文预训练原始语料**（Common Crawl 清洗，100GB）；要中文词表/大模型测评报告线索。
- 怎么取：
  ```bash
  git clone --depth 1 https://github.com/CLUEbenchmark/CLUE
  git clone --depth 1 https://github.com/CLUEbenchmark/FewCLUE        # datasets/ 下每个任务一个目录
  # CLUECorpus2020 数据不直接给：按 README，邮件申请（用途/机构/申请者介绍），承诺不转第三方
  gh api repos/CLUEbenchmark/CLUECorpus2020/readme --jq .content | base64 -d
  ```
  各任务数据的**百度网盘/Google Drive 链接**写在仓库 README 与 `datasets/*/readme`；仓库本身主要是脚本与基线。
- 覆盖：
  - **CLUE**：10 大任务（AFQMC 相似度、TNEWS 新闻分类、IFLYTEK 长文本、CMNLI/OCNLI 推理、CSL 摘要、WSC 指代…）+ 9 基线。
  - **FewCLUE**：10 个小样本任务（`bustm`/`chid`/`cluewsc`/`csl`/`csldcp`/`eprstmt`/`iflytek`/`ocnli`/`tnews` + 1）。
  - **CLUECorpus2020**：**100 GB** 高质量中文预训练语料（Common Crawl 中文部分清洗），附 8,021 词元小词表；技术报告 arXiv:2003.01355。
- 门槛：**仓库/GitHub 免登录**；**CLUECorpus2020 数据需邮件申请**（README 明示）；部分数据集下载走百度网盘。
- 实测：2026-10-03，macOS arm64：`gh api` CLUE → 4,283★、`pushed 2026-02-06`；FewCLUE → 517★、`pushed 2022-09-21`；CLUECorpus2020 → 1,021★、`license=MIT`（仅代码）、README 确认"100GB / 邮件申请"；FewCLUE 含 `datasets/{bustm,chid,cluewsc,csl,csldcp,eprstmt,iflytek,ocnli,tnews}`。
- 上游：CLUE 中文语言理解测评基准团队（`https://github.com/CLUEbenchmark`）。

## 细节

### 仓库速查（2026-10-03 实测）

| 仓库 | 用途 | stars | license | 数据获取 |
|---|---|---|---|---|
| `CLUEbenchmark/CLUE` | 10 任务中文测评基准 | 4,283 | 未声明 | README/网盘 |
| `CLUEbenchmark/FewCLUE` | 小样本评测（10 任务） | 517 | 未声明 | `datasets/` + 网盘 |
| `CLUEbenchmark/CLUECorpus2020` | 100GB 预训练语料 + 小词表 | 1,021 | MIT（代码） | **邮件申请** |

## 坑

1. **仓库不等于数据**：CLUE/FewCLUE 仓里主要是基线代码与脚本，任务数据在 README 给出的网盘链接；CLUECorpus2020 数据**必须邮件申请**。
2. 各任务许可**逐条不同**（新闻/法律/医疗来源各异），正式发布前必核。
3. CLUECorpus2020 只有 **100 GB 全量**，无轻量抽样包；本地磁盘与预处理成本要先估。
4. 榜单已转向 SuperCLUE（`superclueai.com`），老 CLUE 榜单维护变慢；引用注意年份。
