# difangzhi.cn —— 中国方志网

中国地方志工作办公室（原中国地方志指导小组办公室）官网「中国方志网」。**注意：任务书里给的 `dfz.org.cn` 不存在（DNS NXDOMAIN），实际域名是 `www.difangzhi.cn`。**

- 去哪找：
  - 首页：`https://www.difangzhi.cn/`
  - **全文检索接口**：`https://www.difangzhi.cn/was5/web/search`（TRS WAS，返回 HTML 片段）
  - 检索页（人用，结果区 AJAX）：`https://www.difangzhi.cn/jiansuo/qwjs/`；高级检索表单页 `/jiansuo/gjjs/`
  - 志书 / 年鉴栏目：`/zs/` · `/nj/`（JS 跳转到 `zsbz/`、`njbz/`）
  - 在线下载：`/zxfw/zxxz/`；数字方志（动态资讯）：`/xxh/szfz/`
- 什么时候用：需要**全国方志系统**的全文检索（新闻、通知、志书/年鉴选介）；查志书/年鉴**书目与选介**；定位「某地在方志系统的报道/选介」。
- 怎么搜：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  KW=$(python3 -c "import urllib.parse;print(urllib.parse.quote('街乡吹哨'))")
  curl -s -A "$UA" "https://www.difangzhi.cn/was5/web/search?channelid=283767&searchword=${KW}&page=1"
  ```
  参数：`channelid=283767`（固定）、`searchword`（关键词，建议 URL 编码）、`page`（从 1 起）。其余可选项（可留空）：`orderby`、`searchscope`（`doctitle`=标题，空=全文）、`timestart`、`timeend`、`chnls`、`andsen`、`orsen`、`exclude`、`total`。
  返回 HTML（实测）：
  ```html
  <div class="cj_ss_jg_right">约有2125项符合<span>北京</span>的查询结果</div>
  <ul class="cj_ss_jieguo">
    <li><dl><dt><span>2026-10-01</span>
      <a href="https://www.difangzhi.cn/tzgg/…/t….shtml">标题</a></dt>
      <dd>摘要（关键词用 <font color='#b21510'>…</font> 高亮）</dd></dl></li>
  ```
  解析要点：`共/约有 N 项` 取总数；条目用 `cj_ss_jieguo` 下的 `<li>`，取 `<a>` 链接与 `<dt><span>` 日期、`<dd>` 摘要。
- 覆盖：检索范围是**本站全部内容**（新闻、通知、选介文章等），**不是志书原文库**——它不会返回某本志书内页的正文，只能用来定位「某地在方志系统的报道/选介」。志书/年鉴栏目仅提供**书目与介绍**（无正文/附件）。
- 门槛：免费、免登录。`channelid=283767` 是当前检索频道 id，站点改版后可能变化——若返回空，去 `/jiansuo/qwjs/?searchword=x` 页面里重新抓 `channelid`。
- 实测：2026-10-02，macOS（arm64），curl 8.x。`dfz.org.cn` NXDOMAIN；`www.difangzhi.cn` 200；`/was5/web/search?channelid=283767&searchword=北京&page=1` 返回 200 / 11 KB，头部「约有 2125 项符合北京的查询结果」，条目含标题、日期、高亮摘要；志书选介/年鉴选介栏目均为介绍文章页。
- 上游：`https://www.difangzhi.cn/`

## 细节

### 可用性矩阵

| 路径 | 状态 | 现象 |
|---|---|---|
| `https://www.difangzhi.cn/` | ✅ 200 | 首页（中国方志网） |
| `https://www.difangzhi.cn/was5/web/search` | ✅ 200 | **全文检索接口**（TRS WAS，返回 HTML 片段） |
| `https://www.difangzhi.cn/jiansuo/gjjs/` | ✅ 200 | 高级检索表单页 |
| `https://www.difangzhi.cn/zs/` · `/nj/` | ✅ 200 | 志书 / 年鉴栏目（JS 跳转到 `zsbz/`、`njbz/`） |
| `https://www.difangzhi.cn/zxfw/zxxz/` | ✅ 200 | 在线下载（统计模板、编纂教程等） |
| `https://www.difangzhi.cn/xxh/szfz/` | ✅ 200 | 数字方志（动态资讯） |
| `dfz.org.cn` / `www.dfz.org.cn` | ❌ NXDOMAIN | 域名不存在 |

### 志书 / 年鉴（书目与选介，非全文）

| 栏目 | URL | 内容 |
|---|---|---|
| 志书编纂 | `https://www.difangzhi.cn/zs/zsbz/` | 编纂业务 |
| 志书选介 | `https://www.difangzhi.cn/zs/zsxj/` | 逐本志书的**介绍文章**（如「清同治《苏州府志》」），无正文/附件 |
| 年鉴编纂 | `https://www.difangzhi.cn/nj/njbz/` | 编纂业务 |
| 年鉴选介 | `https://www.difangzhi.cn/nj/njxj/` | 逐本年鉴介绍（如「《江西年鉴（2025）》」） |
| 在线下载 | `https://www.difangzhi.cn/zxfw/zxxz/` | 统计模板、编纂教程（.shtml 文章，非电子书） |

**结论：中国方志网不提供志书/年鉴全文在线阅读或下载**，只有书目与介绍。要志书全文请走：
- 各省方志官网（京网 `bjdsdfz.cn`、上海通 `shtong.gov.cn`、江苏 `jssdfz.jiangsu.gov.cn`、浙江 `dfz.zj.gov.cn`…，首页友情链接区有完整 30+ 条清单）。
- 志书/年鉴数字化的商业库：CNKI 年鉴库、中国历史文献总库等（另见 `nlc.cn.md`）。

### 易被误认为方志网的站

| 站 | 域名 | 实测 | 说明 |
|---|---|---|---|
| 中国国情网 | `https://www.zhongguoguoqing.cn/` | ✅ 200 | 有「数字国情 / 古方志 / 新方志 / 年鉴」栏目，但**实测均为介绍性新闻文章，无正文附件** |
| 中国地情网 | `https://www.zhongguodiqing.cn/` | ✅ 200 | 同系统 |
| 中国方志出版网 | `http://fzph.cssn.cn/` | 未验证 | 出版动态 |

## 坑

1. **域名**：`dfz.org.cn` 不存在；正确域名 `difangzhi.cn`（该站自链也用 `www.difangzhi.cn`，部分栏目链接为 `http://`）。
2. 首页示例：检索结果初始为空，必须带 `searchword` 才有内容。
3. `channelid=283767` 是当前检索频道 id，站点改版后可能变化——若返回空，去 `/jiansuo/qwjs/?searchword=x` 页面里重新抓 `channelid`。
4. 高级检索表单提交到 `/jiansuo/qwjs/`（GET，字段 `searchword`、`searchscope`），但结果仍需上面的 `was5` 接口。
5. 不要把「选介」栏目内容当志书正文引用。
