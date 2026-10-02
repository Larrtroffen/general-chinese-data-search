# nmpa.gov.cn —— 药品器械化妆品注册备案库

- 去哪找：**国家药监局数据查询平台** `https://datasearch.nmpa.gov.cn/datasearch/home-index.html`（药品/医疗器械/化妆品/其它四大类的注册、备案、企业、目录子库总入口）；**菜单与全部子库清单** `https://datasearch.nmpa.gov.cn/datasearch/config/NMPA_DATA.json`；**医疗器械唯一标识（UDI）数据库** `https://udi.nmpa.gov.cn/`；政务服务门户 `https://zwfw.nmpa.gov.cn/web/index`。旧入口 `https://www.nmpa.gov.cn/datasearch/home-index.html` 已改为迁移提示页（见坑 1）。
- 什么时候用：查**药品批准文号/注册证号**（境内生产药品、境外生产药品、境内/境外备案公示）；查**医疗器械注册证/备案号**（境内/进口，含历史数据）、器械生产/经营企业许可与备案；查**化妆品**（国产/进口特殊化妆品注册、普通化妆品备案、牙膏备案、新原料、生产企业、检验机构、已使用原料目录）；查药品生产企业/经营企业、GMP/GSP、全国药品抽检、中药保护品种、中药提取物与配方颗粒备案、非处方药目录、执业药师、**国家基本药物（2018 年版）**、疫苗说明书与标签、麻醉药品和精神药品品种目录、兴奋剂目录；查器械**UDI 产品标识**与产品明细。
- 怎么搜：
  - **数据查询平台（Vue SPA + 瑞数 WAF）——仅浏览器**：列表接口 `GET https://datasearch.nmpa.gov.cn/datasearch/data/nmpadata/search?itemId=<子库id>&isSenior=N&searchValue=<词>&pageNum=1&pageSize=10`，详情 `GET …/nmpadata/queryDetail?itemId=<子库id>&id=<记录id>`，计数 `GET …/nmpadata/countNums?itemIds=<逗号分隔子库id>&searchValue=<词>&isSenior=N`；返回 JSON，**须带 `timestamp` 与 `sign` 两个请求头**，签名为站内 `pajax.hasTokenGet` 按混淆算法生成（未公开）。`curl` 与非浏览器 `fetch` 一律被 WAF 拦成 **412**。人读路径：首页点分类 → `search-result.html` 检索，或深链 `search-result.html?nmpaType=NMPA_DATA&nmpaItem=<子库id>`；详情 `search-info.html?nmpa=<base64("id=<记录id>&itemId=<子库id>")>`。
  - **UDI 数据库（可 curl）**：检索页 `POST https://udi.nmpa.gov.cn/showListXXCX.html`（表单 `searchType=1&query=<词>`，返回 HTML）；列表 JSON `POST https://udi.nmpa.gov.cn/getDeviceList.html`（jqGrid 参数 `query=&searchType=1&page=1&rows=15&sidx=&sord=asc`）；详情 `GET https://udi.nmpa.gov.cn/showDetailCX.html?deviceRecordKey=<key>`；字段字典 `POST /deviceField.html`、统计 `POST /getLoginUdiStatistics.html`（均 JSON）。
  - 结果形态：**JSON**（两个站的数据接口）+ **HTML**（UDI 检索结果与详情）。
- 覆盖：药品——境内/境外生产药品与备案公示、生产/经营企业、抽检、GMP/GSP、中药保护品种、执业药师、非处方药中药/化学药品目录、基本药物（2018 版）、疫苗说明书与标签、麻精品种目录、兴奋剂目录；医疗器械——境内/进口的注册与备案（各含历史数据）、生产/经营企业许可与备案、一次性使用产品、网络交易第三方平台、UDI 产品标识（实测按"冠脉支架"命中 `records≈2410`）；化妆品——特殊/普通/牙膏、新原料、企业、检验检测机构、已使用原料目录。年代与更新频率以各子库页面披露为准（注册/备案类随审批实时增补）。
- 门槛：**免费、无需登录**（列表/详情请求头 `token: false`，匿名可查）；但 `datasearch` 数据查询平台前置**瑞数信息 WAF**（非浏览器请求 412），UDI 站无 WAF 可直接 `curl`。
- 实测：2026-10-03，macOS arm64，Chrome 150（无头受管 Chromium）+ curl 8.x 桌面 UA，20 s 超时，同主机 ≥1.5 s 间隔：
  - `curl -sL -o /dev/null -w '%{http_code}' 'https://www.nmpa.gov.cn/datasearch/home-index.html'` → **412**，落地 `https://datasearch.nmpa.gov.cn/datasearch/url_change.html`；浏览器渲染同址 → 标题「数据查询访问地址已变更」，正文给出新址 `https://datasearch.nmpa.gov.cn/datasearch/home-index.html`，4 s 后自动跳转 ✅
  - `dig +short app1.nmpa.gov.cn` → **空**（无 A 记录）；`curl 'https://app1.nmpa.gov.cn/'` → **000** ❌
  - 浏览器打开 `https://datasearch.nmpa.gov.cn/datasearch/home-index.html` → 标题「国家药品监督管理局数据查询」，菜单经 `…/config/NMPA_DATA.json` 加载（**4 大类、约 60 个条目**，见「细节」）✅
  - 页内调站内 `pajax.hasTokenGet(api.queryList,{itemId:'ff80808183cad75001840881f848179f',isSenior:'N',searchValue:'阿司匹林',pageNum:1,pageSize:3})` → `code:200,total:923`，行 `{f0:"国药准字H23022137",f1:"阿司匹林肠溶片",f2:"黑龙江鼎恒升药业有限公司",f3:"86903728000027",f4:"fe81e63e…"}`；实际请求头含 `timestamp`、`sign`、`token:false` ✅
  - 同页 `fetch('https://datasearch.nmpa.gov.cn/datasearch/data/nmpadata/search?…&timestamp='+Date.now())` → **412**（缺签名/被 WAF 拦）⚠️
  - 详情深链 `search-info.html?nmpa=<base64("id=fe81e63e1ebdfa69b88d4a274778159c&itemId=ff80808183cad75001840881f848179f")>` → 渲染「境内生产药品——"国药准字H23022137"基本信息」，接口 `…/queryDetail?itemId=…&id=…`（网络面板 200）✅
  - 化妆品子库 `queryList itemId=ff8080818046502f0180f934f6873f78, searchValue=面膜` → `code:200,total:6057`；器械 `itemId=ff80808183cad7500183cb66fe690285, searchValue=口罩` → `total:3952`；基本药物 `itemId=2c9ba384759c957701759cc91ecf029e, searchValue=阿司匹林` → `total:1`（`{f0:"化学药品和生物制品",f1:"…",f2:"…",f3:"阿司匹林",f4:"79"}`）✅
  - `curl -s -X POST 'https://udi.nmpa.gov.cn/getDeviceList.html' -d 'query=冠脉支架&searchType=1&page=1&rows=2&sidx=&sord=asc'` → **200** JSON `{"records":2410,"total":1205,"rows":[{"deviceRecordKey":"06970431710073…","primaryDeviceId":"06970431710073","agencyName":"GS1","companyName":"上海百心安生物技术股份有限公司","productName":"…","specification":"BX-3023",…}]}` ✅
  - `curl -s -X POST 'https://udi.nmpa.gov.cn/showListXXCX.html' -d 'searchType=1&query=冠脉支架'` → **200** HTML（同关键词 6267 条前置结果）✅
- 上游：国家药品监督管理局 `https://www.nmpa.gov.cn/`；数据查询平台 `https://datasearch.nmpa.gov.cn/datasearch/`；医疗器械唯一标识数据库 `https://udi.nmpa.gov.cn/`。

## 细节

### 一、子库清单（`config/NMPA_DATA.json`，2026-10-03 实测抓取）

菜单分 `item_2` 药品 / `item_3` 医疗器械 / `item_4` 化妆品 / `item_6` 其它；条目含 `itemId`、`itemName`、`itemType`（`table`=可搜索列表、`link`=外链承接页）、`must_searchKey`（是否必须给关键词）。常用 `table` 子库：

| 分类 | 子库 | itemId |
|---|---|---|
| 药品 | 境内生产药品（**国产药品批准文号**） | `ff80808183cad75001840881f848179f` |
| 药品 | 境外生产药品（**进口药品注册证**） | `ff80808183cad7500184088665711800` |
| 药品 | 境内生产药品备案信息公示 | `8a8898c18479eb93018479eca93c0027` |
| 药品 | 境外生产药品备案信息公示 | `8a8898c18479eb93018479ed63eb004e` |
| 药品 | 药品生产企业 | `ff8080818b64b242018b7fa29eb80adc` |
| 药品 | 药品经营企业 | `ff808081817f00dc01818e18c7c80bde` |
| 药品 | 全国药品抽检 | `ff80808184f1402f01854d23186c18a1` |
| 药品 | GMP 认证 / GSP 认证 | `ff80808183cad750018437402f152f3b` / `ff80808183cad75001843740a3de2f5c` |
| 药品 | 中药保护品种 | `ff8080818488c8e90184ade205cc0c65` |
| 药品 | 执业药师注册人员 | `ff80808181249a9c01816c3eb43f1aaa` |
| 药品 | 中药提取物备案公示 / 中药配方颗粒备案公示 | `8a8898c18479eb93018479ede2a4006f` / `ff8080817ca71240017cde691e530bb0` |
| 药品 | 非处方药中药目录 / 非处方药化学药品目录 | `ff808081845be229018464989dc90242` / `ff808081845be229018464992d1d0264` |
| 药品 | **国家基本药物（2018 年版）** | `2c9ba384759c957701759cc91ecf029e` |
| 药品 | 疫苗说明书和标签数据库 | `ff8080817ca71240017cc0495a3b03e4` |
| 药品 | 麻醉药品和精神药品品种目录 / 兴奋剂目录 | `8280808188d244650188d24eb1260020` / `ff8080819444b45601951721d5082ddd` |
| 器械 | 境内医疗器械（注册）/（注册历史数据） | `ff80808183cad7500183cb66fe690285` / `ff80808183cad7500183cb676ebf02b0` |
| 器械 | 境内医疗器械（备案）/（备案历史数据） | `ff80808183cad7500183cb68075c02d7` / `ff8080817ffceba8017ffe40f7150102` |
| 器械 | 进口医疗器械（注册）/（注册历史数据） | `ff808081830b103501838d4871b53543` / `ff808081830b103501838d4a5e32359f` |
| 器械 | 进口医疗器械（备案）/（备案历史数据） | `ff808081830b103501838d49d7ce3572` / `ff8080818488c8e90184a8fde91c0b8e` |
| 器械 | 生产企业（许可）/（备案） | `ff808081830b10350183ca27e2ac413e` / `ff808081830b10350183ca285e2c4160` |
| 器械 | 经营企业（许可）/（备案） | `ff8080818046502f0180df06de3234d8` / `ff8080818046502f0180df094b2a3506` |
| 器械 | 一次性使用医疗器械产品 / 网络交易服务第三方平台 | `ff808081876e56900187982b25c10d74` / `ff80808183cad75001841c2bd4c8248a` |
| 化妆品 | 国产特殊化妆品注册信息 | `ff8080818046502f0180f934f6873f78` |
| 化妆品 | 进口特殊化妆品注册信息 | `ff8080818046502f0180f9519c154181` |
| 化妆品 | 进口化妆品（《条例》实施以前批准） | `2c9ba384759c957701759cdc7efc0443` |
| 化妆品 | 化妆品新原料注册 / 备案信息 | `ff8080818046502f01804f40d0a90355` / `ff8080818046502f01804f41dbf103eb` |
| 化妆品 | 化妆品生产企业 / 检验检测机构 | `ff8080817dff44ef017e08e778be02a8` / `ff8080818281c68801828f92ad040505` |
| 化妆品 | 国产牙膏备案信息 | `ff8080818e63c900018e787bc48d0598` |
| 其它 | 可发布处方药广告的医学药学专业刊物名单 | `ff80808184f1402f01854d2ac5eb18f8` |

`link` 类（跳转承接页，非本站列表）：国产普通化妆品备案信息、进口普通化妆品（含牙膏）备案信息、已使用化妆品原料目录、医疗器械标准目录查询、医疗器械分类目录查询、体外诊断试剂分类目录查询、生物制品批签发产品公示汇总、药物和医疗器械临床试验机构备案管理信息系统（`beian.cfdi.org.cn`）、药品补充检验方法、新批准上市及通过一致性评价化学药品目录集、药包材标准、药品监管信息化标准（标准文档/术语/数据元/值域代码/数据集）。

### 二、数据查询平台接口（`https://datasearch.nmpa.gov.cn/datasearch/data/`，GET，返回 `{"code":"200","data":…}`）

| 端点 | 关键参数 | 含义 | 实测 |
|---|---|---|---|
| `nmpadata/search` | `itemId`、`isSenior=N`、`searchValue`、`pageNum`、`pageSize` | 子库列表（行按 `f0…` 给值） | ✅ 浏览器内 200 |
| `nmpadata/countNums` | `itemIds`（逗号分隔）、`searchValue`、`isSenior=N` | 各子库命中数（`[{itemId,name,nums}]`） | ✅ 浏览器内 200（仅回传有命中的子库） |
| `nmpadata/queryDetail` | `itemId`、`id`（=行的 `f4`/`NMPA_DK`） | 记录详情（部分库附 `captchaResult`） | ✅ 浏览器内 200 |
| `dict/getDictList` / `hotkey/getHotKey` | — | 字典 / 热搜词 | 取自 `api.js`，未单独实调 |
| `config/NMPA_DATA.json` | `?date=<ms>` | 全站菜单（子库清单） | ✅ 200 |
| `config/<itemId>.json` | — | 该子库表头定义 `listFeild`（`desc`=中文名、`alias`=返回字段名） | ✅ 200 |

- 标准/高级查询都是同一 `search` 端点：高级检索传 `isSenior=Y&searchParam=<JSON 字符串>`（普通检索传 `isSenior=N`）。
- 需 `timestamp`（毫秒）+ `sign`（由键值对拼接后 md5，算法在混淆的 `…/js/ajax.js` 的 `pajax.hasTokenGet` 内，**未公开**）；`token` 头匿名时为 `false`。
- 子库字段映射示例（境内生产药品 `config/ff80808183cad75001840881f848179f.json`）：`f0=批准文号`、`f1=产品名称`、`f2=生产单位`、`f3=药品本位码`、`f4=NMPA_DK`（详情主键）。

### 三、UDI 数据库（`https://udi.nmpa.gov.cn/`，无 WAF，可 curl）

| 端点 | 方法/参数 | 返回 |
|---|---|---|
| `/showListXXCX.html` | POST 表单 `searchType=1&query=<词>`（高级 `searchType=2` + 多字段） | HTML 结果页（jqGrid 壳） |
| `/getDeviceList.html` | POST `query=&searchType=1&page=&rows=&sidx=&sord=asc` | **jqGrid JSON** `{records,total,page,rows:[{deviceRecordKey,primaryDeviceId,agencyName,deviceCount,companyName,productName,specification,deviceEndDateStatus}]}` |
| `/showDetailCX.html` | GET `?deviceRecordKey=<key>` | 产品详情 HTML |
| `/deviceField.html`、`/getLoginUdiStatistics.html` | POST | 字段字典 / 首页统计 JSON |
| `/download.html`、`/showListInterr.html` | GET | 「数据共享」（查询/下载/接口对接/RSS）与对接申请页 |

`deviceRecordKey` 由列表行返回，直接拼详情页即可。

## 坑

1. **旧域已下线、旧路径已迁移**：`app1.nmpa.gov.cn`（旧「国产药品/进口药品/医疗器械」数据库入口）本机 `dig` 无 A 记录、`curl` 直接 000；`https://www.nmpa.gov.cn/datasearch/*` 已改为「数据查询访问地址已变更」提示页并跳 `datasearch.nmpa.gov.cn`。复刻旧脚本前先确认域名与路径。
2. **数据查询平台是瑞数信息 WAF 站（`*.yundunwaf5.com`）**：无头 `curl`、甚至**从已通过挑战的页面内直接 `fetch` 数据接口**都返回 412；只有站内 `pajax.hasTokenGet`（带正确 `sign`）能拿到 JSON。**判定为「仅浏览器」**；解析时须在浏览器上下文内借站内 ajax 方法或复刻签名。
3. **`sign` 无公开文档**：算法封装在压缩混淆的 `js/ajax.js`；直接对外复刻成本高，跨端批量取数建议走浏览器渲染 + 页面内 `pajax.hasTokenGet`，或评估 UDI 这类免 WAF 的替代入口。
4. `countNums` 只回传**有命中的子库**（本机一次请求 9 个子库仅回 3 个），**不能据此判定某子库为空**；且空 `searchValue` 对部分子库报 `code:500`「请检查参数是否为空！」，需给关键词。
5. **列表接口的列名是 `f0/f1…` 而非中文**：必须先取 `config/<itemId>.json` 的 `listFeild` 才能还原含义；行内 `f<N>`（`NMPA_DK`）才是详情主键。
6. 注册/备案类含**历史数据与变更记录**（如「注册历史数据」「备案历史数据」），且药品「批准文号」有新旧格式（如 `国药准字H23022137`），引用时记清批准日期与数据子库，避免新旧记录重复计数。
7. 本站与省级药监、UDI 上层应用（GS1/AHM/MA 码）可能给出不同粒度的产品标识，跨源比对须注明 `agencyName`（编码体系）。
