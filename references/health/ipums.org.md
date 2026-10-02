# ipums.org —— IPUMS 国际微观人口数据

- 去哪找：国际项目 `https://international.ipums.org/international/`；变量检索 `https://international.ipums.org/international-action/variables/search`；样本清单 `https://international.ipums.org/international-action/sample_details`；**开发者文档** `https://developer.ipums.org/`。
- 什么时候用：要**跨国人口普查/住户调查的微观数据**（个体/住户级，可自行交叉制表）；要中国普查样本（1982/1990/2000 等）做人口学、劳动、家庭、迁移研究；要**已跨国调和的变量**（harmonized）。
- 怎么搜：网站按 sample（国家×年份）与 variable 浏览检索；程序化取数走 **IPUMS API（需 key）**——
  ```
  POST https://api.ipums.org/extracts        # JSON 定义样本/变量
  Header: Authorization: <你的 API key>
  ```
  亦可用官方客户端 `ipumsr`(R) / `ipumspy`(Python)。返回：定义提取单 → 轮询状态 → 下载 zip（固定宽/CSV + DDI 元数据）。
- 覆盖：100+ 国家的人口普查与调查微数据；中国样本实测含 **China 1982 / 1990 / 2000**；变量经 harmonized 处理便于跨国比较。
- 门槛：**免费注册**；下载微数据需登录并接受使用条款；API 需账号生成 key。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA）：`https://international.ipums.org/` 302 → `/international/` 200（13,024 B，`<title>IPUMS International`）；`/international-action/variables/search` 200（11,380 B，`<title>IPUMS-I: var search`）；`/international-action/sample_details` 200（256,674 B，页面含 `China 1982 / China 1990 / China 2000`）；`https://api.ipums.org/` 404（`text/plain`，根路径无路由，API 走具体端点）。
- 上游：IPUMS，University of Minnesota（`https://developer.ipums.org/`）。

## 细节

### 取数方式

| 方式 | 入口 | 门槛 |
|---|---|---|
| 网页浏览变量/样本 | `international.ipums.org/international-action/…` | 免登录可浏览 |
| 网页勾选生成提取单 | IPUMS 账号内 | 注册 + 同意条款 |
| REST API | `https://api.ipums.org/extracts`（JSON + `Authorization`） | 账号生成 API key |
| 客户端 | `ipumsr`(R) / `ipumspy`(Python) | 同上 |

- 中国样本：1982、1990、2000（另有 2005 等，实测页面列出前三个）；样本年份/规模详见 `sample_details`。
- 变量检索支持按关键词/变量组查（`variables/search`）。

## 坑

1. **微数据不是匿名直下**：API 与下载都要账号 + key；别把 `api.ipums.org` 根路径当健康检查（恒 404）。
2. 提取单是**异步**的：提交后需轮询状态再取 zip。
3. 跨国比较必须用 harmonized 变量；原始变量跨年份口径不一致。
4. 站点已迁移过域名（旧 `international.ipums.org/international/` 仍在用），文档以 `developer.ipums.org` 为准（API 细节为上游声明，未本机跑通提取）。

## 相关

- 中国本土调查（CHNS 等）见 `chns.md` 与 `../surveys/`；普查汇总口径见 `stats.gov.cn-census.md`。
