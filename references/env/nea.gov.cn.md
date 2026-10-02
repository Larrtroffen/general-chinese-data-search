# nea.gov.cn —— 能源月度数据与统计

- 去哪找：国家能源局官网 `https://www.nea.gov.cn/`；站内检索 `https://www.nea.gov.cn/search.htm?kw=<关键词>`；检索数据接口 `POST https://www.nea.gov.cn/was5/web/conwebsite/getNewsFromAllData`。
- 什么时候用：要**能源行业主管口径**的月度数据——电力/用电量、可再生能源装机与发电、绿证核发与交易、电动汽车充电设施、油气产量等；这些多以「国家能源局发布…数据」新闻稿形式发布（如「2026年8月全国可再生能源绿色电力证书核发及交易数据」）。
- 怎么搜：站内检索走 WAS5 的 JSON 接口（匿名，POST）：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  curl -sS -A "$UA" -e 'https://www.nea.gov.cn/search.htm' -X POST \
    --data 'keyword=电力数据&pageNo=1&pageSize=10' \
    'https://www.nea.gov.cn/was5/web/conwebsite/getNewsFromAllData'
  ```
  返回 **JSON**：`{"code":200,"content":{"result":[{"title":…,"url":…,"publishDate":…}]}}`；文章正文是 HTML（`https://www.nea.gov.cn/YYYYMMDD/<hash>/c.html`）。
- 覆盖：全国 · 月度（电力/绿证/充电设施等）+ 不定期行业统计 · 文章级；分省数据散见新闻稿与各省能源局。
- 门槛：**免费、匿名、无需 key**。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA）——`https://www.nea.gov.cn/` → 200（108,833 B）；`/zwgk/index.htm` → **404**（政务公开改版）；站内检索页 `search.htm?kw=电力数据` → 200 但结果由 JS 渲染；`/was5/web/nyj/js/search1.js` 暴露 `dataUrl:'/was5/web/conwebsite/getNewsFromAllData'`；`POST` 该接口（`keyword=电力`）→ 200 `text/plain`，`{"code":200,"content":{"result":[…]}}`。
- 上游：国家能源局（综合司/各业务司）；月度数据另见国家统计局能源口径（[`../stats/data.stats.gov.cn.md`](../stats/data.stats.gov.cn.md)）与中电联（未收）。

## 细节

- 首页数据类新闻标题模板：「国家能源局发布 YYYY年M月全国可再生能源绿色电力证书核发及交易数据」「YYYY年M月全国电动汽车充电设施数据情况」。
- 站内检索三套实现并存：`2024sesrch.js?V1`、`was5/nyj/js/search1.js`（`dataUrl` 指向 `getNewsFromAllData`）与 `/sites-search/common/json/result.js`，后两者本机只验证了前者。
- 分省/分行业电力数据更全的官方来源是**中国电力企业联合会**（`cec.org.cn`）与国家统计局；能源平衡表/年鉴见《中国能源统计年鉴》（CNKI 口径，见 [`../stats/cnki-data.md`](../stats/cnki-data.md)）。

## 坑

1. **没有统一「数据/统计」栏目**：`/xwzx/tjsj/`、`/zwgk/index.htm` 等路径均 404；能源数据以新闻稿散布，必须用站内检索或外部搜索聚合。
2. 检索结果 JSON 只随 `keyword/pageNo/pageSize` 三个参数（本机验证），不要再套旧 TRS 的 `searchword/channelid`。
3. 检索接口返回 `text/plain` 而非 `application/json`，但内容是 JSON，解析按 JSON 处理即可。
4. 新闻稿里的数字**有修订**（初步统计 → 最终核定），引用要记文章标题与日期，并优先取后续修订稿。
5. 站内检索默认按时间/相关度混杂，别用命中数当统计量。
