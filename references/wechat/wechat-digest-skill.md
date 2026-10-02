# wechat-digest-skill —— 后台凭证按号采集与断点续采

Claude Skill / 纯 CLI（Python，MIT，81★，Jackychen-12）：以**微信公众平台后台 `searchbiz`+`appmsg`** 为核心，
按公众号名称拉全文 → 落 JSON+Excel → 攒本地知识库 → 出离线 HTML。
**它最有价值的部分是「失败模式」的实测结论**（对设计我们自己的采集重试逻辑极有用）。

- 去哪找：repo https://github.com/Jackychen-12/wechat-digest-skill ；脚本 `wechat_collector.py`（采集）、`kb.py`（知识库）、`render_html.py`（离线页）；凭证模板 `credentials.example.json`。
- 什么时候用：要**按号全量全文**且接受「后台凭证」路线；需要**频控/风控/断链的可判定状态机**（`contentStatus`）设计参考；要「中断不丢进度、跨天续采」的大号历史抓取。
- 怎么取：
  ```bash
  git clone https://github.com/Jackychen-12/wechat-digest-skill.git ~/.claude/skills/wechat-digest-skill
  pip install -r requirements.txt                 # requests + openpyxl
  cp credentials.example.json credentials.json    # token = mp.weixin.qq.com 地址栏 token= 后纯数字；cookie = F12 任请求 Request Headers 整条
  python3 wechat_collector.py whoami              # 校验登录态
  python3 wechat_collector.py collect 晚点LatePost --since 2025-01-01 --count 10 --resume
  python3 wechat_collector.py collect-urls urls.txt   # 托底：给 URL/RSS，走文章公开页（与 appmsg 两套限流）
  ```
- 覆盖：文章级（`id`(sn 去重)/标题/摘要/链接/封面/正文内图片 URL 列表/发布日期/正文纯文本）；`contentStatus` 七态 `ok|digest|empty|share|blocked|gone|invalid`，并区分「可重试 / 重试无用 / 不可恢复」；**明确不含阅读数/点赞/在看**（需客户端签名参数）。
- 门槛：需自备公众号后台 token + cookie（几小时~几天过期）；MIT
- 实测：2026-10-02 读 `SKILL.md`(22866B)/`README.md`(9174B)，**未运行脚本**（无凭证）。`gh api repos/Jackychen-12/wechat-digest-skill --jq '.license.spdx_id,.stargazers_count'` → `MIT / 81`。
  下述 `200009/200013/blocked` 三条为**上游声明（其自称以真实凭证验证）**，未本机复现。
- 上游：https://github.com/Jackychen-12/wechat-digest-skill

## 细节

### 上游实测结论（决定流程设计的关键事实）

- `search`（`operate_appmsg?action=search_article`）**不存在**：登录态有效时也返回 `ret=200009 not found` → 后台**没有全网文章搜索**，别指望它替代搜狗。
- 频控 `ret=200013` **绑在公众号账号（bizuin）上**：换 cookie、换 token、重新登录、隔天重试**均无效**；额度还分接口——`searchbiz` 宽松，`appmsg` 拉别人的文章列表极紧。
- 凭证失效 `ret=200003`；`blocked` 验证页要**看最终 URL** 才认得出（302 到 `/mp/wappoc_appmsgcaptcha?poc_token=…`，页面 `<title>` 为空的空壳），只看 HTML 会误判成「空正文」。
- `--resume`：每页 appmsg 请求都算配额，不加断点会从头重拉。
- 频控冷却默认 300s 逐次翻倍，失败落 `*_partial.json/.xlsx`，退出码 130。

## 坑

- `collect` 一旦被标记基本无解（转 `collect-urls`）。
- 上游自述仅个人学习研究用途。
- 凭证几小时~几天过期，需自备。
