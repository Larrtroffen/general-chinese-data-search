# sky.zj.gov.cn —— 浙江省社会科学院

- 去哪找：`https://sky.zj.gov.cn/`；科研成果展示厅 `https://sky.zj.gov.cn/file/newcms/kycgzst/Main.html`。
- 什么时候用：要浙江省级社科的机构/专家/成果线索；做浙江地方治理、经济、文化研究。
- 怎么搜：JSP 栏目制，页面用 `dictCode` 标识（`/web/page.jsp?dictCode=NNN`；智库成果 `group=020&dictCode=020001`；专家 `group=011&dictCode=0011003`）；「科研成果展示厅」是独立 SPA。
- 覆盖：浙江社科院本院概况、专家、成果、学科；**无独立数据库/数据中心**。
- 门槛：免费、免登录。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA：`https://sky.zj.gov.cn/` → 200（16,813 B，`<title>浙江省社会科学院`，导航为 `/web/page.jsp?dictCode=…`）；`https://sky.zj.gov.cn/file/newcms/kycgzst/Main.html` → 200（6,321 B，无标题，SPA 壳）。
- 上游：`https://sky.zj.gov.cn/`（浙江省社会科学院）。

## 细节

- 浙江省的「社科专家库 / 大成集智系统」更多挂在**浙江省社科联** `www.zjskw.gov.cn`（《浙江省社科专家库管理办法（试行）》，上游声明，未本机实测）。
- 站内技术支持为第三方 CMS，页面参数以 `dictCode` 为主。

## 坑

1. 首页导航**不是 REST/HAL 链接**，`dictCode` 是任意数字编码，换栏目要回首页读链接，别猜。
2. 「科研成果展示厅」是 SPA，curl 只拿壳；成果正文需 JS。
3. 该院**没有**面向公众的数据集下载，别把「智库成果」当数据平台。
