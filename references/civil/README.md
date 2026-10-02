# civil/ —— 公益·慈善·基金会·志愿服务源

本层收录**公益慈善、基金会、志愿服务**方向的官方与半官方入口：基金会名录与透明指数、慈善组织信息公开、志愿服务平台、互联网公益平台项目页，以及行业协会/媒体指标。

## 文件一览

| 文件 | 来源 | 用途 | 状态 |
|---|---|---|---|
| `cszg.mca.gov.cn.md` | 民政部·慈善中国 | 慈善组织信息公开、募捐备案、年度工作报告（组织登录端） | ⚠️ 需登录 |
| `foundationcenter.org.cn.md` | 基金会中心网 | 全国基金会名录/分面计数/FTI 透明指数 JSON 接口 | ✅ 接口可用 |
| `cvf.org.cn.md` | 中央社会工作部 | 志愿服务协同平台：志愿者/队伍/项目（旧「中国志愿服务网」已关停） | ⚠️ 需登录 |
| `love.alipay.com.md` | 支付宝公益平台 | 公益项目列表页与项目详情（GBK） | ✅ 可用 |
| `gongyi.qq.com.md` | 腾讯公益 | 乐捐项目列表/详情；检索 JSON 接口直连被拒 | ⚠️ 检索需浏览器 |
| `charityalliance.org.cn.md` | 中国慈善联合会 | 会员名单/年度报告/慈善标准/行业资讯 | ✅ 可用 |
| `cfforum.org.cn.md` | 中国基金会发展论坛 | 《基金会蓝皮书》、历届年会资料、行业报告 PDF | ✅ 可用 |
| `gongyishibao.com.md` | 公益时报 | 公益行业新闻、《公益时报》数字报（仅 HTTP） | ✅ 可用 |

## 选路

- **要全国基金会名录/行业分面统计，或 FTI 中基透明指数** → `foundationcenter.org.cn.md`：`api.foundationcenter.org.cn/api` 的 `SearchConditionsList`/`SearchTipList`/`Visualization/FTI` 免登录直出 JSON；单机构详情与基金会列表检索需登录（`code:10`）。
- **核查某基金会/社会组织的登记与年检** → `../gov/chinanpo.md`（社会组织信用信息公示平台，免登录）；「慈善中国」`cszg.mca.gov.cn.md` 是**报送端**，全站需组织账号登录。
- **要志愿服务项目/队伍/志愿者数据** → `cvf.org.cn.md`：走**中国志愿服务协同平台**（`cvf.org.cn/xtpt`，需注册登录）；旧站 `chinavolunteer.mca.gov.cn` 已于 2026-07-20 停止服务，勿再用。
- **要互联网公益募捐项目** → 平台公开页并列取：`gongyi.qq.com.md`（腾讯乐捐，详情页可抓、检索接口需浏览器）+ `love.alipay.com.md`（支付宝公益，GBK 转码后抓）。
- **要基金会行业报告/蓝皮书/年会资料** → `cfforum.org.cn.md`（`/Uploads/file/` PDF 直链可下）；**要慈善行业资讯与会员/标准** → `charityalliance.org.cn.md`；**要行业新闻与数字报** → `gongyishibao.com.md`（仅 HTTP）。
- 第三方聚合/媒体（`suchajun.com`、善达网、中国发展简报）只作线索，正式引用回本层官方卡或民政部口径。

## 相关

- 社会组织登记/年检核查：[`../gov/chinanpo.md`](../gov/chinanpo.md) —— 「慈善中国」的组织数据与之一致，公开查询优先用信用信息公示平台。
- 基金会财务/捐赠的宏观口径与年鉴：[`../stats/ministry-stats.md`](../stats/ministry-stats.md)、[`../stats/`](../stats/README.md)。
- 企业/ESG 与商业数据库：[`../business/`](../business/README.md) —— 企业基金会/CSR 交叉。
- 上游总表与用法：仓库根 `SKILL.md`；候选与进度见根 `CANDIDATES.md`。
