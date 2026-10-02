# forum-docs —— 公文·真题·报告·图纸集散地

论坛/社区**附件区**：帖子正文不值钱，值钱的是附在楼里的**公文原件、考试真题、环评报告全本、建筑图纸与规范图集**。这类文件官方往往不公开，只能靠论坛「楼中楼」流转。本卡只收**可匿名/注册浏览的公开板块**，不涉及破解权限。

- 去哪找：
  - 公考/体制内：`https://bbs.qzzn.com/`（QZZN）、`https://bbs.gwy.com/`（公考论坛）
  - 环评报告全本：`http://www.eiafans.com/`（环评爱好者）、`https://bbs.eiacloud.com/`（新环评论坛）
  - 建筑/结构/规划：`https://bbs.co188.com/`（土木在线）、`https://coyis.com/`（建筑一生）、`http://bbs.okok.org/`（中华钢结构）、`http://bbs.zhulong.com/`（筑龙）、`https://bbs.caup.net/`（国匠城·规划）
  - 法考/考研/学术：`https://bbs.xuefa.com/`（学法网）、`https://muchong.com/`（小木虫）
- 什么时候用：要「某年某省遴选/公考真题」「某项目环评报告全本 PDF」「某图集/规范/施工方案 CAD+PDF」「法考/考研真题讲义」而官网无公开件时；已知文件名/项目名，反查被谁上传过。
- 怎么搜：
  - **站内检索（登录态最稳）**——Discuz 通用模板：
    ```
    /search.php?mod=forum&srchtxt=<urlencode(关键词)>&searchsubmit=yes
    ```
    实测：`www.eiafans.com` 此 URL 返回「您是游客请注册！」→ **需注册**；`bbs.xuefa.com` 需登录。
  - **各站专属检索入口**：
    - 土木在线：`https://s.co188.com/search/?keyword=<关键词>`（✅ 200，游客可用）
    - 筑龙：`https://s.zhulong.com/search.php?keyword=<关键词>`
    - 小木虫：`https://muchong.com/bbs/search.php?q=<关键词>`
    - 建筑一生：`https://coyis.com/?s=<关键词>`（✅ 200，站内搜索）
  - **站内搜索未暴露**（前端 JS/需登录，raw HTML 无 form）：`bbs.gwy.com`、`bbs.caup.net`、`bbs.eiacloud.com`、`bbs.okok.org` → 改用下面的 `site:` 法。
  - **搜索引擎 `site:` 法（最省事，绕过登录墙看到帖子标题与附件名）**：
    - Google/Bing/本库 `web_search`：`site:bbs.co188.com 施工方案 filetype:pdf`、`site:www.eiafans.com 环评报告 全本`、`site:bbs.qzzn.com 遴选 真题`、`site:coyis.com 图集`。
    - 附件多为 `filetype:pdf|xls|dwg|zip|rar|doc`，用 `filetype:` 收窄；百度/搜狗 `site:` 对国内论坛收录更全。
  - **拿到帖子后**：Discuz 帖子形态 `/thread-<tid>-1-1.html` 或 `/forum.php?mod=viewthread&tid=<tid>`；附件直链随帖，但下载通常要登录/积分。
- 覆盖：公务员考录与体制内交流（QZZN、公考论坛）、环评/验收报告公示（环评爱好者系）、建筑结构市政规划资料（土木在线、建筑一生、中华钢结构、筑龙、国匠城）、法考与考研学术（学法网、小木虫）；年代自 2000 年代至今，粒度为「帖 + 附件」，更新靠用户自发上传。
- 门槛：**均需注册**才能搜索/下载附件（`eiafans` 明确游客不可搜索、附件「登录后可见」）；部分站需积分/等级；`bbs.qzzn.com` 本机不可达（疑地区/网络限制，未验证邀请码制）。
- 实测：2026-10-03，macOS（arm64），curl 8.x，桌面 Chrome UA，`-sSk -L -m 15~20`，每主机 1–2 次。12 站首页状态见 `## 细节`；`eiafans` 搜索页返回「您是游客请注册！」、帖子页含「登录后」；`co188` 搜索页 `s.co188.com/search/?keyword=…` ✅ 200；`bbs.qzzn.com` https 000/502（多组头重试仍 000），http 302 跳 https 后不可达。
- 上游：各论坛站点自身（见 `## 细节` 域名列）

## 细节

### 论坛清单（2026-10-03 实测）

| 站名 | 域名 | 引擎 | 首页（协议） | 站内搜索 | 附件/下载门槛 | 定位 |
|---|---|---|---|---|---|---|
| QZZN公务员考试论坛 | bbs.qzzn.com | Discuz | ❌ https 000/502；http 302→https 后不可达 | 需登录 | 注册（疑邀请码，未验证） | 公考真题、遴选、体制内交流 |
| 公考论坛 | bbs.gwy.com | 自建 | ✅ 200（https） | 未暴露（site:） | 注册 | 公考资讯交流 |
| 环评爱好者 | www.eiafans.com | Discuz | ✅ 200，**仅 http**，GBK | `search.php` 需注册 | **游客不可搜；附件登录后可见** | 环评报告/验收公示全本 |
| 环评论坛（新） | bbs.eiacloud.com | 自建 | ✅ 200（→ www.eiacloud.com/bbs/） | 未暴露（site:） | 注册 | 环评行业新址（老 eiabbs.net 2024-05-21 停运跳此） |
| 土木在线论坛 | bbs.co188.com | 自建 | ✅ 200（https，UTF-8） | `s.co188.com/search/?keyword=` ✅ | 游客可看帖，下载需登录/积分 | 土木/市政施工方案、图纸 |
| 建筑一生 | coyis.com | WordPress 型 | ✅ 200（https） | `coyis.com/?s=` ✅ | 注册/积分（资料站） | 规范、图集、施工监理资料 |
| 中华钢结构论坛 | bbs.okok.org | Discuz | ✅ 200，**仅 http** | 需登录 | 注册 | 结构/钢结构图纸与讨论 |
| 筑龙论坛 | bbs.zhulong.com | Discuz 系 | ✅ 200，**仅 http**（https 403） | `s.zhulong.com/search.php` | 注册 | 建筑人工程资料、图集 |
| 国匠城论坛 | bbs.caup.net | 自建 | ✅ 200（https） | 未暴露（site:） | 注册（部分资料入知识星球） | 城乡规划文本、图件 |
| 小木虫 | muchong.com | 自建/GBK | ✅ 200 | `muchong.com/bbs/search.php` | 注册 | 学术、考研真题、调剂 |
| 学法网 | bbs.xuefa.com | Discuz | ✅ 200，GBK | `search.php` 需登录 | 注册 | 法考真题、讲义、经验 |
| 考研论坛 | bbs.kaoyan.com | — | ⚠️ 302→ www.kaoyan.com | 主站自建 | 注册 | 论坛区已并入考研帮主站，弱化 |

> 检测要点：Discuz 站首页含 `Powered by Discuz!`（`okok`、`xuefa` 已证）；`eiafans`/`co188` 帖子页 URL 含 `mod=viewthread&tid=`、`thread-<tid>-1-1.html`。

### 命令备忘

```bash
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
# 环评爱好者：只走 http，GBK
curl -sSk -L -m 20 -A "$UA" 'http://www.eiafans.com/forum.php?mod=viewthread&tid=<tid>' | iconv -f gb18030 -t utf-8
# 土木在线：搜索页可直接取
curl -sSk -L -m 20 -A "$UA" 'https://s.co188.com/search/?keyword=%E6%96%BD%E5%B7%A5%E6%96%B9%E6%A1%88'
# 站内搜索判定（是否被登录墙拦）
curl -sSk -L -m 20 -A "$UA" 'http://www.eiafans.com/search.php?mod=forum&srchtxt=%E7%8E%AF%E8%AF%84%E6%8A%A5%E5%91%8A' | iconv -f gb18030 | grep -o '您是游客请注册'
```

## 坑

1. **协议分流**：`eiafans`、`bbs.okok.org`、`bbs.zhulong.com` 只服务 http（https 000/403），统一 `-sSk` 并改 http；`eiafans` 为 GBK、`xuefa`/`muchong` 为 GBK，抓前判编码，否则标题乱码。
2. **登录墙**：几乎所有论坛的「站内搜索」与「附件下载」都要求注册，`eiafans` 游客连搜索都被拒（「您是游客请注册」）。**不要试图绕过**——本卡的 `site:` 法只读公开帖子页。
3. **`bbs.qzzn.com` 本机不可达**：https 502/000、http 302 后仍不可达（多组浏览器头重试无效）。疑地区/网络限制或站点异常，**未验证**是否有邀请码门槛；用法：换国内网络或真实浏览器直连，或用 `site:bbs.qzzn.com` 间接取帖标题。
4. **附件形态**：帖子附件名常暴露（`site:` 可搜索到），但直链下载要登录/积分；`.dwg/.rar/.zip` 老格式解析麻烦，优先找同帖的 `pdf` 版。
5. **合规**：只读公开页面为限，不破解权限、不批量搬运；注册账号下载须遵守各站《注册协议》与积分规则。盗版/内部件注意版权（`eiafans` 站内也有「请勿上传侵权内容」公告）。
6. **死站/迁移**：老「环境影响评价论坛」`www.eiabbs.net` 已于 2024-05-21 停运维，跳转至 `bbs.eiacloud.com`；`bbs.kaoyan.com` 已并入主站，论坛入口弱化——按新域名找。
