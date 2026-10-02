# universities-open-data —— 高校信息公开与排名

- 去哪找：各校信息公开专栏 `https://xxgk.<校域名>/`（如 `https://xxgk.pku.edu.cn/`、`https://xxgk.nju.edu.cn/`、`https://xxgk.fudan.edu.cn/`）；软科排名 API `https://www.shanghairanking.cn/api/pub/v1/bcur?bcur_type=11&year=2024`；校友会/艾瑞深 `http://www.cuaa.net/`（榜单正文在 `http://www.chinaxy.com/…`）
- 什么时候用：要**单校**的**信息公开年度报告 / 财务预算·决算 / 招生简章 / 本科教学质量报告**；要**毕业生就业质量年度报告**（就业率、升学、行业流向）；要高校**排名**（软科、校友会）；查学科评估、双一流名单（→「上游」与 `../gov/edu-research-institutions.md`）
- 怎么搜：三步——**① 信息公开专栏**：入口 `https://xxgk.<校域名>/`，栏目名按教育部《高等学校信息公开办法》事项清单高度一致（`gksx/` 公开事项 → 招生考试 / 财务·资产及收费 → 财务预算·决算 / 教学质量 → 毕业生就业质量报告 / 年度报告），列表页直读 HTML，附件多为 `.pdf`/`.xls`（路径形如 `/docs/…`、`/_upload/article/files/…`）；**② 就业质量报告**：见「细节」三条路；**③ 排名**：软科走 JSON API（可整表取），校友会走 GBK HTML 页
- 覆盖：各校自主发布（年度报告 2010s→2025；部门预决算逐年；就业质量报告 2013 届至今）；软科中国大学排名（主榜 + 分类榜，可指定年份）；校友会/艾瑞深排名（历年榜单 + 学科/专业排名）。粒度=单校文件 / 整榜 JSON
- 门槛：xxgk 专栏与附件**免登录、可匿名 curl**；软科 API **免 key**；校友会站 **HTTP only + GBK**；个别校被 WAF 或 DNS 不解析（见「坑」）
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA、`-L`、20s 超时）——抽查 8 个 xxgk：北大/复旦/南大/人大/中科大/中山/哈工大 **200**，上海交大 **302→restrict.sjtu.edu.cn**（WAF 中转页 1152 B），清华/浙大/武大 **HTTP 000**（DNS 不解析）；北大年度报告与部门决算 PDF **200**（如 1 063 947 B `application/pdf`）；南大就业质量报告 PDF **200**（600 468 B）；软科 `bcur_type=11&year=2024` **200 / 274 192 B JSON**（594 所），`bcur_type=21` **200**（医药类 84 所，榜首北京协和医学院）；校友会 `http://www.cuaa.net/` **200 / 22 099 B（GBK）**
- 上游：教育部信息公开（`https://www.moe.gov.cn/jyb_xxgk/`）；软科（`https://www.shanghairanking.cn/`）；校友会/艾瑞深（`http://www.cuaa.net/`、`http://www.chinaxy.com/`）；学科评估/学位中心（`https://www.cdgdc.edu.cn/`）

## 细节

### 1. 信息公开专栏抽查（2026-10-03）

| host | 码 | 观察（CMS / 路径规律） |
|---|---|---|
| `xxgk.pku.edu.cn` | 200 | 13 611 B；静态 Sitestar，`/gksx/<类>/<子类>/index.htm`，附件 `/docs/<时间戳或 hash>.pdf` |
| `xxgk.fudan.edu.cn` | 200 | 140 299 B；南大之星系，`/{栏目id}/list.htm`（年度报告如 `/2024w2025xnfddxxxgkndbg/list.htm`） |
| `xxgk.nju.edu.cn` | 200 | 56 169 B；`/{栏目id}/list.htm`，附件 `/_upload/article/files/…/<uuid>.pdf` |
| `xxgk.ruc.edu.cn` | 200 | 22 840 B |
| `xxgk.ustc.edu.cn` | 200 | 38 511 B（首页 → `/main.htm`） |
| `xxgk.sysu.edu.cn` | 200 | 22 118 B（年度报告 `/ndbg`） |
| `xxgk.hit.edu.cn` | 200 | 34 160 B |
| `xxgk.sjtu.edu.cn` | 302→`restrict.sjtu.edu.cn` | 反爬中转页（1 152 B），curl 到不了正文 |
| `xxgk.tsinghua.edu.cn` / `xxgk.zju.edu.cn` / `xxgk.whu.edu.cn` | 000 | 本机 **DNS 不解析**（≠ 该专栏不存在） |

**规律**：`xxgk.<校域名>` 是多数教育部直属高校的通行入口（栏目由教育部清单规定，各校命名基本一致）；但 **CMS 与附件路径各校不同**（北大 `/docs/`、南大 `/_upload/article/files/`），附件名不可拼，必须从列表页取链接。

### 2. 实测可直下的文件（curl 200）

| 学校 | 文件 | URL | 观察 |
|---|---|---|---|
| 北大 | 信息公开年度报告 | `https://xxgk.pku.edu.cn/docs/20241031162656657219.pdf` | 200 / 1 063 947 B / `application/pdf` |
| 北大 | 部门决算（逐年） | 列表 `https://xxgk.pku.edu.cn/gksx/cwzcsf/cwjs/index.htm`，如 `…/docs/20250808181232330844.pdf`、`…/docs/2026-08/a370fd617ccb405e84dc53cb726502e2.pdf` | 同一页给 **2012→2025** 全部决算 PDF 直链（2012–2014 为 `.jpg` 扫描） |
| 南大 | 毕业生就业质量报告 | `https://xxgk.nju.edu.cn/_upload/article/files/35/c9/48fb6d934e7aa2a6b7674978834a/c8f6eed9-8fc7-4489-9697-d1a846d8155c.pdf` | 200 / 600 468 B / `application/pdf`；列表页 `https://xxgk.nju.edu.cn/16401/list.htm` |
| 南大 | 财务决算栏目 | `https://xxgk.nju.edu.cn/15420/list.htm`（预算 `/15419/list.htm`） | 栏目页 200，附件在页内取 |

### 3. 毕业生就业质量报告的三个落点

1. **校信息公开专栏「教学质量」类**：南大 `/16401/list.htm`（本机实测该栏目页存在，附件 PDF 直链 200）。
2. **校就业（指导）中心站**：文件形如 `…/jy/upload/file/<YYYYMMDD>/<时间戳>_<id>.pdf`，例如 `https://www.wenda.edu.cn/jy/upload/file/20250218/20250218104513_80043.pdf`（2024 届，**检索所得，未本机探活**）。
3. **校主站/院系站附件**：`https://www.hsu.edu.cn/_upload/article/files/…/<uuid>.pdf`（**检索所得，未本机探活**）。
   → 找不到时用站内检索 `毕业生就业质量报告 site:<校域名>` 或先看 `xxgk` 目录树。

### 4. 排名数据

**软科（推荐，JSON 可整表取）**

```
curl -s 'https://www.shanghairanking.cn/api/pub/v1/bcur?bcur_type=11&year=2024'
```

- 返回 `{code,msg,data:{rankings[],inds[],provinces[],univCategorys[]}}`；`rankings[i]` 字段：`univNameCn`/`univNameEn`/`univUp`（英文 slug）、`province`、`univCategory`、`score`、`ranking`、`rankOverall`、`univTags`（如 `["双一流","985","211"]`）、`indData`（按指标码 → 分值，码名见 `inds[]`）。
- 实测取值：`bcur_type=11` = 主榜（594 所，2024）；`bcur_type=21` = 医药类（84 所）。**其他 type 取值未逐一探明**，用时以榜页 `https://www.shanghairanking.cn/rankings/bcur/<年>` 为准。

**校友会 / 艾瑞深（弱：GBK + 仅 HTTP）**

- `http://www.cuaa.net/`（**200 / GBK / 22 099 B**）是入口，榜单正文在 `http://www.chinaxy.com/2022index/…`（如 `…/2023/2023dxpmall.html` 200 / 132 924 B / GBK，标题「校友会 2026 中国大学排名…」）；文章页 `…/2022index/news/news.jsp?information_id=<N>`。
- 实测榜单页**基本无 `<table>` 数据行**（多为图文榜单/新闻稿），**未发现 JSON 接口**；`https://www.cuaa.net/` 与 `https://www.chinaxy.com/` 均 **HTTP 000**（仅 http 可用）。

### 5. 相关通道（不重复造卡）

- **机构知识库 / 学位论文**（各校 IR、CALIS ETD）→ `institutional-repos.md`。
- **学科评估、双一流名单、全国高校名单**（学位中心 `cdgdc.edu.cn` 本机 **412** 瑞数挑战，需浏览器）→ `../gov/edu-research-institutions.md`。
- **高校/教育财政经费**（教育部部门预决算、全国教育经费公告）→ `edu-finance.md`。

## 坑

1. **`xxgk.<校>.edu.cn` 不是全称规律**：清华/浙大/武大本机 DNS 不解析，上海交大 302 到 `restrict.sjtu.edu.cn` 反爬页——**不要据「curl 000/302」判定该校没有信息公开专栏**，换出口或走浏览器；正确入口可在校主页搜索「信息公开」。
2. **附件名不可拼**：同一校内也是 `/docs/<时间戳>.pdf`、`/_upload/…/<uuid>.pdf`、`/2026-08/<hash>.pdf` 混用（北大 2025 年末起新附件改用 `/docs/<年-月>/<hash>.pdf`）——**必须解析列表页**，勿硬编码文件名。
3. **有的列表页是 JS 渲染**：南大 `/16401/list.htm` 用简单 `href` 抓取未命中条目（列表由脚本插入），要拿链接需浏览器或换站内检索。
4. **数据时效**：决算通常次年 7–8 月、预算当年 3–4 月、年度报告次年 10–11 月发布；就业质量报告次年 1–4 月（"2024 届"报告多在 2025 年初）。引用务必记**文件标题+发布日期**。
5. **口径不可混用**：高校发布的「部门决算」是**单校**口径；「信息公开年度报告」是**制度执行**报告，不含完整财务数字——财务数字取 `财务决算`/`财务预算` 附件本身。
6. **排名是商业/民间榜单**，指标权重由发布方自定（软科按指标码加权、校友会为星级法），**不能当官方口径**；引用须写明榜单名称、年份与发布机构。
7. 校友会站 **GBK 编码 + 仅 HTTP**：`iconv -f gb18030` 解码；`https://` 一律连接失败。

## 相关

- 教育部全国高校名单 / 双一流 / 学位授权点：`../gov/edu-research-institutions.md`。
- 机构知识库与学位论文定位：`institutional-repos.md`。
- 教育经费与部委预决算：`edu-finance.md`。
- 中文期刊论文（教师成果核验）：`ncpssd.org.md`、`cnki.net.md`。
