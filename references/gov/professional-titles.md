# professional-titles —— 职称评审公示与职业资格

- 去哪找：
  - **各地人社厅「职称评审公示」**：广东 `https://hrss.gd.gov.cn/zwgk/gsgg/`（通知公告）；江苏 `https://jshrss.jiangsu.gov.cn/col/col77278/index.html`（人才人事）、`col/col57143`（文件公告）；浙江 **浙江省专业技术人才管理服务平台** `https://zcps.rlsbt.zj.gov.cn/028/client/index.jsp`（职称评审唯一入口，含评后公示名单）。
  - **职业资格考试**：中国人事考试网 `http://www.cpta.com.cn/`（= `cpta.mohrss.gov.cn`）——考试工作计划 `…/notice/2128.html`、成绩 `/performance/`、证书查询 `/certCheck.html`、电子证书下载 `/certDown2024.html`。
  - **技能人才评价**：技能人才评价工作网 `http://osta.mohrss.gov.cn/`；证书全国联网查询 `http://zscx.osta.org.cn/`；评价机构 `http://pjjg.osta.org.cn/`、机构备案 `http://jigou.osta.org.cn/`。
- 什么时候用：核某人**职称取得情况**（评后公示名单=姓名·单位·专业·申报职称）；查某省**职称评审通过人员公示**；查**职业资格考试**年度计划/成绩/证书真伪；查**职业技能等级证书**真伪与评价机构资质；做人才履历核查、单位职称结构统计。
- 怎么搜：**分省规律**——广东进 `zwgk/gsgg/` 按标题搜「职称评审…公示」；江苏从列表页 `jpage` 初始化参数拼 `dataproxy.jsp` 拿 XML 列表（含标题+文章链接），再进 `/art/{Y}/{M}/{D}/art_{栏}_{id}.html`；浙江走 `zcps.rlsbt.zj.gov.cn` 平台 JSON 接口（需会话 cookie，见 `## 细节` §1.3）。**考试/技能**走 cpta 与 osta 静态栏目 + 证书查询页。逐源操作见 `## 细节`。
- 覆盖：广东/江苏/浙江三省市人社厅**职称评审公示逐年**（评后公示、评审通过人员名单，2018→2026）；全国**专业技术人员职业资格考试**（人社部年度计划、33 项固定合格标准、成绩、电子证书）；**职业技能等级认定**证书全国联网（含机构、评价计划）。粒度=单场评审名单（姓名 + 单位 + 专业 + 职称）或单张证书。
- 门槛：**免费、免登录**为主。浙江 `zcps` 的 JSON 接口需先取 `028JSESSIONID` 会话 cookie（匿名即可，无验证码）；江苏 `dataproxy.jsp` 直连即可；`www.cpta.com.cn` **仅 HTTP 可用**（HTTPS 在 LibreSSL 3.3.6 下握手失败，见坑 1）。
- 实测：2026-10-03，macOS 27（arm64），curl 8.x（desktop Chrome UA、`-L`、20 s 超时、同主机 ≥1.5 s）。广东首页 200 / 92 475 B、`zwgk/gsgg/index.html` 200 / 30 555 B、职称公示样例 `post_4740944.html` 200 / 28 614 B。江苏首页 200 / 195 568 B、人才人事栏 200 / 54 719 B、`dataproxy.jsp` **200 / 123 485 B `text/xml`**（`<totalrecord>1928</totalrecord>`）。浙江 `zcps` 首页 200 / 44 366 B、`findTable56ListByColumn43.action` **200 JSON**、`findTable30ListByColumn111Page1.action` **200 JSON**（返回姓名/单位/职称行）；无 cookie 时 `非法请求 404！`。cpta HTTPS **握手失败**、HTTP 首页 200 / 32 708 B、考试计划页 200 / 22 890 B。osta 200 / 34 757 B、zscx 200 / 5 046 B。逐条见 `## 细节`。
- 上游：广东省人社厅 <https://hrss.gd.gov.cn/>；江苏省人社厅 <https://jshrss.jiangsu.gov.cn/>；浙江省人社厅 <https://rlsbt.zj.gov.cn/>（职称平台 `zcps.rlsbt.zj.gov.cn`）；人社部人事考试中心 <http://www.cpta.com.cn/>；技能人才评价工作网 <http://osta.mohrss.gov.cn/>。

## 细节

> 探测纪律（本机实测）：≤3 请求/主机·轮、间隔 ≥1.5 s、20 s 超时、桌面 Chrome UA。`✅`=本机 200；`⚠️`=有但需浏览器/会话；`❌`=不可达。

### 1. 三省市职称评审公示规律

#### 1.1 广东（hrss.gd.gov.cn）—— 静态栏目 + 文章页

| 栏目 | URL | 实测 |
|---|---|---|
| 通知公告（职称公示多在此） | `https://hrss.gd.gov.cn/zwgk/gsgg/index.html` | ✅ 200 / 30 555 B |
| 人才引进 | `https://hrss.gd.gov.cn/zwgk/rcyj/index.html` | ✅ 200（首页内链 200） |
| 信用信息双公示 | `https://hrss.gd.gov.cn/zwgk/xyxxsgs/index.html` | ✅ 200（首页内链 200） |
| 文章页 | `https://hrss.gd.gov.cn/zwgk/gsgg/content/post_{id}.html` | ✅ 200 / 28 614 B（样例《2024年度广东省人力资源管理专业高级职称评审通过人员名单公示》） |

- 文章 URL 为 `post_{id}.html`；附件为 `/attachment/{…}/{id}.pdf`（示例 `…/attachment/0/599/599288/4804801.pdf`）。
- 栏目列表**只滚动近期**，历史用 `index_1.html`… 翻页或直接按标题检索。

#### 1.2 江苏（jshrss.jiangsu.gov.cn）—— jpage 列表 XML 接口

- 栏目：人才人事 `col/col77278`（文章 `/art/{Y}/{M}/{D}/art_77278_{id}.html`）、文件公告 `col/col57143`（`art_57143_*`）。
- 列表由 `jpage` 组件异步拉取，其请求参数就写在列表页源码里（`proxyUrl:'/module/web/jpage/dataproxy.jsp'`、`totalRecord`、`ajaxParam`）：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  curl -s -A "$UA" 'https://jshrss.jiangsu.gov.cn/module/web/jpage/dataproxy.jsp?page=1&appid=1&webid=67&path=/&columnid=77278&unitid=303271&permissiontype=0'
  ```
  返回 **XML**：
  ```xml
  <datastore><totalrecord>1928</totalrecord><totalpage>20</totalpage>
  <recordset><record><![CDATA[<li class="cf"><a target="_blank"
    href="/art/2026/9/16/art_77278_11830771.html" title="省人力资源社会保障厅关于印发…的通知">…</a></li>]]></record>…
  ```
- **路径必须是 `/module/web/jpage/dataproxy.jsp`**（`/module/jpage/dataproxy.jsp` → 404）；换栏目改 `columnid`+`unitid`（两者都从该列表页源码取），`page` 递增。
- 站内检索：`so.moe` 式统一检索**不适用**（江苏非 so-gov 站）；用站内搜索或搜索引擎 `site:jshrss.jiangsu.gov.cn 职称评审 公示`。

#### 1.3 浙江（zcps.rlsbt.zj.gov.cn）—— 职称评审 JSON API ★

- 浙江省专业技术职务任职资格**申报与评审管理服务平台**（`https://zcps.rlsbt.zj.gov.cn/028/client/index.jsp` ✅ 200 / 44 366 B）集中发布「评后公示名单」；评后公示页 `…/028/client/index6page2.jsp?column1=<uuid>` 是 JS 模板，数据走 `guestServiceAction!*.action`。
- **需会话 cookie**：先 GET 任一页面拿 `028JSESSIONID`，再 POST；否则返回 `非法请求 404！`。
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  J=/tmp/zcps.jar
  curl -s -A "$UA" -c $J 'https://zcps.rlsbt.zj.gov.cn/028/client/index.jsp' -o /dev/null
  B='https://zcps.rlsbt.zj.gov.cn/028/guestService/guestServiceAction!'
  # ① 评后公示列表（近场次）：返回 rows[{column1=场次uuid, column6=标题, column5=年, column43=日期}]
  curl -s -A "$UA" -b $J -H 'Referer: https://zcps.rlsbt.zj.gov.cn/028/client/index.jsp' \
    -X POST "${B}findTable56ListByColumn43.action" --data 'column43='
  # ② 某场公示的**名单**：column2=<场次uuid>
  curl -s -A "$UA" -b $J -H 'Referer: https://zcps.rlsbt.zj.gov.cn/028/client/index6page2.jsp?column1=<uuid>' \
    -X POST "${B}findTable30ListByColumn111Page1.action" --data 'column2=<uuid>'
  # ③ 公示标题/发布时间：column1=<场次uuid>
  curl -s -A "$UA" -b $J -H 'Referer: https://zcps.rlsbt.zj.gov.cn/' \
    -X POST "${B}getTable56ByTable2Column1.action" --data 'column1=<uuid>'
  # ④ 通知公告列表（嵌套数组）
  curl -s -A "$UA" -b $J -H 'Referer: https://zcps.rlsbt.zj.gov.cn/' \
    -X POST "${B}findTable74List1.action" --data 'column1='
  ```
- 名单字段（实测 ②）：`column10`=姓名、`column15`=工作单位、`column25`=申报职称（如「兽医师」）、`column27`=级别（中/高级）、`column48`=现从事专业、`column65`=申报方式（正常申报/转（兼）评）、`column197`=最高学历。
- 省厅官网「公示公告」栏 `https://rlsbt.zj.gov.cn/col/col1229116948/index.html` ✅ 200 / 6 075 B 但为 JS 壳（列表另加载）；**职称评审数据以 zcps 平台为准**。

### 2. 职业资格考试（人社部人事考试中心）

- 官网 `http://www.cpta.com.cn/`（HTTP；HTTPS 见坑 1）✅ 200 / 32 708 B，等价域名 `cpta.mohrss.gov.cn`。
- 栏目规律（`/…` = 数字 id 的文章）：

| 栏目 | URL | 实测 |
|---|---|---|
| 通知公告 | `http://www.cpta.com.cn/notice.html`；文章 `/notice/{id}.html` | ✅ 《2026年度专业技术人员职业资格考试工作计划》`/notice/2128.html` 200 / 22 890 B |
| 考试提醒 | `http://www.cpta.com.cn/examNotice/{id}.html` | ✅（首页内链，如 `2138`/`2221`） |
| 成绩公布 | `http://www.cpta.com.cn/performance/{id}.html` | ✅（如 `2237`/`2239`） |
| 职业资格证书查询 | `http://www.cpta.com.cn/certCheck.html` | ✅（首页内链） |
| 电子证书下载 | `http://www.cpta.com.cn/certDown2024.html` | ✅（首页内链） |
| 山寨证书声明 | `http://www.cpta.com.cn/ShanzhaiCertificate/{id}.html` | ✅（辨伪用） |

- 年度计划页含**全年各考试名称 + 日期**；合格标准见《关于 33 项专业技术人员职业资格考试实行相对固定合格标准有关事项的通告》`/2022/1039.html`。
- 各省**报名/审核**在省级人事考试网（一般 `rsks.{省}.gov.cn` 或人社厅子站），名单与证书仍以 cpta 为准。

### 3. 技能人才评价

| 用途 | URL | 实测 |
|---|---|---|
| 工作网（政策/标准/机构） | `http://osta.mohrss.gov.cn/` | ✅ 200 / 34 757 B |
| **证书全国联网查询** | `http://zscx.osta.org.cn/` | ✅ 200 / 5 046 B（title「技能人才评价证书全国联网查询」） |
| 评价机构（备案） | `http://jigou.osta.org.cn/`、`http://pjjg.osta.org.cn/` | 首页内链（未单独实调） |
| 技能标准 | `osta.mohrss.gov.cn/skillStandard`、`…/career`、`…/evaluation` | 首页内链 |
| 旧站 | `http://www.osta.org.cn/`、`http://old.osta.org.cn/` | 首页内链 |

- 证书查询为表单页（输入姓名 + 证件号 + 证书编号）；`zscx` 页面同时挂有 市场监管（`cnse.samr.gov.cn`）、应急（`cx.mem.gov.cn`）、住建（`zlaq.mohurd.gov.cn`）等其他证书查询入口。

## 坑

1. **`www.cpta.com.cn` 的 HTTPS 在 LibreSSL/旧 curl 下握手失败**（`sslv3 alert handshake failure`，HTTP/1.1 与 `--tlsv1.2` 均 000）——**改用 `http://`**（200）或用现代 OpenSSL 的 curl/浏览器。别据此判站不可用。
2. **证书查询站易被当成「职称库」**：`zscx.osta.org.cn` 查的是**职业技能等级证书/国家职业资格证书**，**不是职称证书**（职称无全国统一查询库，只有各省公示）；两者不要混。
3. **浙江 zcps 接口有会话门**：无 `028JSESSIONID` 时统一返回 `非法请求 404！`（HTTP 200 的文本），易误判为端点失效；务必先 GET 页面带上 cookie jar。响应 `Content-Type` 有 `text/html` 与 `text/plain` 两种但正文都是 JSON。
4. **江苏 jpage 路径与参数**：`/module/web/jpage/dataproxy.jsp`（含 `web`）；`columnid`/`unitid` 一一对应，串用别栏会返回别的栏目数据或空。返回是 **XML+CDATA**，需解析 `record` 里的 `<a href=… title=…>`。
5. **广东文章 id 与栏目绑定**：`post_{id}.html` 只在 `zwgk/gsgg/` 下成立；同一 id 换栏目会 404，务必从列表取全链而非拼 id。
6. **各省「职称评审公示」不在一处**：有的在人社厅「通知公告」，有的在独立职称平台（浙江 zcps）、有的在「双公示/信用」栏（广东 `xyxxsgs`）；按省先试这三类栏目，再退回 `web_search site:{厅域名} 职称评审 公示`。
7. **公示 ≠ 取得资格**：评后公示期内的名单可能被异议撤销；正式资格以「评审结果通知/证书」为准，公示名单应注明「公示」性质与日期。

## 相关

- 人才计划名单（杰青/优青、长江学者、特贴、博士后）：`talent-programs.md`。
- 领导干部任免/任前公示：`renshi-sources.md`；官员研究流程：`../methods/officials-research.md`。
- 事业单位公开招聘、社会组织：`sydj.md`、`chinanpo.md`；高校与科研机构名录：`edu-research-institutions.md`。
- 人社口径统计（参保、职业培训、技工院校）：`../surveys/social-insurance.md`、`../stats/ministry-stats.md`。
