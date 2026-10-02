# lawtext-laws —— flk 全量离线镜像

把**国家法律法规数据库**的 docx 用 `markitdown` 批量转成 markdown 的镜像站源码（Hugo 站点）；另有两个独立仓库保存**官方 docx/doc 原件**。适合离线全文、含已废止版本、按官方条目名/ID 取件。

- 去哪找：
  - markdown 镜像：`https://github.com/lawtext/laws`（站点源码，`content/` 即正文）
  - docx 原件镜像：`https://github.com/lawtext/law-flk-vol1`（全国性，约 51 MB）、`https://github.com/lawtext/law-flk-vol2`（地方性，约 640 MB）
  - raw 模板：`https://raw.githubusercontent.com/lawtext/laws/master/content/<类别>/<bbbs>.md`
- 什么时候用：
  - 要**法条逐条 / 离线**、且需要 flk 的**全量（含已废止）**纯文本：按 flk id（bbbs）直接取 md。
  - 要官方 **docx/doc 原件**（做版式、红头、公报核验）→ vol1（全国）/ vol2（地方）。
  - 按"法律名 + 日期"检索时，先读 vol1 的 `records.json` 拿 bbbs/文件名。
- 怎么取：
  ```bash
  # 1) 正文 markdown（目录名是中文，需 URL 编码；文件名=bbbs）
  curl -s 'https://raw.githubusercontent.com/lawtext/laws/master/content/%E6%B3%95%E5%BE%8B/016c39ca7739492cab1fe3aef22941c7.md'
  # 2) 索引（名称→bbbs/文件/效力）——vol1 的 records.json
  curl -s 'https://raw.githubusercontent.com/lawtext/law-flk-vol1/main/records.json'
  # 3) docx 原件
  curl -sLO 'https://raw.githubusercontent.com/lawtext/law-flk-vol1/main/docx/<类别>/<标题>_<日期>_<bbbs>.docx'
  ```
  目录类别：`content/{法律, 行政法规, 监察法规, 司法解释, 宪法}/`（中文名，curl 需 `--data-urlencode` 或不编码直接放 path）。
- 覆盖：
  - `lawtext/laws`：`content/` 共 **2,548** 个 md（全国性，含已废止；地方性暂未纳入站点）。GitHub Actions 定期自动更新（工作流 `build/deploy`）。
  - `lawtext/law-flk-vol1`：`docx/` **2,517** 个文件（分类同上）；`records.json` 记录 `update`、`stats` 与每条 `bbbs/title/gbrq/sxrq/sxx/zdjgName/flxz/my_file`。
  - `lawtext/law-flk-vol2`：地方法规 docx（体量大，按需 sparse 拉取）。
- 门槛：**无 license 文件**：只记录链接与用法，不复制其内容进我们仓库；正式引用以 flk 原文为准。markdown 由 `markitdown` 自动转换，"文本内容仅供参考"（README 自述），可能有格式损失。raw 单文件走 GitHub（大文件用 `media.githubusercontent.com`）；中文目录名必须 URL 编码。地方性法规在 `laws` 站点未展示；要地方原件用 vol2。
- 实测：2026-10-02，macOS，curl 8.x。① `GET .../lawtext/laws/master/README.md` → **HTTP 200**（6,257 B）。② `GET content/%E6%B3%95%E5%BE%8B/016c39ca7739492cab1fe3aef22941c7.md` → **HTTP 200**；frontmatter 显示《中华人民共和国社会救助法》，`effective_date: 2026-07-01`，`urls: [https://flk.npc.gov.cn/detail?id=016c…]`。③ `GET law-flk-vol1/main/records.json`（range 0-700）→ **HTTP 206**，`update=20261001T19+0800`，`stats.total=2508`。④ `GET law-flk-vol1/main/docx/%E5%AE%AA%E6%B3%95/中华人民共和国宪法修正案（1988年）_19880412_2c909fdd678bf17901678bf594240005.docx` → **HTTP 200**，26,464 B。⑤ GitHub 树统计：`laws` content blob 2,548；vol1 blob 2,517。
- 上游：`https://github.com/lawtext/laws` ｜ 原件：`https://github.com/lawtext/law-flk-vol1`、`https://github.com/lawtext/law-flk-vol2`

## 细节

### 单条 md 结构（实测 frontmatter）

`id`(=bbbs) / `title` / `LinkTitle` / `file`(docx 名) / `author`(制定机关) / `date` / `publication_date` / `effective_date` / `status`(如`有效`) / `group` / `categories[]` / `tags[]` / `keywords[]` / `urls[]`（`https://flk.npc.gov.cn/detail?id=<bbbs>`）；正文为 markdown。
