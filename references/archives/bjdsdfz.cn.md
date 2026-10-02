# bjdsdfz.cn —— 京网 北京地方志

中共北京市委党史研究室·北京市地方志编纂委员会办公室官网（京网）。北京市地方志系统的官方站：志书、区综合年鉴、行业年鉴的在线版。

- 去哪找：
  - 站点：`https://www.bjdsdfz.cn/`
  - 区综合年鉴（列表页）：`https://www.bjdsdfz.cn/dqzhnj.jhtml`
  - 单卷页：`https://www.bjdsdfz.cn/dqzhnj/{id}.jhtml`（如《北京朝阳年鉴（2021）》= `/dqzhnj/104031.jhtml`）
  - 年鉴集萃：`/njjc.jhtml`
- 什么时候用：查北京区综合年鉴、志书在线版；对照上海（`shtong.md`）做市区两级方志核对。
- 怎么搜：站内 `search.htm?q=` 为 JS 异步，curl 拿不到结果 → 用 `web_search site:bjdsdfz.cn {关键词}`，或直接翻栏目页。在线阅读走单卷页内嵌 pdfjs 阅读器：`https://bjsfzg.bjdsdfz.cn/dfz-api/dfz-pdfjs/build/generic-legacy/web/viewer.html?file=%2Fdownload%2FbyField%3FcontentId%3D{id}%26field%3Dpdf_file&id={id}`。
- 覆盖：区综合年鉴（当前公开索引仅列 2021 卷 5 区：通州/丰台/东城/房山/朝阳）；年鉴集萃。
- 门槛：目录/简介可直接抓；**全文需在数字方志馆注册登录后在线阅读**——**PDF 直连 `/download/byField?contentId={id}&field=pdf_file` 返回 302（登录判定）**，页内 JS 注释明确"preview 和 viewer 均有登录判定"，未登录无法取 PDF。老卷（如 2019 卷）可能已从公开索引下线，需登录方志馆账号检索，或走 CNKI 年鉴库（见 `../academic/cnki.net.md`）。
- 实测：（本卡未记录实测日期）列表页 `/dqzhnj.jhtml`、单卷页 `/dqzhnj/{id}.jhtml` 可 GET；PDF 端点返回 302 登录判定。
- 上游：`https://www.bjdsdfz.cn/`

## 细节

### 栏目与 URL

- 区综合年鉴（列表页）：`https://www.bjdsdfz.cn/dqzhnj.jhtml`
  - 当前公开索引仅列 2021 卷 5 区（通州/丰台/东城/房山/朝阳）。
  - 单卷页：`https://www.bjdsdfz.cn/dqzhnj/{id}.jhtml`（如《北京朝阳年鉴（2021）》= `/dqzhnj/104031.jhtml`）。
- 年鉴集萃：`/njjc.jhtml`。
