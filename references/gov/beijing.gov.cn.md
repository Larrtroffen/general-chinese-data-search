# beijing.gov.cn —— 首都之窗市政府门户

- 去哪找：
  - 政策解读：`https://www.beijing.gov.cn/zhengce/zcjd/…`
  - 部门动态：`https://www.beijing.gov.cn/ywdt/gzdt/201901/t20190119_1826708.html`（2019-01-19"169个街乡试点"口径来源）
  - 搜索页（需浏览器渲染）：`https://www.beijing.gov.cn/so/s?qt=…&tab=all`
  - 统一搜索 JSON 接口：`POST https://www.beijing.gov.cn/so/ss/query/s`
- 什么时候用：要市级权威口径的政策解读、部门动态、新闻发布；或按关键词检索整合了各区门户/微信文章的市级搜索索引。
- 怎么搜：
  ```bash
  curl -s -m 25 -X POST 'https://www.beijing.gov.cn/so/ss/query/s' \
    -H 'Referer: https://www.beijing.gov.cn/so/s' \
    --data-urlencode 'qt=吹哨报到' --data 'page=1&pageSize=20&siteCode=1100000088'
  # → {"ok":true,"totalHits":9649,"resultDocs":[{"data":{"title","url","docDate","summary","siteLabel","dbName",…}}]}
  ```
  - **必须 POST 表单**且带 `siteCode`；GET 加查询串（`/so/ss/query/s?qt=…`）实测返回 `{"ok":false,"code":500,未知异常}`。
  - `siteCode=1100000088` = 首都之窗站码（`/so/s` 页隐藏域实测值）。该参数常被后端忽略为全站聚合 → 需要区级结果时按 `resultDocs[].data.url` 的域名自行过滤（`--filter`）。
  - **只对单关键词稳定有效**；含空格的多词 qt 常 0 结果 → 多词拆开分别检索。
  - 抓取文章页（静态 HTML，UTF-8，正文可取）：`curl -s -m 25 -A 'Mozilla/5.0 …' 'https://www.beijing.gov.cn/ywdt/gzdt/201901/t20190119_1826708.html'`
  - 工具：`scripts/bjgov_search.py 关键词 [--page N] [--filter <域名>]`（本 skill），封装的即上述 POST 调用。
- 覆盖：市级（北京市政府门户）政策解读、部门动态、新闻发布；统一搜索索引跨全站聚合（含各区门户、微信公众号文章）。
- 门槛：免费、免登录；搜索**仅 POST + 单关键词**；`api.so-gov.cn` 旧域名对批量请求封出口 IP，须保持低频。
- 实测：2026-10-02，`POST https://www.beijing.gov.cn/so/ss/query/s`（`qt=吹哨报到&page=1&pageSize=20&siteCode=1100000088`）→ `{"ok":true,"totalHits":9649,…}` ✅ 可用；GET 变体返回 `ok:false,code:500`。
- 上游：<https://www.beijing.gov.cn/>

## 细节

### URL 形态

- 政策解读：`https://www.beijing.gov.cn/zhengce/zcjd/…`
- 部门动态：`https://www.beijing.gov.cn/ywdt/gzdt/201901/t20190119_1826708.html`
- 搜索页（需浏览器渲染）：`https://www.beijing.gov.cn/so/s?qt=…&tab=all`

### 搜索表单隐藏域（区级门户一致）

区级门户（如朝阳 bjchy.gov.cn）的「政策文件检索」表单实际 action 就是首都之窗统一搜索：隐藏域 `siteCode=1100000088`、`tab=zcfg`、`docWz=<区名>政府`、`keyPlace` 0 全文/1 标题。

### 限流与通道备注

- 同后端旧域名 `api.so-gov.cn/query/s` 对**批量/连续请求封出口 IP**（`code -101`）——勿扫描 siteCode、保持低频；`www.beijing.gov.cn/so/ss/query/s` 当时未封（2026-10-01 记录）。
- 该搜索索引里连微信公众号文章也在（结果 url 可能是带 `sn` 的 **mp.weixin 永久链接**）——可作绕过搜狗签名链接时效的一条补充通道。

### 已知口径要点（本类课题）

- "作为2018年全市'1号改革课题'，'街乡吹哨、部门报到'在16个区169个街乡开展试点，占总数的51%。"
- 只给数量不给名单——作市级口径引文源，不是名单源。

## 坑

1. 搜索 **必须 POST 表单**，GET 查询串返回 500。
2. 多词查询常 0 结果，须拆词。
3. `siteCode` 常被忽略为全站聚合，需按 URL 域名自行过滤。
4. `api.so-gov.cn` 批量请求封 IP，勿扫描 siteCode。
