# eia —— 建设项目环评公示与全本 PDF

> 本卡指**环境影响评价（环评）**，勿与 [`eia.gov.md`](eia.gov.md)（美国能源信息署）混淆。

- 去哪找：
  - 生态环境部（部批项目，静态栏目）：受理 `https://www.mee.gov.cn/ywgz/hjyxpj/jsxmhjyxpj/xmslqk/`、拟审查 `https://www.mee.gov.cn/ywgz/hjyxpj/jsxmhjyxpj/nscxmgs/`、已批准 `https://www.mee.gov.cn/ywgz/hjyxpj/jsxmhjyxpj/ypzxmgg/`。
  - 第三方公示平台（匿名可搜，附件为报告书**全本**）：
    - 环评云·环境信息公示平台 `https://www.eiacloud.com/gs/`（`/gs/list/1` 环评报告、`/gs/list/3` 公众参与、`/gs/list/14` 审批前、`/gs/list/2` 验收、`/gs/list/4` 水保验收、`/gs/list/11` 清洁生产、`/gs/list/5` 土壤地下水、`/gs/list/10` 环境信息披露）。
    - 环境信息公示网 `http://hjxxgs.com/`（`/eia/`、`/shenpigonggao/`、`/shuitubaochi/`、`/wenping/`、`/jieneng/`）。
  - 北京（审批结果查询）：`https://gzcx.sthjj.beijing.gov.cn/eportal/ui?pageId=132186`（一般建设项目·已受理）/ `132292`（拟审查）/ `132296`（已审查）/ `134007`（备案结果）/ `135037`（核与辐射类）；对应入口在 `https://sthjj.beijing.gov.cn/bjhrb/index/xxgk69/zfxxgk43/fdzdgknr2/1718108/index.html`（双公示信息）。
  - 北京（文章式公告）：`https://sthjj.beijing.gov.cn/bjhrb/index/xxgk69/zfxxgk43/fdzdgknr2/325924085/`（通知公告），如 `…/325924085/1739291/index.html`。
  - 其他行业公示：水利部受理 `http://www.mwr.gov.cn/fw/slgs/`、审批公告 `http://www.mwr.gov.cn/fw/spgg/`（水土保持方案 / 洪水影响评价）；北京市水务局 `https://swj.beijing.gov.cn/swdt/ztzl/scjsxmstbcsszzysbbxxgs/index.html`（水保验收报备）；北京市发改委 `https://fgw.beijing.gov.cn/fzggzl/yfxz/xzxk_sgs/`（项目核准批复，含节能相关）。
  - 配套：排污许可 [`permit.mee.gov.cn.md`](permit.mee.gov.cn.md)、处罚与信息披露 [`enforcement.md`](enforcement.md)、督察 [`inspection.md`](inspection.md)；论坛全本流转见 `../media/forum-docs.md`（`eiafans` / `bbs.eiacloud.com`，本卡不重复）。
- 什么时候用：要**某项目的环境影响报告书/表全本 PDF、公参说明、验收报告、水保方案**；按项目名/建设单位/环评机构反查公示；核某地「环评审批了哪些项目」；做项目级环境合规底稿。
- 怎么搜：
  - **北京站内搜索（JSON，可用）**：
    ```bash
    UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    curl -sSk -m 30 -A "$UA" -H 'Content-Type: application/x-www-form-urlencoded' \
      -H 'Referer: https://sthjj.beijing.gov.cn/' \
      -X POST 'https://sthjj.beijing.gov.cn/so/ss/query/s?siteCode=1100000122' \
      --data-urlencode 'qt=环境影响评价文件受理' --data-urlencode 'page=1' \
      --data-urlencode 'pageSize=15' --data-urlencode "ie=$(python3 -c 'import uuid;print(uuid.uuid4())')"
    ```
    返回 `{"ok":true,"totalHits":…,"resultDocs":[{"data":{"titleO":…,"url":…}}]}`；`siteCode` 必须是 `1100000122`（市生态环境局），传 `sthjj` 会报「不存在的站点」。
  - **第三方平台搜索**：环评云 `https://www.eiacloud.com/gs/search?searchWord=<关键词>`（GET，匿名）；环境信息公示网 `http://hjxxgs.com/search.html?keywords=<关键词>`（GET，匿名），结果形态 `/gongshi/<id>.html`。
  - **静态栏目**：MEE 三栏与水利部两栏均为「年份/月份目录 + `tYYMMDD_*.shtml`」可翻页；北京通知公告为 `<articleId>/index.html`。
  - **全本 PDF 获取规律**（详见 `## 细节`）：①部批 → 受理公示页末附 `W020*.rar` 整包；②北京 → 附件与文章同目录（`<文章URL>/<yyyyMMddHHmmssSSS>.doc|.pdf`），或 `/eportal/fileDir/bjhrb/resource/cms/article/bjhrb_<colId>/<articleId>/<ts>.doc`；③第三方 → 公示页直链或登录后下载。
- 覆盖：生态环境部**部批**项目（受理/拟审查/已批准，近年逐周更新）；北京**省级权限**环评审批与备案结果；第三方平台聚合的**全国**建设单位自办公示（报告书全本、公参、验收、水保、节能、稳评等，约 2020 年至今，日更）；水利部生产建设项目水土保持方案审批。
- 门槛：MEE、水利部、北京市水务局、北京市发改委、`hjxxgs.com` → **免费匿名**；环评云正文与附件**文件名/大小**匿名可见，**下载需登录**（免费注册）；北京 `gzcx` 查询系统列表受 WAF 拦截（需浏览器）；`cepc.lem.org.cn`、`xypt.china-eia.com` → **412 WAF**（未通）。
- 实测：2026-10-03，macOS（arm64），curl 8.x（`-sSk -L -m 25`，桌面 Chrome UA，每主机 1–2 次）。核心观察：`xmslqk/` 200 且文章附 `W020260923567681040451.rar` → 200 `application/x-rar-compressed` 47,473,827 B；`eiacloud` 列表/搜索/详情 200，附件下载 POST `/gs/judgeRole` → 401；`hjxxgs` 详情 200 且附件直链 `/uploads/soft/…pdf`；北京站内搜索 JSON `totalHits=1019`；北京 `gzcx` 页面 200 但列表 AJAX 返回 WAF 页。明细见 `## 细节`。
- 上游：生态环境部、水利部、北京市生态环境局/水务局/发改委、环评云（`eiacloud.com`，尚云环境）、环境信息公示网（`hjxxgs.com`）

## 细节

### 平台一览（2026-10-03 本机探测）

| 平台 | 入口 | 公开程度 | 附件/全本形态 |
|---|---|---|---|
| 生态环境部·受理公示 | `mee.gov.cn/ywgz/hjyxpj/jsxmhjyxpj/xmslqk/` | ✅ 匿名 | 页末 `W020*.rar`（本次 47 MB，含报告书全本） |
| 生态环境部·拟审查项目公示 | `…/jsxmhjyxpj/nscxmgs/` | ✅ 匿名 | 本次抽查 4 篇（2026-07/08）**均无附件**，正文即结论；全本以受理公示附包为准 |
| 生态环境部·已批准项目公告 | `…/jsxmhjyxpj/ypzxmgg/` | ✅ 匿名 | 批复文件 |
| 全国环境影响评价管理信息平台 | `neweia.lem.org.cn/eia/` | ✅ 200（企业申报向） | 审批流程数据，非全本仓库 |
| 全国建设项目环评管理信息平台 `cepc.lem.org.cn` | `https://cepc.lem.org.cn/` | ❌ 412 WAF | — |
| 环评信用平台 `xypt.china-eia.com` | `https://xypt.china-eia.com/XYPT/` | ❌ 412 WAF | 环评单位/工程师信用 |
| 登记表备案系统 `beian.china-eia.com` | `https://beian.china-eia.com/a/login` | ⚠️ 登录（另有公众查询导航页） | 登记表备案信息 |
| 环评云·环境信息公示平台 | `eiacloud.com/gs/list/N` | ⚠️ 正文匿名 / **下载需登录** | 全本 PDF，页内显示文件名+大小 |
| 环境信息公示网 | `hjxxgs.com` | ✅ 匿名 | `/uploads/soft/<YYYYMMDD>/<rand>.pdf` 直链 |
| 生态环境影响评价信息公示平台 | `js-eia.cn` | ⚠️ 登录须知 | — |
| 北京·审批结果查询 | `gzcx.sthjj.beijing.gov.cn/eportal/ui?pageId=132186` | ⚠️ 页面匿名，**列表 AJAX 被 WAF 拦** | 「环评报告文件」列可下载（`V_T_CP_SPAccepted`） |
| 北京·通知公告 | `sthjj.beijing.gov.cn/bjhrb/…/325924085/` | ✅ 匿名 | 附件与文章同目录 |
| 水利部·受理/审批公告 | `mwr.gov.cn/fw/slgs/`、`/fw/spgg/` | ✅ 匿名 | 水保方案审批清单 |
| 北京市水务局·水保验收报备 | `swj.beijing.gov.cn/swdt/ztzl/scjsxmstbcsszzysbbxxgs/` | ✅ 匿名 | 月度报备公告（静态） |
| 北京市发改委·行政许可公示 | `fgw.beijing.gov.cn/fzggzl/yfxz/xzxk_sgs/` | ✅ 匿名 | 核准/批复 HTML |

### 北京 `gzcx` 查询系统栏目号（pageId）

| pageId | 栏目 | 状态 |
|---|---|---|
| 132070 | 首页 | ✅ 200 |
| 132186 | 一般建设项目环评审批·**已受理项目** | ✅ 页面 200 |
| 132292 | 一般建设项目环评审批·**拟审查项目** | ✅ 页面 200 |
| 132296 | 一般建设项目环评审批·**已审查项目** | ✅ 页面 200 |
| 134007 | 备案结果 | ✅ 页面 200 |
| 132284 | 办理进度 | ✅ 页面 200 |
| 132318 | 行政处罚 | ✅ 页面 200 |
| 135037 | 核与辐射类建设项目环评审批 | ✅ 页面 200 |

列表实现：`POST /eportal/admin?moduleId=f0270681ba5545089012be244338c858&struts.portlet.mode=view&struts.portlet.action=/portlet/commonSearch!getDataList.action`，`params=` + base64(JSON)，JSON 形如
`{"start":"0","end":"10","sourceId":"0902fd30eaf04a109c3601389e49ecf4","county":"","ApplicationID":"","ProjName":"","sort":" ACCEPTTIME desc"}`；
附件下载再走 `commonSearch!getFileName.action`（`colName=环评报告文件`、`tableName=V_T_CP_SPAccepted`）。**本机 curl 直连被 `X-Via-JSL`（加速乐）WAF 拦为 `illegalRequest`**，须浏览器或携带 JSL 通行 cookie。

### 全本 PDF 存放规律（抓取时按此拼 URL）

1. **部批**：`……/xmslqk/<YYYYMM>/t<YYYYMMDD>_<id>.shtml` 页末 `<a href="./W020<…>.rar">` → 与文章同目录的 rar（一包多项目，含报告书全本）；`nscxmgs` 拟审查页本次抽查 4 篇无附件，别空手而归。
2. **北京市局文章**：文章 `https://sthjj.beijing.gov.cn/bjhrb/index/xxgk69/zfxxgk43/fdzdgknr2/325924085/<articleId>/index.html`，附件 = 同目录 `<yyyyMMddHHmmss + 3 位毫秒>.doc|.pdf`（实例：`…/325924085/1739291/2022042615380470871.doc`）。
3. **北京 CMS 资源库**：`https://sthjj.beijing.gov.cn/eportal/fileDir/bjhrb/resource/cms/article/bjhrb_<colId>/<articleId>/<ts>.doc`（形态取自该站搜索结果 URL，未逐条复测）；短文偶见 `/bjhrb/resource/cms/article/<colId>/<articleId>/<ts>.pdf`。
4. **第三方平台**：`hjxxgs.com` 详情页直链 `/uploads/soft/<YYYYMMDD>/<rand>.pdf`；`eiacloud` 附件需登录换取下载 URL。
5. **建设单位/环评单位自建站**：官方不公开全本时，常挂在建设单位官网「公示公告」或环评单位站；用 `web_search "项目名" 环境影响报告书 全本 公示` 或搜狗微信定位。

### 全国/北京区级补充

- 称谓澄清：市面所称「**全国建设项目环境信息公示平台 2.0**」是 **环评云（尚云环境）** 的产品名，**不是部委官网**（其微信使用指南见 `https://mp.weixin.qq.com/s/LE1sPaCCfwZecBNKOEiH4A`）；官方口径只有生态环境部三栏 + 「全国环境影响评价管理信息平台」（`neweia.lem.org.cn`，面向申报）+ 环评信用/登记备案（`china-eia.com` 系）。
- 全国：`eiacloud`（聚合建设单位自办公示，条目最全）、`hjxxgs`（同名类目 + 直链）、`js-eia.cn`（需登录）。
- 北京区级：`sthjj.<区>.gov.cn` 子域**均不存在**（bjchy/bjft/bjtzh/bjdx/bjchp/bjsjs/bjshy/bjfsh/bjmy/bjpg/bjhr/bjmtg/bjdch/bjxch/bjyq 全部 NXDOMAIN；bjhd 仅解析到 IPv6 且连接失败）。区级公示散见于**各区门户「政务公开/生态环境」栏目**与**园区管委会**网站，无统一域名；建议用 `web_search` 或门户站内检索按「区名 + 项目名 + 环境影响报告」定位。
- 社会稳定风险评估 / 节能评估：官方口径多为项目所在地**发改委/区政府**的核准批复或专题公示栏（北京见 `fgw.beijing.gov.cn/fzggzl/yfxz/xzxk_sgs/`）；企业自办的稳评/节能公示常同时发在 `hjxxgs.com/wenping/`、`hjxxgs.com/jieneng/` 与 `eiacloud`。

## 坑

1. **WAF 三连**：`gzcx.sthjj.beijing.gov.cn` 的 AJAX POST 被加速乐拦（`X-Via-JSL` + `illegalRequest` 页）；`cepc.lem.org.cn`、`xypt.china-eia.com` 直接 412。别当死站，改浏览器或换入口。
2. **北京站内搜索要带对 `siteCode`**：`…/so/ss/query/s?siteCode=1100000122`，缺参返回「不存在的站点[null]」；`sourceCode`/`siteCode=sthjj` 均无效。
3. **`eiacloud` 附件需登录**：详情页能读到附件名与大小，但 `POST /gs/judgeRole` 未登录返回 `{"code":401}`；免费注册即可，别当成失效链接。
4. **附件与文章同目录**：北京文章附件是相对路径且带长毫秒时间戳，直接拼 `文章目录 + 文件名` 即可，不要猜全局路径。
5. **同名站点混淆**：`eia.gov` 是美国能源信息署（本层 `eia.gov.md`）；`eiafans.com`（环评爱好者）只走 http、GBK、需注册，见 `../media/forum-docs.md`。
6. **时效**：部批栏目逐周更新；北京 `gzcx` 只覆盖**省级权限**项目，区级权限项目须回各区门户找。
7. **合规**：只读公开页面；`rar` 整包可能有数十 MB，按需下载，勿批量搬。
