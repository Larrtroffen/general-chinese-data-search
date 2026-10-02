# taoist.org.cn —— 道教协会官网栏目

- 去哪找：**中国道教协会**`http://taoist.org.cn/`（**非 www**；`www.taoist.org.cn` 被 WAF 拦）；栏目 `welcome.jsp`（首页）、`zgdjxh.jsp`（协会）、`zzjg.jsp`（组织机构）、`getDjzsByC2Action.do?c2=<栏目码>`（列表）、`zgdjzz.jsp`（《中国道教》杂志）。
- 什么时候用：要**中国道教协会的协会介绍、组织机构、历届理事会、法规制度、道教学院与文化研究所**等团体信息；作为宗教团体口径的线索（政策原文回 `sara.gov.cn.md` / `zytzb.gov.cn.md`）。
- 怎么搜：站点为 JSP + `.do` action 的**动态 HTML**，免登录：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
  curl -sS -k --tlsv1.2 -A "$UA" --compressed -L 'https://taoist.org.cn/'    # → 200，落到 http://taoist.org.cn/loadData.do
  curl -sS -A "$UA" --compressed 'http://taoist.org.cn/getDjzsByC2Action.do?c2=ljlsh'   # 历届理事会
  ```
  结果形态：**HTML**（列表页经 `?c2=<栏目码>` 参数切换，如 `ljlsh` 历届理事会、`gzzd` 法规制度、`xy` 道教学院、`yjs` 研究所）。
- 覆盖：协会与组织机构静态介绍、历届理事会、法规制度、道教学院、文化研究所、《中国道教》杂志目录；更新频率低（团体栏目）。
- 门槛：**免费、免登录、无 key**；**www 子域被盘云 WAF（`X-Panyun-Error-Step`）拦**，须用裸域。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA——`https://www.taoist.org.cn/` → LibreSSL **SSL handshake failure**，`http://www.taoist.org.cn/` → **403**（`Server: panyun`，`X-Panyun-Error-Step: 5`）；`https://taoist.org.cn/` → **200**（11 KB，`<title>中国道教协会</title>`，最终 URL `http://taoist.org.cn/loadData.do`）；`http://www.taoist.org.cn/zgdjxh.jsp` → 200（3 KB）；Chromium 打开 `www.taoist.org.cn` → `net::ERR_BLOCKED_BY_CLIENT`。
- 上游：<http://www.taoist.org.cn/>（中国道教协会）。

## 细节

- 导航栏目（首页实测）：`welcome.jsp` 首页、`organization.jsp` 道协组织、`zgdjxh.jsp` 协会、`zgdjxhjj.jsp` 简介、`zzjg.jsp` 组织机构、`getDjzsByC2Action.do?c2=ljlsh` 历届理事会、`…?c2=gzzd` 法规制度、`…?c2=xy` 中国道教学院、`…?c2=yjs` 道教文化研究所、`zgdjzz.jsp`《中国道教》杂志。
- 无公开 JSON API；列表页靠 `c2` 参数路由。

## 坑

1. **域名敏感**：`www.taoist.org.cn` 被盘云 WAF 拦（浏览器也报 `ERR_BLOCKED_BY_CLIENT`），改用 `taoist.org.cn`（无 www）。
2. **https 协商抖动**：`www` 的 https 在 LibreSSL 下握手失败；裸域 https 会 302 到 http，直接走 http 更稳。
3. 站点内容偏团体介绍，**无名录/统计数据**；道教活动场所检索回 `sara.gov.cn.md`。
4. 非官方仿站多（如 `daoisms.org→daoisms.com.cn` 等），引用须认准 `taoist.org.cn`。
