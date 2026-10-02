# insurance —— 保险业统计与公司披露入口

- 去哪找：
  - 中国保险行业协会（中保协）`https://www.iachina.cn/`——**信息披露**入口直跳 `https://icidp.iachina.cn/`（保险公司年度信息披露 / 偿付能力 / 交强险 / 关联交易 / 非保险子公司等，附 PDF 原件）；**协会要闻** `https://www.iachina.cn/col/col22/index.html`（交强险年度经营情况等数据发布）；**研究报告** `/col/col44/index.html`（《中国保险业社会责任报告》）；**行业指数** `/col/col43/index.html` → 中国保险汽车安全指数（CIASI）`/col/col241/index.html`、汽车零整比100指数 `/col/col295/index.html`。
  - 《中国保险年鉴》：CNKI「中国经济社会大数据研究平台」`https://data.cnki.net/`（年鉴库，需机构订阅）；第三方付费年鉴站 `https://www.tjnjdata.com/`（`yearbookchina.com` 301 跳此）。
  - 监管统计：金融监管总局 `nfra.gov.cn.md`（银行业保险业统计、保费/赔付/总资产）；央行口径 `pbc.gov.cn.md`。
  - 上市公司年报与公告：`../business/cninfo.com.cn.md`（中国人保/国寿/平安/太保/新华等 A+H 股）。
- 什么时候用：要保险公司**年度信息披露报告原件**（非上市险企唯一公开入口）、偿付能力报告、交强险年度经营数据、行业指数/榜单（车险安全、零整比）、保费收入与赔付行业统计、保险年鉴分章数据时。
- 怎么搜：两套完全不同的机制——中保协 CMS（栏目页 + 文章页 + 附件）与信息披露平台（`.do` 接口，**必须带两个自定义头**）。
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  CID='aB3dE5fG7hI9jK1lM2nO4pQ6rS8tU0vW'   # 任意自造串；站内 JS 用 localStorage 随机串
  # ① 中保协文章（静态）：栏目页 → 按年/日目录 → 文章
  curl -sSL -A "$UA" 'https://www.iachina.cn/art/2023/7/28/art_22_107056.html'
  # ② 披露平台：先取会话，再带两个头调接口
  curl -s   -A "$UA" -c /tmp/icidp.jar 'https://icidp.iachina.cn/' -o /dev/null
  curl -s   -A "$UA" -b /tmp/icidp.jar -X POST \
    -H "Accept-Encodings: $CID" -H "timestamp: $(date +%s)000" \
    -H 'Referer: https://icidp.iachina.cn/' -H 'X-Requested-With: XMLHttpRequest' \
    'https://icidp.iachina.cn/front/getFirstColumns.do' --data 'pageNo=1'          # 栏目树 JSON
  curl -s   -A "$UA" -b /tmp/icidp.jar -X POST \
    -H "Accept-Encodings: $CID" -H "timestamp: $(date +%s)000" \
    -H 'Referer: https://icidp.iachina.cn/' -H 'X-Requested-With: XMLHttpRequest' \
    'https://icidp.iachina.cn/front/getAllInfosByCid.do?columnid=201510010001'     # 年度披露列表 HTML
  ```
  结果形态：中保协栏目 = HTML 文章页（附件 PDF）；披露平台 = `.do` 返回 **JSON（栏目树）或 HTML/GBK（列表与详情）**；PDF 原件直链 `/files/piluxinxi/pdf/{uuid}.PDF`。
- 覆盖：披露平台 11 类栏目、覆盖全部保险公司与保险资管公司，条目滚动至最新（实测见 2025/2026 年披露报告）；交强险经营情况=年度发布（实测 2022 年度，2023-07-28 发布）；社会责任报告 2019–2024；行业指数自 2017 起；《中国保险年鉴》按年卷（CNKI 年鉴库）。
- 门槛：中保协站与披露平台**免费、免登录**；披露平台需自造 `Accept-Encodings` + `timestamp` 两个请求头（否则 404），无需账号。年鉴全文需 CNKI 机构订阅或第三方付费。
- 实测：2026-10-03，macOS arm64，桌面 UA、20 s 超时、同主机 ≥1.5 s 间隔：
  - `https://www.iachina.cn/` → `200/107,156 B`（title 中国保险行业协会）；`/col/col22/`、`/col/col44/`（`200/10,543`）、`/col/col43/`（`200/8,873`）、`/col/col6/`（`200/21,548`）均可取；col43 内仅两条：CIASI（`/col/col241/`）、汽车零整比100指数（`/col/col295/`）✅
  - `https://www.iachina.cn/art/2023/7/28/art_22_107056.html` → `200/21,466 B`，正文含「2022 年交强险承保机动车 3.37 亿辆、保费收入 2465 亿元、保障金额 67 万亿、赔付成本 1845 亿元、承保亏损 22 亿元」（http 入口 301 → https）✅
  - `https://icidp.iachina.cn/` → `200/28,084 B`（中保协信息披露系统）；`POST /front/getFirstColumns.do` → `200` JSON `totalRecords:63`（去重 11 个栏目）；`POST /front/getColumnsType.do` → `200` JSON `totalRecords:17`；`POST /front/getNotice.do` → `{"totalRecords":0,"data":[]}` ✅
  - `POST /front/getAllInfosByCid.do?columnid=201510010001` → `200`（GBK）列表，条目形如 `info('2026062617484563','01','201510010001')`；`POST /front/infoDetail.do?informationno=2026062617484563` → `200/5,732 B`（GBK）「安诚财产保险股份有限公司2025年度信息披露报告」+ PDF 附件 `8f0ccb92-e7c7-43df-a34e-c434b805297f.PDF`；直链 `GET /files/piluxinxi/pdf/8f0ccb92-e7c7-43df-a34e-c434b805297f.PDF` → `200`（魔数 `%PDF-1.7`）✅
  - `POST /front/generalSearch.do`（`keyword=交强险`）→ `200`（GBK）标题检索结果，命中列 `2015102216550911`（交强险信息披露）✅；**漏带任一头 → 404**（实测）
  - `https://data.cnki.net/` → `200/11,409 B`（SPA 壳，年鉴内容未本机取到）；`https://www.yearbookchina.com/navibooklist-n3025041211-1.html` → `301 → https://www.tjnjdata.com/Yearbook/zhongguo-baoxian-nianjian-2024.html` `200`（2024 年中国保险年鉴 PDF/Excel）⚠️
- 上游：`iachina.cn`（中国保险行业协会）；`icidp.iachina.cn`（中国保险行业信息披露系统）；`data.cnki.net`（CNKI 中国经济社会大数据研究平台）；`nfra.gov.cn`（国家金融监督管理总局）。

## 细节

### 一、信息披露平台（icidp.iachina.cn）栏目表

`POST /front/getFirstColumns.do`（`pageNo=1`）返回 63 行，去重后 11 类栏目（ID 为 `columnid`）：

| columnid | 栏目 |
|---|---|
| `201510010001` | 保险公司年度信息披露（各公司年度/季度报告 PDF） |
| `2015120115460095` | 偿付能力信息披露 |
| `2015102216550911` | 交强险信息披露 |
| `2015111318250002` | 财产险信息披露 |
| `2015111318230001` | 人身险信息披露 |
| `201509301401` | 互联网保险信息披露（非叶子，有子栏目） |
| `201510010002` | 资金运用关联交易信息披露 |
| `201510010003` | 资金运用风险责任人信息披露 |
| `201510010005` | 重大关联交易信息披露 |
| `201510010004` | 非保险子公司信息披露 |
| `2020102321300396` | 投资管理能力信息披露 |

### 二、披露平台端点

基址 `https://icidp.iachina.cn`，除 PDF 外均为 **POST**，返回多为 `text/html;charset=GBK`（JSON 端点除外）：

| 端点 | 参数 | 返回 |
|---|---|---|
| `/front/getFirstColumns.do` | `pageNo` | JSON 顶层栏目树 |
| `/front/getColumnsType.do` | `pageNo` | JSON 栏目类型（17 行） |
| `/front/getChildColumns.do` | `supColumnId` | JSON 子栏目 |
| `/front/getAllInfosByCid.do` | `?columnid={id}` | HTML(GBK) 条目列表 |
| `/front/infoDetail.do` | `?informationno={id}` | HTML(GBK) 详情 + `PDF附件列表` |
| `/front/generalSearch.do` | `keyword`（URL 编码） | HTML(GBK) 标题检索 |
| `/front/captchaCheck.do` | `clientIdCard` | JSON（`msg` 为 AES 加密的状态串） |
| `/files/piluxinxi/pdf/{uuid}.PDF` | GET | PDF 原件 |

- 详情页附件名是 **UUID.PDF**（如 `8f0ccb92-….PDF`），从 `onclick="down3('…PDF')"` 或 `id="…PDF"` 解析；查看器为 `/files/piluxinxi/pdf/viewer.html?file={uuid}.PDF`。
- 列表条目跳转统一为 `info('{informationno}','01','{columnid}')`；`informationno` 即详情接口入参。
- `captchaCheck.do` 返回加密串，AES-128-CBC、key=`0d36c68466e06b99`、iv=`0840e274812143f5`（ZeroPadding，密文 `_` 需换回 `+`），解出 `{clientIpStatus:"success",clientIp:…}`——**实测网络环境无需人机验证**，接口只要两个头即可。

### 三、中保协站点（iachina.cn）

- 栏目页 `/col/col{ID}/index.html`；文章页 `/art/{YYYY}/{M}/{D}/art_{栏目ID}_{文章ID}.html`。
- 已知栏目 ID：`col22` 协会要闻、`col23` 行业要闻、`col24` 公告通知、`col44` 研究报告、`col43` 行业指数、`col6` 实践研究、`col241` CIASI、`col295` 汽车零整比100指数。
- 「加载更多」走 `/module/web/jpage/morecolumndataproxy.jsp?page={n}&appid=1&webid=1&path=/&columnid={ID}&unitid=6412&keyWordCount=30`（自 col43 页面源码提取，**未实调**；返回 XML 包裹的 HTML 片段）。

### 四、口径区分

| 想要 | 去哪 |
|---|---|
| 单家公司年报/偿付能力/交强险（含非上市） | `icidp.iachina.cn` 对应栏目 PDF |
| 行业汇总保费/赔付/总资产 | `nfra.gov.cn.md`（监管统计）；行业指数看 `iachina.cn/col/col43/` |
| 上市险企财务/公告 | `../business/cninfo.com.cn.md` |
| 货币/社融口径 | `pbc.gov.cn.md` |
| 年鉴分章/历史沿革 | CNKI 年鉴库；纸本《中国保险年鉴》 |

## 坑

1. **披露平台必须带 `Accept-Encodings` + `timestamp` 两头**：漏任一个（或漏 `Referer`/`X-Requested-With`）本机一律 `404`；两个头值不需事先注册，自造串即可，故**不是账号门槛**。
2. **`.do` 列表/详情是 GBK**（`Content-Type` 有时写 UTF-8，实际为 GBK）——按 UTF-8 解码会满屏乱码，务必按 `<meta>`/实测编码（GBK）解。
3. **PDF 文件名是 UUID**，不可按公司名猜；必须先请求 `infoDetail.do` 再正则抓 `…PDF`。
4. **中保协 `http://` 301 → `https://`**；披露平台独立子域（`icidp.`），别拼到主站路径下。
5. **《中国保险年鉴》无独立官网**：CNKI 平台是 SPA、内容需机构订阅，本机只验证到首页；第三方站（tjnjdata.com 等）为**付费镜像**，引用时注明版本年份与来源。
6. **交强险等数据以「新闻稿」形式发布在协会要闻（col22）**，不是表格附件；要数字从正文抓，并记标题+发布日期。
7. 机构改制导致口径断裂：原保监会 → 银保监会（`cbirc.gov.cn`）→ 金融监管总局（`nfra.gov.cn`，2023 起），历史口径引用需注明年份。
