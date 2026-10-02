# city-stat-yearbook —— 城市县域统计年鉴取数入口

- 去哪找：
  - 国家统计局免费年鉴（**只有《中国统计年鉴》**）`https://www.stats.gov.cn/sj/ndsj/`
  - 知网·统计年鉴库（含城市/县域年鉴表格）`https://data.cnki.net/trade/yearBook/single?id=<年鉴ID>`——中国城市统计年鉴 2024 `N2025020156`、中国县域统计年鉴 2024 `N2025020141`（登录门槛见 `cnki-data.md`）
  - 国家基础学科公共科学数据中心 数据集 `https://www.nbsdc.cn/general/dataDetail?id=64ef8562bb16e0591d02587b&type=1`（城市统计年鉴数据）
  - 第三方年鉴站：`tjnjdata.com`、`tjcn.org`、`tongjinianjian.com`、`macrodatas.cn`、`shujuxiaomaibu.com`
- 什么时候用：要**地级市 / 县级单位**的年鉴面板（GDP、人口、财政、工业、投资、从业人员…），或要「某年城市统计年鉴里的某张表」；国家统计局官网只免费放《中国统计年鉴》，城市/县域年鉴**无官方免费下载**，须走知网或第三方/商业库。
- 怎么搜：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # 国家统计局年鉴列表（免费，HTML/PDF）
  curl -sS -A "$UA" 'https://www.stats.gov.cn/sj/ndsj/'
  # 知网年鉴详情（SPA 壳，内容需登录后再走 valueSearch 指标检索）
  curl -sS -A "$UA" 'https://data.cnki.net/trade/yearBook/single?id=N2025020156&zcode=Z026'
  ```
  结果形态：国家统计局为 **HTML 目录 + 年鉴页**（2003 年为整本 PDF）；知网为 **SPA（需登录，按指标检索导表）**；第三方站为 HTML 介绍页 + 注册/付费下载。
- 覆盖：国家统计局《中国统计年鉴》**2000–2025**（2001 仅目录、2003 为 PDF、2004 起逐年 HTML）；中国城市统计年鉴 1985–2024、中国县域统计年鉴 2000–2024（**年份跨度系第三方站自述，未逐年核**）。
- 门槛：国家统计局 免费无登录；知网 **订阅 + 登录**（匿名检索 471，见 `cnki-data.md`）；第三方年鉴站 **注册/付费**；nbsdc **注册**（多为科研实名）。
- 实测：2026-10-03，macOS arm64，curl 8.x，桌面 UA，20 s 超时，≥1.5 s 间隔：
  - `https://www.stats.gov.cn/sj/ndsj/` → 200，列表**仅《中国统计年鉴》**（2000、2001、2003–2025；2003=`yearbook2003_c.pdf`，2004=`/sj/ndsj/yb2004-c/indexch.htm`，最新 2025=`/sj/ndsj/2025/indexch.htm`）✅
  - `https://data.cnki.net/trade/yearBook/single?id=N2025020156&zcode=Z026`（中国城市统计年鉴 2024）→ 200（4.3 KB SPA 壳，内容需登录）⚠️
  - `https://data.oversea.cnki.net/trade/yearBook/single?id=N2025020156&zcode=Z026` → 404 ❌；`https://cnki.istiz.org.cn/…` → 000（不可达）❌
  - `https://www.tjnjdata.com/Yearbook/zhongguo-chengshi-tongji-nianjian-2024.html` → 200（页首「官方发布数据整理」、`登录/注册`）⚠️；`tjcn.org` → 200；`tongjinianjian.com/china-county-statistical-yearbook.html` → 200
  - `https://www.nbsdc.cn/general/dataDetail?id=64ef8562bb16e0591d02587b&type=1` → 200（数据集详情，下载需注册）⚠️
- 上游：国家统计局；《中国城市统计年鉴》《中国县域统计年鉴》国家统计局城市/农村社会经济调查司编、中国统计出版社；知网 `data.cnki.net`；第三方站各自页脚。

## 细节

### 三级取数路径

| 层级 | 来源 | 能拿到什么 | 形态 |
|---|---|---|---|
| ① 官方免费 | `stats.gov.cn/sj/ndsj/` | **仅《中国统计年鉴》**全国/分省表（含少量分城市节） | HTML 表 / PDF |
| ② 官方派生 | `../stats/data.stats.gov.cn.md`「主要城市年度数据」 | 分城市年度指标**数值**（免费 API） | JSON |
| ③ 年鉴全文 | 知网 `data.cnki.net` / 第三方站 | 城市/县域年鉴**整表**（按指标检索组配） | 需登录/付费 |

- 知网年鉴 ID 规律：`trade/yearBook/single?id=N{YYMM}…`；城市 2024 = `N2025020156`、县域 2024 = `N2025020141`（`zcode` 取 `Z004`/`Z026` 指向同一库的不同入口）。检索式与登录态见 `cnki-data.md`。
- 要「城市面板」但不想逐本年鉴抄：直接走 `../stats/data.stats.gov.cn.md`（分省/主要城市）或 `epsnet.md`（城市时间序列）更省事；年鉴的价值在于**县级 + 年鉴口径的原始表**。

## 坑

1. **国家统计局没有《城市统计年鉴》/《县域统计年鉴》免费版**：`stats.gov.cn/sj/ndsj/` 只有《中国统计年鉴》，别在官网死找。
2. **第三方站可信度分级**：`tjnjdata.com` 等自述「官方发布数据整理」，非官方；引用前与知网原书或纸本核对表名/口径，正式引用标「转自《…年鉴》××年」。
3. **知网入口域名混乱**：`data.cnki.net` 可用（SPA+登录）；镜像 `data.oversea.cnki.net`（404）、`cnki.istiz.org.cn`（不可达）本机均不可用，别写进脚本。
4. 国家统计局年鉴老版本形态不一：2001=目录页、2003=整本 PDF、2004=`yb2004-c`——爬取要按年份分支处理。
5. 城市/县域年鉴的**口径与《中国统计年鉴》分城市表不完全一致**（行政区域、市辖区 vs 全市），跨源比较前先核行政区范围与「市辖区/全市」口径。
