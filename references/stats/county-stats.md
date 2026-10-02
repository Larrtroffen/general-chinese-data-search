# county-stats —— 县级面板与统计公报取数

县级没有全国统一的免费面板；实际可获取性 = **逐县统计公报（HTML，免费）+ 少数县自印统计年鉴（PDF/ZIP，免费）+ 《中国县域统计年鉴》（付费库）**三层拼。

- 去哪找：
  - 县级公报聚合（免费、非官方）：红黑统计公报库 `https://tjgb.hongheiku.com/category/xjtjgb`；按县 `https://tjgb.hongheiku.com/tag/<县名>`
  - 知网·中国经济社会大数据平台《中国县域统计年鉴》：县市卷 2024 `https://data.cnki.net/trade/yearBook/single?id=N2025020141&zcode=Z026`；**乡镇卷** 2022 `https://data.cnki.net/trade/yearBook/single?id=N2023030095&zcode=Z026`（登录门槛见 `cnki-data.md`）
  - 逐县官方发布位：县统计局/县政府网「统计公报」栏目；**地级市统计局常整编区县公报**，如长沙 `https://tjj.changsha.gov.cn/tjxx/tjsj/tjgb/qxgb/`
  - 县级统计年鉴免费样例：昆山 `https://www.ks.gov.cn/kss/tjnj/`（正文页挂 zip 直下）
  - 县级财政：县政府「财政预决算公开」专栏 + 县财政局《全县及县级财政决算说明》PDF；或《县域统计年鉴》「按地方一般公共预算收入分组」
  - 中郡县域经济大数据 `http://dashujupt.china-county.org/index.php/home/city?code=<6位区划码>`
- 什么时候用：要**县/县级市/市辖区**的 GDP、常住/户籍人口、一般公共预算收入、规上工业、投资、居民收入等年度值；做县级面板、县域榜单核对、乡镇级粗数据。
- 怎么搜（县级公报无统一 API，走「三条发布位」）：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # ① 聚合库：全文搜索（WordPress ?s=）+ 按县 tag 列历年
  curl -sS -A "$UA" 'https://tjgb.hongheiku.com/?s=%E5%BE%B7%E6%B8%85%E5%8E%BF'
  curl -sS -A "$UA" 'https://tjgb.hongheiku.com/tag/%E6%98%86%E5%B1%B1%E5%B8%82'
  # ② 地级市统计局「区县公报」栏目（长沙模式）
  curl -sS -A "$UA" 'https://tjj.changsha.gov.cn/tjxx/tjsj/tjgb/qxgb/'
  # ③ 县府/县统计局栏目（路径见下）；免费年鉴直下 zip
  curl -sS -A "$UA" 'https://www.ks.gov.cn/kss/tjnj/202601/<hash>.shtml'
  ```
  结果形态：聚合库与县府公报为 **HTML 全文**（数值在正文/附表中，非结构化）；昆山年鉴为 **zip**（XLS 表）；知网为 **SPA + 登录**。
- 覆盖：县级公报 2000s–2025（聚合库覆盖 2000+ 县，**逐年完整度不一**）；昆山等县自印年鉴近年齐全；《县域统计年鉴》县市卷 2000–2025、乡镇卷 2000–2025（跨年自述，未逐年核）；中郡县域面板仅到 **2019/2020** 左右且含 2018 旧值。
- 门槛：县级公报与聚合库 **免费**；县级年鉴 zip 免费（昆山实测可下，39 MB）；《县域统计年鉴》**付费/登录**（县市卷+乡镇卷）；中郡免费但数据陈旧；县级财政预决算 PDF 免费。
- 实测：2026-10-03，macOS arm64，curl 8.x，桌面 UA，20 s 超时，≥1.5 s 间隔：
  - `https://tjgb.hongheiku.com/category/xjtjgb` → 200（县级公报目录，分页 `/page/2`）✅；`/tag/昆山市` → 200（22,491 B，列 5 篇历年公报）✅；`/xjtjgb/xj2020/18651.html` → 200（51,103 B，`(湖州市)2012年德清县国民经济和社会发展统计公报`）✅；`/?s=德清县` → 200（title「搜索结果 德清县」）✅
  - `https://tjj.changsha.gov.cn/tjxx/tjsj/tjgb/qxgb/` → 200（长沙县/浏阳市/宁乡市/望城区/天心区 2025 公报同页列出）✅
  - `https://www.ks.gov.cn/kss/tjnj/202601/a10be7f64b8643dfa9f11ca8ea0b46d7.shtml` → 200（附件 `…/files/…zip`；HEAD → 200 `application/zip` **39,396,830 B**）✅
  - `https://data.cnki.net/trade/yearBook/single?id=N2025020141&zcode=Z026`（县市卷2024）→ 200（11,460 B SPA 壳）⚠️；`id=N2023030095`（乡镇卷2022）→ 200 ⚠️
  - `http://dashujupt.china-county.org/index.php/home/city?code=330521` → 200（德清 人口 54.86 万/2020、GDP 537.01 亿/2019、公共财政）✅
  - 县级财政样例 `https://oss.jiaozuo.gov.cn/jiaozuo_xiuwu/sitesources/xwxrmzf/upload/202311/20231124093607895.pdf` → 200 `application/pdf`（修武县 2022 财政决算说明）✅
- 上游：红黑统计公报库（第三方）；国家统计局《中国县域统计年鉴》（县市卷/乡镇卷）→ `data.cnki.net`；各县统计公报原发各县统计局；中郡县域经济研究所；财政部（县级决算只有各县自公开）。

## 细节

### 县级公报的三条发布位（按命中率排序）

| # | 发布位 | 路径规律 | 备注 |
|---|---|---|---|
| ① | **地级市统计局**「区县公报」栏 | `tjj.<市>.gov.cn/…/tjgb/qxgb/`（长沙） | 一页列全地市下辖各县区，**最省事** |
| ② | 县统计局子站 | 县府站 `/xtjj/sjyfx/tjgb/`、`/bmxxgkml/xtjj/…/tjgb/`（长沙县） | 直发原题 |
| ③ | 县府门户统计栏 | 县府站 `/tjgb/`、`/sjkf/sjgb/`、`/governmentInfo/zfxxgk/tjgb`（德格） | 部分县与统计局栏目合并 |

### 免费 vs 付费

- **免费**：逐县公报正文（HTML，可抓）；县府/统计局栏目；少数县自印年鉴 ZIP（昆山）；中郡旧面板；县级财政决算 PDF。
- **付费/登录**：《中国县域统计年鉴》县市卷（县级社会经济主要指标 + 一般公共预算收入分组）与**乡镇卷**（全国前 1000 乡镇 + 各乡镇基本情况）—— 全国口径乡镇数据的唯一系统来源。
- 全国免费源（`data.stats.gov.cn.md`）只到**主要城市**，不含县级，别指望一个 API 出县级面板。

## 坑

1. **没有全国统一县级 API**：县域数据本质是「逐县政务公开」，抓取要按县遍历，路径千差万别；聚合库（红黑）虽省事但**非官方、逐年完整度不一**，正式引用须回各县统计公报/年鉴原文核对。
2. **中郡县域大数据不是面板**：只有零散年份（德清 GDP 停 2019、人口 2020），当线索用，别当连续面板。
3. **乡镇级数据公开度极低**：免费能拿到的只有《中国县域统计年鉴·乡镇卷》（付费）与少数县级年鉴附乡镇表；不要承诺免费全国乡镇面板。
4. 县级 GDP 有**初步核算 / 最终核实**两个口径，且行政区「全县 vs 县本级」不同，跨年跨源比较前先核口径（与 `city-stat-yearbook.md` 坑 5 同理）。
5. 知网镜像 `data.oversea.cnki.net` 本机 **404**（历史卡同结论），脚本里只写 `data.cnki.net`。
