# ccgp-ggzy —— 招投标与政府采购公告检索

两张国家级招投标/采购公告网合为一卡：**ccgp**（中国政府采购网）是财政部唯一指定的政府采购信息发布媒体；
**ggzy**（全国公共资源交易平台）是国家发改委牵头的全国公共资源交易（工程/采购/土地/矿业权/产权/碳排放/排污权）总平台。

- 去哪找：
  - **全国公共资源交易平台（本卡首选）**：首页 `https://www.ggzy.gov.cn/`；交易公开列表 `https://www.ggzy.gov.cn/deal/dealList.html`（按大类 `?HEADER_DEAL_TYPE=01` 工程建设 `=02` 政府采购 `=03` 土地使用权 `=04` 矿业权 `=05` 国有产权 `=21` 碳排放权 `=22` 排污权 …`=90`）；交易信用 `/deal/creditList.html`（`?SHOWTYPE=1|2`）；**检索 API** `POST https://www.ggzy.gov.cn/information/pubTradingInfo/getTradList`；验证码 `GET https://www.ggzy.gov.cn/information/captcha`；公示/政策栏目 `/SIC/web/collectList.po`、`/SIC/web/policyFileList.po`、`/SIC/web/policyReadList.po`。
  - **中国政府采购网**：首页 `https://www.ccgp.gov.cn/`（本机 403）；**采购公告检索** `http://search.ccgp.gov.cn/bxsearch`（必须 http）；公告栏目（按类型）`https://www.ccgp.gov.cn/cggg/`（中央公告 `zygg`、地方公告 `dfgg` 等）。
- 什么时候用：
  - 关键词：项目/标的名称（如"服务器"、"污水治理"）→ 招标公告、中标/结果公告。
  - 关键词：采购人 / 代理机构 → 某单位近年采购项目。
  - 关键词：地区 + 类型 → 某地工程建设/土地出让/国有产权交易记录。
  - 用途：查"某单位是否采购/中标过某类项目"、核对项目编号与公告时间。
  - 不适用：仅政府采购的政策法规原文 → 去 `china-policy-sites.md` / `gov.cn.md`；供应商企业背景 → `gsxt.md`、`credit-china.md`。
- 怎么搜：
  - **ggzy 检索 API（已实测打通）**：
    ```bash
    curl -sS -m 25 'https://www.ggzy.gov.cn/information/pubTradingInfo/getTradList' \
      -H 'Content-Type: application/x-www-form-urlencoded' \
      -H 'Referer: https://www.ggzy.gov.cn/deal/dealList.html' \
      -H 'X-Pass-Token: ' \
      --data 'DEAL_TIME=04' \
      --data 'FINDTXT=服务器' \
      --data 'PAGENUMBER=1'
    # → 200 {"code":200,"message":"success","data":{"records":[20条],"total":1000,"size":20,"current":1,…}}
    ```
    请求字段、返回字段与返回码见 `## 细节`。列表页为 JS 渲染，勿直接解析 HTML。
  - **ccgp 检索（URL 模板，必须 http）**：
    ```
    http://search.ccgp.gov.cn/bxsearch
      ?searchtype=1                # 1=采购公告检索
      &page_index=1                # 页码
      &bidSort=0                   # 排序
      &buyerName=                  # 采购人
      &projectId=                  # 项目编号
      &pinMu=0                     # 品目
      &bidType=0                   # 公告类型：0=所有；7=中标公告；其它见页面下拉
      &dbselect=bidx
      &kw=<关键词 URL编码>
      &start_time=2026:09:30       # 注意分隔符是冒号
      &end_time=2026:10:01
      &timeType=6                  # 6=指定时间
      &displayZone=<省名>           # 如 陕西省
      &zoneId=<省名>
      &pppStatus=0
      &agentName=                  # 代理机构
    ```
    结果形态：**服务端渲染 HTML 列表**（含公告标题、类型、采购人、代理机构、发布日期、地区），分页由 `page_index` 控制；无 JS 依赖，但必须用 http（https 回 500）。
- 覆盖：全国 31 省 + 央企 + 部委来源汇集的交易/采购公告；类型覆盖工程建设、政府采购、土地使用权、矿业权、国有产权、碳排放权、排污权；含公开招标/询价/竞争性谈判/单一来源/资格预审/邀请/中标/成交/更正/终止等公告类型，品目可按货物/工程/服务筛；更新动态（按日，含当天）；粒度=单条公告，正文为静态 HTML 详情页。
- 门槛：免费、免登录；ggzy 平时无需验证码，仅在触发频控（`code=829`）时弹图形验证码；ccgp 反爬严格：`www.` 首页直连 403、检索端限流（"频繁访问"页）。
- 实测：2026-10-03，macOS，curl 8.x，Chrome 126 / Windows Chrome 120 UA。ggzy `POST /information/pubTradingInfo/getTradList`（`DEAL_TIME=04&FINDTXT=服务器&PAGENUMBER=1`）→ **200 JSON，`total=1000`，`records` 20 条**（首条 `title="国产超融合平台服务器项目结果公告（采购包1）"`、`publishTime="2026-10-01"`、`provinceText="山东省"`、`businessTypeText="政府采购"`）；ccgp `https://www.ccgp.gov.cn/` → 403（962 B 拦截页），`http://search.ccgp.gov.cn/bxsearch?…&kw=服务器` → 200 但 1448 B"频繁访问!中国政府采购网"限流页。详见 `## 细节`。
- 上游：<https://www.ggzy.gov.cn/deal/dealList.html>、<http://search.ccgp.gov.cn/bxsearch>、<https://www.ccgp.gov.cn/cggg/>

## 细节

### 站点对照

| 站点 | 主机 | 定位 | 本机 CLI |
|---|---|---|---|
| 中国政府采购网 | `www.ccgp.gov.cn` / `search.ccgp.gov.cn` | 政府采购公告（公开招标/中标/更正…） | 首页 403；检索接口 **http 可达但限流** |
| 全国公共资源交易平台 | `www.ggzy.gov.cn` | 全国交易公开（含政采、工程、土地等） | **可用，有 JSON 接口**（已验证） |

### ggzy `getTradList` 请求字段

由 `dealList.html` 内联 Vue 的 `getList()` 反查：

| 字段 | 含义 / 取值 |
|---|---|
| `FINDTXT` | 关键词（必填才有关键词过滤） |
| `PAGENUMBER` | 页码（从 1 起；每页 20 条） |
| `DEAL_TIME` | `01`当天 / `02`近三天 / `03`近十天 / `04`近一月 / `05`近三月 / `06`时间区间 |
| `TIMEBEGIN` / `TIMEEND` | 配合 `DEAL_TIME=06`（格式 `YYYY-MM-DD`） |
| `DEAL_CLASSIFY` | `00`不限 / `01`工程建设 / `02`政府采购 / `03`土地使用权 / `04`矿业权 / `05`国有产权 |
| `DEAL_STAGE` | 阶段码，如 `0100`/`0200`/`0300`（与 `DEAL_CLASSIFY` 前两位一致，后两位 00=不限） |
| `DEAL_TRADE` | 交易方式（`0`=不限） |
| `DEAL_PROVINCE` / `DEAL_CITY` / `DEAL_PLATFORM` | 省/市/平台码（`0`=不限；区划码如 `370000`=山东） |
| `BID_PLATFORM` / `SOURCE_TYPE` | 招标平台 / 来源（`1`省平台、`2`央企招投标、`3`财政部、`4`自然资源部、`5`国资委、`6`商务部） |
| `X-Pass-Token`（Header） | 仅在返回 `code=829`（要求验证码）时填：`<captchaToken>#<verifyCode>` |

### ggzy 返回字段与返回码

- `data.records[]`：`id`、`title`、`publishTime`、`provinceText`、`businessTypeText`（如"政府采购"）、`informationTypeText`（如"公告信息"）、`transactionSourcesPlatformText`（来源平台）、`url`（详情，形如 `/information/deal/html/a/370000/0201/20261001/<id>.html`）；`total` 上限 **1000**。
- 返回码：`200` 成功；`829` 需验证码（响应带 `captchaToken`+`captchaImage`）；`800` 操作过于频繁；`804` 请细化查询条件；`801` 参数错误。

### ggzy 补充实测（2026-10-03）

- `GET http://www.ggzy.gov.cn/` → 301 → `https://` **200**，70 629 B，`<title>全国公共资源交易平台</title>`。
- `GET /deal/dealList.html?…&FINDTXT=服务器`（curl）→ 200 但列表为 JS 渲染（页面 53 KB 仅含 `searchJson` 配置）。
- `DEAL_TIME=01`（当天）同关键词 → **0 条**（时间窗过滤生效，跨天查询要用 `04`/`05`/`06`）。
- `GET /information/captcha` → **200 JSON** `{"code":200,"data":{"captchaImage":"iVBORw0KGgo…","captchaToken":…}}`。
- 注意：本机对该站 **https 偶发 `tlsv1 alert protocol version`（curl/LibreSSL 3.3.6）** —— 同一命令重试即成功（200 + 完整 JSON），python/OpenSSL 客户端同样正常；是服务端 TLS 协商抖动，重试即可，非站点故障、非参数问题。

### ccgp 补充实测（2026-10-03）

- `GET https://www.ccgp.gov.cn/`（Chrome/126 UA）→ **403**，962 B 自定义拦截页；换 Windows Chrome/120 UA + `Referer: https://www.baidu.com/` → **403**（换 UA 无效）。
- `GET https://search.ccgp.gov.cn/` → **200**，236 B（meta refresh 跳 `http://www.ccgp.gov.cn`）。
- `GET https://search.ccgp.gov.cn/bxsearch?…&kw=服务器` → **500 Internal Server Error**（https 不通）。
- 同 URL 模板（`start_time=2026:06:01&end_time=2026:10:01&displayZone=陕西省&bidType=7`）**被搜索引擎正常收录并返回结果页正文**（见"上游"）→ 接口本身可用，本机受限是**限流 + 需 http + 可能需浏览器指纹**。

## 坑

1. ccgp **必须 http**（https 500）；ggzy 用 https，偶发 TLS 抖动重试即可。
2. ggzy 列表页 HTML 不含数据，必须打 `getTradList`；`FINDTXT` 不填则不做关键词过滤。
3. 触发频控后 ggzy 要求图形验证码（`code=829`）；`X-Pass-Token` 需 `<captchaToken>#<verifyCode>`。
4. ccgp 检索端限流，失败先降频/换 IP，勿连续重试。
5. ggzy `total` 上限 1000，超量需按时间/地区细分查询。
