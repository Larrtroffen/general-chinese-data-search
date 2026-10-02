# cfforum.org.cn —— 基金会论坛与《基金会蓝皮书》

- 去哪找：**中国基金会发展论坛（CFF）官网** `https://www.cfforum.org.cn/`（运营方：北京基业长青社会组织服务中心）；内容页 `/content/<id>`、栏目页 `/category/<id>`、下载件 `/Uploads/file/…`。
- 什么时候用：要**基金会行业报告与原创成果**（《基金会蓝皮书：中国基金会发展报告》系列）、**历届年会（2016–2025）资料/会议册 PDF**、**基金会秘书长成长计划**、**行业数据观察**（如「基金会数量首现负增长」）；做基金会行业研究与政策脉络梳理。
- 怎么搜：**HTML 站点**，无公开检索 API；栏目 `/category/<id>` 列出文章，详情 `/content/<id>`，报告/会议册为 `/Uploads/file/` 下的 PDF 直链：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
  curl -s -A "$UA" 'https://www.cfforum.org.cn/'                       # 首页
  curl -s -A "$UA" 'https://www.cfforum.org.cn/category/26'            # 历届年会栏目
  curl -sLO -A "$UA" 'https://www.cfforum.org.cn/Uploads/file/20251121/691fc11fa40cc.pdf'  # 会议册 PDF 直链
  ```
  结果形态：**HTML（UTF-8）+ PDF 直链**。
- 覆盖：基金会行业年会 2016–2025（届次/资料）、基金会蓝皮书与研究报告、《基金会发展报告》课题、行业数据观察与媒体报道；粒度=文章/报告/届次；随会议与出版节奏更新。
- 门槛：**免费、免登录**（PDF 直链可下）。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA，20 s 超时）——`GET https://www.cfforum.org.cn/` → **200**，70 987 B，`<title>北京基业长青社会组织服务中心</title>`；首页含「历届年会 2016…2025」「原创成果」「基金会蓝皮书时隔十年重启」等栏目与 `/content/<id>`、`/category/<id>` 链接；`/Uploads/file/…pdf` 为可直下报告/会议册（示例 `…/Uploads/file/20251121/691fc11fa40cc.pdf`）。
- 上游：中国基金会发展论坛 `https://www.cfforum.org.cn/`；北京基业长青社会组织服务中心。

## 细节

- 站内导航栏目（实测）：关于我们、历届年会（2016–2025）、原创成果、品牌项目、伙伴成果、信息公开、党建工作、大事记、团队成员、媒体报道。
- 行业动态常被第三方转载：中国发展简报 `chinadevelopmentbrief.org.cn`、善达网、公益时报、基金会中心网。
- 报告主题样例：《基金会蓝皮书：中国基金会发展报告（2025）》新书发布、基金会双月沙龙、县域基金会发展等。

## 坑

1. 无结构化数据接口，名录/统计只能从文章与 PDF 中摘；跨机构可比数字优先用 `foundationcenter.org.cn.md` 的接口。
2. `/Uploads/file/` 为版本化路径（含日期目录），改版后链接会变，需从栏目页重新解析。
3. 官网 title 是运营方名「北京基业长青社会组织服务中心」，非「中国基金会发展论坛」，检索时勿混淆。
