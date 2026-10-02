# wenshu.court.gov.cn —— 中国裁判文书网

最高法主办的裁判文书公开平台。**2021 年起检索须登录**：匿名访问检索链接会被重定向到统一登录页（`/tongyiLogin/authorize`）。本机匿名 curl **拿不到结果**，只能取到 SPA 壳与一个"接口未定义"的 JSON 报错。需要文书全文时请改走替代通道（见下）。

- 去哪找：
  - 站点：`https://wenshu.court.gov.cn/`
  - 首页壳：`https://wenshu.court.gov.cn/website/wenshu/181029CR4M5A62CH/index.html`
  - 数据入口（页面 JS 反查）：`/website/parse/rest.q4w`
  - 替代通道见「细节」
- 什么时候用：要**裁判文书全文**（本文书网本身匿名不可用，仅记入口与替代通道）；**法条原文**改走 `flk.npc.gov.cn.md`。
- 怎么搜：匿名不可用——检索须登录态。数据入口在 `/website/wenshu/181029CR4M5A62CH/index.js?v=1.4`：`"dataParsePath":"/website/parse/rest.q4w"`；`cfg` 取值：`com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO`（检索）、`…LoadDicDsoDTO`（字典）、`…SuggestDsoDTO`（联想）、`com.lawyee.wbsttools.web.parse.dto.AppUserDTO`（用户）。**未验证**：是否需要 `vjkl5` Cookie + 前端 RSA 加密参数、验证码/滑块策略；**本机未跑通**匿名检索。
- 覆盖：全国裁判文书（匿名不可检索）。
- 门槛：**需登录**（手机号/支付宝/钉钉）；匿名检索跳登录页。
- 实测：2026-10-02，macOS，curl 8.x + headless Chromium。① `GET https://wenshu.court.gov.cn/` → **200**，22 309 B HTML（首页；含"登录/注册"）。② `GET /website/wenshu/181029CR4M5A62CH/index.html` → 200（首页同源壳）。③ `GET …/181217BMTKHNT2W0/index.html?pageId=…&s21=行政` → 200（列表页壳），但结果需登录态。④ 匿名点"检索"（浏览器实测）→ **跳转登录页** `/tongyiLogin/authorize`（手机号/支付宝/钉钉）。⑤ `GET /tongyiLogin/authorize` → **405**（POST-only）。⑥ `POST /website/parse/rest.q4w` → **200** `{"code":9,"description":"请求接口未定义或格式错误,cfg=…","success":false}`。所有状态码/跳转/报错均为当日实际请求所得；"登录墙"结论由浏览器实际跳转 + 登录表单截图双重确认。
- 上游：`https://wenshu.court.gov.cn/`（最高人民法院）

## 细节

### 关键证据

```bash
UA='Mozilla/5.0 …Chrome/120…'
curl -s -o /dev/null -w '%{http_code}\n' -m 20 -A "$UA" 'https://wenshu.court.gov.cn/'          # 200
curl -s -m 20 -A "$UA" -H 'Referer: https://wenshu.court.gov.cn/website/wenshu/181029CR4M5A62CH/index.html' \
  -H 'X-Requested-With: XMLHttpRequest' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
  --data 'pageId=1&sortFields=s50:asc&ciphertext=1&cfg=com.lawyee.judgement.JudgementList&searchType=1&sortType=1' \
  'https://wenshu.court.gov.cn/website/parse/rest.q4w'
# → 200 {"code":9,"description":"请求接口未定义或格式错误,cfg=com.lawyee.judgement.JudgementList",…}
```

浏览器（headless）实测：在首页输入"行政"回车 → 页面跳到 `https://wenshu.court.gov.cn/website/wenshu/181010CARHS5BS3C/index.html?…/181217BMTKHNT2W0/index.html?pageId=4a86…&s21=行政` 并渲染出**登录表单**（截图见本会话记录）。

### 可用性矩阵（本机实测）

| 端点 | 状态 | 现象 |
|---|---|---|
| `https://wenshu.court.gov.cn/` | ✅ | 200，22 309 B HTML（首页；含"登录/注册"） |
| `https://wenshu.court.gov.cn/website/wenshu/181029CR4M5A62CH/index.html` | ✅ | 200（首页同源壳） |
| `…/website/wenshu/181217BMTKHNT2W0/index.html?pageId=…&s21=行政` | ⚠️ | 200（列表页壳），但结果需登录态 |
| 匿名点"检索" | ❌ | 浏览器实测**跳转登录页** `/tongyiLogin/authorize`（手机号/支付宝/钉钉） |
| `GET /tongyiLogin/authorize` | ❌ | 405（POST-only） |
| `POST /website/parse/rest.q4w` | ⚠️ | 200 `{"code":9,"description":"请求接口未定义或格式错误,cfg=…","success":false}` |

### 替代通道（仅登记可达性；内容级 API 未验证）

| 站点 | 状态 | 说明 |
|---|---|---|
| `https://rmfyalk.court.gov.cn/`（人民法院案例库） | ✅ 200 | 官方**指导性/参考案例**库，首页显示"共收录案例 5586 篇"，**匿名有检索入口**；实测点检索未捕获到 XHR（提交依赖前端 JS）→ 接口**未验证** |
| `https://www.faxin.cn/`（法信，人民法院出版社） | ⚠️ 200 | 首页 123 KB 可开，正文需登录/订阅 |
| `https://www.itslaw.com/`（无讼） | ⚠️ 200 | 仅 7.5 KB 壳，疑似失效 |
| `https://openlaw.cn/` | ❌ | 302 跳转（已不可用） |
| `https://www.lawxp.com/`（法律屋/把手案例） | ❌ | 302 跳转（已不可用） |

商业库路线见 `pkulaw.com.md`（北大法宝，需 Token）。

### 建议

1. 需要**法条原文** → 用 `flk.npc.gov.cn.md`（官方、免登录）。
2. 需要**裁判文书/案例** → 优先"人民法院案例库"网页检索（人工浏览），或北大法宝（需 Token）。
3. `web_search site:wenshu.court.gov.cn {关键词}` 通常只命中结果页标题、无正文，且链接会再要登录，效率低。
