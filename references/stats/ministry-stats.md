# ministry-stats —— 中央部委数据与统计栏目总表

- 去哪找：入口按部委分散，常用三类——**数据/统计栏目**（如 `https://www.mot.gov.cn/shuju/index.html`、`https://www.miit.gov.cn/gxsj/tjfx/index.html`）、**年度统计公报/年鉴**（如 `https://www.mee.gov.cn/hjzl/sthjzk/sthjtjnb/`、`http://www.moe.gov.cn/jyb_sjzl/sjzl_fztjgb/`）、**数据开放门户**（如 `https://data.moa.gov.cn/`）。全表见「细节」。
- 什么时候用：写报告要**部委口径**的年度/月度数字（财政收支、教育、卫生、能源、交通、邮政、民航、林草、医保、环境、水利…）；要统计公报/年鉴原文与 PDF/xls；国家统计局口径不够细、或需要行业主管部门数据时。
- 怎么搜：两部——**① 栏目浏览**：多数是「栏目首页 → 按年/月列表 → 详情页（HTML 表格或附件）」的静态结构，改 URL 年份即可直取（如教育统计 `…/jyb_sjzl/moe_560/2024/`）；**② 站内全文检索**（找历史文件最有效）：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # 财政部 WAS5 检索（TRS，返回 HTML 结果页）
  curl -s -A "$UA" 'http://search.mof.gov.cn/was5/web/search?searchword=财政收入&channelid=288654'
  # 自然资源部 WAS5；国家医保局 jrobot（以下两条仅提取自页面，未单独实测）
  curl -s -A "$UA" 'http://search.mnr.gov.cn/was5/web/search?searchword=矿产资源&channelid='
  curl -s -A "$UA" 'http://www.nhsa.gov.cn/jrobot/search.do?webid=1&pg=10&p=1&tpl=1&category=&q=统计公报'
  ```
  结果形态：栏目页与公报多为 **HTML**（表格/正文），部分为 **PDF/xls/xlsx 附件**；住建部附件经 `api-gateway` 网关加密下载；工信部列表由 CMS 接口渲染（**均需浏览器会话，curl 拿不到列表**）。
- 覆盖：年度统计年鉴/公报/年报（各站年份跨度不一，最新多为 2025/2026）+ 月度/季度快报；全国口径为主，部分分省（教育、环境、海关等）；粒度到行业大类与指标。
- 门槛：**免费、无需登录**为主；少数站前置 **瑞数动态 JS 挑战**（卫健委、海关总署）或 JS cookie 挑战（人社部），curl 返回 412/JS 页，需浏览器。
- 实测：2026-10-03，macOS（arm64），curl 8.x，桌面 UA（`-L` 跟随跳转、20s 超时）——15 个部委栏目 **200 ✅**（教育/财政/住建/生态环境/工信/水利/人行/交通/农业农村/邮政/自然资源/应急/民航/林草/医保）；文旅部为多级 **JS 跳转 ⚠️**；人社部 JS 挑战、卫健委/海关总署 **412 ❌**；国家能源局 `xwzx/tjsj` **404 ❌**。逐条见下。
- 上游：各部委门户（见「细节」表内链接）。

## 细节

### 一、已实测栏目总表（2026-10-03）

| 部委 | 统计/数据栏目 | 状态 | 备注（粒度 · 结构） |
|---|---|---|---|
| 教育部 | `http://www.moe.gov.cn/jyb_sjzl/` | ✅ 200 | 「文献/数据资料」频道；教育统计数据 `…/jyb_sjzl/moe_560/`（如 `/2024/` ✅）、年报公报 `…/sjzl_fztjgb/` |
| 财政部 | `https://www.mof.gov.cn/gkml/caizhengshuju/` | ✅ 200 | 财政数据栏目；站内检索 `search.mof.gov.cn/was5/web/search` |
| 住建部 | `https://www.mohurd.gov.cn/gongkai/fdzdgknr/sjfb/index.html` | ✅ 200 | 「统计数据」；附件走 `/api-gateway/jpaas-web-server/front/document/download?fileUrl=<加密串>` |
| 生态环境部 | `https://www.mee.gov.cn/hjzl/sthjzk/sthjtjnb/` | ✅ 200 | 生态环境统计年报（逐年） |
| 工信部 | `https://www.miit.gov.cn/gxsj/tjfx/index.html` | ✅ 200 | 「统计分析」；列表由 `/api-gateway/jpaas-publish-server/front/page/build/unit` 渲染 |
| 水利部 | `http://www.mwr.gov.cn/sj/` | ✅ 200 | 「数据」汇总页（锚 `#tjgb` 统计公报；子栏目如 `/sj/tjgb/dxsdtyb/`） |
| 中国人民银行 | `http://www.pbc.gov.cn/diaochatongjisi/116219/index.html` | ✅ 200 | 调查统计司：年度统计数据 `/116319/`、月度数据解读 `/116225/`、问卷调查报告 `/116227/` |
| 交通运输部 | `https://www.mot.gov.cn/shuju/index.html` | ✅ 200 | 「数据」；含运价指数 PDF `/shuju/yunjiazhishu/` |
| 农业农村部 | `https://data.moa.gov.cn/`（→`/nyb/pc/index.jsp`）；规划计划 `https://www.moa.gov.cn/gk/ghjh_1/` | ✅ 200 | 数据开放门户 + 规划计划栏目 |
| 国家邮政局 | `https://www.spb.gov.cn/gjyzj/c100276/common_list.shtml` | ✅ 200 | 「统计信息」；加载更多 `…/c100037/c100150/common_listmore.shtml?channelId=…&code=c100276` |
| 自然资源部 | `https://www.mnr.gov.cn/sj/` | ✅ 200 | 「数据」；站内检索 `search.mnr.gov.cn/was5/web/search`（页面内出现，未单独实测） |
| 应急管理部 | `https://www.mem.gov.cn/gk/tjsj/` | ✅ 200 | 「统计数据」 |
| 中国民航局 | `http://www.caac.gov.cn/XXGK/XXGK/TJSJ/` | ✅ 200 | 信息公开·统计数据（页面含 WAS5 检索、`xzqlspjg/api/v1/search/total`，均未单独实测） |
| 国家林草局 | `https://www.forestry.gov.cn/main/65/index.html` | ✅ 200 | 「林草资源」（跳 `/c/www/lczy.jhtml`） |
| 国家医保局 | `https://www.nhsa.gov.cn/col/col7/index.html` | ✅ 200 | 「统计数据」（统计公报/快报，`art/…/art_7_*.html`）；检索入口 `jrobot/search.do`（页面内出现，未单独实测） |
| 民政部 | 见本层 `mca.gov.cn.md`（`/mzsj/…` 季度统计） | ✅ | 行政区划与季度民政统计 |
| 文化和旅游部 | `https://www.mct.gov.cn/zwgk/tjsj/` | ⚠️ JS 跳转 | → `zwgk.mct.gov.cn/?classInfoId=360` → `./zfxxgkml/`（多级 `location.replace`，需浏览器） |
| 人力资源社会保障部 | `http://www.mohrss.gov.cn/SYrlzyhshbzb/zwgk/szrs/tjgb/` | ⚠️ JS 挑战 | 返回 989B JS（设置 `EO_Bot_Ssid` cookie 后才放行） |
| 国家卫生健康委 | `http://www.nhc.gov.cn/wjw/tjnj/list.shtml`（统计年鉴） | ❌ 412 | 瑞数动态防护（`$_ts` 挑战脚本），curl 不可达 |
| 海关总署 | 统计月报 `http://www.customs.gov.cn/customs/302249/zfxxgk/2799825/302274/index.html`；海关统计查询平台 `http://stats.customs.gov.cn/` | ❌ 412 | 同为瑞数防护；`customs.gov.cn` 与 `stats.customs.gov.cn` 均 412 |
| 国家能源局 | `https://www.nea.gov.cn/xwzx/tjsj/index.htm` | ❌ 404 | 未找到统一统计栏目；月度电力/充电设施等数据散见新闻稿 |

### 二、可直接拼 URL 的规律

- **按年**：`moe.gov.cn/jyb_sjzl/moe_560/{年}/`（教育统计）、`mee.gov.cn/hjzl/sthjzk/sthjtjnb/`（年报列表）。
- **栏目锚点**：`mwr.gov.cn/sj/#tjgb`；`pbc.gov.cn/diaochatongjisi/116219/` 下用栏目 ID（`116319` 年度 / `116225` 月度 / `116227` 调查）。
- **公报正文**：教育部 `…/sjzl_fztjgb/{YYYYMM}/t{YYYYMMDD}_{id}.html`；医保 `nhsa.gov.cn/art/{年}/{月}/{日}/art_7_{id}.html`。
- **检索参数**：WAS5 系（财政/自然资源/民航）用 `searchword=<词>&channelid=<栏目>`；jrobot（医保）用 `q=<词>&pg=<每页>&p=<页>&webid=1`。

## 坑

1. **瑞数动态防护**：卫健委、海关总署（含 `stats.customs.gov.cn`）返回 **412** 并携带 `$_ts` 挑战脚本——换 UA/加浏览器头无效，须浏览器或带 cookie 的会话。
2. **人社部**同为 JS cookie 挑战（`EO_Bot_Ssid`）；**文旅部**是多级 `location.replace` 跳转，`curl -L` 只到中转页。
3. **工信部/住建部用 `api-gateway`（jpaas）**：列表与附件由 `front/page/build/unit`、`front/document/download?fileUrl=` 渲染，`fileUrl` 为加密串，**直接拼接无效**；须先拿页面里的完整链接。
4. **国家能源局**统计入口路径反复变动（`/xwzx/tjsj/`、`/zwgk/` 均 404），别写死；其月度数据常以「数据情况」新闻稿形式发布。
5. 部委网站**改版频繁**（栏目路径 400/404 常见），引用数字务必落到**公报原文**并记标题+日期；同名栏目在不同部委下含义不同。
6. 附件多为 **PDF/xls/xlsx**：公报正文可解析，年鉴/数据表常为扫描图片或需专用阅读器的 xls；下载后注意编码（多数 UTF-8，部分老页面 GB2312）。
7. 站内检索（WAS5/jrobot）匿名可用，但**只覆盖本站**且排序按时间/相关度混杂；跨部委查同一指标请分别检索，或先用国家统计局口径兜底。
