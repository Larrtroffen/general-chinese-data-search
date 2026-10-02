# institutional-repos —— 机构知识库与学位论文定位

- 去哪找：OpenDOAR/Jisc `https://v2.sherpa.ac.uk/opendoar/`（全球 IR 目录）；ROAR `https://roar.eprints.org/`；OpenAIRE `https://api.openaire.eu/`；CALIS 高校学位论文 `https://etd2.calis.edu.cn/`
- 什么时候用：**不知道某校/某所机构的知识库在哪**；要找**某校学位论文**（博士/硕士）或**机构成果**（期刊论文、报告、专利）；要判断一个 IR 用的是什么软件、有没有 OAI-PMH 可批量收割；做"中国有哪些机构知识库"的清单
- 怎么取：定位流程如下——
  1. **OpenDOAR 按国家列中国 IR**：`https://v2.sherpa.ac.uk/view/repository_by_country/China.html`（国家目录根 `https://v2.sherpa.ac.uk/view/repository_by_country`）——每条给名称、URL、软件类型、OAI 接口
  2. **批量接口**：`https://v2.sherpa.ac.uk/cgi/retrieve?item-type=repository&api-key=<免费KEY>&format=Json&filter=[["country","equals","China"]]`（需在 Jisc 注册免费 key；本机 WAF 403）
  3. **ROAR 备用目录**：检索 `https://roar.eprints.org/cgi/search?q=<词>&_action_search=Search&basic_srchtype=ALL&_satisfyall=ALL`（本机被 bot 墙）；最新入库 RSS `https://roar.eprints.org/cgi/latest_tool?output=RSS2`（可直取）
  4. **聚合收割**：OpenAIRE `https://api.openaire.eu/search/publications?keywords=<词>&size=10[&format=json]`（默认 XML，实测可用）；CORE / BASE 见 `paper-lookup.md`、`paper-search-mcp.md`
  5. **中文机构 IR**：中科院各所 `ir.<所域名>.ac.cn`（如 `https://ir.psych.ac.cn/`）；高校多为自研 SPA 或 SSO 登录墙，常见名 `ir.<校域名>`，应从**该校图书馆官网的「机构知识库/成果库」入口**进
  6. **学位论文**：CALIS `https://etd2.calis.edu.cn/`（高校学位论文联合服务）；另有 NCPSSD/知网/万方（见相关）
- 覆盖：OpenDOAR = 全球数千个 IR 的**登记目录**（不含全文本身）；ROAR = 另一份 IR 注册表；OpenAIRE = 欧盟聚合的 OA 成果与 IR 记录；CALIS ETD = 中国高校博硕士论文联合目录；中国机构 IR 各自覆盖本校/本所成果
- 门槛：OpenDOAR/ROAR 网页免登录（**本机被 Jisc WAF / bot 墙挡**）；OpenDOAR API 需注册免费 key；OpenAIRE API 免 key；多数高校 IR 浏览免登录、**下载学位论文常需校内 IP 或登录**
- 实测：2026-10-03，macOS + curl（桌面 UA）——`https://v2.sherpa.ac.uk/opendoar/` 与 `…/view/repository_visualisations/1.html`、`…/id/repository/1?format=json` 均 **403「Jisc - Error 403」**（651KB 拦截页），`opendoar.org` HTTPS 握手失败；`https://roar.eprints.org/` 首页 200，`/cgi/latest_tool?output=RSS2` 200 `application/rss+xml`，但 `/cgi/search?q=China` 返回「Making sure you're not a bot!」；`https://api.openaire.eu/search/publications?keywords=governance&size=2` 200 `application/xml`；`https://ir.psych.ac.cn/` 200；`https://www.irgrid.ac.cn/` 与 `http://www.irgrid.ac.cn/` 均**超时**；`https://ir.scu.edu.cn/`→登录页、`https://ir.xmu.edu.cn/`→SSO 登录、`https://ir.cqu.edu.cn/` 200、`https://ir.ustc.edu.cn/` 200、`ir.whu.edu.cn` 403、`ir.pku.edu.cn` 超时、`ir.nju.edu.cn`/`ir.fudan.edu.cn`/`ir.lib.tsinghua.edu.cn`/`ir.lib.zju.edu.cn` DNS 不解析；`https://etd.calis.edu.cn/`→`https://etd2.calis.edu.cn/` 200「CALIS高校学位论文服务系统」
- 上游：Jisc OpenDOAR（`https://v2.sherpa.ac.uk/opendoar/`）；ROAR（`https://roar.eprints.org/`）；OpenAIRE（`https://www.openaire.eu/`）；CALIS（`http://www.calis.edu.cn/`）

## 细节

### 找某校学位论文/机构成果的最短路径

1. 先在 **OpenDOAR 中国页**（或 ROAR）确认该校有无登记 IR、拿到站点 URL 与软件类型（DSpace/EPrints/…）。
2. 有 OAI-PMH 的直接按 `oai_dc` 批量取元数据；没有就走站点检索页。
3. 学位论文若无 IR 收录，改走 **CALIS ETD**（联合目录）→ 知网/万方学位论文库（正文常需机构授权）。
4. 中国高校 IR 命中率提示：`ir.<校域名>` 有效的不多，很多学校用统一身份认证（SSO）——先在图书馆站内搜"机构知识库/机构库/学术成果库"。

### 中国机构知识库现状（本机实测口径）

- **CAS 系统**：院所级 IR 多为 `ir.<所>.ac.cn`，部分可匿名访问（`ir.psych.ac.cn` 200）；老的"中国科学院机构知识库网格" `www.irgrid.ac.cn` 已**连不上**（HTTP/HTTPS 均超时），不要再作为入口。
- **高校**：川大/厦大需登录，重大/中科大返回站点壳（内容由 JS 渲染），武大 403，北大超时，南大/复旦/清华/浙大域名不解析——**没有"一把钥匙开所有校 IR"的域名规律**，以 OpenDOAR/图书馆入口为准。

## 坑

- **Jisc 全线 403**：OpenDOAR 网页与 API 从本机出口被 WAF 拦（不是没这个服务）；要么换出口，要么用 ROAR/OpenAIRE 替代，或按 `…/view/repository_by_country/<Country>.html` 模板直接记链接。
- **ROAR 首页可开、检索被 bot 墙**：能取 RSS/浏览视图，全文检索返回 bot 校验页。
- OpenAIRE 默认返回 **XML**（`?format=json` 才给 JSON），关键词走 `keywords=`；老接口，字段名 `oaftype`/`resulttypeid`。
- 机构 IR 的"检索"多是 SPA/登录墙：curl 只拿到空壳 HTML（几百字节～几 KB），判断可用性要看**正文是否含记录**而非状态码。
- IR 目录（OpenDOAR/ROAR）只给**站点元数据**，不给全文；要正文去 IR 站点或聚合库。

## 相关

- 国际元数据/引文/OA 全文：`paper-lookup.md`（OpenAlex/Crossref/Unpaywall/CORE/BASE）。
- 多源检索与 PDF 下载链：`paper-search-mcp.md`。
- 中文期刊全文与非正式文献：`ncpssd.org.md`；学位论文与期刊：`cnki.net.md`、`wanfangdata.com.cn.md`、`nstl.gov.cn.md`。
- 中文预印本与科技报告：`preprints-cn.md`。
