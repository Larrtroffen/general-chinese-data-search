# emdat.be —— 国际灾害事件数据库

- 去哪找：EM-DAT 项目站 `https://www.emdat.be/`；数据查询/导出平台 `https://public.emdat.be/`（Login / Register / Documentation）；数据文档 `https://doc.emdat.be/`。
- 什么时候用：要**全球灾害事件级面板**——灾种（洪水/风暴/地震/干旱/高温…）、国家、起止日期、死亡/受伤/受灾/无家可归人数、经济损失、国际援助；做灾害-经济、气候适应、应急管理跨国研究；中国灾害事件可作国际对标。
- 怎么搜：数据在 `public.emdat.be` 的账户体系内（Next.js 应用），登录后按灾种/国家/年份筛选并导出（通常 xlsx/csv）；`doc.emdat.be` 给出口径、偏差与法务说明。无匿名 API 端点（本机未发现）。
- 覆盖：全球 · 1900–至今（1970 年后覆盖较全）· 事件级 · 年度更新（每年数次）。
- 门槛：**免费注册**（学术/非商业用途；商业用途需付费授权）——注册与用途条款见平台（上游声明，未本机实测注册流程）。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA）——`https://www.emdat.be/` → 200（365,842 B）；`https://public.emdat.be/` → 200（14,226 B，Next.js 应用，导航为 `Public EM-DAT / Login / Register / Documentation / EM-DAT Project`）；`https://doc.emdat.be/` → 200（65,054 B，标题「EM-DAT Documentation」）。
- 上游：CRED（灾害流行病学研究中心）· UCLouvain（比利时鲁汶大学）；页脚署名 `CRED/UCLouvain`。

## 细节

- 平台入口分工：`emdat.be`＝项目介绍与新版本公告；`public.emdat.be`＝取数；`doc.emdat.be`＝方法论/口径/引用要求。
- 结构：账号 → 数据集勾选 → 筛选（国家/灾种/时间/指标）→ 导出；**导出字段与灾种编码**见文档站，引用需带 EM-DAT 版本号与访问日期。

## 坑

1. **不是匿名下载**：`public.emdat.be` 必须注册登录；想脚本直取 JSON 的路子本机未找到，按「需浏览器」处理。
2. 不同灾种**起始年份与阈值不同**（如 1900 年前后差异大），跨国长期比较要看覆盖说明，别把「无记录」当「未发生」。
3. **损失/受灾人数口径**经多次修订、且有缺失值（null），建模前先做缺失与一致性检查。
4. 商业用途需授权，学术使用也要按站点要求署名（CRED/UCLouvain + 版本）。
5. 与国内灾害统计（应急管理部 `mem.gov.cn` 统计公报，见 [`../stats/ministry-stats.md`](../stats/ministry-stats.md)）口径不同（中国的自然灾害损失以灾情统计为主），跨国对比需说明来源差异。
