# ncc-cma.net —— 气候监测指数与公报

- 去哪找：国家气候中心 `https://www.ncc-cma.net/`；气候系统监测·诊断·预测（cmdp）`http://cmdp.ncc-cma.net/`；资料服务/下载 `http://cmdp.ncc-cma.net/cn/download.htm`；监测产品 `/Monitoring/cn_report.php?product=<name>`。
- 什么时候用：要**气候监测与指数**——74 项大气环流指数、130 项气候监测指数、160 站降水/气温序列、ENSO/季风/积雪/海冰/干旱监测、气候公报；做气候诊断、ENSO-经济、极端事件背景。
- 怎么取：cmdp 站多为**静态/半静态页面 + 直接文件**，匿名可取：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # 130 项监测指数（全序列，约 950 KB 纯文本，含表头与月份列）
  curl -sS -A "$UA" 'http://cmdp.ncc-cma.net/download/Monitoring/Index/index_all.txt' | head -c 300
  # 资料服务索引页
  curl -sS -A "$UA" 'http://cmdp.ncc-cma.net/cn/download.htm'
  # 下载频道 / 160 站 / 74 项环流指数
  # /nccdownload/index.php?ChannelID=<n>、/nccdownload/data_160.php、/nccdownload/data_74.php
  ```
  监测产品为 PHP 页面：`/Monitoring/cn_report.php?product=cn_report_enso|monsoon|snow|ice|bulletin|gmpb`；返回 HTML（图表 + 文字）。
- 覆盖：全国 + 全球环流 · 逐日/逐月（指数序列可回溯数十年）· 站点/指数；气象要素与气候监测产品。
- 门槛：**免费匿名**（指数文件与监测产品直接可下；页脚有「会员中心」但本机测试的文件无需登录）。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA）——`https://www.ncc-cma.net/` → 200（55,519 B）；`http://cmdp.ncc-cma.net/` → 200；`/cn/download.htm` → 200（12,094 B，列出「160站→降水/温度、74项环流→指数文件、130项检测监测指数、逐月大气环流指数、逐月海温指数」等）；`/download/Monitoring/Index/index_all.txt` → **200 `text/plain`，974,352 B**（表头 `yearmon 1 2 3 …`）；`/nccdownload/index.php?ChannelID=5` → 200。
- 上游：中国气象局国家气候中心（cmdp 为其监测·诊断·预测业务平台）。

## 细节

- 下载页给出的关键路径（均 200）：`../160/160.php`、`../160/74.php`、`../Monitoring/cn_index_130.php`、`../cn/cn_data.php?cat=1..7`、`../nccdownload/{index.php?ChannelID=<n>,data_160.php,data_74.php}`。
- 直接文件还有 `download/Monitoring/Index/{index_allstd.txt,M_Atm_Nc.txt,M_Oce_Er.txt,Index_definition.docx,Index_readme.docx}` 与 `download/Monitoring/Index/dailymonitoring.doc`（字段说明）。
- 页面编码 **GB2312**；文件多为纯文本/`.txt`，可直接进 pandas。

## 坑

1. **编码**：页面与部分文件是 GB2312，`curl`+UTF-8 解码会报错/乱码，需显式解码。
2. 站内链接多用相对路径（`../download/…`），抓取时带 Referer 并按目录拼接。
3. 「会员中心」栏目存在，但本机测试的核心指数文件**无需登录**；会员专属内容范围未逐项验证，别默认全站匿名。
4. 与 `data.cma.cn`（[`data.cma.cn.md`](data.cma.cn.md)）分工不同：这里是指数/监测产品，不是原始观测数据下载。
5. 气候公报等产品有**事后修订**，引用注明产品名与发布时间。
