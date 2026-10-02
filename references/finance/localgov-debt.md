# localgov-debt —— 地方政府债券信息平台

- 去哪找：**中国地方政府债券信息公开平台** `https://www.celma.org.cn/`（运营方：财政部指导、中央国债登记结算有限责任公司）；**数据服务 API** `https://www.governbond.org.cn:4443/api/loadBondData.action`（页面脚本里的 `dataServiceUrl`）；**财政部预算司** `http://yss.mof.gov.cn/`（地方债政策/限额/发行文件）；债券发行文件另见中国债券信息网（`../business/chinabond.com.cn.md`）。
- 什么时候用：要**地方政府债券**官方口径——债务限额/余额、月度/季度/年度发行与偿还、分地区债券余额、分券种发行数据、债券公开信息（发行/存续期/信息披露）、地方政府债券发行计划与公告、募集说明书/评级报告。
- 怎么搜：平台是 **jQuery + AJAX 站**，页面列表与图表都走 `governbond.org.cn:4443` 的 JSON 接口；直接调接口最省事（见「细节」端点表）。人看得去 `https://www.celma.org.cn/` 各栏目（`/zqsc/` 债券市场、`/ydsj/` 月度、`/jdsj/` 季度、`/ndsj/` 年度、`/zqxx/` 债券信息、`/dfzfxjh/` 发行计划、`/cxqpl/` 存续期披露）。结果形态 **JSON**（API）与 **HTML 表格 + 可导出 Excel**（页面）。
- 覆盖：全国 31 省 + 计划单列市；债务限额/余额、发行/偿还/到期月度数据、分地区指标；债券逐只公开信息（发行文件、存续期披露）。年份以平台披露为准（多数 2015 年起）。
- 门槛：平台浏览与 API **免费、无需登录、无 key**；管理端另在 `http://manage.governbond.org.cn/`（登录）。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA——`https://www.celma.org.cn/` `200/12276B`、`/zqsc/index.jhtml` `200/15448`、`/ydsj/index.jhtml` `200`、`/ndsj/index.jhtml` `200`；`GET https://www.governbond.org.cn:4443/api/loadBondData.action?dataType=ZBLIST&flag=month` `200/25330`（JSON `code:"0"`，返回指标树）；`…&flag=year` `200/35007`；`…?dataType=FDQYDZB&zb=03&monthSpan=1` `200`（31 省 `AD_CODE/AD_NAME/AMOUNT` 行）；`…?dataType=YDZB&adCode=87&monthSpan=0&zb=03` `200` 但 `data:[]`。
- 上游：中国地方政府债券信息公开平台（`celma.org.cn` / `governbond.org.cn`）；财政部预算司。

## 细节

### 一、数据 API（`https://www.governbond.org.cn:4443/api/loadBondData.action`）

全部为 **GET**，返回 `{"code":"0","data":[…]}`：

| `dataType` | 关键参数 | 含义 | 实测 |
|---|---|---|---|
| `ZBLIST` | `flag=month`/`year` | 指标树（ID/ZB_NAME/TITLE + 口径备注） | ✅ 200，month/year 均可 |
| `YDZB` | `adCode=87`、`monthSpan=N`、`zb={指标ID}` | 全国（`87`）某指标月度数据 | ⚠️ 本机该组合返回 `[]`（换 zb/monthSpan 再试） |
| `FDQYDZB` | `zb={指标ID}`、`monthSpan=N` | **分地区**同指标（省行 `AD_CODE/AD_NAME/AMOUNT`） | ✅ 200，结构正常（本期 AMOUNT 为 0） |
| `ZYZB` | `adCode=87`、`setYear={年}` | 主要指标（页面脚本） | 参数取自页面，未单独实调 |

```bash
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
# 取指标树（先看有哪些 zb ID）
curl -s -A "$UA" 'https://www.governbond.org.cn:4443/api/loadBondData.action?dataType=ZBLIST&flag=year'
# 取分地区某指标
curl -s -A "$UA" 'https://www.governbond.org.cn:4443/api/loadBondData.action?dataType=FDQYDZB&zb=03&monthSpan=1'
```

- **债券公开信息导出**（页面按钮，脚本拼参）：`GET /api/exportZqGkExcel.action?adList={逗号分隔ad} &adCode=87 &zqlx={券种} &year={发行年} &fxfs={发行方式} &qxr={起息区间} &fxqx={发行期限} &zqCode= &zqName=`（取自 `/zqsc/` 页面脚本，**未实调**）。
- 明细页跳转规律：`https://www.celma.org.cn/ydsjmx/index.jhtml?ad_code={ad}&ad_name={URL编码后的区域名}`。

### 二、平台栏目（人读）

| 栏目 | URL | 说明 |
|---|---|---|
| 债券市场 | `https://www.celma.org.cn/zqsc/index.jhtml` | 债券筛选/统计表（可导出 Excel） |
| 债券信息 | `https://www.celma.org.cn/zqxx/index.jhtml` | 逐只债券信息 |
| 月度/季度/年度数据 | `/ydsj/`、`/jdsj/`、`/ndsj/index.jhtml` | 发行/偿还/余额指标 |
| 发行计划 | `/dfzfxjh/index.jhtml` | 地方债发行计划 |
| 发行公告 | `/fxqgg/{id}.jhtml` | 发行公告 |
| 存续期披露 | `/cxqpl/` | 公开上市/披露 |
| 预决算信息公开 | `/yjsxxgk/` | 平台自披露 |

### 三、其他地方债渠道

- **财政部预算司** `http://yss.mof.gov.cn/`（✅ 200 / 5577 B）：地方债政策、限额与发行安排。
- **中国债券信息网** `chinabond.com.cn`（政府债发行/托管公告，见 `../business/chinabond.com.cn.md`）。
- **省级发行文件**（评级报告、募集说明书、法律意见书）：多为各省财政厅在 `celma` 披露栏目上传 PDF，或以省财政厅/中国债券信息网公告形式发布；按「{省}财政厅 地方政府债券 信息披露」检索后落到 PDF 原文。

## 坑

1. **主站与数据 API 分域、且 API 带非标端口**：数据在 `www.governbond.org.cn:4443`，不是 `celma.org.cn`；某些网络环境封非标端口，调不通时改浏览器抓包。
2. `YDZB` 本机返回空数组（HTTP 200）——**不能据此判定「无数据」**；应换 `zb` / `monthSpan` / `adCode` 组合或对照页面图表。
3. `FDQYDZB` 的 `AMOUNT` 对未披露月份会是 `0`（本机 2026-10 实测多省为 0），引用前确认披露期。
4. 导出 Excel 端点参数若干为下拉选择项（券种/发行方式/期限）的编码，直接手拼易错；建议在页面选定后抓真实请求。
5. 平台部分栏目是 **jQuery AJAX 渲染**，`curl` 拿到的 HTML 是空壳，真正数据必须走 JSON 接口。
6. 债券**评级报告/募集说明书**不都在 `celma`，更多散在各省财政厅与中国债券信息网；跨源比对时注明来源与披露日。
