# data_location —— 省市县与乡镇街道静态 JSON 名录

passer-by.com 整理的行政区划代码 JSON 库（GB/T 2260），**host 在 GitHub 上、可直接 raw 取单文件**：省级/地级/县级用一个大 flat map，乡级（街道/镇/乡）按区县拆成 3000+ 个小文件。**我们只取「入口 + 命名规则」，不整仓搬运。**

- 去哪找：`https://github.com/mumuy/data_location`；演示站 `https://passer-by.com/data_location/`；raw 基址 `https://raw.githubusercontent.com/mumuy/data_location/master/`。
- 什么时候用：要**离线/可缓存的省市县或乡镇街道代码-名称对照**、又不想走民政部 `dmfw` 接口时；做单位/地名归一化、给检索命中反查「街道属于哪个区县」时。
- 怎么取（raw 路径模板，实测 200）：
  ```bash
  RAW=https://raw.githubusercontent.com/mumuy/data_location/master
  curl -s $RAW/list.json        # 省(XX0000)+地(XXXX00)+县(XXXXXX) 的 {"代码":"名称"} 大表，78775 B
  curl -s $RAW/list2.json       # 同上另一种排序/用途的 省市县 大表
  curl -s $RAW/code/110101.json # 单区县的【乡级】名录：{"110101001":"东华门街道", …}，505 B
  curl -s $RAW/history.json     # 含历史代码（有 110103 崇文区、110110 燕山区 等已撤代码）
  curl -s $RAW/diff.json        # 旧代码 -> 现代码 的归并映射（如 "110103":["110101"]）
  curl -s $RAW/list.jsonp       # 带回调的 JSONP 版（给前端直连用）
  curl -s $RAW/version.js       # document.write('2026年4月')，前端展示的版本戳
  ```
- 覆盖：**省/市/县**（`list.json` 更新至 2026-04）；**乡级**按区县分散，`code/` 目录共 **3216 个文件**，最后更新 **2026-09-29**；港澳台编码为自定义（非国标）。
- 门槛：MIT（Copyright 2024 Haole Zheng）；raw 直取，无需登录。
- 实测：2026-10-02，macOS arm64，curl 8.x（**仅用 `gh api`/raw 单文件抓取，未克隆整仓、未下全量 JSON**）：`list.json` → 200/78775 B、`list.jsonp` → 200/78792 B；`code/110101.json` → 200/505 B（17 条乡级）；`gh api …trees/master?recursive=1` → `code/` 下 blob 数 = **3216**；`commits?path=code` 最新提交 2026-09-29；`LICENSE` = MIT。
- 上游：https://github.com/mumuy/data_location （MIT；raw 基址内含 `master` 分支）。

## 细节

### 目录/文件命名

仓库根平铺 `list.json` / `list2.json` / `history.json` / `diff.json` / `list.jsonp` / `version.js` / `index.html`；`code/` 下一个 6 位区县码一个文件（`code/<XXXXXX>.json`）；另有 `static/`（仅页面素材 image/script/style，无数据）、`LICENSE`、`README.md`。

### 代码区段规则（README 明列，可校验取到的码是否合规范）

地级 `XX0100-XX2000`/`XX5100-XX7000` 为地级市，`XX2100-XX5000` 为地区/自治州；县级 `XXXX01-XXXX50` 市辖区/省直管县级市、`XXXX51-XXXX80` 县/自治县、`XXXX81-XXXX99` 地级市代管县级市、`XX90XX` 省直管县级单位。

### 浏览入口

`index.html`（仓库根）是演示页，可直接在 GitHub Pages/演示站按省市区三级联动查；查「某区县有哪些街道」时最快是打开演示站再拼 raw。

### 用法提示

`history.json` 含已撤销代码（崇文 110103、宣武 110104、燕山 110110…），做**跨年对比**时必须用它而非 `list.json`；`diff.json` 是「旧码→新码数组」的归并表，适合把老数据对齐到现行区划。

### 限制

① **非官方整理**，正式引用口径建议标注「整理自民政部/国家统计局」或直接回 `mca.gov.cn.md`；② 行政管理区（开发区/高新区/新区等）不收录；③ 乡级「文件覆盖式更新」——同一区县换版是覆盖同名文件，历史乡镇名要靠 `history.json`/`diff.json`，不在 `code/` 内；④ 无「一区一文件」目录树，需按区县码拼 URL（不能直接按省枚举）。

### 实测明细（2026-10-02，macOS arm64，curl 8.x）

- `curl $RAW/list.json` → 200 / 78775 B；`list.jsonp` → 200 / 78792 B。
- `curl $RAW/code/110101.json` → 200 / 505 B，内容为 `{"110101001":"东华门街道",…,"110101017":"永定门外街道"}`（17 条乡级）。
- `gh api repos/mumuy/data_location/git/trees/master?recursive=1` → 统计 `code/` 下 blob 数 = **3216**；`commits?path=code` 最新提交时间 2026-09-29。
- 许可：仓库 `LICENSE` = **MIT**（Copyright 2024 Haole Zheng）。
