# shclearing.com.cn —— 银行间清算统计与披露

- 去哪找：门户 `https://www.shclearing.com.cn/`；业务数据（统计日报）`https://www.shclearing.com.cn/cpyyw/ywsj/tjrb/`；债券信息披露·发行披露 `https://www.shclearing.com.cn/xxpl/fxpl/`。
- 什么时候用：要**上清所口径**的银行间市场债券**发行披露与要素**（超短融 SCP、中票 MTN、PPN、CRMW 等）、清算/托管等**业务数据日报**、指数与估值披露、兑付注销公告。
- 怎么搜：两类路径——① **信息披露/发行披露是服务端渲染文章页**，可直接抓，URL 形如 `https://www.shclearing.com.cn/xxpl/fxpl/{品种码}/{YYYYMM}/t{YYYYMMDD}_{序号}.html`（品种码如 `crmw`、`mtn`、`scp`）；② **业务数据（统计日报）是 Vue 单页 + 加密签名接口**，页面加载 `crypto-js.js` / `md5.js` / `sm3.js` / `ase.js` / `verify.js`，curl 取不到数据，**仅浏览器**。
- 覆盖：银行间债券各品种的发行与存续期信息披露；业务数据含清算量、托管量等（日报/月报）；全国银行间市场口径。
- 门槛：浏览免费；业务数据接口需浏览器（JS 签名）。
- 实测：2026-10-03，桌面 UA curl——`GET https://www.shclearing.com.cn/` `200/316,156 B`（UTF-8）；`GET /cpyyw/ywsj/` `200/429 B`（JS 跳转 `./tjrb/`）；`GET /cpyyw/ywsj/tjrb/` `200/45,620 B`（页面壳，数据由 JS 渲染）；`GET /xxpl/fxpl/` `200/46,007 B`，正文含服务端渲染文章链接 `./crmw/202609/t20260930_1876868.html`、`./mtn/202609/t20260930_1876814.html`、`./scp/202609/t20260930_1876797.html` 等。
- 上游：`https://www.shclearing.com.cn/`（银行间市场清算所股份有限公司 / 上海清算所）。

## 细节

### 栏目与路径

| 栏目 | URL |
|---|---|
| 产品与业务 | `/cpyyw/cpyw/` |
| 业务数据 | `/cpyyw/ywsj/` → JS 跳 `/cpyyw/ywsj/tjrb/`（统计日报） |
| 发行披露 | `/xxpl/fxpl/` |
| 发行情况报告 | `/xxpl/fxqkbg/` |
| 指数信息披露 / 估值与指数 | 门户导航「估值与指数」下 |
| 清算会员 | `/scfw/qshy/` |

- 信息披露文章页 URL 规律：`/xxpl/fxpl/{品种码}/{YYYYMM}/t{YYYYMMDD}_{序号}.html`，品种码与债券种类对应（`crmw` 信用风险缓释、`mtn` 中票、`scp` 超短融…）。
- 业务数据页前端依赖：`jquery-3.7.1`、`vue.min.js`、`crypto-js.js`、`md5.js`、`sm3.js`、`base64.js`、`ase.js`、`verify.js`（前端签名/加密栈）。

## 坑

1. `/cpyyw/ywsj/` 是 **JS 跳转页（429 B）**，`curl -L` 不跟 `window.location`；要直连 `…/ywsj/tjrb/`。
2. **统计日报数据不在 HTML 内**（Vue 渲染 + 签名接口），curl/requests 拿空壳——须浏览器（见 `../tools/agent-browser.md`），别把它当"页面无数据"。
3. 与中债分工：**上清所**=银行间清算/托管 + 债务融资工具发行披露；**中央结算公司/中债**=国债/地方债等登记托管 + 收益率曲线（见 `../business/chinabond.com.cn.md`）。两者披露品种不重叠。
4. 发行披露正文/附件多为 HTML 或 PDF 挂链，按品种目录遍历；注意月份目录命名差异。
