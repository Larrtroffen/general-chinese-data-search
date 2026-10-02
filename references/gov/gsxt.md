# gsxt.gov.cn —— 企业工商登记官方公示库

- 去哪找：
  - 首页 / 搜索框：`https://www.gsxt.gov.cn/index.html`（等价 `index.htm`）
  - 企业信用信息查询首页：`https://www.gsxt.gov.cn/corp-query-homepage.html`
  - 检索结果页（登录态/实名子域）：`https://shiming.gsxt.gov.cn/corp-query-search-1.html`
  - 登录：`https://shiming.gsxt.gov.cn/socialuser-use-login.html`
  - 个体/农合入口：首页同框，切换"企业/个体/农合"标签
  - 分省子站：`https://<省缩写>.gsxt.gov.cn/`，例：`sc.` `sn.` `hb.` `gd.` `bt.`（兵团）
  - 移动端：微信小程序 / 支付宝小程序"国家企业信用信息公示系统"、官方 APP
- 什么时候用：
  - 关键词：企业全称 / 统一社会信用代码 / 注册号 → 工商登记照面信息、股东、主要人员、分支机构。
  - 关键词：企业名 → **经营异常名录、严重违法失信名单**（招投标资格审查、供应商尽调）。
  - 关键词：企业名 → 年报公示、行政处罚（市场监管口径）、抽查检查结果。
  - 不适用：诉讼/执行（去 `../legal/court-open.md`）、信用红黑名单（去 `credit-china.md`）。
- 怎么搜：
  - **网页路径（唯一可靠）**：浏览器打开首页 → 顶部搜索框输入关键词 → 选择"企业/个体工商户/农民专业合作社" → 输入验证码/完成滑块 → 结果列表 → 点企业名进详情页。
  - **接口路径（上游声明，本机未验证）**：早期爬虫常用形态是 `GET/POST https://www.gsxt.gov.cn/corp-query-search-1.html?searchWord=<名称>` 承接结果页，业务数据由 `corp-query-*` 系列端点以 **POST + 前端计算 hash 的路径**返回 HTML 片段；具体 hash 与分页参数随版本变动，且必须携带挑战 cookie。**不要**照抄任何固定 hash —— 该站 2019 年后加了"每次会话生成路径"的动态防护。
  - 结果形态：结果页/详情页均为**服务端返回的 HTML 片段**（非 JSON），详情页字段以 `<table>` 排列；匿名直连会被 521 挡在首页外。
  - 依赖的客户端能力（缺一不可）：① 执行首页下发的加速乐挑战 JS → 得到 `__jsl_clearance_s` cookie；② 携带挑战 cookie 后再请求业务页；③ 查询时完成验证码 / 滑块（部分省份）。
- 覆盖：全国（含 31 省级 + 兵团）企业、个体工商户、农民专业合作社、分支机构；存续/注销主体当前状态，年报按年份（一般为 2014 年度起），异常名录为当前名单；粒度=单主体级 + 单条年报/异常记录；动态更新（登记机关录入后按日同步）。
- 门槛：免费、**无需登录**即可查登记照面信息与公示名单；**必须浏览器**（站点前置加速乐 Jiasule JS cookie 挑战，本机 curl 无论换 UA/Referer/协议均 521）；频繁查询会触发验证码/滑块；部分功能（年报填报、信用修复）需登录（实名）。
- 实测：2026-10-03，macOS，curl 8.x，桌面 UA + `Accept-Language: zh-CN`。`GET https://www.gsxt.gov.cn/index.html` → **521**（body 866 B，纯 JS：`document.cookie=('_')+('_')+('j')+('s')+…`，拼出 `__jsl_clearance_s=<值>`；加速乐挑战）；换 Windows Chrome/120 UA + `Referer: https://www.gsxt.gov.cn/` → **521**（871 B，同挑战，换 UA 无效）；`GET http://www.gsxt.gov.cn/index.html` → **307**（降级协议同样被挑战）；`GET http://gsxt.gov.cn/`（无 www）→ **000**（DNS 解析失败 → 该域名仅 `www.` 有效）。
- 上游：<https://www.gsxt.gov.cn/index.html>、<https://www.gsxt.gov.cn/corp-query-homepage.html>、<https://shiming.gsxt.gov.cn/corp-query-search-1.html>、分省子站示例 <https://sc.gsxt.gov.cn/index.html> / <https://sn.gsxt.gov.cn/index.html> / <https://hb.gsxt.gov.cn/index.html>；规则依据（官方提示）：《市场主体登记管理条例》实施细则、《市场监管总局办公厅关于调整营业执照照面事项的通知》 <https://www.samr.gov.cn/zw/zfxxgk/fdzdgknr/djzcj/art/2023/>

## 细节

市场监管总局主办，营业执照照面信息（名称、统一社会信用代码、法定代表人、注册资本、经营范围、登记机关、成立日期、经营状态）+ 年报 + 经营异常名录 + 严重违法失信名单的**唯一官方**公示库。**本机状态：全站 521 / 加速乐 JS 挑战，CLI 完全不可用；须真实浏览器。**

对比：搜索引擎可正常收录 gsxt 各子站页面正文（说明挑战可被真实浏览器/爬虫解出），**本机 CLI 受限是能否执行挑战 JS 的问题，不是站点无此数据**。

## 坑

1. 加速乐 JS 挑战 + 会话级动态路径，固定 hash / 直连均不可用。
2. 查询触发验证码/滑块；高频访问会被限。
3. 无 www 的 `gsxt.gov.cn` DNS 不解析；http 会被 307 挑战。
4. 分省子站内容与总站同源，按省下钻可用于减少验证码触发。
