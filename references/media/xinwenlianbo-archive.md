# xinwenlianbo-archive —— 《新闻联播》每日文字稿归档

把央视网《新闻联播》每日文字稿抓成 Markdown 并按日存档在 GitHub 仓库 `news/YYYYMMDD.md`，用 GitHub Actions 每日自动更新（源码 `fetch.js` + `index.js`，`update.yml` 定时跑）。**可直接 raw 直取**，是我们拿"新闻联播文字稿语料"（政策发布、领导人活动时间线）最省事的一条通道——不用碰央视站、不用解析播放器。

- 去哪找：repo <https://github.com/DuckBurnIncense/xin-wen-lian-bo>；逐日文件 `news/YYYYMMDD.md`；日期总索引在 `README.md`（`<!-- INSERT -->` 段，Actions 自动插入最新日期）；上游节目源 央视网 `tv.cctv.com`（仓库即从此抓取，原文方更权威但无稳定文本接口）
- 什么时候用：需要按**日期**取新闻联播全文/摘要做：政策事件时间线、领导人活动对齐、文本语料/词频、与人民日报头版交叉验证；尤其要 **2022-09 之后**的每日连续文本。
- 怎么取：

  ```bash
  # 取某一天
  curl -sS "https://raw.githubusercontent.com/DuckBurnIncense/xin-wen-lian-bo/master/news/20261001.md"
  # 取目录（全部可用日期）
  curl -sS "https://raw.githubusercontent.com/DuckBurnIncense/xin-wen-lian-bo/master/README.md" \
    | grep -oE 'news/[0-9]{8}\.md' | sort
  # 批量取一个日期区间（例：2026-09 全月）
  for d in $(seq -w 1 30); do curl -sS -o "xwlb_202609$d.md" \
    "https://raw.githubusercontent.com/DuckBurnIncense/xin-wen-lian-bo/master/news/202609$d.md"; done
  ```

  也可 `gh api repos/DuckBurnIncense/xin-wen-lian-bo/contents/news --jq '.[].name'` 列目录。
- 覆盖：仓库含 **2022-09-24 起至今**逐日文件（README 索引显示连续每日）；每日一次，通常**滞后约 1 天**（当日档次日可见）。
- 门槛：无（MIT；raw 直取）。
- 实测：2026-10-03，macOS + curl：`news/20261001.md` → **200 / 17,578B**，含 `## 新闻摘要` 与分条正文（首条《求是》杂志发表习近平总书记重要文章…）；`https://duckburnincense.github.io/xin-wen-lian-bo/` → **404**。
- 上游：<https://github.com/DuckBurnIncense/xin-wen-lian-bo>（MIT）

## 细节

- 格式：每个 md = `# 《新闻联播》 (YYYYMMDD)` + `## 新闻摘要`（"本期节目主要内容"分条编号）+ 各条正文段落/口播稿；可 `grep` 关键词直接定位到具体条（标题在正文前一行）。

## 坑

- 许可 **MIT**（可用，建议注明来源）。
- 仅《新闻联播》**一档**节目，不含《焦点访谈》等其他央视栏目。
- 走 `raw.githubusercontent.com`：本机可用，但 GitHub `git clone` 在本网络**不稳定**（HTTP2 framing / 超时），优先 raw 或 `gh api`。
- 无 gh-pages 网页版（`index.html` 实测 404），别去 `duckburnincense.github.io` 找。
