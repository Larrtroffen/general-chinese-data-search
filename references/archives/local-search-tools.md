# local-search-tools —— 本地全文检索工具

抓回来的方志/微信/公报文本躺在 JSONL 里没法用 → 需要**本地全文检索**。三条路：**① SQLite FTS5（标准库、零依赖、中文经 trigram 分词后本机实测可用，推荐）**；② whoosh-reloaded（纯 Python 索引框架，Py3.9 可装，但**上游已停止维护**）；③ jieba（中文分词，索引前置步骤，长期未更新）。本机 Python **3.9.6**、无 requests/bs4/lxml、有 Homebrew Python 3.12 备选。

- 去哪找：
  - ① SQLite FTS5：Python 标准库自带（需 SQLite ≥3.34；本机 `3.54.0`），零安装。
  - ② whoosh-reloaded：`pip3 install Whoosh-Reloaded`（PyPI，纯 Python）。
  - ③ jieba：`pip3 install jieba`（PyPI，MIT）。
  - 上游：https://github.com/Sygil-Dev/whoosh-reloaded · https://github.com/fxsjy/jieba
- 什么时候用：
  - 语料已落盘，要**反复按关键词查**（比每次 `grep` 大目录快一个数量级，支持打分/字段查询/摘要高亮）；
  - 要**离线、无网络、无 key** 地做「站内检索」（对照各源站的在线检索）；
  - 做**词频/共现/主题词**统计（先分词再统计）。
- 怎么取：
  - **A. SQLite FTS5 + trigram（首选，零安装，本机实测通过）**：`unicode61` 分词器**不切中文**（整句一个 token，`MATCH '中关村'` 查不到）；改用 **`tokenize='trigram'`** 即可做中文子串检索（需 SQLite ≥3.34；本机 `3.54.0`）。
    ```python
    import sqlite3, json
    db = sqlite3.connect('corpus.db')
    db.execute("CREATE VIRTUAL TABLE IF NOT EXISTS docs USING fts5(title, body, url UNINDEXED, tokenize='trigram')")
    for line in open('crawl.jsonl'):                      # JSONL → 索引（断点续跑就加主键+try/except）
        r = json.loads(line)
        db.execute('INSERT INTO docs(title, body, url) VALUES (?,?,?)', (r['title'], r['content'], r['url']))
    db.commit()
    for title, url in db.execute("SELECT title, url FROM docs WHERE docs MATCH ? ORDER BY rank LIMIT 20", ('中关村',)):
        print(title, url)
    # 摘要高亮：SELECT snippet(docs, 1, '<b>', '</b>', '…', 12) …
    ```
    要点：trigram **要求查询串 ≥3 字符**（中文即 ≥3 字）→ 2 字人名/简称只能 `LIKE '%王%'`，或先 jieba 分词再存「空格分隔文本 + unicode61」。`ORDER BY rank` = BM25。
  - **B. whoosh-reloaded（PyPI `Whoosh-Reloaded` 2.7.5）**：
    ```bash
    pip3 install Whoosh-Reloaded      # 纯 Python；wheel 标 py2.py3-none-any（类声明覆盖 3.4–3.12，含 3.9）
    ```
    ```python
    from whoosh.index import create_in
    from whoosh.fields import Schema, TEXT, ID
    from whoosh.qparser import QueryParser
    schema = Schema(path=ID(stored=True), title=TEXT(stored=True), content=TEXT(stored=True))
    ix = create_in('idx', schema); w = ix.writer()
    for d in docs: w.add_document(path=d['url'], title=d['title'], content=d['content'])
    w.commit()
    with ix.searcher() as s:
        for hit in s.search(QueryParser('content', ix.schema).parse('地方志'), limit=20):
            print(hit['title'], hit.score, hit.highlights('content'))
    ```
    ⚠️ 仓库 README 顶部横幅：**"This repository (whoosh-reloaded) is NO LONGER MAINTAINED"**（最后发布 2024-02）。新项目优先 A，或换 tantivy/Meilisearch；whoosh 只适合沿用既有代码。
  - **C. jieba（PyPI `jieba` 0.42.1，MIT）**：
    ```bash
    pip3 install jieba
    ```
    ```python
    import jieba
    list(jieba.cut('北京市海淀区人民政府'))          # 精确模式
    list(jieba.cut_for_search('中关村科学城'))       # 搜索引擎模式（细粒度，适合建索引）
    jieba.load_userdict('dict.txt')                  # 必做：补地名全称/机构简称/官职等自定义词
    ```
    与 A 组合：把 `jieba.cut_for_search(text)` 的空格串存进 `unicode61` 的 FTS5 表 → 2 字词也能命中（代价：snippet 是分词后文本）。PyPI **只有 sdist（无 wheel）**，`pip install` 时本地构建；`requires_python` 为空、classifiers 未覆盖 3.9+（老式声明），**未本机安装**。
- 覆盖：SQLite FTS5（标准库，trigram 中文子串）+ whoosh-reloaded（Py3.9/3.12，停维护）+ jieba（分词）。A 方案本机实测通过；B/C 仅上游声明（未安装）。
- 门槛：全部本地离线，无许可/网络风险；whoosh/jieba 只作依赖使用，**不复制其代码进本仓**。**别把索引文件放进本仓**（派生物、体积大）→ 索引放 `/tmp`/工作目录，只把脚本与用法写进 `scripts/` 的说明。FTS5 trigram 索引体积约为原文 3–5×（十万级文章量级没问题，百万级考虑 jieba+unicode61）。召回 vs 精度：trigram = 精确子串（召回准）；jieba = 可能切错专名 → **务必 `load_userdict`**。
- 实测：2026-10-03，macOS 27（arm64），系统 `python3` **3.9.6**（`sqlite3.sqlite_version 3.54.0`）。① `create virtual table t using fts5(x, tokenize='unicode61')` → OK，但 `MATCH '中关村'` **返回空**（中文未分词）；改 `tokenize='trigram'` → 插入 3 条中文后，`MATCH '中关村'`/`'地方志'`/`'老旧小区'`/`'中关村科学城'` **全部正确命中**，`LIKE '%地方志%'` 亦命中。② `curl https://pypi.org/pypi/Whoosh-Reloaded/json` → 2.7.5、wheel `py2.py3-none-any`、classifiers 含 3.9；`curl https://pypi.org/pypi/jieba/json` → 0.42.1、**仅 tar.gz**、`requires_python` 空；`gh api` → whoosh `size=31761 KB`/`pushed_at 2026-08-16`、jieba `size=56033 KB`/`pushed_at 2024-08-21`；tarball 读 whoosh README 确认 **NO LONGER MAINTAINED**。③ **未安装 whoosh/jieba**（遵守「不执行第三方安装」纪律）→ B/C 用法为上游声明；A 为实测通过路径。
- 上游：https://github.com/Sygil-Dev/whoosh-reloaded · https://github.com/fxsjy/jieba
