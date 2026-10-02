# cszg.mca.gov.cn —— 慈善组织信息公开与年报平台

- 去哪找：**慈善中国（民政部慈善信息公开平台）** `https://cszg.mca.gov.cn/`（首页 JS 跳转 `/platform/application.html`）；组织登录入口 `/platform/login.html`。
- 什么时候用：要**全国慈善组织（基金会/慈善会/社会服务机构）名录与年报**、**公开募捐方案备案/募捐资格**、**慈善项目与年度工作报告**；核查某组织是否具有公开募捐资格、是否按期年报。
- 怎么搜：**需组织账号登录**——未登录时全站 302 到 `/platform/login.html?service=%2Fj_spring_security_check&renew=true`；本次探测未发现匿名公开检索入口，`怎么搜` 实为「登录后站内查询」（若需匿名名录，改走 `../gov/chinanpo.md` 或本层 `foundationcenter.org.cn.md`）。
- 覆盖：民政部登记的**慈善组织**（含基金会）基本信息、公开募捐资格与募捐方案备案、慈善项目、年度工作报告（年报）；粒度=单组织 + 单条备案/年报；按组织报送/民政部门录入动态更新。
- 门槛：**需账号（组织账号）**；站点前置 WAF（响应头 `Server: WAF`，下发 `https_waf_cookie`）、`X-Frame-Options: SAMEORIGIN` 等安全头。
- 实测：2026-10-03，macOS arm64，curl 8.x（Chrome 126 桌面 UA，20 s 超时）——`GET https://cszg.mca.gov.cn/` → **200**，64 B，正文为 `<script>location.href="/platform/application.html"</script>`；`GET …/platform/application.html` → **302**，`Location: https://cszg.mca.gov.cn/platform/login.html?service=%2Fj_spring_security_check&renew=true`；响应头含 `Server: WAF`。
- 上游：中华人民共和国民政部 `https://www.mca.gov.cn/`；《慈善组织信息公开办法》（民政部令第 61 号）。

## 细节

- 民政部要求慈善组织在「慈善中国」公开的信息包括：组织基本信息、年度工作报告、公开募捐情况、慈善项目实施情况等（《慈善组织信息公开办法》）。平台前台即本域。
- 基金会年度**年报/年检**通知由民政部按年发布（如《关于开展民政部登记的慈善组织（基金会）2024 年度年报年检工作的函》，`mca.gov.cn/n152/n165/…`）。
- 第三方把本平台数据做了聚合呈现（如 `suchajun.com/shuju/cishanxinxi`），可当线索，正式引用回本域。

## 坑

1. **全站登录墙**：`/`、`/platform/application.html` 均跳转登录，未登录抓不到任何组织数据 → 引用请标注访问日期或用民政部公告补。
2. **WAF**：非浏览器 UA/高频访问会被拦；换正常桌面 UA 亦仅能拿到跳转壳。
3. 平台是**报送端**（组织填报），不是公开检索端；公开名录优先用 `../gov/chinanpo.md` 的信用信息公示平台。
