# CGSS —— 全国年度综合性社会调查

- 去哪找：项目门户 `http://cgss.ruc.edu.cn/`（HTTPS 不通，见「坑」）；数据检索/下载 `https://www.cnsda.org/`；新平台「中国人民大学社会科学数据资源平台」`https://cssd.ruc.edu.cn/`。
- 什么时候用：要**年度横截面**的社会态度、阶层认同、劳动力、家庭、健康、政治参与等主题；做社会变迁趋势、东亚（EASS）与国际比较。
- 怎么取：`cgss.ruc.edu.cn` 的「调查数据」入口跳转到 CNSDA；在 CNSDA 检索到 CGSS 各年项目页后按提示注册/申请下载。2026-07 起可改用 CSSD 平台：实名认证 + 签数据使用协议后，公开数据一键下载、受限数据在线审批。
- 覆盖：2003 年启动，累计执行 17 次年度调查、公开发布 13 期数据（截至 2026-08 公告）；每轮对中国大陆 31 省区市 1 万多户家庭做连续性横截面调查；CGSS2023 数据于 2025-06-21 公开发布。
- 门槛：免费；需注册 + 实名 + 签数据使用协议；受限数据需审批。
- 实测：2026-10-03，curl 桌面 UA：`http://cgss.ruc.edu.cn/` → 200（13,674 B；`https://` 握手失败）；项目概况页 `…/xmjs/xmgk.htm` → 200（16,688 B）；`https://cssd.ruc.edu.cn/` → 200（SPA，878 B）；CNSDA 检索 `?r=projects/index&Projects[title]=综合社会调查` → 200（共 14 条）。
- 上游：中国人民大学中国调查与数据中心（NSRC）`http://nsrc.ruc.edu.cn/`。

## 细节

- CSSD 平台已发布数据集（2026-08-27 上线公告）：CGSS（13 期）、CEPS（3 期）、CLASS 中国老年社会追踪调查（5 期）、中国雇主—雇员匹配数据跟踪调查（7 期）；另有中国发展信心调查等 4 个待上线。
- CNSDA 数据目录：`https://www.cnsda.org/index.php?r=projects/index`（见 `cnsda.org.md`）。
- CGSS 是东亚社会调查（EASS，2006 起，与 JGSS/KGSS/TSCS）成员，2007 年代表中国加入 ISSP。
- 姊妹调查：CLASS `http://class.ruc.edu.cn/`、CRS 中国宗教调查 `http://crs.ruc.edu.cn/`。

## 坑

- `cgss.ruc.edu.cn` **只走 HTTP**（本机 HTTPS 握手失败，`www.` 前缀亦不通）。
- 官网「数据与成果」只做跳转，真正的下载/申请在 CNSDA 与 CSSD，别在项目站内找数据文件。
- CGSS 为**年度横截面**（非同一批人追踪），做面板分析要与其他追踪调查（CFPS/CHARLS）区分。
