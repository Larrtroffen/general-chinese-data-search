# gov.cn —— 政策文件库与国务院公报检索

- 去哪找：
  - 站内检索 API（核心，JSON）：`https://sousuo.www.gov.cn/search-gov/data`
  - 人用的检索页：`https://www.gov.cn/sousuo/search.shtml?code=17da70961a7&searchWord=…`（200，67 KB HTML 壳）
  - 最新政策列表：`https://www.gov.cn/zhengce/zuixin/`（200）
  - 国家规章库：`https://www.gov.cn/zhengce/xxgk/gjgzk/index.htm`（200）
  - 国务院公报索引：`https://www.gov.cn/gongbao/` → JS 跳 `…/gongbao/currentissue.htm`；按期目录 `https://www.gov.cn/gongbao/YYYY/issue_<期号>/`（200）
  - 公报高级检索：`https://www.gov.cn/search/gbsousuo.htm`（200，表单 GET 到 sousuo）
- 什么时候用：要国务院/中央文件的**原文 URL**；按关键词 + 发文机关 + 年份 + 文号检索政策；要国家规章库、国务院公报按期目录。
- 怎么搜：
  - 检索 API 参数：`t`（检索库：`zhengce` 国务院/中央文件、`zhengcelibrary` 政策文件库（含部门文件与公报）、`gongbao` 仅公报）、`q`（关键词）、`p`/`n`（页码/每页条数）、`sort=score`+`sortType=1`、`searchfield=title:content`、`timetype=timeqb`（全部）/`timezd`（自定义）、`mintime`/`maxtime`（`timetype=timezd` 时用）。
  - ⚠️ **不要**带 `type=gwyzcwjk`（或其它 `type=` 值）：实测返回 200 但 `totalCount=0`、`listVO=null`，只剩 facet 计数。
  - 结果形态：JSON，结果按分类在 `searchVO.catMap.<类>.listVO`，`url` 即正文页直链。
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
  curl -s -m 20 -A "$UA" -H 'Referer: https://sousuo.www.gov.cn/' \
    'https://sousuo.www.gov.cn/search-gov/data?t=zhengce&q=%E8%90%A5%E5%95%86%E7%8E%AF%E5%A2%83&timetype=timeqb&sort=score&sortType=1&searchfield=title%3Acontent&p=1&n=5'
  ```
  - 正文抓取（静态 HTML，UTF-8）：`curl -s -m 20 -A "$UA" 'https://www.gov.cn/zhengce/zhengceku/202609/content_7081881.htm'`
- 覆盖：国务院/中央文件（`gongwen`、`zhongyangfile`）+ 部门文件（`bumenfile`）+ 公报（`gongbao`）+ 解读与动态（`otherfile`），全国、历年；粒度=单篇文件；动态更新。
- 门槛：免费、免登录、无 key。
- 实测：2026-10-02，macOS，curl 8.x，桌面 UA。`q=营商环境` → `searchVO.catMap.gongwen.totalCount=1483`、`zhongyangfile=265`、`otherfile=2007`；`p=2` 后首条变为更老的 2023 年文件（翻页有效）；正文页示例 200，28 KB，`<title>` 为文号+文件名。
- 上游：<https://www.gov.cn/>、<https://sousuo.www.gov.cn/>

## 细节

### 可用性矩阵（本机实测）

| 端点 | 状态 | 现象 |
|---|---|---|
| `https://sousuo.www.gov.cn/` | ✅ | 200 |
| `POST/GET https://sousuo.www.gov.cn/search-gov/data?t=zhengce…` | ✅ | 200，`application/json`，约 21–26 KB |
| `…/search-gov/data?t=zhengcelibrary…` | ✅ | 200，含 `gongwen/bumenfile/otherfile/gongbao` 四类 |
| `…/search-gov/data?t=gongbao…` | ✅ | 200，仅有 `gongbao` 类 |
| `https://www.gov.cn/sousuo/search.shtml?code=17da70961a7&searchWord=…` | ✅ | 200（人用的检索页，67 KB HTML 壳） |
| `https://www.gov.cn/zhengce/zuixin/` | ✅ | 200（最新政策列表页） |
| `https://www.gov.cn/zhengce/xxgk/gjgzk/index.htm` | ✅ | 200「国家规章库_中国政府网」 |
| `https://www.gov.cn/zhengce/zhengceku/`（目录页） | ❌ | **403 Forbidden（nginx）**；但 `…/zhengceku/YYYYMM/content_*.htm` 正文页 200 |
| `https://www.gov.cn/gongbao/` | ⚠️ | 200 但仅 898 B JS 跳转 → `gongbao/currentissue.htm` |
| `https://www.gov.cn/search/gbsousuo.htm` | ✅ | 200，公报**高级检索**表单页（GET 提交到 sousuo） |
| `https://sousuo.gov.cn/…`（无 www） | ❌ | DNS 不解析（curl 退出码 6） |

### 请求参数

| 参数 | 说明 / 取值 |
|---|---|
| `t` | 检索库：`zhengce`（国务院/中央文件）、`zhengcelibrary`（政策文件库，含部门文件与公报）、`gongbao`（仅公报） |
| `q` | 关键词（URL 编码） |
| `p` / `n` | 页码 / 每页条数（实测 `p=2` 返回更旧结果，翻页有效） |
| `sort` / `sortType` | `score` / `1`（相关度） |
| `searchfield` | `title:content`（标题+正文） |
| `timetype` | `timeqb`（全部，实测有效）/ `timezd`（自定义，实测有效） |
| `mintime` / `maxtime` | 自定义起止日期（`timetype=timezd` 时用） |

### 响应结构

```
{ "code":200, "msg":"操作成功",
  "searchVO": {
     "totalCount": 0,                       # ← 顶层恒为 0，别用！
     "catMap": {                            # 结果按分类分组，从 catMap.<类> 取
        "gongwen":      { "totalCount":1483, "catName":"gongwen", "listVO":[ … ] },
        "zhongyangfile":{ "totalCount":265,  … },
        "otherfile":    { "totalCount":2007, … } } },
  "paramsVO": { … } }
```

- `t=zhengce` 的 `catMap` 类：`gongwen`（国务院公文）、`zhongyangfile`（中央/中办文件）、`otherfile`（解读/动态）。
- `t=zhengcelibrary` 的类：`gongwen`、`bumenfile`（部门文件）、`otherfile`、`gongbao`。
- `t=gongbao` 的类：仅 `gongbao`（`q=国务院令` 时 `totalCount=15030`）。

### listVO 条目字段

| 字段 | 含义 / 备注 |
|---|---|
| `title` | 标题 |
| `url` | **正文页直链**，如 `https://www.gov.cn/zhengce/zhengceku/202609/content_7081881.htm` |
| `pcode` | 发文字号（如 `国办函〔2026〕84号`；政策类常为空） |
| `puborg` | 发文机关 |
| `pubtimeStr` | 公布日期 `YYYY.MM.DD`；⚠️ 部分条目（翻页后）为 `null`，改用 `ptime` |
| `ptime` | 毫秒时间戳（同页 `pubtime` 亦为毫秒，可能为 0） |
| `childtype` | 主题分类（如 `综合政务\电子政务`） |
| `summary` | 摘要（命中词用 `<em>` 包裹） |
| `index` | 索引号（如 `000014349/2026-00071`） |
| `id` | 内部 id |

- 解析建议：遍历 `catMap` 各 `listVO` 合并，按 `url` 或 `id` 去重；分类间会有重复条目。

### 政策文件库 / 国务院公报（HTML 浏览）

- 国务院公报：索引 `https://www.gov.cn/gongbao/` → JS 跳到 `…/gongbao/currentissue.htm`（返回一段 JS 计算最新期号）→ 按期目录 `https://www.gov.cn/gongbao/YYYY/issue_<期号>/`（实测 200，30 KB，内含 60+ 篇目链接，形如 `https://www.gov.cn/zhengce/gb/content_2683006.htm`）。
- 公报高级检索：`https://www.gov.cn/search/gbsousuo.htm`，表单 GET 到 `https://sousuo.www.gov.cn/sousuo/search.shtml?code=17da70961a7&dataTypeId=15&advance=true&title=&content=&searchMode=precision&…`。

## 坑

1. `totalCount` 顶层恒 0，必须读 `searchVO.catMap.<类>.totalCount`。
2. `type=` 参数会静默清零结果（见上）。
3. 政策文件库**目录页** `/zhengce/zhengceku/` 403，别去爬目录，直接用检索 API 拿 `url`。
4. `sousuo.gov.cn`（无 www）在本机 DNS 不解析；统一用 `sousuo.www.gov.cn`。
5. 翻页条目的 `pubtimeStr` 可能为 `null`，用 `ptime`/`pubtime`。
6. `https://www.gov.cn/zhengce/fagui/`、`/zhengce/content/<date>/…`（凭猜的 id）均 404，正文 URL 只认 API 返回的 `url`。
