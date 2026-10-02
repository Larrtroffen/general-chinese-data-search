# nhc.gov.cn —— 国家卫健委卫生统计年鉴与公报

- 去哪找：门户 `https://www.nhc.gov.cn/`；**统计信息**栏目（月报/季报/年报/公报/统计年鉴）`https://www.nhc.gov.cn/zwgk/tjxx1/ejflist.shtml`；**统计年鉴** `https://www.nhc.gov.cn/zwgk/tjnj1/ejlist.shtml`（旧路径 `/wjw/tjnj/list.shtml`）；统计信息中心 `https://www.nhc.gov.cn/mohwsbwstjxxzx/new_index.shtml`。
- 什么时候用：要**《中国卫生健康统计年鉴》**（卫生机构/人员/床位/经费/居民健康指标）；要**卫生健康事业发展统计公报**；要全国医疗服务月度情况；要各省卫生统计口径。
- 怎么搜：curl 直取被**瑞数信息 JS 挑战 WAF** 拦（一律 **412**），须用真实浏览器渲染后取；拿到 PDF/HTML 后再抽取：
  ```bash
  # 本机实测：直连即 412，无 JS 无法通过；改用 browser 打开下列栏目页
  curl -s -o /dev/null -w '%{http_code}\n' 'https://www.nhc.gov.cn/zwgk/tjxx1/ejflist.shtml'
  ```
  年鉴为 PDF（如《中国卫生健康统计年鉴》`…/mohwsbwstjxxzx/tjtjnj/202501/…/files/<id>.pdf`，URL 见「细节」）；结果形态：HTML 列表 + PDF 正文。
- 覆盖：统计年鉴历年（纸质版扫描/PDF，实测检索结果含 2004–2015 及近年）；统计公报年度；全国医疗服务情况月报。
- 门槛：免费；但**全站前置 WAF（412，需浏览器）**——无头 curl 取不到。
- 实测：2026-10-03，curl 8.x 桌面 UA：`http://www.nhc.gov.cn/` → **412**（3,408 B）、`https://www.nhc.gov.cn/` → **412**（3,503 B）、`https://www.nhc.gov.cn/wjw/tjnj/list.shtml` → **412**（3,505 B）；响应体含 `<meta id="pKiu3fgdT8br" content="l1_zh…">` 的 JS 挑战脚本。上述栏目 URL 来自搜索引擎快照（未本机直连验证）。
- 上游：国家卫生健康委员会 `https://www.nhc.gov.cn/`。

## 细节

### 栏目与文件（来自检索结果，本机被 412 拦，未逐一验证）

| 内容 | URL |
|---|---|
| 统计信息总栏（月报/公报/季报/年报/年鉴） | `https://www.nhc.gov.cn/zwgk/tjxx1/ejflist.shtml` |
| 统计年鉴 | `https://www.nhc.gov.cn/zwgk/tjnj1/ejlist.shtml` |
| 统计年鉴（旧路径） | `https://www.nhc.gov.cn/wjw/tjnj/list.shtml` |
| 统计信息中心（月/季/年报发布） | `https://www.nhc.gov.cn/mohwsbwstjxxzx/new_index.shtml` |
| 《中国卫生健康统计年鉴》PDF 示例 | `https://www.nhc.gov.cn/mohwsbwstjxxzx/tjtjnj/202501/8193a8edda0f49df80eb5a8ef5e2547c/files/1740022743894_10341.pdf` |
| 2015 中国卫生统计年鉴 | `https://www.nhc.gov.cn/mohwsbwstjxxzx/c100228/201606/0db443cfc20b46ddb7f7851de3e00372.shtml` |

- 年鉴栏目历史命名：`中国卫生统计年鉴`（≤2015）→ `中国卫生健康统计年鉴`（近年）。
- 备选获取：各省卫健委转载、统计年鉴共享平台、知网/万方（见 `../stats/cnki-data.md`、`../academic/`）。

## 坑

1. **412 不是封 IP，而是要执行 JS 挑战**；换 UA/加 Referer 均无效（实测三种姿势全 412），必须浏览器或带 JS 引擎的抓取器。
2. 统计年鉴多为**扫描图片/PDF**，无结构化表；数值使用前须核对年份口径（「卫生」→「卫生健康」名称变更）。
3. 栏目路径改过版（`/wjw/tjnj/` → `/zwgk/tjnj1/`），旧链接可能仍可解析但结构不同。
4. 本站与各省卫健委数据可能不一致，正式引用以国家统计局/卫健委官方发布为准。
