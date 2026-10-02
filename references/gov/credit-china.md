# 信用中国 —— 公共信用信息与红黑名单查询

- 去哪找：
  - 首页 / 搜索框：`https://www.creditchina.gov.cn/`
  - 信用信息（企业）检索页：`https://www.creditchina.gov.cn/xinyongfuwu/`（首页右上搜索框提交后进入）
  - 检索后端（现行，public 子域）：`https://public.creditchina.gov.cn/private-api/catalogSearchHome`
  - 检索后端（旧路径，仅形状参考）：`https://www.creditchina.gov.cn/api/credit_info_search?keyword=`
- 什么时候用：
  - 关键词：企业全称 / 统一社会信用代码 / 法定代表人 → **信用概览、行政许可、行政处罚**。
  - 关键词：企业名 → **是否在红名单 / 重点关注名单 / 黑名单**（招投标、供应商尽调、政府采购资格）。
  - 关键词：机构名 → "双公示"记录、信用承诺。
  - 不适用：企业工商登记原始档案（去 `gsxt.md`）；司法失信（去 `../legal/court-open.md`）。
- 怎么搜：
  - **网页路径（推荐，唯一能绕开 WAF 的姿势）**：浏览器打开首页 → 右上搜索框输入"法人和其他组织机构名称或统一信用代码" → 结果页 = 信用概览 + 分类标签页。北京市政务服务网对该流程的官方说明即以本入口为准（见"上游"）。
  - **接口路径（需带有效 WAF 会话 cookie，本机未跑通）**：
    ```bash
    UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    curl -sS -m 20 -A "$UA" \
      -H 'Referer: https://www.creditchina.gov.cn/' -H 'Origin: https://www.creditchina.gov.cn' \
      -H 'X-Requested-With: XMLHttpRequest' -H 'Accept: application/json, text/plain, */*' \
      'https://public.creditchina.gov.cn/private-api/catalogSearchHome?keyword=%E8%85%BE%E8%AE%AF&scenes=defaultScenario&tableName=credit_xyzx_tyshxydm&searchState=2&entityType=1,2,4,5,6,7,8,1001&page=1&pageSize=10'
    # 第一次 → 500 {"status":40001,"message":"请刷新后重试！","data":null}   ← 接口存在、返回 JSON
    # 再试   → 412（瑞数挑战页）
    ```
    现行检索接口参数：`keyword`（URL 编码）、`scenes=defaultScenario`、`tableName=credit_xyzx_tyshxydm`（主体信息表）、`searchState=2`、`entityType=1,2,4,5,6,7,8,1001`、`templateId=`、`page`/`pageSize`；需 `Referer: https://www.creditchina.gov.cn/`。
  - 结果形态：JSON（`data` 为记录数组）。网页端结果页为 JS 渲染 + 分页；"请刷新后重试"是 WAF/会话失效的统一话术，表示**缺有效会话 cookie，不是参数错误**。
- 覆盖：全国法人/其他组织 + 自然人（部分字段脱敏）；含中央部门与地方归集的"双公示"数据；行政许可/处罚逐年累积，黑名单为有效期内的当前名单；粒度=单主体级 + 单条许可/处罚记录；动态更新（各部门实时/按日归集）。
- 门槛：免费、**无需登录/注册**；但有**强反爬 WAF：瑞数（RiverSecurity，`$_ts` 动态脚本）+ 加速乐（`__jsl_clearance` cookie 挑战）**，匿名 curl 拿不到业务数据；可用姿势 = 真实浏览器（含无头浏览器，需能执行挑战 JS）。观察到的 cookie 名：`__jsluid_s`、`insert_cookie`、`https_waf_cookie`、一个 40 位随机名动态 cookie。
- 实测：2026-10-03，macOS，curl 8.x / Chrome 126 UA / `Accept-Language: zh-CN`。`GET https://www.creditchina.gov.cn/` → **412**（body 为 WAF 412 页，2.5 KB）；换 Windows Chrome/120 UA + `Referer` → **412**（2.6 KB，换 UA 无效）；`GET http://www.creditchina.gov.cn/` → **307**（body 为内联 JS `document.cookie='__jsl_clearance=…'`，加速乐第一段挑战）；`GET https://public.creditchina.gov.cn/` → **412**（body 含 `$_ts` 瑞数脚本）；`GET public…/private-api/catalogSearchHome?keyword=腾讯&…` → **500** `{"status":40001,"message":"请刷新后重试！","data":null}`，带 cookie jar 连跑第二次 → **412**。探测纪律：该主机共 6 次请求，跨 ≥1.5 s；被 412 后按"换 UA / 换 Referer / https↔http"各重试 1 次，均未通过。
- 上游：<https://www.creditchina.gov.cn/>；北京市政务服务网《法人和其他社会组织公共信用信息查询》办事指南 <https://banshi.beijing.gov.cn/pubtask/task/1/110113000000/8712af55-a6d9-4aa5-a391-6c88191a2b31_cjwt.html>

## 细节

发改委主办的**公共信用信息**一站式查询台：企业（法人）基本信息 + 行政许可 + 行政处罚 + 守信红名单 / 重点关注名单 / 黑名单，另含"双公示"（行政许可/处罚）与行业信用目录。是本项目"查某机构/企业的官方信用状态"的首选源。

### 旧接口形状（上游声明，仅供参考）

第三方爬虫仓库 `PrimaryDream/Crawl_ChinaInformation` 的 `spider_main`（约 2018–2019 年代码，域名已从 `www.` 迁至 `public.`）：

<https://github.com/PrimaryDream/Crawl_ChinaInformation/blob/master/spider_main>

- `/api/credit_info_search?keyword=`（企业联想/概览）
- `/api/credit_info_detail?encryStr=<key>`（信息概览详情，key 从检索结果里取）
- `/api/pub_permissions_name?name=<名称>&page=1&pageSize=10`（行政许可）
- `/api/pub_penalty_name?name=<名称>&page=1&pageSize=10`（行政处罚）
- `/api/record_param?encryStr=<key>&creditType=2|4|8&dataSource=0&pageNum=1&pageSize=10`（2=守信红名单，4=重点关注名单，8=黑名单）

## 坑

1. 整站被瑞数 + 加速乐包裹，CLI 直连受限；接口存在且返回 JSON，但需有效 WAF 会话 cookie。
2. 换 UA / Referer / 协议均无效，412 是挑战页而非参数错误。
3. `http://` 会返回内联 JS 挑战（307），不是重定向到内容。
