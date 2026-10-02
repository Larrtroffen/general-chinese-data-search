# chinacdc.cn —— 中国疾控中心疫情月报与健康数据

- 去哪找：健康数据栏目 `https://www.chinacdc.cn/jksj/`（下分 4 个子栏 `jksj01/`–`jksj04/`）；英文周报期刊 `https://weekly.chinacdc.cn/`。
- 什么时候用：要**全国法定传染病疫情月度概况**（分病种发病/死亡数）；要**中国需关注的突发公共卫生事件月度风险评估**；要**全球传染病事件月度风险评估**；要**成人/中学生烟草调查**结果；要英文发表的疾控周报。
- 怎么搜：无 API，栏目页直接列条目，抓 HTML 即可（条目为相对路径）——
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  curl -s -A "$UA" 'https://www.chinacdc.cn/jksj/jksj01/' | grep -o 'href="\./[^"]*"[^>]*>[^<]*'
  ```
  结果形态：`jksj01` 为 HTML 正文页；`jksj02`/`jksj03` 为 **PDF**（`…/202609/P020260918450416463901.pdf`）；`jksj04` 为 HTML。
- 覆盖：`jksj01` 全国传染病疫情概况（月报，实测列表 2025-09 → 2026-08）；`jksj02` 中国突发事件风险评估（月报 PDF，2025-09 → 2026-08）；`jksj03` 全球传染病事件风险评估（月报 PDF，同区间）；`jksj04` 烟草调查（2018/2019/2020/2024 年结果）；`weekly.chinacdc.cn` 为英文开放获取期刊。
- 门槛：免费，无需登录；无 API。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA）：`https://www.chinacdc.cn/` 200（75,121 B）；`/jksj/` 200（1,643 B，JS `location.replace("./jksj01/")`）；`/jksj/jksj01/` 200（31,327 B，12 条月度概况）；`/jksj/jksj02/`、`jksj03/`、`jksj04/` 均 200；`https://weekly.chinacdc.cn/` 200（137,064 B，`<title>China CDC Weekly`）。
- 上游：中国疾病预防控制中心 `https://www.chinacdc.cn/`。

## 细节

### 子栏对照（2026-10-03 实测）

| 路径 | 内容 | 形态 | 更新 |
|---|---|---|---|
| `…/jksj/jksj01/` | 全国法定传染病疫情概况（2025-12 起改名「全国传染病疫情概况」） | HTML 正文页 | 月度 |
| `…/jksj/jksj02/` | 中国需关注的突发公共卫生事件风险评估 | PDF | 月度 |
| `…/jksj/jksj03/` | 全球传染病事件风险评估 | PDF | 月度 |
| `…/jksj/jksj04/` | 全国成人烟草调查、中学生烟草调查结果 | HTML | 不定期 |

- 条目 URL 规律：`…/<子栏>/<YYYYMM>/t<YYYYMMDD>_<id>.html`（HTML）或 `…/<YYYYMM>/P<19位>.pdf`（PDF）。
- `weekly.chinacdc.cn`（China CDC Weekly）为英文摘要/全文期刊，可当英文引用来源；站内检索未本机验证。

## 坑

1. `/jksj/` 本身是 JS 跳转壳，正文在 4 个子栏；直接抓 `/jksj/` 拿不到条目。
2. 条目链接是**相对路径**（`./202609/…`），拼接时注意父目录。
3. 疫情概况只有正文数字，无结构化表/CSV；要数值需自行解析 HTML，PDF 需 OCR/抽取。
4. 栏目名在 2025-12 改过一次（去掉「法定」），检索历史时两种名称都要试。
