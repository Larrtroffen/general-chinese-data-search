# university-ss-data —— 高校社科数据平台总表

我国高校的社科数据/调查平台分散在各校自建门户，无统一域名规律；本卡做一张「要哪类数据 → 去哪家校」的对照表，并标注本机可达性。

- 去哪找：各校入口见「细节」表；独立成卡的有复旦（`rdr.fudan.edu.cn.md`）、清华（`tcdc.sem.tsinghua.edu.cn.md`）、厦大（`econpub.xmu.edu.cn.md`）。
- 什么时候用：要找**高校侧的社科数据集/调查数据/共享平台**，但不知道是哪家、入口在哪；要判断某平台是公开可下还是校内受限。
- 怎么搜：先按数据类型定位学校 → 再进对应平台。**没有跨校聚合接口**，只能逐校探测；DOI 型数据可回到 `../repos/` 的 Dataverse/Zenodo 检索。
- 覆盖：见「细节」表（10 家高校/平台），从数据仓储、微观数据开发到调查数据申请。
- 门槛：多数**校内账号 / 统一身份认证**；少数目录页公开可见。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA，逐站 GET（状态见各行）。
- 上游：各校平台官方入口。

## 细节

| 学校 | 平台 | 入口 | 类型 | 本机实测 |
|---|---|---|---|---|
| 复旦 | 社会科学数据平台 | `https://rdr.fudan.edu.cn/datahome/` | 数据仓储+变量检索 | ✅ 200（SPA）→ `rdr.fudan.edu.cn.md` |
| 清华 | 中国经济社会数据研究中心 | `http://www.tcdc.sem.tsinghua.edu.cn/` | 微观数据开发 | ✅ 200 → `tcdc.sem.tsinghua.edu.cn.md` |
| 厦大 | 经济学科研究共享平台 | `https://econpub.xmu.edu.cn/elib/` | 数据集/代码共享 | ✅ 200（申请需微信认证）→ `econpub.xmu.edu.cn.md` |
| 北大 | 中国社会科学调查中心（ISSS） | `https://www.isss.pku.edu.cn/` | CFPS 等调查 | — 见 `../surveys/cfps.md` |
| 人大 | 中国调查与数据中心 / CNSDA | `http://nsrc.ruc.edu.cn/` · `https://www.cnsda.org/` | 调查数据仓储 | — 见 `../surveys/cnsda.org.md` |
| 中山大学 | 社会科学调查中心（CLDS） | 经 CNSDA 项目页 | 追踪调查 | — 见 `../surveys/clds.md` |
| 西南财大 | 中国家庭金融调查（CHFS） | `https://chfser.swufe.edu.cn/data/` | 家庭金融调查 | — 见 `../surveys/chfs.md` |
| 浙大 | 中国家庭大数据库（CFDB） | `https://ssec.zju.edu.cn/` | 家庭追踪 | — 见 `../surveys/cfdb.md` |
| 武大 | 经济与管理学院（企研·社科大数据平台机构版；武大-北大城市营商环境数据库） | `https://ems.whu.edu.cn/` | 院系数据服务 | ⚠️ 未逐个实测（上游声明） |
| 高校联合 | 中国高校社会科学数据中心 | `https://cweb.csdc.info/` | 高校社科数据 | ❌ 本机连接超时（DNS `122.205.5.253` 有解析） |

- **武大**：院系以采购/试用「企研·社科大数据平台（机构版）」向师生提供数据（`ems.whu.edu.cn/info/7808/257261.htm`，上游声明）；另与北大联合发布「中国城市营商环境数据库」（`ems.whu.edu.cn/info/1587/215141.htm`，上游声明）。
- **南大**：图书馆数字资源里挂「中国经济社会大数据研究平台」（知网系，见 `../stats/cnki-data.md`）；未见校级独立社科数据平台。
- **中国高校社会科学数据中心**（`cweb.csdc.info`）：本机 12 s 连接超时，**不可达**；引用前先重新探测。

## 坑

1. 高校平台**无统一规律**：`rdr.`、`econpub.`、`isss.`、`nsrc.`、`ssec.` 各校自定，只能靠「学校+数据平台」搜或本表。
2. 高校自建平台多为 **SPA + 统一身份认证**，脚本难直取；能匿名拿的通常是目录/元数据，**数据本体要校内账号**。
3. 调查类微观数据（CFPS/CGSS/CHARLS/CHFS/CLDS/CFDB）**统一走 `../surveys/`**，本卡不重复其申请流程。
4. `cweb.csdc.info` 本机不可达 ≠ 已停运，可能是网络边界；别据此下结论。
