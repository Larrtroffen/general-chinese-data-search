# hf-mirror.com —— HF Hub 数据集镜像检索

- 去哪找：镜像门户 `https://hf-mirror.com/`；数据集页 `https://hf-mirror.com/datasets`；**API** `https://hf-mirror.com/api/datasets?search=<词>`（与 `huggingface.co/api/datasets` 同构）
- 什么时候用：找 **HF Hub 上的中文 / 多语数据集**（语料、指令数据、评测集、语音、图像）；HF 官网在本机不通时用镜像做检索与下载；给 `huggingface_hub` / `datasets` 换源（`export HF_ENDPOINT=https://hf-mirror.com`）。
- 怎么搜：
  ```bash
  curl -s 'https://hf-mirror.com/api/datasets?search=chinese&limit=2&full=true'
  curl -s 'https://hf-mirror.com/api/datasets?filter=language:zh&sort=downloads&direction=-1&limit=3'
  # → [{"_id":"621ffdd236468d709f182a80","id":"allenai/c4","author":"allenai",
  #     "gated":false,"likes":674,"lastModified":"2024-01-09T19:14:03.000Z","sha":"…",
  #     "description":"…","tags":[…]},…]
  ```
  - 参数：`search`（全文）、`author`、`filter`（如 `language:zh` / `task_categories:text-classification`，可多条）、`sort`（`downloads` / `likes` / `lastModified` / `trendingScore`）、`direction=-1`、`limit`、`full=true`（补全元数据）。
  - 单库 `/api/datasets/{repo}`；文件树 `/api/datasets/{repo}/tree/main`；文件直链 `/datasets/{repo}/resolve/main/{path}`。模型同理 `/api/models`。
- 覆盖：HF Hub 全量公开数据集镜像（含 `gated` 库的元数据）；中英双语语料与各类评测集都在。
- 门槛：公开库检索 / 列目录 **免登录**；公开库下载免登录；`gated` 库仍需 HF token（镜像转发不了权限）。
- 实测：2026-10-03，macOS arm64，curl：`/api/datasets?search=chinese&limit=2&full=true` → **200**，1,729 B；`?filter=language:zh&sort=downloads&direction=-1&limit=3` → **200**，10,288 B（首条 `allenai/c4`）；`https://hf-mirror.com/` → **200**，`<title>HF-Mirror</title>`。
- 上游：`https://hf-mirror.com/`（公益镜像）；上游 `https://huggingface.co/`

## 坑

- **`datasets-server.huggingface.co` 本机 20s 超时**：预览 / `/rows` / `/search` 那套行级接口走不通；镜像只代理 Hub API 与文件，不代理 datasets-server。
- 镜像不做权限转发：`gated` 数据集仍要真 HF token。
- HF 官方另有 parquet 转换端点 `https://huggingface.co/api/datasets/{repo}/parquet`（上游声明，未本机实测），本机经镜像未验。
- 镜像的筛选能力 = 上游 Hub 的筛选能力，镜像本身不加索引。
