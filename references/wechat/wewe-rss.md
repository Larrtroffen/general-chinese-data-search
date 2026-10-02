# wewe-rss —— 公众号订阅转 RSS 服务

把公众号变成标准 RSS/Atom/JSON feed 的自托管服务：后台定时拉历史与新文章、可出全文、可导 OPML。
Node/TypeScript，MIT，约 9.7k★。**与搜狗互补**：搜狗负责关键词召回，它负责「订阅某号后持续增量」。

- 去哪找：repo https://github.com/cooderl/wewe-rss ；镜像 `cooderl/wewe-rss:latest`（MySQL）/ `cooderl/wewe-rss-sqlite:latest`；部署清单 `docker-compose.yml`、`docker-compose.sqlite.yml`；feed 端点 `{SERVER_ORIGIN_URL}/feeds/{feedId}.{rss|atom|json}`、聚合源 `/feeds/all.atom`。
- 什么时候用：要「按公众号订阅 + 定时增量 + 机器可读 feed」时（公众号 RSS / 订阅 / 增量更新 / feed 化 / OPML / fulltext）。
  **不要**用于：按关键词全网检索（走 `weixin.sogou.com.md`）、要阅读数/点赞数（feed 不含）、要 2018 前的冷门老号（受微信读书收录限制）。
- 怎么取（最小可复现）：
  ```bash
  docker network create wewe-rss
  docker run -d --name db -e MYSQL_ROOT_PASSWORD=123456 -e TZ='Asia/Shanghai' \
    -e MYSQL_DATABASE='wewe-rss' -v db_data:/var/lib/mysql --network wewe-rss \
    mysql:8.3.0 --mysql-native-password=ON
  docker run -d --name wewe-rss -p 4000:4000 -e AUTH_CODE=123567 \
    -e DATABASE_URL='mysql://root:123456@db:3306/wewe-rss?schema=public' \
    --network wewe-rss cooderl/wewe-rss:latest
  ```
  登录 `http://<host>:4000` → **微信读书扫码**加账号（别勾「24 小时后自动退出」）→ 提交公众号分享链接订阅 →
  `curl 'http://<host>:4000/feeds/MP_WXS_123.json?limit=30&title_include=张三|李四'`；手动刷新 `/feeds/MP_WXS_123.rss?update=true`。
  结果形态：**RSS/Atom/JSON feed + 全文**。
- 覆盖：公众号历史发布文章（文章级：标题/正文/时间/链接）；定时 `CRON_EXPRESSION`（默认 `35 5,17 * * *`，`UPDATE_DELAY_TIME=60s`）；`FEED_MODE=fulltext` 输出全文；`AUTH_CODE` 保护接口（`/feeds` 路径不校验）；许可 MIT。
- 门槛：需扫码登录**微信读书账号**（凭据自持）；自托管需 Docker + MySQL/SQLite
- 实测：2026-10-02 未部署（未跑 Docker/未扫码）。已做证据：`gh api repos/cooderl/wewe-rss --jq '.license.spdx_id,.stargazers_count,.pushed_at'` → `MIT / 9657 / 2026-03-20`；`curl -o /dev/null -w '%{http_code}' https://weread.111965.xyz` → **502**（默认转发服务本次不可达，仅影响默认 `PLATFORM_URL`）。
- 上游：https://github.com/cooderl/wewe-rss

## 细节

### 何时优于/不如搜狗

- 优于搜狗：搜狗只能按关键词召回**被索引的**文章且无时间过滤；本服务订阅某号后**按时间序全量增量**推送，适合「长期盯 10~50 个号」。
- 不如搜狗：只做一次性关键词普查（如「双井街道 吹哨报到 2018」）时，搜狗直接给结果，无需先知道要订哪些号。

## 坑

- ① 需扫码登录**微信读书账号**，凭据自持；② 添加订阅过频会被封控（「今日小黑屋」，等 24h）；
- ③ 部分请求经第三方转发 `weread.111965.xyz`，国内 DNS 问题可换 `weread.965111.xyz`；④ 不提供阅读/点赞数；
- ⑤ 覆盖受微信读书收录限制；⑥ 自托管需 Docker + MySQL/SQLite。
