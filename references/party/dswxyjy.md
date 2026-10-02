# dswxyjy.org.cn —— 党史文献全文检索

- 去哪找：首页 `https://www.dswxyjy.org.cn/`；**站内检索页**（服务端空壳）`https://www.dswxyjy.org.cn/GB/458021/index.html?keywords=<JS escape 编码>`；**检索 JSON API** `POST https://search.peopletech.cn/search-platform/front/searchTalk`；成果总库 `https://ebook.dswxyjy.org.cn/`。
- 什么时候用：已知一个人名/事件名，要**党的文献原文或权威转述**；要**年谱 / 大事记 / 生平 / 传记**类条目；要**《党的文献》《中共党史研究》《百年潮》**等党刊文章；要**著作/文献汇编图书目录**。
- 怎么搜：**打 API，别爬检索页**——
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36'
  BODY='{"key":"年谱","limit":10,"page":1,"isFuzzy":false,"isHotIndex":false,"hasTitle":true,"hasContent":true,"type":8,"originalName":"","domain":"www.dswxyjy.org.cn","sortType":1,"startTime":1519833600000}'
  curl -s -m 20 -A "$UA" -H 'Content-Type: application/json;charset=UTF-8' \
    -X POST --data "$BODY" 'https://search.peopletech.cn/search-platform/front/searchTalk'
  ```
  ⚠️ 请求体必须**单行**：`--data '…'` 里的换行/续行符会被当成字面量，JSON 会解析失败。
  结果形态：`{"code":0,"data":{"records":[…],"total":N,"pages":M,"size":10,"current":1}}`；**`contentOriginal` 就是文章正文**（含 `<p>` 段落、`&lt;` 实体），入库时剥标签即可，多数文章**不必再回抓文章页**。
- 覆盖：站点文章约 **2018-03 至今**（检索页把 `startTime` 写死在 2018-03-01；更早稿件是否可得**未验证**），更新到 **2026-10**；粒度=单篇文章（含党刊文章）、图书（成果总库）；**没有**结构化的「人物条目 / 任职表」。
- 门槛：**免费、免登录、无验证码**；API **不需要 cookie、不需要 Origin/Referer**。
- 实测：2026-10-03，macOS arm64，curl 8.x，桌面 Chrome UA，`-m 20`：首页 200/103,038 B；检索页 200/10,736 B（空壳）；`POST /searchTalk` `key=年谱` → 200 `total=881, pages=89`；`key=周恩来` → `total=2639`；`key=习近平`（不带 Origin/Referer/cookie）→ `total=22933`；`contentOriginal` 抽样 1,037–50,847 字符（全文非摘要）；成果总库 200/38,036 B；旧「党史网」`zgdsw.org.cn` 三次 curl 000（NXDOMAIN）。明细见下。
- 上游：官网首页与 `…/img/MAIN/2019/06/119328/copy_nav.html`（栏目 URL 来源）；检索页 `/GB/458021/index.html` 内联 JS（API 路径、请求体字段、`escape()` 编码来源）；成果总库首页与 `/detail/163`。

## 细节

### 栏目入口（做「人物 / 事件」课题时按栏目下钻，比全站检索更干净）

| 栏目 | URL |
|---|---|
| 党史研究 | `https://www.dswxyjy.org.cn/GB/427167/index.html` |
| 人物研究 | `https://www.dswxyjy.org.cn/GB/423724/index.html` |
| 文献编辑 | `https://www.dswxyjy.org.cn/GB/423733/index.html` |
| 经典编译 | `https://www.dswxyjy.org.cn/GB/427184/index.html` |
| 理论研究 | `https://www.dswxyjy.org.cn/GB/427152/index.html` |
| 馆藏资源 | `https://www.dswxyjy.org.cn/GB/427195/index.html` |
| 成果总库（站内页） | `https://www.dswxyjy.org.cn/GB/427196/index.html` |
| 影像纪录 | `https://www.dswxyjy.org.cn/GB/427202/index.html` |
| 地方工作 | `https://www.dswxyjy.org.cn/GB/427192/index.html` |
| 《中共党史研究》 | `https://www.dswxyjy.org.cn/GB/427245/219030/index.html` |
| 《党的文献》 | `https://www.dswxyjy.org.cn/GB/427245/423799/index.html` |
| 《百年潮》 | `https://www.dswxyjy.org.cn/GB/427245/219031/index.html` |
| 专题集锦（人物纪念专题） | `https://www.dswxyjy.org.cn/GB/427277/index.html` |

其他入口：文章页 `https://www.dswxyjy.org.cn/n1/<年>/<月日>/c<栏目id>-<文章id>.html`（人民网系 `n1` CMS 风格，如 `/n1/2019/0228/c423718-30918217.html` =《毛泽东年谱》评介）；馆藏检索 `http://lib.dswxyjy.org.cn/`（首页导航里**被注释掉**，**未实测**）。

### A. 站内检索（标题+全文）

请求体字段（全部来自检索页内联 JS，逐项实测）：

| 字段 | 值 | 说明 |
|---|---|---|
| `key` | 关键词 | 中文直接传 |
| `page` | 1,2,… | 检索页是 0 基、接口是 1 基（`page: page+1`） |
| `limit` | 10 | 检索页固定 10，**上限未验证** |
| `hasTitle` / `hasContent` | true / true | 标题、全文开关；检索页两者都 true |
| `type` | 8 | 站点类型（该检索中台的站点编号） |
| `domain` | `www.dswxyjy.org.cn` | **锁定本站**，别去掉 |
| `sortType` | 1 | 检索页用 1（其他值未验证） |
| `startTime` | `1519833600000` | 检索页写死 = 2018-03-01（0 时，UTC+8）；**是否真起过滤作用、能否改小以取更早稿件未验证** |

一条记录样例：

```json
{"title":"《毛泽东<em>年</em><em>谱</em>（1949—1976）》的主要特点和研究价值",
 "url":"http://www.dswxyjy.org.cn/n1/2019/0228/c423718-30918217.html",
 "content":"…（带 <em> 逐字高亮 的片段，514–1220 字符）…",
 "contentOriginal":"<p style=\"text-indent: 2em;\">…（**正文原文 HTML，最长实测 50,847 字符**）…",
 "author":"","editor":"刘小源","belongsName":"#河北#编研成果#","belongsId":"[\"427987\",\"430648\"]",
 "originName":"","sourcetitle":"","source":1,"sourceId":32393652,"contentId":32393652,
 "displayTime":1551384270000,"inputTime":…,"domain":"www.dswxyjy.org.cn","isOfficial":…}
```

- `displayTime` / `inputTime` = epoch **毫秒**（`1551384270000` = 2019-02-28）。
- `belongsName` 是栏目路径（`#` 分隔，如 `#河北#编研成果#`），可据此过滤"只保留中央或某栏目"。
- 替代通道（**给浏览器用**）：检索页 `…/GB/458021/index.html?keywords=<值>`，值要用 JS `escape()` 编码，即中文编成 `%uXXXX`（页面里是 `unescape(decodeURI(参数))`）。

### B. 成果总库（图书）

- 目录页 `https://ebook.dswxyjy.org.cn/ebooks/list/<分类id>`（分类 id 实测出现 1–5、6、8、33、64–75、81–90、134），单书 `https://ebook.dswxyjy.org.cn/detail/<id>`。
- 站内搜索表单：`<form name="searchForm" method="post">`，字段 `keyword`，action 由 JS 设成站点根 `https://ebook.dswxyjy.org.cn:443` → **POST 到根路径**（**未实测**，仅页面源码）。
- 「立即阅读」指向静态翻页壳：`https://ebook.dswxyjy.org.cn/dswxbooks/storage/files/<日期>/<hash>/mobile/index.html`（实测 200，仅 2 KB；正文由 `javascript/main.js` + 页面图渲染）→ **正文取不到纯文本，只能人读**。

### 命中量与实测记录（2026-10-03，macOS arm64，curl 8.x，桌面 Chrome UA，`-m 20`）

命中量（`limit` 不同，`pages` 随之变：`pages = ceil(total/limit)`）：`年谱` = **881 条**（limit=5→177 页；limit=10→89 页）；`周恩来` = **2,639 条**；`习近平` = **22,933 条**。

| 请求 | 结果 |
|---|---|
| `GET https://www.dswxyjy.org.cn/` | **200 / 103,038 B**，`<title>中央党史和文献研究院官网` |
| `GET …/GB/458021/index.html?keywords=%u5B5F%u5B89%u5AB4` | **200 / 10,736 B** —— `搜索结果页` 空壳（内联 JS 调 API） |
| `GET …/GB/458021/index.html?keywords=%E5%85%9A%E5%8F%B2`（UTF-8 百分号编码） | **200 / 10,736 B**，同样空壳（页面自己再 `unescape(decodeURI())`，两种编码都不影响，因为结果靠 API） |
| `POST …/searchTalk` `key=年谱`（limit=5） | **200**，`code=0, total=881, pages=177`；首条 2022-04《李锋传记与年谱》出版发行 |
| `POST …/searchTalk` `key=年谱`（limit=10，即本卡示例命令） | **200**，`total=881, pages=89, n=10`，`contentOriginal=1037` 字符 |
| `POST …/searchTalk` `key=周恩来` | **200**，`code=0, total=2639, pages=528` |
| `POST …/searchTalk` `key=习近平`（**不带 Origin/Referer/cookie**） | **200**，`total=22933` |
| `contentOriginal` 长度抽样 | 1,037 / 50,847 / 37,863 / 15,526 字符 → **是全文，不是摘要** |
| `GET …/img/MAIN/2019/06/119328/copy_nav.html` | **200 / 6,366 B**，全部一级栏目 URL（上表） |
| `GET https://ebook.dswxyjy.org.cn/` | **200 / 38,036 B**，`<title>成果总库` |
| `GET …/detail/163` | **200 / 16,331 B**，《建国以来重要文献选编（第一册）》，"立即阅读"→ 静态翻页壳 |
| `GET …/dswxbooks/storage/files/20220713/845e…/mobile/index.html` | **200 / 2,171 B**，图片翻页壳（非文本） |
| 旧「党史网」`http://www.zgdsw.org.cn/`（3 次：http、https、/GB/） | **000**；`dig`：`www.zgdsw.org.cn` = **NXDOMAIN**，apex `zgdsw.org.cn` = NOERROR 但**无 A 记录（NODATA）** → 域名已无可用解析，不再是可用入口 |

请求纪律：单主机 ≤3 次（本站因核实编码/栏目/示例命令各多打了几次，共 5 次 `www.dswxyjy.org.cn`、4 次 `search.peopletech.cn`、3 次 `ebook.dswxyjy.org.cn`），间隔 ≥1.7 s，未触发任何拦截。

### 从「人名 / 事件名」到原文的检索路径（本库用法）

1. 人名 + 体裁词：`key = "<人名> 年谱"` 或 `"<人名> 传"`/`"<人名> 生平"`（如 `周恩来 家风`、`毛泽东 年谱`）；
2. 只给事件：`key = "<事件名>"`（如 `南渡长江`、`建国以来重要文献`），`sortType=1` 走默认相关度；
3. 取回 JSON → 用 `contentOriginal` 存正文、`displayTime` 排序、`belongsName` 过滤栏目；
4. 补一手原件：文章里引的《毛泽东年谱》《建国以来重要文献选编》等，去 `ebook.dswxyjy.org.cn` 按书名找 `/detail/<id>` 在线阅读；
5. 需要党报口径的同一稿：再用 `cpc.people.com.cn` 站内检索（见 `cpc.people.com.cn.md`）交叉验证。

## 坑

1. **检索页 ≠ 检索结果**：`/GB/458021/index.html` 是 Laravel 式空壳，参数由 `unescape(decodeURI(QueryString("keywords")))` 取出后 POST 到 `search.peopletech.cn`。要自动化就直接打 API。
2. **`search.peopletech.cn` 是共用检索中台**：`search.people.cn` 的同族接口（注释里留着 `//search.people.cn/search-platform/front/searchTalk`）。换站点要改 `type` + `domain`；本次只验证了 `type=8 / domain=www.dswxyjy.org.cn`。
3. **高亮标签要剥**：`title`/`content` 里是 `<em>` 逐字高亮；要干净正文用 `contentOriginal`。
4. **正文可能被拆句**：短讯（如《…出版发行》）`contentOriginal` 只有 1 KB 左右，长文可到 50 KB —— 别用长度阈值判"是否全文"。
5. **成果总库不是文本库**：`/detail/<id>` 只有书目 + 简介；正文在图片翻页壳里，**不能当语料库用**，只能人工阅读。
6. **`lib.dswxyjy.org.cn`（馆藏检索）在首页被注释掉**：可能已下线，未实测，别当作可靠通道。
7. **「年谱 / 大事记」是文章标题词，不是独立数据库**：本站没有可检索的年谱数据集，靠关键词召回文章后再抽表。
