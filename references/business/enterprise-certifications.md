# enterprise-certifications —— 高企与专精特新名单

- 去哪找：**高新技术企业认定工作网** `http://www.innocom.gov.cn/`（公示公告栏目 `http://www.innocom.gov.cn/gqrdw/c101334/list_gsgg_l2.shtml`）；**优质中小企业梯度培育平台（专精特新）** `https://zjtx.miit.gov.cn/`（通知公告 `/zxqySy/tzggMore`）；工信部发布 `https://www.miit.gov.cn/`。
- 什么时候用：要**高新技术企业（高企）备案公示/认定名单**、**专精特新"小巨人"/省级专精特新公示名单**；做企业创新、产业政策、地方补贴与"政策工具"研究的样本框。
- 怎么搜：高企名单以**逐省分批公示/公告**发布（附件多为 PDF/Excel）；专精特新名单分**工信部公示 + 各省工信厅公示**两级，认定申报走培育平台（需企业账号登录）。
- 覆盖：高企：按认定机构（省/计划单列市）× 批次 × 年份；专精特新：国家级"小巨人"（第 N 批）+ 省级专精特新 + 复核通过名单。
- 门槛：名单**免费公开**；**申报/信息更新需登录**（培育平台）；部分省级名单散落在各省工信厅站点（`gxt.<省>.gov.cn` 等）。
- 实测：2026-10-03，macOS arm64 curl 8.x（桌面 UA）——`GET https://www.innocom.gov.cn/` 与 `http://www.innocom.gov.cn/` **均连接超时**（30s 无响应，`curl (28)`），**本机不可达**；`GET https://zjtx.miit.gov.cn/` → `200/70 KB`（`<title>优质中小企业梯度培育平台`），页面含"政务服务平台"链接 `ythzxfw.miit.gov.cn` 与通知公告"查看更多"`/zxqySy/tzggMore`；`GET https://www.miit.gov.cn/` → `200/65 KB`（工信部，含 `__jsluid_s` WAF Cookie）。
- 上游：火炬高技术产业开发中心（高企认定工作网）；工信部中小企业局 / 优质中小企业梯度培育平台。

## 细节

### 高新技术企业认定工作网（`innocom.gov.cn`）

> 本机网络不可达（超时）；以下 URL 为上游（web_search 抓取）所见，**未本机实测**。

| 栏目 | URL |
|---|---|
| 公示公告总栏 | `/gqrdw/c101334/list_gsgg_l2.shtml` |
| 认定备案公告 | `/gqrdw/c101481/list_gsgg_l2.shtml` |
| 企业更名公告 | `/gqrdw/c101482/list_gsgg_l2.shtml` |
| 取消高企资格公告 | `/gqrdw/c101483/list_gsgg_l2.shtml` |
| 异地搬迁公告 | `/gqrdw/c101484/list_gsgg_l2.shtml` |
| 分省公示（例：北京 2025 第一批） | `/gqrdw/c101407/202510/{uuid}.shtml` |

- 公示正文含"认定机构 + 年份 + 批次 + N 家企业（名单详见附件）"；**企业名单在附件**（PDF/Excel），正文不列全。

### 专精特新（优质中小企业梯度培育平台 / 工信部）

| 内容 | URL |
|---|---|
| 梯度培育平台首页 | `https://zjtx.miit.gov.cn/` ✅ 200 |
| 通知公告列表 | `https://zjtx.miit.gov.cn/zxqySy/tzggMore` |
| 政务服务平台 | `https://ythzxfw.miit.gov.cn/index` |
| 工信部认定/复核通知（例：2026 年度） | `https://www.miit.gov.cn/zwgk/zcwj/wjfb/tz/art/2026/art_76ee858469814146a1ce17becc6bb325.html` |

- 国家级"小巨人"名单由**工信部公示**，省级专精特新由**各省工信厅公示**（例：山东 `gxt.shandong.gov.cn`）；省级附件常见 `module/download/downfile.jsp?…` 下载链接。

## 坑

1. **`innocom.gov.cn` 本机不可达**（连接超时，非 404），学术网络/海外出口常被挡；需换网络或用浏览器代理确认。
2. 高企名单**分散在分省公示页**，且名单在附件里——批量整理须逐页下附件，无统一检索 API。
3. 专精特新申报入口**需企业账号**；公开名单只在"公示"阶段出现，之后可能下架，**要留档**（网页存档见 `../tools/web.archive.org.md`）。
4. 工信部站点亦有 `__jsluid_s` WAF Cookie；`www.miit.gov.cn` 与 `zjtx.miit.gov.cn` 为不同主机。
5. 高企"公示"≠"最终认定公告"：研究口径应以**认定备案公告**为准，勿把公示当终稿。
