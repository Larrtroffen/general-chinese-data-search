# mca.gov.cn —— 民政部行政区划代码

- 去哪找：**四级代码查询平台** `https://dmfw.mca.gov.cn/XzqhVersionPublish.html`；县以上静态表 `https://www.mca.gov.cn/mzsj/xzqh/{年}/{文件名}.html`；老查询平台 `http://xzqh.mca.gov.cn/`。
- 什么时候用：要**官方行政区划代码**（含乡级街道/镇/乡）；要区划「变更沿革」（新设/撤销/更名）；要县以上（省/地/县）静态代码表。
- 怎么搜：四级平台两个接口（均 `dmfw.mca.gov.cn`，GET/POST 表单，**无需登录**）——
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # ① 行政区划树（逐级）：code=父级代码（顶层用 0），maxLevel=5 可下钻到乡级
  curl -s -A "$UA" 'https://dmfw.mca.gov.cn/xzqh/getList?code=11&trimCode=true&maxLevel=5'
  # ② 代码检索（按名称/代码）
  curl -s -A "$UA" -X POST \
    --data 'tableName=Xzqh20251231' --data 'type=' --data 'pageNum=1' --data 'pageSize=10' \
    --data 'parentCode=' --data 'placeCode=' --data-urlencode 'title=东华门' \
    'https://dmfw.mca.gov.cn/xzqh/getCodeList'
  ```
- 覆盖：四级（省/地/县/乡）行政区划代码，**数据截止 2025-12-31**；县以上静态表 2019–2023 每年一张全量 HTML（列 `行政区划代码 | 单位名称`，不含乡级）。
- 门槛：免费，无需登录；`www.mca.gov.cn` 前置 WAF（`Server: WAF`）。
- 实测：2026-10-02，macOS（arm64），curl 8.x：`www.mca.gov.cn` 200；2023/2022/2020/2019 县以上代码表均 200（2023 表 3226 行）；`dmfw.mca.gov.cn/xzqh/getList?code=11&maxLevel=5` 返回 16 区 + 343 个乡级单位（街道 165/镇 143/乡 30/民族乡 5）；`getCodeList` POST 命中「东华门街道 110101001」；`xzqh.mca.gov.cn` HTTPS 443 超时、HTTP 200；2024/2025 县以上静态表多种命名均 404。
- 上游：民政部 `https://www.mca.gov.cn/`。

## 细节

### 可用性矩阵

| 路径 | 状态 | 现象 |
|---|---|---|
| `https://www.mca.gov.cn/` | ✅ 200 | 门户首页（WAF 前置，`Server: WAF`） |
| `https://www.mca.gov.cn/mzsj/xzqh/` | ⚠️ 200 但 1 字节 | 空壳页（无目录列表），**不能当索引用** |
| `https://www.mca.gov.cn/mzsj/xzqh/2023/202301xzqh.html` | ✅ 200 / 1.42 MB | 2023 年县以上行政区划代码（表格） |
| `https://www.mca.gov.cn/mzsj/xzqh/2022/202201xzqh.html` | ✅ 200 / 1.38 MB | 2022 年县以上代码 |
| `https://www.mca.gov.cn/mzsj/xzqh/2020/20201201.html` | ✅ 200 | 2020-12 县以上代码 |
| `https://www.mca.gov.cn/mzsj/xzqh/1980/2019/202002281436.html` | ✅ 200 | 2019-12 县以上代码 |
| `…/mzsj/xzqh/2024/…`、`…/2025/…xzqh.html` | ❌ 404 | 2024/2025 县以上静态表**未找到**（换名或未发布，见「未验证」） |
| `https://dmfw.mca.gov.cn/XzqhVersionPublish.html` | ✅ 200 | **四级代码查询平台**（数据截止 2025-12-31） |
| `http://xzqh.mca.gov.cn/` 与 `/map` | ⚠️ 仅 HTTP 200 | **HTTPS(443) 连接超时**，只能走 http；老「全国行政区划信息查询平台」（GBK、d3 地图） |

### 一、四级代码查询平台（推荐，含乡级）

入口页 `https://dmfw.mca.gov.cn/XzqhVersionPublish.html`（标题「行政区划代码」）。页面说明：

> 本库发布的行政区划代码信息包括全国省、地、县、乡**四级**行政区划建制的行政区划代码。数据截止日期为 **2025 年 12 月 31 日**。

#### ① 行政区划树（逐级）

```bash
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
# code=父级代码（顶层用 0），maxLevel=5 可下钻到乡级
curl -s -A "$UA" 'https://dmfw.mca.gov.cn/xzqh/getList?code=11&trimCode=true&maxLevel=5'
```

返回嵌套 JSON：

```
data
 .code .name .level .type .children[]
   11     北京市  1     直辖市  [ 110101 东城区 L3 市辖区, … ]
                                 110101001 东华门街道 L4 街道, …
```

- `trimCode=true`：父代码不补零（`11` 而非 `110000`）。
- 实测：`code=11` → 16 个区；**乡级合计 343 = 街道 165 + 镇 143 + 乡 30 + 民族乡 5**（2025-12-31）。
- 普通省份会多一层「地级市（level 2）」，直辖市无城市层。

#### ② 代码检索（按名称/代码）

```bash
curl -s -A "$UA" -X POST \
  --data 'tableName=Xzqh20251231' --data 'type=' --data 'pageNum=1' --data 'pageSize=10' \
  --data 'parentCode=' --data 'placeCode=' --data-urlencode 'title=东华门' \
  'https://dmfw.mca.gov.cn/xzqh/getCodeList'
```

返回：

```
data[].name=东华门街道  code=110101001  level=4  parentName=东城区
       namePath=北京市/东城区/东华门街道
```

- `tableName=Xzqh20251231` 为当前版本（页面源码中的常量）。
- 传 `tableName=Xzqh20241231` / `Xzqh20231231` 亦返回相同结果 → **历史版本是否真的可查未验证**（疑似恒用当前库）。

### 二、县以上行政区划代码（静态表，2019–2023）

每年一张全量 HTML 表，列：`行政区划代码 | 单位名称`，覆盖省/地/县（不含乡级）。

```bash
curl -s -A "$UA" 'https://www.mca.gov.cn/mzsj/xzqh/2023/202301xzqh.html' -o 2023xzqh.html
# 已实测：3226 个 <tr>，含 110000 北京市 / 110101 东城区 / …
```

已确认可用的年份与地址：

```
2019-12  https://www.mca.gov.cn/mzsj/xzqh/1980/2019/202002281436.html   (3215 行)
2020-12  https://www.mca.gov.cn/mzsj/xzqh/2020/20201201.html
2022     https://www.mca.gov.cn/mzsj/xzqh/2022/202201xzqh.html
2023     https://www.mca.gov.cn/mzsj/xzqh/2023/202301xzqh.html
```

### 三、其他有用页

| 内容 | URL | 状态 |
|---|---|---|
| 县以下（乡级）代码**变更情况** | `https://www.mca.gov.cn/mzsj/xzqh/2025/202402xzqh.html` | ✅ 200（2024 年变更表，含「新设街道/撤销/更名」与批准文号） |
| 季度民政统计数据（含全国乡级总数） | `https://www.mca.gov.cn/mzsj/xzqh/2025/2025{01..04}tjsj.htm` | ✅ 200（Q2 实测：镇 21482 / 乡 6988 / 民族乡 956 / 苏木 153 / 街道 9135） |
| 民政数据栏目 | `https://www.mca.gov.cn/n156/n2679/index.html` | ✅ 200（列季度统计） |
| 行政区划代码栏目页 | `https://www.mca.gov.cn/n156/n186/index.html` | ⚠️ 200，但省份列表由 JS 渲染，curl 抓不到 |

## 坑

1. `www.mca.gov.cn` 前置 WAF，`-I`/`-i` 会看到 `Server: WAF`；`/mzsj/xzqh/` 只回 1 字节空页，**没有目录索引**，必须知道具体年份文件名。
2. `xzqh.mca.gov.cn` **只支持 HTTP**（443 超时）——脚本里别写 https。
3. 县以上静态表**无乡级**；要乡级必须用 `dmfw.mca.gov.cn/xzqh/getList` 或年度「县以下代码变更情况」。
4. 四级平台虽无频控提示，但拉全国乡级数据量较大，建议按省逐个 `getList` 并 ≥1.5s 间隔。
5. 编码：静态表为 UTF-8；`xzqh.mca.gov.cn` 老平台为 GBK。
