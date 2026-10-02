# construction-realestate —— 住建部建设统计年鉴与公报

- 去哪找：住建部「信息公开 · 统计数据」总栏目 `https://www.mohurd.gov.cn/gongkai/fdzdgknr/sjfb/index.html`；**统计信息（年鉴/公报下载）** `…/sjfb/tjxx/index.html`；统计调查制度 `…/sjfb/tjbbzd/index.html`；统计法规政策 `…/sjfb/tjfgzc/index.html`；统计信息系统登录 `…/sjfb/tjxxxtdl/index.html`；附件 CDN 域 `cms_files/filemanager/…`。
- 什么时候用：要**城市建设/城乡建设统计年鉴**（市政公用设施、供水燃气、园林绿化、固定资产投资分城市）、**中国城市建设状况公报**，或 **工程勘察设计 / 建设工程监理 / 工程造价咨询**统计公报；写城市基础设施、城镇化、建筑业与房地产市场供给端时需要建设主管部门口径（需求端投资/销售走国家统计局，见下）。
- 怎么搜：栏目浏览 + 附件下载；统计信息页把「年鉴 + 各类公报」集中成列表，附件多为 xls/zip/pdf/doc。附件直链两类：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # ① 新版走 api-gateway（相对本站，须带完整加密 fileUrl + fileName；curl -L 跟 302 到真实 xls）
  curl -sS -L -A "$UA" 'https://www.mohurd.gov.cn/api-gateway/jpaas-web-server/front/document/download?fileUrl=<加密串>&fileName=2024年城市建设统计年鉴.xls'
  # ② 旧版直接 cms_files
  curl -sS -L -A "$UA" 'https://www.mohurd.gov.cn/cms_files/filemanager/mohurdold/file/2023/20231011/4de09801-07f4-4273-97cb-1e1fc78704fd.xls'
  ```
  结果形态：栏目 HTML 列表；年鉴为 **xls（旧版）/ zip**，公报为 **pdf/doc/docx**；`api-gateway` 链 302 跳 `cms_files/filemanager/<id>/attach/<yyyymm>/<hash>.<ext>`。
- 覆盖：城市建设统计年鉴 ——2024（每期一个 xls）；城乡建设统计年鉴 ——2024（每期一个 zip）；中国城市建设状况公报 2024；工程勘察设计 / 建设工程监理 / 工程造价咨询统计公报 2024–2025；建筑业特级一级企业月度快报（2016，历史残留）。
- 门槛：**免费、无登录**；附件经 `api-gateway` 加密跳转（须从页面取**完整** `fileUrl`，别自造）。
- 实测：2026-10-03，macOS arm64，curl 8.x，桌面 UA，20 s 超时，≥1.5 s 间隔：
  - `mohurd.gov.cn/gongkai/fdzdgknr/sjfb/index.html` → 200；`…/sjfb/tjxx/index.html` → 200（列出 2023/2024 城市建设与城乡建设统计年鉴、2024 中国城市建设状况公报、2025 勘察设计/监理/造价咨询公报）✅
  - 2024 城市建设统计年鉴网关链 → **302** → `…/cms_files/filemanager/1150240553/attach/20259/f7977fce5e6e4195aae89f94c9781623.xls?fileName=x` → **200** `application/vnd.ms-excel` 2.16 MB ✅
  - 2022 城市建设统计年鉴直链 `cms_files/filemanager/mohurdold/file/2023/20231011/4de09801-07f4-4273-97cb-1e1fc78704fd.xls` → 200 2.44 MB ✅
  - 城乡建设统计信息管理系统 `http://cxtj.mohurd.gov.cn/` → 200（小页面，疑为登录/入口页）⚠️
- 上游：住房和城乡建设部 `mohurd.gov.cn`；年鉴/公报编辑部见各附件 fileName。

## 细节

### 统计信息页附件清单（2026-10-03 页面实测）

| 名称 | 形态 | 取法 |
|---|---|---|
| 2024 年城市建设统计年鉴 | xls | `api-gateway …download?fileUrl=…&fileName=2024年城市建设统计年鉴.xls` |
| 2024 年城乡建设统计年鉴 | zip | 同上（`fileName=…城乡建设统计年鉴.zip`） |
| 2023 年城市建设统计年鉴 / 城乡建设统计年鉴 | xls / zip | 同上 |
| 2022 年城市建设统计年鉴 | xls | 直接 `cms_files/filemanager/mohurdold/…xls` |
| 2024 年中国城市建设状况公报 | pdf | `api-gateway …download?fileUrl=…` |
| 2025 年全国工程勘察设计 / 建设工程监理 / 工程造价咨询统计公报 | doc / docx | 同上 |
| 2024 年工程造价咨询统计公报 | docx | 同上 |

- 相关子系统（页面给出、未逐个实测）：城乡建设统计信息管理系统 `http://cxtj.mohurd.gov.cn/`、综合统计平台 `http://59.255.8.249:8081/home/index`、统计信息系统登录栏目 `…/sjfb/tjxxxtdl/index.html`。

### 与房地产相关的口径分界

- **供给/建设侧**（本卡）：城市建设统计年鉴（市政公用）、城乡建设统计年鉴、城市建设状况公报。
- **投资/销售侧**（房地产投资、商品房销售面积与额）：住建部不发，走**国家统计局**（`../stats/data.stats.gov.cn.md`）+ 地方统计局月报。
- **企业/市场侧**（房企销售榜、房地产市场分析）：走中国房地产业协会 `../industry/fangchan.com.md`。
- 部委总表与附件加密规律参见 `../stats/ministry-stats.md`（住建部条目）。

## 坑

1. **`api-gateway` 的 `fileUrl` 是加密串且相对本站**：整条链接（含 `fileName`）从页面复制，`curl -L` 跟 302 才落到真实 `cms_files` 文件；手工改 `fileName` 或截断 `fileUrl` 会 302 后空/错文件。
2. 年鉴是**旧版 .xls**（非 xlsx），解析前注意编码与合并单元格；城乡建设年鉴是 **zip 包**，内含多表。
3. 新老链接并存：2022 及更早年鉴走 `cms_files/filemanager/mohurdold/…`；2023+ 统一走 `api-gateway`，别用旧规律猜新年链。
4. 公报与年鉴混排在同一「统计信息」列表里，靠标题区分（「…公报」= 文字/pdf 报表口径，「…统计年鉴」= 整表 xls）。
5. 同页含大量历年通知/制度文件（`.doc`），列表较长；按「年鉴 / 公报 / 调查制度」标题过滤。
