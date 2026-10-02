# worldvaluessurvey.org —— 世界价值观调查

- 去哪找：门户 `https://www.worldvaluessurvey.org/`；各波文档 `https://www.worldvaluessurvey.org/WVSDocumentationWV7.jsp`（WV1–WV7 同理换编号）；在线分析 `https://www.worldvaluessurvey.org/WVSOnline.jsp`；欧洲姊妹项目 EVS `https://europeanvaluesstudy.eu/`。
- 什么时候用：要**公众价值观/态度**（政治信任、宗教、性别角色、家庭、腐败容忍、环境、幸福、移民态度）；跨国跨波比较社会心态；做"制度 × 民意"交互研究。
- 怎么取：官网正文由 JS（`SetContent(...)`）注入，curl 只拿到壳；**数据下载在各波的 Documentation 页**，逐波提供 SPSS/Stata/CSV，需注册/同意条款（上游声明，本机未实测下载流程）。
  - 联合趋势文件（EVS-WVS 1981–2022）与各波文件同站；EVS 侧入口在 `europeanvaluesstudy.eu`。
  - 常见转引：QoG（`wvs_*`）、GESIS（部分波次 ZA 编号）。
- 覆盖：WV1 1981 → **WV7 2017–2022**（80+ 国家/地区）；EVS 1981–至今（欧洲）；粒度=个体受访者（概率/配额抽样），国家 × 波（上游声明，未本机实测）。
- 门槛：免费；**下载多需注册并接受条款**；在线分析工具可免登录跑交叉表。
- 实测：2026-10-03，macOS arm64，curl 8.x：`https://www.worldvaluessurvey.org/` → 200；`WVSDocumentationWV7.jsp` → 200 / 13.5 KB（页面链接全是 `javaScript:SetContent(...)` 锚点，抓不到数据直链）；`WVSDataArchive.jsp` → **404**（旧路径已废）；`https://europeanvaluesstudy.eu/` → 200 / 339 KB。
- 上游：`https://www.worldvaluessurvey.org/`（WVSA）；`https://europeanvaluesstudy.eu/`（EVS）。

## 细节

### 入口速查

| 项目 | 入口 |
|---|---|
| WVS 各波文档 | `WVSDocumentationWV1..WV7.jsp` |
| WVS 在线交叉表 | `WVSOnline.jsp` |
| EVS 官网/数据 | `europeanvaluesstudy.eu` |
| 合并趋势文件 | WVS 站内 "EVS-WVS trend" 相关页 |

## 坑

1. 站点是**老式 JS 注入页面**，curl/爬虫拿不到正文与下载直链；下载必须浏览器（或反向其表单接口，未验证）。
2. 各波变量命名不统一（WV7 用 `Q*` 编号），跨波合并要用官方合并文件或逐波映射。
3. 抽样多为 1000–2000 人/国，**国别均值误差大**，别当精确统计。
4. 同波有多次修订版本（如 WV7 v1–v4），引用须注明版本。
5. 中国大陆仅在部分波次入样，做面板前先查各波覆盖表。
