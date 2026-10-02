# papercash —— 百度学术/知网/万方接入要点

一个面向中文学生的论文全流程 skill（检索→综述→查重预检→降 AI→引文格式化），8 源汇总。**我们只要它的"中文三源怎么接"**：百度学术（免 key 解析式）、知网（Cookie + KNS8S QueryJson）、万方（Cookie + 搜索页）。结论先行：**它宣称"百度学术免费可用"，但本机匿名 curl 被"安全验证"挡死；知网/万方如实标了需 Cookie——三源实际都不可免登录直取**。

- 去哪找：repo `https://github.com/Jesseovo/PaperCash`（276KB）。三源代码：`scripts/lib/sources/baidu_xueshu.py`、`cnki.py`、`wanfang.py`；索引入口 `scripts/papercash.py`；Cookie 配置 `~/.config/papercash/.env`（`CNKI_COOKIE` / `WANFANG_COOKIE` / `GOOGLE_SCHOLAR_PROXY`）
- 什么时候用：需要**百度学术**这一条中文检索线（含学位论文/会议/专利的宽口径中文元数据），或要看**知网 KNS8S 检索接口**与**万方搜索页**的参数写法时，来这里抄端点；**不要**指望用它的"查重/降 AI"功能替代正式查重（它自己也声明不替代知网/维普）
- 怎么取：端点 + 参数（来自其源码，本机已逐条探活）。

```bash
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36'
# 1) 百度学术：HTML 解析（h3 a / .c_author / .c_abstract / .c_source / .sc_cite_cont）
curl -s -A "$UA" 'https://xueshu.baidu.com/s?wd=%E5%9F%BA%E5%B1%82%E6%B2%BB%E7%90%86&pn=0&ie=utf-8'
# 2) 知网 KNS8S 结果栅格（GET，走 QueryJson）
curl -s -A "$UA" -H 'Referer: https://kns.cnki.net/' \
  'https://kns.cnki.net/kns8s/brief/grid?CurPage=1&RecordsCntPerPage=20&DBCode=CFLS&SearchSql=基层治理'
#    其源码把 QueryJson 写成：{"Platform":"","DBCode":"CFLS","KuaKuCode":"CJFQ,CDMD,CIPD,CCND,CISD,SNAD,BDZK,CCJD,CCVD,CJFN",
#      "QNode":{"QGroup":[{"Key":"Subject","Items":[{"Title":"主题","Name":"SU","Value":"<词>","Operate":"="}]}]}}
#    （KuaKuCode 即库范围：期刊/学位/会议/报纸/年鉴/专利/标准…；字段名 SU=主题）
# 3) 万方：搜索页 HTML（div.normal-list / a.title / .author / .periodical a）
curl -s -A "$UA" 'https://s.wanfangdata.com.cn/paper?q=%E5%9F%BA%E5%B1%82%E6%B2%BB%E7%90%86&p=1&s=20&style=detail&f=top'
```
`papercash.py search "<主题>"`（其余免费源 Semantic Scholar / arXiv / Crossref / PubMed 走对应公开 API，可零配置）；依赖 `requests`+`beautifulsoup4`+`jieba`+`python-docx`（**要 pip 装，非 stdlib**）。
- 覆盖：中文论文元数据（题名/作者/年/刊/摘要/被引）。粒度到条目，无全文。实时随各站。许可：**MIT**
- 门槛：**百度学术**需真实浏览器 Cookie 或代理；**知网**需 `CNKI_COOKIE`（无 Cookie 时该源静默返回空）；**万方**需 `WANFANG_COOKIE`；依赖 `requests`+`beautifulsoup4`+`jieba`+`python-docx`（要 pip 装，非 stdlib）；中文库全文下载仍要机构订阅（另见本层 `cnki.net.md` / `wanfangdata.com.cn.md` / `cqvip.com.md`）
- 实测：2026-10-02，macOS + curl（未安装其依赖，仅复现其请求）：
  - 百度学术 `xueshu.baidu.com/s?wd=基层治理&pn=0&ie=utf-8` → **`HTTP 403`，正文含"安全验证"**；带 `BAIDUID` cookie 预热重试仍 `403`（`div.result` 计数 0）
  - 知网 `kns.cnki.net/kns8s/brief/grid?...` → **`HTTP 403` JSON**：`{"code":-403,"message":"https://kns.cnki.net/verify/home?captchaType=blockPuzzle&ident=…&returnUrl=…"}`（即滑块验证，与 `cnki.net.md` 一致）
  - 万方 `s.wanfangdata.com.cn/paper?...` → **`HTTP 200`（171KB）但正文为登录壳**，无 `div.normal-list` 结果节点
- 上游：`https://github.com/Jesseovo/PaperCash`（MIT；三源端点取自其 `scripts/lib/sources/*.py`）

## 坑

- 三源均为 **HTML 选择器解析**，改版即失效。
- `http_client` 默认 UA 被判爬虫风险高。
- 百度学术匿名返回滑块/安全验证；知网未登录直接 403 + 滑块 URL；万方未登录只给登录壳。
