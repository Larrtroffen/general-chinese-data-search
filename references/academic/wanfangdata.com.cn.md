# wanfangdata.com.cn —— 万方期刊/学位/会议论文

万方数据知识服务平台，国内三大中文文献库之一。**本机实测：站点对自动化/无痕访问统一弹滑块人机验证，curl 与 headless 浏览器均被挡在验证墙外，不可作为抓取通道。**

- 去哪找：`https://www.wanfangdata.com.cn/`；检索 `https://s.wanfangdata.com.cn/paper?q={关键词}`；旧接口 `POST /SearchService.SearchService.search.aspx`；验证墙 `https://www.wanfangdata.com.cn/verify`
- 什么时候用：要中文期刊/学位/会议论文时的万方一路；需核对机构订阅内的中文库原件
- 怎么搜：无匿名通道——检索页 302 → `/verify` 滑块；有权限时走可见浏览器人工过滑块（参照 `navi.cnki.net.md` 的 `headed:true, persist:true` 手法），或改用机构 IP 直连
- 覆盖：中文期刊/学位/会议论文；前端已迁移 gRPC-Web
- 门槛：访客一律滑块验证墙；机构 IP（校园网/图书馆代理）通常免滑块并带订阅权限
- 实测：2026-10-02，macOS + curl 8.x + 本机 headless Chromium（`browser` 工具）：
  - `GET https://www.wanfangdata.com.cn/` → `HTTP 200`
  - `GET https://s.wanfangdata.com.cn/paper?q=基层治理`（curl，desktop UA）→ `HTTP 200 size=171424`，`<title>万方数据知识服务平台</title>`，HTML 内无结果条目
  - `POST /SearchService.SearchService.search.aspx`（form-urlencoded，`searchWord=基层治理`）→ `HTTP 415`
  - headless Chromium 打开检索页 → 最终 URL `https://www.wanfangdata.com.cn/verify?ip=anymous&redirect=https%3A%2F%2Fs.wanfangdata.com.cn%2Fpaper%3Fq%3D…`，正文含"请按住滑块，拖动到最右边"
  - `GET /verify` → `HTTP 200 type=text/html`
  - `GET https://www.nationaldata.cn/` → `HTTP 000`（连接失败，另见索引说明）
- 上游：`https://www.wanfangdata.com.cn/`

## 细节

### 可用性矩阵

| 入口 | 状态 | 现象 |
|---|---|---|
| `https://www.wanfangdata.com.cn/` | ✅ | HTTP 200（首页壳） |
| `https://s.wanfangdata.com.cn/paper?q={关键词}` | ⚠️ | curl 返回 200 但只是 SPA 空壳（HTML 内无结果）；**浏览器访问立即 302** |
| 浏览器/headless 打开检索页 | ❌ | 302 → `https://www.wanfangdata.com.cn/verify?ip=anymous&redirect=…`，页面提示"为保障数据与服务安全，我们需要确认您是真人操作…请按住滑块，拖动到最右边"（滑块验证码） |
| 旧接口 `POST /SearchService.SearchService.search.aspx` | ❌ | `HTTP 415 Unsupported Media Type` |
| `GET /verify` | ⚠️ | 200 text/html（验证墙页面） |

### 结论与路径

- **curl / 无头浏览器均不可用**：站点有 `anti-climb`（反爬）机制，访客一律跳 `/verify` 滑块；验证通过前拿不到结果。
- 前端已迁移到 **gRPC-Web**：SPA 从 `https://cdn.s.wanfangdata.com.cn/js/api.*.js` 加载 `SearchServicePromiseClient`（protobuf，方法 `Search`/`AdvancedSearch`），请求携带 `anti-climb` 元数据 token，非 curl 可直接构造。
- 若要采集万方，可行路径（按成本排序）：
  1. **可见浏览器人工过滑块**（参照 `references/academic/navi.cnki.net.md` 的 `headed:true, persist:true` 手法），过码后用浏览器读取结果，或复用其 gRPC-Web 会话；
  2. 改用机构 IP（校园网/图书馆代理），机构内通常免滑块并带订阅权限；
  3. 改用万方"智研"APP 接口（未验证）。
- 替代库见 `references/academic/cqvip.com.md`（维普，curl 可直取首页结果）与 `references/academic/ncpssd.org.md`（NCPSSD，JSON API 直连）。

## 坑

- `s.wanfangdata.com.cn` 的检索页**curl 也给 200**，容易误判为"可抓"；实际结果全在客户端 gRPC-Web 响应里，HTML 里一条都没有。
- 万方对同一 IP 的滑块判定很敏感，连续探针会加剧封堵；本库礼貌值 ≤3 req/host。
