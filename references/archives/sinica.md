# sinica —— 中研院档案与人物库

台湾中央研究院人文组的档案与人物数据库群。对近代中国人物/档案检索的价值：**史語所人名權威檔（48,593 筆）消歧人名 + 近史所檔案館館藏檢索（5.9 萬筆级命中）定位档案 + 史語所檔案館站内检索 + 漢籍全文（史部）取人物传记原文**。绝大多数**免登录、免付费**，但从大陆直连**慢**（单页 1.5–13 s），且 curl 直连对 JS/TTSearch 型界面无效 → **这部分要浏览器**。

> ⚠️ **域名更正（本卡实测）**：任务书里把 `archives.ihp.sinica.edu.tw` 记作"近代史研究所檔案館"是**错的** —— 该域名页面标题是《中央研究院**歷史語言研究所**檔案館》（史語所行政檔案）。**近史所檔案館**的入口是 `https://archives.sinica.edu.tw/`，馆藏检索系统是 `https://archivesonline.mh.sinica.edu.tw/`。旧的 `archives.mh.sinica.edu.tw` **已无 A 记录**（`dig` = NOERROR/NODATA，无 answer），不可用。

- 去哪找：
  - **史語所檔案館**：`https://archives.ihp.sinica.edu.tw/`（`/archives` 館藏檔案）；检索 `GET /search?query=<词>`
  - **近史所檔案館入口網**：`https://archives.sinica.edu.tw/`
  - **近史所檔案館館藏檢索系統**：`https://archivesonline.mh.sinica.edu.tw/`（`GET /search/?query_term=&query_field=&query_op=and&match_type=phrase&page=&page_size=`）；人名索引 `/byname/init/init/`
  - **人名權威-人物傳記資料庫**：`https://newarchive.ihp.sinica.edu.tw/sncaccgi/sncacFtp`（同系另有**清代職官資料庫** `…/officerc/officertp`，链接来自「相關檢索資源」页，**未实测**）
  - **漢籍全文資料庫**（免費版）：`https://hanchi.ihp.sinica.edu.tw/ihpc/ttswebquery?@hanjiquery`；授权入口 `/ihpc/ttsweb?@hanji`
  - 明清檔案工作室（內閣大庫）：`https://newarchive.ihp.sinica.edu.tw/`、`/mcttp/`
  - 傅圖整編史語所檔案目錄：`https://fsntts.ihp.sinica.edu.tw/ttscgi/ttsweb?@0:0:1:fsn@@…`
  - 近史所加值资料库：`https://archwebs.mh.sinica.edu.tw/`（`/salary_db/`、`/agr_statistics/`、`/network/`、`/sourcemap/`、`/MNA/`、`/huai/`）；`https://ktli.sinica.edu.tw/`（李國鼎先生資料庫）
  - 逐库一览（检索方式、实测状态）见「细节」表。
- 什么时候用：
  - **人名消歧 + 人物基本盘**：已知「李鸿章 / 李鴻章 / 少荃」等异名，要生卒（中曆+西曆）、籍貫、旗籍、出身、履歷 → 人名權威檔（与 `cbdb.md` 的 CBDB 互补：**明清→民国初**这条线史語所收得更细）。
  - **近代（民国）档案定位**：要「某人/某机关在某年」的档案件 → 近史所館藏檢索（`query_field=author` 人名 / `date` 日期 / `place` 地名 / `callno.raw` 馆藏号）。
  - **人物传记原文**：二十五史/《清史稿》里的传、志 → 漢籍全文（免费档已含史部，《清史稿》可全文命中）。
  - **史語所自身档案 / 傅斯年、姚從吾等学人文献**：史語所檔案館站内检索（题名/描述级）。
  - **公务员薪俸/物价类量化数据**：近史所加值库（級俸補助費、農情調查）。
- 怎么搜：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36'

  # 1) 史語所檔案館：站内检索（服务端渲染 HTML，curl 可用）
  curl -s -m 20 -A "$UA" 'https://archives.ihp.sinica.edu.tw/search?query=%E5%82%85%E6%96%AF%E5%B9%B4'
  #   → <p class="search-info">查詢詞 : `傅斯年`, 共找到 11 筆相符的結果</p>

  # 2) 近史所檔案館館藏檢索：GET 参数齐全，服务端渲染，curl 可用（结果页 1.3 MB，注意落盘）
  curl -s -m 20 -A "$UA" 'https://archivesonline.mh.sinica.edu.tw/search/?query_term=%E8%83%A1%E9%81%A9&query_field=text&query_op=and&match_type=phrase&page=1&page_size=10'
  #   query_field 取值（实测 <select>）：text(不限欄位) / callno.raw(館藏號) / title(題名)
  #                                    / date(日期) / author(人名) / place(地名) / subject(主題)
  #   query_op=and|or|…, match_type=phrase(精確)|…(模糊), page=N, page_size=10
  #   → 页面显示「總共找到 59352 結果」；首页表单 action=/search/，method=get
  #   人名索引：curl -s -A "$UA" 'https://archivesonline.mh.sinica.edu.tw/byname/init/init/'   # 筆畫分類 + 精確/模糊

  # 3) 人名權威 / 漢籍 / 內閣大庫 / 傅圖目錄：TTSearch 型界面，**curl 无效，必须浏览器**
  #    - 人名權威首页：https://newarchive.ihp.sinica.edu.tw/sncaccgi/sncacFtp
  #    - 漢籍免費入口：https://hanchi.ihp.sinica.edu.tw/ihpc/ttswebquery?@hanjiquery
  ```
- 覆盖：
  - **史語所檔案館**：史語所行政檔案（元/昆/李/京/楊/港 等字號所檔）+ 同仁檔案 + 徵集檔案 + 影音資料；检索落在**题名/摘要级**（站内全文检索，非档案全文）。
  - **近史所檔案館**：全宗五大类 **外交 / 經濟 / 個人文書 / 機關團體 / 地圖**；`/byname/` 人名索引按筆畫组织；命中量上万（`胡適` 59,352 条）。已数字化者**可线上阅览影像**（须先登录，未实测）。
  - **人名權威檔**：48,593 筆，**含 CBDB 与故宮（NPM）汇入**（建檔單位分面：IHP 史語所 / IHP-CBDB / NPM）；字段含 朝代、籍貫、旗籍、出身、異名、中曆/西曆生卒、履歷。
  - **漢籍全文**：免费档可用；实测《清史稿》在库（`李鴻章` 命中 234 章節）。授权档另含更多丛书。
  - 更新：各库长期维护；本次未做"最新收录时间"核查。
- 门槛：
  - **免费、免登录**：史語所檔案館检索、近史所館藏檢索、人名權威、漢籍**免費使用**档。
  - 漢籍另有 **授權使用** 档（机构/IP 或订购）；近史所**档案影像线上阅览需要登录/申请**（页面有 reCAPTCHA 与「登入」入口，检索本身不需要）。
  - 部分 TTSearch 库用**会话 token + 表单往返**，无法用一次性 curl 稳定复现 → 用浏览器。
  - 大陆直连**时延高**（实测首页 1.5–13 s / 请求），批量抓取要限速。
- 实测：2026-10-03，macOS arm64，curl 8.x + 无头 Chromium（`-m 20`，桌面 Chrome UA）。要点：`archives.ihp.sinica.edu.tw` 200 / 22,428 B，`/search?query=傅斯年` → 200 / 28,691 B「共找到 11 筆相符的結果」；`archivesonline.mh.sinica.edu.tw/search/?query_term=胡適&query_field=text…` → 200 / 1,370,463 B「總共找到 59352 結果」，`/byname/init/init/` 200 / 322,173 B；人名權威檔浏览器实测首页显示 48,593 筆、查「李鴻章」177 筆；漢籍免费入口浏览器实测「李鴻章」240 個章節 / 3 本書（《清史稿》234、《續金山志》5、《雲棲志》1）；`archives.sinica.edu.tw` 200 / 182,251 B；`archwebs.mh.sinica.edu.tw/salary_db/` 200、`table.php` 200；`mhdb.mh.sinica.edu.tw` → **403 Cloudflare challenge（本机不可用）**；`www.drnh.gov.tw`（國史館）→ **DNS 可解析但 TCP 超时 000**。完整表见「细节」。请求纪律：单主机 ≤3 次（`newarchive.ihp` 因核实两个入口略超，共 5 次；`hanchi.ihp` 4 次；`archivesonline.mh` 3 次），间隔 ≥1.7 s；未见封禁或验证码拦截（mhdb 是 Cloudflare 主动挑战）。
- 上游：
  - `newarchive.ihp.sinica.edu.tw/reference/1/`（史語所「相關檢索資源」页）—— 人名權威、清代職官、漢籍、內閣大庫、傅圖目錄、臺大淡新檔案、一史馆等入口 URL 均出自此页
  - `archives.ihp.sinica.edu.tw/js/app.js` —— `/search?query=` 路由
  - `archivesonline.mh.sinica.edu.tw/` 首页表单与 `/search/` 结果页 —— `query_field` 枚举、`page/page_size`
  - `archives.sinica.edu.tw/` 导航 —— 近史所加值库（`archwebs.mh`…、`ktli.sinica.edu.tw`）清单
  - `hanchi.ihp.sinica.edu.tw/ihp/hanji.htm` —— 免费/授权两个入口按钮

## 细节

### 逐库一览

| 库 | 入口 URL | 检索方式 | 本机实测（2026-10-03） |
|---|---|---|---|
| **史語所檔案館** | `https://archives.ihp.sinica.edu.tw/`；`/archives`（館藏檔案） | 🔎 **GET `/search?query=<词>`** | ✅ 200 / 22,428 B；搜索「傅斯年」→ 200，`共找到 11 筆相符的結果` |
| **近史所檔案館入口網** | `https://archives.sinica.edu.tw/` | 门户页（含外交史研究、檔案知識、典藏機構等栏目） | ✅ 200 / 182,251 B |
| **近史所檔案館館藏檢索系統** ⭐ | `https://archivesonline.mh.sinica.edu.tw/` | 🔎 **GET `/search/?query_term=&query_field=&query_op=and&match_type=phrase&page=&page_size=`** | ✅ 200；`query_term=胡適` → `總共找到 59352 結果`（1.37 MB 服务端渲染 HTML） |
| ↳ 人名索引 | `https://archivesonline.mh.sinica.edu.tw/byname/init/init/` | 按筆畫分類；精確/模糊檢索 | ✅ 200 / 322 KB |
| ↳ 全宗浏览 / 進階查詢 / 分類瀏覽 | `/byfonds/init/byfonds/`、`/advance/`、`/browse/` | — | 链接来自首页（未逐一实测） |
| **人名權威-人物傳記資料庫** ⭐ | `https://newarchive.ihp.sinica.edu.tw/sncaccgi/sncacFtp`；同系另有 **清代職官資料庫** `…/officerc/officertp`（链接来自「相關檢索資源」页，**未实测**） | 表单 POST（`簡易檢索` / `進階檢索` / `履歷查詢`），**必须浏览器** | ✅ 浏览器实测：首页显示 **目前系統筆數 48,593 筆**；查「李鴻章」→ **177 筆**，带分面（朝代/籍貫/出身/旗籍） |
| **漢籍全文資料庫**（免費版） | 免费入口 `https://hanchi.ihp.sinica.edu.tw/ihpc/ttswebquery?@hanjiquery`；授权入口 `/ihpc/ttsweb?@hanji`（根 `hanchi.ihp.sinica.edu.tw/` → meta refresh 到 `/ihp/hanji.htm` 说明页） | TTSearch 表单 POST；`不限欄位` + 書名/內文/註釋/標題 + 異體字/同義詞 + 成書朝代；另有 文本比對 / 文本分析 | ✅ 浏览器实测：查「李鴻章」→ **240 個章節 / 3 本書**（《清史稿》234、《續金山志》5、《雲棲志》1） |
| 明清檔案工作室（內閣大庫） | `https://newarchive.ihp.sinica.edu.tw/`、`/mcttp/`；免費 `/mcttpc/mctwebtp`、授權 `/mcttpc/mcttpc…` | 免费/授权两档入口 | ✅ 200（入口页可读）；免费库未深入检索 |
| 傅圖整編史語所檔案目錄 | `https://fsntts.ihp.sinica.edu.tw/ttscgi/ttsweb?@0:0:1:fsn@@…` | TTSearch 5.1.1 表单（`不限欄位`/`題名`/`日期`/`摘由`），POST 到表单 ACTION（**token 随会话变化**） | ✅ 入口 200 / 2,927 B；直接猜 token 的 POST **只回空表单** → 需按会话往返或浏览器 |
| 近史所加值资料库 | `https://archwebs.mh.sinica.edu.tw/`（根路径 404）→ `/salary_db/`（級俸補助費，含 `table.php` 下拉：人物/機關/任務/級別 + `book.pdf` 物價參考）、`/agr_statistics/`（近代農情調查）、`/network/`（近代農業技術人才社會網絡）、`/sourcemap/`（農業復員委員會）、`/MNA/`（國防部軍事新聞通訊社檔案）、`/huai/`（導淮委員會）；`https://ktli.sinica.edu.tw/`（李國鼎先生資料庫） | 网页表格 / JS 筛选 | ✅ `/salary_db/` 200 / 10,457 B；`/salary_db/table.php` 200 / 20,213 B（下拉字段实测存在）；**其余未实测** |

**汉籍/人名權威之外的延伸（来自史語所「相關檢索資源」页，未实测，仅供顺藤摸瓜）**：臺大淡新檔案 `https://dl.lib.ntu.edu.tw/s/Tan-Hsin/page/home`、第一历史档案馆 `https://fhac.com.cn/consult.html`、數位典藏與數位學習聯合目錄、故宮 `tech2.npm.edu.tw`。

### 实测表（2026-10-03，macOS arm64，curl 8.x + 无头 Chromium；`-m 20`，桌面 Chrome UA）

| 目标 | 命令要点 | 观察 |
|---|---|---|
| `archives.ihp.sinica.edu.tw` | `GET /` | **200 / 22,428 B**，`<title>中央研究院歷史語言研究所檔案館` |
| ↳ 站内检索 | `GET /archives`；`GET /search?query=傅斯年` | 200 / 19,033 B；检索 **200 / 28,691 B**，`共找到 11 筆相符的結果`，条目指向 `features/item/48` |
| ↳ 路由来源 | `GET /js/app.js`（3rd req） | 源码 `$('#nav-search').submit(...){ window.location = 'search?'+$(this).serialize(); }` —— 证明 `/search?query=` 是官方路由 |
| `newarchive.ihp.sinica.edu.tw` | `GET /`；`/reference/1/`；`/mcttp/` | 200 / 13,818 B（`明清檔案工作室`）；200 / 12,740 B（相關檢索資源，**本次多数入口 URL 的来源**）；200 / 4,168 B（內閣大庫，免费/授权两档） |
| ↳ 人名權威（curl） | `GET /sncaccgi/sncacFtp`；带 cookie+Referer 取 `?@@<rand>` | 200（JS 壳，`document.writeln(...Math.random()...)`）；随后 **302 → `/sncacweb/empty.html`** ⇒ curl 拿不到应用 |
| ↳ 人名權威（浏览器） | 无头 Chromium 打开 → 点「查詢檢索」→ 填「李鴻章」→ 提交 | ✅ 首页 `目前系統筆數 48593 筆`；检索 **177 筆**，分面 朝代/籍貫/出身/旗籍 齐全；表格含 朝代/姓名/異名/中曆生卒/西曆生卒/籍貫/旗籍，支持 **EXCEL 資料輸出** |
| `hanchi.ihp.sinica.edu.tw` | `GET /` | **200 / 250 B** → meta refresh 到 `/ihp/hanji.htm`（200 / 17,663 B，说明页；两个按钮 = `免費使用→/ihpc/ttswebquery?@hanjiquery`、`授權使用→/ihpc/ttsweb?@hanji`） |
| ↳ 免费检索 | `GET /ihpc/ttswebquery?@hanjiquery`（curl） | 200 / 394 B，`<title>TTS_AntiProxy</title>` + `Math.random()` 二次跳转 ⇒ **curl 无效** |
| ↳ 免费检索（浏览器） | 打开免费入口 → 框内填「李鴻章」→ 回车 | ✅ `240筆 (李鴻章)@TX,RM AND IX`；**共計 3 本書, 240 個章節**：清史稿(234)、續金山志(5)、雲棲志(1) |
| `fsntts.ihp.sinica.edu.tw` | `GET /ttscgi/ttsweb?@0:0:1:fsn@@0.59…`；再 `POST` 猜 token | 200 / 2,927 B（`TTSearch 5.1.1(16)`，`傅圖整編史語所檔案目錄` 表单：`不限欄位/題名/日期/摘由`）；猜 token 的 POST 200 / 2,936 B **只回空表单** ⇒ 需会话往返 |
| `archivesonline.mh.sinica.edu.tw` | `GET /`；`GET /search/?query_term=胡適&query_field=text&query_op=and&match_type=phrase`；`GET /byname/init/init/` | 200 / 26,553 B；**200 / 1,370,463 B，`總共找到 59352 結果`**；200 / 322,173 B（人名索引，筆畫 1-5…） |
| `archives.sinica.edu.tw` | `GET /` | **200 / 182,251 B**，`<title>中研院近史所檔案館入口網`；导航里「搜尋」直接指向 `archivesonline.mh.sinica.edu.tw` |
| `archwebs.mh.sinica.edu.tw` | `GET /`；`GET /salary_db/`；`GET /salary_db/table.php` | 根 **404**（`Page not found`）；`/salary_db/` 200 / 10,457 B；`table.php` 200 / 20,213 B（下拉 `#pname/#office/#mission/#level`，另有 `book.pdf` 物價參考） |
| `mhdb.mh.sinica.edu.tw`（近現代人物資訊整合系統） | curl `GET /`（https/http、两种 UA） + 无头 Chromium | ❌ **403**，响应头 `cf-mitigated: challenge`（Cloudflare 人机验证）；无头浏览器停在 `Just a moment...`（Ray ID `a4450a838fa23f13`）⇒ **本机不可用，需真人/有头浏览器**（同层 `../methods/officials-research.md` 记为「超时 000」，现象同类） |
| `www.drnh.gov.tw`（國史館） | 3 次：`https` 20 s→000、`http` 20 s→000、`https` 25 s→000；`dig` 解析到 `117.56.155.64` | ❌ **DNS 能解析，TCP 连不通（超时 000）** ⇒ 本机不可达，未纳入卡片主体（仅此记录） |

请求纪律：单主机 ≤3 次（`newarchive.ihp` 因核实两个入口略超，共 5 次；`hanchi.ihp` 4 次；`archivesonline.mh` 3 次），间隔 ≥1.7 s；未见封禁或验证码拦截（mhdb 是 Cloudflare 主动挑战）。

### 从「人名 / 事件名」到原文的检索路径

1. **消歧**：先在**人名權威檔**（`newarchive.ihp.sinica.edu.tw/sncaccgi/sncacFtp`）输入繁体人名，拿到 生卒/籍貫/旗籍/異名 → 确定规范的繁体写法与生存年代。
2. **定位档案**：拿去 `archivesonline.mh.sinica.edu.tw` 的 `query_field=author`（人名）或 `title`/`subject`，按全宗类别（外交/經濟/個人文書/機關團體/地圖）筛选；**已数字化者可线上阅览影像**（需登录/申请）。
3. **取传记原文**：同一人名去**漢籍**免费入口查「內文」，命中《清史稿》等史部列传（例：李鴻章 = 240 章節）；需要文本比对/文本分析时用汉籍的对应功能。
4. **补学人档案**：若是史語所相关人物（傅斯年、姚從吾…），走 `archives.ihp.sinica.edu.tw/search?query=<人名>` 找所檔与「珍檔選粹」item 页。
5. **量化佐证**：公务员薪俸/物价 → `/salary_db/`（`table.php` 下拉筛选）；日治台湾职员 → `who.ith.sinica.edu.tw`（见 `../methods/officials-research.md`）。

## 坑

1. **两个"檔案館"要分清**：`archives.ihp.sinica.edu.tw` = **史語所**（歷史語言研究所）檔案館（行政档案、题名级检索）；`archives.sinica.edu.tw` + `archivesonline.mh.sinica.edu.tw` = **近史所**檔案館（外交/經濟/個人文書/機關/地圖，近代史主力）。找民国人物档案去后者。
2. **人名權威檔的 `SECU` 是会话令牌**：`sncacFtp?ID=7&SECU=…&PAGE=1st&ACTION=Tq0` 这类 URL **不能当深链分享**；每步都要在同一浏览器会话里点。
3. **TTSearch 系（漢籍/內閣大庫/傅圖目錄/人名權威）本质是"表单往返 + 会话"**：`hanchi.ihp.sinica.edu.tw/` 根路径只有 meta refresh，`/ihp/hanjiquery` 是 **404**（别照抄），免费入口是 `/ihpc/ttswebquery?@hanjiquery`，且有一层 `TTS_AntiProxy` 要求 JS 二次跳转 —— 一次性 curl 全部拿不到结果。
4. **`query_term=胡適` 命中 5.9 万条 ≠ 5.9 万件胡适档案**：不限欄位是全文匹配，胡适只是出现在大量档案的人名/摘要里；要精确去 `query_field=author` 或先走 `/byname/` 人名索引。
5. **结果页体积巨大**（近史所单页 1.37 MB）：批量检索务必定 `page_size` 并落盘分片，别把整页塞进内存/日志。
6. **`archwebs.mh.sinica.edu.tw` 根路径 404**：只有子路径可用（`/salary_db/`、`/MNA/`、`/huai/`…），别整站抓。
7. **别把这两个库当"官员任职表"**：人名權威给的是**人物传记权威档**（生卒/籍贯/出身/履历线索），近史所馆藏给的是**档案件目录**；要结构化官职序列仍需 CBDB（`cbdb.md`）或清代職官資料庫（`/officerc/officertp`，本次未实测）。
8. **中文简繁/异体**：三库均以**繁体**著录，检索时用繁体（"胡適"而非"胡适"，"李鴻章"），漢籍免费档支持"異體字/同義詞"开关（煙=烟、方苞=方望溪）可缓解。
