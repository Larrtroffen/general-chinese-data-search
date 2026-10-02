# sara.gov.cn —— 宗教活动场所名录接口

- 去哪找：**国家宗教事务局**官网 `https://www.sara.gov.cn/`；**宗教基础信息查询系统** `https://www.sara.gov.cn/resource/common/zjjcxxcxxt/`：宗教活动场所 `…/zjhdcsjbxx.html`、宗教院校 `…/zjyxjbxx.html`、宗教教职人员 `…/zjjzryxxcx.html`；数据接口主机 `https://api.sara.gov.cn/mis//web/…`。
- 什么时候用：要**全国宗教活动场所名录**（按省/市/县、宗教、派别、关键词检索；含场所名、地址、负责人）；要佛教/道教/伊斯兰教/天主教/基督教及派别字典；核对某地宗教活动场所登记信息。
- 怎么搜：场所查询走 JSON API，**匿名 GET**：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
  # ① 宗教活动场所（分页）
  curl -sS -A "$UA" --compressed \
    'https://api.sara.gov.cn/mis//web/religionPlace/list?areaCode=&factionTypeId=&keyWord=&religionTypeId=&pageNum=1&pageSize=15'
  # → 200 JSON {"code":200,"info":{"total":42440,"list":[{placeName:"广济寺",province:"北京",…}]}}
  # ② 宗教类别字典
  curl -sS -A "$UA" --compressed 'https://api.sara.gov.cn/mis//web/religion/getAllReligion?pageNum=1&pageSize=999'
  # ③ 派别字典（汉语系/藏语系/正一/全真/巴利语系…）
  curl -sS -A "$UA" --compressed 'https://api.sara.gov.cn/mis//web/faction/getAllFaction?pageNum=1&pageSize=999'
  ```
  参数：`religionTypeId`（宗教，取自②）、`factionTypeId`（派别，取自③）、`areaCode`（行政区码，页面经 `POST /mis/country/api/getRegionLevel1List` 取省）、`keyWord`、`pageNum`/`pageSize`。结果形态：**JSON**。
- 覆盖：**宗教活动场所约 42440 条**（`total:42440`），字段含 `placeName`、`province/city/town/allAddress`、`religionType`、`factionType`、`personCharge`、`siteId`；宗教类别 5 大类与派别字典；院校/教职人员查询页同体系（细粒度检索需页面交互）。
- 门槛：**免费、免登录、无 key**（场所检索）；另有 `POST /mis/country/api/getRegionLevel1List` 本机 404（区划走页面交互）。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA、Chromium 无头——`GET https://www.sara.gov.cn/` → **200**（`<title>国家宗教事务局</title>`，内容块经 `/web/block/<id>.html` 异步加载）；`GET religionPlace/list?…&pageSize=1` → **200 JSON** `{"code":200,…,total:42440}`；`GET getAllReligion?pageSize=999` → 200，返回佛教/道教/伊斯兰教/天主教/基督教；浏览器打开 `…/zjhdcsjbxx.html` 实测 XHR `POST api.sara.gov.cn/mis//web/religionPlace/list`、`GET …/religion/getAllReligion`、`GET …/faction/getAllFaction`。
- 上游：<https://www.sara.gov.cn/>（国家宗教事务局，现由中央统战部管理）；相关口径另见 `../culture/zytzb.gov.cn.md`。

## 细节

### 查询系统入口

| 系统 | URL |
|---|---|
| 宗教活动场所基本信息 | `/resource/common/zjjcxxcxxt/zjhdcsjbxx.html` |
| 宗教院校基本信息 | `/resource/common/zjjcxxcxxt/zjyxjbxx.html` |
| 宗教教职人员信息查询 | `/resource/common/zjjcxxcxxt/zjjzryxxcx.html` |
| 政策法规 | `/web/xxgk/flfg/`、`/web/xxgk/bmgz/index.html`、`/web/xxgk/gfxwj/index.html` |
| 要闻 | `/web/ywdt/index.html` |

- 场所 API 返回字段：`id`、`siteId`、`placeName`、`allAddress`、`province/city/town`、`regionCode`（如 `AREA-101010102`）、`religionType`/`religionTypeId`、`factionType`/`factionTypeId`、`personCharge`、`createTime/updateTime`。
- 官网为前后端分离（页面 `hunlan` 模板 + `api.sara.gov.cn` 数据域），列表页 HTML 不含数据。

## 坑

1. 接口路径有**双斜杠** `mis//web/…`，需原样保留。
2. `areaCode` 为内部区划码（`AREA-…`），按县检索要先取得对应码；区划接口本机未打通，建议按省名/关键词先粗筛。
3. 宗教院校、教职人员页的检索接口未在页面初始加载触发，需在浏览器内操作后抓 XHR；本卡仅确证场所接口。
4. 场所信息为**登记信息快照**，`updateTime` 参差（部分为 `null`），引用时注明取数日期。
5. 国家宗教事务局政务职能已并入中央统战部，重大政策以 `zytzb.gov.cn` 为准。
