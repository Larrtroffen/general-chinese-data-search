# national-data-corpus —— 年鉴指标 CSV 语料仓

把《中国统计年鉴》「年度数据」全部指标抓成 CSV 的**离线语料库**：`data/zb/<27 个年鉴大类>/<指标>.csv`，一个指标一个文件、一行一年。**没有 API，就是 raw 单文件直取**——适合做历史长表、口径沿革对照、离线跑批。

- 去哪找：`https://github.com/yiyuezhuo/National-Data`；raw 基址 `https://raw.githubusercontent.com/yiyuezhuo/National-Data/master/`。
- 什么时候用：要**1978–2014 年的年度指标历史值**且不想逐次打 NBS 接口；要做「指标名 → 历年数值」的本地底表；要按年鉴章节名（人口/国民经济核算/财政…）批量取一组指标时。
- 怎么取（raw 路径模板，注意中文需 URL 编码）：
  ```bash
  RAW=https://raw.githubusercontent.com/yiyuezhuo/National-Data/master
  # 指标清单树（JSON/文本，673040 B）：$RAW/tree
  # 单指标 CSV：$RAW/data/zb/<大类>/<指标>.csv
  curl -s "$RAW/data/zb/%E4%BA%BA%E5%8F%A3/%E6%80%BB%E4%BA%BA%E5%8F%A3.csv"   # data/zb/人口/总人口.csv
  # 整仓（含 1852 个 CSV）：
  git clone --depth 1 https://github.com/yiyuezhuo/National-Data /tmp/National-Data
  ```
- 覆盖：**年度数据 1978–2014**（README：网站上「所有」指标；2016 可由脚本现抓）；不含分省/月度。编码 UTF-8 无 BOM。
- 门槛：公共 GitHub raw；**仓库无 LICENSE**（仅作检索线索/自查用，勿整仓再分发）。
- 实测：2026-10-02，macOS arm64：`curl -o /dev/null -w '%{http_code} %{size_download}' "$RAW/data/zb/人口/总人口.csv"` → **200 / 1509 B**；`gh api …/git/trees/master?recursive=1` → `*.csv` 计数 = **1852**、一级类 = **27**、`tree` 文件 = 673040 B；`gh api repos/yiyuezhuo/National-Data` → `license.spdx_id = null`（**无许可**）。
- 上游：https://github.com/yiyuezhuo/National-Data （无 license；数据止于 2014/2016）。

## 细节

### 结构 / 粒度

`data/zb/` 下 **27 个一级类**，与年鉴章名一致：人口、国民经济核算、就业人员和工资、固定资产投资和房地产、对外经济贸易、能源、财政、价格指数、人民生活、城市概况、资源和环境、农业、工业、建筑业、运输和邮电、批发和零售业、住宿和餐饮业、金融业、科技、教育、卫生、社会服务、文化、体育、旅游业、公共管理·社会保障及其他、综合。

- 共 **1852 个 CSV**；每个 CSV：**首列 `1978年`… 年份行，表头为该指标下的分项名**。

### CSV 样例（`data/zb/人口/总人口.csv`，首行 + 两行）

```
,乡村人口,城镇人口,女性人口,年末总人口,男性人口
1978年,79014,17245,46692,96259,49567
1979年,79047,18495,47350,97542,50192
```

### 限制

① **停更**（最后推送 2020-12），数据止于 2014/2016，**不要当“最新数据”用**；② **无 LICENSE**（仓库未声明许可，只可作检索线索/自查用，勿整仓再分发）；③ 附带的 `main.py` 是 2016 年写的、打**旧的 `easyquery.htm`**（现 403），脚本已失效，CSV 才是价值所在；④ Excel 打开无 BOM UTF-8 中文可能乱码 → 仓库自带 `convert_to_gbk.py <src> <dest>` 转 GBK；⑤ 表格为「年鉴印刷口径」，与 NBS 新版 API 数值可能因修订略有出入。
