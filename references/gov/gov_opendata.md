# gov_opendata —— 全国政府开放数据平台清单

- 去哪找：
  - repo：`https://github.com/LuMitchell/gov_opendata`（默认分支 `master`，**无 LICENSE**，仅 1 个 README.md，约 4 KB）
  - raw 直取：`https://raw.githubusercontent.com/LuMitchell/gov_opendata/master/README.md`
  - 备用：`gh api repos/LuMitchell/gov_opendata/contents/README.md --jq .content | base64 -d`
- 什么时候用：
  - 要**省级开放数据平台**（如「北京市公共数据开放平台」「广东省开放数据」）→ 本表省级段。
  - 要**地市级开放数据平台**（成都、深圳、青岛、苏州、宁波、武汉…）→ 本表城市段。
  - 做「政府数据开放程度」研究、找某地数据集的下载门户。
  - 不适用：要政策文件 → `gov.cn.md` / `china-policy-sites.md`；要统计数据 → `../stats/`。
- 怎么取：`curl -sL 'https://raw.githubusercontent.com/LuMitchell/gov_opendata/master/README.md'`（raw 200 / 4.0 KB）；结果为 Markdown 纯链接清单，无 API、无数据格式、无字段。进站后各自的开放目录/接口需自行探测。
- 覆盖：README 全量，13 个省级 + 27 个地市级「政府开放数据平台」（数据集下载门户），含若干已下线标注；是**数据本体**入口，不是政策文本源。
- 门槛：免费、免 key、raw 直取；**无 LICENSE**，内容 2019 年前后整理；多数平台为 http 且部分走 301→https（脚本取用 `curl -L`），部分需登录（重庆）。
- 实测：2026-10-02，macOS，`curl -sIL -m 15~20`，带桌面 UA。README raw 直取 200（4.0 KB，`master` 分支）；上表状态列即实测结果（200 者直连；301/302 者注明跳转目标；412=上海反爬；000=DNS/连接失败：陕西、贵州、重庆、宁夏）。**未**逐个下载数据集。
- 上游：<https://github.com/LuMitchell/gov_opendata>

## 细节

一份**纯链接清单**：把全国 13 个省级 + 27 个地市级「政府开放数据平台」（数据集下载门户）整理成一个 README，含若干已下线标注。

### 省级（13）

| 平台 | URL | 状态 |
|---|---|---|
| 北京 | https://data.beijing.gov.cn/ | 200 |
| 上海 | https://data.sh.gov.cn/ | 412（反爬，需 UA/浏览器） |
| 天津 | https://data.tj.gov.cn/ | 200 |
| 福建 | https://data.fujian.gov.cn/odweb/ | 200 |
| 海南 | http://data.hainan.gov.cn/ | 200 |
| 河南 | http://data.hnzwfw.gov.cn/odweb/ | 302 → www.hnzwfw.gov.cn（原开放平台疑已并入政务网） |
| 广东 | http://gddata.gd.gov.cn/ | 301 → https 200 |
| 江西 | http://data.jiangxi.gov.cn/ | 200 |
| 宁夏 | http://ningxiadata.gov.cn/odweb/index.htm | **已下线**（000，README 原标注） |
| 山东 | http://data.sd.gov.cn/ | 301 → https 200 |
| 陕西 | http://www.sndata.gov.cn/ | 000（连不上） |
| 浙江 | http://data.zjzwfw.gov.cn/jdop_front/index.do | 301 → https://data.zjzwfw.gov.cn/dopServer/（改版） |
| 贵州 | http://data.guizhou.gov.cn/ | 000（连不上） |

### 地市级（28 + 重庆/台湾，含下线）

| 平台 | URL | 状态 |
|---|---|---|
| 成都 | http://www.cddata.gov.cn/ | — |
| 深圳 | https://opendata.sz.gov.cn | 200 |
| 雅安 | http://www.yaan.gov.cn/shuju.html | — |
| 厦门 | http://data.xm.gov.cn/opendata/index.html#/ | — |
| 佛山 | http://www.foshan-data.cn/ | **已下线**（README 标注，2019 升级未上线） |
| 广州 | http://data.gz.gov.cn/odweb/ | — |
| 东莞 | http://dataopen.dg.gov.cn/dataopen/ | — |
| 惠州 | http://data.huizhou.gov.cn/ | — |
| 珠海 | http://data.zhuhai.gov.cn | — |
| 江门 | http://data.jiangmen.gov.cn/odweb/ | — |
| 中山 | http://zsdata.zs.gov.cn/web/index | — |
| 肇庆 | http://www.zhaoqing.gov.cn/sjkf/ | — |
| 贵阳 | http://www.gyopendata.gov.cn/city/index.htm | — |
| 遵义 | http://www.zyopendata.gov.cn/ | — |
| 铜仁 | http://gztrdata.gov.cn/ | — |
| 石嘴山 | http://szssjkf.nxszs.gov.cn/ | — |
| 银川 | http://data.yinchuan.gov.cn/odweb/ | — |
| 济南 | http://data.jinan.gov.cn/ | — |
| 青岛 | http://data.qingdao.gov.cn/ | — |
| 哈尔滨 | http://data.harbin.gov.cn/ | — |
| 宁波 | http://www.datanb.gov.cn/nbdatafore/web/indexpage.action | — |
| 合肥 | http://61.133.142.137:8800/open-data-web/index/index-hfs.do | — |
| 蚌埠 | http://data.bengbu.gov.cn/ | — |
| 黄山 | http://www.huangshan.gov.cn/DataDevelopment/ | — |
| 武汉 | http://www.wuhandata.gov.cn/whData/ | — |
| 长沙 | http://www.changsha.gov.cn/data/ | — |
| 苏州 | http://www.suzhou.gov.cn/OpenResourceWeb/home | — |
| 常州 | http://opendata.changzhou.gov.cn/ | — |
| 重庆 | http://data.cq.gov.cn | 000；**需登录**（README 标注） |
| 台湾 | https://data.gov.tw | 200（响应慢） |

> ⚠️ README 中「新疆」一行重复了常州的 URL（`opendata.changzhou.gov.cn`），疑为笔误，未采信。
> 「石嘴山/银川」属宁夏——宁夏省级平台已下线，市级或仍有镜像。

## 坑

1. **无 license**，内容 2019 年前后整理，**2024-08 后未更新** → 大量链接已漂移/下线（状态列为 2026-10-02 实测）。
2. 纯清单，无 API 说明、无数据格式、无字段。
3. 多数为 http 且部分走 301→https，脚本取用请 `curl -L`；上海 412 反爬需带浏览器 UA 或走浏览器。
4. 部分平台需登录（重庆）；部分老平台（合肥为 IP:端口）稳定性差。
