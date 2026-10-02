# stat-yearbook-download —— 统计年鉴与公报批量下载

- 去哪找：**国家统计局年鉴** `https://www.stats.gov.cn/sj/ndsj/`（逐年 `…/ndsj/{年}/indexch.htm`）；**全国统计公报** `https://www.stats.gov.cn/sj/tjgb/ndtjgb/qgndtjgb/index.html`；**省级年鉴**见 `../regional/provincial-yearbooks.md`；年鉴聚合站 `http://www.tjcn.org/tjnj/`、`https://www.tjnjdata.com/`。
- 什么时候用：要把**整本统计年鉴/公报**按章节批量取回本地（做语料、离线查表、OCR 提取数字）；要判断某年年鉴是「HTML 表」还是「扫描图片」；要给年鉴站写可复现的下载配方。
- 怎么取：年鉴正文是 **frameset** —— `indexch.htm`（壳）→ `left.htm`（目录，列出全部资源）→ 逐表页/图片/PDF。**先抓 `left.htm`、正则抽资源直链、再 `wget -i` 批量下**，比递归爬全站更准更快。统计公报另有「列表页 → 文章页 → PDF」三段规律。
- 覆盖：国家统计局年鉴（约 2000 年代至今，逐年一份）；各省统计年鉴（路径无统一规律，见 `../regional/provincial-yearbooks.md`）；全国/各省统计公报（HTML 正文 + PDF）。
- 门槛：官方站免费、无需登录；注意 `robots`、限速（本库纪律：≤3 请求/主机、间隔 ≥1.5s）。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA——国家年鉴 `sj/ndsj/2024/indexch.htm` `200/887B`（frameset）；同年 `left.htm` 抽出 **759 条唯一资源**（702 `jpg` 表图 + 27 `pdf` 附录 + `sm*.htm` 章节说明），抽出的 `html/C01-01.jpg` 实取 `200 / 222425B / image/jpeg`；`sj/ndsj/2025/indexch.htm`、`2023`、`2022` 均 `200`；四川 `tjj.sc.gov.cn/scstjj/tjnjnew/{2024,2025}/zk/indexch.htm` `200/886B`（left 含 376 jpg / 20 pdf）；河南 OSS 直链 `…/tjnj/2025/zk/indexch.htm`；上海 `tjj.sh.gov.cn/tjnj/` 2025 卷页 `200`。
- 上游：国家统计局、各省统计局官网。

## 细节

### 一、国家统计局年鉴（`stats.gov.cn`）

URL 骨架：
```
https://www.stats.gov.cn/sj/ndsj/{年}/indexch.htm     # 页面壳（frameset，GB2312）
https://www.stats.gov.cn/sj/ndsj/{年}/left.htm        # 目录：列出全书资源直链
https://www.stats.gov.cn/sj/ndsj/{年}/html/sm{NN}.htm # 各章「要 说」/章节说明
https://www.stats.gov.cn/sj/ndsj/{年}/html/C{CC}-{NN}.jpg   # 正文数据表（图片）
https://www.stats.gov.cn/sj/ndsj/{年}/html/zb{NN}.pdf       # 各章附录 PDF
```

- **批量下载配方**（照抄即用；只抽直链、不下正文）：
  ```bash
  Y=2024
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
  curl -s -A "$UA" "https://www.stats.gov.cn/sj/ndsj/$Y/left.htm" \
    | grep -oE 'html/[A-Za-z0-9_.-]+\.(jpg|pdf|htm)' | sort -u \
    | sed "s|^|https://www.stats.gov.cn/sj/ndsj/$Y/|" > urls.txt
  wc -l urls.txt            # 2024 卷 759 项（702 jpg + 27 pdf 等）
  wget -c -x -nH --cut-dirs=0 --wait=1 -i urls.txt -P ndsj$Y/
  ```
- 也可用本库脚本（不解析正文、自动建目录）：
  ```bash
  python3 scripts/fetch.py 'https://www.stats.gov.cn/sj/ndsj/2024/html/C01-01.jpg' --out ndsj2024/C01-01.jpg
  python3 scripts/site_crawl.py --host www.stats.gov.cn \
      --seeds https://www.stats.gov.cn/sj/ndsj/2024/left.htm --budget 40 --delay 1.5
  ```
- **形态判断**：2022–2025 卷正文表为 **`html/C*.jpg` 图片**（需 OCR 才能拿数字），附录为 `zb*.pdf`；更早年份可能是 HTML 表。先看 `left.htm` 里 `.jpg` 与 `.htm` 谁多，再决定走 OCR 还是解析。

### 二、全国统计公报（`stats.gov.cn`）

```
列表  https://www.stats.gov.cn/sj/tjgb/ndtjgb/qgndtjgb/index.html
文章  https://www.stats.gov.cn/sj/zxfb/{YYYYMM}/t{YYYYMMDD}_{id}.html
PDF   https://www.stats.gov.cn/zs/tjwh/tjkw/tjqk/zgxxb/{YYYYMM}/P{timestamp}.pdf
```

```bash
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
curl -s -A "$UA" 'https://www.stats.gov.cn/sj/tjgb/ndtjgb/qgndtjgb/index.html' \
  | grep -oE 'href="[^"]*t20[0-9]{6}_[0-9]+\.html"' | sort -u
```
- 列表页 48 条左右（实测），正文同时在 `/xxgk/sjfb/…` 与 `/sj/zxfb/…` 有副本；引用以官网最新路径为准。

### 三、省级年鉴直链规律（补测，2026-10-03）

| 省 | 直链规律 | 实测 |
|---|---|---|
| 四川 | `https://tjj.sc.gov.cn/scstjj/tjnjnew/{年}/zk/indexch.htm` → `left.htm`（376 jpg / 20 pdf） | ✅ 2024、2025 卷 200 |
| 河南 | `https://oss.henan.gov.cn/sbgt-wztipt/attachment/hntjj/hntj/lib/tjnj/{年}[nj]/zk/indexch.htm` | ✅ 栏目页列出 2016–2025 卷（注意 2025/ 无后缀、2024nj/、2023nj/、2022/ 后缀不一） |
| 上海 | `https://tjj.sh.gov.cn/tjnj/{YYYYMMDD}/{hash}.html`（每年一个落地页，再从页面进各表） | ✅ 2025 卷页 200 |
| 广东 | 年鉴 `https://stats.gd.gov.cn/gdtjnj/`（上游声明，未本机请求） | ⚠️ |
| 其他省 | 无统一规律，逐省见 `../regional/provincial-yearbooks.md` | 该卡有总表 |

- 省级年鉴同样多为 **frameset + `zk/indexch.htm` + `left.htm`**（四川、河南一致）；照上面「一」的配方换 base URL 即可。

### 四、与 `data.stats.gov.cn` 的分工

- 要**具体指标的数值**（可跨年/跨省拼接）→ 用国家统计局数据库 API（见 `../stats/data.stats.gov.cn.md`），别下年鉴图片再 OCR。
- 要**年鉴原文/版式/分县细表** → 用本卡的批量下载配方。

## 坑

1. **年鉴表是 JPG 图片**（近年国家卷、四川卷均如此）：直接下载得到图片，数字需 OCR；先用 `left.htm` 判形态再定方案。
2. `indexch.htm` 是 **GB2312 编码的 frameset 壳**，`curl` 只拿到壳；必须跟 `left.htm`。用 `iconv -f gb2312 -t utf-8` 处理文本。
3. **目录里的资源名逐年/逐省漂移**（`C01-01.jpg` vs `C0101.htm`、`2025/` vs `2024nj/`），别写死文件名，一律从 `left.htm`/栏目页动态抽。
4. 站内 `window.open('aa.htm')` 之类脚本引用的页在官网上 **404**（实测），别当资源目标。
5. 大批量 `wget` 前置 `--wait=1`，并控制并发；年鉴动辄数百 MB，**先 `urls.txt` 核对条数再下**。
6. 河南年鉴挂在 **OSS（`oss.henan.gov.cn`）**上，与省统计局主站不同主机；限速/robots 按 OSS 与统计局站分别遵守。
7. 统计公报数字**逐年修订**，离线留档要连同抓取日期与官方 URL 一起记。
