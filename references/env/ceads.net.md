# ceads.net —— 中国多尺度碳排放清单

- 去哪找：数据入口 `https://www.ceads.net/data/`；碳排放清单 `https://www.ceads.net/data/carbon-inventory/`；投入产出表 `https://www.ceads.net/data/input-output-tables/`；清单检索辅助接口 `/user/category_tree.php?rootid=224`、`/user/search_suggest.php?typeid=224&q=<词>`、`/user/search_tags.php?typeid=224`。
- 什么时候用：中国分省/城市/县级 **CO₂ 清单、能源清单**（能源类型 × 部门）、省级投入产出表；写碳达峰、排放核算、能源结构类报告要「学术口径」的中国排放面板；CEADs 是国际论文中最常被引的中国碳数据源。
- 怎么取：清单页是**一张 101 行的表格**（列：No./Name/Year/Spatial Resolution/Temporal Resolution/Element/Energy Type/Industry Type/Search Tags/Published/Action），行本身用 `data-id` 标识，点击（页面脚本）打开新窗口 `/user/index.php?id=<id>&lang=en`。**取数需登录**：`/user/index.php?id=<id>` 会 302 到 `/user/login.php`（含算术验证码）。页面内三个 `*.php` 是匿名 JSON 辅助接口（分类树/联想/标签），**未单独实测**。
- 覆盖：中国 · 省级 / 城市级 (地市) / 县级 · 2000–2022（分省分部门 CO₂ 到 2022、城市工业过程 CO₂ 2000–2021）· 年度 · 47 个社会经济部门、17 类化石能源 + 水泥。
- 门槛：**免费注册**（登录后才能下载；学术使用，需遵守免责声明）。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA）——`https://www.ceads.net/` → 200；`/data/carbon-inventory/` → 200（52,852 B，表内 101 个 `data-id` 行）；`/data/inventory/` → **404**；`/public/js/custom.js` → 200（下载走 `window.open('/user/index.php?id='+id+'&lang='+lang)`）；`/user/index.php?id=2052&lang=en` → 302 → `/user/login.php`（200，算术验证码）。
- 上游：CEADs（Carbon Emission Accounts and Datasets，Shan Yuli / Guan Dabo / Liu Zhu）；联系人见登录页 `shanyuli@outlook.com`、`zhuliu@tsinghua.edu.cn`。

## 细节

- 表格里的「Action」列与「Name」列是同一套 `data-id`，下载/详情都走 `/user/index.php?id=<id>`，`lang=en|cn` 切换语言。
- 同一批数据的命名规律：`China Provincial Sectoral CO2 Emission Inventory (YYYY)` / `China Provincial Sectoral Energy Inventory (YYYY)`、`China City-Level ... CO2 Emission Inventory`；「Published」列是上架日期，不是数据年份。
- 站内还有 MEIC（清华多尺度排放清单）、GID（全球基础设施排放）、CHRED（企业排放）入口，多为单独站点/登录。

## 坑

1. 下载**必须登录**，`data-id` 拼不出直链；匿名只能看到清单目录与元数据（年份/空间/时间分辨率/能源与部门口径）。
2. `/data/inventory/` 是失效旧路径，正确是 `/data/carbon-inventory/`；站点导航与路由改版频繁，以首页 `/data` 为准。
3. 各数据集年份上限不一致（分省到 2022、城市级到 2021），引用前逐行看「Year」列，别默认「最新到 2025」。
4. 站点主体英文、子页有中文；`lang=cn` 走 `https://www.ceads.net` 前缀。请求建议 ≥1.5 s 间隔、桌面 UA。
