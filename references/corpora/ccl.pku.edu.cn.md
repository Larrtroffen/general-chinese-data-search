# ccl.pku.edu.cn —— 北大 CCL 语料库检索

- 去哪找：检索系统 `http://ccl.pku.edu.cn:8080/ccl_corpus/`；中心主页 `https://ccl.pku.edu.cn/`。
- 什么时候用：要**带左右上下文的例句/索引行**（现代汉语、古代汉语）；语言学论文里的经典引用库；需要"文献时间从公元前 11 世纪到当代"的通用语料做词频/搭配/语法考察。
- 怎么搜：检索是**普通 GET 表单**，匿名可直接拼 URL：
  ```bash
  curl -s 'http://ccl.pku.edu.cn:8080/ccl_corpus/search?q=%E7%BB%8F%E6%B5%8E&dir=xiandai&start=0&num=50&index=FullIndex&outputFormat=HTML&encoding=UTF-8&maxLeftLength=30&maxRightLength=30&orderStyle=score&LastQuery=&scopestr='
  ```
  参数：`q`=检索词（支持 `|` 或、`$`/`#`/`+`/`-`/`~`/`!`/`:` 等操作符）；`dir`=语料方向（现代汉语 `xiandai` / 古代汉语 `gudai`）；`start`+`num`=分页；`index`=索引（默认 `FullIndex`）；`outputFormat=HTML`；`maxLeftLength`/`maxRightLength`=左右上下文长度；`scopestr`=限定子库；`orderStyle`=排序。结果形态：**HTML 索引行**，页内给"共在 N 个文档中出现"。
- 覆盖：现代汉语约 **6 亿字符** + 古代汉语（文献时间**公元前 11 世纪—当代**），含文学/戏剧/报刊等子库（上游声明，未逐库核实）。
- 门槛：**免费、免登录**（实测匿名可用）。
- 实测：2026-10-03，macOS arm64，curl 8.x，桌面 UA：`GET /ccl_corpus/` → 200（标题「CCL语料库检索系统（网络版）」）；`search?q=经济&dir=xiandai` → 200 / 48,425 B，页内「共在 **1,918,402** 个文档中出现」；`https://ccl.pku.edu.cn/` → 200（标题「北京大学中国语言学研究中心」）。
- 上游：北京大学中国语言学研究中心（CCL = Center for Chinese Linguistics）。

## 细节

### 检索参数（表单字段）

| 参数 | 取值 | 说明 |
|---|---|---|
| `q` | 关键词 | 检索词；操作符前后不能有空格 |
| `dir` | `xiandai` / `gudai` | 现代汉语 / 古代汉语（页面另有"汉英双语"选项） |
| `start` / `num` | 整数 | 起始偏移 / 每页条数（默认 50） |
| `index` | `FullIndex` 等 | 索引类型 |
| `outputFormat` | `HTML` | 输出格式（页面另有 JSON 相关隐藏字段 `jsonDis`/`jsonVal`，未追） |
| `encoding` | `UTF-8` | 编码 |
| `maxLeftLength` / `maxRightLength` | 整数（默认 30） | 索引行左右上下文长度 |
| `orderStyle` | `score` | 排序方式 |
| `scopestr` | 子库串 | 限定检索范围 |

## 坑

1. 检索端在 **8080 端口、只走 HTTP**（`http://ccl.pku.edu.cn:8080/…`）；写 https 会失败。
2. 页面是 2003 年风格（jQuery 1.6 + dynatree），**HTML 结构老**，解析要靠 `totalleft/totalright` 与结果表。
3. 分页用 `start`+`num`，**一次拉太大页会被截**；要全量请按页递增。
4. 只给**索引行/例句**，**不提供整库下载**；要整库文本请另找 BCC 频表、CLUECorpus 或购买授权。
