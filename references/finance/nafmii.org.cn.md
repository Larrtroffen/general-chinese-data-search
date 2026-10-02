# nafmii.org.cn —— 债务融资工具市场统计

- 去哪找：门户 `https://www.nafmii.org.cn/`；数据栏目 `https://www.nafmii.org.cn/sjtj/`；主承分类统计 `https://www.nafmii.org.cn/sjtj/zcfltj/`；信用风险缓释凭证 `https://www.nafmii.org.cn/sjtj/crmwct/`。
- 什么时候用：要**交易商协会口径**的银行间**债务融资工具**发行/承销统计——业务量统计、主承销商分类统计、信用风险缓释工具（CRMW）创设统计、CDS 指数披露、会员/主承名单。
- 怎么搜：CMS 栏目两层（`/sjtj/{子栏目}/{YYYYMM}/P0{时间戳}.pdf`）。`/sjtj/` 本身是导航壳（9.5 KB），条目由各子栏目列表与首页渲染；直接在首页/子栏目页解析 **PDF 直链**即可。
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  curl -s -A "$UA" 'https://www.nafmii.org.cn/' | grep -oE 'href="[^"]*\.pdf"'
  ```
  结果形态：HTML 列表 + PDF 附件（**无 JSON 接口**）。
- 覆盖：债务融资工具（中票/短融/超短融/PPN/ABN 等）发行量与主承分类统计、CRMW/CDS 创设统计、CDS 指数；月度；银行间市场口径。
- 门槛：无。
- 实测：2026-10-03，桌面 UA curl——`GET https://www.nafmii.org.cn/` `200/195,138 B`；`GET /sjtj/` `200/9,480 B`（导航壳）；首页已见 PDF 直链 `…/sjtj/zcfltj/202609/P020260928630841530689.pdf`（2026 年 1–8 月债务融资工具主承分类统计）、`…/sjtj/crmwct/202609/P020260929646796770278.pdf`（2026 年 1–8 月信用风险缓释凭证创设统计）、`…/xhdt/202609/P020260928631310847205.pdf`（2026 年 8 月债务融资工具业务量统计）。
- 上游：`https://www.nafmii.org.cn/`（中国银行间市场交易商协会）。

## 细节

### 栏目与数据

| 栏目 | URL |
|---|---|
| 数据（总） | `/sjtj/` |
| 主承分类统计 | `/sjtj/zcfltj/` |
| 信用风险缓释凭证创设统计 | `/sjtj/crmwct/` |
| 业务运行情况 | `/cpxl/xyfxhsgjcrm/ywyyqk/` |
| CDS 指数披露 | `/xxpl/crmxxpl/cdszspl/` |
| 会员总名单 | `/hyfw/hyflmd/hyzmd/` |
| 协会年报 | `/ljxh/xhjs/xhnb/` |
| 市场研究与分析 | `/yj/scyjyfx/` |

- 附件规律：`/{栏目}/{YYYYMM}/P0{20位时间戳}.pdf`（时间戳不可猜，从列表页解析）。
- 统计口径：业务量统计=发行规模/只数；主承分类统计=按承销商排名；CRMW 创设统计=缓释凭证创设规模。

## 坑

1. `/sjtj/` 页面**本身不含条目**（导航壳），别以它为空判断无数据——条目在首页与各子栏目列表页。
2. **只有 PDF，没有 JSON/Excel 接口**；需要结构化数字时自行解析 PDF（见 `../tools/mineru.md`）。
3. 「业务量统计」PDF 有时发在**协会动态**（`/xhdt/`）而非 `/sjtj/`，抓取时两处都扫。
4. 交易商协会=**承销/发行统计**；上清所=**清算/托管与信息披露**（`shclearing.com.cn.md`）；中债=**登记托管与收益率曲线**（`../business/chinabond.com.cn.md`）。三者口径不同别互换。
