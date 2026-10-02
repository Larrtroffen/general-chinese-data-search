# clic.org.cn —— 物流与 PMI 指数源站

- 去哪找：`http://www.clic.org.cn/`；数据列表 `/data_list.html?code={pmi|logistics|production|logistics_modern}&category=<32位hex>`；详情 `/data_detail/{hash}.html?rid={hash}`
- 什么时候用：要 PMI 与物流指数的**分类归档**（钢铁 PMI、国际/全球 PMI、运价/景气/仓储/电商/快递物流指数、大宗商品指数、生产资料），或找联合会各直报系统入口时。
- 怎么搜：URL 参数直取（`code` 为栏目、`category` 为子类哈希；哈希只能从页面抓）：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  curl -sS -A "$UA" 'http://www.clic.org.cn/data_list.html?code=pmi'
  curl -sS -A "$UA" 'http://www.clic.org.cn/data_list.html?code=logistics&category=98a77404401d4f969b8a1f56ad13dd40'   # 景气指数
  ```
  结果形态：HTML 列表 + 详情页；无 JSON API。
- 覆盖：PMI 及物流/仓储/电商/运价指数月度（实测有 2026-09 期），生产资料大宗商品指数，经济信息周报。
- 门槛：浏览免费；**直报系统需账号**——`pmi.clic.org.cn:9001/netrep/login.jsp`（PMI 调查）、`wltj.clic.org.cn`（全国社会物流统计）、`wljq.clic.org.cn`（物流业景气指数）、`cc.clic.org.cn`（仓储指数调查）、`124.205.112.46:7002/netrep`（生产资料行业统计）。
- 实测：2026-10-03 `http://www.clic.org.cn/` → 200，41 KB，title「中国物流信息中心」；首页实测列出「9月份制造业PMI为50.1%」「2026年9月份中国非制造业商务活动指数为50.2%」及全套 `code/category` 链接 ✅。
- 上游：中国物流信息中心（中国物流与采购联合会直属）。

## 细节

### code / category 对照（实测自首页）
| code | 子类 |
|---|---|
| `pmi` | 制造业PMI / 非制造业PMI / 综合PMI / PMI英文 / 国际PMI / 全球PMI / PMI分析 / 钢铁PMI |
| `logistics` | 运价指数 / 景气指数 / 仓储指数 / 电商物流指数 / 快递物流指数 / 运行分析 / 形势分析 / 50强 |
| `production` | 大宗商品指数 / 价格评述 / 市场综述 |
| `logistics_modern` | 仓储 / 危化品 / 冷链 / 电商 / 跨境 / 供应链 |
| `logistics_technology` | 物流科技奖 / 科技动态 / 获奖展示 / 信息化 / 国际 |
| `logistics_comprehensive` | 行业动态 / 地方 / 企业 / 产业动态 / 政策 / 标准 |

## 坑

1. `category` 是 32 位 hex、无规律，**必须从首页或列表页抓**；`data_list.html?code=xxx` 不带 `category` 时是栏目首页。
2. 直报系统在内网/独立端口（`10.200.x`），公网不可达；`netrep` 系入口需机构账号。
3. 详情页 URL 带 `rid` 参数，去掉可能 404。
