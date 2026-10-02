# permit.mee.gov.cn —— 排污许可证信息公开

- 去哪找：全国排污许可证管理信息平台·公开端 `http://permit.mee.gov.cn/`（首页 JS 跳转到 `/permitExt/defaults/default-index!getInformation.action`）；公告详情 `/permitExt/syssb/xxgk/xxgk!showggfk.action?pkid=<32位id>`。
- 什么时候用：要**某企业是否取得排污许可证**、许可证申请受理/拟批准/批准公告、变更与延续记录；做企业环境合规核验、污染源名录；配合 IPE（[`ipe.org.cn.md`](ipe.org.cn.md)）的企业环境监管记录一起看。
- 怎么搜：公开端首页即「信息公开」列表（受理/拟批准/批准公告、新闻），条目链接带 `pkid`（UUID）与类型参数，URL 可直接打开、正文 HTML；平台内「许可证信息查询 / 登记信息」入口（`getRegisterInfo.action`）会 302 到 **CAS 统一登录**。旧的 `xkgg!licenseInformation.action` 已废弃，会跳到提示页。
- 覆盖：全国 · 排污许可证核发公告（滚动更新，按日）；企业许可证正本信息（登录后）· 企业级。
- 门槛：公告列表与详情 **免费匿名**；**许可证详细信息/登记信息需登录**（CAS 账号）。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA）——`http://permit.mee.gov.cn/` → 200，返回 124 B JS 跳转页；`/permitExt/defaults/default-index!getInformation.action` → 200（135,290 B，标题「全国排污许可证管理信息平台-公开端」，含多个 `xxgk!showggfk.action?pkid=…` 公告链接）；`/permitExt/syssb/xkgg/xkgg!licenseInformation.action` → 跳 `…/perxxgkinfo/errorinfo.jsp`，提示「请访问 permit.mee.gov.cn 点击许可信息公开查询」；`/permitExt/defaults/getRegisterInfo.action` → 302 → `https://permit.mee.gov.cn/cas/login?service=…`（200 登录页）。
- 上游：生态环境部（全国排污许可证管理信息平台）。

## 细节

- 公开端动作 URL 规律：`/permitExt/syssb/xxgk/xxgk!showggfk.action?pkid=<uuid>`（公告详情）、`/permitExt/defaults/default-index!getInformation.action`（信息公开首页）、`/permitExt/defaults/getRegisterInfo.action`（登记信息，需登录）。
- 详情页附件走 `/permitExt/syssb/xxgk/showImage.action?dataid=<id>`。
- 平台依赖 Baidu 统计与 jQuery 校验脚本，列表数据在 HTML 中直接渲染（无需额外 XHR）。

## 坑

1. **无公开批量接口**：公告是逐条 HTML，`pkid` 无法从外部枚举；要全量只能翻列表页/用搜索引擎站内检索。
2. 许可证**正本/副本信息**（排放口、许可排放量）在登录后系统里，公开端只给公告性材料；企业自行公开的信息可能不完整。
3. 主站域名为 `permit.mee.gov.cn`（生态环境部二级域），部分镜像写作 `permit.mee.gov.cn/permitExt/…`，路径大小写敏感（`xxgk` 小写）。
4. 与「全国污染源监测数据管理与信息共享平台」不是同一入口，后者在生态环境部数据中心体系内，需另找（本卡未实测）。
