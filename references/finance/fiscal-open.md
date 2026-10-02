# fiscal-open —— 财政预决算公开入口

- 去哪找：**中央预决算公开平台** `https://www.mof.gov.cn/zyyjsgkpt/`（中央政府预决算 `/zyzfyjs/`、中央部门预决算 `/zybmyjs/`、中央对地方转移支付 `/zyddfzyzf/`）；**财政部预算司（原表）** `http://yss.mof.gov.cn/`；**财政数据栏目** `https://www.mof.gov.cn/gkml/caizhengshuju/`。各省级财政厅预决算专栏见「细节」。
- 什么时候用：要**中央/部门/省级政府预决算原文**（一般公共预算、政府性基金、国有资本经营、社保基金四本账；部门预算/决算、「三公」经费、转移支付分地区表）；核对某单位当年预算数；做财政透明度/预算研究。
- 怎么搜：**三步 URL 法** —— ① 进 `zyyjsgkpt` 选层级（中央/部门/转移支付），② 列表页按年（`index_1.html`、`index_2.html` 递增），③ 文章页规律：财政部本平台 `…/bumenyusuan/{YYYYMM}/t{YYYYMMDD}_{id}.htm`，中央财政预算原文走 `http://yss.mof.gov.cn/{YYYY}zyczys/`（逐年目录）。省级是各家 CMS：`/col/col{NNNNN}/index.html`、`/art/{Y}/{M}/{D}/art_{id}_{id}.html`、`/scczt/c{NNNNN}/{Y}/{M}/{D}/{hash}.shtml`。结果形态 **HTML**（正文表或附件 PDF/xls），无通用 JSON 接口。
- 覆盖：中央本级与部门预决算（约 2012 年起逐年）；中央对地方转移支付分地区表；31 省市县各级预决算（公开深度各省不一）；全国财政收支月/年度数据（财政数据栏目）。粒度到「款/项/目」级科目与单位。
- 门槛：免费、无需登录；部分省专栏是 JS 跳转壳（如江苏统一平台、广东 `/tjzl/`）。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA——`zyyjsgkpt/` `200/4654B`；`…/zyzfyjs/zyys/` `200/3691`；`…/zybmyjs/bmys/` `200/4118`；`…/zyddfzyzf/` `200/3551`；`gkml/caizhengshuju/` `200/4829`；`yss.mof.gov.cn` `200/5577`；广东 `/zdlyxxgk/index.html` `200/8648`、江苏 `col51147` `200/4288`、四川 `c102361` `200/22872`、湖南 `xxgk` `200/16201`、浙江 `col1172179` `200/9501`。
- 上游：财政部（`mof.gov.cn`）；各省财政厅官网。

## 细节

### 一、中央预决算公开平台（`https://www.mof.gov.cn/zyyjsgkpt/`）

| 栏目 | URL | 实测 |
|---|---|---|
| 平台首页 | `/zyyjsgkpt/` | ✅ 200 / 4654 B |
| 中央政府预算 | `/zyyjsgkpt/zyzfyjs/zyys/` | ✅ 200 / 3691 B |
| 中央政府决算 | `/zyyjsgkpt/zyzfyjs/zyjs/` | 同栏目结构 |
| 中央部门预算 | `/zyyjsgkpt/zybmyjs/bmys/` | ✅ 200 / 4118 B |
| 中央部门决算 | `/zyyjsgkpt/zybmyjs/bmjs/` | 同栏目结构 |
| 中央对地方转移支付 | `/zyyjsgkpt/zyddfzyzf/` | ✅ 200 / 3551 B |

- **中央财政预算原文**（平台首页外链，逐年目录）：`http://yss.mof.gov.cn/{YYYY}zyczys/`，如 `2026zyczys/`、`2025zyczys/`。
- **部门预算/决算文章页**形态：`https://www.mof.gov.cn/zyyjsgkpt/zybmyjs/bmys/bumenyusuan/{YYYYMM}/t{YYYYMMDD}_{id}.htm`；列表页用 `index_1.html`、`index_2.html` 翻页。
- `/zybmyjs/bmys/` 列表里每条直接外链到**各部委自建的部门预算页**（教育部 `moe.gov.cn/srcsite/…`、文旅部 `zwgk.mct.gov.cn/zfxxgkml/cwxx/ysjs/…`、体育总局 `sport.gov.cn/n315/n332/c…` 等）——要找某部预算，从这张列表跳最省事。

### 二、省级财政厅预决算专栏（抽查 5 省，2026-10-03）

| 省 | 专栏 URL | 状态 | 文章页规律 |
|---|---|---|---|
| 广东 | `https://czt.gd.gov.cn/zdlyxxgk/index.html`（重点领域信息公开·财政数据）；地市财政信息 `https://czt.gd.gov.cn/dfczxx/index.html` | ✅ 200 / 8648 B | 省站 CMS |
| 江苏 | 政府预决算 `https://czt.jiangsu.gov.cn/col/col51147/index.html`；部门预决算 `…/col/col51148/index.html` | ✅ 200 / 4288 B、4467 B | `/art/{Y}/{M}/{D}/art_{栏目id}_{文档id}.html`；统一平台 `http://yjsgk.jsczt.cn/`（本机 25s 超时 ❌） |
| 浙江 | 政府信息公开 `https://czt.zj.gov.cn/col/col1172179/index.html` | ✅ 200 / 9501 B | `/art/{Y}/{M}/{D}/art_{id}_{id}.html`；旧检索命中的 `col/col1416803`、`col/col1416805` 本机 **404** ❌ |
| 四川 | 预决算信息公开 `https://czt.sc.gov.cn/scczt/c102361/common_list.shtml`；省级政府预算 `/scczt/c102371/common_list.shtml`；市县预决算 `/scczt/scszsyjs/sxyjs.shtml` | ✅ 200 / 22872 B | `/scczt/c102361/{Y}/{M}/{D}/{hash}.shtml` |
| 湖南 | 政府信息公开 `https://czt.hunan.gov.cn/czt/xxgk/index.html`；预算执行情况 `…/czt/xxgk/yszx/index.html` | ✅ 200 / 16201 B | 省站 CMS |

> 更多省级年鉴式入口见 `../regional/provincial-yearbooks.md`；本卡只收「预决算公开」这一类专栏。

### 三、中国财政年鉴

- 官方入口：`https://www.mof.gov.cn/zaixianfuwu/baokannianjian/CaiZhengBuBaoKanNianJian/CaiZhengBuNianJian/CaiZhengBuZhongGuoCaiZhengNianJian/`（实测 200 / 3772 B，**仅栏目壳、无逐年目录**）。
- 实际取书：中国统计信息网 `http://www.tjcn.org/tjnj/CCC/`（如 2024 卷 `http://www.tjcn.org/tjnj/CCC/43454.html`，✅ 200，非官方）；或商业年鉴站（见 `../stats/ministry-stats.md`、`../regional/provincial-yearbooks.md`）。

## 坑

1. **列表页翻页是 `_1/_2` 序号文件**（`index_1.html`），不是 `?page=`；改年份要找栏目页里的目录链接。
2. **省级路径逐年改版**：浙江旧 `col` 号已 404；照搬搜索结果里的 URL 前先 `--probe` 一次。
3. 江苏统一公开平台 `yjsgk.jsczt.cn`、广东统计资料 `/tjzl/` 等是 **JS 跳转壳/SPA**，curl 拿不到内容，需浏览器。
4. 部门预决算的**正文常是附件**（PDF/xls/扫描图），列表页标题 ≠ 数据；拿数字要落到附件并记标题+日期。
5. 「预决算公开」有两种粒度：**政府预决算**（财政厅本级）与**部门预决算**（各单位），别混用；中央部门数据在 `zybmyjs` 下按部委分开。
6. 财政数据栏目（`gkml/caizhengshuju/`）是**月度财政收支**快报，与年度预决算不同口径，引用时标明。
