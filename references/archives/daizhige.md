# daizhige —— 殆知阁古籍 txt 全库

`garychowcmu/daizhigev20`：汉籍**纯文本**大合集，按佛藏/儒藏/史藏/子藏/集藏/易藏/医藏/艺藏/诗藏/道藏 分目录，二级目录进去就是「一本文档」。**不是在线检索站，而是一个可整包下载的语料库**——适合「要语料、不挑版本」的场景（抄本来源杂、无校勘，学术引用要谨慎）。

- 去哪找：
  - 仓库（顶层目录 = 藏）：`https://github.com/garychowcmu/daizhigev20`
  - 整包下载（约 2.1 GB）：`https://github.com/garychowcmu/daizhigev20/archive/refs/heads/master.zip`（README 里的 `archive/master.zip` 同效）
  - 单文件 raw（按需取，别整包）：`https://raw.githubusercontent.com/garychowcmu/daizhigev20/master/<藏>/<子路径>/<书名>.txt`（中文路径需 URL 编码）
  - 说明：仓内 `README.md` / `使用须知.md`
- 什么时候用：
  - 需要**大量古籍文本做检索/统计/词频/训练**，且**不要求底本精良**；
  - 想要**一次拿全、离线可 grep**（不用逐个仓拉，对比 `kanripo.md` 的「一书一仓」）；
  - 手上有生僻书名/句子的**线索定位**（先整包 grep 定位到书，再回 `kanripo`/`ctext` 找精校本）。
- 怎么取：
  ```bash
  # 只看目录（不下载）：顶层 10 个「藏」
  gh api repos/garychowcmu/daizhigev20/contents --jq '.[]|[.name,.type]|@tsv'
  # 列某个藏的二级目录（示例：儒藏）
  gh api repos/garychowcmu/daizhigev20/contents/儒藏 --jq '.[]|.name' | head
  # 整包（2.1 GB；建议 --depth 1 浅克隆或直接下 zip）
  git clone --depth 1 https://github.com/garychowcmu/daizhigev20 /tmp/dzg
  # 取单本（例：要某子目录下的 txt），中文路径要编码：
  curl -L 'https://raw.githubusercontent.com/garychowcmu/daizhigev20/master/%E5%84%92%E8%97%8F/...'
  ```
- 覆盖：体积 —— `gh api` 报 `size=2177348`（KB）≈ **2.1 GB**；顶层 10 个藏目录 + `README.md` + `使用须知.md`。**不要克隆进本仓**（交付纪律：只记录入口）。粒度：目录 = 藏 → 书（一本一个大 txt），**未做章节切分**（README 里作者自己招志愿者做三级目录）。更新：基本停更（`pushed_at = 2024-05-13`）；百度网盘链接**已失效**，README 让走 GitHub「clone or download」。
- 门槛：**无 license 文件** → 只记链接与用法，不复刻文本进我们仓库；古籍本体为公版，但**文本整理成果的权利状态不明**，对外发布前自行评估。文本质量：来源不统一、无校勘记、可能有错讹与重复；**引用前必须与精校本（Kanripo / 中华经典古籍库 / 点校本）核对**。大仓库操作建议：`git clone --depth 1`；浏览器打开超大目录（如「医藏」）可能卡；大文件解压注意磁盘。
- 实测：2026-10-02，macOS 27（arm64）。① `gh api repos/garychowcmu/daizhigev20 --jq '.size'` → **2177348**（KB ≈ 2.1 GB）；`--jq '[.size,.license.spdx_id,.pushed_at,.default_branch]|@tsv'` → `2177348  (空 license)  2024-05-13T18:36:27Z  master`。② `gh api repos/garychowcmu/daizhigev20/contents --jq '.[]|[.name,.type,.size]|@tsv'` → 顶层 10 个目录（佛藏/儒藏/医藏/史藏/子藏/易藏/艺藏/诗藏/道藏/集藏）+ `README.md`(1782 B) + `使用须知.md`(597 B) + `_config.yml`。③ raw 取 `README.md`、`使用须知.md`（URL 编码中文路径）→ **200**，确认「百度云链接已失效，走 GitHub clone/download」与检索提示。**未整包下载**（2.1 GB，按需再取）。
- 上游：`https://github.com/garychowcmu/daizhigev20`

## 细节

### 入口表

| 入口 | 地址 |
|---|---|
| 仓库（顶层目录 = 藏） | `https://github.com/garychowcmu/daizhigev20` |
| 整包下载（约 2.1 GB） | `https://github.com/garychowcmu/daizhigev20/archive/refs/heads/master.zip`（README 里的 `archive/master.zip` 同效） |
| 单文件 raw（按需取，别整包） | `https://raw.githubusercontent.com/garychowcmu/daizhigev20/master/<藏>/<子路径>/<书名>.txt`（中文路径需 URL 编码） |
| 说明 | 仓内 `README.md` / `使用须知.md` |
