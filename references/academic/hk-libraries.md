# hk-libraries —— 香港公共图书馆数码馆藏与政府档案

- 去哪找：
  - 香港公共图书馆「數碼館藏」（原 MMIS）：`https://sls.hkpl.gov.hk/digital-collection/tc/index.html`
  - 香港記憶（HKM）：`https://www.hkmemory.hk/tc/index.html`
  - 香港政府檔案處检索：`https://search.grs.gov.hk/en/index.xhtml`（入口 `https://www.grs.gov.hk/`）
- 什么时候用：找**香港本地的一手材料**——旧报纸（香港工商日報、華僑日報、大公報…）、政府档案（HKRS 系列、Carl Smith Collection）、老照片/海报/地图、口述史；做港澳史、省港关系、英殖时期研究时。
- 怎么搜：
  - **數碼館藏**：结果页 = 一个 URL 编码的 JSON 参数——`https://sls.hkpl.gov.hk/digital-collection/tc/searchresults.html?param=<URL编码 {"filterList":[{"keyword":["<词>"]}]}>`；另有可直接调用 JSON 的建议词接口（见 `## 细节`）。
  - **GRS**：`https://search.grs.gov.hk/en/search.xhtml?q=<词>`，curl 直取 HTML 结果。
- 覆盖：數碼館藏含香港舊報紙、政府刊物、照片、海报、地图、录音/录影、兒童樂園特藏等（实测命中：香港工商日報 1963、華僑日報 1975–1989、大公報 1991）；GRS 为政府档案与图书馆藏书（含 Carl Smith Collection），GRS 实测 `Kowloon` → Archives 34,688 / Library Holdings 2,052 / Carl Smith Collection 1,939 条。
- 门槛：免费、免登录（两个源均无付费墙）；數碼館藏**有 Queue-it 虚拟等候室**（`lcsdsls.queue-it.net`）需浏览器过闸；GRS 是 JSF（`.xhtml`）页面但 URL 参数可直取。
- 实测：2026-10-03：`curl 'https://search.grs.gov.hk/en/search.xhtml?q=Kowloon'` → **200 / 66,883 B**（含 Archives/Library/Carl Smith 分组计数）；`curl 'https://sls.hkpl.gov.hk/api/drmapi/client-api/mmissearch/getSuggest?keyword=香港'` → **200 JSON**；`mmis.hkpl.gov.hk` → 301 → `sls.hkpl.gov.hk`，经 Queue-it 后浏览器 ✅ 200（标题《數碼館藏》）。
- 上游：<https://www.hkpl.gov.hk/>、<https://www.grs.gov.hk/>、<https://www.hkmemory.hk/>

## 细节

### 1. 香港公共图书馆「數碼館藏」（sls.hkpl.gov.hk）

| 用途 | URL / 端点 | 形态 |
|---|---|---|
| 首页 | `https://sls.hkpl.gov.hk/digital-collection/tc/index.html` | ✅ 浏览器 200（Vue 3 SPA） |
| **检索结果** | `…/digital-collection/tc/searchresults.html?param=<URL编码 JSON>`，JSON = `{"filterList":[{"keyword":["<词>"]}]}` | ✅ 200，标题《檢索結果 \| 香港公共圖書館》 |
| 舊報紙专集 | `…/digital-collection/tc/collection_old-hk-newspapers.html` | ✅ 链接存在于首页 |
| 建议词 API | `GET /api/drmapi/client-api/mmissearch/getSuggest?keyword=<词>` | ✅ curl 200 JSON（`{"code":200,…,"data":[{"type":1,"keyword":"香港"},…]}`） |
| 检索/分面 API 前缀 | `/api/drmapi/client-api/mmis/search/advanceBoxOptions`、`/mmis/browseCollection/dropDownBoxLists`、`/common/contentRecommendation/{gupItems,mostPopular}` | 结果页实际发出的请求（未逐条记状态码；同级 `mmissearch/*` 才是检索族） |
| 用户态 | `/ecmapi/currentuser`；`/tcapi/api/drmapi/fileLocal/file/mmis/img/...` | ✅ 200 |

- 旧域 `mmis.hkpl.gov.hk` → 301 → `sls.hkpl.gov.hk`。
- `param` 里的 `filterList[].keyword` 是**关键词数组**（首页「數碼館藏推介」链接里还带 `searchOptionId`），可按同样结构手拼 URL。
- 反爬：进站先过 **Queue-it 排队页**（`lcsdsls.queue-it.net`，带 `queueittoken`），随后 URL 才可正常访问；JS 渲染（axios），**curl 首页只能拿到排队/框架 HTML**。

### 2. 香港政府檔案處（政府檔案處網上檢索）

| 用途 | URL | 形态 |
|---|---|---|
| 入口 | `https://www.grs.gov.hk/` → meta refresh → `/en/index.html` | ✅ 200 |
| **检索** | `https://search.grs.gov.hk/en/search.xhtml?q=<词>` | ✅ curl 200 / 66,883 B，HTML |
| 检索首页 | `https://search.grs.gov.hk/en/index.xhtml` | ✅ 200；表单 `action="search.xhtml" method="GET"`，输入框 `name="q"`（另有 `e_k`＝精确匹配复选框） |
| 網上目錄（另一系统） | `https://www.grs.gov.hk/ws/online/80VWR/en/home/index.html` | 首页链接，未本机实测 |

- 结果分组：`Archives` / `Library Holdings` / `Carl Smith Collection`，可按 `Group by Series` 归并。
- 技术栈 JSF（PrimeFaces 风格，`.xhtml` + `javax.faces.ViewState`），但 **GET 查询串 `?q=` 可直接构造**，无需会话。

### 3. 香港記憶（hkmemory.hk）

- `https://www.hkmemory.hk/tc/index.html` → ✅ 200 / 199,429 B，标题《香港記憶 | Hong Kong Memory》。
- 港府「香港記憶」计划，专题式数字馆藏；繁中入口 `/tc/`（英文路径未实测）。检索入口与内容分类未本机细探。

## 坑

1. **Queue-it 排队页**是 `sls.hkpl.gov.hk` 的硬门槛：脚本直连拿不到内容页，需真实浏览器（或至少带 `queueittoken` 的会话）。批量抓取前先确认这一点。
2. 舊報紙等图像的**版权/使用条款**按馆藏分档，商用需申请；以站内使用条款为准。
3. GRS 结果是**档案系列/目录级**（如 `HKRS819` 缩微胶卷），**不是全文库**；Carl Smith Collection 同为缩微胶卷目录。
4. 两站界面为繁中/英双语；GRS 检索语言可切（页面 `chglang(1)/(2)`），繁中路径推测为 `/tc/`（未实测）。
