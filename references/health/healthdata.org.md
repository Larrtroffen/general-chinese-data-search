# healthdata.org —— IHME / 全球疾病负担 GBD

- 去哪找：IHME 门户 `https://www.healthdata.org/`；GBD 数据入口 `https://www.healthdata.org/research-analysis/gbd-data`；GHDx 数据目录 `https://ghdx.healthdata.org/`；GBD 2021 记录页 `https://ghdx.healthdata.org/gbd-2021`；GBD Results 可视化/取数 `https://vizhub.healthdata.org/gbd-results/`；下载说明 `https://www.healthdata.org/downloading-results`。
- 什么时候用：要**全球疾病负担（GBD）**估计（死亡/发病/YLL/YLD/DALY，按国家 × 年龄 × 性别 × 病因/风险）；要中国及分省 GBD 结果；要可比的风险因素与伤害负担；要 GBD 编码本（病因/风险层级）。
- 怎么搜：GBD Results 是**交互式前端**，其数据接口走 Azure AD 鉴权（`https://ihmecsu.onmicrosoft.com/data-api/data.read`，登录 `login.healthdata.org`），**无公开匿名 API**；程序化只用得到公开静态文件（编码本等），完整结果集在 GHDx 记录页按「Files」下载：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # 公开可直接下载：GBD 2021 编码本
  curl -sL -A "$UA" -o IHME_GBD_2021_CODEBOOK.zip \
    'https://ghdx.healthdata.org/sites/default/files/ihme_query_tool/IHME_GBD_2021_CODEBOOK.zip'
  ```
  结果形态：GHDx 记录页（HTML）+ 附件 zip/csv；GBD Results 页（SPA）。
- 覆盖：GBD 2021（1990–2021），204 个国家/地区，分年龄 × 性别 × 病因/风险；含中国与分省结果；历年修订版（GBD 2019/2021…）。
- 门槛：浏览免费；**结果数据下载需注册/登录并同意 IHME 使用条款**（非商业免费）；无开放取数 API。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA）：`https://www.healthdata.org/` 200（154,224 B）；`https://ghdx.healthdata.org/` 200（`<title>Global Health Data Exchange | GHDx`）；`https://ghdx.healthdata.org/record/ihme-data/gbd-2021-cause-specific-mortality-1990-2021` 200（`<title>Global Burden of Disease Study 2021 (GBD 2021) Cause-Specific Mortality 1990-2021 | GHDx`）；GBD 2021 codebook zip 200（127,869 B，`application/zip`）；`https://vizhub.healthdata.org/gbd-results/` 200（`<title>VizHub - GBD Results`）；其主 bundle 含 `ihmecsu.onmicrosoft.com/data-api/data.read` 与 `login.healthdata.org`（B2C）、`myrequests.healthdata.org/request/`。
- 上游：Institute for Health Metrics and Evaluation（IHME）/ GHDx。

## 细节

### 取数路径

| 目的 | 入口 | 形态 |
|---|---|---|
| 结果浏览/下载 | `https://vizhub.healthdata.org/gbd-results/` | SPA（需登录取数） |
| 数据记录与附件 | `https://ghdx.healthdata.org/gbd-2021` | HTML + zip/csv |
| 编码本（公开直下） | `https://ghdx.healthdata.org/sites/default/files/ihme_query_tool/IHME_GBD_2021_CODEBOOK.zip` | zip |
| 数据来源工具 | `https://sources.healthdata.org/` | 工具（登录） |
| 下载与许可说明 | `https://www.healthdata.org/downloading-results` | HTML |
| 非商业使用协议 | `https://www.healthdata.org/about/ihme-free-charge-non-commercial-user-agreement` | HTML |

- GBD Results 前端使用的鉴权：Azure AD B2C（`login.healthdata.org`）+ scope `…/data-api/data.read`；批处理下载另走 `myrequests.healthdata.org` 申请。
- 中国分省（subnational）结果单独发布，需在 GHDx 找对应「GBD China」记录。

## 坑

1. **没有开放 API**：想脚本化取 GBD 数值得先过 IHME 登录 + 条款（实测前端即调鉴权 API）；别指望匿名 JSON。
2. 下载需同意**非商业使用协议**；商用需另行授权。
3. 不同 GBD 修订版（2019/2021/2023）数值不可混用，引用必须写明版本与年份区间。
4. GHDx 记录页的附件链接**未必在 HTML 里**（部分按「Files」标签动态展开），直接 curl 记录页可能拿不到文件名。

## 相关

- 与 `who-gho.md`（WHO GHO 开放 API）互补：要免 key 的全球指标先走 WHO，要 GBD 口径的 DALY/病因负担再回 IHME。
