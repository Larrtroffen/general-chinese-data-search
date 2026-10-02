# tieba.baidu.com —— 地方讨论线索检索

贴吧可作地方话题/民间讨论的补充线索（如某街道居民反映的帖子），但**本机出口 IP 被「百度安全验证」拦死**：站内搜索、吧首页、移动版一律 403，连 `www.baidu.com` 网页搜索也被 302 到图形验证码。

- 去哪找：吧内搜索 `https://tieba.baidu.com/f/search/res?ie=utf-8&qw={kw}`、吧首页 `https://tieba.baidu.com/f?kw={吧名}`、移动版 `https://tieba.baidu.com/mo/q/m?kw={吧名}`。
- 什么时候用：要**地方话题/民间讨论**的补充线索时（注意本机当前不可直连）。
- 怎么搜：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
  curl -s -o /tmp/tb.html -w '%{http_code}\n' -m 20 -A "$UA" \
    'https://tieba.baidu.com/f/search/res?ie=utf-8&qw=%E8%A1%97%E4%B9%A1%E5%90%B9%E5%93%A8'
  grep -o '<title>[^<]*' /tmp/tb.html        # → <title>百度安全验证
  ```
  结果形态：**HTML**（本机返回安全验证页）。
- 覆盖：站内搜索 / 吧首页 / 移动版；本机（该 IP/时段）**全部不可直连**。
- 门槛：无账号门槛，但**本机 IP 被百度安全验证拦截**（需换网络/人工过验证）
- 实测：2026-10-02，macOS（arm64），curl 8.x（`-m 20`，桌面/iPhone UA，同主机间隔 ≥1.5s）：`tieba.baidu.com/f/search/res?ie=utf-8&qw=街乡吹哨` → 403/2551 B；`tieba.baidu.com/f?kw=北京` → 403/2506 B；`tieba.baidu.com/mo/q/m?kw=北京` → 403/2512 B（三次均 `<title>百度安全验证`）；`www.baidu.com/s?wd=site:tieba.baidu.com 街乡吹哨` → 302 → `wappass.baidu.com/static/captcha/tuxing_v2.html`。
- 上游：https://tieba.baidu.com/

## 细节

### 可用性矩阵（本机实测 2026-10-02，macOS + curl）

| 通道 | URL | 状态 | 现象 |
|---|---|---|---|
| 吧内搜索 | `https://tieba.baidu.com/f/search/res?ie=utf-8&qw={kw}` | ❌ 403 | 2551 B，`<title>百度安全验证`；页内引用 `captcha-1.baidu.com/v1/webapi/static`、`captcha.js` |
| 吧首页 | `https://tieba.baidu.com/f?kw={吧名}` | ❌ 403 | 2506 B，同款安全验证页 |
| 移动版 | `https://tieba.baidu.com/mo/q/m?kw={吧名}` | ❌ 403 | 2512 B，同款安全验证页 |
| 兜底：百度网页搜索 | `https://www.baidu.com/s?wd=site%3Atieba.baidu.com%20{kw}` | ❌ 302 | → `https://wappass.baidu.com/static/captcha/tuxing_v2.html?...&backurl=…`（图形验证码） |

**结论**：本机（该 IP/时段）对百度系（`tieba.baidu.com` + `www.baidu.com`）**全部落到安全验证/图形验证码** → 贴吧当前不可直连采集。

### 可用路径（前两条本机未验证）

1. **换出口网络/换时段**：安全验证常与 IP 段（机房/VPN/代理）绑定；家宽 + 浏览器人工过一次码后 cookie 通常可复用。
2. **浏览器人工打开**目标吧/搜索页，过验证后导出 cookie，再用 curl 复用 cookie jar（**未验证**）。
3. **改用其它引擎做 `site:` 点查**：头条搜索（`../engines/so.toutiao.com.md`）、必应中国（`../engines/cn.bing.com.md`）、搜狗网页 —— 注意本机 `www.baidu.com` 也已被验证码拦（见上表），不要用它兜底。
4. 贴吧**不适合做「按单位逐年」语料**：帖子无稳定机构归属、时间线不可靠、删帖率高 —— 优先级应低于政府网站与公众号。

## 坑

1. **别把 403 当限流**：返回体是「百度安全验证」HTML（含 `captcha` 资源引用），不是 JSON 限流响应；原样重试无效，须换网络/过验证。
2. 本机对百度系整体收紧：同批实测中 `www.baidu.com/s?wd=…` 也 302 到图形验证码 —— 比 `../engines/baidu.com.md` 记录的「桌面首次可、翻页才验证」更严，说明该 IP/时段阈值更低；**做批量前先探一次**。
3. 未验证：带 cookie 后各入口的真实可用性；是否存在免验证的移动端/开放接口。
