# akshare —— 中国宏观 / 金融数据总库

Python 金融数据总库，2.2 万星、更新极勤（2026-09 仍在推）。**与统计层直接相关的增量：它的 `macro_china_nbs_nation/region` 已改用 NBS 新站 `external` 接口**，是一份「新接口的标准实现参考」；其余宏观函数走金十/东财等第三方源，注意别与 NBS 官方口径混用。

- 去哪找：`https://github.com/akfamily/akshare`；文档 `https://akshare.akfamily.xyz/`；接口总检索 `https://akshare.akfamily.xyz/registry.html`；宏观文档 `https://akshare.akfamily.xyz/data/macro/macro.html`（源文件 `docs/data/macro/macro.md`）。
- 什么时候用：要**一批现成的中国宏观指标**（GDP/CPI/PMI/M2/社融…）或**股票/期货/基金行情**，且能接受「非 NBS 直连源」时；或想抄它的 NBS 新接口调用方式（会话预热 + 树/指标/取数三步）自己实现时。
- 怎么取（只读参考；本项目未安装）：
  ```bash
  pip install akshare           # 官方安装方式（我们未执行）
  ```
  ```python
  import akshare as ak
  # NBS 官方新接口（对应新站，kind 决定库、path 用 " > " 连接目录）
  ak.macro_china_nbs_nation(kind="年度数据", path="人口 > 总人口", period="LAST5")
  ak.macro_china_nbs_region(kind="分省季度数据", path="国民经济核算 > 地区生产总值",
                            period="last3", indicator=None, region="河北省")
  ak.macro_china_nbs_region(kind="分省季度数据", path="人民生活 > 居民人均可支配收入",
                            indicator='居民人均可支配收入_累计值(元)', period="2022")
  ```
- 覆盖：全国月/季/年 + 分省 + 主要城市 + 港澳台（NBS 口径），另有大宗行情/股票/基金/期货等；输出 pandas DataFrame。
- 门槛：开源免费（MIT）；本项目未安装、未运行，仅作只读参考。
- 实测：2026-10-02，macOS arm64：**只读**——用 `raw.githubusercontent.com` 抓取 `README.md`、`akshare/economic/macro_china_nbs.py`、`docs/data/macro/macro.md` 通读，并用 `gh api .../git/trees/main?recursive=1` 定位模块；**未安装 akshare、未运行其函数**。源码确认它是调 `…/dg/website/publicrelease/web/external/…` 新端点（非已 403 的 easyquery）。
- 上游：https://github.com/akfamily/akshare （MIT；文档 akshare.akfamily.xyz）。

## 细节

### NBS 相关接口（`akshare/economic/macro_china_nbs.py`）

`macro_china_nbs_nation`、`macro_china_nbs_region`。

- `kind` 取值 = 新站库名，内部映射 `{“月度数据”:1, “季度数据”:2, “年度数据”:3, “分省月度数据”:4, “分省季度数据”:5, “分省年度数据”:6, “主要城市月度价格”:7, “主要城市年度数据”:8, “港澳台月度数据”:9, “港澳台年度数据”:10}`，与 `data.stats.gov.cn.md` 的 `code` 一一对应。
- `path` 是**中文目录路径**，多级用 ` > ` 连接（如 `国民经济核算 > 支出法国内生产总值`），内部靠 `queryIndexTreeAsync` 逐级 resolve 出 `cid`/`rootId`。
- `period`：年 `2012,2013`／季 `2012A,2012B`／月 `201201`／至今 `2013-`／最近 `last10`；内部转成新站 `dts`（如 `2020YY-2024YY`）。
- 实现细节：用 `curl_cffi` + `impersonate="chrome"` 起会话，**先 GET 一次新站页面预热**，再带 `Origin/Referer` 调接口——比裸 curl 更“像浏览器”，可作反爬兜底参考。

### 检索接口用哪条

- 官方接口总表 `https://akshare.akfamily.xyz/registry.html`（按中文关键词/接口名搜），宏观类在 `https://akshare.akfamily.xyz/data/macro/macro.html`。

### 版本线索

- `akshare/__init__.py` 内 changelog：`macro_china_nbs_nation` 于 **1.10.94** 加入，**1.14.22/1.14.23** 连续修复；说明该组接口仍较新、遇到异常先升级 akshare 再报错。

### 限制

① 包体大、依赖多（curl_cffi/pandas…），且行情类接口随第三方站改版常坏（changelog 里大量 `fix:`）；② 与 NBS 无关的宏观函数（`macro_china_gdp*`/`macro_china_cpi` 走**金十数据中心**、`macro_cnbs` 走**国家金融与发展实验室 CNBS** 的杠杆率，**不是国家统计局**）——引用时务必区分口径；③ 无内置缓存、无频控保障。
