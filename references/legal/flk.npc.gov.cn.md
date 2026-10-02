# flk.npc.gov.cn —— 国家法律法规数据库

全国人大常委会办公厅主办的**官方**法律法规全文库：宪法、法律、行政法规、监察法规、地方性法规、司法解释，含**官方 Word/PDF 原件下载**。是引用法条原文的首选一手来源（优于商业库）。

⚠️ 2024–2025 已**改版为 Vue SPA**：旧的 `/api/?type=…` 接口**已废弃**（现返回 SPA 的 HTML 壳），新接口全部在 `/law-search/*` 下，**POST JSON**。

- 去哪找：
  - 站点：`https://flk.npc.gov.cn/`
  - 检索主接口：`POST /law-search/search/list`
  - 枚举：`GET /law-search/search/enumData`
  - 详情：`GET /law-search/search/flfgDetails?bbbs=<id>`
  - 原件下载：`GET /law-search/download/pc?format=docx|pdf&bbbs=&fileId=`
- 什么时候用：要宪法/法律/行政法规/监察法规/地方性法规/司法解释的**法条原文**，或需**官方 Word/PDF 原件**（版式、红头、公报核验）；引用法条原文的首选一手来源。
- 怎么搜：`POST /law-search/search/list`，JSON body（字段一个都不能少，见「细节」）；结果形态 JSON（命中 `rows[]`）；站点为同源 API（axios `baseURL:""`），无需 Token/Cookie 即可检索与下载。
  ```bash
  curl -s -m 20 \
    -H 'Content-Type: application/json;charset=utf-8' \
    -H 'Referer: https://flk.npc.gov.cn/' \
    -X POST \
    --data '{"searchRange":1,"sxrq":[],"gbrq":[],"searchType":2,"sxx":[],"gbrqYear":[],"flfgCodeId":[],"zdjgCodeId":[],"searchContent":"安全生产","orderByParam":{"order":"-1","sort":""},"pageNum":1,"pageSize":5}' \
    'https://flk.npc.gov.cn/law-search/search/list'
  ```
- 覆盖：宪法、法律、行政法规、监察法规、地方性法规、司法解释；含已废止/已修改/尚未生效（时效性字段 `sxx`）；提供官方 Word/PDF 原件。
- 门槛：免费、免登录、**无需 Token/Cookie**。
- 实测：2026-10-02，macOS，curl 8.x。`searchContent=安全生产` 的检索 → `total=1170`；`sxx:[3]` → 707，`sxx:[1]` → 96（返回行的 `sxx` 与筛选一致）。`GET /` → **200**，552 B SPA 壳（`<div id="app">`）。可用性矩阵与各端点观察见「细节」。接口地址由当日 SPA bundle（`assets/index-BZ9XHUiV.js`、`assets/index-DvwoonSa.js`）反查并经实际请求验证。
- 上游：`https://flk.npc.gov.cn/`（全国人大常委会办公厅）

## 细节

### 可用性矩阵（本机实测）

| 端点 | 状态 | 现象 |
|---|---|---|
| `https://flk.npc.gov.cn/` | ✅ | 200，552 B SPA 壳（`<div id="app">`） |
| `https://flk.npc.gov.cn/api/?type=xzfg&…`（旧接口） | ❌ | 200 但返回 SPA HTML（`text/html`），**不再是 API** |
| `GET /law-search/search/enumData` | ✅ | 200 JSON（分类/制定机关枚举） |
| `POST /law-search/search/list` | ✅ | 200 JSON，检索主接口 |
| `GET /law-search/search/flfgDetails?bbbs=<id>` | ✅ | 200 JSON，含 OSS 文件路径 |
| `GET /law-search/download/pc?format=docx\|pdf&bbbs=&fileId=` | ✅ | 200 JSON，返回**预签名 OSS 直链** |
| `GET /law-search/download/mobile?…` | ⚠️ | 302（跳转文件） |
| `GET /law-search/index/captchaImage` | ⚠️ | 存在验证码接口（纠错/举报用，检索不需要） |

### 1. 检索：POST /law-search/search/list

请求体（JSON）：

```json
{
  "searchRange": 1,
  "sxrq": [], "gbrq": [], "sxx": [], "gbrqYear": [],
  "flfgCodeId": [], "zdjgCodeId": [],
  "searchType": 2,
  "searchContent": "安全生产",
  "orderByParam": {"order": "-1", "sort": ""},
  "pageNum": 1,
  "pageSize": 20
}
```

| 字段 | 含义 / 取值 |
|---|---|
| `searchContent` | 关键词（URL 无需编码，直接放 JSON 字符串） |
| `searchRange` | **1=标题，2=正文** |
| `searchType` | **1=精确，2=模糊** |
| `orderByParam` | **对象** `{"order":"-1","sort":""}`；`-1`=默认排序。写成字符串会 500（最容易踩的坑） |
| `pageNum` / `pageSize` | 翻页；实测 `pageNum=2` 返回不同结果 |
| `flfgCodeId` | 法律法规分类 codeId 数组（取自 `enumData.data.flfgfl`）；实测 `[110]` → total 2 |
| `zdjgCodeId` | 制定机关 codeId 数组（取自 `enumData.data.zdjgfl`） |
| `sxx` | 时效性数组：**3=有效，1=已废止，2=已修改，4=尚未生效** |
| `gbrqYear` | 公布年份数组 |
| `sxrq` / `gbrq` | 施行/公布日期区间数组 |

响应：

```
{ "code":200, "msg":"查询成功", "total":1170, "searchType":2, "searchContent":null,
  "rows": [ { … } ] }
```

| rows[] 字段 | 含义 |
|---|---|
| `bbbs` | **文档唯一 id**（32 位十六进制），详情/下载都用它 |
| `title` | 标题（命中词包在 `<em class='highlight'>` 里，需剥离标签） |
| `gbrq` / `sxrq` | 公布日期 / 施行日期（`YYYY-MM-DD`） |
| `sxx` | 时效性（1/2/3/4，见上） |
| `flxz` | 法律性质（法律/行政法规/地方性法规/司法解释…） |
| `zdjgName` | 制定机关名称 |
| `flfgCodeId` / `zdjgCodeId` | 分类 / 制定机关 编码 |
| `titleHightLightList` | 标题分词+高亮布尔数组 |
| `score` | 相关度 |

### 2. 枚举：GET /law-search/search/enumData

```bash
curl -s 'https://flk.npc.gov.cn/law-search/search/enumData'
```

`data.flfgfl`（法律法规分类，一级 codeId）：宪法 **100**、法律 **101**、行政法规 **201**、监察法规 **220**、地方法规 **221**、司法解释 **311**；`data.zdjgfl`（制定机关）：全国人大及其常委会 **90**、国务院 **120**、国家监察委 **130**、最高法 **140**、最高检 **150**、地方人大及其常委会 **165** 等。

### 3. 详情：GET /law-search/search/flfgDetails?bbbs=<id>

```bash
curl -s 'https://flk.npc.gov.cn/law-search/search/flfgDetails?bbbs=ff8081817a66b816017a7956b7db0ad4'
```

`data` 字段：`bbbs`、`title`、`flxz`、`zdjgName`、`gbrq`、`sxrq`、`sxx`、`content`（**条文目录树**：`{id,parentId,title,index,children}`）、`lsyg`（历史沿革/历次版本）、`xgzl`（相关资料）、`xgwj`（相关文件）、`xfFlag`、`ossFile`：`{ossWordPath, ossPdfPath, ossWordOfdPath, ossPdfOfdPath, ossWordOfdSize, ossPdfOfdSize}`。缺 `bbbs` 报 `Required request parameter 'bbbs' …`。

### 4. 原件下载：GET /law-search/download/pc

```bash
curl -s -H 'Referer: https://flk.npc.gov.cn/' \
  'https://flk.npc.gov.cn/law-search/download/pc?format=docx&bbbs=ff8081817a66b816017a7956b7db0ad4&fileId='
# format=pdf 同理
```

返回：

```json
{"code":200,"msg":"操作成功","data":{
  "urlIn":"http://172.16.220.27:38080/law-search/file/download?…",   // 内网地址，不可用
  "url":"https://flkoss.obs-bj2.cucloud.cn/prod/…/xxx.docx?X-Amz-…&X-Amz-Expires=3600" }}
```

- 用 `data.url` 直连华为云 OBS（预签名，**有效期 3600 s**）；实测下载得到 36 238 B 的 `Microsoft Word 2007+` 文件（`application/vnd.openxmlformats-officedocument.wordprocessingml.document`）。
- `fileId` 用于"相关文件"场景；主文档传空即可（本次实测 `fileId=` 有效）。
- `data.urlIn` 是 172.16 内网地址，**本机不可达，别用**。

## 坑

1. `orderByParam` 必须是对象；写成字符串 → `{"code":500,"msg":"系统异常"}`。
2. 请求体缺字段 → 500「系统异常」（无字段级报错提示），照上面模板照抄。
3. 旧 `/api/` 与 `/api/detail` 已废，返回 HTML 壳，别浪费时间。
4. `title` 含 `<em class='highlight'>` 高亮标签，入库前要清洗。
5. 下载 URL 是**预签名直链、1 小时过期**，不要缓存长期使用，随时重新请求 `download/pc`。
6. 未实测：`highSearch/highSearch`（高级检索）、`search/hitDisplay`（正文命中高亮）、`xgzlDetails`/`xgwjDetails`。
