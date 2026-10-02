# zotero-cn —— 中文元数据与 GB/T 7714 引文

Zotero 中文生态三件套（`l0o0/jasminum` + `l0o0/translators_CN` + `zotero-chinese/styles`）：**translators_CN** 是 99 个中文站点抓取器（元数据从哪抓、字段怎么映射）；**jasminum** 是 Zotero 插件，把知网元数据抓取、中文表达式/引文格式装进 Zotero；**styles** 是 343 个中文 CSL 引文样式（GB/T 7714 各版本）。**要 GB/T 7714 引文 → styles；要中文库元数据抓取逻辑 → translators_CN + jasminum；要中文条目落 Zotero → jasminum 或 Zotero Connector API。** 注意三个仓库都**不提供全文**，且 translators_CN/jasminum 为 AGPL —— 其代码**只可读不可抄进本仓**。

- 去哪找：
  - `https://github.com/zotero-chinese/styles`（88MB，勿全量克隆）—— 样式站 `https://zotero-chinese.com/styles/`；单样式 raw：`https://raw.githubusercontent.com/zotero-chinese/styles/main/src/<样式名>/<样式名>.csl`（目录名含全角括号与破折号，**必须 URL 编码**）。
  - `https://github.com/l0o0/jasminum`（1.7MB，Zotero 8/9 插件，v1.1.39）—— 知网元数据服务在 `src/modules/services/cnki.ts`。
  - `https://github.com/l0o0/translators_CN`（8.4MB，99 个 `*.js`）—— 也可从 Gitee 镜像取。
- 什么时候用：**GB/T 7714—1987/2005/2015**（顺序编码/著者-出版年/注释、双语、姓名大小写变体）引文与参考文献表；**知网元数据**（题名/作者/刊/年/卷期页/基金等，经知网导出接口）；**万方/维普/读秀/NCPSSD/人民网/数字报/flk/gov.cn 政策/统计局的元数据抓取规则**（translators_CN 有对应 translator）；中英文混排引文（需给条目设 `language: zh-CN` / `en-US`）。
- 怎么取：
  - 下载一个 GB/T 7714 样式（目录名含全角符号，**必须先 URL 编码**；实测可用）：
    ```bash
    P='src/GB-T-7714—2015（顺序编码，双语）/GB-T-7714—2015（顺序编码，双语）.csl'
    ENC=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$P")
    curl -s "https://raw.githubusercontent.com/zotero-chinese/styles/main/$ENC" -o gbt7714-2015.csl
    ```
  - 知网**元数据导出**（jasminum 主通道，需登录态 Cookie，返回含 EndNote/GBTREFER 文本）：
    ```bash
    curl -s -X POST 'https://kns.cnki.net/dm8/API/GetExport' \
      -H 'Content-Type: application/x-www-form-urlencoded' -H 'Referer: https://kns.cnki.net/kns8s/defaultresult/index' \
      -H 'Cookie: <知网登录 Cookie>' --data 'filename=<exportId>&uniplatform=NZKPT&displaymode=GBTREFER,learning,EndNote'
    # 检索接口：GET https://kns.cnki.net/kns8s/brief/grid（QueryJson 里 KuaKuCode 列库范围；明细见 papercash.md）
    # 海外镜像：https://chn.oversea.cnki.net/kns/Brief/GetGridTableHtml 与 /kns/Manage/APIGetExport
    ```
  - translators 自动更新源（jasminum 内置）：`https://oss.wwang.de/translators_CN`、`https://www.wieke.cn/translators_CN`、`https://ftp.zotero-chinese.com/translators_CN`、`https://ftp.linxingzhong.top/translators_CN`（均为目录索引页，`-L` 可列文件）。
  - 落入 Zotero：本机 Connector API `http://127.0.0.1:23119/connector`，头 `X-Zotero-Connector-API-Version: 3`，`saveItems`（201=成功，409=已存在）。
- 覆盖：**styles 343 个**中文样式（GB/T 7714 三版系 + 各刊/学位论文变体）；**translators_CN 99 个**，含 `CNKI.js`（`kns8s|kcms2|KNavi`）、`CNKI Scholar.js`、`Ncpssd.js`、`Wanfang Data.js`、`CQVIP.js`、`Duxiu.js`、`dpaper.js`（数字报 `dpaper.las.ac.cn`）、`gov.cn Policy.js`、`stats.gov.cn.js`、`flk.npc.gov.cn.js`、人民网系列。更新：仓库持续提交 + 上述 4 个自动更新源。许可：**styles = CC BY-SA 3.0**；**translators_CN = AGPL-3.0**；**jasminum = AGPL-3.0**。
- 门槛：styles 可匿名 raw 直取（CC BY-SA 3.0）；**知网元数据抓取必须登录/Cookie**；jasminum 元数据目前**只支持知网**（上游明说）；jasminum 插件需 Zotero 桌面；AGPL 仓库**不得复制代码入本仓**，只记链接与用法
- 实测：2026-10-02，macOS + curl / `gh api`：
  - `raw.githubusercontent.com/.../src/GB-T-7714—2015（顺序编码，双语）/….csl`（URL 编码后）→ **`HTTP 200`，15000B，`<style …version="1.0" …>`**；`https://zotero-chinese.com/styles/` → `200`（14967B）
  - 样式总数：`gh api repos/zotero-chinese/styles/git/trees/HEAD?recursive=1` 统计 `src/**/metadata.json` → **343**
  - 知网未登录直取 `kns.cnki.net/kns8s/brief/grid` → **`HTTP 403`**，`message` 为 `…/verify/home?captchaType=blockPuzzle…`（印证须登录/过滑块）
  - translators 更新源 `oss.wwang.de/translators_CN`、`ftp.zotero-chinese.com/translators_CN` → 301→`200` 目录索引页
  - **jasminum 插件与 Zotero 落库流程未本机实测**（需 Zotero 桌面 + 知网账号）
- 上游：`https://github.com/zotero-chinese/styles`（CC BY-SA 3.0）、`https://github.com/l0o0/jasminum`（AGPL-3.0）、`https://github.com/l0o0/translators_CN`（AGPL-3.0）

## 坑

- styles 的 `.csl` 用了 CSL-M 扩展，Zotero 安装时会弹"不是有效 CSL 1.0.2"警告（正常，忽略）。
- 中英混排必须在条目里设 `language` 字段（`zh-CN`/`en-US`，不能写 `中文`/`English`）。
