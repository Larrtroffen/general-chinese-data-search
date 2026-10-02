# commute-city —— 城市通勤与交通运行

四家合为一卡，均为**报告/指数型**来源：**中规院 + 百度地图慧眼《中国主要城市通勤监测报告》**（通勤时耗/距离/跨城通勤，PDF 可直下）、
**百度地图《中国城市交通报告》**（拥堵/交通健康指数，季度·年度 PDF 可直下）、
**高德《中国主要城市交通分析报告》**（拥堵延时指数，在线报告页 + JS 下载）、
**交通运输部 城市客运量**（月度分省 xlsx）。

- 去哪找：
  - **百度地图慧眼 报告中心** `https://huiyan.baidu.com/reports`；报告清单 API `https://huiyan.baidu.com/hycms/home/reports.jsonp?issue=true`；单篇落地页 `https://huiyan.baidu.com/reports/landing?id={id}`
  - **通勤监测报告 PDF** `https://huiyan.baidu.com/boswebsite/cms/report/{YYYY}tongqin/{YYYY年度中国主要城市通勤监测报告}.pdf`；发布新闻（中国城市规划网）`https://www.planning.org.cn/news/view?id=16083`
  - **百度地图 交通报告入口** `https://jiaotong.baidu.com/reports/`；`https://jiaotong.baidu.com/reports/landing?id={id}`；**城市交通报告 PDF** `https://huiyan.baidu.com/cms/report/{期次}jiaotong/{文件名}.pdf`
  - **高德交通报告** `https://report.amap.com/`（title「高德交通--中国主要城市交通分析报告」）；实时大数据 `/home.html`；迁徙排名 `/migrate/index.do`
  - **交通运输部** 数据栏目 `https://www.mot.gov.cn/shuju/`；月度《全国城市客运量》`https://xxgk.mot.gov.cn/jigou/zhghs/{YYYYMM}/t{YYYYMMDD}_{id}.html`（正文附 **xlsx**）
- 什么时候用：要**通勤时耗/通勤距离/5 公里内通勤比例/跨城通勤人口/轨道覆盖通勤人口**；要城市**拥堵延时指数、高峰车速、交通健康指数**及排名；要**月度城市客运量、轨道交通客运量**（分省 xlsx）；写城市交通、职住分离、都市圈通勤、轨道 TOD 类报告时。
- 怎么搜：三种取法——**① 慧眼清单 API 定位报告 id**（JSONP）→ **② 按模板拼 PDF 直链**（`curl` 直接下）；**③ 交通运输部**栏目 HTML + xlsx 附件。
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # ① 全部报告清单（64 期，含 id/title/link/pdf_link/role）；加 &role=traffic 只看交通类
  curl -sS -A "$UA" 'https://huiyan.baidu.com/hycms/home/reports.jsonp?issue=true'
  # ② 通勤监测报告 PDF（年度，已验证 2024/2023 可下）
  curl -sS -A "$UA" -o 2024通勤监测报告.pdf \
    'https://huiyan.baidu.com/boswebsite/cms/report/2024tongqin/2024%E5%B9%B4%E5%BA%A6%E4%B8%AD%E5%9B%BD%E4%B8%BB%E8%A6%81%E5%9F%8E%E5%B8%82%E9%80%9A%E5%8B%A4%E7%9B%91%E6%B5%8B%E6%8A%A5%E5%91%8A.pdf'
  # ③ 百度城市交通报告 PDF（季度/年度，已验证 2026Q2 可下）
  curl -sS -A "$UA" -o 2026Q2城市交通报告.pdf \
    'https://huiyan.baidu.com/cms/report/2026Q2jiaotong/2026%E5%B9%B4%E7%AC%AC2%E5%AD%A3%E5%BA%A6%E4%B8%AD%E5%9B%BD%E5%9F%8E%E5%B8%82%E4%BA%A4%E9%80%9A%E6%8A%A5%E5%91%8A.pdf'
  # ④ 交通运输部 月度城市客运量（正文含 xlsx 相对链接 ./P0….xlsx）
  curl -sS -A "$UA" 'https://xxgk.mot.gov.cn/jigou/zhghs/202607/t20260721_4210104.html'
  ```
  结果形态：慧眼 = **JSONP**（`cb({"data":{"list":{"list":[{id,title,link,pdf_link,…}]}}})`）；报告本体 = **PDF**；高德站 = JS 会话驱动的 JSP 页面；交通运输部 = HTML + xlsx。
- 覆盖：**通勤监测报告** 年度（2022/2023/2024 有直链，2025 落地页 `id=189` 已上线）；**百度城市交通报告** 季度·年度（2019Q3 起，最新 2026Q2）；**慧眼报告中心**共 64 期（含假期出行预测，见 `mobility.md`）；**高德交通分析报告** 季度/年度（入口）；**交通运输部城市客运量**月度（分省 xlsx）。
- 门槛：**免费、免登录**（慧眼 API 与 PDF 直链均无 key）；高德 `report.amap.com` 的 `/index.do`、`/download.do` 依赖 JS 会话，CLI 直取受限（见坑 3）。
- 实测：2026-10-03，macOS arm64，curl 8.x，桌面 UA，20 s 超时：
  - `GET huiyan.baidu.com/hycms/home/reports.jsonp?issue=true` → **200**，256 KB，`pagination.total=64`；`?role=traffic&issue=true` → **200**，243 KB，`total=63` ✅
  - `GET .../reports/landing?id=190` → **200**，title「百度地图《2025年度中国城市交通报告》」；`?id=189` → **200**，title「百度地图《2025年度中国主要城市通勤监测报告》」✅
  - `GET`（Range 0-200）`.../cms/report/2026Q2jiaotong/2026年第2季度中国城市交通报告.pdf` → **200** `application/pdf` 17 312 009 B，magic `%PDF-1.3` ✅
  - `GET`（Range 0-200）`.../boswebsite/cms/report/2024tongqin/2024年度中国主要城市通勤监测报告.pdf` → **200** `application/pdf` 6 312 472 B ✅；`.../2023tongqin/2023年度中国主要城市通勤监测报告.pdf` → **200** 5 121 596 B ✅
  - `GET planning.org.cn/news/view?id=16083` → **200**，title「《2024年度中国主要城市通勤监测报告》发布-学会资讯-中国城市规划网」✅
  - `GET report.amap.com/` → **200**，title「高德交通--中国主要城市交通分析报告」；`/home.html` → **200**「高德大数据」；`/migrate/index.do` → **200**，title「中国主要城市迁徙排名」；`/index.do`、`/download.do` → **200** 但仅 **89 B** 的 `window.location.reload()` 存根 ⚠️
  - `GET xxgk.mot.gov.cn/jigou/zhghs/202607/t20260721_4210104.html` → **200**，title「2026年1-6月全国城市客运量」，正文含 xlsx 附件链接 `./P020260721336688693301.xlsx` ✅；`GET mot.gov.cn/shuju/index.html` → **200**，110 KB ✅
- 上游：中国城市规划设计研究院（报告联合发布方）；百度地图慧眼 <https://huiyan.baidu.com/reports>；高德交通 <https://report.amap.com/>；交通运输部 <https://www.mot.gov.cn/shuju/>。

## 细节

### 慧眼 `reports.jsonp` 清单与 PDF 直链模板

- 清单：`https://huiyan.baidu.com/hycms/home/reports.jsonp?issue=true`（全部）/ `&role=traffic`（交通类）；每条字段 `id / title / abstract / link / pdf_link / cover / role / issue_time`。
- 落地页：`https://huiyan.baidu.com/reports/landing?id={id}`（可加 `&role=traffic`）。
- 报告 id（实测自清单，便于直接拼 URL）：

| id | 报告 | link（PDF 目录） |
|---|---|---|
| 195 / 194 | 2026 年第 2 季度·中国城市交通报告 | `huiyan.baidu.com/cms/report/2026Q2jiaotong/` |
| 192 / 193 | 2026 年第 1 季度·中国城市交通报告 | `huiyan.baidu.com/cms/report/2026Q1jiaotong/` |
| 190 / 191 | 2025 年度·中国城市交通报告 | `huiyan.baidu.com/cms/report/2025jiaotong/` |
| 187 / 188 | 2025 年第 3 季度·中国城市交通报告 | `huiyan.baidu.com/cms/report/2025Q3jiaotong/` |
| 184 / 185 | 2025 年第 2 季度·中国城市交通报告 | `huiyan.baidu.com/cms/report/2025Q2jiaotong/` |
| 182 | 2025 年第 1 季度·中国城市交通报告 | `huiyan.baidu.com/cms/report/2025Q1jiaotong/index.html` |
| 179 | 2024 年度·中国城市交通报告 | `huiyan.baidu.com/cms/report/2024annualtrafficreport/` |
| 189 | 2025 年度·中国主要城市通勤监测报告 | `huiyan.baidu.com/boswebsite/cms/report/2025tongqin/` |
| 177 / 178 | 2024 年度·中国主要城市通勤监测报告 | `huiyan.baidu.com/boswebsite/cms/report/2024tongqin/` |
| 158 / 159 | 2023 年度·中国主要城市通勤监测报告 | `huiyan.baidu.com/boswebsite/cms/report/2023tongqin/` |

- PDF 文件名规律：城市交通报告 = `{YYYY年第N季度中国城市交通报告}.pdf` 或 `百度地图《{YYYY}年度中国城市交通报告》.pdf`；通勤监测报告 = `{YYYY}年度中国主要城市通勤监测报告.pdf`。以 `pdf_link` 字段为准，勿硬编码中文名。

### 高德 `report.amap.com`

| 路径 | 内容 | 本机 |
|---|---|---|
| `/` | 站点入口（title 中国主要城市交通分析报告） | 200 |
| `/home.html` | 高德大数据（实时拥堵监测） | 200 |
| `/migrate/index.do` | 中国主要城市迁徙排名（春运交通播报） | 200 |
| `/index.do`、`/download.do` | 报告列表/下载（JSP 会话 + 阿里 baxia 反爬） | 89 B reload 存根 |

- 静态资源与图表数据在 OSS：`traffic-report-statics.oss-cn-beijing.aliyuncs.com`、`alibaba-traffic-brain.oss-cn-beijing.aliyuncs.com`（含 `jspdf.js`/`highcharts.js`，报告由前端生成）。第三方研报站（发现报告、东方财富 `pdf.dfcfw.com`）常见同份 PDF 镜像。

### 交通运输部 城市客运量

- 列表入口：`https://www.mot.gov.cn/shuju/`（数据栏目）→ 月度文章在综合规划司信息公开 `https://xxgk.mot.gov.cn/jigou/zhghs/{YYYYMM}/t{YYYYMMDD}_{id}.html`。
- 正文附 **xlsx**（相对路径 `./P020…xlsx`，须按文章所在年月目录拼全）；含分省城市客运量、公共汽电车/轨道交通/出租等分方式。

## 坑

1. **慧眼 PDF 不要用 HEAD**：该域对 `curl -I` 一律回 **500**，但 `GET`（含 `-r 0-200`）正常 200 —— 下载前先 `GET` 取 magic `%PDF` 再用 `-o` 拉全量，勿以 HEAD 状态码判定链接死活。
2. **2025 年度通勤报告的 `pdf_link` 被截断**：清单里为 `…/2025tongqin/2025`、落地页「下载报告PDF」也指向它，实测 **500**；2025 报告请走落地页 `?id=189` 内嵌长图，或 2024/2023 的完整 PDF 直链。2025 年度城市交通报告（`id=190/191`）的 `pdf_link` 同样被截断，但其季度报告（`2025Q1~Q3`）链接完整可用。
3. **高德站是 JS 会话 + baxia**：`/index.do`、`/download.do` 直接请求只回 89 B 的 `window.location.reload()`，须带浏览器指纹/会话；报告 PDF 建议从浏览器或第三方研报镜像取。
4. **百度落地页是长图不是 PDF**：`reports/landing` 与 `jiaotong.baidu.com/reports/landing` 的报告正文由 `bj.bcebos.com/mapopen/report/*.png`（带 `authorization` 签名的临时图）承载，签名会过期；要可留存的 PDF 用慧眼 `pdf_link`。
5. **口径来源不同**：通勤监测报告由**中国城市规划设计研究院 + 百度地图慧眼**联合发布（基于手机信令/百度位置大数据），高德报告基于高德浮动车与导航数据；两者指数不可混用同一表，引用须写全发布方与期次。
6. **交通运输部客运量是官方统计口径**（分省 xlsx），与百度/高德的商业指数属不同量纲，做「通勤」需自行折算，勿直接对齐。
7. 假期类报告（五一/十一/春节出行预测）在慧眼清单里期数最全，且多为 `.jpg` 长图；要结构化数字仍得回 `mobility.md` 的迁徙 API。
