# safe.gov.cn —— 外汇储备与国际收支数据

- 去哪找：门户 `https://www.safe.gov.cn/`；**统计数据** `https://www.safe.gov.cn/safe/tjsj1/index.html`；各专题 `https://www.safe.gov.cn/safe/{slug}/index.html`（见下表）。
- 什么时候用：要**外汇局口径**的外汇储备/官方储备资产、国际收支平衡表（BPM6 时间序列）、国际投资头寸表、全口径外债、货物和服务贸易、银行结售汇、银行代客涉外收付款、人民币汇率中间价、各种货币对美元折算率、中国外汇市场交易概况。
- 怎么搜：两层。① 门户导航「统计数据」下拉 → 各专题页；② 专题页（如「国际收支平衡表时间序列(BPM6)」）正文给 **xlsx 直链**，形如 `https://www.safe.gov.cn/safe/file/file/{YYYYMMDD}/{32位md5}.xlsx`；「外汇储备」页按年列「官方储备资产」「国际储备与外币流动性数据模板」，点进文章页再取附件。另有「统计数据跨表查询」`/safe/tjsjkbcx/index.html`。结果形态：HTML 列表 → 文章页 → xlsx 附件。
- 覆盖：国际收支平衡表 BPM6 时间序列（另含 1982–2014 的 BPM5 旧口径）、外汇储备与官方储备资产（2015-06 起，逐年/逐月）、外债（2014-12 末以来时间序列）、货物和服务贸易（2015 起，月度）；全国口径。
- 门槛：无。
- 实测：2026-10-03，桌面 UA curl——`GET https://www.safe.gov.cn/` `200/102,315 B`；`GET /safe/tjsj1/index.html` `200/23,698 B`；`GET /safe/zggjszphb/index.html` `200/19,087 B`；`GET /safe/whcb/index.html` `200/23,598 B`；`GET /safe/rmbhlzjj/index.html` `200/16,020 B`；`GET /safe/2019/0627/13519.html`（国际收支平衡表时间序列 BPM6）`200/15,944 B`，正文含 `https://www.safe.gov.cn/safe/file/file/20260929/6674650e17de4f20a45c64610118a96f.xlsx`（仅解析链接，未下载本体）。`/safe/whcbsj/index.html` 为 `404`（下拉无此 slug，别猜）。
- 上游：`https://www.safe.gov.cn/`（国家外汇管理局）。

## 细节

### 统计数据专题 slug（首页「统计数据」下拉，2026-10-03 实测）

| slug | 栏目 |
|---|---|
| `tjsjkbcx` | 统计数据跨表查询 |
| `zggjszphb` | 中国国际收支平衡表（含 BPM6 时间序列） |
| `zggjtztcb` | 中国国际投资头寸表 |
| `zghyhfwmy` | 中国货物和服务贸易 |
| `zgdwzqtzzcfgjdq` | 中国对外证券投资资产 |
| `zgyhydwjrzcfz` | 中国银行业对外金融资产负债 |
| `yhjsh` | 银行结售汇 |
| `yhdkswsfk` | 银行代客涉外收付款 |
| `jrjgzjtz` | 金融机构直接投资 |
| `whcb` | 外汇储备（官方储备资产 / 国际储备与外币流动性数据模板） |
| `gzhbdmyzslb` | 各种货币对美元折算率表 |
| `rmbhlzjj` | 人民币汇率中间价 |
| `zgwhscjygk` | 中国外汇市场交易概况数据 |
| `zgwz` | 中国外债 |
| `zgcqydqwzdjghzz` | 中国长期与短期外债的结构和增长 |
| `zgwzygmjjwhsr` | 中国外债与国民经济、外汇收入 |
| `zgwzldygmjjwhsr` | 中国外债流动与国民经济、外汇收入 |
| `sjbz` | 数据标准 |

### 常用文章页（时间序列类）

| 数据 | 文章页 |
|---|---|
| 国际收支平衡表时间序列（BPM6） | `/safe/2019/0627/13519.html` |
| 国际收支平衡表时间序列 1982–2014（BPM5） | `/safe/2015/0630/3269.html` |
| 货物和服务贸易数据（BPM6，2015 以后） | `/safe/2018/0427/8886.html` |
| 全口径外债情况表时间序列（2014-12 末以来） | `/safe/2018/0329/8810.html` |

- 附件命名：`/safe/file/file/{YYYYMMDD}/{md5}.xlsx`（日期=上传日，md5=文件指纹，均不可猜）。

## 坑

1. **附件路径含 md5**，无法按规律拼；必须解析文章页 HTML。
2. slug **不能猜**：`whcb`（外汇储备）有效，`whcbsj` 直接 `404`；一律从门户下拉枚举。
3. 「统计数据列表」`/safe/zggjszphb/index.html` 是 BPM6 与 BPM5 两个入口的列表，不直接含 xlsx，要再点一层。
4. 汇率类：人民币汇率中间价、各种货币对美元折算率在 SAFE；**CFETS 人民币汇率指数、Shibor** 在中国货币网（`../business/chinamoney.com.cn.md`），两边口径不同别混用。
5. 外债页有 4 个近义专题（`zgwz` / `zgcqydqwzdjghzz` / `zgwzygmjjwhsr` / `zgwzldygmjjwhsr`），按「全口径 vs 结构 vs 与国民经济关系」选，别只取一个。
6. 全口径外债与「中国银行业对外金融资产负债」（`zgyhydwjrzcfz`）是两个表，前者是经济体对外债务、后者是银行部门对外头寸。
