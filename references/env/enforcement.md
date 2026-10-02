# 环境行政处罚与执法公示 —— 部省两级入口与检索

- 去哪找：生态环境部「执法制度与行政处罚」`https://www.mee.gov.cn/ywgz/sthjzf/zfzdyxzcf/`（父栏目「生态环境执法」`https://www.mee.gov.cn/ywgz/sthjzf/`）；部本级处罚决定书（核安全领域）直链形如 `https://www.mee.gov.cn/xxgk2018/xxgk/xxgk03/{YYYYMM}/t{YYYYMMDD}_{id}.html`；省级专栏与「企业环境信息依法披露系统」见「细节」表。
- 什么时候用：查**某企业/某地是否被环境行政处罚**、处罚决定书文号与裁量；写执法监管、典型案例、企业环保合规与 ESG 报告；配合 [`ipe.org.cn.md`](ipe.org.cn.md)（监管记录）、[`permit.mee.gov.cn.md`](permit.mee.gov.cn.md)（排污许可）、[`../gov/credit-china.md`](../gov/credit-china.md)（信用中国双公示）交叉核验。
- 怎么搜：**部级**列表是静态分页（`index.shtml` 为第 1 页，`index_1.shtml` 为第 2 页，`createPageHTML(22,…)` → 共 22 页），条目 HTML 直读；**省级**多为「栏目列表 + 站内搜索框」，江苏为表单式接口：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # 部级：执法制度与行政处罚（第 2 页）
  curl -s -A "$UA" 'https://www.mee.gov.cn/ywgz/sthjzf/zfzdyxzcf/index_1.shtml'
  # 江苏省级「双公示」行政处罚检索（q_GGTJ=行政相对人名称/决定书文号/法人代表）
  curl -s -A "$UA" -e 'http://ywxt.sthjt.jiangsu.gov.cn:9081/sgs/business/sgs/wzsgs/sgscontroller/sgsList' \
    -X POST -d 'q_GGTJ=环罚&P_CURRENT=1' \
    'http://ywxt.sthjt.jiangsu.gov.cn:9081/sgs/business/sgs/wzsgs/sgscontroller/sgsXzcfGsList'
  ```
  结果形态：部级与山东、湖北为 **HTML**；广东、浙江、江苏部分页面为 **JS 渲染**（需浏览器/XHR）。
- 覆盖：全国 · 部级列表 22 页（`index_1` 已见 2024-12 条目，上溯约 2015）· **核安全**行政处罚决定书按案逐篇；省级专栏年度不一（多为 2019 年后）· 企业级；企业环境信息依法披露自 2022-02-08《管理办法》施行后逐年。
- 门槛：部级与多数省级 **免费匿名**；湖北 **412 WAF**；广东/浙江列表 **JS（需浏览器）**；披露系统公开查询多匿名、企业填报需账号。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA，20s 超时）——`/ywgz/sthjzf/zfzdyxzcf/` → 200（45,820 B，标题「执法制度与行政处罚」，`createPageHTML(22,…)`）；`/ywgz/sthjzf/zfzdyxzcf/index_1.shtml` → 200（45,626 B，含「第二十三/二十四批生态环境执法典型案例」「核安全行政处罚决定书（甘肃东方瑞龙…）」等）；省级与披露系统逐条见「细节」。
- 上游：生态环境部（生态环境执法局·行政处罚与强制处）；各省生态环境厅（市县级处罚多在**市局**网站）。

## 细节

### 省级「行政处罚」专栏抽查（2026-10-03）

| 省份 | 专栏 URL | 列表形态 | 实测 |
|---|---|---|---|
| 山东 | `http://www.sdein.gov.cn/hjjc/xzcf/` | 静态 HTML 列表；含「行政处罚决定书（鲁环罚〔2025〕1号）」；典型案例部分外链微信公众号 | ✅ 200 |
| 广东 | `https://gdee.gd.gov.cn/bgtxzcf/index.html` | 栏目页 18 KB、无条目链接，列表 JS 渲染 | ⚠️ 仅浏览器 |
| 江苏 | `http://ywxt.sthjt.jiangsu.gov.cn:9081/sgs/business/sgs/wzsgs/sgscontroller/sgsXzcfGsList` | 省厅「双公示」表单页，`POST q_GGTJ=…` 检索；省本级常 0 条 | ✅ 200 |
| 浙江 | 厅站 `https://sthjt.zj.gov.cn/`（JS）；全省 `https://xzcf.zjzwfw.gov.cn/punishment` | 均为 Vue SPA，条目需浏览器 | ⚠️ 仅浏览器 |
| 湖北 | `https://sthjt.hubei.gov.cn/fbjd/xxgkml/cfqz/xzcfjd` | 静态列表（决定书标题 + 日期） | ❌ 412 WAF |

### 企业环境信息依法披露系统（各省自建，无全国统一入口）

| 省市 | 入口 | 形态/门槛 |
|---|---|---|
| 北京 | `https://hjxxpl.bevoice.com.cn:8002/` | SPA 首页（3.1 KB），公开查询 + 企业填报 |
| 上海 | `https://e2.sthj.sh.gov.cn/jsp/view/hjpl/index.jsp` | 6.2 KB，含滑块验证脚本 `longbow.slidercaptcha` |
| 浙江 | `https://mlzj.sthjt.zj.gov.cn/eps/index/enterprise-search` | Vue，按区域/企业检索披露名单 |

- 部级「政府信息公开」目录把处罚列入**「行政处罚和行政复议」**类；`/xxgk2018/xxgk/xxgk03/` 目录不可浏览（直链 200、目录 403/空），只能按文章 URL 取。
- 江苏双公示另有**省级信用专栏** `https://zwpt.da.jiangsu.gov.cn/datacenter/dc/sgslist`；许可类接口为 `sgsXzxkGsList?q_XKLX=WZSGS_XK01`，处罚为 `sgsXzcfGsList`。
- 生态环境部 6 个**督察局**（华北/华东/华南/西北/西南/东北）域名 `hbdc/hddc/hndc/xbdc/xndc/dbdc.mee.gov.cn`，另有流域海域监管局，均挂部站。

## 坑

1. **部本级只公开核安全处罚决定书**；一般环境行政处罚在**市/县生态环境局**网站（省本级常为空，如江苏 `sgsXzcfGsList` 匿名查询总记录 0）。
2. 省级专栏**无统一路径规律**：山东 `/hjjc/xzcf/`、广东 `/bgtxzcf/`、湖北 `/fbjd/xxgkml/cfqz/xzcfjd` 各不相同，须逐省找导航或站内检索。
3. 不少省级「典型案例」发布在**微信公众号**（山东列表直接外链 `mp.weixin.qq.com`），非站内可抓文本。
4. 广东/浙江列表由 JS 渲染、湖北为 **WAF 412**，脚本直取失败属正常，需浏览器会话。
5. 披露系统**一省一域名**，无 `.gov.cn` 统一前缀（北京在 `bevoice.com.cn`），别按域名猜；公开查询与企业填报入口不同。
6. 处罚决定书是单篇公文，**无结构化字段表**；要企业×违法类型×罚没金额面板需自行解析（或走 IPE/信用中国整合口径，且正式引用回链原公告）。
