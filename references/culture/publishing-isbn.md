# publishing-isbn —— 图书书目核发与零售榜单入口

- 去哪找：**全国新书目 · 国家版本数据中心** `https://cnpub.com.cn/`（ISBN/CIP 查询，`/search.html` 快速查书）；**全国图书馆联合编目中心** `https://olcc.nlc.cn/`；**国家图书馆 OPAC** `http://opac.nlc.cn/F`；**开卷（北京开卷信息技术）** `https://www.openbook.com.cn/`；**中金易云** `https://www.centrin-ecloud.com/`；**当当图书榜** `https://bang.dangdang.com/`；**清博智能** `https://www.gsdata.cn/`（传播/舆情，非书目）。
- 什么时候用：要**某一 ISBN/CIP 的书目信息**（书名、作者、出版社、CIP 核准号）；要**新书出版快照**（按 CIP 核发日）；要**馆藏书目/索书号**（联合编目、OPAC）；要**图书零售市场**码洋、渠道结构、畅销榜（开卷/中金易云/当当）；核对出版社与版本。
- 怎么搜：能查的走接口，商业的给入口——
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
  # 全国新书目：CIP 核发数据（匿名），响应是 AES-128-CBC 密文（hex）
  K=$(printf '16weizifuchuan16' | xxd -p); IV=$(printf '1suibianshurude6' | xxd -p)
  curl -sL -A "$UA" 'https://cnpub.com.cn/api/index/hfList?pageNum=1&pageSize=20' \
    | tr -d '"' | xxd -r -p | openssl enc -d -aes-128-cbc -K "$K" -iv "$IV"
  # → {"code":200,"data":{"state":200,"list":[{cip_approveno,cip_firstbookname,ca_author,ca_publisher,cip_createdate,id},…]}}
  ```
  结果形态：全国新书目为 **JSON（AES 密文）**；开卷/中金易云为 **SPA + 订阅后台**；当当榜为 **HTML**；OPAC/联合编目为 **HTML 检索页**。
- 覆盖：全国新书目 CIP 数据按核发日滚动（实测最新一批 `cip_createdate` 到 2026-09-30）；ISBN 库自称 2009 年至今（上游声明）；联合编目为成员馆书目规范；开卷/中金易云覆盖全国图书零售监测（含实体店、平台电商、内容电商）；当当榜按分类/渠道动态。
- 门槛：全国新书目 **CIP 列表匿名**、**关键词检索需登录**（`searchVersionInfo`/`listQa` 返回 401）；开卷、中金易云 **付费订阅**（公开渠道只有新闻稿二手转述）；当当榜 **免费**；OPAC/联合编目 **免费**（编目中心正式数据/下载权限需成员资格）。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA、`-L`、20s）——`GET https://cnpub.com.cn/api/index/hfList` → 200，AES 密文解密得 `{"code":200,…,"list":[{"cip_approveno":"2026KE1718","cip_firstbookname":"城市建设者金融知识手册","ca_publisher":"中国金融出版社","cip_createdate":"2026-09-30",…}]}`（单页约 100 条）；`searchVersionInfo?keyword=…` 解密后 `{"code":401,"msg":"登录状态已过期"}`；`GET https://olcc.nlc.cn/index.html` → 200（22,051 B）；`GET http://opac.nlc.cn/F` → 200（37,383 B，**https 000**）；`GET https://www.openbook.com.cn/` → 200（416 B SPA 外壳）；`GET https://www.centrin-ecloud.com/` → 200；`GET https://www.gsdata.cn/` → 200；`GET https://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-recent7-0-0-1-1` → 200（113 KB）。❌ 本机不可达（20s 超时）：`isbncn.cn`（http/https 均 000）、`capub.cn`（中国版本图书馆）。
- 上游：`https://cnpub.com.cn/`（中国国家版本馆/国家版本数据中心）；`https://olcc.nlc.cn/`（国家图书馆）；`https://www.openbook.com.cn/`；`https://www.centrin-ecloud.com/`。

## 细节

### 一、源与可用性（2026-10-03 实测）

| 源 | 入口 | 状态 | 说明 |
|---|---|---|---|
| 全国新书目（国家版本数据中心） | `https://cnpub.com.cn/`、`/search.html` | ✅ API 可解 | CIP 核发列表匿名；检索需登录 |
| 全国图书馆联合编目中心 | `https://olcc.nlc.cn/` | ✅ 200 | 编目业务/规范/资格；**非公开书目检索** |
| 国家图书馆 OPAC | `http://opac.nlc.cn/F` | ⚠️ 仅 http | 中文图书馆藏书目；https 不通 |
| 开卷 | `https://www.openbook.com.cn/` | ⚠️ SPA | 图书零售码洋/渠道监测，订阅制 |
| 中金易云 | `https://www.centrin-ecloud.com/` | ⚠️ SPA | 出版发行数据服务，订阅制 |
| 当当图书榜 | `https://bang.dangdang.com/` | ✅ 200 | 分类/渠道榜 HTML |
| 清博智能 | `https://www.gsdata.cn/` | ✅ 200 | 传播力/舆情数据（非图书书目） |
| 中国ISBN中心（isbncn.cn） | `https://isbncn.cn/` | ❌ 本机超时 | 上游声明：国家新闻出版署主管、中国版本馆主办，ISBN 2009– 至今 |

### 二、全国新书目接口

- 加密：AES-128-CBC / Pkcs7，密文为 hex；key `16weizifuchuan16`、iv `1suibianshurude6`（取自前端 `chunk-common`）。
- `GET /api/index/hfList` —— CIP 核发列表（匿名），字段 `cip_approveno`（核准号，如 `2026KE1718`）、`cip_firstbookname`（书名）、`ca_author[]`、`ca_publisher`、`cip_createdate`、`id`。
- `GET /api/index/searchVersionInfo?keyword=&pageNum=&pageSize=`、`/api/index/listQa` —— 需登录（401）。
- `GET /api/index/info` —— 页面配置（匿名，返回 shopping/新闻等）。

## 坑

1. **响应是 AES 密文不是明文 JSON**：直接 `head` 只看到一长串十六进制；必须按上面的 key/iv 解。
2. `hfList` 的 `pageNum`/`pageSize` **实测未生效**（`pageSize=1` 仍返回整批约 100 条），当「最新一批」用，别当分页检索。
3. **开卷、中金易云的码洋/市占率要订阅**；公开渠道（中国出版协会 `pac.org.cn`、行业媒体）只有新闻稿里的零散引用，引用时写明「据开卷/中金易云，转载于…」。
4. `isbncn.cn`、`capub.cn` 本机**连接超时**，不代表站点下线；换网络/浏览器重试。
5. 国家图书馆 OPAC **只走 http**（`https://opac.nlc.cn/` → 000）。
6. 联合编目中心 `olcc.nlc.cn` 是**编目业务与规范**站，不提供面向公众的书目查询；要馆藏书目去 OPAC 或各省馆书目。
7. 当当榜页 URL/标题随分类与周期变化，抓取按当页 HTML 解析，别写死榜单条目。
8. 出版**统计**口径（种数、印数、发行）见 [`market-stats.md`](market-stats.md) 的国家新闻出版署统计信息（PDF 公报），本卡只管**书目与零售**。
