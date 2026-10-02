# 近代报刊数据库总览 —— 民国报刊库入口与权限一览

「近代报刊」没有单一总库：晚清民国报刊分散在**爱如生（典海）、瀚堂、全国报刊索引、大成故纸堆、国图系列、人民日报/光明日报自建库、台湾机构库**等十来个互不重叠的平台上。本卡只解决「**有哪些库、去哪进、要什么权限**」——除少数可匿名试看的，绝大多数要机构 IP/订阅。可程序化取数的优先看 `modernhistory.md`、`cnbksy.md`。

- 去哪找：
  - **爱如生·典海数字平台**（近代报刊/申报/大公报/新华日报/基本古籍/方志的总入口）：`http://dh.ersjk.com/`；产品页与个人版在 `www.er07.com` / `isk.er07.com` / 体验站 `ty.er07.com`
  - **瀚堂**（古籍 + 近代报刊，超大字符集）：古籍 `https://www.hytung.cn/`；近代报刊 `https://www.neohytung.com/`
  - **全国报刊索引**：`https://www.cnbksy.com/`（详见 `cnbksy.md`）
  - **大成故纸堆**：`https://www.dachengdata.com/`（详见 `dachengdata.md`）
  - **国图·民国时期文献**：`http://mylib.nlc.cn/specialResourse/minguoIndex`（民国图书/法律/期刊/报纸），民国期刊检索页 `http://read.nlc.cn/allSearch/searchList?pageNo=1&searchType=35&showType=1`，近代报纸库 `http://bz.nlcpress.com/`
  - **人民日报图文数据库**：`https://data.people.com.cn/rmrb/`（1946 至今，未登录只能看目录）
  - **光明日报**：`https://epaper.gmw.cn/gmrbdb`（历年库，需浏览器）、搜索页 `https://zhonghua.gmw.cn/`
  - **台湾**：中研院臺史所 `https://taicool.ith.sinica.edu.tw/`（免费）、聯合知識庫 `https://udndata.com/`、臺灣國圖 `https://newspaper.ncl.edu.tw/`
- 什么时候用：
  - 要找**晚清/民国某报某刊的全文或影像**（申报、大公报、益世报、顺天时报、民国日报、中央日报、新华日报、红色中华…）；
  - 只拿到一个刊名/年份，要先确认**哪个平台收了、需要什么账号**；
  - 需要**近代期刊篇目/题录**做线索（全国报刊索引篇名库）；
  - 需要**当代党报全文**（人民日报 1946–、光明日报）。
- 怎么搜：多数库**没有公网匿名检索入口**，只能到机构 IP 内的检索页用；本卡给的是「入口 + 匿名可用性」。三条**本机可复现**的入口：
  1. 爱如生典海平台（登录/介绍页，匿名可见产品目录）：`curl -sSL -A '<桌面 Chrome UA>' 'http://dh.ersjk.com/'`（**注意只有 http 通，https 连不上**）
  2. 瀚堂近代报刊（登录框 + 库简介，匿名可见）：`curl -sSL -A '<桌面 Chrome UA>' 'https://www.neohytung.com/'`
  3. 人民日报图文数据库（未登录可读当日目录，全文要登录）：`curl -sSL -A '<桌面 Chrome UA>' 'https://data.people.com.cn/rmrb/20260827/1'`
  结果形态：均为 **HTML**；检索 API 未探到（各库都在登录墙后）。
- 覆盖：晚清（1833 起）至 1949 的报纸、期刊、要刊；当代党报（人民日报 1946–、光明日报）。粒度：影印页 + 全文录文（爱如生/瀚堂/报刊索引），题录级（部分）。各库范围见「细节」表。
- 门槛：**以订阅 / 机构 IP / 读者卡为主**；少数可匿名试看目录（人民日报、瀚堂登录框、典海介绍页、国图民国文献页），全文一律要权限。中研院臺史所库免费。
- 实测：2026-10-03，macOS 27（arm64），curl 8.x，桌面 Chrome UA。`GET http://dh.ersjk.com/` → **200 / 27.9 KB**（`<title>erDataBases</title>`，爱如生典海平台）；`https://dh.ersjk.com/` → **000（连接失败）**。`http://www.er07.com/home/pro_89.html` → **200 / 53 KB**（中国近代要刊库参数）。`https://www.hytung.cn/` → **200 / 29 KB**；`https://www.neohytung.com/` → **200 / 25 KB**（瀚堂近代报刊数据库）。`https://data.people.com.cn/rmrb/20260827/1` → **200 / 40 KB**（未登录提示「无法浏览全部内容」）。`https://zhonghua.gmw.cn/` → **200 / 7.7 KB**；`http://epaper.gmw.cn/gmrbdb` → **301 → https 后 Connection reset（curl 56）**。`http://read.nlc.cn/allSearch/searchList?pageNo=1&searchType=35&showType=1` → **200 / 26.6 KB**；`http://mylib.nlc.cn/specialResourse/minguoIndex` → **200 / 22.6 KB**。`http://bz.nlcpress.com/` → **200（Tomcat 7.0.109 默认页）**，`https://bz.nlcpress.com/library/` → **200 → `/library/publish/Main.jsp`（77 B 框架页）**。`https://tk.cepiec.com.cn/tknewsc/tknewskm` → **200 / 368 B（`TTS_AntiProxy` 反代理页）**。`https://taicool.ith.sinica.edu.tw/` → **200 / 36.9 KB**（臺灣文獻全文資料庫）。`https://udndata.com/` → **403**；`https://tpl.ncl.edu.tw/` → **403 / 46 B**；`https://newspaper.ncl.edu.tw/` → **200 → `/mysite/notification/`**；`https://www.ntl.edu.tw/...` 与 `https://nctpehd.ntl.edu.tw/advance` → **000 连接超时**。
- 上游：`http://www.er07.com/`（爱如生）、`https://www.hytung.cn/`、`https://www.neohytung.com/`、`https://www.cnbksy.com/`、`https://www.dachengdata.com/`、`https://www.nlc.cn/`、`https://data.people.com.cn/`、`https://www.gmw.cn/`

## 细节

> 下表的「收录范围/年代」均取自各库官网产品页或图书馆库介（**上游声明，未本机实测**）；只有上面「实测」行列出的入口状态是本机 2026-10-03 验证的。

### 总表：库 → 入口 → 范围/年代 → 门槛

| 库 | 入口 | 收录范围/年代 | 门槛 |
|---|---|---|---|
| 爱如生·典海数字平台（总入口） | `http://dh.ersjk.com/` | 平台登录/产品导航；含下列各库 | 机构 IP / 注册；**仅 http** |
| 爱如生·中国基本古籍库 | `http://www.er07.com/home/pro_3.html`；个人版 `http://isk.er07.com/` | 先秦至民国古籍全文 | 订阅；个人版付费 |
| 爱如生·中国近代要刊库（全文检索版） | `http://www.er07.com/home/pro_89.html` | **1833–1949**，精选 **1000 种期刊（约 5 万期号）**，影像 300 万页 / 录文 19 亿字 | 订阅（机构 IP） |
| 爱如生·申报数据库 | `http://www.er07.com/home/pro_220.html` | 《申报》**1872–1949**（上海版/汉口版等，保留全部原报影像） | 订阅；有**个人版**（`info_10.html`） |
| 爱如生·大公报数据库 | `http://www.er07.com/home/pro_222.html` | 《大公报》近代各版 | 订阅 |
| 爱如生·新华日报数据库 | `http://www.er07.com/home/pro_230.html` | 《新华日报》**1938–1947**（武汉创刊→重庆→停刊） | 订阅 |
| 爱如生·红色中华/新中华报数据库 | `http://www.er07.com/home/pro_229.html` | 中央苏区/延安时期党报 | 订阅 |
| 爱如生·红色历史文献库 | `http://www.er07.com/home/pro_189.html` | **1915–1949**，大报 10 种 / 要刊 150 种 / 纪实 40 种，影像 100 万页 | 订阅 |
| 爱如生·中国方志库 | 见 `http://ty.er07.com/` 24 库列表与 `www.er07.com` | 历代方志全文 | 订阅 |
| 瀚堂典藏（古籍库） | `https://www.hytung.cn/` | 约 **40,000 种古籍** + 25,000 种民国报刊，7,000 万条记录，超大字符集 | 机构 IP / 登录 |
| 瀚堂近代报刊数据库 | `https://www.neohytung.com/` | **3,000 多万笔记录、25,000 种报刊**；含《申报》《大公报》《顺天时报》《益世报》《遐迩贯珍》《北洋画报》《民国日报》 | 机构 IP / 登录（匿名可看登录框+简介） |
| 全国报刊索引（上图） | `https://www.cnbksy.com/` | 篇名库 1816 至今；晚清/民国期刊全文、近代报纸全文 1850–1951 | 机构订阅 + WAF（见 `cnbksy.md`） |
| 大成故纸堆 | `https://www.dachengdata.com/` | 老刊 / 民国图书 / 晚清民国报纸 / 方志 / 家谱 | 机构登录（见 `dachengdata.md`） |
| 国图·民国时期文献门户 | `http://mylib.nlc.cn/specialResourse/minguoIndex` | 民国图书 / 法律 / 期刊 / 报纸 / 革命历史文献资源库（导航页） | 读者卡登录 / 到馆 |
| 国图·民国期刊检索 | `http://read.nlc.cn/allSearch/searchList?pageNo=1&searchType=35&showType=1` | 民国期刊题录/全文 | 读者卡登录 |
| 中国历史文献总库·近代报纸数据库 | `http://bz.nlcpress.com/`（→ `/library/publish/Main.jsp`） | 近代报纸（国图出版社，按期/辑采购） | 机构 IP，无并发限制（厦大口径）；商业库 |
| 中国历史文献总库·民国图书数据库 | `http://mg.nlcpress.com/` | 民国图书（已出 8 期约 22 万种） | 付费/机构（见 `nlc.cn.md`） |
| 人民日报图文数据库 | `https://data.people.com.cn/rmrb/` | 《人民日报》**1946 至今**，全文+版面 | 免费看目录，**全文需登录** |
| 光明日报·历年光明日报数据库 | `https://epaper.gmw.cn/gmrbdb` | 《光明日报》历年，全文+版面 | 免费但 **curl 被 reset，需浏览器** |
| 光明日报·报系历史数据检索 | `https://zhonghua.gmw.cn/`、`https://zhonghua.neamco.com/search_advanced.htm` | 光明日报报系（光明日报/中华读书报/文摘报） | 匿名可用（搜索页） |
| 繙云历史文献库（教图代理） | `http://fanyun.cepiec.com.cn/`；大公报 `http://tk.cepiec.com.cn/tknewsc/tknewskm`（台服 `http://tk.dhcdb.com.tw/...`） | 《民国日报》《中央日报》《大公报》《申报》 | 机构订阅；裸访问遇 `TTS_AntiProxy` 反代理页 |
| 中研院臺史所·臺灣文獻全文資料庫 | `https://taicool.ith.sinica.edu.tw/` | 臺灣文獻叢刊（方志/檔案/文獻三类）+ 《臺灣新聞》1938–1944 報紙標題與影像 | **免费**（另有 `sinica.md`） |
| 聯合知識庫 | `https://udndata.com/` | 聯合報系 1951 至今（联合报/经济日报/联合晚报…） | 订阅；裸访问 **403** |
| 臺灣國家圖書館·報紙 | `https://newspaper.ncl.edu.tw/` | 台湾报纸资源 | 免费页面（落到 `/mysite/notification/`） |
| 臺灣期刊論文索引 | `https://tpl.ncl.edu.tw/` | 台湾期刊论文题录 | 裸访问 **403** |
| 國立臺灣圖書館（近代報刊資料庫/报纸目录） | `https://www.ntl.edu.tw/` | 中國近代報刊資料庫(典藏版)、自立晚報資料庫等 | 本机**连接超时**，未验证 |

## 坑

1. **爱如生典海只认 `http://dh.ersjk.com/`**：`https://dh.ersjk.com/` 本机直接连不上（000），别把 TLS 失败当成站挂了。
2. **三个「申报/大公报」不是一套**：爱如生（典海，含个人版）、瀚堂近代报刊、繙云（教图代理）/全国报刊索引各自收录不同版本与时段；引用前先确认是哪家的数字本。
3. **瀚堂有两个域名**：`hytung.cn` = 古籍（瀚堂典藏），`neohytung.com` = 近代报刊；不要混用。
4. **繙云的 `tk.cepiec.com.cn` / `tk.dhcdb.com.tw` 返回 368 B `TTS_AntiProxy`**，是反代理页，必须经机构 IP 内的正式入口访问，勿尝试绕行。
5. **光明日报 `epaper.gmw.cn/gmrbdb` 对 curl 直接 reset**（浏览器可用），要自动取数改用 `zhonghua.gmw.cn` 或另找接口。
6. 国图 `bz.nlcpress.com` 根路径是 Tomcat 默认页，真正应用在 `/library/publish/Main.jsp` 框架里，直接抓根路径会误判为「没有内容」。
7. 台湾 `udndata.com`、`tpl.ncl.edu.tw` 对裸访问返回 403；`ntl.edu.tw` 系在本机超时——结论只能写「需浏览器/未验证」，不要臆测其检索接口。
8. 当代库与近代库别混：人民日报（1946–）与民国报刊是两套；`data.people.com.cn` 未登录只能看目录。
9. **优先级**：能匿名批量取数的先走 `modernhistory.md`（JSON+IIIF）；要最宽的报刊面走 `cnbksy.md`；本卡其余多为「知道去哪、要什么权限」的通道。
