# bri-data —— 一带一路数据与项目库

- 去哪找：**中国一带一路网（官方）** `https://www.yidaiyilu.gov.cn/`，数据频道 `https://www.yidaiyilu.gov.cn/dataChart`；**CSIS Reconnecting Asia** `https://reconasia.csis.org/`（项目库 `/reconnecting-asia-map/`）；**Lowy Institute 太平洋援助地图** `https://pacificaidmap.lowyinstitute.org/data/`（中国视角 `/map/?donors=china`）。
- 什么时候用：要一带一路**官方口径**的国别宏观/外贸/投资、中欧班列与"海上丝路"贸易指数、政策与项目清单；要第三方**项目级**基建/能源项目库（Reconnecting Asia）；要中国对太平洋岛国援助的项目级数据（Pacific Aid Map）。
- 怎么搜：**官网是 SSR 静态站，栏目页与文章页可直接 curl**（数据频道的图表数值内嵌在 HTML 里）；第三方两家本机不通，只能给上游入口与替代镜：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # ① 官方数据频道 + 专题
  curl -sL -A "$UA" 'https://www.yidaiyilu.gov.cn/dataChart'                 # 各国数据/贸易指数/航贸指数
  curl -sL -A "$UA" 'https://www.yidaiyilu.gov.cn/dataChart?to=AIR'          # "一带一路"航贸指数
  curl -sL -A "$UA" 'https://www.yidaiyilu.gov.cn/zoblPc.htm'                # 中欧班列
  curl -sL -A "$UA" 'https://www.yidaiyilu.gov.cn/list/w/xiangmu'            # 栏目列表（项目/园区/政策…）
  curl -sL -A "$UA" 'https://www.yidaiyilu.gov.cn/p/<id>.html'               # 正文（含公报转载）
  # ② Reconnecting Asia / Pacific Aid Map：本机超时，走浏览器或经 SPC 镜像
  #   https://reconasia.csis.org/reconnecting-asia-map/     （上游声明，未本机实测）
  #   https://sdd.spc.int/dataset/df_pam                    （SPC 版 Pacific Aid Map）
  ```
  结果形态：官网为 **HTML**（文章表格/内嵌图表 JSON），无对外 XHR 检索接口；第三方为 **JS 地图应用**（需浏览器交互，导 CSV/Excel）。
- 覆盖：官网覆盖政策/项目/国别/指数（中欧班列、丝路海运、贸易指数、各国宏观与外贸投资数据）；Reconnecting Asia 覆盖 6 大洲基础设施/能源项目（约上万条，2017 起）；Pacific Aid Map 覆盖太平洋岛国援助/发展融资（1970s–今，含中国贷款）。
- 门槛：**免费、无需登录**；官网对 curl 友好；Reconnecting Asia / Lowy 需浏览器（且本机网络不可达）。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA、`-L`、20s）——`www.yidaiyilu.gov.cn/` `200`/807,347 B（`<title>中国一带一路网_推进"一带一路"建设官方网站`）；`/dataChart` `200`/678,602 B（title 数据_一带一路大数据汇总，含 17 段图表数据数组）；`/zoblPc.htm` `200`/59,356 B（中欧班列）；`/list/w/dsjjdydyl` `200`/668,181 B；`/p/0IEI15KS.html` `200`（商务部对外投资统计公报转载）；`eng.yidaiyilu.gov.cn` `200`/723,390 B。❌ 本机不通：`reconasia.csis.org`（及 `reconnectingasia.csis.org`、`csis.org`、`chinapower.csis.org`）、`pacificaidmap.lowyinstitute.org`、`www.lowyinstitute.org`、`pacificdata.org` 均连接超时；`stats.pacificdata.org` → `403 Cloudflare`；`sdg.casearth.cn`（站内链接的 SDGs 大数据平台）超时。✅ 替代：`sdd.spc.int/dataset/df_pam` `200`/180,605 B（SPC 版 Pacific Aid Map，数据指向 PDH.stat `SPC:DF_PAM(1.0)`）。
- 上游：中国一带一路网（推进"一带一路"建设工作领导小组办公室指导）`https://www.yidaiyilu.gov.cn/`；CSIS Reconnecting Asia `https://reconasia.csis.org/`；Lowy Institute Pacific Aid Map `https://www.lowyinstitute.org/pacific-aid-map`。

## 细节

### 官网栏目路径（可拼 URL）

| 入口 | URL | 说明 |
|---|---|---|
| 首页/资讯 | `https://www.yidaiyilu.gov.cn/` | SSR；多语种子站 `eng/ara/esp/fra/rus.yidaiyilu.gov.cn` |
| 数据频道 | `/dataChart`（`?to=AIR` 航贸指数） | 各国数据、海上丝路贸易指数、"一带一路"航贸指数 |
| 中欧班列 | `/zoblPc.htm` | 专题页；正文资源在 `yidaiyilu.gov.cn/z/221226/index/` 与 `imsilkroad.com` |
| 丝路海运·福建 | `/fjzt.htm` | 省级专题 |
| 栏目列表 | `/list/w/{栏目码}` | 如 `xiangmu`（项目）、`hwyq`（海外园区）、`zcgh`（政策规划）、`dsjjdydyl`（图说） |
| 文章正文 | `/p/{短ID}.html` | 公报/政策/统计转载，可直接 curl |
| 站内检索 | — | 未见独立检索 API；`/search?keyword=` 返回首页，建议逐栏目或用 `site:yidaiyilu.gov.cn` |

### 第三方数据入口（上游声明）

| 源 | 数据页 | 形态 |
|---|---|---|
| CSIS Reconnecting Asia | `reconasia.csis.org/reconnecting-asia-map/`、`/category/maps-data/` | 交互地图 + 项目表，可导出（需浏览器） |
| Lowy Pacific Aid Map | `pacificaidmap.lowyinstitute.org/data/`、`/map/?donors=china` | 交互地图/表格 + 下载（需浏览器） |
| Lowy 数据镜像（SPC） | `sdd.spc.int/dataset/df_pam` → PDH.stat `SPC:DF_PAM(1.0)` | SPC 统计平台，CC 授权再发布 |

## 坑

1. **本机网络**：`csis.org`、`lowyinstitute.org`、`pacificdata.org` 全超时，`stats.pacificdata.org` 被 Cloudflare 403——第三方库在本机只能"记入口 + 浏览器取"，别据此判定无数据。
2. **官网不是数据库**：`/dataChart` 的图表数值内嵌在 HTML（无 JSON API），要批量取数得解析页面或直接抄官方指数发布稿；检索功能以 Nuxt 前端为主，**没有可脚本化的站内搜索**。
3. **命名易混**：官方站数据频道里的 "SDGs 大数据共享平台"（`sdg.casearth.cn`，中科院）与本站不同源且本机不通；"丝路海运"入口 `/fjzt.htm` 实为**福建**专题页。
4. **指数口径**：海上丝路贸易指数、航贸指数由**第三方机构编制**（宁波航交所/浙大等），官网友情转载，引用请回原始编制方。
5. 第三方项目库（Reconnecting Asia / Pacific Aid Map）是**独立汇编**，与中国官方统计不可互加；量级/覆盖年份以各库 readme 为准。
