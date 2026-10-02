# weixin.sogou.com —— 公众号文章关键词检索

唯一能稳定程序化检索微信公众号文章的通道是 **wap 版**；桌面版、时间过滤、账号页全部被反爬封死。以下全部经本机实测。

- 去哪找：
  - 检索页 `https://weixin.sogou.com/weixinwap?type=2&ie=utf8&query=…`（wap 版，**必须 iPhone UA**）；
  - 文章链接解析 `https://weixin.sogou.com/link?url=…`（仅限「会话预热 + 现取现解析」）。
- 什么时候用：按**关键词/单位/年份词**批量搜公众号文章（如「双井街道 吹哨报到 2018年」）；要唯一的关键词召回通道时。
- 怎么搜：
  ```bash
  UA='Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
  curl -s -m 30 -A "$UA" -b jar.txt -c jar.txt \
    'https://weixin.sogou.com/weixinwap?type=2&ie=utf8&query='$(python3 -c 'import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))' "双井街道 吹哨报到")
  ```
  用 `-b/-c` 维护 cookie jar；每次任务开始先访问一次任意搜索页「预热」（否则首次 `/link` 易被反爬）。`query` 用 URL 编码；空格可用 `%20` 或 `+`。结果形态：**HTML（需解析）**。
- 覆盖：wap 版关键词检索；每页 10 条、翻页上限 10 页（即 ≤100 条/检索式，结果页内嵌 JS `totalPages=10`）；**无时间过滤**（用年份词放量）；只是索引子集，不保证某号全量。
- 门槛：无（需 iPhone UA + cookie jar；高频触发搜狗反爬/验证码）
- 实测：2026-10-02 本机实测——单请求 0.4–0.7s，0.6–1.8s 随机间隔、3–4 进程并发下上千次请求 0 次被反爬；批量链接解析最终 **847/849 ≈ 99.8%** 成功；翻页上限有硬证据 `totalPages=10`。
- 上游：https://weixin.sogou.com/

## 细节

### 可用/不可用矩阵

| 端点 | 状态 |
|---|---|
| `https://weixin.sogou.com/weixinwap?type=2&ie=utf8&query=…` | ✅ 可用（必须 iPhone UA） |
| 同上 + `&page=N`（N=2..10） | ✅ 可用（每页 10 条，上限 10 页） |
| 同上 + `&tsn=1/4/5/0`、`&ft=`、`&et=` | ❌ 302 → 首页（时间过滤被封死） |
| `https://weixin.sogou.com/weixin?type=2&query=…`（桌面） | ❌ 302 → antispider 验证码 |
| `https://weixin.sogou.com/link?url=…` | ✅ 仅限「会话预热 + 现取现解析」（见下） |
| `https://weixin.sogou.com/gzh?openid=…`（公众号主页） | ❌ 404（页面已下线） |
| `https://weixin.sogou.com/gzhjs?openid=…&page=…&t=…` | ❌ 302 → antispider（账号文章列表接口不可用） |
| 裸 curl（无 UA / 桌面 UA） | ❌ 302 |

### 结果页解析（字段定位）

每个结果项 `<li id="sogou_vr_数字_box_序号" d="docid">`：

| 字段 | 定位 |
|---|---|
| 标题 | `<h4><a href="/link?url=…"><div>标题(含 <em> 高亮)</div></a></h4>` |
| 跳转链接 | 同上 `href`（形如 `/link?url=dn9a_…&type=2&query=…&token=…`） |
| 公众号 | `<span class="s2" data-openid="oIWsFt…" data-sourcename="公众号名">` |
| 发布日 | `<span class="s3" data-lastModified="unix秒">` → `datetime.fromtimestamp` |
| 摘要 | `<p data-type="article_summary">`（约 100–150 字） |
| 无结果页 | `<div class="img-err"><p>抱歉，没有找到相关的微信文章。</p>` |

解析注意：页面头部 JS 模板里会出现 `${openid}` 这类占位符——openid 必须匹配 `^o[A-Za-z0-9_\-]{10,}` 才是真实值。

### 文章链接解析（/link 现取现解析）

`/link` 里的 token 与搜索会话绑定且**时效极短（分钟级）**，旧结果文件里的 token 全部失效（直接触发反爬）。必须：抓搜索页 → 立即对其中条目调 `/link`。

```bash
# 1) 先抓搜索页（预热 + 拿新 token）
REF='https://weixin.sogou.com/weixinwap?type=2&ie=utf8&query=<urlencoded query>'
curl -s -A "$UA" -b jar.txt -c jar.txt "$REF"

# 2) 立即解析该页某条结果的 href
curl -s -A "$UA" -b jar.txt -c jar.txt -H "Referer: $REF" \
  'https://weixin.sogou.com'$(python3 -c 'import sys,html;print(html.unescape(sys.argv[1]).replace(" ","%20"))' "/link?url=…&type=2&query=…&token=…")
```

返回 200 的 HTML 里是逐段拼接的 JS：

```html
<script>
(new Image()).src = '…/approve?uuid=…&token=…&from=inner';
setTimeout(function () {
    var url = '';
    url += 'https://mp.';
    url += 'weixin.qq.c';
    url += 'om/s?src=11';
    url += '&timestamp=';
    url += '1790866122&';
    url += 'ver=7000&si';
    url += 'gnature=xHk';
    url += 'PwVSXwyEdTg…';
    url += '&new=1';
    url.replace("@", "");
    window.location.replace(url)
},100);
</script>
```

用正则 `url \+= '([^']*)';` 取出全部片段按顺序拼接，得到最终链接：`https://mp.weixin.qq.com/s?src=11&timestamp=…&ver=7000&signature=…&new=1`（**搜狗签名链接，有时效**）。

**成功公式（实测 99.8% 的批量成功率）**：

1. **预热**：先访问一次任意 wap 搜索页（拿新 session token）；
2. **带 Referer**：解析 `/link` 时 `Referer: <刚才那一页的搜索 URL>`；
3. **现取现解析**：搜索结果页抓到后**立刻**逐条解析，token 只有分钟级寿命（旧 token 直接触发反爬）。

失败模式对照（历史实测）：无 jar / 无 Referer / Referer 用 `https://www.sogou.com/` → 全部 302 antispider；一次 `curl rc=3` 是 href 里 `&amp;` 未反转义所致（记得 `html.unescape`）。

批量成功率脉络：首轮 `ok=1040 fail=174` → 等待+重试 `ok=161 fail=13` → 剩余按「标题前 24/16 字重搜」5 成功 4 失败 → 最终 **847/849 ≈ 99.8%**。
`/link` 返回 200 时响应会顺带下发 `Set-Cookie: black_passportid=1`（正常风控标记）；签名链接响应头 `expires` 显示**签发后约 8 分钟**过期。

**兜底重解析（索引漂移）**：页面里找不到该条目（标题换了页）→ 原检索式跨页 1–3 重查 → 仍无则用「标题前 30 字」当检索词搜 1–2 页 → 匹配用**标题前 12–14 字前缀**（不做全等）。`antispider` 时等 30s + 重置 jar + 重抓当前页再解析。

> 工具：本 skill `scripts/sogou_wechat.py`（search 子命令内置现取现解析；resolve 子命令做上述兜底重解析；`--shard i/n` 分片、逐检索式断点续跑）。

### 放量技巧（没有时间过滤时的替代）

1. **年份词**：`{单位} 2018年`（"年"字很重要；`2018` 与 `2018年` 结果不同）。能把 2018 年发布文章顶到前列（2018 文章正文常含"2018年"）。
2. **主题词**：`{单位} {主题词}`（双报到/疏解整治促提升/环境整治/综合执法/拆违/背街小巷/安全生产/防汛/垃圾分类/老旧小区/社区治理/志愿服务）。每个检索式约 50–60 条去重结果，2018 占比 5–15%。
3. **账号名当检索词**：`{公众号名} 2018年`（如 `北京延庆 2018年` → 65 条去重、18 条 2018）。
4. **翻页到底**：每查询翻 1–10 页，空页或整页重复即停（不要用"条数<8 就停"这种提前中断）。
5. 多词 AND 过严：`双井街道 2018 双报到` 这类 3 token 组合常为 0 条，优先两词组合。

### 实测吞吐与规模

- 单请求 0.4–0.7s；带 0.6–1.8s 随机间隔、3–4 进程并发，无反爬。
- 主题词式检索式每个约 10–15s（含 6 页翻页 + 若干链接解析）。
- 每 500 个检索式约 1 小时/分片；任务超 1 小时会被杀，务必断点续跑（`query_done` 标记 + 跳过已完成的查询）。
- 分片吞吐参考：市级 90 查询 ≈ 312s（≈3.5s/查询）；一轮 345 查询/分片 ≈ 934s（≈2.7s/查询，3365 条结果、949 条 2018、949 条链接全成功）。
- 放量规模经验：单波 1000–2000 条检索式较好；曾一次性造 4980 条的主题词波次（333 单位 × 15 主题词），**因量级过大被弃用**后重建为 921 条/1992 条分波推进。主题词取 6 个左右（双报到/疏解整治促提升/环境整治/综合执法/拆违/背街小巷）即可覆盖多数年份文。

## 坑

- 触发特征：302 到 `weixin.sogou.com/`（Set-Cookie `black_passportid=1`）、或 302 到 `/antispider/?antip=wx_sh2&from=…`。
- 处置：等待 45–90s → 删除 cookie jar → 重新预热 → 重试（最多 3 次）。实测按 0.6–1.8s 随机间隔串行请求、3–4 个进程并发时，上千次请求 0 次被反爬。
- **判定要准**（两个已知误判/误区）：
  - 空结果页 `<div class="img-err"><p>抱歉，没有找到相关的微信文章。</p>` 是**合法结果**，不是封禁，应作为「翻到底」的停止条件；
  - 只看 body 正则会双计：有实测样本 `HTTP 200 且 items=12 却被旧判定函数标 blocked=True`。可靠判定 = 响应前 1.5KB 出现 `antispider`，或既无 `sogou_vr_` 也无「没有找到相关的微信文章」。
- 唯一实测封禁样本：一次**超长标题式检索式**（把整句 40+ 字标题当 query）连试 3 次（45/75/105s 退避）均失败 → 检索式要短（单位+年份词/主题词），长标题先截断再搜。
- 分片每进程独立 jar（如 `sogou_jar2018_{shard}.txt`）；3–4 分片数千请求封禁计数 0（0.6–1.2s/请求；另有脚本用 2.2–3.8s 更保守）。
- 出现 302+antispider 后**同一时刻**再发查询会连续失败（封禁窗口内批量查询 items=0）；退避等待必须真正等待，不能连着换查询硬试。
- `read` 工具直取桌面 URL 会落到 antispider 页（trafilatura 解析，IP/时间戳在页内）；`read` 对桌面版有时只拿到外壳（无结果项）。搜狗通道一律用 **curl + iPhone UA**。
- 浏览器（Chromium）访问搜索页同样落到 antispider 字符点选验证码（"请依次点击【俗,坏,轨,污】"），不可自动化。
