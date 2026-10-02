# 北京市级机构站群 —— 委办局·群团·党派名录

- 去哪找：
  - 机构总入口（市政府部门信息公开专栏索引，一次列全 50+ 委办局官网与信息公开指南）：`https://www.beijing.gov.cn/gongkai/zfxxgk/`
  - 机构职能导航（逐部门机构设置/职责）：`https://www.beijing.gov.cn/gongkai/zfxxgk/fdzdgknr/jgzn/`
  - 权责清单：`https://banshi.beijing.gov.cn/pubtask/right.html?locationCode=110000000000`
  - 市级门户（政策解读/部门动态）：`https://www.beijing.gov.cn/`
- 什么时候用：
  - 要**市级某个委办局的官网**，去其站内「通知公告/政策文件/信息公开」翻文件、公示、名单；
  - 按机构找人：公示、任免、评审结果、执法处罚、年度报告；
  - 找**群团/民主党派/工商联**的发文、活动、委员与领导班子线索；
  - 需要非结构化附件（PDF/Word）时定位对口发布站。
- 怎么搜：
  - 探测（每主机一次）：
    ```bash
    UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    curl -sSk -L -m 12 -A "$UA" -o /dev/null -w '%{http_code} %{url_effective}\n' 'https://<host>/'
    ```
  - 找栏目：进官网后看顶部导航「政务公开/信息公开」→ 找「政策文件」「通知公告」「规划计划」「财政信息」「人事信息」；静态 CMS 的列表页可用 `index_N.html` 翻页（见 `beijing-xxgk.md`）。
  - **站内检索普遍不可直连**（JS 异步 + 签名），跨站找文用 `web_search site:<host> <关键词>` 或搜狗微信（见 `../engines/`）。
  - 结果形态：绝大多数为静态 HTML（UTF-8 为主）；文件/名单多为 `.pdf/.doc/.docx/.xls` 附件。
- 覆盖：北京市级党政机构 —— 市政府办公厅/组成部门/直属机构/特设机构/管委会（约 57 个）、市级群团组织（12）、民主党派北京市委（8）、市工商联；含各站「信息公开/文件」栏目入口。不含 16 区门户（见 `beijing-districts.md`）与市档案馆/市属媒体（见「特设」）。
- 门槛：免费、免登录；个别站 WAF/本机不可达（见 `## 细节` 标注）；数据仅发布页，无批量 API。
- 实测：2026-10-03，macOS（arm64），curl（`-sSk -L -m 12`，桌面 Chrome UA，各主机各 1 次）。市政府口 52 个 `*.beijing.gov.cn` 子站全部 **200**；群团/民主党派域名抽样见 `## 细节`（含 2 个连接被拒、1 个根 404、1 个 403 备用域）。状态码与 URL 分支见下表。
- 上游：<https://www.beijing.gov.cn/gongkai/zfxxgk/>、<https://www.beijing.gov.cn/gongkai/zfxxgk/fdzdgknr/jgzn/>

## 细节

### 市政府组成部门 / 直属机构（官网 + 信息公开栏目）

> 「信息公开」列为各站政府信息公开**指南/专栏**入口（取自`首都之窗` 信息公开索引，官方给定；未逐一实测路径，状态码为**官网首页**结果）。

| 机构 | 官网 | 信息公开/文件栏目 | 状态 |
|---|---|---|---|
| 市政府办公厅 | www.beijing.gov.cn | `/gongkai/zfxxgk/szfbgt/` | ✅ 200 |
| 市发展改革委 | fgw.beijing.gov.cn | `/fgwzwgk/zfxxgk/zfxxgkzn/` | ✅ 200 |
| 市教委 | jw.beijing.gov.cn | `/xxgk/zfxxgkml/zfxxgkzn/` | ✅ 200 |
| 市科委、中关村管委会 | kw.beijing.gov.cn | `/zwgk/zfxxgk/zfxxgkzn/202211/t20221116_3805759.html` | ✅ 200 |
| 市经济和信息化局 | jxj.beijing.gov.cn | `/zwgk/zfxxgk/zfxxgkzn/201912/t20191201_768532.html` | ✅ 200 |
| 市民族宗教委 | mzzjw.beijing.gov.cn | `/zwgk/zfxxgkzl/zfxxgkzn/201911/t20191130_767177.html` | ✅ 200 |
| 市公安局 | gaj.beijing.gov.cn | `/zfxxgk/index.html` | ✅ 200 |
| 市民政局 | mzj.beijing.gov.cn | `/col/col6402/index.html` | ✅ 200 |
| 市司法局 | sfj.beijing.gov.cn | `/sfj/zwgk/zfxxgk81/zfxxgkzn11/index.html` | ✅ 200 |
| 市财政局 | czj.beijing.gov.cn | `/zwxx/zfxxgk/index.html` | ✅ 200 |
| 市人力社保局 | rsj.beijing.gov.cn | `/xxgk/zfxxgk/zfgkzn/` | ✅ 200 |
| 市规划自然资源委 | ghzrzyw.beijing.gov.cn | `/zhengwuxinxi/zfxxgkzn/` | ✅ 200 |
| 市生态环境局 | sthjj.beijing.gov.cn | `/bjhrb/index/ztzl/zfxxgkzl60/zfxxgkzn94/index.html` | ✅ 200 |
| 市住房城乡建设委 | zjw.beijing.gov.cn | `/bjjs/zwgk46/743822685/743822686/index.shtml` | ✅ 200 |
| 市城市管理委 | csglw.beijing.gov.cn | `/zwxx/zfxxgk/zfxxgkzn/201912/t20191231_1548291.html` | ✅ 200 |
| 市交通委 | jtw.beijing.gov.cn | `/xxgk/zfxxgk/ggzn/202001/t20200116_1585340.html` | ✅ 200 |
| 市水务局 | swj.beijing.gov.cn | `/zfxxgkpt/zfxxgkzn/202001/t20200119_1617893.html` | ✅ 200 |
| 市农业农村局 | nyncj.beijing.gov.cn | `/nyj/zwgk/xxgk63/zfxxgkzn36/index.html` | ✅ 200 |
| 市商务局 | sw.beijing.gov.cn | `/zt/zfxxgk/index.html` | ✅ 200 |
| 市文化和旅游局 | whlyj.beijing.gov.cn | `/zfxxgkpt/zn/` | ✅ 200 |
| 市卫生健康委 | wjw.beijing.gov.cn | `/zwgk_20040/zfxxgk2020/gkzn/` | ✅ 200 |
| 市退役军人局 | tyjrswj.beijing.gov.cn | `/zfxxgk/zfxxgkzn/index.html` | ✅ 200 |
| 市应急局 | yjglj.beijing.gov.cn | `/col/col6472/index.html` | ✅ 200 |
| 市市场监管局 | scjgj.beijing.gov.cn | `/zwxx/zfxxgkpt/ptzfxxgkzn/201912/t20191203_781928.html` | ✅ 200 |
| 市审计局 | sjj.beijing.gov.cn | `/zwxx/zfxxgkzn/202007/t20200713_1947370.html` | ✅ 200 |
| 市政府外办 | wb.beijing.gov.cn | `/home/zwxx/zwxx_zwgk/zwgk_gkzn/202001/t20200108_1569597.html` | ✅ 200 |
| 市国资委 | gzw.beijing.gov.cn | `/xxfb/zfxxgk/zfxxgkzn/201912/t20191230_1543911.html` | ✅ 200 |
| 市广电局 | gdj.beijing.gov.cn | `/zfxxgk/zfxxgkzn/202103/t20210326_2330110.html` | ✅ 200 |
| 市文物局 | wwj.beijing.gov.cn | `/bjww/362690/zfxxgk/gkzn/index.html` | ✅ 200 |
| 市体育局 | tyj.beijing.gov.cn | `/bjsports/zfxxgk_/zfxxgkzl/zfxxgkzn76/` | ✅ 200 |
| 市统计局 | tjj.beijing.gov.cn | `/zwgkai/zfxxgk_31395/zfxxgkzn/202601/t20260123_4460077.html` | ✅ 200 |
| 市园林绿化局 | yllhj.beijing.gov.cn | `/zwgk/gkzn/202212/t20221230_2887491.shtml` | ✅ 200 |
| 市政务和数据局 | zwfwj.beijing.gov.cn | `/zwgk/zfxxgk/zfxxgkzn/202103/t20210319_2311902.html` | ✅ 200 |
| 市机关事务局 | jgj.beijing.gov.cn | `/zwgk/zfxxgk/zfxxgkzn/` | ✅ 200 |
| 市国动办（人防） | gdb.beijing.gov.cn | `/rf_zwgk/rf_zfxxgk/rf_zfxxgkzl/` | ✅ 200 |
| 市信访办 | xfb.beijing.gov.cn | `/zwgkyxxgks/zfxxgknew/zfxxgkzn/202311/t20231101_3292960.html` | ✅ 200 |
| 市知识产权局 | zscqj.beijing.gov.cn | `/zscqj/zwgk/zfxxgkzl/zfxxgkzn/index.html` | ✅ 200 |
| 市医保局 | ybj.beijing.gov.cn | `/zwgk/2020_zfxxgk/2020_xxgkzn/` | ✅ 200 |
| 市中医药局 | zyj.beijing.gov.cn | `/zwgk/zfxxgkpt/zfxxgkzn/202103/t20210302_2296467.html` | ✅ 200 |
| 市药监局 | yjj.beijing.gov.cn | `/yjj/zfxxgkzl17/zfxxgkzn7/index.html` | ✅ 200 |
| 市疾控局 | jkj.beijing.gov.cn | `/zwgk/zfxxgk/zfxxgkzn/202509/t20250912_4200776.html` | ✅ 200 |
| 市监狱局 | jyj.beijing.gov.cn | `/zfxxgk/` | ✅ 200 |
| 市粮食和储备局 | lsj.beijing.gov.cn | `/zfxxgkjty/index.html` | ✅ 200 |
| 市重大项目办 | zdb.beijing.gov.cn | `/zfxxgk/zfxxgkzl/zn/202503/t20250321_4041040.html` | ✅ 200 |
| 市城管执法局 | cgj.beijing.gov.cn | `/xxgk/zfxxgk/zfxxgkzn/202103/t20210309_3180376.html` | ✅ 200 |
| 市文化市场执法总队 | whsczfzd.beijing.gov.cn | `/zwgk/zfxxgkzn/` | ✅ 200 |
| 市投资促进服务中心 | invest.beijing.gov.cn | `/zwgk/zfxxgk/zfxxgkpt/xxgkzn/202206/t20220621_2747970.html` | ✅ 200 |
| 北京住房公积金管理中心 | gjj.beijing.gov.cn | `/web/zwgk61/1737313/1737315/index.html` | ✅ 200 |
| 市地方金融监管局 | jrj.beijing.gov.cn | `/zfxxgk/fdzdgknr/qtfdxx/202601/t20260115_4432623.html` | ✅ 200 |
| 市委老干部局 | www.bjlgbj.gov.cn | （站内政务公开栏） | ✅ 200 |
| 市委台办（市台办） | www.bjstb.gov.cn | （站内政务公开栏） | ✅ 200 |

### 特设机构 / 功能区管委会

| 机构 | 官网 | 信息公开/文件栏目 | 状态 |
|---|---|---|---|
| 北京经济技术开发区管委会 | kfqgw.beijing.gov.cn | `/zwgkkfq/zfxxgk/zfxxgkzn/202211/t20221117_2860677.html` | ✅ 200 |
| 天安门地区管委会 | tamgw.beijing.gov.cn | `/zhengwugongkai/zfxxgkzl/` | ✅ 200 |
| 重点站区管委会 | zdzqgw.beijing.gov.cn | `/zwgk/zfxxgk/zfxxgkzn/202001/t20200103_1555923.html` | ✅ 200 |
| 市地震局 | www.bjdzj.gov.cn | （站内政务公开栏） | ✅ 200 |
| 城市副中心管委会 | www.beijing.gov.cn | `/gongkai/zfxxgk/csfzxgwh/` | ✅ 200 |
| 市政府参事室 | www.beijing.gov.cn | `/gongkai/zfxxgk/szfcss/` | ✅ 200 |

### 群团组织

| 机构 | 官网 | 状态 / 备注 |
|---|---|---|
| 北京市总工会 | www.bjzgh.org | ✅ HTTPS 200（http 504，**走 https**） |
| 共青团北京市委 | www.bjyouth.gov.cn / www.bjyouth.net | ✅ 200（`bjyouth.net` 为登录/办公入口） |
| 北京市妇女联合会 | www.bjwomen.gov.cn | ✅ 200（备用 `www.bjwomen.org.cn` → ❌ 403） |
| 北京市科学技术协会 | www.bast.net.cn | ✅ 200 |
| 北京市残疾人联合会 | www.bdpf.org.cn | ✅ 200 |
| 北京市文学艺术界联合会 | www.bjwl.org.cn | ✅ http 200（HTTPS 443 不可达，**走 http**） |
| 北京市红十字会 | www.bjredcross.org.cn | ✅ 200 |
| 北京市法学会 | www.bjfxh.org.cn | ✅ 200 |
| 北京市归国华侨联合会 | www.bjql.org.cn | ✅ 200（http→https 跳转） |
| 北京市社会科学界联合会 | www.bjsk.org.cn | ⚠️ 根路径 404（内容页由搜索索引可见，如 `detail-*.html`） |
| 北京市欧美同学会 | www.bjwrsa.org.cn | ✅ 200 |
| 北京市台湾同胞联谊会 | — | 无独立官网，见市台办 `bjstb.gov.cn` 下属栏目 |
| 北京市黄埔军校同学会 | — | 无独立官网，见市台办 `bjstb.gov.cn` 下属栏目 |
| 北京市工商联 | www.bjgsl.gov.cn | ✅ 200（注意：`bjgsl.org.cn` 已被抢注为游戏站，勿用） |

### 民主党派北京市委

| 党派 | 官网 | 状态 / 备注 |
|---|---|---|
| 民革北京市委 | bjmg.org.cn | ⚠️ 域名存在，本机连接被拒（2026-10-03，端口 80/443 均拒） |
| 民盟北京市委 | www.bjmm.org.cn | ⚠️ 域名存在，本机连接被拒（同上） |
| 民建北京市委 | www.bjmj.gov.cn | ✅ 200（`bjmj.com.cn` 为待售域名，勿用） |
| 民进北京市委 | www.mj.org.cn/bj/ | ✅ 200（民进中央站下的北京频道） |
| 农工党北京市委 | www.bjng.gov.cn | ✅ 200 |
| 致公党北京市委 | www.bjzg.org.cn | ✅ 200（首页无 `<title>`，疑前端渲染） |
| 九三学社北京市委 | www.bj93.gov.cn | ✅ 200 |
| 台盟北京市委 | — | 无独立官网，见台盟中央 `www.taimeng.org.cn`（✅ 200）及市台办栏目 |

### 特设：档案馆 / 市属媒体（引用已有卡，不重复）

- 北京市档案馆 `www.bjma.gov.cn`（开放档案文件级目录查询）→ 见 `../archives/archives-cn.md`。
- 北京日报 / 京报网 / 北京晚报等市属媒体与数字报 → 见 `../media/epaper/README.md`、`../media/`。
- 北京市地方志（北京市志/年鉴/区县志）→ 见 `../archives/bjdsdfz.cn.md`、`../archives/bjsfzg.bjdsdfz.cn.md`。

## 坑

1. **`*.beijing.gov.cn` 子站不代表机构独立**：委办局域名多为 `简称.beijing.gov.cn`（如 `fgw`=发改委、`jw`=教委、`rsj`=人社局），但也有特例 `www.bjdzj.gov.cn`（地震局）、`www.bjgsl.gov.cn`（工商联）、`www.bjstb.gov.cn`（台办）为独立域。
2. **易混/抢注**：`bjgsl.org.cn`=游戏站≠工商联；`bjmj.com.cn`=待售域名≠民建；民建实为 `bjmj.gov.cn`。群团/党派用 `.org.cn` 与 `.gov.cn` 混用，需核对站名。
3. **HTTPS 不通用**：总工会 `bjzgh.org` 只有 443 可用（80 返回 504）；文联 `bjwl.org.cn` 只有 http；妇联备用域 403。
4. **民主党派站点可达性差**：民革 `bjmg.org.cn`、民盟 `bjmm.org.cn` 域名在搜索索引中有效，但本机连接被拒 —— 换网络/浏览器重试，或改从**北京市政协** `www.bjzx.gov.cn/zxgz/dptt/`（「党派团体」栏）与市台办子站取稿。
5. **信息公开栏目路径无统一规律**：同样是「信息公开指南」，各局路径从 `/zfxxgk/` 到 `/bjhrb/index/ztzl/zfxxgkzl60/…` 不一，勿套模板；以本表「信息公开」列为准，失效时回 `beijing.gov.cn/gongkai/zfxxgk/` 索引重取。
6. **站内检索不可直连**：见 `beijing-districts.md` 结论（JS + `api.so-gov.cn` 签名、封 IP）；跨站找文用 `web_search site:` / 搜狗微信。
