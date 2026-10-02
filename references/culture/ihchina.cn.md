# ihchina.cn —— 非遗名录与传承人检索

- 去哪找：**中国非物质文化遗产网·中国非物质文化遗产数字博物馆**`https://www.ihchina.cn/`；名录入口 `/project.html`、传承人 `/representative`、UNESCO 名录 `/chinadirectory.html`、文化生态保护区 `/shiyanshi`、生产性保护示范基地 `/shifanjidi`、联合国名录名册 `/directory_list`。
- 什么时候用：要**国家级非物质文化遗产代表性项目名录**（五批 1557 项，按十大门类）；要**国家级代表性传承人名单**（六批，含姓名/性别/民族/类别/项目编号/申报地区）；要**国家级文化生态保护区/生产性保护示范基地**；要**中国列入 UNESCO 非遗名录、名册项目**；做非遗清单核对、项目-传承人关联。
- 怎么搜：名录列表由 **JSON 接口**驱动，可直接 curl：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
  # ① 国家项目名录（关键词 + 门类 + 地区 + 时间 + 分页）
  curl -sS -A "$UA" --compressed 'https://www.ihchina.cn/getProject.html?province=&rx_time=&type=&cate=&keywords=%E7%9A%AE%E5%BD%B1&category_id=&limit=10&p=1'
  # → 200 JSON {"total":37,"list":[{"num":"Ⅶ-91","title":"皮影戏…"}],…}
  # ② 代表性传承人
  curl -sS -A "$UA" --compressed 'https://www.ihchina.cn/art/representative.html?province=&rx_time=&type=&sex=&keywords=%E7%9A%AE%E5%BD%B1&limit=10&p=1'
  # → 200 JSON {"total":59,"list":[{"num":"02-0663","title":"丁振耀","sex":"男","nation":"汉族","project_num":"Ⅶ-91",…}]}
  ```
  参数：`keywords` 关键词、`province` 地区、`type`/`cate`、`rx_time` 公布时间、`sex`（仅传承人）、`limit` 每页、`p` 页码；`category_id=1..10` 对应十大门类（民间文学/传统音乐/传统舞蹈/传统戏剧/曲艺/传统体育游艺与杂技/传统美术/传统技艺/传统医药/民俗）。保护区与示范基地页为**服务端渲染 HTML**。
- 覆盖：国家级项目名录五批（2006/2008/2011/2014/2021，合计 **1557 项**）；国家级传承人六批（页面自述截至 2025 年 12 月共 **3994 人**，检索头显示「共 3995 条」）；中国入选 UNESCO 非遗名录/名册项目；国家级文化生态保护区、生产性保护示范基地。
- 门槛：**免费、免登录、无 key**；URL 编码关键词即可。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA（带 `X-Requested-With`/`Referer` 亦同）——`GET /getProject.html?keywords=皮影&limit=10&p=1` → **200 JSON**，`total:37`；`GET /art/representative.html?keywords=皮影&limit=10&p=1` → **200 JSON**，`total:59`，首条 `02-0663 丁振耀 男 汉族 传统戏剧 Ⅶ-91 皮影戏`；`GET /project.html` → 200 HTML，正文「共计1557个国家级非物质文化遗产代表性项目」。
- 上游：<https://www.ihchina.cn/>（文化和旅游部主管、中国非物质文化遗产保护中心主办）。

## 细节

### 接口与页面

| 资源 | URL | 形态 |
|---|---|---|
| 国家级项目名录 | `/getProject.html?province=&rx_time=&type=&cate=&keywords=&category_id=&limit=10&p=1` | JSON |
| 国家级传承人 | `/art/representative.html?province=&rx_time=&type=&sex=&keywords=&limit=10&p=1` | JSON |
| 项目/传承人页面 | `/project.html`、`/representative` | HTML |
| 中国入选 UNESCO 项目 | `/chinadirectory.html`、`/directory_list` | HTML |
| 文化生态保护区 / 示范基地 | `/shiyanshi`、`/shifanjidi` | HTML |

- 项目记录字段：`num`（编号 Ⅶ-91）、`title`、`category_id`、申报地区等；传承人记录字段：`num`（02-0663）、`title`（姓名）、`sex`、`nation`、`type`（门类）、`project_num`、`project`、`day`（出生年）。
- 分页链接在 JSON 的 `links` 内给出（`total_pages`/`current`）。

## 坑

1. 关键词走 `keywords`（不是 `kw`）；门类筛选走 `category_id`（数字 1–10），项目接口另有 `cate`。
2. `total` 与页面自述人数可能差 1（3995 vs 3994），系名册与检索库口径差，引用以官网名录页为准。
3. 名录详情页按 `/news_details/…`、`/zhengce_details/…` 等分路由，抓取正文须按栏目前缀区分。
4. 部分内嵌媒体在 `https://www.ihchina.cn/Uploads/Media/…`，下载不设限但无批量清单。
5. UNESCO 部分（`/chinadirectory.html`）为**HTML 静态页**，不提供 JSON，需解析页面。
