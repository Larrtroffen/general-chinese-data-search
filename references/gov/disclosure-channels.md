# 政府信息公开渠道 —— 易漏文件的栏目类型总表

- 去哪找：
  - 首都之窗政务公开总入口：`https://www.beijing.gov.cn/gongkai/`
  - 依申请公开网页申请（全市机关入口列表）：`https://www.beijing.gov.cn/gongkai/zfxxgk/ysqgk/`
  - 逐类栏目 URL 见 `## 细节`（10 类，北京为主 + 全国代表源）
- 什么时候用：要**不进政策文件库的角落文件**——依申请公开、政府公报、规范性文件、意见征集、价格听证、审计工作报告（问题单位/金额）、事故调查报告全文、巡视巡察反馈、规划批前公示、房屋征收公告；或问"这类文件在哪一栏"。
- 怎么搜：
  - 先按 `## 细节` 表里的 URL 直达；列表页翻页有三形态——静态 `index_N.html`、慧兰 `javascript:next(N)`、eportal `?currentPage=N`，抓前先确认。
  - 站内检索多为 JS 异步或需签名（`api.so-gov.cn` 后端），**不要直连站内搜索**；定位文章优先 `web_search site:<域名> 关键词` 或搜狗微信。
  - 正文路径有规律：慧兰系 `…/YYYYMM/tYYYYMMDD_<id>.html`；搜索命中后按日期段拼路径可取。
- 覆盖：北京市级 10 类栏目 + 16 区对应入口；另给全国对齐源（国务院公报、审计署、应急管理部、中央纪委巡视、国家法律法规数据库）。粒度=单篇文件/单条公告；多数为动态更新列表。
- 门槛：免费、免登录；部分栏目检索为 JS 表单（需浏览器渲染）；朝阳/延庆只服务 http。
- 实测：2026-10-03，macOS（arm64），curl 8.x（`-sSk -L -m 25`，桌面 Chrome UA），对 17 个不同主机各 1–2 次探测 + 关键页 `read`；抽查 32 个 URL，除 `ccdi` 首次 302 → `-L` 200 外均直连 200（`ghzrzyw…/zhengwuxinxi/ghgs/` 为 404 死链）。明细见 `## 细节`。
- 上游：<https://www.beijing.gov.cn/gongkai/>、各栏目见 `## 细节`

## 细节

### ① 依申请公开（逐机关申请入口）

市统一入口 `…/gongkai/zfxxgk/ysqgk/` 列全 70+ 市级部门与 16 区，逐机关平台 URL 形态：
`http://<机关二级域>.beijing.gov.cn/ysq-web/a/ysqwebset/ysqWebset/ysqweb?officeId=<N>&type=cx`

| 对象 | 申请入口（officeId） |
|---|---|
| 市政府 / 市政府办公厅 | `http://www.beijing.gov.cn/ysq-web/a/ysqwebset/ysqWebset/ysqweb?officeId=61&type=cx` |
| 市发改委 62 / 市住建委 75 / 市审计局 83 / 市应急局 99 | 同形态 `<对应二级域>.beijing.gov.cn/ysq-web/…?officeId=<N>&type=cx` |
| 市规自委 | `https://yewu.ghzrzyw.beijing.gov.cn/gwhd/ysqgk/sqlc.html` |
| 市市场监管局 | `https://cx.scjgj.beijing.gov.cn/InfoPub/notice/` |
| 东城 23 / 海淀 122 / 通州 127 / 顺义 128 / 大兴 129 / 昌平 130 / 密云 133 | `https://<区平台域>/ysq-web/…?officeId=<N>&type=cx` |
| 西城 | `https://www.bjxch.gov.cn/xxgk/ysqgk.html` |
| 朝阳（http）/ 丰台 / 石景山 / 门头沟 / 房山 / 怀柔 / 平谷 / 延庆 | 见下表 |

| 区 | 入口 |
|---|---|
| 朝阳 | `http://www.bjchy.gov.cn/ysqgk/gkzlbgxz.html` |
| 丰台 | `http://www.bjft.gov.cn/ftq/ysqgkzl/ztysqgkzl.shtml` |
| 石景山 | `https://www.bjsjs.gov.cn/gongkai/ysq/` |
| 门头沟 | `https://www.bjmtg.gov.cn/mtgysq/client/homePage` |
| 房山 | `https://www.bjfsh.gov.cn/fsysq/client/selectAcceptanceUnit` |
| 怀柔 | `https://www.bjhr.gov.cn/zwgk/ysqgk/` |
| 平谷 | `http://www.bjpg.gov.cn/eportal/ui?pageId=559300` |
| 延庆（http） | `http://www.bjyq.gov.cn/yanqing/zwgk/wysq/2808001/index.shtml` |

检索/翻页：无列表，进入各机关平台按表单提交申请（JS 表单，需浏览器）。**全国无统一平台**，国家层面逐部门各一（示例：中国政府网"国务院部门信息公开" `https://www.gov.cn/zhengce/xxgk/` ✅200）。

### ② 政府公报

| 栏目 | URL | 形态 | 状态 |
|---|---|---|---|
| 北京市人民政府公报 | `https://www.beijing.gov.cn/zhengce/gongbao` | HTML + JS 检索表单（政策检索/公报检索：标题/全文/发文单位/年份期号） | ✅ 200 |
| 历史公报（按期） | `https://www.beijing.gov.cn/so/zcdh/zfgbHistory` | 按期目录，回溯至 2000 年 | 首页引用 |
| 国务院公报（全国） | `https://www.gov.cn/gongbao/` → `…/gongbao/currentissue.htm`；按期 `…/gongbao/YYYY/issue_<N>/`；高级检索 `https://www.gov.cn/search/gbsousuo.htm` | JS 跳当期 | 见 `gov.cn.md` |

翻页：公报正文由 JS 表单驱动，回溯按"年+期"。

### ③ 规范性文件库

| 栏目 | URL | 状态 |
|---|---|---|
| 北京市规范性文件 | `https://www.beijing.gov.cn/zhengce/gfxwj/` | ✅ 200（403 KB，列表+检索） |
| 首都之窗"政府规章" | `https://www.beijing.gov.cn/gongkai/zfxxgk/zc/gz/index.html` | 公报页引用 |
| 国家法律法规数据库（全国） | `https://flk.npc.gov.cn/` | ✅ 200（552 B SPA 壳，需 JS） |
| 司法部行政法规库（全国） | `http://xzfg.moj.gov.cn/search2.html` | 见 `china-policy-sites.md` |

合法性审核：北京**无独立公开专栏**，审核结论散见各部门文件页与市司法局动态（`https://sfj.beijing.gov.cn/`）——未定位专门库。

### ④ 意见征集

| 栏目 | URL | 状态 |
|---|---|---|
| 政策性文件意见征集（市区两级统一展示） | `https://www.beijing.gov.cn/hudong/gfxwjzj/` | ✅ 200（26 KB） |
| 区级反馈信息 | `https://www.beijing.gov.cn/hudong/gfxwjzj/qjfkxx/` | 首页引用 |
| 网上调查 | `https://www.beijing.gov.cn/hudong/wsdc/` | 首页引用 |
| 东城 调查征集 / 大兴 意见征集 / 密云 政民互动 / 朝阳 互动平台 | `https://www.bjdch.gov.cn/zmhd/dczj/`、`https://www.bjdx.gov.cn/eportal/ui?pageId=1841022`、`https://www.bjmy.gov.cn/zmhd/`、`http://www.bjchy.gov.cn/hdpt/` | 均 ✅ 200 |
| 市发改委 调查征集 | `https://fgw.beijing.gov.cn/zmhd/dczj/` | 搜索命中 |
| 中国政府网（全国） | `https://www.gov.cn/hudong/` | 未验证 |

翻页：区级分页参数不统一（`currentPage=` / `?pageId=` / `list-N`）；"征集—反馈"多成对。

### ⑤ 价格听证

市发改委**无独立听证专栏**，公告散见两列表（标题含"价格听证会公告"）：

| 栏目 | URL | 状态 |
|---|---|---|
| 通知通告 | `https://fgw.beijing.gov.cn/gzdt/tztg/` | ✅ 200（58 KB） |
| 最新消息 | `https://fgw.beijing.gov.cn/gzdt/zxxxnew/` | ✅ 200；`index_10.htm` 载"北京市发展和改革委员会价格听证会公告 2025-09-30" |
| 价格听证目录 | `https://fgw.beijing.gov.cn/fgwzwgk/2024zcwj/bwqtwj/201912/t20191226_3726002.htm` | 搜索命中 |

找法：`web_search site:fgw.beijing.gov.cn 价格听证会公告` → 按 `…/gzdt/tztg/YYYYMM/tYYYYMMDD_<id>.htm` 取正文。全国对口：国家发改委 `https://www.ndrc.gov.cn/` ✅200（听证公告少）。

### ⑥ 审计报告（含问题单位/金额）

| 栏目 | URL | 状态 |
|---|---|---|
| 北京市审计局 审计公告 | `https://sjj.beijing.gov.cn/zwxx/sjgg/` | ✅ 200（16 KB，静态列表，共 27 页，`javascript:next(0)`） |
| └ 年度审计工作报告 / 整改报告 | 同列表（如 2025 年度 `…/sjgg/202607/t20260731_4803494.html`） | 直取 |
| 审计署 公告及解读 / 报告及解读（全国） | `https://www.audit.gov.cn/n5/n25/index.html`、`https://www.audit.gov.cn/n5/n26/index.html` | ✅ 200（后者 43 KB） |

正文多为 HTML，个别附 PDF（审计署 `…/part/<id>.pdf`）。区级报告在区门户/区审计局栏目。

### ⑦ 事故调查报告（调查组报告全文）

| 栏目 | URL | 状态 |
|---|---|---|
| 北京市应急局 事故调查结果公示 | `https://yjglj.beijing.gov.cn/col/col4520/index.html` | ✅ 200（53 KB）：表头「被调查单位/个人 · 报告名称 · 调查部门 · 报告」，同列含"整改评估报告" |
| 单篇形态 | `https://yjglj.beijing.gov.cn/art/YYYY/M/D/art_4520_<N>.html` | 搜索命中多篇 |
| 应急管理部 调查报告（全国） | `https://www.mem.gov.cn/gk/sgcc/tbzdsgdcbg/` | ✅ 200（8.5 KB，JS 列表） |

翻页：慧兰 CMS；栏目页两个过滤框（被调查单位、报告名称）为 JS。

### ⑧ 巡视巡察公开

| 栏目 | URL | 状态 |
|---|---|---|
| 北京纪检监察网 巡视巡察反馈（市委巡视 + 区委巡察） | `http://www.bjsupervision.gov.cn/zt/shejswxc/xsfk/` | ✅ 200（21 KB，静态列表） |
| 高级搜索（WAS5 全文） | `http://www.bjsupervision.gov.cn/was5/web/advanced_search.html` | 页面引用 |
| 中央纪委国家监委 巡视巡察（全国） | `https://www.ccdi.gov.cn/xsxcn/` | ⚠️ 直连 302 → `-L` 200 |

翻页：推断 `…/xsfk/index_N.html`（未逐页验证）；稿件路径 `…/lzbj/YYYYMM/tYYYYMMDD_<id>.html`。各区纪委子站见该页页脚（东城等 15 区）。

### ⑨ 规划公示（批前公示 / 地块）

| 栏目 | URL | 状态 |
|---|---|---|
| 规划类公示（地块规划综合实施方案） | `https://yewu.ghzrzyw.beijing.gov.cn/gwxxfb/cxghghlgs/ghlgs.html` | 首页引用；单篇 `…/ghlgsxq.html?id=<32hex>` |
| 规划类公告（反馈采信/总平面图公布） | `https://ghzrzyw.beijing.gov.cn/chengxiangguihua/ghlgg/` | 首页引用（静态 HTML） |
| 国有土地划拨批前公示 | `https://ghzrzyw.beijing.gov.cn/ziranziyuanguanli/tdhb/tdhbgs/` | ✅ 200（36 KB）；分市/区分局子目录 `sj_tdhbgs`、`sy_tdhbgs`… |
| 土地招拍挂 / 用地预申请 | `https://yewu.ghzrzyw.beijing.gov.cn/gwxxfb/tdsc/tdzpgxm.html` | 首页引用 |
| 自然资源部（全国） | `https://www.mnr.gov.cn/` | ✅ 200 |

翻页：`yewu.*` 为 JS 门户（详情 `?id=`）；主站公告静态（`…/<区码>_ghlgg/YYYYMM/t…html`）。注意 `/zhengwuxinxi/ghgs/` 是 404 死链。

### ⑩ 征收拆迁公告

| 栏目 | URL | 状态 |
|---|---|---|
| 市住建委 房屋征收（汇总） | `https://zjw.beijing.gov.cn/bjjs/fwzs/index.shtml` | ✅ 200（134 KB） |
| └ 征收公告（各区） | `https://zjw.beijing.gov.cn/bjjs/fwzs/ygdxx69/zs/<id>/index.shtml` | 搜索命中多区 |
| 东城 房屋征收拆迁 | `https://www.bjdch.gov.cn/zwgk/zdlygk/fwzscq/` | ✅ 200 |
| 西城 房屋征收（拆迁） | `https://www.bjxch.gov.cn/xxgk/zdly/fwxxgk/zdjscq/zdjscq.html` | ✅ 200（49 KB） |
| 朝阳 房屋征收拆迁 | `http://www.bjchy.gov.cn/affair/zhengshou/` | ✅ 200（http，7.8 KB） |
| 石景山 征收决定 | `http://bjjs.zjw.beijing.gov.cn/bjjs/fwgl/fwzscqgl/ygdxx/zs/<id>/index.shtml` | 搜索命中 |
| 住建部（全国） | `https://www.mohurd.gov.cn/` | ✅ 200 |

翻页：市住建委慧兰静态列表；区级按月倒序静态 HTML。其余 13 区在门户"重点领域公开/房屋征收"栏。

### 实测主机抽样（2026-10-03，本机）

`www.beijing.gov.cn`、`fgw`、`sjj`、`yjglj`、`ghzrzyw`(+`yewu`)、`zjw`、`bjsupervision`、`audit.gov.cn`、`mem.gov.cn`、`ccdi.gov.cn`、`mnr.gov.cn`、`mohurd.gov.cn`、`ndrc.gov.cn`、`flk.npc.gov.cn`、`gov.cn`、`bjdch`/`bjxch`/`bjdx`/`bjmy`/`bjchy` —— 各 1–2 次请求，均 200（例外：`ccdi/xsxcn/` 302→`-L`200；`ghzrzyw…/zhengwuxinxi/ghgs/` 404）。

## 坑

1. **依申请公开逐机关**：统一入口只是"入口列表"，真正提交在各机关 `ysq-web`（`officeId` 不同，不可复用）；全国无统一平台。
2. **"已归档"页仍在用**：`…/ysqgk/` 页脚带 2018 归档角标，但部门/区清单为现行，勿因角标跳过。
3. **站内检索不可直连**：`api.so-gov.cn`、`www.beijing.gov.cn/so/ss/query/s` 为签名/全站聚合，旧域名封出口 IP（见 `beijing.gov.cn.md`、`beijing-districts.md`）——改用 `web_search site:` + 搜狗微信。
4. **列表翻页三形态**（静态 `index_N.html` / 慧兰 `javascript:next(N)` / eportal `?currentPage=N`）勿统一套模板。
5. **HTTPS 不通用**：朝阳、延庆只服务 http；`bjsupervision` 站为 http —— 统一 `-sSk`。
6. **审计/事故列表混含"整改评估报告"**：与初查报告命名相近，勿混用。
7. **规划公示双域**：列表在 `yewu.ghzrzyw…`（JS）、公告在 `ghzrzyw…`（静态）；`/zhengwuxinxi/ghgs/` 死链，正确为 `…/chengxiangguihua/ghlgg/`。
8. **区级路径漂移严重**：区级栏目（征收、审计、规划公示）常改版，用前先探活（参见 `beijing-xxgk.md` 的路径漂移结论）。
