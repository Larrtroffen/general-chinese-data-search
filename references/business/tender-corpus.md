# tender-corpus —— 现成招标公告数据集与语料

不想自己爬时的**招标/政采公告成品数据集与语料仓**总卡：学术付费库、开源微调集、数据交易平台三路。
自建爬取路线见 `procurement.md`；国家级公告检索接口见 `../gov/ccgp-ggzy.md`。

- 去哪找：
  - **CnOpenData**（学术/商业付费库）：政府采购公告数据 `https://www.cnopendata.com/data/m/tender&bid/gov-pro-gg.html`；招投标数据目录 `https://www.cnopendata.com/catalogs/tender%26bid`。
  - **Hugging Face**：`https://huggingface.co/datasets/Qiaowenshu/bid-announcement-zh-v1.0`（国内镜像 `https://hf-mirror.com/datasets/Qiaowenshu/bid-announcement-zh-v1.0`）；同域另有 `ted-z/bid-report`。
  - **知了标讯开放平台**（百炼智能）：`https://www.zhiliaobiaoxun.com/`（提供 MCP / CLI / API 接入）。
  - **数据交易集市**：`https://www.selectdataset.com/`（"6000 万条全国标讯数据集"等挂牌条目）。
- 什么时候用：
  - 要**跨年全量结构化公告面板**（做计量/事件研究）→ CnOpenData（2013 起，含原始文档）。
  - 要**招标文本 NLP 微调集**（指令/问答/信息抽取）→ Hugging Face 开源集。
  - 要**实时+历史标讯的接口化调用**（不想自建爬虫）→ 知了标讯 API/MCP。
  - 要**买现成标讯数据包** → 数据交易集市（先比价与查 license）。
  - 不适用：只要单条公告原文 → 直接去 `procurement.md` / `../gov/ccgp-ggzy.md` 查。
- 怎么取：
  - **CnOpenData**：注册/登录 `https://sso.cnopendata.com/user/login` 后按数据集条目下单或申请（学术多走机构/申请制）；交付形态为结构化表 + 原始公告文档（**上游声明，未本机实测取数流程**）。
  - **Hugging Face**：直连超时，**用镜像 `hf-mirror.com`**：
    ```bash
    curl -sS 'https://hf-mirror.com/api/datasets/Qiaowenshu/bid-announcement-zh-v1.0'   # 元数据 JSON
    curl -sS 'https://hf-mirror.com/datasets/Qiaowenshu/bid-announcement-zh-v1.0/raw/main/README.md'
    # 数据文件 data/train-00000-of-00001.parquet，用 datasets / pandas 读
    ```
  - **知了标讯**：站内注册后用其 API/MCP（一行配置查询），免费额度每日 3 条（**上游声明**）。
- 覆盖：CnOpenData 政府采购公告数据宣称「2013 年以来全国各级政府公开渠道发布的政府采购公告，涵盖招标、中标、合同全流程，基础信息表 1700 万条 + 13 张明细表 + 原始公告文档」；HF `bid-announcement-zh-v1.0` 为 2000 条中文招标公告（Alpaca 格式）；知了标讯宣称 3.1 亿+ 招投标数据、2500 万+ 企业信息。
- 门槛：CnOpenData **付费/申请**（需账号）；HF 数据集**免费开源**（MIT）；知了标讯**注册 + 付费**（每日免费 3 条）；数据集市**付费**。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA）。`GET https://www.cnopendata.com/data/m/tender&bid/gov-pro-gg.html` → **200**，页面 meta description 给出「2013 年以来…1700 万条记录及 13 张详细表…提供原始公告文档」，正文数据项为 JS 异步加载（页面显示"加载中…"）；`GET https://www.cnopendata.com/catalogs/tender%26bid` → 200，目录含「招投标数据」「司法拍卖数据」。Hugging Face **直连 `huggingface.co` 超时（curl 28）**，改用镜像：`GET https://hf-mirror.com/api/datasets/Qiaowenshu/bid-announcement-zh-v1.0` → **200 JSON**（`license=mit`、`lastModified=2024-09-20`、siblings 含 `data/train-00000-of-00001.parquet`）；其 README → 200，`num_examples=2000`、`dataset_size=11 607 613 B`、字段 `instruction/input/output`、`language=zh`；`GET …/ted-z/bid-report`（镜像）→ 200，**仅 4 条**（`dataset_size=27 959 B`，apache-2.0），样本量可忽略。`GET https://www.zhiliaobiaoxun.com/news/infor/2250.html` → 200，页面文案含「3.1 亿+ 招投标数据、2500 万+ 企业信息、MCP/CLI/API、免费每天 3 条」（**上游声明**）。详见 `## 细节`。
- 上游：CnOpenData <https://www.cnopendata.com/>；Hugging Face 镜像 <https://hf-mirror.com/>；知了标讯（百炼智能）<https://www.zhiliaobiaoxun.com/>。

## 细节

### 成品数据集对照

| 源 | 形态 | 覆盖/规模 | 门槛 | 本机验证 |
|---|---|---|---|---|
| CnOpenData 政府采购公告数据 | 结构化表（1 基础表 + 13 明细表）+ 原始公告文档 | 2013 年起，1700 万条 | 注册/付费 | ⚠️ 页面 meta 可读，取数未跑 |
| CnOpenData 招投标数据目录 | 目录页（多数据集） | 招投标/司法拍卖 | 注册/付费 | ✅ 目录 200 |
| HF `Qiaowenshu/bid-announcement-zh-v1.0` | Alpaca 微调集（instruction/input/output），parquet | 2000 条，≈11.6 MB | 免费，MIT | ✅ 元数据 + README |
| HF `ted-z/bid-report` | 同上 | **4 条** | 免费，apache-2.0 | ✅（样本量可忽略） |
| 知了标讯开放平台 | API / MCP / CLI | 宣称 3.1 亿+ 标讯 | 注册 + 付费（日免费 3 条） | ⚠️ 仅站点文案 |
| selectdataset.com 挂牌条目 | 数据包（多卖家） | 宣称 6000 万条全国标讯 | 付费 | ❌ 未访问 |

### 与自建路线的关系

- **学术面板**：CnOpenData 的「政府采购公告数据」把公告拆成 13 张表（招标/中标/合同等），适合直接回归；自建则按 `procurement.md` 的分页 + 时间窗法，成本在于过反爬与清洗。
- **NLP 语料**：HF 那 2000 条 Alpaca 集太小，只能当**微调种子**；要大规模预训练语料仍须自采（千里马/北京 JSON 接口最省事）。
- **实时 + 接口化**：知了标讯这类商业 API 与 `procurement.md` 里中国招标投标公共服务平台的付费 API 是同一档替代品，按价格与字段比选。

## 坑

1. **Hugging Face 直连不通**（本机 `huggingface.co` 超时，`curl (28)`），必须换 `hf-mirror.com`；Hf API 与 raw 文件路径在镜像上一致。
2. **小样本陷阱**：`ted-z/bid-report` 只有 **4 条**（README 自述的 splits 里 `num_examples: 4`），别当成可用语料；Hugging Face 上标 "bid" 的数据集半数样本量极小或为英文 EU 招标（TED），引用前先看 `num_examples` 与 `language`。
3. **付费库数字是"上游声明"**：CnOpenData 的 1700 万条、知了标讯的 3.1 亿条均来自其页面文案，本机未取数核对；采购/引用前**先要样本行 + 字段说明 + 覆盖年份**。
4. **二次分发与 license**：CnOpenData / 知了标讯条款对再分发有限制；HF 集要看具体 `license`（两者为 MIT / apache-2.0，可再用，但数据本身源自公告，仍受源头条款与个人信息约束）。
5. **口径混淆**：数据集的"招标公告"可能只含**政府采购**（CnOpenData 该集口径）或含工程/央企；跨源合并前先对齐行业与公告类型字典（参照 `../gov/ccgp-ggzy.md` 的 `informationTypeText`/`businessTypeText`）。
