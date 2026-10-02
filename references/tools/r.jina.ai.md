# r.jina.ai —— 网页转 Markdown 代理（本机不可达）

Jina Reader：在服务端渲染目标网页后返回 Markdown/纯文本，常用于「目标站被 JS 挡住 / 被反爬拦住时，用第三方渲染代理取正文」的场景。**本机（2026-10-02）对该域名完全不可达**（与 `web.archive.org` 同类的网络封锁），不要把它放进关键路径。

- 去哪找：`https://r.jina.ai/{目标完整 URL}`（目标 URL 直接拼在主机根路径之后）
- 什么时候用：换到能联网的环境时，作为被 JS/反爬拦住页面的第三方渲染通道；本机不要用，也不要重试硬等
- 怎么用：`curl -s -m 40 'https://r.jina.ai/https://example.com/page.html'`；可选头 `Authorization: Bearer <JINA_API_KEY>`、`X-Return-Format: markdown|text|html`、`X-Timeout: 30`；无 key 亦可用（较低速率限制，具体限额未测）
- 覆盖：通用网页 → Markdown/纯文本；本机 `*.jina.ai` DNS 可解析但 TCP 443 全不通（`api`/`eu.r`/`s.jina.ai` 三个子域均失败）
- 门槛：需能连通 `*.jina.ai`（本机不通）；有 key 可提高额度
- 实测：2026-10-02，macOS（arm64），curl 8.x —— `HTTP=000`（45 s 超时）、`nc` TCP 443 FAIL、替代代理 allorigins 500 / codetabs 522；完整记录见下
- 上游：站点自身入口（无 repo/Skill 出处）

## 细节

### 现状（本机实测 2026-10-02，macOS + curl）

| 检查 | 命令 | 结果 |
|---|---|---|
| DNS | `nslookup r.jina.ai` | ✅ 解析出 `103.214.168.106`（另有 IPv6 `2a03:2880:f10c:283:face:b00c:0:25de`，属 Facebook/AS32934 段） |
| TCP | `nc -z -G 6 -4 r.jina.ai 443` | ❌ 失败（TCP-FAIL） |
| HTTPS 请求 | `curl -s -D - -m 45 'https://r.jina.ai/http://www.bjchy.gov.cn/dynamic/zwhd/8a24fe836274afa5016275d0fada0067.html'` | ❌ `HTTP=000`，45 s 超时、`SIZE=0`、无任何响应头；`curl -sv` 显示卡在 `Trying 103.214.168.106:443` → `Connection timed out` |
| 备选域名 | `nc -z -G 5 {api,eu.r,s}.jina.ai 443` | ❌ 三个全失败（`api.jina.ai` → `31.13.71.19`） |

→ `*.jina.ai`：**DNS 可解析但 TCP 443 不通**，与 `web.archive.org` 的封锁特征一致。**不要再重试硬等**（每次白耗 45 s）。

### 使用方式（能联网的环境；本机未验证）

```bash
# 基本用法：目标完整 URL 直接拼在主机根路径之后
curl -s -m 40 'https://r.jina.ai/https://example.com/page.html'

# 公开文档中的可选头（本机无法验证，仅记录）：
#   Authorization: Bearer <JINA_API_KEY>     # 提高额度
#   X-Return-Format: markdown|text|html      # 返回格式
#   X-Timeout: 30                            # 服务端抓取超时
# 无 key 亦可用（较低速率限制）；具体限额本次未测。
```

### 替代方案（本机实测）

| 方案 | 命令/地址 | 结果 |
|---|---|---|
| 直连目标站（优先） | `curl -s -m 20 -A "$UA" '<页面>'` + `iconv -f gb18030 -t utf-8` | ✅ 多数政府/媒体/数字报页面是静态 HTML，直连即可（见 `../gov/README.md`、`../media/`） |
| 微信文章正文 | 见 `../wechat/mp.weixin.qq.com.md` | ✅ 签名链接可直读 |
| 站内检索接口直调 | 见 `../party/dangjian.cn.md`、`../party/cpc.people.com.cn.md` | ✅ 检索页是壳、接口可用（比代理更稳） |
| allorigins | `https://api.allorigins.win/raw?url={encoded}` | ❌ HTTP 500（本机） |
| codetabs | `https://api.codetabs.com/v1/proxy?quest={encoded}` | ❌ HTTP 522（本机） |
| 其他代理 | `corsproxy.io`、`thingproxy`、自建 Cloudflare Worker | 未验证 |

- 结论：本机（当前网络）**第三方渲染/代理通道普遍不通**；正文抓取以「直连 + 编码处理」为主，代理只作最后兜底。

### 实测记录（2026-10-02）

macOS（arm64），curl 8.x：`curl -s -D /tmp/jina.h -m 45 'https://r.jina.ai/http://www.bjchy.gov.cn/dynamic/zwhd/8a24fe836274afa5016275d0fada0067.html'` → `HTTP=000`（45.0 s 超时，无响应头、无 body）；`curl -sv -m 12 'https://r.jina.ai/'` → `Trying 103.214.168.106:443` → `Connection timed out`；`nc -z -G 6 -4 r.jina.ai 443` FAIL；`api.jina.ai`/`eu.r.jina.ai`/`s.jina.ai` TCP 443 均 FAIL；`nslookup` 正常解析。替代代理：`api.allorigins.win/raw?url={bjchy 页}` → 500；`api.codetabs.com/v1/proxy?quest={bjchy 页}` → 522。

## 坑

1. `HTTP=000` + 45 s 是**网络层不通**，不是目标站的问题；先用 `nc -z -G 6 <host> 443` 判 TCP，再决定要不要发请求。
2. 代理进流水线前必须探活（3 秒 TCP 探测），否则一批任务会被超时拖死。
3. 代理返回的是「代理视角」的页面（可能是地域化首页，或代理 IP 被目标站封）→ 关键结论仍需直连复核。
4. 部分代理要求目标 URL **完整编码**（连 `:`、`/` 一起）或只接受 `?url=` 参数，形态各异；接入前逐个确认。
