# epaper/ —— 数字报 / 电子报平台（索引）

数字报是「把某报某年逐期版面/文章拉全」的通道：URL 规则化、可枚举、多数可 curl 直读。本目录一报一文件，README 内嵌其余各报的平台总览，给**可用的入口 + 期次/版面/文章 URL 模板 + 存档深度**。所有 `✅/⚠️/❌` 为 **2026-10-02 本机 curl 实测**（macOS，桌面 UA）。

## 文件一览

| 文件 | 来源 | 用途/何时用 | 状态 |
|---|---|---|---|
| `xepaper.com.md` | 密云报等区报数字报 | 按日期取逐期原文（含 2018 吹哨报到配套文件） | ✅ 静态 HTML 直读 |
| `yqb.bjyq.gov.cn.md` | 延庆报数字报（PDF） | 逐期 PDF 直链，2018 全年 151 期 604 版可全量 | ✅ PDF 可下载 |
| （README 内嵌）人民日报 / 光明日报 / 经济日报 / 北京日报 / 新京报 | 各报数字报 | 入口 + 期次/版面/文章 URL 模板 + 存档深度（见下「平台总览」） | ✅/⚠️ 见下表 |

### 平台总览（实测 2026-10-02）

| 报纸 | 入口（✅=curl 可直读） | 期/版面 URL 模板 | 文章 URL 模板 | 存档深度（实测） |
|---|---|---|---|---|
| **人民日报** | `http://paper.people.com.cn/` ✅ → `rmrb/pc/layout/index.html` ✅ | `/rmrb/pc/layout/YYYYMM/DD/node_NN.html`（NN 两位） | `/rmrb/pc/content/YYYYMM/DD/content_NNNNNNNN.html` | 约近 2 年：2025-09 ✅、2024-12 ✅、2024-11 ❌、2024-09 ❌；更早走图文数据库（需登录） |
| **光明日报** | `http://epaper.gmw.cn/` ✅；`/gmrb/html/layout/index.html` ✅ | 旧：`/gmrb/html/YYYY-MM/DD/nbs.D110000gmrb_NN.htm` ✅<br>新：`/gmrb/html/layout/YYYYMM/DD/node_NN.html` ✅ | 旧：`/gmrb/html/YYYY-MM/DD/nw.D110000gmrb_YYYYMMDD_N-NN.htm` ✅ | **旧模板覆盖 2012 起**：2012 ✅、2015 ✅、2018 ✅、2019/2021/2023/2024 ✅、2025-06 ✅、2025-09 ✅；2026-01 起转新模板（旧模板 404） |
| **经济日报** | `http://paper.ce.cn/` ✅；`/pc/layout/index.html` ✅ | `/pc/layout/YYYYMM/DD/node_NN.html` ✅ | `/pc/content/YYYYMM/DD/content_NNNNNN.html` ✅ | 2026-10 ✅、2024-12 ✅、2023-01 ✅、2022-01 ✅；2018 ❌ |
| **北京日报** | `https://www.bjd.com.cn/bjrb/dzb` ✅（302→mobile 页） | `/bjrb/mobile/YYYY/YYYYMMDD/YYYYMMDD_m.html` ✅ | 同页（当期为整版/目录页） | 2025 ✅、2024 ✅、2022-01 ✅、2020 ❌、2019 ❌、2018 ❌ → **无 2018 存档** |
| **新京报** | `https://epaper.bjnews.com.cn/` ⚠️ meta 跳转壳 | `/html/YYYY/YYYYMMDD/YYYYMMDD_A0N/YYYYMMDD_A0N_<稿号>.html` | 同页为**整版图片**（无正文文本） | 当期 ✅；2018 版面 URL 301 回落根壳（不可靠） |
| **延庆报** | `http://yqb.bjyq.gov.cn/` ✅ | `/resfile/YYYY-MM-DD/NN/NN.pdf`（PDF 直链） | 即 PDF | 2018 全年 151 期 604 版可全量（见文件） |
| **密云报** | `https://xepaper.com/` ✅ | `/myb/html/YYYY-MM/DD/node_N.htm`（版面目录） | `/myb/html/YYYY-MM/DD/content_N_M.htm` | 见文件 |

> 逐报细节见对应 `.md`。上表「存档深度」是**抽样**结论：只验证了所列日期，未逐日穷举。

## 选路

1. **先探模板再放量**：每报只验证了少量日期；批量前先用 `curl -s -o /dev/null -w '%{http_code}'` 打几个日期确认模板与深度，再逐日枚举（≤3 次/主机、间隔 ≥1.5s、timeout 20s）。
2. **版面目录页 → 文章链接**：先取 `node_NN.html`（或旧模板 `nbs…` 首页），grep 出文章链接，避免猜文章 id。
3. **编码**：多数为 UTF-8；个别旧站 GBK，用 `iconv -f gb18030` 兜底。
4. **2018 覆盖现实**：人民日报/经济日报/北京日报数字报**均无 2018 存档**；能覆盖 2018 的是**光明日报旧模板**、延庆报 PDF、密云报，以及各报网站的历史文章页（人民网/新京报/京报网文章直链）。

## 相关

- media 主层：`../README.md`（央媒/市媒转载/检索通道、各报网站搜索 API）。
- 各报网站层：`../people.com.cn.md`、`../bjnews.com.cn.md`。

## 细节

### 分报说明

#### 人民日报（`paper.people.com.cn`）

- ✅ `http://paper.people.com.cn/` → 301 到 `/rmrb/index.html` → `/rmrb/paperindex.htm` → `/rmrb/pc/layout/index.html`（当期版面列表，2,721 B）。
- 当期版面：`http://paper.people.com.cn/rmrb/pc/layout/202610/02/node_01.html`（✅ 200，25,720 B）。
- 文章：版面页里链接形如 `../../../content/202609/30/content_30183818.html` → 全路径 `/rmrb/pc/content/YYYYMM/DD/content_NNNNNNNN.html`。
- **旧模板** `/rmrb/html/YYYY-MM/DD/nbs.D110000renmrb_01.htm` 实测 403（不可用）。
- 全量存档（1946 至今）在 `https://data.people.com.cn/rmrb/YYYYMMDD/N`，**跳登录**（`member/login`），需机构账号。
- 同平台姐妹报（根页有链接，未逐个验证）：`rmrbhwb`（人民日报海外版）、`rmlt`（人民论坛）、`rmzk`、`mszk`、`zgcsb`、`zgjjzk` 等，模板同上。

#### 光明日报（`epaper.gmw.cn`）

- ✅ `http://epaper.gmw.cn/`（6,702 B，`<title>光明数字报`）。
- **旧模板（2012–2025-09，含 2018）**：`http://epaper.gmw.cn/gmrb/html/2018-03/15/nbs.D110000gmrb_01.htm` → ✅ 200，标题「2018年03月15日 星期四_光明日报_第01版:头版」。
  - 版面页里的文章链接：`nw.D110000gmrb_YYYYMMDD_<文章序号>-<版面号>.htm`，例：`nw.D110000gmrb_20180315_1-01.htm`（✅ 200，《汪洋当选全国政协主席》）。
- **新模板（2026 起）**：`http://epaper.gmw.cn/gmrb/html/layout/202610/02/node_01.html`（✅ 200），文章链接 `/gmrb/html/content/YYYYMM/DD/content_NNNNN.html`。
- 频道：`gmrb`（光明日报）、`wzb`（文摘报）、`zhdsb`（中华读书报）、`blqs`、`sz`、`lx`（根页链接，名称未核）。
- **2018 用旧模板**（`YYYY-MM` 带横杠 + `nbs`/`nw` 前缀）。

#### 经济日报（`paper.ce.cn`）

- ✅ `http://paper.ce.cn/` → `/pc/layout/index.html`（当期版面列表）。
- 版面：`http://paper.ce.cn/pc/layout/202610/02/node_01.html`（✅ 200，标题「要闻」）。
- 文章：`http://paper.ce.cn/pc/content/YYYYMM/DD/content_NNNNNN.html`（如 `content_339736.html`）。
- 存档：2022-01 ✅ / 2023-01 ✅ / 2024-12 ✅；2018 ❌。
- 注意：`epaper.ce.cn` 域名**连接失败**（curl 000），正确入口是 `paper.ce.cn`。

#### 北京日报 / 京报网

- 数字报入口：`https://www.bjd.com.cn/`（京报网首页）→「电子报」→ 北京日报 `https://www.bjd.com.cn/bjrb/dzb`（✅ 302 到 `…/bjrb/mobile/2026/20261002/20261002_m.html`）。
- 期次模板：`https://www.bjd.com.cn/bjrb/mobile/YYYY/YYYYMMDD/YYYYMMDD_m.html`。
- `paperindex.htm` 入口（JS 跳转当期，338 B）：北京日报 `https://bjrbdzb.bjd.com.cn/bjrb/paperindex.htm`；北京晚报 `…/bjwb/paperindex.htm`；法制晚报 `…/fzxb/paperindex.htm`；`https://bjsbdzb.bjd.com.cn/bjsb/paperindex.htm`（名单来自首页，中文名未核）。
- 存档深度：2022-01-01 ✅、2024-01-01 ✅、2025 ✅；**2020/2019/2018 ❌ → 无 2018 存档**。
- 西城数字报 `https://xichengdzb.bjd.com.cn/` 实测 **403 Forbidden**；`/bjxc/mobile/2018/20181105/20181105_m.html` 与 2025 版本均 404（未验证可用）。
- **2018 替代**：改用京报网文章页 `https://xinwen.bjd.com.cn/content/<id>.html`。实测 `https://xinwen.bjd.com.cn/content/s5c2c0e24e4b06597cc7df95a.html` → ✅ 200，标题《"吹哨报到"北京16区各有妙招》。

#### 新京报（`epaper.bjnews.com.cn`）

- ⚠️ 图片版：`https://epaper.bjnews.com.cn/`（759 B meta 壳）→ `/html/2026/20260930/20260930_A01/20260930_A01_7315.html`。
- 版面页含整版 JPG（`//epfile.bjnews.com.cn/group1/M00/…JPG`）+ `usemap="#mapPage"`，**正文不在 HTML**（JS 加载），curl 只能拿图。
- 2018 版面 URL 实测 301 回落根壳（不可靠）。**要 2018 新京报文本，用网站搜索 API**（见 `../bjnews.com.cn.md`，已验证含 2018：`s.bjnews.com.cn/bjnews/getlist`）。

#### 延庆报 / 密云报（已有文件）

- 延庆报：`yqb.bjyq.gov.cn.md` —— PDF 直链 `/resfile/YYYY-MM-DD/NN/NN.pdf`，2018 全年可全量枚举。
- 密云报：`xepaper.com.md` —— 静态 HTML，`/myb/html/YYYY-MM/DD/node_N.htm` 版面目录 + `content_N_M.htm` 文章。

### 实测

2026-10-02，macOS + curl：见上表各条状态码与字节数；关键抽样 —— 人民日报 `pc/layout/202609/30/node_01.html` 200，`202411/15` 404；光明日报 `gmrb/html/2018-03/15/nbs.D110000gmrb_01.htm` 200、`nw.D110000gmrb_20180315_1-01.htm` 200、新模板 `layout/202610/02/node_01.html` 200；经济日报 `pc/layout/202610/02/node_01.html` 200、`201803/15` 404；北京日报 `/bjrb/mobile/2024/20240101/20240101_m.html` 200、`2018/20180315` 404；京报网 `xinwen.bjd.com.cn/content/s5c2c0e24e4b06597cc7df95a.html` 200；新京报电子报版面页 200（含 `epfile.bjnews.com.cn` JPG）；`epaper.ce.cn` 000；`xichengdzb.bjd.com.cn` 403。
