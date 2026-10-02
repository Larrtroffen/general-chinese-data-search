# MinerU —— 文档解析 OCR（云 API / 本地 CLI）

`opendatalab/MinerU`（AGPL-3.0，4.0.10）把 PDF/图片/Office 解析成 Markdown/HTML/LaTeX/DOCX/EPUB 等 9 种格式。对我们最有价值的是**云端「Agent 轻量解析 API」：免登录、无需 Token、IP 限频**，专为 AI Agent 设计（≤10 MB、≤20 页、固定轻量模型、只出 Markdown）；其次是本地 `mineru` CLI（离线、隐私优先，要 Python 3.10+）。

- 去哪找：仓库 https://github.com/opendatalab/MinerU ；云端 API 文档（含 Agent API 全参数）https://mineru.net/apiManage/docs ；网页版（免费额度）https://mineru.net/ ；本地 CLI 安装/档位 https://opendatalab.github.io/MinerU/zh/quick_start/ · `/usage/tiers/`
- 什么时候用：拿到**扫描 PDF / 图片版公报 / 表格多的统计资料**，要文本 + 表格结构；不想本地装依赖，只想**一条 curl 把 PDF 变 Markdown**（Agent 轻量 API）；有 token 且要**高精度、批量（≤200）、多格式输出**（精准解析 API）；本地已有 Py3.10+，要**离线批量**（`mineru` CLI，Apple Silicon 走 `standard` 档）
- 怎么用：见下三路（A 免 token Agent API / B 带 token 精准 API / C 本地 CLI）
- 覆盖：输入 PDF/图片/Office → 输出 Markdown/HTML/LaTeX/DOCX/EPUB 等 9 种；Agent API 限 ≤10 MB / ≤20 页、只出 Markdown（CDN 链接）；精准 API 每账号每天 1000 页最高优先级、单文件 ≤200 MB / ≤200 页、批量 ≤200；许可 **AGPL-3.0**（本地部署代码有传染性，只调云 API 不受影响）
- 门槛：Agent API 免 token（每 IP 每分钟限频，超限 429）；精准 API 需 `MINERU_TOKEN`；本地 CLI 需 Python ≥3.10,<3.15（本机未装）
- 实测：2026-10-03，macOS 27（arm64），curl 8.x ——免 token 端点存在、签名上传跑通、但输出的 markdown 三次均 0 字节；完整记录见下
- 上游：https://github.com/opendatalab/MinerU

## 细节

### A. 云端 Agent 轻量 API —— 免 Token（本机实测协议通）

```bash
# ① 提交（JSON，不要 multipart）→ 拿 task_id + 签名上传 URL
curl -s -X POST -H 'Content-Type: application/json' \
  -d '{"file_name":"doc.pdf","language":"ch","page_range":"1-20","enable_table":true,"is_ocr":true}' \
  'https://mineru.net/api/v1/agent/parse/file'
# ② PUT 上传：必须不带 Content-Type，否则 OSS 签名 403
curl -X PUT --upload-file doc.pdf -H 'Content-Type:' '<返回的 file_url>'
# ③ 轮询 state: waiting-file → running → done，done 后拉 markdown_url
curl -s 'https://mineru.net/api/v1/agent/parse/<task_id>'
```

远程文件另有 `POST /api/v1/agent/parse/url`，body `{"url":"https://.../a.pdf","language":"ch"}`。
限制：**≤10 MB / ≤20 页**；仅 PDF/图片/docx/pptx/xlsx；**只出 Markdown（CDN 链接）**；每 IP 每分钟限频（超限 429）。官方明说**国外 URL（github/aws）会超时** → 先下到本机再 PUT。

### B. 云端精准解析 API（需 Token，能力全）

在 `mineru.net/apiManage/docs` 登录后自建 Token（`MINERU_TOKEN`）。

```bash
curl -X POST -H "Authorization: Bearer $MINERU_TOKEN" -H 'Content-Type: application/json' \
  -d '{"url":"https://.../a.pdf","model_version":"vlm"}' 'https://mineru.net/api/v4/extract/task'
# 轮询 /api/v4/extract/task/{id}，done 后从 full_zip_url 下 zip（含 full.md + JSON，可导出 docx/html/latex）
```

额度：**每账号每天 1000 页最高优先级**（超出降优先级）；单文件 ≤200 MB / ≤200 页；批量 ≤200 个。

### C. 本地 CLI（离线免费）

```bash
uv pip install -U "mineru>=4.0,<5"        # requires-python >=3.10,<3.15
mineru parse "paper.pdf"                  # 默认档；--tier flash 最快最低质；--pages 1-10
mineru server start && mineru server status --json
mineru config set parse_server.local.managed_tier standard && mineru config set parse_server.local.mode managed
mineru-kit models download --tier standard && mineru-kit models verify --tier standard
```

档位 `flash`（极速/最差，仅预览索引）/`basic`/`standard`（默认）/`advanced`（最慢最好）；Office/HTML/EPUB/OFD/CSV 只在本地 `flash` 解析；`.txt/.md` 不解析。**Apple Silicon 推荐 `standard`（`torch` extra）**。远程解析（`--remote`）需 `MINERU_API_KEY` 且**必须用户显式同意**（会传文件），本地失败**不会**静默转远程。

### 实测记录（2026-10-03）

macOS 27（arm64），curl 8.x。

① `POST /api/v1/agent/parse/url`（空 body）→ `400 invalid_request: field "url" is not set`；`{"url":"https://example.com/nonexistent.pdf"}` → `{"code":-60023,"msg":"this URL is restricted by regional regulations and cannot be accessed"}` → **端点存在且免 token**。
② 完整签名上传跑通：POST → `code:0` + `task_id` + `file_url`（mineru.oss-cn-shanghai）；PUT 带默认 Content-Type → **403**，改 `--upload-file` + `-H 'Content-Type:'` → **200**；轮询 → `state: done` + `markdown_url`；**该 md 三次均 0 字节**。
③ `https://mineru.net/apiManage/docs` → 200，抓到两种 API 对比表与全部参数/限额/错误码。

未本机实测：本地 CLI、带 Token 的精准 API。

## 坑

1. Agent API 的 PUT **必须去掉 Content-Type**：`curl -X PUT --data-binary` 带 `application/x-www-form-urlencoded` → 签名不匹配 **403**（实测）。
2. `/api/v1/agent/parse/file` body 必须是 **JSON**（`file_name` 必填），**不支持 multipart**（实测报 `field "file_name" is not set`）。
3. 实测三次（PNG×2、PDF×1）任务都 `state=done`，但 `markdown_url` 拉回是 **200 / Content-Length: 0（空）** —— 免 token 通道协议通、**输出为空**，生产前必须复核，或改走带 Token 的精准 API。
4. **AGPL-3.0**：本地部署代码有传染性；只调云 API 不受影响。额度/计费以 mineru.net 为准。
5. `flash` 不是默认档、也别当最终阅读质量（官方原话）；改配置/重启服务前先 `mineru server stop`。
