# city-credit —— 城市信用监测排名与信用政策

- 去哪找：
  - 全国城市信用状况监测平台 `https://creditcity.creditchina.gov.cn/Index.aspx`；信用报告下载 `https://creditcity.creditchina.gov.cn/page/CreditReportDownload.aspx`
  - 信用中国「城市信用」栏目 `https://www.creditchina.gov.cn/chengshixinyong/`（站点接口与 WAF 详见 `credit-china.md`，此处不重复）
  - 地方信用站镜像（月度排名与《城市信用监测简报》）：信用河南 城市信用排名 `https://credit.henan.gov.cn/ca/20240809000009.htm`；信用珠海「信用城市状况监测」`https://credit.zhuhai.gov.cn/xyzh2024/csxyzkjc/ranking/toIndexRanking?menu=csxyzkjc`；信用无锡 `https://wuxicredit.wuxi.gov.cn/`
  - 中办国办《关于健全社会信用体系的意见》 `https://www.gov.cn/gongbao/2025/issue_11986/202504/content_7019258.html`（解读 `https://www.gov.cn/zhengce/202503/content_7016601.htm`）
  - 《2024—2025年社会信用体系建设行动计划》 `https://www.gov.cn/zhengce/zhengceku/202406/content_6955501.htm`
  - 发改委财金司（信用口）`https://www.ndrc.gov.cn/fzggw/jgsj/cjd/`（工作动态 `…/cjd/sjdt/`）
  - 全国社会信用体系建设示范区名单：第五批 `https://www.ndrc.gov.cn/xxgk/zcfb/tz/202608/t20260820_1407094.html`（附件 `P020260820301111407100.pdf`）；第三批 `https://www.ndrc.gov.cn/xwdt/tzgg/202110/t20211029_1301581.html`
- 什么时候用：
  - 关键词：城市信用监测 / 城市综合信用指数 / 城市信用排名 → **全国城市月度信用指数与分档排名**。
  - 关键词：城市信用监测简报 / 城市信用监测月报 → **某城指数等级（优/良/好…）与位次**。
  - 关键词：社会信用体系 意见 / 信用建设行动计划 / 信用修复 → **国家层面政策原文与制度安排**。
  - 关键词：社会信用体系建设示范区 → **示范城市名单（分批）**。
  - 不适用：单主体红黑名单、双公示 → `credit-china.md`；企业工商 → `gsxt.md`。
- 怎么取：
  - **官方排名**：走 `creditcity` 平台（含报告下载页）；本机不可直连（见实测）。同一套月度数还会以**新闻/简报**形态发在各地信用站与地方发改委，用 `web_search`「城市信用监测排名 <城市>」或地方站「城市信用排名」栏目定位。
  - **地方站栏目**：省级信用站多为 `credit.<省>.gov.cn`；部分站（如珠海）是 Vue+axios 单页，排名在 XHR，需浏览器或复现其 XHR。
  - **政策原文**：gov.cn 公报 / 政策文件库（见 `gov.cn.md`）；发改委财金司栏目 + 通知公告 PDF 附件（示范区名单）。
  - 结果形态：HTML（地方站简报/新闻）+ PDF（示范区名单）+ SPA（`creditcity`、珠海等排名页）。
- 覆盖：城市信用监测为**月度**（综合信用指数 + 等级 + 分档排名），覆盖全国省会 / 地级 / 县级市；示范区名单 2018 起分批（第三批 2021、第五批 2026-08）；信用政策 2014《社会信用体系建设规划纲要》—2025《健全社会信用体系的意见》。
- 门槛：官方平台与信用中国有 WAF（瑞数 + 加速乐）；地方信用站与 gov.cn 免费、免登录。
- 实测：2026-10-03，macOS arm64，curl 8.x，桌面 UA，20 s 超时。
  - `https://creditcity.creditchina.gov.cn/Index.aspx` → `000`（20 s 超时，0 字节）；换 `http://` → **412**（2,565 B WAF 页）。
  - `https://www.creditchina.gov.cn/chengshixinyong/` → **412**（body 含瑞数 `$_ts`；站点 WAF 详见 `credit-china.md`）。
  - `https://credit.henan.gov.cn/ca/20240809000009.htm` → `200`（标题「城市信用排名」；正文含字体混淆 token 串与全国省级信用站 URL 目录）。
  - `https://credit.zhuhai.gov.cn/xyzh2024/csxyzkjc/ranking/toIndexRanking?menu=csxyzkjc` → `200`（Vue+axios 外壳，排名走 XHR）。
  - `https://wuxicredit.wuxi.gov.cn/` → `200`（「信用中国（江苏无锡）」，含《城市信用监测简报》类新闻）。
  - `https://credit.xining.gov.cn/` → `000`（连接被重置）。
  - gov.cn《意见》公报页 `200`；《行动计划》`200`；发改委财金司 `200`；第五批示范区通知 `200`（含 PDF 附件）。
- 上游：<https://www.creditchina.gov.cn/>；<https://creditcity.creditchina.gov.cn/>；<https://www.gov.cn/>；<https://www.ndrc.gov.cn/>

## 细节

### 地方信用站 URL 规律与排名入口

- 省级：`credit.<省拼音缩写或全拼>.gov.cn`（河南 `credit.henan.gov.cn`、浙江 `credit.zj.gov.cn`、江苏 `credit.jiangsu.gov.cn`、山东 `credit.shandong.gov.cn`、湖北 `credit.hubei.gov.cn`…）；直辖市/计划单列另式（北京 `creditbj.jxj.beijing.gov.cn/credit-portal`、天津 `credit.fzgg.tj.gov.cn`、上海 `credit.fgw.sh.gov.cn`）。
- 「城市信用排名 / 信用城市状况监测」栏目内嵌于地方站；珠海示例路径 `…/csxyzkjc/ranking/toIndexRanking?menu=csxyzkjc`（`csxyzkjc` = 城市信用状况监测）。
- 全国省级信用站 URL 目录可从 `credit.henan.gov.cn/ca/20240809000009.htm` 页脚一次取全。

### 政策与名单

| 资源 | URL |
|---|---|
| 中办国办《关于健全社会信用体系的意见》(2025) | `https://www.gov.cn/gongbao/2025/issue_11986/202504/content_7019258.html` |
| 　└ 政策解读 | `https://www.gov.cn/zhengce/202503/content_7016601.htm` |
| 《2024—2025年社会信用体系建设行动计划》 | `https://www.gov.cn/zhengce/zhengceku/202406/content_6955501.htm` |
| 发改委财金司（信用） | `https://www.ndrc.gov.cn/fzggw/jgsj/cjd/` |
| 第五批全国社会信用体系建设示范区名单（发改办财金〔2026〕589号） | `https://www.ndrc.gov.cn/xxgk/zcfb/tz/202608/t20260820_1407094.html` |
| 第三批示范区名单 | `https://www.ndrc.gov.cn/xwdt/tzgg/202110/t20211029_1301581.html` |

### 城市信用指数怎么看

- 指标：**综合信用指数**（百分制），对应等级（如「优/良/好/一般/差」），按城市分档（省会及副省级、地级、县级市）分别排名。
- 发布节奏：月度；官方口径在 `creditcity` 平台，地方以《城市信用监测简报》或新闻稿转载当月结果。

## 坑

1. **官方平台不可直连**：`creditcity.creditchina.gov.cn` 本机 20 s 超时，`http://` 得 412；与信用中国主站同族 WAF（瑞数 + 加速乐，见 `credit-china.md`）。
2. **无全国统一开放表**：月度排名没有公开 API / 可下载全表；只能逐城市从地方站简报、地方发改委新闻或第三方转载拼。
3. **地方站常做字体混淆**：如信用河南排名页正文混入随机 token 串（字体反爬），直接取文本会拿到乱码。
4. **部分站不可达**：信用西宁等 `credit.<city>.gov.cn` 会连接重置；先用 `web_search` 找有转载的站再抓。
5. **SPA 排名**：珠海等 Vue+axios 站点须执行 JS 或复现 XHR，纯 curl 只得到外壳。
6. 示范区名单分批、以 PDF 附件形式发布；批次越新越要靠发改委通知公告检索（可用 `business-environment.md` 的 `fwfx.ndrc.gov.cn/api/query`）。
