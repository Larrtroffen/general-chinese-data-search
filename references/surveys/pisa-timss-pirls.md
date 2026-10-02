# pisa-timss-pirls —— 国际教育测评的中国数据

- 去哪找：
  - **PISA**：数据文件直链服务器 `https://webfs.oecd.org/pisa2022/`（按文件名直取，如 `STU_QQQ_SPSS.zip`）；数据集页 `https://www.oecd.org/en/data/datasets/pisa-2022-database.html`（新页 `…/pisa-2022-database.html`）；在线制表 `https://pisadataexplorer.oecd.org/ide/idepisa/`；OECD SDMX API `https://sdmx.oecd.org/public/rest/`。
  - **TIMSS / PIRLS**：IEA 数据仓 `https://www.iea.nl/data-tools/repository`；TIMSS 2019 国际数据库 `https://timss2019.org/international-database/`；PIRLS 2021 `https://pirls2021.org/data/`；项目主页 `https://timssandpirls.bc.edu/`。
- 什么时候用：**跨国/地区教育测评比较**——PISA（15 岁学生阅读/数学/科学素养与问卷）、TIMSS（四年级/八年级数学科学）、PIRLS（四年级阅读）；要学生/学校微观数据、趋势与时序比较、中国参与地区（上海、北京-上海-江苏-广东/浙江；香港、澳门、中国台北）的表现。
- 怎么搜：**PISA 微观数据免注册直下 zip**（`webfs.oecd.org/pisa{年}/文件名.zip`）；汇总指标走 PISA Data Explorer 或 OECD SDMX。**TIMSS/PIRLS** 从各期 IDB 下载页按文件取（SPSS/SAS 数据 + 代码本 + 年鉴），如 `https://timss2019.org/international-database/downloads/T19_G4_Almanacs.zip`。结果形态：SPSS/SAS 数据包、Excel/CSV、HTML/PDF 结果报告。
- 覆盖：PISA 2000→2022 数据（2025 结果已发布）；中国参与：**2009/2012 上海**，**2015 北京-上海-江苏-广东**，**2018/2022/2025 北京-上海-江苏-浙江**。TIMSS 1995→2019（中国参与为**香港、中国台北**，无内地）；PIRLS 2001→2021（**香港、澳门、中国台北**）。粒度=学生 + 学校（含问卷与成绩）。
- 门槛：PISA 文件服务器与 TIMSS/PIRLS IDB **免费直下**（无需登录）；OECD 官网页受 Cloudflare 拦 curl，需浏览器；IEA 部分数据/在线工具需免费注册（上游声明）。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA（`-I` 探测）：`https://webfs.oecd.org/pisa2022/STU_QQQ_SPSS.zip` → 200 `application/x-zip-compressed`；同目录 `STU_COG_SPSS.zip`、`STU_QQQ_SAS.zip`、`SCH_QQQ_SPSS.zip` 均 200；`CY08MSP_STU_QQQ.SAV` → 404（文件名不同）；`https://www.oecd.org/en/data/datasets/pisa-2022-database.html` → **403**（Cloudflare「Just a moment…」）；`https://pisadataexplorer.oecd.org/ide/idepisa/` → 200（56 892 B）；`https://sdmx.oecd.org/public/rest/dataflow/all/all/latest?format=structure` → 200（约 8.9 MB，非 CF）；`https://timss2019.org/international-database/` → 200（含 `downloads/T19_G4_*.zip` 链接）；`https://pirls2021.org/data/` → 200；`https://www.iea.nl/data-tools/repository` → 200。
- 上游：OECD PISA；IEA（TIMSS & PIRLS 国际研究中心，波士顿学院）。

## 细节

### PISA 2022 常下文件名（webfs.oecd.org/pisa2022/）

| 文件 | 内容 | 实测 |
|---|---|---|
| `STU_QQQ_SPSS.zip` | 学生问卷 SPSS | ✅ 200 |
| `STU_COG_SPSS.zip` | 学生认知（成绩）SPSS | ✅ 200 |
| `STU_QQQ_SAS.zip` | 学生问卷 SAS | ✅ 200 |
| `SCH_QQQ_SPSS.zip` | 学校问卷 SPSS | ✅ 200 |

年份换目录名即适用（`pisa2018`、`pisa2015`…）；完整文件清单在 OECD 数据集页（需浏览器过 CF）。中国四省市结果另见教育部发布稿 `http://www.moe.gov.cn/jyb_xwfb/gzdt_gzdt/s5987/201912/t20191204_410707.html`。

### TIMSS / PIRLS

- TIMSS 2019 IDB 下载目录：`https://timss2019.org/international-database/downloads/`；文件按 `T19_G4_*`（四年级）、`T19_G8_*`（八年级）命名（Almanacs、Codebooks、Curriculum Data、IRT Item Parameters…）。
- 早期周期与 PIRLS 数据在 `timssandpirls.bc.edu`（项目主站）与各期站点（`timss2015.org`、`pirls2021.org`）分发。
- 中国参与证据：TIMSS 2019 附录 A（`https://timss2019.org/reports/wp-content/themes/timssandpirls/download-center/appendices/T19_AppA_country-participation-trend.pdf`）列 **Hong Kong SAR、Chinese Taipei** 历年参与，无中国内地。

## 坑

- **`webfs.oecd.org` 目录列举 403**，但**具体文件名直链有效**——不要因为目录打不开就以为下不了，直接拼文件名。
- OECD 官网（`www.oecd.org`）对命令行全站 Cloudflare 挑战，`curl` 403；改走 `webfs.oecd.org`（文件）与 `sdmx.oecd.org`（API）绕开。
- **PISA「中国」不是全国样本**：2009/2012 只有上海，2015 起为若干省市联合体（B-S-J-G / B-S-J-Z），比较时口径必须写明，勿当全国均值。
- **TIMSS/PIRLS 无中国内地**：只含香港、澳门、中国台北；想用内地数据需另找（如教育部测评、区域调查）。
- SDMX 端点对 `format` 有要求（`structure`/`xml-struct` 等），乱传返回 **406**；取数据前先查 dataflow。
