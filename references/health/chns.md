# chns —— 中国健康与营养调查

- 去哪找：项目主页 `https://chns.cpc.unc.edu/`；数据页 `https://chns.cpc.unc.edu/data`；数据集清单 `/data/datasets/index`；UNC Dataverse 镜像 `https://data.cpc.unc.edu/projects/7/view`。
- 什么时候用：要**中国家庭/个体长期健康与营养面板**（膳食 24 小时回忆、体格测量、生物标记、收入、劳动、生育）；做营养转型、慢性病、儿童生长、城乡/社会经济差异研究；需要**多轮纵向追踪**的微观数据。
- 怎么取：站点按**调查年份打包**下载（zip），配问卷/编码本等文档——
  ```
  https://chns.cpc.unc.edu/data            → 数据与文档总览
  https://chns.cpc.unc.edu/data/datasets/index  → 数据集清单
  ```
  形态：网页 + zip（数据 + 文档）；无公开 API。
- 覆盖：**1989 年启动，至 2015 年共 10 轮**（2019 年采集见站方新闻）；9 省城乡居民住户与个体；2009/2015 年生物标记数据已发布；逾 4 万住户、跟踪 35 年（上游声明）。
- 门槛：免费；数据下载站方称可直接从网站下载，**是否需注册/登录未本机验证**；使用须遵守其数据使用条款。
- 实测：2026-10-03，macOS arm64，curl 桌面 UA：`https://www.cpc.unc.edu/projects/china` 301 → `https://chns.cpc.unc.edu/` 200（33,509 B，`<title>CHNS`）。
- 上游：UNC Carolina Population Center（NIH 资助）。

## 细节

### 数据组织

| 资源 | 位置 |
|---|---|
| 数据总览 | `https://chns.cpc.unc.edu/data` |
| 数据集清单 | `https://chns.cpc.unc.edu/data/datasets/index` |
| 新闻/发布公告 | `https://chns.cpc.unc.edu/news` |
| UNC Dataverse 项目页 | `https://data.cpc.unc.edu/projects/7/view` |

- 文件按 survey year 打包（zip）；含个体/住户/社区等多层问卷与生物标记。
- 常被用于与 `../surveys/` 层其他中国微观调查（CFPS/CHARLS/CHIP 等）对照。

## 坑

1. 站点**换过域名/结构**：旧链接 `cpc.unc.edu/projects/china` 现 301 到 `chns.cpc.unc.edu`，脚本里请写新域。
2. 各年份问卷变量不完全可比（新增/改题），做纵向面板须先核编码本。
3. 数据使用有条款限制（学术用途为主），再分发前看清许可。
4. 2019 轮数据发布状态以站方 news 为准（本机未验证下载流程）。
