# neac.gov.cn —— 民族统计·政策与名录

- 去哪找：**国家民族事务委员会**官网 `https://www.neac.gov.cn/`；资料栏目 `https://www.neac.gov.cn/seac/ziliao/index.shtml`（民族地区经济社会发展统计数据 `/seac/c103544/common_list.shtml`、少数民族古籍 `/seac/c103545/common_list.shtml`、民族团结进步教育基地 `/seac/c103547/common_list.shtml`、创建示范单位 `/seac/c103548/common_list.shtml`）；政务公开 `https://www.neac.gov.cn/seac/xxgk/index.shtml`；**站内搜索** `https://zs.kaipuyun.cn/s?siteCode=bm08000014&searchWord=<关键词>`（开普云托管）。
- 什么时候用：要**民族地区/自治州的经济社会发展统计公报**；要**民族工作政策文献**（民族团结进步促进法、兴边富民规划、少数民族语言文字工作规划等）；要**民族团结进步教育基地/示范单位名录**；要**少数民族古籍提录**（蒙古文、古壮字、托忒蒙古文等书目）；要国家民委课题/统计管理办法。
- 怎么搜：站点为 TRS WCM 静态页（`/seac/.../index.shtml`、`common_list.shtml`、`年月份/编号.shtml`），**直接抓 HTML**；站内检索走开普云，**服务端渲染**，URL 模板：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
  curl -sS -A "$UA" --compressed \
    'https://zs.kaipuyun.cn/s?siteCode=bm08000014&searchWord=%E6%B0%91%E6%97%8F%E7%BB%9F%E8%AE%A1&pageNum=1'
  # → 200，HTML（约 330 KB），正文含「相关结果 N 个」与命中列表；pageNum 翻页
  ```
  结果形态：**HTML**（开普云页内直接嵌结果，无独立 JSON 接口）；栏目页亦为静态 HTML。
- 覆盖：统计栏目聚合**国家统计公报（2024/2025）+ 各自治州统计公报**（伊犁、克孜勒苏柯尔克孜等，逐年）；民族政策法规与规划全文；民族团结进步教育基地/示范单位名录；少数民族古籍书目条目；更新随站内发稿（2026 年在更）。
- 门槛：**免费、免登录、无 key**；开普云需带 `siteCode=bm08000014`。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA——`GET https://www.neac.gov.cn/` → **200**（34 KB，`<title>国家民族事务委员会</title>`）；`GET /seac/ziliao/index.shtml` → 200，栏目含「民族地区经济社会发展统计数据 / 少数民族古籍 / 民族团结进步教育基地 / 民族团结进步创建示范单位」；`GET https://zs.kaipuyun.cn/s?siteCode=bm08000014&searchWord=民族统计` → **200，344 KB HTML**，含命中「民族统计工作管理办法」与「相关结果 18 个」；`?…&pageNum=2` 正常翻页。
- 上游：<https://www.neac.gov.cn/>（中华人民共和国国家民族事务委员会）；站内搜索由开普云 `zs.kaipuyun.cn` 提供。

## 细节

### 常用栏目

| 栏目 | URL |
|---|---|
| 资料总入口 | `/seac/ziliao/index.shtml` |
| 民族地区经济社会发展统计数据 | `/seac/c103544/common_list.shtml` |
| 少数民族古籍 | `/seac/c103545/common_list.shtml` |
| 民族团结进步教育基地 | `/seac/c103547/common_list.shtml` |
| 民族团结进步创建示范单位 | `/seac/c103548/common_list.shtml` |
| 政务公开（政策文件/解读/规划/预决算/采购） | `/seac/xxgk/index.shtml` |

- 直属单位与主管社团名单在 `/seac/mwjs/zsgx/`、`/seac/mwjs/zswhdw/`、`/seac/mwjs/zgst/`（含中央民族大学、民族出版社、中国民族语文翻译中心、中国民族博物馆、中国民族报社等）。
- 开普云搜索参数：`siteCode`（该站固定 `bm08000014`）、`searchWord`、`pageNum`；无 Referer 要求，但保留 `-A` 桌面 UA。

## 坑

1. 开普云页返回体量大（~330 KB/页），正文混排导航与页脚，抽取结果需按「相关结果」锚点定位。
2. 统计栏目本身**不产数据**，只**转载**国家统计局与各自治州公报；要结构化数字仍回 `../stats/data.stats.gov.cn.md`，本卡只作民族口径汇编线索。
3. 部分栏目（如「专题」`/seac/ztzl/`）为历史专题，链接指向外部（新华、地方民宗委、微信公众号），引用前核原始发布方。
4. 站内许多正文含外链图片与附件（`/seac/.../P020….pdf` 之外多为网页正文），未提供批量数据下载。
