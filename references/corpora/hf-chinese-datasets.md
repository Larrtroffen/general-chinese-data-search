# hf-chinese-datasets —— HF 镜像的中文数据集

- 去哪找（走国内镜像）：`https://hf-mirror.com/datasets`；API `https://hf-mirror.com/api/datasets`。镜像与 HF Hub 同构，详见 `../methods/dataset-hubs.md`（本卡只补**中文子集**的检索入口）。
- 什么时候用：要找**HF 生态里的中文语料/指令数据/评测集**（规模远大于国内平台）；HF 直连下载不动时的中转；给中文模型准备 SFT/预训练集。
- 怎么搜：
  ```bash
  # ① 关键词（最简单）
  curl -s 'https://hf-mirror.com/api/datasets?search=chinese&limit=3'
  # ② 按语言标签过滤（中文）
  curl -s 'https://hf-mirror.com/api/datasets?filter=language:zh&limit=100'
  # ③ 排序取大热中文集
  curl -s 'https://hf-mirror.com/api/datasets?filter=language:zh&sort=downloads&direction=-1&limit=20'
  # ④ 单库文件树 / 直链
  curl -s 'https://hf-mirror.com/api/datasets/{repo}/tree/main'
  # CLI 下载：HF_ENDPOINT=https://hf-mirror.com huggingface-cli download <repo>
  ```
  返回字段同 HF Hub：`id` / `author` / `likes` / `downloads` / `gated` / `lastModified` / `sha` / `description` / `tags`。
- 覆盖：镜像 HF Hub 全量数据集元数据。中文相关集散落在：通用网页/预训练语料（`wikimedia/wikipedia`、`openbmb/UltraData-*`）、指令/SFT（`ZefanCai/Open-Jev` 等）、评测（`ikala/tmmluplus`）、语音/多模态中文集。**中文数据集的规模与更新实时变化，按需现搜**。
- 门槛：**公开库免登录**；标注 `gated: true` 的库仍需 **HF token**（镜像转发不了权限）；检索/元数据匿名可用。
- 实测：2026-10-03，macOS arm64，curl 8.x：`GET /api/datasets?search=chinese&limit=3` → **200**，返回 3 条（首条 `DataoceanAI/Chinese_Male_Speech_Synthesis_Corpus_Live_Streaming_for_Sales`）；`GET /api/datasets?filter=language:zh&limit=100` → **200**，返回 100 条，含 `wikimedia/wikipedia`、`openbmb/UltraData-SFT-Agent-2609`、`ikala/tmmluplus`、`zgcagi/ZGCM-1-Data` 等中文/多语集。
- 上游：Hugging Face Hub（`https://huggingface.co`）；国内镜像 `https://hf-mirror.com`。

## 细节

### 中文检索姿势

| 目的 | 参数 | 备注 |
|---|---|---|
| 关键词 | `search=chinese` / `search=中文` | 匹配 repo 名与描述 |
| 语言标签 | `filter=language:zh` | 依赖上传者打的 tag，覆盖不全 |
| 任务标签 | `filter=task_categories:...` | 可与 language 组合 |
| 热门排序 | `sort=downloads&direction=-1` | 找成熟/大热集 |
| 单库信息/文件 | `/api/datasets/{repo}`、`/tree/main` | 同 HF Hub |

## 坑

1. `filter=language:zh` **依赖社区自打标签**，会漏（没打 tag 的中文集搜不到）也会误纳多语集（如 `wikimedia/wikipedia`）；**别把 tag 当权威中文清单**。
2. 镜像只做**加速**，**不改权限**：`gated` 库仍需 HF token，镜像帮不上。
3. 数据集**许可逐库不同**（有些禁商用/需署名），用前必读仓库 README 的 license；HF 上二次分发的中文语料尤其要回源核。
4. 与国内平台分工：国内竞赛/产业集走 **天池/和鲸**、中文 NLP 大语料走 **ModelScope/HF**（见 `../methods/dataset-hubs.md`）；官方统计口径回 `../stats/`。
