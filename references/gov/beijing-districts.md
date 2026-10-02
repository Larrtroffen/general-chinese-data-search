# 北京16区门户站群 —— 区级名录与任免检索

- 去哪找：
  - 16 区门户（HTTPS 首页）：`www.bjmy.gov.cn`（密云）、`www.bjdx.gov.cn`（大兴）、`www.bjhr.gov.cn`（怀柔）、`www.bjchp.gov.cn`（昌平）、`www.bjmtg.gov.cn`（门头沟）、`www.bjfsh.gov.cn`（房山）、`www.bjtzh.gov.cn`（通州）、`www.bjpg.gov.cn`（平谷）、`www.bjyq.gov.cn`（延庆，**仅 http**）、`www.bjsjs.gov.cn`（石景山）、`www.bjhd.gov.cn`（海淀）、`www.bjchy.gov.cn`（朝阳，**仅 http**）、`www.bjft.gov.cn`（丰台）、`www.bjshy.gov.cn`（顺义）、`www.bjdch.gov.cn`（东城）、`www.bjxch.gov.cn`（西城）。
  - 区人大/政协/区委/融媒体子站：`chynews.bjchy.gov.cn`（朝阳融媒体/朝阳报）、`chyrd.bjchy.gov.cn`（朝阳人大）、`hdqw.bjhd.gov.cn`（海淀区委）、`hdrd.bjhd.gov.cn`（海淀人大）、`renda.bjft.gov.cn`（丰台人大）、`renda.bjtzh.gov.cn`（通州人大）、`www.dcrd.gov.cn`（东城人大）、`www.bjlgbj.gov.cn`（市委老干部局，非区属）。
  - 专表：朝阳 `bjchy.gov.cn.md`、大兴 `bjdx.gov.cn.md`；年报通道 `beijing-xxgk.md`。
- 什么时候用：
  - 按区核对「街道/镇/乡」名录与主官（主任/镇长/乡长）任免；
  - 定位区级新闻、公报、政府文件（附件多为 Office/PDF）的抓取入口；
  - 与 `beijing-xxgk.md`（政府信息公开年报通道）配套使用。
- 怎么搜：
  - 探测（统一命令）：
    ```bash
    UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    curl -sSk -o /dev/null -w '%{http_code} %{content_type}\n' -m 20 -A "$UA" '<url>'
    ```
  - 抓取模板：
    ```bash
    UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'

    # ① UTF-8 门户正文（密云年报文章，本次实测 200 / text/html; charset=utf-8）
    curl -sSk -L -m 20 -A "$UA" \
      'https://www.bjmy.gov.cn/zwgk/zfxxgk/zfxxgknb/gknb2017/201802/t20180223_195744.html'
    # <title>高岭镇_2017年_北京市密云区人民政府< → 正文可直取

    # ② GB2312/GBK 区（朝阳，http 专用；本次实测 200 / text/html，meta=gb2312）
    curl -sSk -L -m 20 -A "$UA" \
      'http://www.bjchy.gov.cn/dynamic/zwhd/8a24fe836274afa5016275d0fada0067.html' | iconv -f gb18030 -t utf-8

    # ③ 只 http 的延庆
    curl -sSk -L -m 20 -A "$UA" 'http://www.bjyq.gov.cn/'

    # ④ 自签证书的丰台人大
    curl -sSk -L -m 20 -A "$UA" 'https://renda.bjft.gov.cn/'

    # ⑤ 东城人大（https 502 → http）
    curl -sSk -L -m 20 -A "$UA" 'http://www.dcrd.gov.cn/'
    ```
  - **编码判定**：先看响应头 `Content-Type`，无 charset 时再读 HTML `<meta charset=…>`；朝阳系（chynews/chyrd/bjchy）为 GBK/GB2312，一律 `iconv -f gb18030 -t utf-8` 兜底。
  - **列表页枚举**：静态 CMS 的栏目可用 `index_N.html` / `index_N.htm` 全量翻页（另见 `beijing-xxgk.md`）。
  - **站内检索**：多为 JS 异步或需签名，**不要指望直连站内搜索**；定位文章请用搜狗微信 / `web_search site:`（见各分文件与 `../engines/`）。现状明细见 `## 细节`。
- 覆盖：北京 16 个区的政府门户及其人大、政协、区委、融媒体子站（全国/区级）；区级新闻、公报、政府文件。
- 门槛：免费、免登录；**HTTPS 不通用**（朝阳、延庆只服务 http；丰台人大等自签证书）；`www.bjshy.gov.cn/robots.txt` = `User-agent: *\nDisallow: /`（顺义，使用前自行确认合规）。
- 实测：2026-10-02，macOS（arm64），curl 8.x（`-sSk -L -m 20`，桌面 Chrome UA，主机间隔 ≥0.4s，单主机 ≤3 次）。16 区门户中 14 个 HTTPS 200（通州偏慢 2.7s）；延庆 HTTPS 000、朝阳 HTTPS 000，均 http 200；子站除东城人大（HTTPS 502 / http 200）外均 200。明细见 `## 细节`；标注「历史实测 2026-09-28 / 2026-10-01」者为前序会话结论，本轮未复测。
- 上游：<https://www.beijing.gov.cn/>、北京各区区政府门户（见上）

## 细节

### 16 区门户（HTTPS 首页）

| 主机 | 区 | 首页状态 | 编码 | 现象/备注 |
|---|---|---|---|---|
| www.bjmy.gov.cn | 密云区 | ✅ 200 | utf-8 | 年报树路径见 xxgk 文件 |
| www.bjdx.gov.cn | 大兴区 | ✅ 200 | utf-8 | 站内结构见 `bjdx.gov.cn.md` |
| www.bjhr.gov.cn | 怀柔区 | ✅ 200 | utf-8 | |
| www.bjchp.gov.cn | 昌平区 | ✅ 200 | utf-8 | |
| www.bjmtg.gov.cn | 门头沟区 | ✅ 200 | 无 charset 头 | 缺省目录会 301 回首页 |
| www.bjfsh.gov.cn | 房山区 | ✅ 200 | 无 charset 头 | |
| www.bjtzh.gov.cn | 通州区 | ✅ 200（偏慢 2.7s） | 无 charset 头 | |
| www.bjpg.gov.cn | 平谷区 | ✅ 200 | 无 charset 头 | 错误页 charset=iso-8859-1 |
| www.bjyq.gov.cn | 延庆区 | ⚠️ HTTPS 000（20s 超时）/ http 200 | — | **只走 http** |
| www.bjsjs.gov.cn | 石景山区 | ✅ 200 | 无 charset 头 | |
| www.bjhd.gov.cn | 海淀区 | ✅ 200 | 无 charset 头 | |
| www.bjchy.gov.cn | 朝阳区 | ⚠️ HTTPS 000（443 握手失败）/ http 200 | — | **只走 http**，见 `bjchy.gov.cn.md` |
| www.bjft.gov.cn | 丰台区 | ✅ 200 | 无 charset 头 | |
| www.bjshy.gov.cn | 顺义区 | ✅ 200 | 无 charset 头 | **robots.txt = `Disallow: /`**，见表下注 |
| www.bjdch.gov.cn | 东城区 | ✅ 200 | utf-8 | 东城门户（勿与大兴 bjdx 混） |
| www.bjxch.gov.cn | 西城区 | ✅ 200 | UTF-8 | |

> 注：`bjdch.gov.cn` = **东城区**门户；`bjdx.gov.cn` = **大兴区**门户（易混，已更正）。

### 区人大/政协/区委/融媒体子站

| 主机 | 归属 | 状态 | 编码 | 现象/备注 |
|---|---|---|---|---|
| chynews.bjchy.gov.cn | 朝阳区融媒体（朝阳报） | ✅ 200（→ `/web/992/index.html`） | **GBK** | 新闻子频道 `/sub/newsSubMore/<id>.htm` |
| chyrd.bjchy.gov.cn | 朝阳区人大 | ✅ 200 | **gb2312** | 任免类稿件密度高 |
| hdqw.bjhd.gov.cn | 海淀区委 | ✅ 200 | utf-8 | 栏目 `/qwyw/cwhd/` 会 301，需 `-L` |
| hdrd.bjhd.gov.cn | 海淀区人大 | ✅ 200（落 `http://`） | — | |
| renda.bjft.gov.cn | 丰台区人大 | ✅ 200 | utf-8 | TLS 自签证书 → 必须 `-k` |
| renda.bjtzh.gov.cn | 通州区人大 | ✅ 200（1.7s） | utf-8 | 慧兰 CMS（`uiFramework/huilan-jquery-ui`） |
| www.dcrd.gov.cn | 东城区人大 | ❌ HTTPS 502 / ✅ http 200 | utf-8 | 证书无备用名，**走 http** |
| www.bjlgbj.gov.cn | 市委老干部局（非区属） | ✅ 200 | UTF-8 | 涉老同志/干部动态，可作旁证 |

### 站内检索（现状）

| 通道 | 状态（2026-10-02 或标注来源） | 说明 |
|---|---|---|
| `https://www.beijing.gov.cn/so/ss/query/s?qt=…&tab=all&page=1` | ❌ 200 但 `{"ok":false,"code":500,"msg":"未知异常"}` | 本次实测，两个变体均同 |
| 区级门户「政策文件检索」表单 → `http://www.beijing.gov.cn/so/s`（带隐藏 siteCode） | 历史实测 2026-09-28，壳页 200 | 需签名，勿直调 |
| `http://www.dcrd.gov.cn/htmls/jiansuo/list-1.html?tab=all&qt=<urlencoded>` | 本次实测返回正文 HTML（200） | 东城人大站内检索 |
| `http://www.bjrd.gov.cn/so/s?tab=all&siteCode=bjrd&qt=…` | 本次实测 200，仅高级检索壳页 | 其 JS 接口需服务端签名，不可直调 |
| `POST https://api.so-gov.cn/query/s`（表单） | 历史实测 2026-10-01：**本站出口 IP 已被禁用**（code -101） | 勿再扫 siteCode；若用仅低频单次 |
| `POST https://www.beijing.gov.cn/so/ss/query/s`，body `qt=<单词>&page=1&pageSize=20&ie=<uuid4>` | 历史实测 2026-10-01 可用 | `siteCode`/`sourceCode` 不生效，须按 url 域名自行过滤；仅单关键词有效 |

结论：区级门户站内检索**建议用搜狗微信 + `web_search site:` 代替**，或按已知 URL 形态小范围枚举。

### 数字报 / 融媒体（本轮探测附注）

- 北京日报数字报平台模板 `xichengdzb.bjd.com.cn/bjxc/mobile/<YYYY>/<YYYYMMDD>/<YYYYMMDD>_m.html` 存在，但 **2018 期次全 404（无 2018 存档）**。
- 昌平区报站点（`szb.bjchp.gov.cn`、`chpb.com`、`bjcpb.cn`、`cpbao.cn`、`cprmt.cn`、`cnepaper.com`、`<区名>dzb.bjd.com.cn`）探测均无有效站点；**石景山报无数字报**。
- 朝阳区融媒体 `chynews.bjchy.gov.cn`（朝阳报）是少数可直连的区级报纸源。
- 京报网/千龙网文章可直读：`https://xinwen.bjd.com.cn/content/s5c2c0e24e4b06597cc7df95a.html` ✅（历史实测 2026-10-01）。

## 坑

1. **HTTPS 不通用**：朝阳、延庆只服务 http（443 握手失败/超时）；丰台人大、延庆融媒体为自签/证书异常 → 统一 `-sSk`；东城人大 https 502 必须退回 http。
2. **编码混杂**：同一个区，门户 UTF-8、人大站 GB2312 都常见，抓前必判编码，否则标题乱码。
3. **robots**：`www.bjshy.gov.cn/robots.txt` = `User-agent: *\nDisallow: /`（本次实测 200）。历史会话在用户明确指令下 `--ignore-robots` + 加大延迟绕过；使用前请自行确认合规，莫默认爬。
4. **JS 搜索**：门户检索全为前端异步 + `api.so-gov.cn` 后端，站点级 siteCode 扫描会被封出口 IP。
5. **并发落盘**：多进程 append 同一 JSONL 会撕裂行 → 按主机分片 `pages.<host>.jsonl`（历史教训）。
