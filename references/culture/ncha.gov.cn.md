# ncha.gov.cn —— 国保单位与博物馆年报

- 去哪找：**国家文物局**官网 `http://www.ncha.gov.cn/`（注意 **http**）；全国重点文物保护单位名单 `http://www.ncha.gov.cn/col/col2289/index.html`（第八批）、`http://www.ncha.gov.cn/col/col2284/index.html`；单篇全名单 `http://www.ncha.gov.cn/art/2019/10/18/art_2289_157100.html`；**全国博物馆年度报告信息系统** `http://nb.ncha.gov.cn/museum.html`；文保工程审批 `http://gl.sach.gov.cn/`；国家文物局数据中心（中国文物信息咨询中心）`http://www.cchicc.org.cn/`。
- 什么时候用：要**全国重点文物保护单位（国保）名单**（各批次，含名称/年代/地址）；要博物馆年度报告口径的**博物馆数量/名录**线索；要文物政策、考古、博物馆管理通知原文；要文保资质/审批信息。
- 怎么搜：站点为 TRS WCM 静态页，**用 http（https 连不通）**，直接抓 HTML/附件：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
  curl -sS -A "$UA" --compressed 'http://www.ncha.gov.cn/col/col2289/index.html'          # 第八批国保名单栏目
  curl -sS -A "$UA" --compressed 'http://www.ncha.gov.cn/art/2019/10/18/art_2289_157100.html'  # 第八批全名单（HTML，~700 KB）
  ```
  结果形态：**HTML**（名单以网页表格/正文承载）；`nb.ncha.gov.cn` 年报系统为 JS 前端（`museum/js/museumList.js`），面向博物馆填报，**读名单需登录**。
- 覆盖：国保单位分批次名单（第八批起在 `col/col2284–2289`，历代批次散见栏目与国务院通知）；博物馆年报系统覆盖全国博物馆基础信息与年报（填报制）；文保工程审批、考古、政策通知按日更新。
- 门槛：**免费、免登录、无 key**（国保名单）；年报系统与审批平台需注册/单位登录。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA——`GET http://www.ncha.gov.cn/` → **200**（17 KB，`<title>国家文物局</title>`）；`GET https://www.ncha.gov.cn/` → 20 s 超时（**https 不可达**）；`GET http://www.ncha.gov.cn/col/col2289/index.html` → **200**（699 KB，`<title>国家文物局 第八批国保名单</title>`）；`GET …/art_2289_157100.html` → **200**（700 KB，含「全国重点文物保护单位」全名单）；Chromium 打开 `http://www.ncha.gov.cn/` → `net::ERR_BLOCKED_BY_CLIENT`、`https://…` → `ERR_CONNECTION_CLOSED`（该站仅 CLI/http 路径可用）。
- 上游：<http://www.ncha.gov.cn/>（国家文物局）；数据中心 <http://www.cchicc.org.cn/>。

## 细节

- 栏目命名规律：`/col/colNNNN/index.html`（列表）、`/art/YYYY/M/D/art_<栏目>_<id>.html`（正文）。
- 国保名单相关栏目：`col2289`（第八批名单）、`col2284`/`col2285`（第八批公布通知与解读）。
- 关联机构入口（页脚）：中国文化遗产研究院 `cach.org.cn`、中国文物报社 `zhongguowenwubao.com`、中国博物馆协会 `chinamuseum.org.cn`、国家文物局考古研究中心 `uch-china.com`。
- 全国博物馆年度报告系统 `http://nb.ncha.gov.cn/museum.html` 前端脚本 `museum/js/museumList.js`（含 `getNbProvCount` 等按省统计调用），后端另挂 `:8081`/`bwgnb.cchicc.org.cn` 登录。

## 坑

1. **必须用 http**：https 主机在本机直接超时；浏览器打开亦被拦，取数用 curl（桌面 UA）。
2. `nb.ncha.gov.cn` 为**填报系统**，博物馆名录若需公开数据，应先看系统是否匿名展示，否则回退到年度报告公告与统计口径。
3. 国保名单**跨批次、跨栏目**，无统一「全部批次」单页；引用第 N 批须定位当批公布通知与附件。
4. 站内**未见可用站内检索**；找站内某文用外部引擎 `site:ncha.gov.cn`。
5. 部分旧栏目附件为扫描件或网页表格，抽取需逐页解析。
