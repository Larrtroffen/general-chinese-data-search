# 事业单位登记平台 —— 法人登记与年报公示查询

- 去哪找：
  - 平台首页（通知公告/政策法规/技术服务）：`https://gjsy.scopsr.gov.cn/`
  - 事业单位法人登记信息查询（页面，内嵌 iframe）：`https://gjsy.scopsr.gov.cn/sydwfrxxcx/`
  - **法人登记查询应用（iframe 源）**：`http://search.gjsy.gov.cn/`（自动 POST 到 `/wsss/view`）
  - **年度报告公示：列表框架页**：`http://search.gjsy.gov.cn:9090/queryAll/listFrame1?districtCode=100000`
  - **年度报告公示：检索**：`http://search.gjsy.gov.cn:9090/queryAll/search?districtCode=<区划码>&sydwName=<名称>`
  - 年报详情（iframe）：`http://search.gjsy.gov.cn:9090/queryAll/iframeRandom/<区划码>/<年份>/<HASH>`
  - 年报查询（含证书号）：`http://search.gjsy.gov.cn:9090/query/search?districtCode=<区划码>`（表单页，提交到 `/queryAll/search`）
  - `districtCode=100000` 表示全国；各省/市/区县用对应行政区划码。
- 什么时候用：
  - 关键词：事业单位名称 → **是否登记在册**、统一社会信用代码、法定代表人、举办单位、有效期。
  - 关键词：事业单位名称 / 法人证书号 → **年度报告**（年报正文、资产、人员、业务活动）。
  - 关键词：机构名 → 判断"某中心/某院/某学校"是否为**正规事业单位**（而非企业或非法机构）。
  - 不适用：企业（`gsxt.md`）；社会组织/协会（`chinanpo.md`）；行政机关（编办口径另行）。
- 怎么搜（两条都已在命令行跑通）：
  - **① 年度报告公示检索（GET，服务端渲染 HTML）**
    ```bash
    # 全国范围按名称检索（关键词需为中文/字母数字，长度 1–20，否则前端正则拒绝）
    curl -sS -m 20 'http://search.gjsy.gov.cn:9090/queryAll/search?districtCode=100000&sydwName=%E5%8D%9A%E7%89%A9%E9%A6%86' \
      -H 'Referer: http://search.gjsy.gov.cn:9090/queryAll/listFrame1?districtCode=100000' \
      -o out.html
    grep -oE '/queryAll/iframeRandom/[0-9]+/[0-9]{4}/[0-9A-F]+' out.html | sort -u
    # → 200，28 039 B，<title>年度报告-机关赋码和事业单位登记管理平台</title>，含 20+ 条年报链接
    ```
    结果形态：**服务端渲染 HTML 表格**；每条记录链接形如 `/queryAll/iframeRandom/100000/2025/1FD71273D6111CAECB4A1FB4FA3BCA8D`（区划码 / 年度 / 记录 hash），取该 URL 即得年报正文。另有 `sydwCode`（法人证书号）可作检索条件（`/query/search` 表单页支持"名称 + 证书号"）。
  - **② 法人登记查询（POST 表单）**：`http://search.gjsy.gov.cn/` 加载后由 `trans()` 自动提交表单到 `/wsss/view`：
    ```bash
    curl -sS -m 20 'http://search.gjsy.gov.cn/wsss/view' \
      -H 'Referer: http://search.gjsy.gov.cn/' \
      --data 'c=100000&t=0&at=null&sn=null&mc=null&ts=<毫秒时间戳>&w=null&h=null'
    ```
    字段：`c`=区划码（`100000`=全国）、`t`/`at`、`sn`、`mc`、`ts`=时间戳、`w`/`h`。结果形态：HTML 查询页（查询目标为法人登记信息）。
- 覆盖：全国事业单位（按 `districtCode` 下钻到省/市/区县）；法人登记为当前在册状态，年度报告按年度（列表实测含 2025 年度）；粒度=单单位级 + 单年度年报；动态更新（登记机关录入后同步）。
- 门槛：**免费、免登录、无验证码**（本机实测直连即返回数据）；技术注意：**只能走 http**（`https://…/sydwfrxxcx` → 301 到 http；`http://…/sydwfrxxcx` → 301 回 https，形成重定向循环，必须带尾部斜杠或直连 `search.gjsy.gov.cn:9090`）；旧域名 `www.gjsy.gov.cn` 已失效（DNS 不可解析），勿再引用。
- 实测：2026-10-03，macOS，curl 8.x，Chrome 126 UA。`GET https://gjsy.scopsr.gov.cn/` → **200**，4 009 B，`<title>机关赋码和事业单位登记管理平台</title>`；`GET https://gjsy.scopsr.gov.cn/sydwfrxxcx` → **301 → http://gjsy.scopsr.gov.cn/sydwfrxxcx/**；`GET http://gjsy.scopsr.gov.cn/sydwfrxxcx/` → **301 → https://…:443/sydwfrxxcx/**（循环），**加尾部斜杠走 https 即 200**（2 419 B，含 iframe `http://search.gjsy.gov.cn`）；`GET http://search.gjsy.gov.cn/` → **200**，1 118 B（含 `trans()` → POST `/wsss/view`，隐藏字段 `c=100000,t=0,at,sn,mc,ts,w,h`）；`GET http://search.gjsy.gov.cn:9090/queryAll/listFrame1?districtCode=100000` → **200**，25 784 B（表单 `#searchForm` action `/query/search`，字段 `districtCode`、`sydwName`）；`GET …:9090/query/search?districtCode=100000&sydwName=博物馆` → **404**（页面仍是查询表单，提示 action 实为 `/queryAll/search`）；`GET …:9090/queryAll/search?districtCode=100000&sydwName=博物馆` → **200**，28 039 B，**命中 20+ 条年报记录**；`GET http://www.gjsy.gov.cn/` → **000** DNS 解析失败（旧域名已下线）。
- 上游：<https://gjsy.scopsr.gov.cn/>、<https://gjsy.scopsr.gov.cn/sydwfrxxcx/>、<http://search.gjsy.gov.cn:9090/queryAll/listFrame1?districtCode=100000>

## 细节

中央编办事业单位登记管理局主办。含**事业单位法人登记信息查询**与**事业单位年度报告公示查询**，是本项目"查某事业单位是否真实存在、法人证书是否有效、年报内容"的官方源。

地方登记管理站（平台首页友情链接，可作分省补充）：北京 `bjsy.bjbb.gov.cn`、天津 `tjsy.gov.cn`、辽宁 `lnsydwzx.gov.cn`、黑龙江 `heilj.gjsy.gov.cn`、上海 `sydjsh.cn`、江苏 `180.101.234.208:8095/sydjweb/home`、浙江 `zjjgbz.gov.cn/sdjgl/`、福建 `fjbb.gov.cn`、山东 `sydwjg.sdbb.gov.cn`、湖北 `111.47.11.106:81`、湖南 `hunanbb.gov.cn`、广东 `gdbb.gov.cn/gdsydwdjgl/`、陕西 `sxdjgl.gov.cn`。

## 坑

1. 只能走 http + 尾部斜杠，否则 301 循环。
2. `query/search` 是表单页（404），实际检索 action 为 `/queryAll/search`。
3. 关键词长度 1–20，非中文/字母数字会被前端正则拒绝。
