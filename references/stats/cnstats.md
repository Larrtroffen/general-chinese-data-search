# cnstats —— 国家统计局取数 Python 包与 CLI

一个封装国家统计局数据的 Python 包与命令行工具（`cnstats`）。**增量价值：它把「旧 `easyquery.htm`」的 `dbcode` 命名法（hgyd/fsyd/csyd…）与指标代码层级讲得清楚，可作为新接口的「语义字典」；但它本身仍打旧接口，现已全站 403，不能直接用。**

- 去哪找：`https://github.com/songjian/cnstats`；PyPI `cn-stats`（v0.1.3）；核心源码 `cnstats/common.py`、`cnstats/stats.py`、`cnstats/regcode.py`、`cnstats/zbcode.py`。
- 什么时候用：需要**旧口径的指标代码体系**（`A010101` 货币供应量、`A01010B` 2021 后分省口径）或 `dbcode` 与库的对应关系时；要给新接口的 `code`（1–14）找语义参照时。取数本身请走 `data.stats.gov.cn.md` 的新接口。
- 怎么取（若坚持用）：
  ```bash
  uv add cn-stats   # 或 pip install cn-stats
  uv run cnstats A0D01 202201                       # 宏观月度：2022-01 货币供应量
  uv run cnstats A01010B01 202112,202201 --regcode 110000   # 分省月度
  uv run cnstats A0101 --tree --dbcode fsyd         # 下钻指标树
  uv run cnstats --list-regcode --dbcode csnd       # 列主要城市地区代码
  ```
  Python：`from cnstats.stats import stats; stats(zbcode='A010101', datestr='202201', regcode='370200', dbcode='csyd', as_df=True)`
- 覆盖：NBS 的宏观/分省/城市 月·季·年指标（数据源 `stats.gov.cn` / `data.stats.gov.cn`）；输出 list 或 pandas DataFrame（`as_df=True`）。
- 门槛：MIT 开源；但所打旧接口已全站 403，包当前实质不可用，仅作语义字典。
- 实测：2026-10-02，macOS arm64，curl 8.x：`curl 'https://data.stats.gov.cn/easyquery.htm?cn=A01'` → **403**（页含 `reason:UrlACL`、`Client IP: …`）。**未安装/未运行该包**（只读研究，不执行第三方代码）；源码结论来自 `main` 分支文件通读。
- 上游：https://github.com/songjian/cnstats （PyPI `cn-stats`）。

## 细节

### regcode / zbcode 映射表到底怎么来（本任务关键）

**不是内置静态表**，而是运行时从接口取：

- `cnstats/regcode.py::get_reg()` → `easyquery(m='QueryData', dbcode, rowcode='reg', wds=[{"wdcode":"zb","valuecode":"A01010101"}])`，读返回 `returndata.wdnodes[1].nodes`（每项 `{code,name}`）。
- `cnstats/zbcode.py::get_tree()` → 递归 `easyquery(m='getTree', dbcode, wdcode='zb', id=...)`，靠返回节点的 `isParent` 下钻。
- 结论：代码-名称映射**随接口元数据走**，没有可离线复用的映射文件；新接口同理用 `queryIndexTreeAsync` + `queryIndicatorsByCid` 现场取，见 `data.stats.gov.cn.md`。

### dbcode 语义

README 表（映射新站库码 1–8）：`hgyd` 宏观月度、`hgjd` 宏观季度、`hgnd` 宏观年度、`fsyd` 分省月度、`fsjd` 分省季度、`fsnd` 分省年度、`csyd` 城市月度、`csjd` 城市季度、`csnd` 城市年度。

### 版本/演进

v0.1.3(2026-03-03) 新增 `as_df`；v0.1.2 修复 `--regcode` 未传 `wds` 导致地区过滤失效、按 `wdcode` 动态对齐列；`--tree [zbcode]` 支持下钻子类。CLI 输出用 `tabulate`+`wcwidth` 排版成表格。

### 指标代码命名空间（旧口径，可作新接口语义参照）

`A0D01` 货币供应量、`A010101` 居民消费价格、`A01010B*` 为 **2021 及以后**的分省口径（README 特别提示用错会得空结果）。

### 额外可用物

`tests/cassettes/*.yaml` 是旧接口的真实响应录像（vcrpy），可离线研究 `getTree` / `QueryData` 的返回结构（`returndata.wdnodes`、`datanodes`），对理解新接口的 `values[]._id/i_showname/du_name` 有帮助。

## 坑

1. 打的是 **`https://data.stats.gov.cn/easyquery.htm`**，**该域名现全站 403（UrlACL）**，故包当前基本失效。
2. 需自备 `requests`/`pandas`/`urllib3<2`。
3. `tests/cassettes/*.yaml` 是旧接口的录制响应，可读但过时。
