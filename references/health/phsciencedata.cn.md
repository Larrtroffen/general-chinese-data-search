# phsciencedata.cn —— 公共卫生科学数据中心

- 去哪找：门户 `https://www.phsciencedata.cn/Share/`（注意 `/Share/` 路径，HTTP 会 301 到 HTTPS）；资源目录 `https://www.phsciencedata.cn/Share/ky_sjml.jsp`；资源检索 `https://www.phsciencedata.cn/Share/advancedSearchDataSet.jsp`；站内检索 `https://www.phsciencedata.cn/Share/jsp/PublishManager/AllSearchNew.jsp?keyword=<词>`。
- 什么时候用：要**公共卫生专题数据库**（法定报告传染病、中国健康与营养调查、中国老年人口健康状况调查、青少年健康危险行为、人体重要寄生虫病、食品营养成分、2002 居民营养与健康状况调查…）；要疾控口径的传染病分类数据。
- 怎么取：老式 JSP 站点，无 JSON API，走页面 + 相对链接（**UTF-8**）——
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  curl -s -L -A "$UA" 'https://www.phsciencedata.cn/Share/jsp/PublishManager/AllSearchNew.jsp?keyword=%E8%82%BF%E7%98%A4'   # 站内检索
  curl -s -L -A "$UA" 'https://www.phsciencedata.cn/Share/edtShareNew.jsp?id=39101'                                      # 数据集详情
  ```
  结果形态：HTML（JSP 渲染）；数据集详情 = `edtShareNew.jsp?id=<数字>`。
- 覆盖：专题数据库按病类/主题组织（传染病分甲乙丙类、慢性病、营养、环境、职业、地方病等）；条目含时间范围/空间范围；北京市法定传染病报告情况按月（实测列表见 2025-09 → 2026-02）。
- 门槛：浏览免费；**下载/申请需注册登录**。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA）：`https://www.phsciencedata.cn/` 200（304 B，JS 跳 `http://www.phsciencedata.cn/Share/`）；`https://www.phsciencedata.cn/Share/` 200（76,698 B，`<title>公共卫生科学数据中心`）；`/Share/ky_sjml.jsp` 200（61,134 B，`<title>资源目录-公共卫生科学数据中心`）；`/Share/advancedSearchDataSet.jsp` 200（16,364 B，`<title>资源检索 - 公共卫生科学数据中心`）；`/Share/jsp/PublishManager/AllSearchNew.jsp?keyword=肿瘤` 200（13,328 B，`<title>站内检索`）；`/Share/edtShareNew.jsp?id=39101` 200（109,412 B，`<title>数据市场 -公共卫生科学数据中心`）。
- 上游：公共卫生科学数据中心（挂「国家人口健康科学数据中心 / 国家卫生健康委员会」）；门户见 `ncmi.cn.md`。

## 细节

### 入口与检索路径

| 用途 | URL | 实测 |
|---|---|---|
| 门户（首页） | `https://www.phsciencedata.cn/Share/` | ✅ 200 |
| 资源目录 | `/Share/ky_sjml.jsp` | ✅ 200 |
| 资源检索（高级） | `/Share/advancedSearchDataSet.jsp` | ✅ 200 |
| 站内检索 | `/Share/jsp/PublishManager/AllSearchNew.jsp?keyword=<词>` | ✅ 200 |
| 数据集详情 | `/Share/edtShareNew.jsp?id=<数字>` | ✅ 200 |
| 登录/注册 | `/Share/login.jsp`、`/Share/userRegister.jsp` | — |
| 英文版 | `/Share/en/index.jsp` | — |

- 高级检索表单字段：`searchContion`（关键词）；提交函数 `sharch()`（页面内 JS，取 `#text` 值）。
- 首页专题示例：中国健康与营养调查数据库、中国老年人口健康状况调查数据库、2002 中国居民营养与健康状况调查数据库、全国人体重要寄生虫病现状调查数据库、食品营养成分、法定报告传染病（甲乙/丙类）等。

## 坑

1. **必须带 `/Share/` 前缀**：`/PublishManager/…` 直接访问 404；站内 JS 用 `window.location.href="/Share/jsp/PublishManager/…"`。
2. 同一路径 HTTP 会 301 到 HTTPS，脚本里统一用 `https://` 并加 `-L`。
3. 无 API、无结构化表；结果是 JSP 页面，批量取数需逐条抓 `edtShareNew.jsp?id=`。
4. 站内检索页返回的**结果可能由 JS/异步填充**，curl 只拿到壳（实测关键词「肿瘤」结果链接为 0）。
5. 站点与 `ncmi.cn`（国家人口健康科学数据中心）互链、主题有重叠，取数前先判口径归属。
