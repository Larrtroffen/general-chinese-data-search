# standards-cn —— 国标/行标/地标检索与全文

中国标准体系的**官方一手入口**：国家标准（GB/GB-T）分两个站点——市场监管总局的**全国标准信息公共服务平台**（元数据检索）与**国家标准全文公开系统**（全文在线预览/下载）；行业标准、地方标准分别由 `hbba`/`dbba` 两个平台承接；团体标准在 `ttbz`；部委（生态环境、住建、交通）另有自有标准栏目。引用标准号/条款时优先用这些官方源。

- 去哪找：
  - 国标元数据检索：`https://std.samr.gov.cn/gb/gbQuery`
  - 国标全文公开：`https://openstd.samr.gov.cn/bzgk/std/`（`/bzgk/gb/` 301 到此）
  - 行业标准：`https://hbba.sacinfo.org.cn/stdList?key=&trade=`
  - 地方标准：`https://dbba.sacinfo.org.cn/stdList?key=&trade=`
  - 团体标准：`https://www.ttbz.org.cn/`
- 什么时候用：要查**标准号 ↔ 标准名称**对应、现行/废止状态、发布/实施日期、归口/主管部门；要**在线看国标全文**（免登录）；要查行业标准（AQ/DL/JT…）、地方标准（DBxx）、团体标准（T/…）；要生态环境/住建/交通部委标准正文或公告。
- 怎么搜：见下「细节」——`std.samr`/`hbba`/`dbba`/`mohurd` 有 **JSON 接口**，`openstd` 列表与详情是 HTML 但行内带 `hcno` 可拼全文预览；`mee` 是 HTML 站内搜索；`ttbz` 前台被 WAF 拦。
- 覆盖：国标元数据（现行+废止+即将实施，实测全量 79 816 条）、国标全文（强制+推荐性含 GB/T，部分外文版）、行业标准（约 20 个行业）、地方标准（各省 DB）、团体标准（T/）、生态环境标准全文 PDF、住建行业标准公告。
- 门槛：`std.samr`/`hbba`/`dbba`/`mohurd` 免费免登录；`openstd` 在线预览免登录，**下载可能弹验证码**；`ttbz` 需浏览器过 WAF。
- 实测：2026-10-03，macOS，curl 8.x，桌面 UA。
  - `std.samr`：`GET /gb/search/gbQueryPage?searchText=安全生产&ics=&state=&ISSUE_DATE=&limit=3&offset=0` → `{"total":40,…}`；加 `state=G_STATE:"现行"` → `total=28`；空 `searchText` → `total=79816`。
  - `openstd`：`GET /bzgk/std/std_list?p.p1=0&p.p90=circulation_date&p.p91=desc&p.p2=安全生产` → 200 HTML（94 KB，30 行 `showInfo('<hcno>')`）；`POST /bzgk/std/ajaxIcsList`（`pcode=`）→ 200 JSON ICS 树。
  - `hbba`：`POST /stdQueryList`（`key=安全生产&size=5`）→ `{"pages":41,…}`；`industry=电力` → `pages=2156`。
  - `dbba`：`POST /stdQueryList`（`key=安全生产`）→ `{"pages":139,…}`；`industry=江苏省` → `pages=2845`。
  - `ttbz`：`GET /Home/Standard` → 200 **WAF「WEB 应用防火墙」JS 挑战页**。
  - `mee`：`GET /searchnew/?searchword=大气污染物排放标准` → 200 HTML 结果页；详情 `.shtml` 内附 `W020…pdf`。
  - `mohurd`：`GET /api-gateway/jpaas-publish-server/front/page/build/unit?…` → `{"success":true,"data":{"html":"<li>…"}}`。
  - `jtst.mot.gov.cn` → **503**（31 B）。
- 上游：市场监管总局 / 国家标准化管理委员会（`std.samr.gov.cn`、`openstd.samr.gov.cn`）；国家标准技术审评中心（`hbba`/`dbba.sacinfo.org.cn`）；`ttbz.org.cn`；`mee.gov.cn`；`mohurd.gov.cn`；`mot.gov.cn`。

## 细节

> 下文 curl 示例中 `$UA` 为桌面浏览器 UA，例如：`UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'`。

### 1. std.samr.gov.cn 全国标准信息公共服务平台（国标元数据，JSON）

国家标准检索页 `/gb/gbQuery` 的表格数据接口（bootstrap-table，`queryParamsType:""` → 用 `limit`/`offset`）：

```bash
curl -s -A "$UA" \
  'https://std.samr.gov.cn/gb/search/gbQueryPage?searchText=%E5%AE%89%E5%85%A8%E7%94%9F%E4%BA%A7&ics=&state=&ISSUE_DATE=&limit=15&offset=0'
```

| 参数 | 含义 / 取值 |
|---|---|
| `searchText` | 关键词（标准名/标准号，URL 编码） |
| `ics` | ICS 分类（左侧菜单文本，如 `13.100`；空=全部） |
| `state` | 状态，格式 `G_STATE:"现行"`；多值逗号分隔（`现行`/`废止`/`即将实施`） |
| `ISSUE_DATE` | 发布日期，`-1/-3/-6/-12/-24/-36` = 近 1/3/6/12/24/36 月；空=不限 |
| `limit` / `offset` | 每页条数 / 偏移（`offset=0` 起） |

响应 `{"total":40,"pageNumber":1,"rows":[…]}`，`rows[]` 字段：`id`(64 位 hex)、`C_C_NAME`(名称，命中词包在 `<sacinfo>…</sacinfo>` 标签内)、`C_STD_CODE`(标准号)、`STD_NATURE`(强制性/推荐性)、`STATE`(现行/废止/即将实施)、`ISSUE_DATE`/`ACT_DATE`(发布/实施日期)、`PROJECT_ID`。

其他入口：

| 页面 | URL | 形态 |
|---|---|---|
| 国标高级检索 | `/gb/search/gbAdvancedSearch` → 数据接口 `/gb/search/gbAdvancedSearchPage?` + 表单序列化 | JSON（未实测） |
| 统一检索（国标/行标/地标…） | `/search/std?q=<kw>`；数据接口 `/search/stdPage?tid=&q=&op=&limit=&offset=` | HTML（服务端渲染） |
| 机构 / 委员 / 人员 / ISO | `/search/org?q=`、`/search/person?q=`、`/search/kpi?q=`、`/search/iso?q=` | （未实测） |
| 国家标准样品 / 外文版 / 技委会 | `/gsm/query`（国家标准样品）、`/gfs/query`（国家标准外文版）、`/org/orgTcQuery`（技术委员会目录查询） | HTML |
| 地方标准（平台内） | `/db/search/dbQuery` | ❌ 本机 **404**（改版，改用 `dbba`） |

### 2. openstd.samr.gov.cn 国家标准全文公开系统

列表 `GET /bzgk/std/std_list?…`（**HTML**），表单参数：

| 参数 | 含义 / 取值 |
|---|---|
| `p.p1` | 标准类型：空=全部、`1`=强制性、`2`=推荐性、`3`=指导性技术文件、`6`=外文版 |
| `p.p2` | 关键词（标准号或名称） |
| `p.p5` | 状态：`PUBLISHED`/`TOBEIMP`/`REPLACED`/`WITHDRAWN` |
| `p.p6` | ICS 分类码 |
| `p.p7` | 时间范围：`0.08/0.25/1/2/3/6` |
| `p.p90` / `p.p91` | 排序字段（`circulation_date`）/ 方向（`desc`） |

- 分类快捷页：`/bzgk/std/std_list_type?p.p1=1|2|3|6&p.p90=circulation_date&p.p91=desc`
- ICS 树 JSON：`POST /bzgk/std/ajaxIcsList`，data `pcode=<父码>` → `[{icsCode,icsName_cn,icsName_en,count,text}]`
- 详情：列表每行 `onclick="showInfo('<hcno>')"` → `GET /bzgk/std/newGbInfo?hcno=<hcno>`（HTML，含 CCS/ICS/发布/实施/主管/归口/发布单位）
- **在线全文预览（免登录）**：`GET /bzgk/std/showGb?type=online&hcno=<hcno>` → 查看器 HTML；正文按页为图片，`GET /bzgk/std/viewGbImg?fileName=<token>` → 302 到 `/bzgk/data/<标准号>/<宽-高-页_令牌>.webp`
- 下载：`GET /bzgk/std/showGb?type=download&hcno=<hcno>` → 小页 JS：`isValid=='true'` 时跳 `GET /bzgk/std/viewGb?hcno=<hcno>`（`application/octet-stream`）；否则弹验证码（图片 `/bzgk/std/gc`，校验 `POST /bzgk/std/verifyCode`，参数 `verifyCode`）

### 3. hbba / dbba 行业·地方标准平台（同构，JSON）

入口 `GET /stdList?key=&trade=`（HTML 壳），数据接口两站一致：

```bash
# 行业标准
curl -s -A "$UA" -H 'Content-Type: application/x-www-form-urlencoded' -X POST \
  --data 'current=1&size=15&key=%E5%AE%89%E5%85%A8%E7%94%9F%E4%BA%A7' \
  'https://hbba.sacinfo.org.cn/stdQueryList'
# 地方标准（industry 传省/市名）
curl -s -A "$UA" -X POST --data 'current=1&size=15&key=&industry=%E6%B1%9F%E8%8B%8F%E7%9C%81' \
  'https://dbba.sacinfo.org.cn/stdQueryList'
```

| 参数 | 含义 |
|---|---|
| `current` / `size` | 页码（1 起）/ 每页条数 |
| `key` | 关键词 |
| `industry` | hbba=行业名（电力/安全生产/包装…）；dbba=省/市名（江苏省…） |
| `ministry` | 主管部门 |
| `pubdate` / `date` / `status` | 发布/实施时间、状态（现行/废止/即将实施） |

响应 `{"current":1,"pages":41,"records":[…]}`，`records[]`：`pk`(64 位 hex，详情用)、`chName`、`code`(标准号)、`chargeDept`(归口/主管)、`industry`、`status`、`issueDate`/`actDate`/`recordDate`(**epoch 毫秒**)、`recordNo`(备案号)、`empty`；dbba 另含 `reviseStdCode`。日期字段需 `/1000` 后按毫秒时间戳解析。

- 详情：`GET /stdDetail/<pk>`（HTML，含 全文 按钮）
- 全文（部分开放）：`GET /portal/online/<pk>` → 链接 `GET /attachment/onlineRead/<pk>`（**HTML 全文**，`@media print{body{display:none}}`）

### 4. 部委标准入口

| 部委 | 入口 | 检索/接口 | 正文 |
|---|---|---|---|
| 生态环境部 | `https://www.mee.gov.cn/ywgz/fgbz/bz/bzwb/`（按要素：大气/水/固废/噪声/土壤/生态/核辐射） | 站内搜索 `GET /searchnew/?searchword=<kw>`（HTML） | 详情 `.shtml` 内附 PDF（相对路径 `W020….pdf`） |
| 住建部 | `https://www.mohurd.gov.cn/gongkai/fdzdgknr/bzgg/index.html`（标准公告） | 列表接口 `GET /api-gateway/jpaas-publish-server/front/page/build/unit?parseType=bulidstatic&webId=86ca573ec4df405db627fdc2493677f3&tplSetId=fc259c381af3496d85e61997ea7771cb&pageType=column&tagId=栏目-list&editType=null&pageId=Y53uSscFTKvrbHxaF9Cvp` → `{"success":true,"data":{"html":"…"}}` | 公告附件（PDF/doc） |
| 交通运输部 | `https://jtst.mot.gov.cn/`（标准化信息平台） | ❌ 本机 503 | — |

生态标准相关栏目：发布公告 `/ywgz/fgbz/bz/bzfb/`、标准管理 `../bzgl/`、征求意见 `../bzzqyj/`、地方生态环境标准 `/ywgz/fgbz/bz/dfhjbhbzba/`。

## 坑

1. `openstd` 的列表/详情是**服务端 HTML**，无公开 JSON 列表接口；解析用 `showInfo('<hcno>')` 正则取 id 再拼 `newGbInfo`。
2. `openstd` 在线预览/下载的图片与文件在本机（curl）返回 `Content-Type: image/webp` / `application/octet-stream` 但 **`Content-Length: 0`**，疑为防盗链/需浏览器会话；用浏览器可正常显示。`viewGbImg` 与 `viewGb` 均如此，脚本直连取不到字节。
3. `openstd` 页内含 `console-ban.min.js`（禁 F12）与右键/打印限制；部分标准下载需 FileOpen 插件（`http://c.gb688.cn/bzgk/FileOpenInstaller.exe`）。
4. `openstd` 下载**不一定**弹验证码：页面内 `isValid` 决定，`false` 时才校验 4 位图形码（`gc` + `verifyCode`）。
5. `std.samr` 的 `state` **不是**裸值，必须写成 `G_STATE:"现行"`（含引号），否则过滤无效。
6. `std.samr` 统一检索 `/search/stdPage` 返回 HTML（服务端渲染），不是 JSON。
7. `hbba`/`dbba` 的日期是 **epoch 毫秒**，直接入库会得到 1970 年附近的错值；需 `/1000` 换算。
8. `hbba`/`dbba` 全文并非全部开放（详情页有「暂不开放原因」），且 `onlineRead` 返回 HTML 而非 PDF，`@media print` 屏蔽打印。
9. `std.samr` 官方导航里的地方标准页 `/db/search/dbQuery?initnode=` 现已 **404**，地方标准改用 `dbba.sacinfo.org.cn`。
10. `ttbz.org.cn` 前台 `/Home/Standard` 命中 **WAF JS 挑战**；后台 API 前缀 `/ms/`（如 `/ms/portal/standardRecommend/recommendList`）需过 WAF，脚本不可直取。
11. 国标全文公开系统**不覆盖全部**国标：仅强制性与部分推荐性；工程建设标准（住建）多在公告附件而非 openstd。
12. `mohurd` 的 CMS 接口只接受 **GET**（POST 报「不支持的HTTP方法」），返回的是 HTML 片段字符串而非结构化列表。
