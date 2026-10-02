# wechat/ —— 微信公众号采集通道索引

微信公众号没有公开搜索/枚举 API。本目录收录多条**互补**通道，各有明确适用边界——先按「你要什么」选（见「选路」）。
A 组（`weixin.sogou.com.md`、`mp.weixin.qq.com.md`、`wechatspider.md`）是本机实测通道；B 组（自建服务/后台凭证）、C 组（单篇/整号下载器）是**来源卡**（只记录「去哪找、需要什么钥匙、能给到什么」，不搬运代码/数据）。

## 文件一览

| 文件 | 来源 | 用途 | 状态 |
|---|---|---|---|
| `weixin.sogou.com.md` | 搜狗微信搜索（wap 版） | 按**关键词**检索一批文章（标题/公众号/发布日/摘要/可解析正文链接）；唯一关键词通道、无时间过滤 | ✅ 本机实测 |
| `mp.weixin.qq.com.md` | 微信文章页 | 单篇文章**正文/元数据**（`#js_content`、永久链接 `__biz/mid/idx/sn`） | ✅ 直取 200 |
| `wechatspider.md` | 本机微信客户端抓包（`~/Research_Assistant/wechatspider`） | **按号全量**历史列表 + 正文 + **阅读/点赞数** | ⚠️ 未真实抓包 |
| `wewe-rss.md` | cooderl/wewe-rss（自托管 RSS，MIT） | 按号订阅 + `CRON` 定时增量 + `json/rss/atom` feed + 全文 | ⚠️ 未部署 |
| `wechat-download-api.md` | tmwgsicp/wechat-download-api（**AGPL⚠️**） | 后台凭证 HTTP API：`searchbiz`→`fakeid`→按号**真历史分页**（≤100/次）+ 号内关键词搜索 + 7 格式导出 + RSS + MCP 6 工具 | ⚠️ 未部署 |
| `wechat-digest-skill.md` | Jackychen-12/wechat-digest-skill（MIT） | 后台 Cookie+Token 采集 + `--resume` 跨天续采 + `contentStatus` **七态**失败判定 | ⚠️ 未运行 |
| `wechat-downloaders.md` | qiye45 / jackwener / gxcsoccer 三工具 | 已有链接 → HTML/MD/PDF/DOCX/图片落地；含 crawl4ai **抗风控技术要点** | ⚠️ 未安装 |
| `wechat-article-extractor.md` | freestylefly/wechat-article-extractor-skill | 单篇元数据/正文 + **删除/违规/过期错误码**判定表 | ⚠️ 未运行 |

## 选路

- 按**关键词/单位/年份词**批量搜公众号文章（如「双井街道 吹哨报到 2018年」）→ **搜狗微信**（唯一能关键词检索；但只是索引子集，拿不到阅读数）。
- 已知某公众号，要它**号内尽量全的文章**（含 2018 及更早）→ **wechatspider** / **B 组**（搜狗按账号页已下线 `gzhjs` 反爬；只有凭据路线能按号枚举）。
- 要**持续增量**（每天有新文章就进库）→ **wewe-rss** 或 **wechat-download-api**（前者只出 feed，后者还能导出多格式）。
- 要在**某号内部按关键词**筛文章 → **wechat-download-api**（`/api/public/articles/search?fakeid=&query=`；后台无全网搜索能力）。
- 需要**阅读数 / 点赞数** → **wechatspider**（客户端抓包；后台凭证与 RSS 都拿不到，`getappmsgext` 才有）。
- 只要**正文**（已有链接）→ **mp.weixin** 文件 / **C 组下载器**（签名链接有时效，需现取现抓）。
- 判定某篇老文章**是否已删/违规** → **wechat-article-extractor** 的错误码表（别把「正文为空」当成功入库）。
- 大规模语料（数百单位 × 多检索式）→ **搜狗微信**（分片并发；凭据路线受频控/凭证寿命限制，适合按号精采）。
- 选型要点：**搜狗 = 广度**（关键词索引，覆盖多号但非全量、无时间过滤）；**wechatspider = 深度**（单号最全 + 阅读数，但需客户端、`key` 约 2h 过期）；**B 组 = 有钥匙的深度**（无 macOS/客户端时的替代，钥匙会过期、频控绑账号）；**mp.weixin + C 组 = 正文抓取层**（被上面所有通道引用）。
- 链接互通：搜狗 → 签名链接 → 正文页 → 文章身份 `__biz`/`mid`/`idx`/`sn`（`sn` 可作去重主键；`__biz` 可喂给 wechatspider 的 `--biz`）。另注：首都之窗统一搜索的索引里能直接搜到带 `sn` 的 mp.weixin **永久链接**（见 `../gov/beijing.gov.cn.md`）。
- **B 组两条后台路线不要同时指望**：它们共用同一把「公众平台后台」钥匙，风控额度也绑账号（见 `wechat-digest-skill.md` 对 `ret=200013` 的结论）。
- 许可提醒：`wechat-download-api.md`（AGPL-3.0）、`wechat-downloaders.md` 中 qiye45 与 jackwener、`wechat-article-extractor.md` **无 LICENSE** —— 只作品路参考，**不直接引入**。
- 实测口径：A 组本机实测（`wechatspider.md` 单测 58 个全过、环境已装，但**真实抓包链路本次未复现**，文件内逐条标 `未验证`）；B/C 组来源卡**均未安装/未部署/未运行**，只读 README/SKILL.md/目录，「实测」只写真正跑过的命令（多为 `gh api` 元数据、raw 抓取、HTTP 探活），其余标「上游声明」。

## 相关

- 社交平台（舆情/事件补充线索）：`../social/README.md`
- 综合搜索引擎（`site:` 点查、替代召回）：`../engines/README.md`
- 数据源总索引与用法：仓库根 `SKILL.md`
