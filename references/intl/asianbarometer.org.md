# asianbarometer.org —— 亚洲晴雨表调查

- 去哪找：门户 `https://www.asianbarometer.org/`；数据页 `https://www.asianbarometer.org/data`；区域项目汇总 `https://globalbarometer.net/`（Global Barometer Surveys，含 Asian/Latinobarómetro/Afrobarometer/Arab Barometer 入口）。
- 什么时候用：要**东亚/东南亚/南亚公众**的政治态度（民主观、选举、政党与议会信任、腐败、治理评价、威权支持）；做亚洲比较政治；补 WVS/Afrobarometer 之外的区域覆盖。
- 怎么取：
  - 官网 `/data` 逐波提供数据（SPSS/Stata），需填用途表单/同意条款；页面为 Tomcat + JS 渲染，curl 只见壳。
  - 汇总入口在 Global Barometer Surveys `https://globalbarometer.net/`（首页导航进入各区域项目）。
  - 转引：QoG 含部分 ABS 变量。
- 覆盖：Wave 1 (2001–2003) → Wave 5+；东亚/东南亚/南亚十余个经济体；个体级；约 3–4 年一波（上游声明，未本机实测）。
- 门槛：免费；**需注册/填写用途表单**（上游声明，本机未实证下载流程）。
- 实测：2026-10-03，macOS arm64，curl 8.x：`https://www.asianbarometer.org/data` → 200 / 18 KB（title "Asian Barometer"，`lang="zh-Hant"`；除 CSS/字体外仅 `_release.jsp` 链接，正文与下载项由 JS 注入）；`https://globalbarometer.net/` → 200（Tomcat 应用）；`https://globalbarometer.net/data` → **404**。
- 上游：Asian Barometer Survey（中研院政治学所等）；`https://globalbarometer.net/`。

## 坑

1. 站点技术老旧（Tomcat + JS 注入），curl 抓不到数据直链，必须浏览器操作。
2. 中国大陆是否入样、以何名义入样，各波不同——**先看每波覆盖表**再用。
3. `globalbarometer.net` 的 `/data` 路径 404，入口只在首页导航，别硬拼 URL。
4. ABS 与 WVS 亚洲模块题目重叠但抽样与措辞不同，跨国合并要谨慎。
5. 各波问卷与变量有改动，跨波比较须读对应 codebook。
