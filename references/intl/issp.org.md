# issp.org —— 国际社会调查项目

- 去哪找：门户 `https://issp.org/`；下载导航 `https://issp.org/data-download/by-topic/`（另有 `by-year/`、`archive/`）；**实体数据托管在 GESIS**：新平台 `https://search.gesis.org/research_data/{ZA编号}`，老入口 `https://dbk.gesis.org/dbksearch/sdesc2.asp?no={ZA号}`。
- 什么时候用：要**主题轮换**的跨国态度调查——社会不平等、政府角色、家庭与性别、宗教、环境、健康、国家认同、工作取向、数字社会；做"主题 × 国家 × 年份"的三维比较。
- 怎么取：
  - ISSP 站只做导航；从 `by-topic` / `by-year` 点进模块 → 跳 GESIS 的 ZA 编号页 → 接受条款后下载（SPSS/Stata/CSV）。
  - 示例实测链接：`https://search.gesis.org/research_data/ZA10000`、`https://www.gesis.org/en/issp/data-and-documentation/{主题}/{年}`。
- 覆盖：1985–至今，每年一个模块、约 40–50 国；个体级；有各年文件与累积（Cumulative）文件（上游声明，未本机实测）。
- 门槛：免费；下载走 GESIS（需接受数据使用条款，部分需注册）。
- 实测：2026-10-03，macOS arm64，curl 8.x：`https://issp.org/data-download/by-topic/` → 200 / 45.6 KB，页内实测含 `search.gesis.org/research_data/ZA10000`、`gesis.org/en/issp/data-and-documentation/...`、老 `dbk.gesis.org/dbksearch/sdesc2.asp?no=3090...` 等实体链接；`https://search.gesis.org/` → **403 Cloudflare "Just a moment..."**（本机 curl 被挡，需浏览器）。
- 上游：`https://issp.org/`（ISSP）；数据档案 `https://www.gesis.org/`（GESIS）。

## 坑

1. `search.gesis.org` 有 **Cloudflare 人机验证**，curl 直连 403；下载走浏览器，或试老入口 `dbk.gesis.org`。
2. ISSP 模块**不是每国每年都参加**；做面板前先核该国的参与矩阵。
3. 变量名跨模块复用（`v1`–`vN`），语义随模块变，必须逐模块读 codebook。
4. 中国（大陆）参与模块有限，多数主题缺中国样本；取数前先查覆盖表，勿默认可得。
