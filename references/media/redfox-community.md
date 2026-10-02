# redfox-community —— 红狐数据社媒检索 API

红狐数据社区维护的 100+ 枚 Agent Skill，全部围绕**社媒平台检索/热榜/下载**：公众号、抖音、小红书、B站、微博、快手、视频号、今日头条、X(Twitter)、TikTok、YouTube、Instagram。每个技能背后是同一套 `redfox.hk` 的 **付费 `POST /story/api/...` 接口**。对 media 层是**社媒补充通道**（尤其"公众号搜索""微博热搜""今日头条搜索"）——与 `../wechat/`、`../social/` 有重叠，重点在"一个 KEY 打通多平台"。

- 去哪找：repo <https://github.com/redfox-data/redfox-community>（上游仓内：`skills/<name>/SKILL.md` + `scripts/*.py` + `references/api-reference.md`）；API Host `https://redfox.hk`（Method `POST`，`Content-Type: application/json`）；申请 KEY <https://redfox.hk/settings/api-keys>；接口总表 `skills/global-ai-news-brief/references/api-reference.md`
- 什么时候用：要跨平台社媒检索/热榜/舆情（媒体层里微信/微博/抖音的补充）；或要"全网搜索 + 热点聚类"式情报简报。
- 怎么搜：鉴权与调用形态来自源码。
  - 鉴权：请求头 `X-API-KEY: <key>`；KEY 来源三选一——环境变量 `REDFOX_API_KEY=ak_…`、`--api-key` 参数、或 `~/.qoder/apis/redfox.json`。
  - 用法：clone 后 `python3 skills/gzh-search/assets/search.py "关键词" --count 50`（终端表格 + CSV + 交互式 HTML）。
- 覆盖：11 个平台（公众号/微博/头条/抖音/小红书/B站/快手/视频号/TikTok/Instagram/X/YouTube 检索）。
- 门槛：**付费 KEY**（`redfox.hk` 注册）；公众号只覆盖近 30 天"腰部以上"账号，关键词 ≤10 字符。
- 实测：2026-10-03，macOS：通过 `gh api` 读取 `README.md`、`skills/gzh-search/SKILL.md`、`skills/gzh-search/assets/search.py`（确认 `API_URL=https://redfox.hk/story/api/gzh/data/searchArticle`、`X-API-KEY` 头、`REDFOX_API_KEY` 环境变量）、`skills/global-ai-news-brief/references/api-reference.md`（确认下 11 个平台端点）、`git/trees` 确认 100+ 技能目录；**未持 key，未调用任何 API**。
- 上游：<https://github.com/redfox-data/redfox-community>（无 LICENSE）

## 细节

### 代表端点（均来自上游仓内 `references/api-reference.md` / 各 `scripts/*.py`，均为 `POST`）

| 平台 | 端点 |
|---|---|
| 公众号文章搜索 | `/story/api/gzh/data/searchArticle` |
| 微博热搜 | `/story/api/weibo/ability/hotSearch` |
| 今日头条搜索/详情 | `/story/api/toutiao/searchWork`、`/story/api/toutiao/workDetail` |
| 抖音搜索 | `/story/api/dy/data/searchWork` |
| 小红书搜索 / 用户笔记 | `/story/api/xhs/search/search`、`/story/api/xhsUser/searchArticle` |
| B站作品搜索 | `/story/api/bili/data/workSearch` |
| 快手 / 视频号 | `/story/api/ksAllData/searchWork`、`/story/api/sphAllData/searchWork` |
| TikTok / Instagram / X / YouTube | `/story/api/tiktok/ability/searchVideo`、`/story/api/ins/search`、`/story/api/x/search`、`/story/api/youtube/searchVideo` |

### 代表技能（按平台）

- 公众号 `gzh-search`/`gzh-subscribe`；微博 `weibo-hot-search`/`weibo-realtime-search`/`weibo-post-search`；头条 `toutiao-search`；抖音 `douyin-search`/`douyin-hot-trend`；小红书 `xiaohongshu-search`/`-dailytop`/`-top-account`；B站 `bilibili-search-download`；海外 `twitter-work-search`/`tiktok-topic-aweme-list`；聚合 `multi-content-feed`/`trending-hub`/`global-ai-news-brief`（11 平台聚合 + AI 摘要）。

## 坑

- **付费**：所有 API 需注册获取 API KEY（本机未持 key，未实测）；额度/计费见官网。
- 抓取范围受限（如公众号只覆盖近 30 天"腰部以上"账号；关键词 ≤10 字符）。
- 仓库**无 LICENSE**——只记平台/端点/用法，**不复制其代码**。
- 平台接口随对方反爬变化，稳定性取决于 redfox 服务。
