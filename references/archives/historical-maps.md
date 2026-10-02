# historical-maps —— 历史地图与历史 GIS

- 去哪找：**CHGIS（哈佛）** 主站 `https://chgis.fas.harvard.edu/`、数据发布 `https://dataverse.harvard.edu/dataverse/chgis_v6`、旧镜像 `https://sites.fas.harvard.edu/~chgis/`；**CHGIS 复旦镜像**（复旦大学中国历史地理研究所）数据下载 `https://yugong.fudan.edu.cn/CHGIS/sjxz.htm`、时空地名辞典 `http://tgaz.fudan.edu.cn/tgaz/`；**中研院人社中心地理資訊科學研究專題中心** `https://gis.rchss.sinica.edu.tw/`、臺灣百年歷史地圖 `https://gissrv4.sinica.edu.tw/gis/twhgis/`、中華文明時空基礎架構 `https://ccts.sinica.edu.tw/`；**谭图数字化** 观沧海/地图书 `https://www.ageeye.cn/`（已并入 `https://www.ditushu.com/`，新版 `https://ageeye.app.ditushu.com/`）、GitHub `imbian/chinese_historical_map`（按朝代分目录）、OSGeo 中国中心史地目录 `https://osgeo.cn/mapage/`。
- 什么时候用：要**历代政区矢量**（省/府/县界线与治所、村镇、河流湖泊）做空间分析；要**历史地名 + 经纬度 + 年代**（时空地名辞典查询）；要**台湾百年老地图**叠加比对；要**谭其骧《中国历史地图集》**的扫描图或粗略矢量；关键词：CHGIS、谭图、历史地图、政区沿革、历史地名、时空基础架构、臺灣百年歷史地圖。
- 怎么搜：历史 GIS **多可直接 curl 取 JSON/附件**——
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # ① CHGIS 时空地名辞典（复旦）：n=名、yr=年、ftyp=类型、src=CHGIS/TBRC/HGR、fmt=json|html
  curl -s -A "$UA" 'http://tgaz.fudan.edu.cn/tgaz/placename?n=%E5%8C%97%E4%BA%AC&fmt=json'
  # ② CHGIS 数据包直下（复旦镜像，VSB 附件 .rar，列出见「细节」）
  curl -s -A "$UA" -I 'https://yugong.fudan.edu.cn/virtual_attach_file.vsb?afc=…&oid=2084931748&e=.rar'
  ```
  其余：**哈佛 CHGIS 主站**是静态 HTML（`/data/chgis/v1…v6/`），数据本体指向 Harvard Dataverse；**中研院臺灣百年歷史地圖**为 ASP.NET 浏览器查看器（`/gis/twhgis/`，分县视图 `/gis/<county>.aspx`），需浏览器；**中华文明时空基础架构**是 2000 年代旧 frameset 站，仅浏览器。
- 覆盖：CHGIS **公元前 222 – 1911**（V6 时间序列；另 1820/1911 时间切片），v1(2002)→v6(2016) 逐年迭代；台湾百年历史地图 1895 至今多期底图；谭图数字化覆盖先秦至清各朝代。
- 门槛：CHGIS **免费**（许可：**限学术研究**，禁商业使用/转售/再分发，引用需注出处）；复旦 tgaz / 附件无需登录；中研院查看器免费但需浏览器；Harvard Dataverse 本机被 Cloudflare 挑战（见「坑」）。
- 实测：2026-10-03，macOS（arm64），curl 8.x，桌面 UA：
  - `chgis.fas.harvard.edu/` → 200（5827 B，title CHGIS）；`/data/chgis/v6/` → 200，正文含「Version 6 (Published: Dec 2016)」「License: free for academic research, no commercial use, resale, or redistribution permitted」与 `Distribution URL: …/dataverse/chgis_v6`；
  - `sites.fas.harvard.edu/~chgis/` → **302** → `chgis.fairbank.fas.harvard.edu`；
  - `dataverse.harvard.edu/dataverse/chgis_v6` → **202**（无正文，Cloudflare 挑战）；
  - `yugong.fudan.edu.cn/CHGIS/sjxz.htm` → 200，含 ~28 个 `virtual_attach_file.vsb?…&e=.rar` 附件；抽 1 个 HEAD → 200，`Content-Type: application/x-rar-compressed`，`Content-Length: 698493`；
  - `tgaz.fudan.edu.cn/tgaz/placename?n=%E5%8C%97%E4%BA%AC&fmt=json` → 200 `text/json`，3456 B，`count of total results: 7`（首条 `hvd_111929 北京路`）；`…/placename/hvd_111929?fmt=json` → 200 详情；
  - `ccts.sinica.edu.tw` → 200（旧 frameset，title 中華文明之時空基礎架構）；`gis.rchss.sinica.edu.tw` → 200（WordPress）；
  - `gissrv4.sinica.edu.tw/gis/twhgis/` → 200（臺灣百年歷史地圖，含各县 `.aspx` 链接）；`/gis/twhgis.aspx`、`/gis/twhgis/wmts?...GetCapabilities`、`gis.sinica.edu.tw/twhgis/wmts?...` → 均为浏览器错误页 / **404**；
  - `www.loc.gov/maps/` → **403**（Cloudflare「Just a moment...」）；`gisportal.rchss.sinica.edu.tw` → **000**（连接失败）；`hgis.com.cn` → 200 但正文「数据库错误」；
  - `www.ageeye.cn` → 200（告示已并入地图书）；`www.ditushu.com`、`ageeye.app.ditushu.com` → 200；`api.github.com/repos/imbian/chinese_historical_map/contents/` → 200 JSON（按朝代目录：夏商/西周/春秋/战国/秦/西汉/东汉/三国…）；`osgeo.cn/mapage/` → 200；`osgeo.cn/list/gzgls` → 404（旧链失效）。
- 上游：CHGIS 主站 `https://chgis.fas.harvard.edu/`（站点源码 `github.com/vajlex/chgis-fas-website`）；复旦禹贡 `https://yugong.fudan.edu.cn/CHGIS/`；中研院 GIS 中心 `https://gis.rchss.sinica.edu.tw/`；观沧海/地图书 `https://www.ageeye.cn/`、`https://www.ditushu.com/`。

## 细节

### 一、CHGIS 数据下载（复旦镜像，VSB `.rar` 包）

入口 `https://yugong.fudan.edu.cn/CHGIS/sjxz.htm`，附件形如
`https://yugong.fudan.edu.cn/virtual_attach_file.vsb?afc=<长串>&oid=2084931748&e=.rar`（`oid` 固定，`afc` 每文件不同，**必须从页面解析，不能拼 URL**）。清单：

| 组 | 图层 |
|---|---|
| T-S 时间序列 | 政权界线 / 政权治所 / 省级界线 / 省级治所 / 府级界线 / 府级治所 / 县级治所 / 福建县级界线 |
| 1820 切片 | 省级界线 / 省级治所 / 府级界线 / 府级治所 / 县级治所 / 村镇 / 河流 / 湖泊河流 |
| 1911 切片 | 省级界线 / 省级治所 / 府级界线 / 府级治所 / 县级界线 / 县级治所 / 村镇 |
| 底图背景 | DEM 地形背景图像（1 分 / 2 分 / 30 秒）、太湖流域分层设色地形图 |

解析命令（只取链接、不下载本体）：
```bash
curl -s -A "$UA" 'https://yugong.fudan.edu.cn/CHGIS/sjxz.htm' \
 | grep -oE 'href="/virtual_attach_file\.vsb\?[^"]+"' | sed 's/href="//;s/"$//'
```
数据本体为 `.rar`（内多含 Shapefile / E00），许可见 `CHGIS/bqsm.htm`（版权声明）与哈佛 V6 页。

### 二、时空地名辞典 API（CHGIS Temporal Gazetteer，复旦）

`http://tgaz.fudan.edu.cn/tgaz/placename?<参数>`（GET），参数：`n`=地名（支持前缀，`北京` 命中 `北京路`）、`yr`=年份、`ftyp`=要素类型、`src`=数据源（`CHGIS` / `TBRC` Tibetan Buddhist Resource Center / `HGR` Historical Gazetteer of Russia，空=所有）、`fmt`=`json`|`html`（`html` 返回 Leaflet 地图页）。

```json
{"system":"CHGIS - Harvard University & Fudan University",
 "memo":"Results for query matching key '北京%'",
 "count of displayed results":"7","count of total results":"7",
 "placenames":[{"sys_id":"hvd_111929","uri":"…/tgaz/placename/hvd_111929",
                "name":"北京路","transcription":"Beijing Lu", …}]}
```
详情：`http://tgaz.fudan.edu.cn/tgaz/placename/<sys_id>?fmt=json`。哈佛旧入口 `https://sites.fas.harvard.edu/~chgis/search/`（现 302）。

### 三、中研院地图资源

| 平台 | 入口 | 形态 | 门槛 |
|---|---|---|---|
| 地理資訊科學研究專題中心 | `https://gis.rchss.sinica.edu.tw/` | WordPress（有 `/wp-json/`），平台/圖集/計畫页 | 免费 |
| 臺灣百年歷史地圖 | `https://gissrv4.sinica.edu.tw/gis/twhgis/` | ASP.NET 查看器，分县 `/gis/<county>.aspx` | 免费·需浏览器 |
| 中華文明時空基礎架構（CCTS） | `https://ccts.sinica.edu.tw/` | 2000 年代 frameset（intro/framework/searches…） | 免费·需浏览器 |

臺灣百年歷史地圖是**多期底图叠加**工具（1895 起各年代地形/都市计划/航道图等），非批量 API；本机 WMTS `GetCapabilities` 两处均 404，须走网页。

### 四、谭图（《中国历史地图集》）数字化

- **观沧海 / 地图书**：`https://www.ageeye.cn/` 2025-04 改版并入 `https://www.ditushu.com/`，新域 `https://ageeye.app.ditushu.com/`；志愿者协作、矢量可缩放，含《中国历史地图集》矢量数据。
- **GitHub `imbian/chinese_historical_map`**：按朝代目录（夏商/西周/春秋/战国/秦/西汉/东汉/三国/西晋/东晋/南北朝/隋/唐/五代十国/辽北宋/金南宋/元/明/清），`api.github.com/repos/…/contents/` 可直接列文件。
- 扫描版：国学导航 `http://www.guoxue123.com/other/map/zgmap/index.htm`、OSGeo 中国中心 `https://osgeo.cn/mapage/`（史地知识分类目录；旧 `/list/gzgls` 已 404）。
- 民国/晚清地图：**LoC 美国国会图书馆** `https://www.loc.gov/maps/` 本机被 Cloudflare 拦（403）；日本国立国会图书馆地图见 `../academic/ndl-japan.md`；标准地图/天地图底图见 `../stats/geodata.md`。

## 坑

1. **Harvard Dataverse 走 Cloudflare**：`dataverse.harvard.edu/dataverse/chgis_v6` 本机返回 **202**（挑战页、无正文）；拿 CHGIS 数据优先走**复旦镜像 `.rar`**（`yugong.fudan.edu.cn`，直连 200）。
2. **复旦附件 `afc` 是动态签名**，逐文件不同，`sjxz.htm` 页面解析后即用；`oid=2084931748` 为该页所有附件的固定归属 id，**不要自己构造**。
3. **`gisportal.rchss.sinica.edu.tw` 本机 000**（连接失败）；平台入口用 `gis.rchss.sinica.edu.tw`。
4. **臺灣百年歷史地圖是 ASP.NET + 浏览器检测**：直接请求 `.aspx` 会回「请用 Chrome/Firefox」错误页；`wmts?...GetCapabilities` 在 `gis.sinica.edu.tw/twhgis/wmts` 与 `gissrv4.sinica.edu.tw/gis/twhgis/wmts` 均 **404**，**无公开批量 WMTS**，只能网页目视。
5. **`ccts.sinica.edu.tw` 是旧 frameset 站**（charset utf-8、`<map>` 热区导航），内容以「中华文明时空基础架构」项目介绍为主，非数据集下载口。
6. **许可**：CHGIS 数据**限学术研究**，禁商业/转售/再分发；引用格式（国内）「中国历史地图集 / 中国历史地理信息系统（CHGIS）…」，正式引用见 `yugong.fudan.edu.cn/CHGIS/bqsm.htm` 与哈佛 V6 页。
7. **谭图/观沧海为志愿者或扫描成果**，界线精度与断代参差，**勿当权威政区数据**；正式研究以 CHGIS 为准并注明版本（v1–v6）。
8. **LoC maps 本机不可达**（403 Cloudflare）；需要美国国会图书馆藏民国/晚清地图时，走镜像或浏览器代理，勿在脚本里硬试。
