# microdata-access —— 微观调查数据获取路线图

- 去哪找：分发平台是入口，不是各家官网。国内：PKU Dataverse `https://opendata.pku.edu.cn/`、CNSDA 中国国家调查数据库 `https://www.cnsda.org/`、CHARLS 数据门户 `https://charls.charlsdata.com/`、CHFS 数据服务系统 `https://chfser.swufe.edu.cn/datasso/`、国家统计局微观数据 `https://microdata.stats.gov.cn/`。国际：IPUMS `https://www.ipums.org/`、ICPSR `https://www.icpsr.umich.edu/`、GESIS `https://www.gesis.org/`（检索 `https://search.gesis.org/`）、UK Data Service `https://ukdataservice.ac.uk/`、Harvard Dataverse `https://dataverse.harvard.edu/`。
- 什么时候用：要的是**个体 / 家户 / 企业级原始数据**（问卷级、可自己设口径跑回归），而不是年鉴汇总表；或要判断「这份调查数据我能不能拿到、要多久、要不要钱、怎么交付」。
- 怎么搜：分三步——**①定位**：先在 Dataverse 的 JSON 检索接口确认数据集在不在、DOI 是多少（见「细节·检索接口」）；**②判权限层**：公开直下 → 注册即下 → 提交研究计划等审批 → 机构 IP → 现场机房；**③按层走入口**：注册下载类走各库 sign_up，审批类走申请表单/机构通道。
- 覆盖：国内 CFPS / CGSS / CHARLS / CLDS / CHFS / CEPS / CHIP / CHNS、国家统计局微观数据；国际 IPUMS / ICPSR / GESIS / UKDS / Dataverse（Harvard、PKU）。年份视各 wave 而定（多为 2008 起多轮追踪）。
- 门槛：从「免费注册」到「机构会员 / 审批 / 付费」不等，逐库见速查表；**多数库的数据下载页匿名 curl 打不开主页以外的内容**（IPUMS / ICPSR / GESIS 被 Cloudflare 挡，需浏览器）。
- 实测：2026-10-03，macOS arm64，curl 8.x，桌面 UA，同主机 ≤3 请求、间隔 ≥1.5 s；仅验证入口可达性与检索接口，**未注册账号、未走完真实申请**；「谁可申请 / 时长 / 费用」凡未经本机验证的一律标「（上游声明）」。
- 上游：各库官网 / 数据门户（入口见上）。

> 申请流程和时长随机构政策变动，**以入口页最新公告为准**；本卡的「时长 / 费用」列只作路线参考，未本机实测。

## 细节

### 速查表

| 库 | 分发入口（实测） | 谁可申请 | 交付 / 门槛 | 费用 | 核实度 |
|---|---|---|---|---|---|
| CFPS 中国家庭追踪调查 | `opendata.pku.edu.cn/dataverse/CFPS`（北大 Dataverse） | 高校/科研研究者（实名注册） | 在线下载含 DOI 的 wave 数据集 | 免费（上游声明） | 入口 ✅ |
| CGSS 中国综合社会调查 | `cgss.ruc.edu.cn` → CNSDA `cnsda.org` | 研究者 / 机构 | CNSDA 注册申请后下载 | 免费（上游声明） | 入口 ✅ |
| CHARLS 健康与养老追踪 | `charls.charlsdata.com/pages/data/111/zh-cn.html` | 研究者（注册+同意协议） | 按 wave 在线下载 | 免费（上游声明） | 入口 ✅ |
| CLDS 劳动力动态调查 | `css.sysu.edu.cn` | 研究者 | 申请制（上游声明） | — | ❌ 本机超时 |
| CHFS 中国家庭金融调查 | `chfser.swufe.edu.cn/datasso/` | 研究者（注册/登录） | 数据服务系统内下载 | 免费（上游声明） | 入口 ✅ |
| CEPS 中国教育追踪调查 | `ceps.ruc.edu.cn` | 研究者 | 申请制（上游声明） | — | 入口 ✅ |
| CHIP 收入分配课题组 | 北师大 / CIID 门户（未核实） | — | — | — | ❌ 未解项 |
| CHNS 健康与营养调查 | `chns.cpc.unc.edu`（UNC CPC） | 注册用户 | 免费注册后下载 | 免费（上游声明） | 入口 ✅ |
| 国家统计局微观数据 | `microdata.stats.gov.cn` | 机构 / 研究者申请 | 申请制，部分须到指定场所使用（上游声明） | — | 入口 ✅ |
| IPUMS | `ipums.org` | 注册研究者 | 在线定制 extract | 免费（上游声明） | ⚠️ CF 挡 curl |
| ICPSR | `icpsr.umich.edu` | 成员机构成员 / 非成员申请 | 会员 IP 直下；非成员按件 | 成员免费 / 非成员付费 | ⚠️ CF 挡 curl |
| GESIS | `gesis.org` / `search.gesis.org` | 注册研究者 | 注册后下载，部分签协议 | 免费（上游声明） | ⚠️ CF 挡 curl |
| UK Data Service | `ukdataservice.ac.uk/find-data/` | 注册用户（国际用户需申请） | 注册后下载；Special Licence 需审批 | 多数免费 | 入口 ✅ |
| Harvard / PKU Dataverse | `dataverse.harvard.edu` / `opendata.pku.edu.cn` | 任何人（公开数据集） | 免登录直下，走 API | 免费 | ✅ API 实测 |

### 检索接口：先定位再申请（Dataverse 通用 JSON API）

PKU 与 Harvard 都是 Dataverse 实例，**API 同构**，可匿名调用，用来确认「这份数据在不在、DOI 是多少、有几个文件」：

```bash
# 在北大平台找 CFPS / CHARLS
curl -s 'https://opendata.pku.edu.cn/api/search?q=CFPS&type=dataset&per_page=10'
curl -s 'https://opendata.pku.edu.cn/api/search?q=CHARLS&type=dataset&per_page=10'
# 在 Harvard Dataverse 找（量级参照）
curl -s 'https://dataverse.harvard.edu/api/search?q=china+survey&type=dataset&per_page=2'
# 单数据集元数据（含文件清单）
curl -s 'https://opendata.pku.edu.cn/api/datasets/:persistentId?persistentId=doi:10.18170/DVN/SXKEWK'
```

- 返回：`{"status":"OK","data":{"q":…,"total_count":N,"start":0,"items":[{name,type,url,global_id,description,…}]}}`。
- 参数：`q` 关键词、`type=dataset|dataverse|file`、`per_page`、`start`（翻页）、`sort=date|name`、`order=asc|desc`、`fq`（字段过滤）；分页用 `start + per_page` 对 `total_count`。
- 实测：PKU `q=CFPS&type=dataset` → 200，`total_count=4`；`q=CHARLS` → `total_count=4`，首条 `China Health and Retirement Longitudinal Study（2008 pilot survey）`，`global_id=doi:10.18170/DVN/SXKEWK`。Harvard `q=china survey&type=dataset` → 200，`total_count=81060`；`GET /api/info/version` → `6.10.1`。
- 注意：PKU 站点的 `/api/info/version` 返回 **403（Apache）**，但 `/api/search` 正常——别因单个路径 403 就判定 API 全挂。

### 国内各库的入口与申请路径

- **CFPS**：官网 `www.isss.pku.edu.cn/cfps/`（200）页内直指北大开放研究数据平台的 CFPS 子库；数据带 DOI（`10.18170/DVN/…`），注册后按 wave 下载。（上游声明）
- **CGSS**：官网 `cgss.ruc.edu.cn`（200），页脚外链 **CNSDA 中国国家调查数据库** `www.cnsda.org`——CGSS 的实际分发在 CNSDA，走 `index.php?r=projects/index` 项目页。（上游声明）
- **CHARLS**：`charls.pku.edu.cn`（200）→ 数据门户 `charls.charlsdata.com`，实测 `pages/data/111/zh-cn.html` 列出 2008 pilot、2011/2013/2015/2018 各 wave 页；注册入口 `users/sign_up/agreement`（需先同意使用协议）。（上游声明）
- **CHFS**：`chfs.swufe.edu.cn`（200）→ 数据服务系统 `chfser.swufe.edu.cn/datasso/`（200），实测含 `CasLogin` / `Regeist`（注册）/ `ForgetPwd`，注册后在线下载。
- **CEPS**：`ceps.ruc.edu.cn`（200）；数据申请入口需在站内按「数据申请」导航走（本机未展开）。
- **CLDS**：`css.sysu.edu.cn` **本机连接超时（18 s）**，未能核实；换网络或走中山大学社科调查中心其它入口再试。
- **CHIP**：中国收入分配课题组住户调查，归属北师大/CIID；**分发入口本机未核实**（未解项），需向课题组/所属机构确认后再写卡。
- **CHNS**：官网 `www.cpc.unc.edu/projects/china` → 301 到 `chns.cpc.unc.edu`（200）；免费注册后下载各 wave。（上游声明）

### 通用申请路线（三步）

1. **定位**：Dataverse `/api/search` 打关键词，或 CNSDA 项目页 / 各库官网找「数据下载 / 数据申请」。
2. **判权限层**（决定要做什么）：
   - 公开直下（Dataverse 公开数据集、部分 OWID 类数据）；
   - 注册即下（CFPS/CHARLS/CHFS/CHNS/IPUMS/UKDS——填实名 + 同意使用协议）；
   - 提交申请审批（国家统计局微观数据、CNSDA 部分、ICPSR 非成员、UKDS Special Licence）；
   - 机构 IP / 会员（ICPSR 成员校）；
   - 现场机房（部分高敏微观数据，须在指定场所使用）。
3. **按层走**：注册类直接建号下载 zip（常附 do/dta/sav 与问卷代码本）；审批类备研究计划、机构证明。**引用时带 DOI / 数据集版本。**

### 探测记录（2026-10-03，macOS arm64，curl 8.x，桌面 UA，同主机 ≤3 请求、间隔 ≥1.5 s）

| host | 状态码 | 观察 |
|---|---|---|
| www.isss.pku.edu.cn | 200 | CFPS 官网；页内链向 `opendata.pku.edu.cn/dataverse/CFPS` |
| opendata.pku.edu.cn | 200 / 200 / 403 | `/api/search?q=CFPS`=4 条、`q=CHARLS`=4 条；`/api/info/version` → 403 |
| cgss.ruc.edu.cn | 200 | 官网；外链 `cnsda.org` |
| nsrc.ruc.edu.cn | 200 | 人大中国调查与数据中心；CGSS 项目页 `dcxm/zgzhshdc_CGSS/index.htm` |
| www.cnsda.org | 301 → 200(-k) | http→https 跳转；**HTTPS 证书已过期**，`curl -k` 才 200 |
| charls.pku.edu.cn | 200 | 官网，链向 charlsdata.com 注册/协议页 |
| charls.charlsdata.com | 200 | 数据页列出各 wave |
| chfs.swufe.edu.cn | 200 | 官网，链向 chfser |
| chfser.swufe.edu.cn | 200 | `/datasso/`，含登录/注册 |
| ceps.ruc.edu.cn | 200 | 官网 |
| css.sysu.edu.cn | 000 | **连接超时（18 s）**，CLDS 未核实 |
| www.cpc.unc.edu | 301 → chns.cpc.unc.edu 200 | CHNS |
| microdata.stats.gov.cn | 200 | SPA 外壳（682 B） |
| www.ipums.org | 403 | Cloudflare「Just a moment…」（桌面 UA 与裸 UA 均 403） |
| www.icpsr.umich.edu | 403 | Cloudflare 挑战 |
| www.gesis.org / search.gesis.org | 403 | Cloudflare 挑战 |
| ukdataservice.ac.uk | 200 / 200 | 首页与 `/find-data/` |
| dataverse.harvard.edu | 200 / 200 | search API 81060 条；version 6.10.1 |
| data.stats.gov.cn | 200 / 403 | 首页 200；`easyquery.htm` JSON 端点 → **403 UrlACL（本机 IPv6 出口被拦）** |

## 坑

- **Cloudflare「Just a moment…」≠ 站点挂了**：IPUMS / ICPSR / GESIS 对匿名 curl 一律 403，必须用真实浏览器（或带浏览器指纹的会话），本卡只能记入口。
- **CNSDA 的 HTTPS 证书已过期**：http 会 301 到 https 然后 SSL 失败，需 `curl -k` 或浏览器忽略警告。
- **CLDS（`css.sysu.edu.cn`）本机网络不可达**：别把「连不上」当「没有这个库」。
- **时长 / 费用多为上游声明**：申请制库要账号才能走完流程，本机未实注册；用前以入口页公告为准。
- **同一份数据的入口可能不止一个**（官网 / Dataverse / CNSDA），且**版本与 DOI 不同**——引用时记清来源平台与数据集版本。
- **别只信官网导航**：CFPS、CHARLS 这类官网首页很薄，真正的数据在 Dataverse / charlsdata 等**独立数据域**，先检索接口再谈申请。
