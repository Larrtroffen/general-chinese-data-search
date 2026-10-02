# talent-programs —— 国家级人才计划名单

- 去哪找：
  - **国家杰青 / 优青**（国家自然科学基金）：各科学部「申请与资助」栏的逐年资助清单（HTML 表）——生命科学部入口 `https://www.nsfc.gov.cn/p1/2853/3102/sqyzz1.html`；NSFC 项目查询入口 `https://www.nsfc.gov.cn/p1/2961/2962/3648/cx.html` → 大数据知识管理服务门户 `https://kd.nsfc.cn/`、资助项目查询 `https://grants.nsfc.gov.cn`。
  - **长江学者奖励计划**（教育部）：人事司「人才与专家工作」栏 `https://www.moe.gov.cn/srcsite/A04/s8132/`；站内检索 `https://so.moe.gov.cn/s?qt=长江学者`。
  - **国家高层次人才特殊支持计划（万人计划，中组部）**：无公开总名单，靠部委/单位公示与新闻转载（见 `## 细节` §4）。
  - **享受政府特殊津贴人员**（人社部）：部内要闻的名单新闻 + 省级人社厅「拟推荐人选公示」（湖南 `rst.hunan.gov.cn`、云南 `hrss.yn.gov.cn`、青岛 `hrss.qingdao.gov.cn` 等）。
  - **博士后**：中国博士后网 `https://www.chinapostdoctor.org.cn/website/index.html`（通知公告 + 中国博士后科学基金资助名单 PDF）。
- 什么时候用：核某人是否**杰青/优青**获资助者及其依托单位、项目编号；查**长江学者**、**万人计划**、**享受政府特殊津贴**入选者；查**中国博士后科学基金**（面上/特别资助）获资助名单；做人才履历核查、团队/单位人才统计。
- 怎么搜：一句话——**杰青/优青**走 NSFC 各科学部「申请与资助」清单页（逐年 HTML 表，表头=序号/科学部编号/研究方向/负责人/依托单位/所属学科）或 `kd.nsfc.cn` 成果检索 API；**长江学者**走教育部站内检索 + 高校人事处转载（教育部旧公示页多已下线）；**特贴**按「省/市 + 年份 + 政府特殊津贴 + 公示」在省级人社厅找 HTML/PDF；**博士后**在中国博士后网 `/website/` 下按栏目取名单 PDF。逐源操作见 `## 细节`。
- 覆盖：杰青/优青=各科学部逐年资助清单（NSFC 官网「申请与资助」栏现存 2018–2019 等批次，文章 ID 落在 `72645–72663` 段、分页至 `sqyzz1_4.html`）；基金大数据门户含历年项目/成果/人员（授权范围内）；长江学者=1998 年起计划，公示页现存零散；万人计划=第 1–4 批通知（2012 起，多为转载）；特贴=国务院批准的年度名单（人社部新闻稿 + 省级公示）；博士后基金=第 1–79 批面上资助、第 1–18 批特别资助等名单 PDF。粒度=姓名 + 单位 + （部分）项目/专业。
- 门槛：**全部免费、免登录**为主。例外：`grants.nsfc.gov.cn` 需**依托单位管理员账号**；`kd.nsfc.cn` 的**资助项目查询需验证码**（成果检索匿名可查、响应为 DES 密文）；中国博士后网**首页 500**（须走 `/website/` 深链）；人社部主域为 JS 挑战（用 IP 镜像）。
- 实测：2026-10-03，macOS 27（arm64），curl 8.x（desktop Chrome UA、`-L`、20 s 超时、同主机 ≥1.5 s）。`nsfc.gov.cn` 首页 200 / 111 487 B；`…/sqyzz1.html` 200 / 20 781 B；`…/72657.html`（2018 生命科学部杰青清单）200 / 19 800 B；`…/72649.html`（2019 优青清单）200 / 55 341 B。`kd.nsfc.cn/api/baseQuery/search` POST 200 / 5 068 B 密文，DES-ECB 解密成功。`moe.gov.cn/srcsite/A04/s8132/` 200 / 11 089 B（空壳）；2017 长江学者公示旧页 **404**。`www.chinapostdoctor.org.cn/` **500**，`/website/index.html` **200** / 24 290 B，名单 PDF **206** `application/pdf`。人社部 IP 镜像首页 200 / 165 932 B；`zyjsrygls/` 200 / 27 544 B。湖南特贴公示 PDF 200 / 147 951 B。逐条见 `## 细节`。
- 上游：国家自然科学基金委员会 <https://www.nsfc.gov.cn/>；教育部 <https://www.moe.gov.cn/>；人力资源社会保障部 <https://www.mohrss.gov.cn/>；中国博士后网（人社部专家中心 / 中国博士后科学基金会）<https://www.chinapostdoctor.org.cn/>。

## 细节

> 探测纪律（本机实测）：≤3 请求/主机·轮、间隔 ≥1.5 s、20 s 超时、桌面 Chrome UA。`✅`=本机 200/206；`⚠️`=有但需浏览器/验证码/会话；`❌`=不可达/已下线。

### 1. NSFC 杰青 / 优青（国家自然科学基金）

| 入口 | URL | 形态 | 实测 |
|---|---|---|---|
| 生命科学部·申请与资助 列表 | `https://www.nsfc.gov.cn/p1/2853/3102/sqyzz1.html` | 静态 HTML 列表（分页 `sqyzz1_2.html`…） | ✅ 200 / 20 781 B |
| 2018 杰青资助清单（生命科学部） | `https://www.nsfc.gov.cn/p1/2853/3102/72657.html` | HTML 表：序号·科学部编号·研究方向·**申请人**·**依托单位**·所属学科 | ✅ 200 / 19 800 B |
| 2019 优青资助清单（生命科学部） | `https://www.nsfc.gov.cn/p1/2853/3102/72649.html` | 同上 | ✅ 200 / 55 341 B |
| 项目查询说明 | `https://www.nsfc.gov.cn/p1/2961/2962/3648/cx.html` | 静态页 | ✅ 200 / 13 148 B（指向 `grants.nsfc.gov.cn` 与 `kd.nsfc.cn`） |
| 栏目 index | `…/p1/2853/3102/index.html` | — | ❌ 404（栏目首页名是 `sqyzz1.html`，不是 `index.html`） |

- 科学部栏目路径规律：`/p1/2853/<子栏>/<页>.html`；生命科学部子栏 = `smkxb1.html`（本部）、`3101/tzgg1111.html`（通知公告）、`3102/sqyzz1.html`（申请与资助）、`3103/zzcg1111.html`（资助成果）。**其余科学部**同构但数字 ID 不同，从首页 `https://www.nsfc.gov.cn/` → 科学部导航进入后取链接。
- 清单文章 ID 连续：2018/2019 批次落在 `72645`–`72663`，可小范围枚举（`…/p1/2853/3102/72645.html`…）。
- 上游同时以**通告/新闻**形式发布「建议资助项目申请人名单」，但官网 `nsfc.gov.cn` 现多已下线或改版，历史公示常在 CERNET、EOL、科学网转载中留存。
- ⚠️ **注意口径**：这里是**资助清单**（正式资助名单），与「建议资助项目申请人名单公示」（评审后公示）时序不同；引用须记标题、年份、科学部与 URL。

### 2. 科学基金大数据知识管理服务门户（kd.nsfc.cn）—— JSON API

- 站点是 Vue SPA（`https://kd.nsfc.cn/` ✅ 200 / 1 087 B），脚本 `/js/app.fdf53da0.js`（✅ 200 / 68 473 B）里有全部端点；接口基址 `https://kd.nsfc.cn/api`。
- **响应体为密文**：`DES/ECB/PKCS7`，密钥 `IFROMC86`（ASCII），Base64 编解码（源码：`p.a.DES.decrypt({ciphertext:…Base64.parse(e)}, Utf8.parse("IFROMC86"), {mode:ECB,padding:Pkcs7})`）。
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # ① 成果（论文/专利/著作）检索：匿名可用，响应为 DES 密文
  curl -s -A "$UA" -H 'Content-Type: application/json' -H 'Referer: https://kd.nsfc.cn/' \
    -X POST 'https://kd.nsfc.cn/api/baseQuery/search' \
    -d '{"keyword":"杰出青年","pageNum":1,"pageSize":5}' -o r.enc
  # ② 解密（key = ASCII "IFROMC86" → hex 4946524f4d433836）
  openssl enc -d -des-ecb -K 4946524f4d433836 -nopad -a -A -in r.enc
  # → {"code":200,"message":"Success","data":{"all_achievement":[{"zhTitle":"…","authors":"李宗金; 向荣; …",…}]}}
  ```
- 端点（取自 `app.js` 路由表）：`/baseQuery/search`、`/baseQuery/searchScreening`、`/baseQuery/searchDetails`、`/baseQuery/supportQueryResultsData`、`/baseQuery/completionQueryResultsData`、`/advancedQuery/personQueryResultsData`、`/advancedQuery/supportQueryPersonResultsData`、`/advancedQuery/orgQueryResultsData`、`/captcha/get`、`/captcha/check`、`/common/kdstatistic`。
- 实测：`POST /api/baseQuery/search` → 200 密文（解密得成果列表 ✅）；`POST /api/baseQuery/supportQueryResultsData {"pageNum":1,"pageSize":5}` → 200 `{"code":500,"message":"验证码错误"}` ⚠️（**资助项目查询带验证码门**，须先过 `/captcha/get`）；`POST /api/baseQuery/personQueryResultsData` → 404（人员类在 `/advancedQuery/…`）。
- 方法名对应 HTTP：`S/N` 系用于 GET/POST 的封装，`/baseQuery/homepageHotWord` 用 GET → 405（即该端点须 POST，勿用 GET）。

### 3. 长江学者奖励计划（教育部）

- 现行政策/推荐通知栏：`https://www.moe.gov.cn/srcsite/A04/s8132/`（✅ 200 / 11 089 B，但**栏目根是「信息提示」空壳，无文章列表**）。
- 文章 URL 规律：`https://www.moe.gov.cn/srcsite/A04/s8132/{YYYYMM}/t{YYYYMMDD}_{id}.html`（例：《"长江学者奖励计划"管理办法》`…/201809/t20180921_349638.html`）。
- **旧公示页已下线**：2017 年度建议人选公示 `http://www.moe.gov.cn/srcsite/A04/s7051/201801/t20180105_323866.html` → **404**（现仅 `web.archive.org` 有快照）；`/srcsite/A04/s7051/` 同为空壳。
- 可用的检索通道：`https://so.moe.gov.cn/s?qt=长江学者` → ✅ 200 / 183 275 B，但**结果由 JS 渲染**（HTML 里只有 `相关结果";` 模板）；`http://www.moe.gov.cn/was5/web/search?channelid=239993&searchword=…` → 200 模板壳（`共"+recordCount+"条`），**取不到列表**。
- 实务结论：长江学者**现势全名单无公开结构性库**——靠 ①教育部发函（不公开全名单，逐校通知）；②**高校人事处/新闻网**转载（`site:*.edu.cn 长江学者 建议人选 公示`）；③`../academic/` 与 `engines/` 的搜狗微信/`web_search site:`。
- 第三方整理：维基百科「长江学者特聘教授列表」（⚠️ 民间汇编，须回源核验）。

### 4. 万人计划 / 国家高层次人才特殊支持计划（中组部）

- 无全国统一查询库。第 1–4 批名单以**中组部办公厅通知**（《关于印发第 N 批国家"万人计划"入选人员名单的通知》）形式下发，公开渠道多为**转载**（如浙江省人才发展研究院 `zjrcfz.com`、微信公众号）与**部委/单位公示**。
- 可检索的公示样本：应急管理部 `https://www.mem.gov.cn/gk/rsxx/`、教育部教学名师遴选 `https://www.moe.gov.cn/srcsite/A10/s7011/`（✅ 域内 200，按「万人计划 + 年份」检索文章）。
- 检索式：`web_search`「万人计划 第N批 入选名单」、「国家高层次人才特殊支持计划 公示 site:gov.cn」；微信侧见 `engines/`（搜狗微信）。

### 5. 享受政府特殊津贴人员

- **人社部侧**：名单多以**部内要闻**新闻稿发布（如《2018年享受国务院特贴人员名单来了》`www.mohrss.gov.cn/SYrlzyhshbzb/dongtaixinwen/buneiyaowen/…`）；主域为 JS 挑战，走 IP 镜像 `http://114.255.111.180/`（✅ 200 / 165 932 B，栏目 `/zyjsrygls/` 专业技术人员管理司 ✅ 200 / 27 544 B；文章 `…/<col>/{YYYYMM}/t{YYYYMMDD}_{id}.html`）。
- **省级侧（更全、更规整）**：各省人社厅「拟推荐/拟入选享受政府特殊津贴人员公示」多为 HTML 或 PDF。实测湖南 `http://rst.hunan.gov.cn/rst/xxgk/tzgg/202506/33719505/files/5475c9de5f2f4d08abefc693b37c797d.pdf` → ✅ 200 / 147 951 B `application/pdf`（`%PDF-1.7`）。
- 检索式：「{省/市} {年份} 享受政府特殊津贴 公示/拟推荐人选」→ 落省级人社厅 `tzgg`/`gsgg` 栏。
- 国家级名单分**国务院特贴**（人社部组织）与**省/市政府特贴**（省市自评），两者别混；记录须注明是哪一级。

### 6. 博士后（中国博士后网 / 中国博士后科学基金会）

| 入口 | URL | 实测 |
|---|---|---|
| 首页（正确路径） | `https://www.chinapostdoctor.org.cn/website/index.html` | ✅ 200 / 24 290 B，title「人社部专家中心(中国博士后科学基金会)」 |
| 站点根 | `https://www.chinapostdoctor.org.cn/`、`/index.html`（302→https） | ❌ **500**（nginx，579 B）——勿以首页可达性判断站点死活 |
| 通知公告 | `https://www.chinapostdoctor.org.cn/website/infolist_xwdt.html?categoryid=<uuid>` | ✅ 200 / 13 820 B（`categoryid=ca7906f8-ec92-46d8-8a3c-a2caa26fde06` 为「通知公告」） |
| 基金名单 PDF | `https://www.chinapostdoctor.org.cn/prod-api/profile/info/fujian/{YYYYMMDD}/{uuid}.pdf` | ✅ 206 / `application/pdf`（`-r 0-80` 得到 `%PDF-1.7`）；旧式路径 `/website/userfiles/info/fujian/{YYYYMMDD}/{uuid}.pdf` |
| 博士后科学基金分站 | `https://jj.chinapostdoctor.org.cn/` | ❌ 500 |

- 名单标题示例（检索所得，PDF 直链已实测 206）：《中国博士后科学基金第79批面上资助获资助人员名单》《第18批特别资助获资助人员名单》。检索式：「中国博士后科学基金 第N批 面上资助/特别资助 获资助人员名单」。
- `prod-api` 为前后端分离附件服务，PDF 直链是 UUID 形式，**不能拼**——须先取列表页里的 href。

## 坑

1. **NSFC 栏目根不是 `index.html`**：科学部各子栏首页名各异（`sqyzz1.html`、`smkxb1.html`、`tzgg1111.html` 等），猜 `index.html` 一律 404；从首页导航或文章面包屑取真名。
2. **杰青/优青 ≠ 一个集中名单**：官方按**科学部**分别发布资助清单，全委级公示另发通告；别只查生命科学部就宣称「全量」。
3. **`kd.nsfc.cn` 全接口密文**：不解密会误判为「乱码/加密无解」；`DES-ECB` 密钥固定 `IFROMC86`，`openssl enc -d -des-ecb -K 4946524f4d433836 -nopad` 即可；`supportQueryResultsData`（资助项目查询）**要验证码**，成果检索才匿名。
4. **教育部旧公示页大量 404**：`moe.gov.cn/srcsite/A04/s7051/…`（长江学者公示）与 `/A04/s8132/` 栏目根现为「信息提示」空壳；`so.moe.gov.cn` 检索结果 JS 渲染，命令行取不到列表 → 转高校人事处转载 / `web.archive.org`。
5. **中国博士后网「假死」**：`/` 与 `/index.html` 均 500，但 `/website/*` 与 `prod-api/*` 正常——务必走深链，别因首页 500 判定源不可用。
6. **人社部主域 JS 挑战**：`www.mohrss.gov.cn` 返回 ~988 B 空壳（`EO_Bot_Ssid`），用 IP 镜像 `114.255.111.180`；镜像**非全量**（旧文章可能 404），找不到时回主域用浏览器。
7. **同名不同级**：政府特殊津贴分国务院 / 省 / 市三级；「长江学者」分特聘教授 / 讲座教授 / 青年学者；「万人计划」含杰出人才 / 领军人才 / 青年拔尖，统计与引用务必写清类别。

## 相关

- 院士、国家荣誉/道德模范/中国好人、革命英烈：`../archives/person-databases.md`（**不重复**，本卡只管计划性人才名单）。
- 领导干部任免/任前公示：`renshi-sources.md`；官员研究流程：`../methods/officials-research.md`。
- 高校与科研机构名录：`edu-research-institutions.md`；职称与职业资格：`professional-titles.md`。
