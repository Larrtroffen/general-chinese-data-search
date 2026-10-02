# CHIP·CHNS·CSS —— 收入·营养·社会状况三调查

- 去哪找：CHIP 元数据/CNSDA 检索 `https://www.cnsda.org/`（如 `…?r=projects/view&id=66120595`）；CHNS `https://www.cpc.unc.edu/projects/china`；CSS `http://css.cssn.cn/css_sy`。
- 什么时候用：要**收入分配（CHIP）**、**健康与营养（CHNS）**、**社会状况与社会态度（CSS）**三类经典全国调查之一时。
- 怎么取：三者渠道不同——CHIP 经 CNSDA/项目方申请（1988/1995/2002/2007/2013 各期）；CHNS 在 UNC Dataverse 下载家庭与个人层主文件，社区层须签 data use agreement（邮件 `chns@unc.edu`）；CSS 走社科院社会学所的数据申请系统。
- 覆盖：CHIP 1988 / 1995 / 2002 / 2007 / 2013（城乡分样本，收入分配专题）；CHNS 1989 起多轮纵向（家庭/个人/社区三层，含生物标记物；波次为上游声明）；CSS 2005 年发起、双年度纵贯，覆盖 31 省、156 区市县、624 村/居委会，每轮访问 7000–10000 余家庭，可推论全国 18–69 周岁住户人口。
- 门槛：免费为主；CHNS 家庭/个人数据同意条款后下载、社区数据需 DUA；CSS 需注册/申请；CHIP 需申请。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA：`https://www.cpc.unc.edu/projects/china` → 200（33,509 B）；`…/projects/china/data/datasets` → 200（33,183 B，数据说明）；`…/about/design` → 200（32,538 B）；`http://css.cssn.cn/css_sy` → 200（28,063 B，CSS 项目介绍与历年数据）；CSS 申请系统 `http://skycss.haoboyihai.com:8099/skyuser/user_center/` → 200（17,106 B，标题「用户中心-中国社会综合状况调查」）。
- 上游：CHNS——北卡罗来纳大学人口中心（UNC CPC）与中国疾控中心营养与健康所；CSS——中国社会科学院社会学研究所；CHIP——中外研究者合作的收入分配项目（详见 CNSDA）。

## 细节

- CSS 历年数据与申请说明：`http://css.cssn.cn/css_sy/zlysj/lnsj/`；「历年数据申请方式说明」单页 `…/zlysj/lnsj/202209/t20220926_5541891.html`。
- CHNS 数据说明：家庭与个人层主文件在 Dataverse 下载（**SAS 格式**）；社区层需提交 data use agreement 并经项目主任批准；生物标记物另有入口。
- CHIP 在 CNSDA 有各期项目页，早期年份另有英文条目（如 `Chinese Household Income Project, 1988`），摘要含收入与住房等变量描述。
- 三者均为**老牌经典**调查，最新波次距今较远，跨源合用时注意年份口径。

## 坑

- CSS 数据申请系统域名（`skycss.haoboyihai.com:8099`）非 cssn.cn 主域，**须以官网链接为准**；本机实测 200，但属第三方托管。
- CHNS 主文件仅 SAS 格式，需 SAS 或可读 SAS 的工具；社区数据不能直接从 Dataverse 取。
- 北京师范大学中国收入分配研究院 `ciid.bnu.edu.cn` 本机不可达（HTTP/HTTPS 均连接失败），CHIP 最新资料改走 CNSDA 与项目方。
