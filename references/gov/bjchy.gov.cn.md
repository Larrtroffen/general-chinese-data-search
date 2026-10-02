# bjchy.gov.cn —— 朝阳区政府门户

- 去哪找：
  - 新闻页（动态）：`http://www.bjchy.gov.cn/dynamic/zwhd/{16 进制 id}.html`
  - 示例：`…/dynamic/zwhd/8a24fe836274afa5016275d0fada0067.html`（2018-03-30 朝阳报：试点单位 11 个）、`…/dynamic/zwhd/8a24fe83622bebd801622cddc489000c.html`（2018-03-15 专题会）
  - 站内检索后端（不可直调）：`api.so-gov.cn`
- 什么时候用：要朝阳区区级新闻全文（朝阳报转载）、区财政绩效评价报告 PDF（`UserFiles/File/….pdf`，绩效报告里常回溯"试点单位"表述）。
- 怎么搜：
  - 站内检索接口为 JS 异步（`api.so-gov.cn`，需 `siteCode` 等参数），直连抓不到结果 → 优先：
    1. 搜狗微信搜「北京朝阳 / 朝阳报」账号与标题；
    2. `web_search`：`site:bjchy.gov.cn {关键词}`；
    3. 搜索引擎 `so.com` 站内：`site:bjchy.gov.cn 试点单位`（见 `../engines/so.com.md`）。
  - 已拿到页面的可推导：同栏目文章 id 相近，可小范围枚举 id 试取。
  - 抓取：
    ```bash
    curl -s -m 25 -A 'Mozilla/5.0 …' 'http://www.bjchy.gov.cn/dynamic/zwhd/8a24fe836274afa5016275d0fada0067.html' | iconv -f utf-8
    ```
- 覆盖：朝阳区政府门户新闻（2018 年新闻仍在线上），静态 HTML 正文含全文（朝阳报转载）。
- 门槛：免费、免登录；**HTTPS 不可用（443 握手失败），只能走 http**；抓取统一 `curl -sSk`。
- 实测：2026-10-02（站群实测，见 `beijing-districts.md`）：`www.bjchy.gov.cn` HTTPS 000（443 握手失败）/ http 200。
- 上游：<http://www.bjchy.gov.cn/>

## 细节

同类区门户：其余 15 区门户结构类似（`www.bjhd.gov.cn`、`www.bjfsh.gov.cn` 等），方法通用——动态新闻直连可抓；站内搜索一律 JS 异步，改用搜狗微信/360/`web_search site:` 定位。

## 坑

1. 只服务 http；HTTPS 连接失败。
2. 页面编码为 GB2312/GBK 系，`iconv -f gb18030 -t utf-8` 兜底（示例中 `-f utf-8` 为原文写法，遇到乱码改 gb18030）。
3. 站内检索不可直连（JS 异步 + `api.so-gov.cn`）。
