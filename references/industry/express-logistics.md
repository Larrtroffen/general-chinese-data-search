# express-logistics —— 快递与物流统计

以**国家邮政局**行业统计为主（月度快递业务量/收入、年度统计公报、快递发展指数，官方口径、免登录），
**交通运输部**补货运量与城市客运量（月度、附 xlsx），
**中物联/中国物流信息中心**补 PMI 与物流指数（不重复建卡，见 `clic.org.cn.md`、`chinawuliu.com.cn.md`）。

- 去哪找：
  - **国家邮政局 统计信息** `https://www.spb.gov.cn/gjyzj/c100276/common_list.shtml`（年度《邮政行业发展统计公报》+ 月度运行情况汇总；「查看更多」`/gjyzj/c100037/c100150/common_listmore.shtml?channelId=ce2d4d5628314ff7a81553529fb7f6a0&code=c100276`）
  - **中国快递发展指数** `https://www.spb.gov.cn/gjyzj/c100278/common_list.shtml`（月度指数报告）
  - **月度《邮政行业运行情况》正文**（新闻动态栏目）`https://www.spb.gov.cn/gjyzj/c100015/c100016/{YYYYMM}/{hash}.shtml`
  - **交通运输部** 数据栏目 `https://www.mot.gov.cn/shuju/`；月度《全国城市客运量》与交通运输经济运行情况 `https://xxgk.mot.gov.cn/jigou/zhghs/{YYYYMM}/t{YYYYMMDD}_{id}.html`
  - **中物联 / 物流信息中心** 见 `industry/clic.org.cn.md`（`code=pmi|logistics`）、`industry/chinawuliu.com.cn.md`；**国家邮政局发展研究中心** `http://www.spbdrc.org.cn/`、**中国快递协会** `http://www.cea.org.cn/`
- 什么时候用：要**快递业务量 / 快递业务收入**（当月 + 累计、同比）、**同城/异地/国际港澳台**分项、**邮政行业寄递业务量**、邮政普遍服务业务；要**中国快递发展指数**（月度分项指数）；要**年度邮政行业发展统计公报**；要社会物流总额、物流业景气/仓储/电商物流/快递物流指数与 PMI；要**公路/铁路货运量、城市客运量**月度数字。
- 怎么搜：清一色**公开 HTML**（列表 + 正文表格），无需 key；列表页服务端渲染，文章标题在 `<p>`、日期在 `<span>`：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # ① 邮政局统计信息列表（含年度公报与每月运行情况）
  curl -sS -A "$UA" 'https://www.spb.gov.cn/gjyzj/c100276/common_list.shtml'
  # ② 某月《邮政行业运行情况》正文（内含「全国邮政行业发展情况表」）
  curl -sS -A "$UA" 'https://www.spb.gov.cn/gjyzj/c100015/c100016/202609/5da542159e1449b4ba8334b6054e0718.shtml'
  # ③ 中国快递发展指数列表
  curl -sS -A "$UA" 'https://www.spb.gov.cn/gjyzj/c100278/common_list.shtml'
  # ④ 交通运输部月度城市客运量（正文附 xlsx，相对链接 ./P0….xlsx）
  curl -sS -A "$UA" 'https://xxgk.mot.gov.cn/jigou/zhghs/202607/t20260721_4210104.html'
  ```
  结果形态：HTML 列表 + 正文 **HTML 表格**（邮政局）；交通运输部正文附 **xlsx** 附件（相对路径）。
- 覆盖：**月度**（如 2026 年 1–8 月、上半年、1–5 月…的累计 + 当月、同比）；**年度**（《邮政行业发展统计公报》，最新 2025 年，2026-05 发布）；**快递发展指数**月度（2026-08 期已出）；口径为**全国**（分省见各省邮政管理局子站与年度公报附表）；交通运输部为**分省**城市客运量/货运量月度 xlsx。
- 门槛：**免费、免登录、无 key**（邮政局与交通运输部均为公开栏目）。
- 实测：2026-10-03，macOS arm64，curl 8.x，桌面 UA，20 s 超时，同主机 ≥1.5 s 间隔：
  - `GET spb.gov.cn/gjyzj/c100276/common_list.shtml` → **200**，30 KB，title「统计信息」；服务端渲染出文章列表（如「2026-09-18 国家邮政局公布2026年1-8月邮政行业运行情况」「2026-05-22 2025年邮政行业发展统计公报」）✅
  - `GET …/gjyzj/c100278/common_list.shtml` → **200**，title「中国快递发展指数」，含「2026年8月中国快递发展指数报告」等月度条目 ✅
  - `GET …/gjyzj/c100015/c100016/202609/5da542159e1449b4ba8334b6054e0718.shtml` → **200**，title「国家邮政局公布2026年1-8月邮政行业运行情况」，正文含 1 张「全国邮政行业发展情况表」（收入 12 304.5 亿元、快递业务量 1 340.6 亿件…）✅
  - `GET xxgk.mot.gov.cn/jigou/zhghs/202607/t20260721_4210104.html` → **200**，title「2026年1-6月全国城市客运量」，含 xlsx 附件链接 `./P020260721336688693301.xlsx` ✅；`GET mot.gov.cn/shuju/index.html` → **200** ✅
- 上游：国家邮政局 <https://www.spb.gov.cn/>；交通运输部 <https://www.mot.gov.cn/>；中国物流与采购联合会 <http://www.chinawuliu.com.cn/>、中国物流信息中心 <http://www.clic.org.cn/>。

## 细节

### 国家邮政局 URL 形态（2026-10-03 实测）

| 内容 | 栏目 | URL 形态 |
|---|---|---|
| 月度《邮政行业运行情况》 | 新闻动态 `c100015/c100016` | `https://www.spb.gov.cn/gjyzj/c100015/c100016/{YYYYMM}/{hash}.shtml` |
| 年度《邮政行业发展统计公报》 | 统计信息 `c100276` | `https://www.spb.gov.cn/gjyzj/c100276/{YYYYMM}/{hash}.shtml` |
| 月度《中国快递发展指数报告》 | 快递发展指数 `c100278`（文章亦在 `c100015/c100016`） | 同上 |
| 「查看更多」分页 | `c100037/c100150/common_listmore.shtml?channelId={32位hex}&code={c100276\|c100278}` | 列表首页内联给出 channelId |
| 站内检索 | `/html/searchResult.html?siteCode=bm71000001&columnId=0&searchWord=…` | 索引出版总署站 |

### 月度运行情况表字段（实测 2026 年 1-8 月）

「全国邮政行业发展情况表」按 8 月/累计分列，含：**邮政行业业务收入、其中快递业务、邮政普遍服务业务**；**邮政行业寄递业务量、其中快递业务（同城/异地/国际港澳台）、邮政普遍服务业务**，并给出累计与当月**同比增速**。数值单位为亿元 / 亿件。

### 分省与货运量

- **分省快递业务量/收入**：不在全国月度正文表中，见**各省邮政管理局子站**（`http://{省缩写}.spb.gov.cn/`，如 `bj.spb.gov.cn`）、年度统计公报附表，或国家统计局/地方统计局口径。
- **货运量**：交通运输部「交通运输经济运行情况」月报（`xxgk.mot.gov.cn/jigou/zhghs/`）含公路/水路货运量与周转量；铁路货运见 `industry/rail-aviation.md`；国家统计局口径见 `data.stats.gov.cn.md`。
- **物流指数**：PMI、物流业景气、仓储、电商物流、公路运价指数走 `clic.org.cn.md`（`code=logistics` 下有「快递物流指数」子类）；联合会门户 `chinawuliu.com.cn.md`。

## 坑

1. **列表标题不在 `<a>` 文本里**：邮政局列表页每条的标题在 `<a …><img/><p>标题</p><span>日期</span></a>`，用「`<a>` 后紧跟文本」的正则会漏抓；按 `<p>…</p>…<span>YYYY-MM-DD</span>` 抓。
2. **两类文章分属不同栏目**：月度《运行情况》在新闻动态 `c100015/c100016`，年度《统计公报》在统计信息 `c100276`；只看 `c100276` 会漏掉月度表。
3. **「查看更多」是额外端点**：列表首页只给约 10 条，历史要拼 `common_listmore.shtml?channelId=…&code=…`（channelId 每次改版可能变，从首页 `<a class="listmore">` 现取）。
4. **口径区分**：邮政局表内「**邮政行业业务收入**」≠「快递业务收入」，后者是前者子项；「寄递业务量」含普遍服务，勿与「快递业务量」混用。
5. **全国 ≠ 分省**：全国月度表不带分省明细，做分省面板须另取各省局子站或年度公报，口径/时点可能与全国表有差。
6. **交通运输部是另一套统计**：城市客运量、货运量口径与邮政口径完全不同，且附件 xlsx 为相对路径，下载须补文章所在年月目录。
7. **PMI 与国家统计局联合发布**：制造业/非制造业 PMI 由国家统计局与中国物流与采购联合会联合发布，媒体转载值可能被改写，引用记发布日（详见 `chinawuliu.com.cn.md`）。
