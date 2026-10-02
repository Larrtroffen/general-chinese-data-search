# commercial-databases —— 商科研究商业数据库总卡

- 去哪找：**CSMAR 国泰安** `https://data.csmar.com/`（旧域名 `gtarsc.com` 已停用）；**CNRDS 中国研究数据服务平台** `https://www.cnrds.com/`；**CEIC** `https://www.ceicdata.com/`（中国大陆跳转 `https://www.ceicdata.com.cn/zh-hans`）；**Wind 万得** `https://www.wind.com.cn/`。
- 什么时候用：要**中国上市公司财务/治理/股价/事件面板**（CSMAR）、**中国研究用特色数据库**（CNRDS：ESG、文本、专利、政府等）、**宏观经济时间序列**（CEIC）、**金融终端级行情与一致预期**（Wind）——即"官方统计拿不到的结构化面板"。
- 怎么取：**均需订阅/机构授权**，无公开 API 直取；申请路径——校园用户走**本校图书馆数据库导航**（多数 985/211 已购 CSMAR/CNRDS/Wind，凭学号或校内 IP）；非校园用户联系厂商销售开通试用/付费账号。数据以网页查询导出或随附客户端/SDK 取用。
- 覆盖：CSMAR（股票、财务、治理、基金、债券、宏观等）；CNRDS（上市公司特色库、文本、ESG、政府/区域）；CEIC（全球与中国宏观，长序列）；Wind（全品种金融终端 + Excel 插件）。
- 门槛：**付费/机构订阅**；CEIC/CSMAR/CNRDS 有高校版；Wind 以终端席位计费。**无免费匿名数据接口**（实测）。
- 实测：2026-10-03，macOS arm64 curl 8.x（桌面 UA）——`https://data.csmar.com/` `200/2243 B`（SPA 壳，`<title>CSMAR`）；`https://www.gtarsc.com/` HTTPS 证书**已过期**（`-k` 后 `200`，页面提示"该域名已不再使用，请访问 data.csmar.com"）；`https://www.cnrds.com/` `302 → /Home/Login` `200/347 KB`（`<title>Chinese Research Data Services Platform`）；`https://www.ceicdata.com/` `302` 链 → `https://www.ceicdata.com.cn/zh-hans`（`202`，CloudFront 地理跳转）；`https://www.wind.com.cn/` `200/9 KB`（`<title>万得信息网`）。
- 上游：各厂商官网（见上）。

## 细节

### 定位与获取方式对照

| 库 | 域名 | 面向 | 覆盖 | 获取 |
|---|---|---|---|---|
| CSMAR 国泰安 | `data.csmar.com` | 高校/券商/基金研究 | A股财务·治理·事件·基金·债券·宏观 | 机构订阅；高校图书馆入口 |
| CNRDS | `cnrds.com` | 学术研究 | 上市公司特色库·文本·ESG·专利·政府 | 注册（学术邮箱）+ 机构订阅 |
| CEIC | `ceicdata.com` / `.com.cn` | 宏观研究/投研 | 全球>200 经济体长序列 | 订阅；部分高校有 |
| Wind 万得 | `wind.com.cn` | 全行业金融从业 | 全品种行情/数据/一致预期 | 终端席位付费 |

- **域名变更提醒**：CSMAR 旧域 `www.gtarsc.com` 已下线（HTTPS 证书过期 + 提示跳 `data.csmar.com`），旧脚本/书签需替换。
- CEIC 国际站会对中国大陆访客 `302` 到 `www.ceicdata.com.cn`（`CloudFront` 设 `geolocated`/`china` Cookie）。

### 与免费源的组合策略

- **先免费后商业**：宏观数值优先 `../stats/`（国家统计局、`../stats/data.stats.gov.cn.md`）；上市公司**公告原文**优先 `cninfo.com.cn.md`（免费）；只有需要**已清洗的结构化面板**（财务附注、治理变量、事件窗口）时才上 CSMAR/CNRDS。
- **论文复现**：C刊常见"CSMAR + Wind"口径，引用时须写明**库名 + 表名 + 下载日期 + 版本**，否则无法复现。
- 免费替代线索：`akshare`（`../stats/akshare.md`）封装了部分行情/财务，但**不等于** CSMAR 的清洗口径。

## 坑

1. **无公开 API**：四家均登录后才可导出；本机匿名只到登录/门户页，**未验证登录态取数流程**。
2. CSMAR 新旧域名并存会误导脚本；以 `data.csmar.com` 为准。
3. CEIC 的地理跳转可能把请求导向 `.com.cn`，接口域名随之变化。
4. 授权范围（可用于论文/能否再分发）随合同而定，**二次分发数据前务必查 license**。
5. 校园 IP 仅覆盖已购库；跨校访问需各自机构授权，勿共用账号（多数许可禁止）。
