# npc-gov-regulations —— 法规与党内法规聚合索引

法律/行政法规/司法解释的**官方全文**在 `flk.npc.gov.cn`（见 `flk.npc.gov.cn.md`）；本文件补齐两块"法规体系"聚合源：**国务院部门规章库**与**共产党员网党内法规库**，并给出分工表。

- 去哪找：
  - 宪法/法律/行政法规/监察法规/地方性法规/司法解释 → 国家法律法规数据库 `flk.npc.gov.cn`（免登录，含 Word/PDF 原件）
  - 国务院部门规章 → 中国政府网「国家规章库」`www.gov.cn/zhengce/xxgk/gjgzk/index.htm`
  - 党中央/中办文件（含党内法规性质文件） → 中国政府网检索 `t=zhengce` 的 `zhongyangfile` 类，`sousuo.www.gov.cn/search-gov/data`
  - 党内法规（党章/准则/条例/规则/规定等） → 共产党员网「党内法规库」`www.12371.cn/special/dnfg/search/index.shtml` + JSONP 接口
- 什么时候用：要**国务院部门规章**；要**党中央/中办文件**（新闻口径转载）；要**党内法规**（党章/准则/条例/规则/规定等，引用条文优先法规库正式版）。
- 怎么搜：
  - 国家规章库：页面内检索跳到 `https://sousuo.www.gov.cn/s.htm?t=zhengcelibrary`；其 JSON 接口 `GET https://sousuo.www.gov.cn/search-gov/data?t=zhengcelibrary&q=<词>&p=1&n=5`（实测返回 `catMap`：`gongwen` / `bumenfile`（部门文件）/ `otherfile` / `gongbao`）。
  - 党中央/中办文件：`GET https://sousuo.www.gov.cn/search-gov/data?t=zhengce&q=<词>&p=1&n=5` → `searchVO.catMap.zhongyangfile`（实测 `q=营商环境` 时 `totalCount=265`）。
  - 党内法规库：JSONP 接口 `GET https://search.12371.cn/service/xuexipingtaisearch.php?t=xuexipingtai&pageids=<8 个 PAGE id 逗号分隔>&sort=&mindate=&searchfield=&format=jsonp&q=<词>&p=<页码>`（`pageids` 必须带全 8 个，见「细节」）。
- 覆盖：国务院部门规章（国家规章库）；党中央/中办文件（新闻口径转载，不一定覆盖全部党内法规）；党内法规（12371 法规库正式版）。
- 门槛：免费、免登录（12371 接口亦免登录，实测可用）。
- 实测：2026-10-02，macOS，curl 8.x。国家规章库、gov.cn `t=zhengcelibrary`、12371 党内法规 JSONP 接口均为当日实际请求验证（见各节状态码与返回片段）。
- 上游：`https://www.gov.cn/`（中国政府网） ｜ `https://www.12371.cn/`（共产党员网）

## 细节

### 分工表

| 法规层级 | 权威来源 | 端点 |
|---|---|---|
| 宪法 / 法律 / 行政法规 / 监察法规 / 地方性法规 / 司法解释 | 国家法律法规数据库 | `flk.npc.gov.cn`（免登录，含 Word/PDF 原件）|
| 国务院部门规章 | 中国政府网「国家规章库」 | `www.gov.cn/zhengce/xxgk/gjgzk/index.htm` |
| 党中央/中办文件（含党内法规性质文件） | 中国政府网检索 `t=zhengce` 的 `zhongyangfile` 类 | `sousuo.www.gov.cn/search-gov/data` |
| 党内法规（党章/准则/条例/规则/规定等） | 共产党员网「党内法规库」 | `www.12371.cn/special/dnfg/search/index.shtml` + JSONP 接口 |

### 1. 国家规章库（国务院部门规章）

- 页面：`https://www.gov.cn/zhengce/xxgk/gjgzk/index.htm` → **200**，标题「国家规章库_中国政府网」（21 KB 静态 HTML）。
- 页面内检索跳到 `https://sousuo.www.gov.cn/s.htm?t=zhengcelibrary`；其 JSON 接口即 `GET https://sousuo.www.gov.cn/search-gov/data?t=zhengcelibrary&q=<词>&p=1&n=5`（实测返回 `catMap`：`gongwen` / `bumenfile`（部门文件）/ `otherfile` / `gongbao`）。
- 字段与翻页同 `gov.cn.md`（结果从 `searchVO.catMap.<类>.listVO` 取）。

### 2. 党中央/中办文件

- `GET https://sousuo.www.gov.cn/search-gov/data?t=zhengce&q=<词>&p=1&n=5` → `searchVO.catMap.zhongyangfile`（实测 `q=营商环境` 时 `totalCount=265`）。
- 条目示例：「中共中央 国务院转发《…》」「中共中央办公厅 国务院办公厅印发《…》」。
- 注意：这是**新闻口径**转载的中央文件，不一定覆盖全部党内法规；系统性党内法规仍用下一节。

### 3. 共产党员网「党内法规库」（党章党规检索）

检索页（人用）：`https://www.12371.cn/special/dnfg/search/index.shtml` → **200**（102 KB HTML）。页面用 **JSONP** 调后端，接口（免登录，实测可用）：

```
GET https://search.12371.cn/service/xuexipingtaisearch.php
      ?t=xuexipingtai
      &pageids=<页面内 baurl 变量里的 8 个 PAGE id，逗号分隔>
      &sort=&mindate=&searchfield=
      &format=jsonp&q=<关键词>&p=<页码>
```

`pageids` 固定为（从检索页 `var baurl` 抄出，实测不带会漏结果）：

```
PAGE1472610694036842,PAGE1460954369233788,PAGE1460106930943150,PAGE1460106641214705,PAGE1460103255609145,PAGE1459927326501323,PAGE1459911513949209,PAGE1563157469366649
```

（一行逗号分隔；实测带全 8 个 id 才返回完整结果。）

实测 curl：

```bash
curl -s -m 20 -H 'Referer: https://www.12371.cn/special/dnfg/search/index.shtml' \
  'https://search.12371.cn/service/xuexipingtaisearch.php?t=xuexipingtai&pageids=PAGE1472610694036842,PAGE1460954369233788,PAGE1460106930943150,PAGE1460106641214705,PAGE1460103255609145,PAGE1459927326501323,PAGE1459911513949209,PAGE1563157469366649&sort=&mindate=&searchfield=&format=jsonp&q=%E9%97%AE%E8%B4%A3&p=1'
```

响应（JSONP 包裹）：

```
callback_search({"q":"问责","p":"1","n":10,
  "searchVO":{"totalcount":60, "maxPageSize":6,
     "listVO":[{"pubtime":"2019-09-04 18:33:31",
                "title":"中国共产党<em class=\"highlgt\">问责</em>条例",
                "keywords":[...], "type":"图文",
                "url":"https://www.12371.cn/2019/09/04/ARTI1567593093489593.shtml",
                "brief":"…<em class=\"highlgt\">问责</em>…", "pageid":"…", "imagelink":…}, …]}})
```

- 解析：剥掉 `callback_search( … )` 外壳再 `json.loads`；`title`/`brief` 含 `<em class="highlgt">` 高亮标签，需清洗。
- `totalcount` 为总命中，`maxPageSize` 为总页数（实测 `q=问责`：60 条 / 6 页）。
- 实测 `q=党内法规` → `totalcount=7`（含党章两版）；`q=问责` → `totalcount=60`（含《中国共产党问责条例》等）。

## 坑

1. 国家规章库只有 HTML 目录页 + 走 `sousuo` 的 JSON；`/zhengce/zhengceku/` 目录页是 403（见 `gov.cn.md`）。
2. 党内法规库接口是 **JSONP**（`callback_search(...)`），不是纯 JSON，需去壳；`pageids` 必须带上完整 8 个 id。
3. 党内法规的"新闻转载版"（gov.cn `zhongyangfile`）与"法规库正式版"（12371）会有出入，引用条文优先 12371。
4. 未验证：12371 该接口的 `sort` / `mindate` / `searchfield` 取值语义（默认空即可用）。
