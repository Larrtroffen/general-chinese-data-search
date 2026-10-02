# ipe.org.cn —— 企业环境监管记录

- 去哪找：公众环境研究中心（IPE·蔚蓝地图）`https://www.ipe.org.cn/`；数据服务说明 `https://www.ipe.org.cn/about/DataServices.html`；企业环境监管记录检索 `https://www.ipe.org.cn/IndustryRecord/Regulatory.html`；数据介绍 `/IndustryRecord/DataIntro.aspx`；供应链 CITI/CATI 与下载 `/GreenSupplyChain/CITI.html`、`/GreenSupplyChain/download.html?isfile=1`；地图类入口 `/AirMap_fxy/AirMap.html?q=1`、`/MapPowerStation/PowerStationV2.html`。
- 什么时候用：要**企业层面的环境监管记录**（环境处罚/限停产/自动监测超标/监督性监测、政府信用等级、绩效分级、正面清单），或品牌供应链环境表现（CITI/CATI/碳数据披露）；做企业环保合规、ESG、供应链风险扫描。
- 怎么搜：站点为 ASP.NET + jQuery，数据接口集中在 `/data_ashx/GetAirData.ashx`，用 `xx=` 选择命令：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # 省份/行业等下拉项（匿名可）
  curl -sS -A "$UA" -e 'https://www.ipe.org.cn/IndustryRecord/Regulatory.html' \
    -X POST -d 'cmd=getprovinces&countryId=1' \
    'https://www.ipe.org.cn/data_ashx/GetAirData.ashx'
  # 企业监管记录检索（需登录）
  curl -sS -A "$UA" -e 'https://www.ipe.org.cn/IndustryRecord/Regulatory.html' \
    -X POST -d 'cmd=getRecords&pageSize=15&pageIndex=1&countryId=0&provinceId=0&cityId=0&professionId=0&indusName=宝钢&index=1' \
    'https://www.ipe.org.cn/data_ashx/GetAirData.ashx?xx=getRecords'
  ```
  其他命令：`?xx=GetCommonTab`、`?xx=getcountry_v1`、`?xx=getindustrycount_new`、`?xx=gethuanping_canyu&keycode=<主页 token>`；企业详情页 `RegulatoryRecord.aspx?companyId=<id>`。**返回是伪 JSON**（`{isSuccess:'1',content:'…'}`，单引号 + `%uXXXX` 转义 HTML），需 `eval`/自行解析，不是严格 JSON。
- 覆盖：全国 · 企业级 · 环境监管记录可上溯多年（按年度记录，最新到 2026）· 另含省/城市双碳指数、电厂/风电/光伏地图、供应链指数。
- 门槛：**公开页面匿名可看**（地图、下拉项、部分榜单）；**企业监管记录检索需登录**（返回 `isSuccess:'201' 本栏目需要登录才能访问`）；批量数据/API 走「数据服务」申请（机构合作/付费）。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA）——`https://www.ipe.org.cn/` → 200（49,039 B，EWC 首页）；`/about/DataServices.html`、`/IndustryRecord/DataIntro.aspx` → 200；`/IndustryRecord/Regulatory.html?keycode=4543j9f9ri334233r3rixxxyyo12` → 200（33,092 B），源码 `js_fxy/Regulatory2023.js` 给出上述 `data_ashx` 端点；`POST /data_ashx/GetAirData.ashx`（`cmd=getprovinces`）→ 200 `text/plain`，`{isSuccess:'1',content:'…'}`；`POST …?xx=getRecords`（`indusName=宝钢`）→ 200 `{isSuccess:'201',msg:'本栏目需要登录才能访问'}`。
- 上游：公众环境研究中心（Institute of Public and Environmental Affairs, IPE）；数据源自各级生态环境部门公开信息，IPE 做整合（蔚蓝地图）。

## 细节

- 首页导航给出全部子站路由：`/AirMap_fxy/AirMap.html`（空气）、`/MapWater/water.html`、`/MapSoil/MassIf.html`、`/MapRadiation/Nuclear.html`、`/MapPowerStation/`、`/GreenSupplyChain/{CITI,CATI,CarbonPRTR}.html`、`/CityEnvironment/CityIndex_33.html`、`/Carbon/CarbonList_*.html`、`/Climate/CCII.html`、`/IndustryRecord/Regulatory.html`。
- 部分页面 URL 需要主页颁发的一次性 `keycode` 参数（如 `?keycode=4543j9f9ri334233r3rixxxyyo12`），**从首页抓取后再拼**，写死会失效。
- 数据下载页 `/GreenSupplyChain/download.html?isfile=0|1`；产品/企业碳计算器指南在 `ipesource.oss-cn-qingdao.aliyuncs.com`。

## 坑

1. **接口返回不是标准 JSON**（单引号、`%uXXXX`、HTML 片段），`json.loads` 会失败；用 `eval` 等价解析或正则。
2. 企业监管记录检索**要登录**；登录后是否放开全量、是否限次，未实测。批量数据不要指望爬，走数据服务合作。
3. `keycode` 是一次性/会话级 token，过期后 403/空结果，脚本要先取首页解析。
4. IPE 是**第三方整合**，用于正式引用时应回链到原生态环境部门公告；记录年份/口径以原文为准。
5. 站点混合 HTTP/HTTPS 与 `aspx/ashx`，路径大小写与 `?xx=` 参数名敏感。
