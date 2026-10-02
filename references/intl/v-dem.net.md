# v-dem.net —— V-Dem 民主多样性数据库

- 去哪找：数据集页 `https://v-dem.net/data/the-v-dem-dataset/`；**国-年主表** `https://v-dem.net/data/the-v-dem-dataset/country-year-v-dem-fullothers-v16/`；历史版本 `/data/dataset-archive/`；绘图 `/graphing/`。
- 什么时候用：政治学跨国面板的**核心自变量库**——选举民主/自由民主/参与民主/协商民主、公民自由、行政约束、腐败、学术自由；要长时段、带专家编码不确定性的制度指数；与 Polity5/Freedom House 交叉验证。
- 怎么取：官网是**表单门控下载**（免费，留邮箱 + 同意条款即可），无常开 REST API：
  - 进 v16 Country-Year "Full+Others" 页 → 填 `email` → 勾 `accept_terms` → 选格式（`dataset_file` 单选：STATA / CSV / R / SPSS）→ 提交后自动下载；直链由表单签名，无常量 URL。
  - 编码手册与方法论：`https://v-dem.net/documents/70/codebook_v16.pdf`、`/documents/71/methodology_v16.pdf`。
  - 程序化替代：R 包 `vdemdata`；或经 QoG（`vdem_*` 列）/ OWID 转引。
- 覆盖：1789–2024，~200 个国家/政体，v16 含 500+ 指标；三档粒度——国-年 / 国-日 / 编码者级（coder-level）；年度更新（上游声明，未本机实测）。
- 门槛：免费；**需填邮箱表单**（国-年表无需账号）；"Coder-level" 数据需登录 `/accounts/login/`。
- 实测：2026-10-03，macOS arm64，curl 8.x：`/data/the-v-dem-dataset/` → 200 / 42 KB；`/country-year-v-dem-fullothers-v16/` → 200 / 31 KB，页面含 `id="dataset-download"` 表单（字段 `csrfmiddlewaretoken`、`email`、`gender`、`newsletter`、`accept_terms`、`website`、`dataset_file`，单选值 `224`=STATA / `225`=CSV / `226`=R / `227`=SPSS）；`/data/dataset-archive/`、codebook PDF 链接均在页内。
- 上游：`https://v-dem.net/`（V-Dem Institute, University of Gothenburg）。

## 坑

1. **没有直接 REST API**：别指望 curl 一条 URL 拿 CSV；要么浏览器走表单，要么用 R `vdemdata` 或转引库。
2. 表单是 Django CSRF——脚本化需先 GET 取 `csrfmiddlewaretoken` 与 cookie，再 POST，并带真实邮箱、勾 `accept_terms`。
3. Coder-level 数据需登录且体量 GB 级；一般研究用国-年表足够。
4. 版本号（v16/v15…）必须与论文引用一致；跨版本变量增删过，别混用。
5. 覆盖区间与指标数以上游页面为准（本机只验证到页面与表单，未下载数据核对）。
