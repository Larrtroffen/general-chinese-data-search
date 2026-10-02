# chinawuliu.com.cn —— 物流与 PMI 月度指数

- 去哪找：`http://www.chinawuliu.com.cn/`（中国物流与采购网）；联合会官网 `http://www.cflp.org.cn/`（实测与前者同标题同体积，同站）；统计数据 `/xsyj/tjsj/`
- 什么时候用：要 PMI（制造业/非制造业/综合）月度值、物流业景气指数、仓储指数、电商物流指数、公路运价指数、物流运行通报；写宏观景气与物流行业报告。
- 怎么搜：静态 shtml，按年月分目录：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  curl -sS -A "$UA" 'http://www.chinawuliu.com.cn/xsyj/tjsj/'                  # 列表（约 20 条/页）
  curl -sS -A "$UA" 'http://www.chinawuliu.com.cn/xsyj/202609/30/668954.shtml' # 2026-09 综合PMI
  ```
  结果形态：HTML 列表 + 正文；无 JSON API。
- 覆盖：PMI 系列月度（实测列表含 2026-09-30 综合 PMI 50.7）；物流业景气 / 仓储 / 电商物流 / 公路运价指数月度；年度全国物流运行通报。
- 门槛：免费、无需登录；http 必需。
- 实测：2026-10-03 `http://www.chinawuliu.com.cn/` → 200，44 KB，title「中国物流与采购网」；`/xsyj/tjsj/` → 200，22.8 KB，最新「2026年9月份综合PMI产出指数为50.7%」✅；`http://www.cflp.org.cn/` → 200，44 KB，同标题（同站）。
- 上游：中国物流与采购联合会。

## 细节

- 联合会数据实际生产方是**中国物流信息中心**（见 `clic.org.cn.md`）：要指数分类归档与直报系统入口去那张卡。

## 坑

1. `https://www.chinawuliu.com.cn/` 证书主机名不匹配（`SSL: no alternative certificate subject name matches`）→ 用 http。
2. 「统计数据」列表只翻出约 20 条，查历史要走 `/{栏目}/YYYYMM/DD/{id}.shtml` 规律或站内检索。
3. PMI 定稿口径由国家统计局与中国物流与采购联合会**联合发布**，媒体转载值可能被改写；引用记发布日。
