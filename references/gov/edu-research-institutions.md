# edu-research-institutions —— 高校与科研机构名录核实

- 去哪找：
  - 教育部·全国高等学校名单（专栏，历年入口）：`https://www.moe.gov.cn/jyb_xxgk/xxgk/neirong/fenlei/sxml_gdjy/gdjy_gxsz/gxsz_xxmd/`
  - 教育部·学位管理与研究生教育司（国务院学位委员会办公室）公告栏：`http://www.moe.gov.cn/jyb_xxgk/s5743/s5744/A22/`
  - 学信网：`https://www.chsi.com.cn/`；研招网（招生单位/专业目录）：`https://yz.chsi.com.cn/zsml/`；阳光高考院校库：`https://gaokao.chsi.com.cn/`
  - 中国科学院·机构设置（院属机构名录）：`https://www.cas.cn/zz/jg/`；社科院·组织机构：`http://www.cass.cn/ywzzjg/`
  - 中国科协：`https://www.cast.org.cn/`；全国学会办事大厅：`https://bsdt-kc.cast.org.cn/index`
  - 国家卫健委·查信息（查询应用目录）：`https://zwfw.nhc.gov.cn/cxx/`；全国医疗机构查询：`https://zgcx.nhc.gov.cn/unit`
- 什么时候用：给定**单位名称**要核实"是否为正规高校/科研机构、官网是哪、资质/备案情况"——机构新闻与研究的背景核查；关键词如"XX学院 是不是正规高校""XX研究所 隶属""双一流/学位授权点""医疗机构执业登记""学会 挂靠单位"。
- 怎么搜：**以教育部名单为权威底本**（能下 XLS 全校逐一比对），院校官网/资质走**学信网—研招网**，科研机构走**各院自己的机构名录页**，医疗机构走**卫健委查询应用**；需检索而非名单时用**教育部站内检索** `https://so.moe.gov.cn/s?qt=<词>`。逐源操作见 `## 细节`。
- 覆盖：全国普通高校 + 成人高校（2006→2026 逐年名单，2026 版 3 196 所）；研究生招生单位/专业目录（研招网，当期）；双一流名单（第一/二轮）；中科院院属机构（含分院与研究所，188 个链接）；社科院研究所；科协全国学会（办事大厅）；全国医疗机构（按省 + 名称 + 验证码）。粒度=单位条目 / 单文件（XLS/PDF）。
- 门槛：名单与名录**免费、免登录**；教育部附件 XLS/PDF 可直接下载(`✅ 200`)；**阳光高考 `gaokao.chsi.com.cn` 与学位中心 `cdgdc.edu.cn` 被 WAF 拦（412 瑞数类 JS 挑战）**，需真实浏览器；**卫健委 `zgcx.nhc.gov.cn/unit` 为 Vue SPA 且带点击式验证码，仅浏览器**。
- 实测：2026-10-03（逐源见 `## 细节`末表）。教育部 2026 名单页→200，附件 XLS 200（464 896 B）；专栏页 302→http 后 200（含 2006→2026 全部年份）；双一流通知页→200，2 个 PDF 均 200；研招网 `/zsml/`→200；`gaokao.chsi.com.cn`、`cdgdc.edu.cn`→412；`cas.cn/zz/jg/`→200（188 机构链接）；`cass.cn`→200；`cast.org.cn`→200；`zgcx.nhc.gov.cn/unit`→200（763 B SPA）。
- 上游：<https://www.moe.gov.cn/>、<https://www.chsi.com.cn/>、<https://www.cas.cn/>、<http://www.cass.cn/>、<https://www.cast.org.cn/>、<https://www.nhc.gov.cn/>

## 细节

### 1. 教育部 · 全国高等学校名单（权威底本，可下 XLS）★

- 专栏（历史年份入口）：`https://www.moe.gov.cn/jyb_xxgk/xxgk/neirong/fenlei/sxml_gdjy/gdjy_gxsz/gxsz_xxmd/`
  - 实测 302 → 跳到 **http** 同路径；加 `-L` 后 **200 / 104 140 B**。页面列出历年名单与备案函（2006、2010、2011、2012、2013、2014、2015、2016、2017、2019、2020、2022、2023、2025、2026…）。
- 最新一期（2026）：`http://www.moe.gov.cn/jyb_xxgk/s5743/s5744/202606/t20260618_1441074.html` → **200 / 13 439 B**
  - 正文口径：**截至 2026 年 6 月 17 日，全国高校共 3196 所**（普通 2952，含本科 1412、高职专科 1540；成人 244；不含港澳台）。
  - 附件（同目录相对路径，可直下）：
    - 附件1 全国普通高等学校名单：`…/jyb_xxgk/s5743/s5744/202606/W020260618416094865984.xls` → **200 / 464 896 B / application/vnd.ms-excel**
    - 附件2 全国成人高等学校名单：`…/202606/W020260618307096079727.xls`
- 往年页面命名规律：`…/jyb_xxgk/s5743/s5744/YYYYMM/tYYYYMMDD_<id>.html`（2024-06、2025-06 等），从专栏页取链接即可。
- 站内检索：`https://so.moe.gov.cn/s?qt=<关键词>` → **200 / text/html**（结果页为 JS 渲染；`/api/search` 猜测接口 **404**，勿依赖）。

### 2. 学信网 / 研招网 / 阳光高考（院校 → 官网/招生资质）

| 站点 | URL | 实测 | 用途 |
|---|---|---|---|
| 学信网 | `https://www.chsi.com.cn/` | ✅ 200 / 48 032 B | 高校学籍学历、阳光高考入口 |
| 研招网 | `https://yz.chsi.com.cn/` | ✅ 200 / 98 929 B | 研究生招生单位、招生简章 |
| 研招网·硕士专业目录 | `https://yz.chsi.com.cn/zsml/` | ✅ 200 / 51 814 B | 按招生单位/专业查学科点 |
| 阳光高考 | `https://gaokao.chsi.com.cn/` | ⚠️ 412 | 院校库（本科招生信息、院校简介） |
| 学位中心 | `https://www.cdgdc.edu.cn/` | ⚠️ 412 | 学位授权点评估、学科评估 |

`gaokao.chsi.com.cn`、`cdgdc.edu.cn` 返回 **412**，正文为 JS 挑战（`$_ts`/`nsd` 变量、`document.createElement("section")`），**加全浏览器头重试仍 412** → 需真实浏览器（Playwright/agent-browser）。

### 3. 学位授权点 / 双一流（教育部页面，静态可下）

- 学位管理与研究生教育司公告栏：`http://www.moe.gov.cn/jyb_xxgk/s5743/s5744/A22/` → **200 / 26 246 B**（学位授权点、学科评议、双一流相关通知）。
- 第二轮双一流通知：`https://www.moe.gov.cn/srcsite/A22/s7065/202202/t20220211_598710.html` → **200 / 17 827 B**，附件 2 个 PDF 均 **200 application/pdf**：
  - `…/202202/W020220214318455516037.pdf`（第二轮建设高校名单）
  - `…/202202/W020220214318455522038.pdf`（建设学科名单）
- 第一轮学科名单另见 `https://www.moe.gov.cn/s78/A22/A22_ztzl/ztzl_tjsylpt/sylpt_jsxk/201712/t20171206_320669.html`（搜索所得）。

### 4. 科研机构（院属机构名录页）

- **中国科学院·机构设置**：`https://www.cas.cn/zz/jg/` → **200 / 123 214 B**，页面含 **188 个 `*.cas.cn` 机构链接**（如 `amss.cas.cn` 数学与系统科学研究院、`iop.cas.cn` 物理研究所、`itp.cas.cn` 理论物理研究所…）；相邻页：院级非法人单元 `/zz/jg/ys/ys/`、所级分支机构 `/zz/jg/ys/sjfzjg/`、分院（`syb/shb/whb/gzb/cdb/kmb/xab/lzb/xjb.cas.cn`）。
- **中国社会科学院**：`http://www.cass.cn/` → **200 / 64 752 B**，首页直接列研究所及子域（`iccs.cssn.cn` 当代中国研究所、`literature.cass.cn` 文学研究所、`philosophy.cssn.cn`…）；组织机构页 `/ywzzjg/`。
- **中国科协**：`https://www.cast.org.cn/` → **200 / 12 765 B**；全国学会办事大厅 `https://bsdt-kc.cast.org.cn/index` → **200 / 1 570 B**（"全国学会办事大厅_智慧科协"）；学会治理 `/xs/XHZL/index.html` → 200 但仅 **2 958 B JS 骨架**，名录内容需浏览器。

### 5. 医疗卫生机构（卫健委）

- **查信息应用目录**：`https://zwfw.nhc.gov.cn/cxx/` → **200 / 13 084 B**，列出各查询入口（相对路径）：
  - `ywjgcx/` 医卫机构类：`qgyzjg/`（器官移植机构）、`ayyymd/`（爱婴医院名单）、`fzszjg/`（辅助生殖机构）、`cqzdjsyljg/`（产前诊断技术医疗机构）、`ywzgshzzml/`（**委业务主管社会组织名录** → 实测 **200 / 15 551 B**）
  - `ywrycx/`（执业医师/护士）、`jbywmlcx/`（基本药物目录）、`swbzcx/`（卫生标准）等
  - 注：`ywjgcx/yyzydj/` 医卫机构查询子页本机 **404**（可能为 JS 路由或改版）。
- **全国医疗机构查询**：`https://zgcx.nhc.gov.cn/unit` → **200 / 763 B**（Vue SPA，`assets/main-*.js`），表单需 **所在省份 + 机构名称（≥连续 4 字）+ 点击式验证码**；实测其 JS 资源路径也回吐 index.html → **仅浏览器**。数据截止见页面（实测提示"截止到 2026-09-21 0 时"）。
- 社会组织/事业单位资质交叉核对：`chinanpo.md`（民政部社会组织）、`sydj.md`（事业单位登记）、企业走 `gsxt.md`。

### 探测状态表

| host | 码 | 观察 |
|---|---|---|
| www.moe.gov.cn 专栏 | 302→200 | http 跳转；104 140 B；含 2006→2026 年份 |
| www.moe.gov.cn 2026 名单页 | 200 | 13 439 B；高校 3196 所 |
| www.moe.gov.cn 附件 XLS | 200 | 464 896 B；application/vnd.ms-excel |
| www.moe.gov.cn 双一流 PDF×2 | 200 | application/pdf |
| so.moe.gov.cn | 200 | 检索页 JS；/api/search 404 |
| www.chsi.com.cn | 200 | 学信网首页 |
| yz.chsi.com.cn /zsml/ | 200 | 研招网专业目录 |
| gaokao.chsi.com.cn | 412 | JS 挑战，需浏览器 |
| www.cdgdc.edu.cn | 412 | JS 挑战，需浏览器 |
| www.cas.cn/zz/jg/ | 200 | 188 机构链接 |
| www.cass.cn | 200 | 研究所子域列表 |
| www.cast.org.cn | 200 | /xs/XHZL/ 为 JS 骨架 |
| bsdt-kc.cast.org.cn | 200 | 全国学会办事大厅 |
| zwfw.nhc.gov.cn/cxx/ | 200 | 查询应用目录 |
| zgcx.nhc.gov.cn/unit | 200 | SPA + 验证码，仅浏览器 |

## 坑

1. **名单权威性排序**：核对"是否正规高校"以**教育部全国高等学校名单（XLS）**为准；学信网/研招网只解决"官网与招生"；阳光高考与学位中心有 WAF，命令行不可达，检索前先规划浏览器。
2. 教育部名单页是 **https → http 302**，脚本抓取需跟随重定向或直接用 `http://`。
3. 历年名单 **URL 无固定模板**，须从专栏页取当期链接；口径每年 6 月更新（如 2026-06-17）。
4. 科研机构名录随改革调整（分院/非法人单元变动），以 `cas.cn/zz/jg/` 当期页为准；协会学会的挂靠关系另查民政部 `chinanpo.md`。
5. 卫健委 `zgcx` 查询**凌晨 1–5 点维护不可用**，且需验证码，无法批量；社会组织名录类走 `chinanpo.md` 更全。
6. 附件 XLS 为旧版 `.xls`（OLE，代码页 GBK/936），读取时注意编码。
