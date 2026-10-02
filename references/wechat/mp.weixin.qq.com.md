# mp.weixin.qq.com —— 单篇文章正文与元数据抓取

微信文章公开页：**只要已有文章链接**（搜狗签名链接或永久链接）即可 curl 直取正文与元数据；本身**没有检索入口**。

- 去哪找：文章页两种 URL 形态——
  - 搜狗签名链接：`https://mp.weixin.qq.com/s?src=11&timestamp=1790866185&ver=7000&signature=…&new=1`（由 `weixin.sogou.com.md` 的 `/link` 解析得到；`timestamp` 为签发时间、`signature` 为校验串，响应头带 `expires`，实测签发后约 8 分钟）；
  - 永久链接：`https://mp.weixin.qq.com/s?__biz=…&mid=…&idx=…&sn=…`（在正文页的 `var msg_link = "…"` 中取得，需先抓一次正文）。
- 什么时候用：**已有链接、只要正文 + 元数据**时；抓搜狗召回的老文章、需判定「还活着 / 已删 / 受限」时；需要文章永久链接 `__biz/mid/idx/sn` 做去重主键时。
- 怎么取：
  ```bash
  UA='Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
  curl -s -m 25 -A "$UA" -H 'Referer: https://weixin.sogou.com/' '<签名链接>' -o article.html
  ```
  页面为服务端渲染 HTML，正文在 `<div id="js_content">`；元数据在页内 JS 变量中（`var msg_title`/`var msg_desc`/`var msg_link`/`var nickname`/`var ori_head_img_url`，部分文章带 `var msg_source_url`）——详见「细节」。结果形态：**HTML（需解析）**。
- 覆盖：单篇；文章级（标题 / 摘要 / 正文 / 公众号名 / 头像 / 永久链接）；**无按号枚举能力**（见「坑」）。
- 门槛：无（公开页面直取，无需登录、无验证码；签名链接有时效，部分老文章已删）
- 实测：2026-10-01/02——iPhone UA 下签名链接直接返回 **HTTP 200**（无需登录、无验证码），正文页 HTTP/2 200、单篇 1s 级；批量抓间隔 ≥1s（脚本 `scripts/mp_article.py`，含 deleted/blocked 判定与 `.md`/`.json` 落盘）。
- 上游：https://mp.weixin.qq.com/ （无独立 repo；签名链接来自 `weixin.sogou.com.md`）

## 细节

### 正文与字段提取

- 页面为服务端渲染 HTML，正文在 `<div id="js_content">`。
- 元数据在页内 JS 变量：
  - `var msg_title = "标题";`
  - `var msg_desc = "摘要";`
  - `var msg_link = "http://mp.weixin.qq.com/s?__biz=…"`（永久链接）
  - 公众号名：`var nickname = "…";`、`var ori_head_img_url = "…";`
- 提取正文文字：`#js_content` 内 `p/span/section` 的文本；图片为 `data-src` 懒加载（原始 `src` 是占位图）。
- 部分文章带「阅读原文」跳转 `var msg_source_url`。

### 签名链接页的实测真相（2026-10-01/02）

- **`msg_link` 常为空**：`src=11&timestamp=…&signature=…` 形态的页面里 `var msg_link = "";`，且 `var sn = "";` 也可能为空 → 拼不出永久链接。**文章唯一标识改用 `var biz` + `var mid` + `var idx`**（可用于去重与断链后重找）。若 `sn` 非空，可拼 `https://mp.weixin.qq.com/s?__biz={biz}&mid={mid}&idx={idx}&sn={sn}`。
- **受限/错误页识别**：页面约 32KB、无 `msg_title`、`js_content` 正文为空（样例：一条「报告推荐」文 `msg_title=""`、`body=""`）；用浏览器渲染同一链接显示 "System error"。批抓时应把「无标题且正文为空」判为失败并重试/重解析，不要落成空语料。
- **解析坑**：用 `page.find('js_content')` 会先命中页面脚本（得到 1.6MB 的 JS 垃圾，实测坑）；必须用 `id="js_content"` 定位、以 `</div>\s*<script` 为正文结束边界。
- **变量取值坑**：`var` 行可能是拼接式（`var biz = "Mzg4NjEwNjEyNQ==" || "";`）→ 正则要取该行全部引号串拼接，再 `html.unescape`（否则拿到带 `||` 的脏值）。

## 坑

- 不能按公众号枚举历史文章（需登录态/接口 token），只有拿到文章链接才能逐篇抓。
- 老文章（2018）有的已删除或需关注才可见；删除文章返回「该内容已被发布者删除」或跳转错误页。
- 批量抓取注意频率（微信对高频请求有风控），建议间隔 ≥1s，失败退避重试。
