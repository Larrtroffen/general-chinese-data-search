# drug-procurement —— 药品集采中选与目录

- 去哪找：
  - **上海阳光医药采购网**（上海市医药集中招标采购事务管理所；国家组织药品联合采购办公室发布口）`https://www.smpaa.cn/`——国家组织医药集中采购栏目 `https://www.smpaa.cn/gjsdcg/index.shtml`、公告列表 `https://www.smpaa.cn/gjsdcg/index_gg.shtml`、站内检索 `https://www.smpaa.cn/search.shtml?searchContent=<词>`。
  - **国家医保局·药品和耗材集中带量采购·国家组织集中采购**专栏 `https://www.nhsa.gov.cn/col/col187/index.html`（转载 smpaa 结果，正文 `…/art/{y}/{m}/{d}/art_187_<id>.html`）。
  - **国家医保药品目录**——目录 PDF 下载 `https://www.nhsa.gov.cn/module/download/downfile.jsp?classid=0&filename=<hash>.pdf`；查询入口 `https://wx.nhsa.gov.cn/#/pages/NRDL/index/index`；国家医保服务平台 `https://fuwu.nhsa.gov.cn/`；发布通知见政策法规 `https://www.nhsa.gov.cn/col/col104/index.html`、通知公告 `…/col/col109/index.html`。
  - **基本药物目录**——国家药监局数据查询平台「国家基本药物（2018 年版）」子库（`itemId=2c9ba384759c957701759cc91ecf029e`，见 `nmpa.md`）；卫健委委业务栏目 `nhc.gov.cn` 的 `jbywmlcx/`（基本药物目录查询，全站 412，见 `nhc.gov.cn.md`）。
- 什么时候用：要历批**国家组织药品集中带量采购**的中选结果与中选价、中选品种供应清单、拟中选公示、企业信息/关联关系公示、中选药品信息变更与取消资格公告、开标与执行提示；要**国家基本医疗保险、生育保险和工伤保险药品目录**（西药/中成药/协议期内谈判药品/中药饮片）清单及每年调整通知；要**国家基本药物目录**。
- 怎么搜：
  - **smpaa 是服务端渲染的 `.shtml` 静态站，无 JSON API**：栏目列表 → 文章正文 → 附件 PDF 三步。列表分页为「页码直接拼数字」——第 2 页是 `index_gg2.shtml`（`?page=2` 会被忽略）；文章附件在 `/mhwz/docResource/docFiles/<YYYYMMDD>/<名称>_<时间戳>.pdf`，可直接下。
    ```bash
    UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    curl -sS -A "$UA" 'https://www.smpaa.cn/gjsdcg/index_gg.shtml'        # 公告列表（第 2 页 …/index_gg2.shtml）
    curl -sS -A "$UA" 'https://www.smpaa.cn/gjsdcg/2026/08/06/23603.shtml' # 第12批中选结果通知 → 正则取附件 href
    ```
  - **nhsa**：`col187` 分类列表 → `art_187_*` 正文 → 附件经 `downfile.jsp?classid=0&filename=<hash>.pdf` 直连 PDF；站内检索 `https://www.nhsa.gov.cn/jrobot/search.do?webid=1&pg=10&p=1&tpl=1&category=&q=<词>`（HTML，见 `../surveys/social-insurance.md`）。
  - 结果形态：**HTML**（列表/正文）+ **PDF**（集采中选结果表、供应清单；医保目录）；**目录查询入口是 SPA，仅浏览器**。
- 覆盖：国家组织药品集采**第 1–12 批**（第 12 批采购文件 `GY-YD2026-1` 于 2026-08-06 公布中选结果，另有复方氨基酸注射剂等专项/接续与信息变更公告，结果文章在 smpaa 长期保留）；医保药品目录历年版（含 2024 版、2025 版及 2026 年调整方案，通知随 `col104/col109` 发布）；基本药物目录（2018 年版，NMPA 平台可按类别/品种检索）。
- 门槛：**免费、无需登录、无 key**；smpaa 与 nhsa 均可用桌面 UA 的 `curl` 直取，PDF 可下。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA，20–25 s 超时，同主机 ≥1.5 s 间隔：
  - `curl 'https://www.smpaa.cn/gjsdcg/index_gg.shtml'` → **200**（12,804 B，20 条/页）；`…/index_gg2.shtml` → **200**（13,124 B，条目与第 1 页不同）✅；`…/index_gg_2.shtml` → **404**；`…/index_gg.shtml?page=2` → **200 但内容与第 1 页相同**（参数被忽略）⚠️
  - 文章 `https://www.smpaa.cn/gjsdcg/2026/08/06/23603.shtml` → **200**（11,604 B），正文含附件 `/mhwz/docResource/docFiles/20260806/第12批国家组织药品集中带量采购中选结果表（GY-YD2026-1）_202608061786007462909.pdf`；该 PDF → **200 `application/pdf`**（267,962 B，`%PDF-1.7`）✅
  - `https://www.smpaa.cn/search.shtml?searchContent=集采` → **200** HTML 结果页 ✅
  - `https://www.nhsa.gov.cn/col/col187/index.html` → **200**（24,935 B，含 `art_187_*` 列表）；`https://www.nhsa.gov.cn/art/2025/12/7/art_104_18970.html`（2025 版药品目录通知）→ **200**，附 2 个 `downfile.jsp` 附件 ✅
  - `curl -r 0-200 'https://www.nhsa.gov.cn/module/download/downfile.jsp?classid=0&filename=de66e92b7edd4056ac41c0c4d3c011f3.pdf'` → **206 `application/pdf`**，`Content-Range: bytes 0-200/1459033`，体首 `%PDF-1.7`（2024 版目录）✅
  - `https://wx.nhsa.gov.cn/#/pages/NRDL/index/index` → **200**（555 B，SPA 外壳，**仅浏览器**）；`https://fuwu.nhsa.gov.cn/` → 200（跳转壳）⚠️
  - 基本药物（2018 版）经 NMPA 数据查询平台子库检索命中，见 `nmpa.md`。
- 上游：上海阳光医药采购网 `https://www.smpaa.cn/`（上海市医药集中招标采购事务管理所）；国家医疗保障局 `https://www.nhsa.gov.cn/`；国家药品监督管理局 `https://www.nmpa.gov.cn/`。

## 细节

### 一、上海阳光医药采购网（smpaa.cn）

| 内容 | URL 形态 | 说明 |
|---|---|---|
| 国家组织医药集中采购（总栏） | `/gjsdcg/index.shtml` | 动态 + 公告两个子栏 |
| 集采动态 / 公告 | `/gjsdcg/index_dt.shtml` / `/gjsdcg/index_gg.shtml` | 公告第 N 页 = `/gjsdcg/index_gg<N>.shtml` |
| 集采文章 | `/gjsdcg/{yyyy}/{mm}/{dd}/{id}.shtml` | 中选结果/公示/变更原文 |
| 文章附件 | `/mhwz/docResource/docFiles/{yyyymmdd}/<中文名>_<时间戳>.pdf` | 中选结果表、供应清单等 |
| 信息公开·公告公示 | `/xxgk/gggs/index_zhaobiao.shtml`（招标）/ `index_zhongbiao.shtml`（**结果公布**）/ `index_gengzheng.shtml`（信息变更）/ `index_qt.shtml`（其他） | 上海本地招采口径 |
| 政策知识库 | `/xxgk/zczsk/index_fg.shtml`（国家）/ `index_jd.shtml`（上海） | 集采政策文件 |
| 站内检索 | `/search.shtml?searchContent=<词>` | HTML 结果页（≥2 字） |
| 网站地图 | `/wzMap.shtml` | 全站栏目索引（便于枚举栏目） |

- 网站由上海市医药集中招标采购事务管理所运营；国家组织药品联合采购办公室的中选结果、拟中选公示、企业信息变更等**首发于此**，国家医保局 `col187` 为转载。

### 二、国家医保局（nhsa.gov.cn）

| 内容 | URL 形态 | 形态 |
|---|---|---|
| 集采专栏（药品和耗材集中带量采购·国家组织集中采购） | `https://www.nhsa.gov.cn/col/col187/index.html` | 静态列表 HTML |
| 集采文章 | `https://www.nhsa.gov.cn/art/{y}/{m}/{d}/art_187_<id>.html` | 正文 HTML（附件多为 smpaa 转载） |
| 医保目录通知（政策法规/通知公告） | `/col/col104/index.html`、`/col/col109/index.html` | 静态列表 |
| 目录/附件下载 | `/module/download/downfile.jsp?classid=0&filename=<hash>.pdf` | **PDF 直链**（需从文章页取 `filename`） |
| 目录查询入口 | `https://wx.nhsa.gov.cn/#/pages/NRDL/index/index` | SPA（仅浏览器） |
| 国家医保服务平台 | `https://fuwu.nhsa.gov.cn/` | 政务服务门户 |
| 站内检索（jrobot） | `/jrobot/search.do?webid=1&pg=10&p=1&tpl=1&category=&q=<词>` | HTML 结果页 |

- 历年医保药品目录正式 PDF 经 `downfile.jsp` 发布；`filename` 是**内容哈希**（如 2024 版 `de66e92b7edd4056ac41c0c4d3c011f3.pdf`，约 1.43 MB），**不能凭规则拼**，须从对应文章页/列表页解析后下载。
- 目录结构分四部分：西药、中成药、协议期内谈判药品（含竞价）、中药饮片。

### 三、基本药物目录

- **国家药监局数据查询平台**「国家基本药物（2018 年版）」子库（`itemId=2c9ba384759c957701759cc91ecf029e`）可按类别/品种检索明细，行字段 `{f0:大类, f1:类别, f2:功能, f3:品种, f4:序号}`（见 `nmpa.md`）。
- 官方发布与政策口径在**国家卫健委**（`nhc.gov.cn` 的 `jbywmlcx/` 基本药物目录查询；全站 412 WAF，见 `nhc.gov.cn.md`、`../gov/edu-research-institutions.md`）。

## 坑

1. **smpaa 分页是「页码拼进文件名」而非查询参数**：第 2 页为 `index_gg2.shtml`（无下划线）；实测 `index_gg_2.shtml` → 404、`index_gg.shtml?page=2` → 200 但返回第 1 页内容（静默失效）。翻页务必按 `index_gg<N>.shtml`。
2. **smpaa 无 JSON API**，列表与正文都是可直取的 `.shtml`；不要找 XHR。
3. **首发 vs 转载**：集采中选结果的原始件（含中选价、供应清单）在 **smpaa**，nhsa `col187` 多为转载或摘要；引用落 **smpaa 附件 PDF**，并记采购文件编号（`GY-YD<年>-<批>`）。
4. **医保目录 PDF 的 `filename` 是哈希**：`downfile.jsp` 不能靠命名规则构造，必须从文章页解析；同一内容哈希换版本即变。
5. **目录查询入口是 SPA**：`wx.nhsa.gov.cn` 与 `fuwu.nhsa.gov.cn` 都是前端路由站，`curl` 只拿到外壳（555 B），**仅浏览器**。
6. 集采按批次滚动、含**接续/专项/信息变更**（如复方氨基酸注射剂、胰岛素等），同一品种可能多次调整中选价；统计"中选结果"时须按批次 + 公告日期去重。
7. 基本药物目录官方发布在卫健委（412 WAF），NMPA 平台的 2018 版子库便于逐品种查询，但**政策与增补口径以卫健委为准**。
