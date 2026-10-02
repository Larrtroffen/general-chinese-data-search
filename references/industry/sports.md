# sports —— 体育产业与场地统计

- 去哪找：
  - **国家体育总局**「公开 > 体育数据」`https://www.sport.gov.cn/n315/n329/index.html`；**体育经济司**（`jjs`）栏目：体育统计 `https://www.sport.gov.cn/jjs/n5043/index.html`、体育产业 `https://www.sport.gov.cn/jjs/n5039/index.html`——全国体育场地统计调查数据（2018–2025）、全国体育产业总规模与增加值数据公告、国民体质监测公报等
  - **国家统计局「最新发布」** `https://www.stats.gov.cn/xxgk/sjfb/zxfb2020/`——全国体育产业总规模与增加值数据公告由**体育总局 + 国家统计局联合发布**，规范正文在此（如 2024 年公告 `…/202512/t20251231_1962228.html`）
  - **中国体育用品业联合会** `https://www.csgf.org.cn/`——《中国体育用品业年度发展报告》
  - **单项协会数据平台**：中国篮球协会大数据平台 `https://bd.cba.net.cn/`（需登录）、技战术服务平台 `https://k8.cbastats.com/`（SPA）；中国田径协会官网 `https://www.athletics.org.cn/` → 成绩查询 `https://athletics.fairplaycloud.com/`（第三方 SPA）
- 什么时候用：要**体育产业总规模/增加值及其占 GDP 比重**；要**体育场地**数量/面积/人均面积、分机构类型与分运动项目场地数；要国民体质监测、群众体育/全民健身场地等官方数字；或要单项协会的成绩/技战术/注册类数据。
- 怎么搜：总局两套入口（公开>体育数据、体育经济司）都是「栏目列表 → 详情页（`c{id}/content.html`）」静态结构，改 ID 直取；**统计正文多为 JPG 海报图片**，附件在 `part/` 下：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # 体育经济司·体育统计 列表（历年场地数据）
  curl -sS -A "$UA" 'https://www.sport.gov.cn/jjs/n5043/index.html'
  # 2025 全国体育场地统计调查数据（正文为图片）
  curl -sS -A "$UA" 'https://www.sport.gov.cn/n315/n329/c29462896/content.html'
  # 年度体育产业总规模与增加值（规范文字版在统计局）
  curl -sS -A "$UA" 'https://www.stats.gov.cn/xxgk/sjfb/zxfb2020/202512/t20251231_1962228.html'
  ```
  结果形态：**HTML 正文（常内嵌 JPG 海报，`part/{id}.jpg`）+ 部分年份 PDF（`part/{id}.pdf`）**；协会数据平台为 **SPA 或需登录**。
- 覆盖：全国体育场地统计调查数据 2018–2025（年度，附件 PDF/JPG）；全国体育产业总规模与增加值数据公告约 2018 年起（近年 2023/2024 在统计局与总局同步）；国民体质监测公报（第五次等）；体育用品业年度发展报告（联合会，逐年）；篮协/田径等协会成绩与技战术数据（各自平台）。
- 门槛：体育总局、国家统计局、体育用品业联合会 **免费、免登录**；篮协大数据平台需登录、k8 技战术平台与田径 fairplaycloud 为 **SPA/第三方平台**。
- 实测：2026-10-03，macOS arm64，curl 8.x，桌面 UA，20 s 超时，同主机 ≥1.5 s 间隔：
  - `https://www.sport.gov.cn/n315/n329/index.html` → 200 / 18153 B（「体育数据」栏目）；`https://www.sport.gov.cn/jjs/index.html` → 200 / 60979 B（体育经济司，含 `n5039` 体育产业、`n5043` 体育统计）
  - `…/jjs/n5043/index.html` → 200 / 36856 B，列表含 2018–2025 全国体育场地统计调查数据；`…/jjs/n5039/index.html` → 200 / 38135 B，含《2024年全国体育产业总规模与增加值数据公告》✅
  - `…/n315/n329/c29462896/content.html` → 200 / 12338 B（2025 场地数据），正文图片 `…/n315/n329/c29462896/part/29462992.jpg` → 200 `image/jpeg` 1.15 MB ✅
  - `…/jjs/n5039/c29331451/part/29331561.jpg`（2024 体育产业公告图）→ 200 `image/jpeg` 22 KB；`…/jjs/n5043/c24251191/part/24251201.pdf`（2021 场地数据）→ 200 `application/pdf` 165 KB ✅
  - 旧文章详情页 `…/jjs/n5043/c24251191/content.html`、`…/n5043/c941611/content.html` → **403 Forbidden**（换 `n315/n329` 路径、加 Referer 均 403）⚠️
  - `https://www.stats.gov.cn/xxgk/sjfb/zxfb2020/202512/t20251231_1962228.html` → 200 / 47492 B（2024 全国体育产业总规模与增加值数据公告）✅；`https://www.csgf.org.cn/` → 200 / 68009 B ✅
  - `https://bd.cba.net.cn/` → 200（标题「登录」）；`https://k8.cbastats.com/` → 200（SPA）；`https://www.athletics.org.cn/` → 200，成绩查询指向 `https://athletics.fairplaycloud.com/`（SPA）⚠️
- 上游：国家体育总局 `sport.gov.cn`；国家统计局 `stats.gov.cn`；中国体育用品业联合会 `csgf.org.cn`；中国篮球协会 `cba.net.cn` / `cbastats.com`；中国田径协会 `athletics.org.cn`。

## 细节

### 一、源与入口（官方口径为主）

| 源 | 入口 | 口径 · 形态 |
|---|---|---|
| 体育总局 · 公开>体育数据 | `https://www.sport.gov.cn/n315/n329/index.html` | 场地数据、体质监测公报等入口；**HTML 列表** |
| 体育总局 · 体育经济司 体育统计 | `https://www.sport.gov.cn/jjs/n5043/index.html` | 全国体育场地统计调查数据（2018–2025）；**列表 + JPG/PDF** |
| 体育总局 · 体育经济司 体育产业 | `https://www.sport.gov.cn/jjs/n5039/index.html` | 全国体育产业总规模与增加值数据公告；**正文 JPG** |
| 国家统计局 · 最新发布 | `https://www.stats.gov.cn/xxgk/sjfb/zxfb2020/` | 体育产业总规模与增加值（联合发布，规范文字版）；**HTML** |
| 中国体育用品业联合会 | `https://www.csgf.org.cn/` | 体育用品业年度发展报告；**HTML/SPA** |
| 中国篮球协会 | `https://bd.cba.net.cn/`（大数据，登录）、`https://k8.cbastats.com/`（技战术，SPA） | 注册/赛事/技战术数据；**需登录/SPA** |
| 中国田径协会 | `https://www.athletics.org.cn/` → `https://athletics.fairplaycloud.com/` | 成绩查询（第三方平台）；**SPA** |

### 二、可直接拼的 URL 规律

- 总局详情页：`https://www.sport.gov.cn/n315/n329/c{id}/content.html`（公开>体育数据）与 `https://www.sport.gov.cn/jjs/n5043/c{id}/content.html`（体育经济司）——**同一文章 ID 两处路径可达**
- 附件：正文图片 `…/c{id}/part/{附件id}.jpg`；PDF `…/c{id}/part/{附件id}.pdf`（须从详情页解析，`附件id` 不可猜）
- 国家统计局：`https://www.stats.gov.cn/xxgk/sjfb/zxfb2020/{YYYYMM}/t{YYYYMMDD}_{id}.html`
- 体育统计调查制度：《全国体育场地统计调查制度》（国统字〔2020〕41 号），以每年 12 月 31 日为标准时点。

## 坑

1. **统计正文常是 JPG 海报**：近年「全国体育场地统计调查数据」「全国体育产业总规模与增加值数据公告」详情页正文是整张图片（`part/{id}.jpg`），无 HTML 表格；引用数字需 OCR，或改从统计局文字版/新闻稿取。**早期年份（如 2021 场地）反而是 PDF**（`…/c24251191/part/24251201.pdf`），逐篇形态不一。
2. **体育产业总规模与增加值以统计局文字版为准**：公告由体育总局与国家统计局联合发布，总局 `jjs/n5039` 是图片版，`stats.gov.cn`「最新发布」有可复制的文字正文——写论文引数字优先用后者。
3. **旧文章详情页会被 WAF 403**：本机对 `c24251191`（2021）、`c941611`（2018）等较旧 `content.html` 直接返回 `403 Forbidden`（换公开路径、加 Referer 均拦），但**同源的 `part/*.pdf`、`part/*.jpg` 附件与较新文章（如 2025 `c29462896`）正常**；取旧数据从列表页解析附件直链，或走浏览器。
4. **两个入口同源**：`n315/n329/c{id}/`（公开>体育数据）与 `jjs/n5043/c{id}/`（体育经济司）指向同一文章，别当两份数据重复计数。
5. **协会数据不统一、多要登录或为 SPA**：篮协大数据平台需登录，k8 技战术平台、田径 `fairplaycloud` 成绩查询均为 SPA，无稳定开放接口；协会官网通常只给入口链接。
6. **口径随调查制度调整**：全国体育场地统计调查制度（国统字〔2020〕41 号）历年口径可能微调，跨年比较需看公报附注。
7. 「体育数据」栏目也混入体质监测公报、体彩管理等非统计条目，按标题筛选，勿把政策/通知当数据。
