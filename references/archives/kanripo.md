# kanripo —— 漢籍リポジトリ 古籍全文

`kanripo`（日本「漢籍リポジトリ」）把**汉文古籍全文**拆成**一部书一个 GitHub 仓**（org 下共 **9355** 个 repo），文本是 TEI 风格纯文本（带页码锚点 `<pb:...>`、行符号 `¶`）。入口组织在 **`kanripo/KR-Catalog`**（目录仓，含分类清单）。对中文研究的价值：**公版古籍全文、可 raw 直取、按卷分文件、可 git 克隆做本地语料**——且**不需要 key、不被 Cloudflare 挡**（对比 `ctext.md`）。

- 去哪找：
  - 站点（检索 UI）：`https://www.kanripo.org/`（裸域 `https://kanripo.org/` 实测返回 **HTTP 525**，用 `www`）
  - 目录仓（分类清单、ID 规则）：`https://github.com/kanripo/KR-Catalog`
  - 单书仓：`https://github.com/kanripo/<KR_ID>`（如 `kanripo/KR1a0001` = 周易）
- 什么时候用：
  - 要**古籍/经史子集原文**（周易、论语、史书、道藏、大藏经…）做检索、引文核对、语料统计；
  - 要**稳定可复现的取数**：raw URL 直连、可校验、可增量拉；
  - 需要在本地建**全文索引**（配合 `local-search-tools.md`）。
  > 不要用 `ctext.org` 做批量抓取（见 `ctext.md`）；Kanripo 是更省事且不违反条款的正路。
- 怎么取：
  ```
  raw 模板（已实测，《周易》可取）：
  https://raw.githubusercontent.com/kanripo/<KR_ID>/<branch>/<KR_ID>_<卷号3位>.txt
  例：https://raw.githubusercontent.com/kanripo/KR1a0001/master/KR1a0001_001.txt
  ```
  目录/文件清单也可走 API：`gh api repos/kanripo/KR1a0001/contents --jq '.[]|[.name,.size]|@tsv'`。
  批量拉一部书：`git clone --depth 1 https://github.com/kanripo/KR_ID /tmp/kr/KR_ID`；**全量 9355 个仓不要克隆**（先按目录挑 ID）。
- 覆盖：经史子集 + 道藏 + 大藏经（taisho.org 对照）+ 四部叢刊/四庫全書（`general/*.org` 清单）；**按卷分文件**（`_001.txt`、`_002.txt`…）。格式：纯文本 + 标记（`<pb:KR1a0001_tls_001-1a>` 页码锚点、`¶` 分行、`#+TITLE/#+PROPERTY` 头）。要纯文本直接 grep，要结构化需自己剥标记。更新：低频（单书仓多为 2017 前后一次性导入）；`pushed_at` 不代表内容更新。
- 门槛：许可 —— repo **无 license 字段**（内容为公版古籍；底本多为四庫全書/大正藏）。我们只记录入口与用法，**不把文本拷进本仓**；正式引用请核对底本与站点声明。单仓很小（示例 KR1a0001 = 66 KB），raw 直取快；**别一次拉几千个仓**（GitHub rate limit + 磁盘），按需取。
- 实测：2026-10-02，macOS 27（arm64）。① `gh api 'orgs/kanripo/repos?per_page=1' -i` → `Link: ... page=9355; rel="last"`（**org 下共 9355 个仓**）。② `curl -s -o KR1a0001_001.txt -w '%{http_code} %{size_download}' https://raw.githubusercontent.com/kanripo/KR1a0001/master/KR1a0001_001.txt` → **200 / 5771 字节**，正文首行 `#+TITLE: 周易`、`<pb:KR1a0001_tls_001-1a>`、`** 《乾第一》`、`䷀乾下乾上`、`初九、潛龍勿用。`。③ `gh api orgs/kanripo/repos` 与 `KR-Catalog` tarball（3.5 MB）解包确认 `KR/KR1*.txt` 分类清单与 `KR1a0001 周易(正文)` 条目、`general/sbck.org`（四部叢刊）清单。④ `https://www.kanripo.org/` → 200（8.4 KB）。
- 上游：https://github.com/kanripo/KR-Catalog

## 细节

### ID 规则（`KR-Catalog/KR/KR*.txt` 与 `README.org`）

```
KR1 經部 KR1a 易類 … KR1j 小學類     KR2 史部 KR2a 正史 … KR2o 史評
KR3 子部 KR3a 儒家 … KR3l 小說家      KR4 集部 KR4a 楚辭 … KR4j 詞曲
KR5 道部 KR6 佛部                     general/ 另收 四部叢刊(sbck)、四庫全書(skqs1-4)
ID 形如 KR<部><類><4位序> 例：KR1a0001（周易正文）
```

目录条目字段：`KR_ID`、书名+作者+朝代、`CUSTOM_ID`（如 `ZB1a0001`、`H15-23-0084`）、`SOURCE`（如「四庫全書 文淵閣版, V7.1, p1」）、`EXTENT`（卷数）。
