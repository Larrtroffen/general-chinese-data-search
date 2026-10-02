# GLM-OCR —— 中文表格/公式/手写 OCR

`zai-org/GLM-OCR`（Apache-2.0）是智谱的 0.9B 文档理解模型：OmniDocBench V1.5 得分 94.62（官方称第一），强项是**复杂表格、公式（LaTeX）、印章、代码混排、手写**。两路用法：**云 MaaS（要 key，最省事）** 或 **本地 vLLM/SGLang/Ollama（要 GPU/Apple Silicon）**。**扫描件先试 `macos-vision-ocr.md`**，只有版式结构/公式/表格要求高时才来这里。

- 去哪找：仓库（含 SDK / 部署脚本 / Agent 技能）https://github.com/zai-org/GLM-OCR ；Agent 技能说明书 `skills/glmocr/SKILL.md`（raw：`https://raw.githubusercontent.com/zai-org/GLM-OCR/main/skills/glmocr/SKILL.md`）；云 API 文档 https://docs.z.ai/guides/vlm/glm-ocr · https://docs.bigmodel.cn/cn/guide/models/vlm/glm-ocr ；取 API key https://www.bigmodel.cn/usercenter/proj-mgmt/apikeys ；权重 https://huggingface.co/zai-org/GLM-OCR（本机不通）· https://modelscope.cn/models/ZhipuAI/GLM-OCR （**本机可达**）
- 什么时候用：macOS Vision 搞不定的——**表格要还原成 Markdown、公式要 LaTeX、印章/竖排/复杂版式**；需要**批量、高质量中文** OCR 且能接受上传到智谱云（有 key）或本地跑模型；民国报刊、统计年鉴表格、公报扫描页这类「结构比纯文本更值钱」的档
- 怎么用：见下两路（A 云 API / B 本地自托管）
- 覆盖：**输入** 图片（PNG/JPG…）、PDF、URL；**输出** Markdown + 布局 JSON（`layout_details`）；许可：模型/代码 Apache-2.0、云 API 按智谱计价
- 门槛：云路需 `ZHIPU_API_KEY`（实名 + key，数据出境，敏感公文注意）；本地路需 GPU 显存 / Apple Silicon + 数 GB 权重；`glmocr` 要 **Python ≥3.10**（本机系统 python3 是 3.9，需另建 3.12 环境）
- 实测：2026-10-02，macOS 27（arm64）——可达性 `huggingface.co` 000 / `hf-mirror.com` 200 / `modelscope.cn` 200 / pypi `glmocr` 0.1.5 `requires-python >=3.10`；**未安装 SDK、未配置 key → OCR 功能未本机实测**
- 上游：https://github.com/zai-org/GLM-OCR

## 细节

### A. 云 API（推荐起步，需 `ZHIPU_API_KEY`）

```bash
pip install glmocr                       # PyPI glmocr 0.1.5，requires-python >=3.10（本机 python3.9 不够用）
# 或只抄它的 CLI：skills/glmocr/scripts/glm_ocr_cli.py
python glm_ocr_cli.py --file 扫描页.jpg --output out.json --pretty
python glm_ocr_cli.py --file-url "https://<文件直链>/a.pdf" --output out.json
# 返回 JSON：{ok, text(Markdown), layout_details, error, source}
```

SDK 另一条路：`config.yaml` 里 `pipeline.maas.enabled: true` + `api_key: ...`，SDK 当薄封装转发给智谱云（文档输入支持 URL 或 `data:<mime>;base64,...`）。

### B. 本地自托管（无 key，要硬件）

```bash
pip install "glmocr[selfhosted]"
pip install -U "vllm>=0.19.0" && vllm serve zai-org/GLM-OCR --port 8080 \
  --speculative-config '{"method":"mtp","num_speculative_tokens":3}' --served-model-name glm-ocr
# 或 SGLang：SGLANG_ENABLE_SPEC_V2=1 sglang serve --model-path zai-org/GLM-OCR --port 8080 ...
# 或 Ollama / MLX（README Option 3）
```

权重下载走 ModelScope（`modelscope download --model ZhipuAI/GLM-OCR`）—— **本机 huggingface.co 不通**。

### 实测记录（2026-10-02）

macOS 27（arm64）。可达性：`https://huggingface.co` → HTTP 000（15 s 超时，**不通**）；`https://hf-mirror.com/` → 200；`https://www.modelscope.cn/models/ZhipuAI/GLM-OCR` → 200；`https://pypi.org/pypi/glmocr/json` → 0.1.5 / requires-python `>=3.10`。**未安装 SDK、未配置 key → OCR 功能未本机实测**（上游声明）。

## 坑

- 云路 = 数据出境（敏感公文注意）；本地路 = 需 GPU 显存 / Apple Silicon + 数 GB 权重。
- 官方 SKILL 自带强约束（「只用本 API、失败即停、不做 fallback」）—— 我们收编时**不照搬**，只取用法。
