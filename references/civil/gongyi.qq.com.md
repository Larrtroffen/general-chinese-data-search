# gongyi.qq.com —— 腾讯公益乐捐项目库

- 去哪找：**腾讯公益** `https://gongyi.qq.com/`；乐捐**项目列表** `https://gongyi.qq.com/succor/project_list.htm`；**项目详情** `https://gongyi.qq.com/succor/detail.htm?id=<项目ID>`；移动端 `https://ssl.gongyi.qq.com/m/weixin/index2_gzzh.htm`。
- 什么时候用：要**腾讯公益平台在筹/已结项公益项目**（名称、发起机构、目标额/已筹额、捐赠人次、进展）、按**状态/领域（s_tid 分类）/发布方**筛项目；做互联网募捐项目监测。
- 怎么搜：公开项目页为 HTML（`乐捐项目列表`、`乐捐-项目详情`）；列表数据由 `gongyi.succor.list.v3.js` 调 **JSON 接口**（前端反查所得）：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
  # 按分类（免关键词）
  curl -s -A "$UA" -H 'Content-Type: application/json; charset=utf-8' \
    -H 'Origin: https://gongyi.qq.com' -H 'Referer: https://gongyi.qq.com/succor/project_list.htm' \
    -X POST -d '{"s_status":1,"s_tid":"73","page":1,"page_size":10,"cate_id":"73"}' \
    'https://ssl.gongyi.qq.com/gygw-app/ed/project_es_search_pc/ProjectSearchByClass'
  # 按关键词
  curl -s -A "$UA" -H 'Content-Type: application/json; charset=utf-8' \
    -H 'Referer: https://gongyi.qq.com/succor/project_list.htm' \
    -X POST -d '{"page":1,"page_size":10,"key_word":"教育"}' \
    'https://ssl.gongyi.qq.com/gygw-app/ed/project_es_search_pc/ProjectSearchByKeyword'
  ```
  请求体字段（JS 内 `_parData`）：`s_status`（状态，默认 1）、`s_tid`（领域，默认 "73"）、`s_puin`（发布者）、`s_fid`、`s_key`、`p`/`page`、`page_size`、`cate_id`、`key_word`/`keyword`、`project_first_code`。成功返回 `code:0` 的 `data.proj_list`。
- 覆盖：腾讯公益乐捐项目（含专项基金项目），字段含项目图、目标/已筹金额、捐赠人次与进展；平台级汇总见 `GetPlatformDonateData`；状态码映射 3→1、4/5→2、6/7/8→3（JS `stateMap`）。
- 门槛：项目页**免费、免登录**（未登录时前端会遮蔽金额/人次）；**检索 JSON 接口 curl 直连被拒**（见实测），实际取用建议浏览器/带会话。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA，20 s 超时）——`GET https://gongyi.qq.com/` → **200**，1 685 B（Vue SPA 壳，含 `ssl.gongyi.qq.com` 与 `gygw-app/ed/proj_data_agg/GetPlatformDonateData`）；`GET …/succor/project_list.htm` → **200**，21 421 B，`<title>乐捐项目列表_腾讯公益</title>`；`GET …/succor/detail.htm?id=1` → **200**，59 864 B，`<title>乐捐-项目详情</title>`；`GET …/gygw-app/ed/proj_data_agg/GetPlatformDonateData` → **200**，`{"code":0,"data":{"total_data":{}}}`（空，疑需参数）；`POST …/gygw-app/ed/project_es_search_pc/ProjectSearchByClass`、`…/ProjectSearchByKeyword` → **200**，`{"code":30800001,"msg":"param invalid"}`（多次修正 body/头后仍被拒）。
- 上游：腾讯公益 `https://gongyi.qq.com/`；列表 JS `https://gongyi.qq.com/static/tnews/4760e2a7-f854-42be-8151-d9517cd8e9a7/gongyi.succor.list.v3.js`。

## 细节

- 列表页脚本 `gongyi.succor.list.v3.js` 内含两个 ES 检索端点：`project_es_search_pc/ProjectSearchByClass`（按领域）与 `project_es_search_pc/ProjectSearchByKeyword`（有 `key_word` 时切此端点并清空 `s_tid`）。
- 项目详情页模板 `detail.htm?id=<%=_vo.id%>`；列表项渲染 `item.info.phone_list_image`、金额、人次（未登录遮蔽）。

## 坑

1. **检索接口 curl 直连返 `30800001 param invalid`**：即便补齐 `Content-Type`/`Origin`/`Referer`/`X-Requested-With` 与 JS 同构 body 仍被拒——疑接口已加签或校验会话，**建议浏览器**取列表，或只抓 HTML 详情页。
2. 首页/详情为 **SPA/模板混合**，数值可能由 JS 填充；离线抓 HTML 未必含全部字段。
3. `GetPlatformDonateData` 免参返空 `total_data`，未探明所需参数。
