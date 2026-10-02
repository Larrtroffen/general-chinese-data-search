# china-policy-sites —— 全国政策发布站点总表

- 去哪找：
  - repo：`https://github.com/changwu/china-policy-sites`（默认分支 `main`，**无 LICENSE**）
  - raw 基址：`https://raw.githubusercontent.com/changwu/china-policy-sites/main/`
  - 目录结构（实测）：
    ```
    README.md          # 项目说明 + 10 个镜像存档仓库索引
    国家部委.md        # 80 行：国务院/组成部门/直属特设/直属机构/办事机构/事业单位/部管国家局
    地级市.md          # 28 省区 × 地级市「名单」（仅名称，除江苏/福建外无 URL）
    直辖市.md          # 京/沪/津/渝 的区县名单（仅名称）
    广东省/广东省.md    # 省级 54 个部门入口
    江苏省/江苏省.md    # 省级 35 个部门入口；江苏省/ 下另有 12 个地级市文件
    福建省/福建省.md    # 省级 46 个部门入口；福建省/ 下另有 厦门/泉州/漳州
    ```
- 什么时候用：
  - **已知某国家部委名**（「国家能源局」「海关总署」「国家药监局」），要直接拿它的主页 / 政策文件库 / 信息公开 URL → `国家部委.md`（见下方内联表）。
  - **已知某省厅名**（「广东省生态环境厅」「江苏省医疗保障局」），要省级部门入口 → `广东省/广东省.md`、`江苏省/江苏省.md`、`福建省/福建省.md`。
  - **已知某地级市名**，要找市政府/市部门入口 → `江苏省/<市>.md`、`福建省/<市>.md`（目前仅这 15 市成稿）。
  - **要省级/地级市的行政名册**（名单核对、按省枚举城市）→ `地级市.md`、`直辖市.md`。
  - 不适用：要政策**正文/检索** → 走 `gov.cn.md` 的检索 API；本表只给入口。
- 怎么取（最小可复现步骤如下）：
  ```bash
  # 单文件直取（raw 无需 key；中文路径需 URL 编码）
  F='广东省/广东省.md'
  curl -s "https://raw.githubusercontent.com/changwu/china-policy-sites/main/$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$F")"
  # 全国部委表 / 名录
  curl -s "https://raw.githubusercontent.com/changwu/china-policy-sites/main/$(python3 -c "import urllib.parse;print(urllib.parse.quote('国家部委.md'))")"
  ```
  网络受限时：`gh api repos/changwu/china-policy-sites/contents/国家部委.md --jq .content | base64 -d`。取目录：`gh api repos/changwu/china-policy-sites/contents/ --jq '.[].name'`。
- 覆盖：粒度=一行一个机关，含主页 + 1~6 个栏目 URL。**部委已完成**；省级只完成广东/江苏/福建；其余 25 省区、294 地级市、4 直辖市部门**仅名称或完全未做**（README 自述「未完成」）。更新低频（文件整理日期 2026-07-15，push 2026-09-22）；链接会漂移，**用前先探活**。
- 门槛：免费、免 key、raw/gh 直取；**无 LICENSE** → 只用其链接与事实，不把整理成果整体搬进我们仓库。
- 实测：2026-10-02，macOS，curl。raw 直取 6 个文件（国家部委/地级市/直辖市/广东省/江苏省/厦门市）均 **200**；抽查目标站：`mee.gov.cn/zcwj/` 200、`mca.gov.cn` 200、`ndrc.gov.cn/xxgk/wjk` 302→200（须 `-L`）、`xxgk.mca.gov.cn:8011`（000，连不上）、`gd.gov.cn/gkmlpt/index` 200、`drc.gd.gov.cn/gkmlpt/index` 200、`jiangsu.gov.cn/col/col84242/index.html` 200、`xm.gov.cn/zwgk/flfg/` 200。
- 上游：<https://github.com/changwu/china-policy-sites>

## 细节

一份**站点 URL 清单**：把国务院 80 个国家部委（65+15 加挂牌）、23 省+5 自治区及 294 个地级市、4 个直辖市的「主页 / 政府信息公开 / 政策文件库 / 政策解读」URL 按层级整理成 Markdown。**不含政策正文**，只回答「某机关的政策从哪个 URL 出」。

### 省级索引（省名 → 本仓文件）

| 省/区 | 本仓文件 | 部门条目 |
|---|---|---|
| 广东省 | `广东省/广东省.md` | 54 |
| 江苏省 | `江苏省/江苏省.md`（+ 12 市文件） | 35 |
| 福建省 | `福建省/福建省.md`（+ 厦门/泉州/漳州） | 46 |
| 其余 25 省区（河北/山西/内蒙古/辽宁/吉林/黑龙江/浙江/安徽/江西/山东/河南/湖北/湖南/广西/海南/四川/贵州/云南/西藏/陕西/甘肃/青海/宁夏/新疆/台湾） | 仅 `地级市.md` 的城市名单 | 无 URL |

- 已有 URL 的地级市：`江苏省/` 下 南京、无锡、徐州、常州、苏州、南通、连云港、淮安、盐城、扬州、镇江、泰州；`福建省/` 下 厦门、泉州、漳州。宿迁、福建其余 6 市及其余省份城市**均未做**。
- 直辖市 `直辖市.md` 只有区县名称（北京16、上海16、天津16、重庆25区+12县），**无区政府 URL**。

### 国家部委 65+15 内联（`国家部委.md` 全量，名称 ｜ 链接）

| 机关 | 入口 |
|---|---|
| 中华人民共和国国务院/国务院办公厅 | [主页](https://www.gov.cn/) ｜ [最新政策](http://www.gov.cn/zhengce/zuixin.htm) ｜ [文件库](http://sousuo.gov.cn/s.htm?q=&t=zhengcelibrary&orpro=) |
| 外交部 | [主页](https://www.fmprc.gov.cn/) ｜ [信息公开](https://www.fmprc.gov.cn/web/wjb_673085/zfxxgk_674865/gknrlb/zcfg/) |
| 国家发展改革委 | [主页](https://www.ndrc.gov.cn/) ｜ [政务公开](https://www.ndrc.gov.cn/xxgk/) ｜ [文件库](https://www.ndrc.gov.cn/xxgk/wjk) |
| 科学技术部 | [主页](http://www.most.gov.cn/) ｜ [科技政策](http://www.most.gov.cn/kjzc/) |
| 国家民族事务委员会 | [主页](http://www.neac.gov.cn/) ｜ [政府信息公开](http://www.neac.gov.cn/seac/xxgk/index.shtml) |
| 国家安全部 | [主页](https://www.12339.gov.cn/) |
| 司法部 | [主页](http://www.moj.gov.cn/) ｜ [行政法规库](http://xzfg.moj.gov.cn/search2.html) |
| 人力资源和社会保障部 | [主页](http://www.mohrss.gov.cn/) ｜ [信息公开](http://www.mohrss.gov.cn//xxgk2020/) |
| 生态环境部 | [主页](https://www.mee.gov.cn/) ｜ [政策文件](https://www.mee.gov.cn/zcwj/) |
| 交通运输部 | [主页](https://www.mot.gov.cn/) ｜ [政策](https://www.mot.gov.cn/zhengce/) |
| 农业农村部 | [主页](http://www.moa.gov.cn/) ｜ [公开](http://www.moa.gov.cn/gk/) |
| 文化和旅游部 | [主页](https://www.mct.gov.cn/) ｜ [政府信息公开](http://zwgk.mct.gov.cn/zfxxgkml/447/458/463/index_3081.html) |
| 退役军人事务部 | [主页](http://www.mva.gov.cn/) ｜ [政策解读](http://www.mva.gov.cn/jiedu/zcjd/) |
| 中国人民银行 | [主页](http://www.pbc.gov.cn/) ｜ [政策解读](http://www.pbc.gov.cn/rmyh/3963412/index.html) ｜ [政策文件](http://www.pbc.gov.cn/zhengwugongkai/4081330/4081344/4081395/4081686/index.html) ｜ [条法司](http://www.pbc.gov.cn/tiaofasi/144941/index.html) |
| 国防部 | [主页](http://www.mod.gov.cn/) ｜ [法规文献](http://www.mod.gov.cn/regulatory/index.htm) |
| 教育部 | [主页](http://www.moe.gov.cn/) ｜ [政策解读](http://www.moe.gov.cn/jyb_xwfb/s271/) ｜ [教育部文件](http://www.moe.gov.cn/was5/web/search?channelid=239993) |
| 工业和信息化部 | [主页](https://wap.miit.gov.cn/) ｜ [政策文件](https://wap.miit.gov.cn/search/wjfb.html?websiteid=110000000000000&tpl=14&category=51) |
| 公安部 | [主页](https://8221110.com/) ｜ [政策文件](https://8221110.com/n6557558/index.html) ｜ [政策解读](https://8221110.com/n6557563/index.html) |
| 民政部 | [主页](http://www.mca.gov.cn/) ｜ [政策文件](http://xxgk.mca.gov.cn:8011/gdnps/pc/index.jsp?mtype=1) |
| 财政部 | [主页](http://www.mof.gov.cn/index.htm) ｜ [政策发布](http://www.mof.gov.cn/zhengwuxinxi/zhengcefabu/) ｜ [政策解读](http://www.mof.gov.cn/zhengwuxinxi/zhengcejiedu/) |
| 自然资源部 | [主页](http://www.mnr.gov.cn/) ｜ [政策法规库](http://f.mnr.gov.cn/) ｜ [政策解读](http://www.mnr.gov.cn/gk/zcjd/) |
| 住房和城乡建设部 | [主页](http://www.mohurd.gov.cn/) ｜ [政策发布](http://www.mohurd.gov.cn/wjfb/index.html) |
| 水利部 | [主页](http://mwr.gov.cn/) ｜ [政策法规](http://www.mwr.gov.cn/zw/zcfg/fl/) ｜ [政策解读](http://www.mwr.gov.cn/zw/zcjd/) |
| 商务部 | [主页](http://www.mofcom.gov.cn/) ｜ [政策发布](http://www.mofcom.gov.cn/article/zcfb/) ｜ [政策解读](http://www.mofcom.gov.cn/article/zcjd/) ｜ [政策图解](http://www.mofcom.gov.cn/article/tj/) |
| 国家卫生健康委员会 | [主页](http://www.nhc.gov.cn/) ｜ [规范性文件](http://www.nhc.gov.cn/wjw/gfxwjj/list.shtml) ｜ [政策解读](http://www.nhc.gov.cn/wjw/zcjd/list.shtml) |
| 应急管理部 | [主页](https://www.mem.gov.cn/) ｜ [政策解读](https://www.mem.gov.cn/gk/zcjd/) ｜ [法律法规标准](https://www.mem.gov.cn/fw/flfgbz/) |
| 审计署 | [主页](https://www.audit.gov.cn/) ｜ [法律法规](https://www.audit.gov.cn/n6/n36/index.html) |
| 国务院国资委 | [主页](http://www.sasac.gov.cn/) ｜ [政策](http://www.sasac.gov.cn/n2588035/n2588320/index.html) ｜ [政策解读](http://www.sasac.gov.cn/n2588035/n2588320/n2588340/index.html) |
| 海关总署 | [主页](http://www.customs.gov.cn/) ｜ [最新文件](http://www.customs.gov.cn/customs/302249/2480148/index.html) ｜ [海关法规](http://www.customs.gov.cn/customs/302249/302266/index.html) ｜ [政策解读](http://www.customs.gov.cn/customs/302249/302270/302272/index.html) |
| 国家市场监督管理总局 | [主页](https://www.samr.gov.cn/) ｜ [总局文件](https://www.samr.gov.cn/zw/wjfb/) ｜ [政策解读](https://www.samr.gov.cn/zw/wjfb/zdjd/) |
| 国家体育总局 | [主页](https://www.sport.gov.cn/) ｜ [政策法规](http://www.sport.org.cn/search/system/) |
| 国家国际发展合作署 | [主页](http://www.cidca.gov.cn/) ｜ [法规政策](http://www.cidca.gov.cn/fgzd.htm) |
| 国务院参事室 | [主页](http://www.counsellor.gov.cn/) ｜ [法规文件](http://www.counsellor.gov.cn/fgwj.htm) ｜ [文件解读](http://www.counsellor.gov.cn/wjjd.htm) |
| 国家税务总局 | [主页](http://www.chinatax.gov.cn/) ｜ [税收政策](http://www.chinatax.gov.cn/chinatax/n810341/index.html) |
| 国家广播电视总局 | [主页](http://www.nrta.gov.cn/) ｜ [部门规章](http://www.nrta.gov.cn/col/col1588/index.html) ｜ [规范性文件](http://www.nrta.gov.cn/col/col2062/index.html) |
| 国家统计局 | [主页](http://www.stats.gov.cn/) ｜ [政策](http://www.stats.gov.cn/xxgk/list1.html) |
| 国家医疗保障局 | [主页](http://www.nhsa.gov.cn/) ｜ [政策法规](http://www.nhsa.gov.cn/col/col37/index.html) ｜ [政策解读](http://www.nhsa.gov.cn/col/col38/index.html) |
| 国家机关事务管理局 | [主页](http://www.ggj.gov.cn/) ｜ [法律法规](http://www.ggj.gov.cn/zcfg/flfg/) ｜ [部门规章](http://www.ggj.gov.cn/zcfg/bmgz/) ｜ [规范性文件](http://www.ggj.gov.cn/zcfg/fgxwj/) ｜ [政策解读](http://www.ggj.gov.cn/zcfg/zcjd/) |
| 国家认证认可监督管理委员会 | [主页](http://www.cnca.gov.cn/) ｜ [政务](http://www.cnca.gov.cn/zw/) |
| 国家标准化管理委员会 | [主页](http://www.sac.gov.cn/) ｜ [政策文件](http://www.sac.gov.cn/sxxgk/zcwj/) ｜ [政策解读](http://www.sac.gov.cn/sxxgk/zcjd/) |
| 国家新闻出版署（国家版权局） | [主页](http://www.nppa.gov.cn/) ｜ [政策法规](http://www.nppa.gov.cn/nppa/channels/308.shtml) |
| 国家宗教事务局 | [主页](http://www.sara.gov.cn/) ｜ [信息公开](http://www.sara.gov.cn/xxgk/index.jhtml) |
| 国务院港澳事务办公室 | [主页](https://www.hmo.gov.cn/) ｜ [政策法规](https://www.hmo.gov.cn/zcfg_new/xf/) |
| 国务院研究室 | [主页](http://www.gov.cn/gjjg/2005-12/26/content_137261.htm) |
| 国务院侨务办公室 | [主页](https://www.gqb.gov.cn/) ｜ [政策法规](http://www.gqb.gov.cn/gqb/zcfg/index.shtml) |
| 国务院台湾事务办公室 | [主页](http://www.gwytb.gov.cn/) ｜ [政策措施](http://www.gwytb.gov.cn/zccs/) |
| 国家互联网信息办公室（中央网信办） | [主页](http://www.cac.gov.cn/) ｜ [权威发布](http://www.cac.gov.cn/qwfb/A0903index_1.htm) ｜ [政策法规](http://www.cac.gov.cn/zcfg/xzfg/A090902index_1.htm) |
| 国务院新闻办公室 | [主页](http://www.scio.gov.cn/index.htm) ｜ [政府白皮书](http://www.scio.gov.cn/zfbps/index.htm) |
| 新华通讯社 | [主页](http://203.192.6.89/xhs/xhsjj.htm) |
| 中国社会科学院 | [主页](http://cass.cssn.cn/) |
| 国务院发展研究中心 | [主页](https://www.drc.gov.cn/) |
| 中国气象局 | [主页](http://www.cma.gov.cn/) ｜ [政策文件](http://zwgk.cma.gov.cn/zfxxgk/gknr/wjgk/gfxwj/) ｜ [政策解读](http://zwgk.cma.gov.cn/zfxxgk/gknr/wjgk/zcjd/) |
| 中国证券监督管理委员会 | [主页](http://www.csrc.gov.cn/pub/newsite/) ｜ [监管信息公开目录](http://www.csrc.gov.cn/pub/zjhpublic/index.htm?channel=3300/3311) |
| 中国科学院 | [主页](https://www.cas.cn/) ｜ [规章制度](https://www.cas.cn/gzzd/zkxzc/) |
| 中国工程院 | [主页](https://www.cae.cn/) ｜ [政策文件](https://www.cae.cn/cae/html/main/col25/column_25_1.html) |
| 中央广播电视总台 | [主页](http://www.cnr.cn/) |
| 中国银行保险监督管理委员会 | [主页](https://www.cbirc.gov.cn/) ｜ [政务信息](https://www.cbirc.gov.cn/cn/view/pages/zhengwuxinxi/zhengwuxinxi.html) |
| 国家行政学院与中央党校 | [主页](https://www.ccps.gov.cn/) |
| 国家信访局 | [主页](https://www.gjxfj.gov.cn) ｜ [法规文件](https://www.gjxfj.gov.cn/gjxfj/fgwj/index.htm) ｜ [规范性文件](https://www.gjxfj.gov.cn/gjxfj/fgwj/gfxwj.htm) ｜ [政策解读](https://www.gjxfj.gov.cn/gjxfj/fgwj/zcjd.htm) |
| 国家能源局 | [主页](http://www.nea.gov.cn/) ｜ [最新文件](http://www.nea.gov.cn/policy/zxwj.htm) ｜ [通知](http://www.nea.gov.cn/policy/tz.htm) ｜ [公告](http://www.nea.gov.cn/policy/gg.htm) ｜ [解读](http://www.nea.gov.cn/policy/jd.htm) |
| 国家烟草专卖局 | [主页](http://www.tobacco.gov.cn/) ｜ [行政规范文件](http://www.tobacco.gov.cn/gjyc/xzgfwj/xxgk_gknr_list.shtml) ｜ [政策文件库](http://www.tobacco.gov.cn/gjyc/zcwjk/zck.shtml?tab=zcwj) |
| 国家林业和草原局 | [主页](http://www.forestry.gov.cn/) ｜ [林草政策](http://www.forestry.gov.cn/main/5461/index.html) ｜ [规范性文件](http://www.forestry.gov.cn/sites/main/main/gfxwj/gfxwj-list.jsp) |
| 中国民用航空局 | [主页](http://www.caac.gov.cn) ｜ [政策发布](http://www.caac.gov.cn/XXGK/XXGK/index_172.html?fl=10) |
| 国家文物局 | [主页](http://www.ncha.gov.cn/) ｜ [法定主动公开内容](http://www.ncha.gov.cn/col/col2237/index.html?id=0) |
| 国家矿山安全监察局 | [主页](https://www.chinamine-safety.gov.cn/) ｜ [法定主动公开内容](https://www.chinamine-safety.gov.cn/zfxxgk/fdzdgknr/tzgg/) |
| 国家药品监督管理局 | [主页](https://www.nmpa.gov.cn/) ｜ [法规文件](https://www.nmpa.gov.cn/xxgk/fgwj/index.html) |
| 国家粮食和物资储备局 | [主页](http://www.lswz.gov.cn) ｜ [法定主动公开内容](http://www.lswz.gov.cn/html/zfxxgk/fdzdgknr.shtml) |
| 国家国防科技工业局 | [主页](http://www.sastind.gov.cn/) ｜ [政策文件](http://www.sastind.gov.cn/n4235/n6654336/index.html) |
| 国家移民管理局 | [主页](https://www.nia.gov.cn/) ｜ [政策文件](https://www.nia.gov.cn/n741440/n741547/index.html) ｜ [政策解读](https://www.nia.gov.cn/n741440/n741577/index.html) |
| 国家铁路局 | [主页](http://www.nra.gov.cn/) ｜ [行政许可](http://www.nra.gov.cn/wsbs/xzxk/xzxkxm/) ｜ [监管履职](http://www.nra.gov.cn/jgzf/) |
| 国家邮政局 | [主页](http://www.spb.gov.cn/) ｜ [政策](http://www.spb.gov.cn/zc/) |
| 国家中医药管理局 | [主页](http://www.satcm.gov.cn/) ｜ [政策文件](http://www.satcm.gov.cn/zhengcewenjian/) |
| 国家外汇管理局 | [主页](http://www.safe.gov.cn/safe/index.html) ｜ [政策法规](http://www.safe.gov.cn/safe/zcfg/index.html) |
| 国家知识产权局 | [主页](https://www.cnipa.gov.cn/) ｜ [政策文件](https://www.cnipa.gov.cn/col/col74/index.html) ｜ [政策解读](https://www.cnipa.gov.cn/col/col66/index.html) |
| 国家公务员局 | [主页](http://www.scs.gov.cn/) ｜ [政策法规](http://www.scs.gov.cn/zcfg/) |
| 国家档案局与中央档案馆 | [主页](https://www.saac.gov.cn/) ｜ [档案政策法规库](https://www.saac.gov.cn/daj/falv/dazc_list.shtml) ｜ [档案标准库](https://www.saac.gov.cn/daj/gjbz/dabz_list.shtml) |
| 国家保密局与中央保密委员会办公室 | [主页](http://www.gjbmj.gov.cn/) ｜ [政策法规](http://www.gjbmj.gov.cn/409049/index.html) |
| 国家密码管理局与中央密码工作领导小组办公室 | [主页](https://www.oscca.gov.cn/) ｜ [政策法规](https://www.oscca.gov.cn/sca/xxgk/zcfg.shtml) |

> 加挂牌（出入境管理局、国家公园管理局）与部分事业单位主页与上级机关重复；银保监会（cbirc）已于 2023 年改为国家金融监督管理总局，表内未更新。

### 附带：10 个「政务公开内容存档」镜像仓库

README 汇总了发起人名下 **10 个城市政务公开 HTML 存档仓**（`<城市>-policy-opening-html`），是**离线正文**来源（非 URL 清单）。仓库极大，**不要克隆**，按需 raw/网页取单文件：

| 城市 | 仓库 | size（gh api，KB） |
|---|---|---|
| 福州 | `changwu/fuzhou-policy-opening-html` | 300,238 |
| 泉州 | `changwu/quanzhou-policy-opening-html` | 245,602 |
| 漳州 | `changwu/zhangzhou-policy-opening-html` | 49,146 |
| 厦门 | `changwu/xiamen-policy-opening-html` | 39,989 |
| 龙岩 | `changwu/longyan-policy-opening-html` | 2,933,924 |
| 平潭 | `changwu/pingtan-policy-opening-html` | 15,548,273 |
| 三明 | `changwu/sanming-policy-opening-html` | 3,217,652 |
| 南平 | `changwu/nanping-policy-opening-html` | 310,791 |
| 莆田 | `changwu/putian-policy-opening-html` | 699,052 |
| 南京 | `changwu/nanjing-policy-opening-html` | 1,276,344 |

## 坑

1. **无 license**；整理有错漏：工信部、公安部给了非 www 域名（wap/8221110）；广电总局的「政策解读」误填到 nhsa.gov.cn；「新疆」条目重复了常州的 URL。
2. 部分 http 链接 302→https，取用需 `curl -L`；民政部 xxgk 端口 8011 实测连不上。
3. 机构名未更新（银保监会、2018 年机构改革后的变动）→ 与 `gov.cn.md` 的机关名交叉核对。
4. 只给 URL 不给接口；进站后如何检索见 `gov.cn.md`、`beijing.gov.cn.md`。
