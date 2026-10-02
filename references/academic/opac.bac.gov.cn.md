# opac.bac.gov.cn —— 北京市委党校图书馆 OPAC

市委党校图书馆书目查询：查党内出版物（皮书/研究报告）的完整书目信息与馆藏索书号。

- 去哪找：`http://opac.bac.gov.cn:8080/NTRdrBookRetr.do?SearchKey={书名}&SearchType=title&searchWay=searchWay`
- 什么时候用：查党内出版物的书目与馆藏索书号；核对 ISBN/页数/丛书名（比电商页可靠）
- 怎么搜：`SearchType=title`（书名）/`author`（作者）/`anyword`（任意词）；直接 curl 可读（页面静态 HTML，把 `<…>` 剥掉即文本），无需登录
- 覆盖：市委党校图书馆馆藏书目；结果含作者、出版社、出版时间、ISBN、丛书名、分类号、页数、价格
- 门槛：无
- 实测：2026-10-03，macOS + curl（desktop UA）：`GET http://opac.bac.gov.cn:8080/NTRdrBookRetr.do?SearchKey=北京党的建设研究报告&SearchType=title&searchWay=searchWay` → `HTTP 200 size=110080`，`<title>书目查询</title>`
- 上游：`http://opac.bac.gov.cn:8080/`

## 细节

- 书名带"．"分卷号（如《北京党的建设研究报告．2019》），检索时只输主书名即可出全系列。
- 各市/区图书馆 OPAC 类似（URL 参数同族），改主机即可复用。
