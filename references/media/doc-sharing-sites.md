# doc-sharing-sites —— 文库分享站取材通道

- 去哪找：站点矩阵见 `## 细节`（首页 + 站内搜索页）；范围最广的入口是 **360搜索 `site:`**（见「怎么搜」）
- 什么时候用：官方未公开/已删除的实施方案、汇报、报告、合同范本、题库等文本；`wenku-mirrors.md`（51jzrc/人人文库/豆丁/道客巴巴/夸克/百度）之外的**补充站与存活现状核查**
- 怎么搜：把 `site:<域名> "<原文成句>"` 丢给 **360搜索**（本机 curl 直达、返回真实文档 URL）；各站站内搜索模板见表，SPA 站结果多为 JS 渲染
- 覆盖：境内 20+ 文库/文档分享站（含已停运者）；文档年代 2016–2026 为主
- 门槛：浏览普遍免费；**下载几乎都要登录 + 积分/金贝/VIP/付费**；无 key、无单位 IP
- 实测：2026-10-03，macOS(arm64) + curl（每主机 1–2 次状态探测）+ `read` 抽验文档页。示例：`https://www.so.com/s?q=site%3Amax.book118.com+实施方案` → 200 且正文含真实文档 URL；`read https://max.book118.com/html/2022/0530/5040024323004233.shtm` → 200 含「文本预览」正文；`read https://www.renrendoc.com/paper/252533477.html` → 200 含全文「文档简介」
- 上游：kill-doc 平台清单 <https://github.com/systemmin/kill-doc>、资源收藏夹文库页 <https://zyscj.com/zy/study/wenku.html>

## 细节

### 站点矩阵（2026-10-03 探测）

| 站名 | 域名 | 站内搜索入口 | 预览/下载门槛 | 实测状态 |
|---|---|---|---|---|
| 原创力文档 | `max.book118.com`（`www.book118.com`） | `https://max.book118.com/search.html?q=<kw>`（结果 JS 渲染，静态页只见空壳） | 文本预览免费（文档页静态 HTML 内嵌前若干页正文）；下载标 *VIP*/付费 | ✅ 首页 200(90KB)；搜索页 200；样本 200 取到正文 |
| 人人文库 | `renrendoc.com` | `https://www.renrendoc.com/search.html?q=<kw>`（结果 JS 加载） | 「文档简介」含正文（可能脱敏/OCR 讹字）；下载 20 积分 | ✅ 首页 200；搜索页 200；样本 200 取到正文（详见 `wenku-mirrors.md`） |
| 金锄头文库 | `jinchutou.com` | 首页搜索跳 `so.jinchutou.com/search.html`（GET 带 `q` 返回 404，疑需表单参数） | 「文本预览」含正文；下载 20 金贝 | ✅ 首页 200；样本 200（`/p-<id>.html` 302→`/shtml/<hash>.html`）取到正文 |
| 360文库 | `wenku.so.com` | `https://wenku.so.com/s?q=<kw>` ✅ | 登录 + 积分/VIP | ✅ 首页 200（9KB SPA）；搜索模板由结果页自身链接确认 |
| 百度文库 | `wenku.baidu.com` | `https://wenku.baidu.com/search?word=<kw>`；文档 `/view/<id>.html` | 部分预览免费；全文/下载需 VIP/下载券 | ⚠️ 首页/搜索页 200 但均为 SPA 空壳，本机未取到正文（详见 `wenku-mirrors.md`） |
| 淘豆网 | `taodocs.com` | 首页搜索框；移动版 `m.taodocs.com` | 阅读/下载需登录 + 积分 | ✅ 首页 200(310KB)；`/search/?q=` 200 但回落移动壳 |
| 豆丁建筑 | `jz.docin.com` | 同豆丁网 | 预览受限，登录看更多 | ✅ 首页 200(148KB)（**主站 `www.docin.com` 本机两次 502**） |
| 蚂蚁文库 | `mayiwenku.com` | 站内搜索 | 30 积分/篇 | ⚠️ 首页 503；样本 `/p-50140566.html` 200（元信息在，正文需 JS） |
| 道客巴巴 | `doc88.com` | 站内搜索 URL 未确认（`/search.html?q=` 404、`/search?q=` 非搜索页） | 预览需登录/积分（样本标 1300 积分） | ⚠️ 首页 200；样本 `/p-90729851704740.html` 200 但正文需 JS（详见 `wenku-mirrors.md`） |
| 七彩学科 | `7cxk.com` | 站内搜索（未取到模板） | 积分 | ⚠️ 首页 200 但返回「浏览器安全检查中」（JS 挑战） |
| 夸克文档 | `doc.quark.cn`（`vt.quark.cn`） | `https://doc.quark.cn/search?q=<kw>`（SPA）；文档 `/preview/<id>` | 登录/会员；本机浏览器打开曾崩溃 | ⚠️ 首页 200；搜索/预览页为 SPA 空壳（详见 `wenku-mirrors.md`） |
| MBA智库文库 | `doc.mbalib.com` | 站内搜索 | 会员 | ⚠️ 根域 404，未探到文库入口 |
| 爱问共享资料（爱问文库） | `ishare.iask.sina.com.cn` / `ishare.iask.com` | — | — | ❌ 证书过期 + 域名不解析 → 现状不可用 |
| 微传网 | `weizhuannet.com` | — | — | ❌ 两次超时（不可达，未验证） |
| 360doc 个人图书馆 | `360doc.com` | — | — | ❌ 两次超时（不可达） |
| 搜弘文库 | `wenku.chochina.com` | — | — | ❌ 两次超时（不可达） |
| 麦档网 | `maidangwang.com` | — | — | ⚠️ 503「站点正在建设中」（域名存疑，`maidang.com` 拒连） |
| 得力文库 | `deliwenku.com` | — | — | ❌ 根域与搜索路径均 404；360 无索引 → 疑停运 |
| 读根网 | `dugen.com` | — | — | ❌ 域名挂售（4.cn 停放页） |
| 文库吧 | `wenkuba.com` | — | — | ⚠️ 域名已转型为汉语字典站（`wenkuba.cn` 亦无关） |
| 文档之家 | `doczj.com` | — | — | ⚠️ 200「网站维护中」 |
| 天天文库 | `ttwenku.com` | — | — | ⚠️ 403 WAF |
| 第一文库网 / 快文库 / 汇文网 / 三一刀客 | `wenku1.com` / `kwenku.com` / `huiwenwang.cn` / `3ydoc.com` | — | — | ❌ 均不可达 |
| 无忧文档网 | `51jzrc.cn` | 站内搜索 | 免费 | ✅ 可 curl 直取全文，详见 `wenku-mirrors.md` |

### 检索通道（怎么定位文档页）

1. **360搜索 —— 本机 curl 唯一稳定拿到真实文档 URL 的引擎**：

   ```bash
   UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
   curl -sSk -L -m 25 -A "$UA" -H 'Accept-Language: zh-CN,zh;q=0.9' \
     'https://www.so.com/s?q=site%3Amax.book118.com+%E5%AE%9E%E6%96%BD%E6%96%B9%E6%A1%88'
   ```

   → 200，正文含 `max.book118.com/html/…shtm`、`doc88.com/p-*.html`、`renrendoc.com/paper/*.html`、`docin.com/p-*.html`、`jinchutou.com/p-*.html`、`doc.quark.cn/preview/*`、`wenku.baidu.com/view/*.html`、`mayiwenku.com/p-*.html`、`7cxk.com/p-*.html`。加引号可做精确短语：`site:<域名> "<原文成句>"`。
2. **头条搜索**：`https://so.toutiao.com/search?keyword=<site:…>` → 200（1.7MB，结果内联渲染，本轮未逐条解析）。
3. **必应**：curl 得壳页（`b_algo` 存在但结果需浏览器/cookie，`format=rss` 会**忽略** `site:`）→ 按 `wenku-mirrors.md` 走可见浏览器。
4. 搜狗（5.6KB 壳页）、百度（安全验证）、DuckDuckGo html（0 字节）本机均不可直用。
5. 已停运站仍有存量页被索引（docin、ishare 等）：`site:` 能定位链接，但打开可能已失效 → **命中即落盘**。

### 公开预览取文小抄（不破解付费）

- `read` 工具直读文档页即可得公开预览正文：**book118**（「文本预览」+ `meta-description` 含首段）、**金锄头**（「文本预览」）、**人人**（「文档简介」）、**蚂蚁**（`meta` 简介）。
- SPA 站（百度/夸克/道客巴巴/淘豆网/360文库）静态页无正文；正文在预览图/画布，非公开 HTML，需浏览器渲染。
- 积分/VIP 内容**不代下、不破解**；只取站点公开的预览文本作交叉比对。

## 坑

- **存活率低**：本轮 20+ 站里超半数不可达或转型（得力/读根/爱问/微传/360doc/文库吧…）；别把搜索引擎里的存量索引当成「站还活着」。
- **站名 ≠ 域名**：麦档网 `maidangwang.com`（域名存疑）、得力文库 `deliwenku.com`（已 404）；核域名先看 360搜索结果里的域名。
- **二手与脱敏**：上传版常见 `广西 XXXX 科技`、`世***` 之类脱敏，以及 OCR 讹字（人人文库样本把「第二种」识别成「其次种」、「必须」写成「必必须」）→ 只作交叉比对，关键人名/数字回官方源核实。
- **编码/协议**：多为 UTF-8；`51jzrc` 走 http 更稳（见 `wenku-mirrors.md`）。
- **版权**：仅用公开可访问页面；付费/积分下载属侵权高风险，勿用第三方「代下/破解」服务（kill-doc 类脚本原理仅截取浏览器已渲染的公开预览）。
