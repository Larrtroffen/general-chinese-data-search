# ilostat.ilo.org —— 国际劳工组织劳动统计

- 去哪找：门户 `https://ilostat.ilo.org/`；**数据接口** `https://rplumber.ilo.org/data/indicator/`；批量下载 `https://ilostat.ilo.org/data/bulk/`。
- 什么时候用：就业/失业、劳动参与、非正规就业、工资与劳动成本、工时、童工、社保覆盖、按性别/年龄/教育分解；要跨国可比劳动指标。
- 怎么搜：GET + JSON，无 key：
  ```bash
  # 单指标取数：id=指标码，ref_area=国家，timefrom/to，format=json
  curl -s 'https://rplumber.ilo.org/data/indicator/?id=UNE_TUNE_SEX_AGE_NB_A&ref_area=CHN&timefrom=2020&format=json'
  # → [{"ref_area":"CHN","source":"BA:16044","indicator":"UNE_TUNE_SEX_AGE_NB",
  #     "sex":"SEX_T","classif1":"AGE_YTHADULT_YGE15","time":"2022","obs_value":35120, ...}]
  ```
  - 主要参数：`id`（指标码，**末尾 `_A/_Q/_M` 是频率**）、`ref_area`（ISO3，多值 `CHN+USA`）、`timefrom`/`timeto`、`sex`、`classif1`、`format=json|csv`。
  - 指标/国家字典与 bulk 文件在 `https://ilostat.ilo.org/data/bulk/`（zip，免费）；元数据端点路径以官方文档为准（本机 `/metadata/indicator/?format=json` → 404）。
- 覆盖：180+ 国家/地区；劳动与体面工作全套指标；多数 1990s 起（部分 1969 起），年/季/月。
- 门槛：免费、**无 key、无注册**（bulk zip 亦免费）。
- 实测：2026-10-03，macOS arm64，curl 8.x：`/data/indicator/?id=UNE_TUNE_SEX_AGE_NB_A&ref_area=CHN&timefrom=2020&format=json` → 200 / 734 B，返回中国 2022 年 `obs_value=35120`（`SEX_T` 合计、`AGE_YTHADULT_YGE15`），并带 `note_*` 脚注码。
- 上游：`https://ilostat.ilo.org/`；`https://rplumber.ilo.org/`（上游声明）。

## 细节

### 指标码的构成

`{主题}_{细分}_{频率}`，例：`UNE_TUNE_SEX_AGE_NB_A` = 失业人数（Une）按性别/年龄（Tune=S 表示 sex+age），`_A` 为年度。查询时**要带频率后缀**。

## 坑

1. `id` 末尾 `_A/_Q/_M` 是频率，漏掉会 404。
2. `sex`/`classif1` 不筛会同时返回合计（`SEX_T`）与分组行。
3. 观测值的年份由 `time` 给，但**各国上报滞后不同**（中国最新常滞后 1–2 年）；做面板前查 `source`/`note_*`。
4. `rplumber.ilo.org` 是 R Plumber 服务，偶发 5xx，重试即可。
5. 数值单位随指标而异（千人 / 千小时 / % 等），取数必读指标元数据。
