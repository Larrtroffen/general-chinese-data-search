# bse.cn —— 北交所信息披露与市场数据

- 去哪找：门户 `https://www.bse.cn/`；**上市公司公告** `https://www.bse.cn/disclosure/announcement.html`；**市场数据/统计**（栏目入口见「细节」）。
- 什么时候用：要**北京证券交易所**的上市公司公告、发行上市、市场统计；北交所与新三板的研究样本。
- 怎么搜：官网本机匿名**过不了反爬**（JS 挑战 + API 重定向环）。绕行方案：北交所上市公司公告可经 `../business/cninfo.com.cn.md` 的公告接口取（`szse_stock.json` 已含北交所 `430/83x/87x/920` 代码与 orgId）。
- 覆盖：北交所上市公司公告与市场数据（栏目范围，未逐项枚举）。
- 门槛：官网**需浏览器**（执行 JS 种 Cookie 后才放行）；cninfo 绕行路径**免登录**。
- 实测：2026-10-03，macOS arm64 curl 8.x（桌面 UA）——`GET https://www.bse.cn/` → `200` 但响应仅 **345 B**，正文是 `<script>…window.open("/","_self");document.cookie="C3VK=b594c1; path=/; max-age=300;"</script>`（反爬首跳挑战）；补 `Cookie: C3VK=b594c1` 后仍返回同一 345 B 挑战页；`https://www.bse.cn/disclosureInfoController/infoResult.do?...` 与 `https://www.bse.cn/disclosure/announcement.html` → `302` 且 **超过 50 次重定向**被 curl 中止（`Maximum (50) redirects followed`）。
- 上游：`https://www.bse.cn/`（北京证券交易所）。

## 细节

### 现象拆解

| 请求 | 观察 |
|---|---|
| `GET https://www.bse.cn/` | `200` / 345 B，JS 设 Cookie `C3VK=b594c1` 后 `location.reload` |
| 同上 + `Cookie: C3VK=b594c1` | 仍是 345 B 挑战页 |
| `GET /disclosure/announcement.html` | `302`，无限重定向 |
| `GET /disclosureInfoController/infoResult.do` | `302`，无限重定向 |

- 该 WAF（`C3VK` 系"创宇盾"）需要执行首跳 JS 并带正确随机值才放行，**curl 静态 Cookie 不够**，须真实浏览器（Playwright/Chromium）自动带 Cookie 后再取接口。

### 绕行

- 北交所公告 → `../business/cninfo.com.cn.md`：`column=szse` 的 `hisAnnouncement/query` 覆盖北交所代码（`szse_stock.json` 里 `430/830/831/…/920` 共 600+ 条）。
- 名单/公司信息 → 国家级入口见 `../gov/gsxt.md`（工商）与 `../business/enterprise-certifications.md`（认定名单）。

## 坑

1. `-L` 会把 302 环跟到上限（50 次）才报错；遇到 `Maximum (50) redirects` 即该站的反爬签名，不是网络问题。
2. 不要用 `C3VK=b594c1` 硬编码：该值按会话/时间变化，实测固定值无效。
3. 北交所数据如需**官方口径精确页**，须在浏览器里人工打开；批量研究样本优先走 cninfo。
