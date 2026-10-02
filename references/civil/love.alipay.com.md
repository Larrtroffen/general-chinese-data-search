# love.alipay.com —— 支付宝公益平台项目页

- 去哪找：**支付宝公益平台** `https://love.alipay.com/donate/index.htm`（公益项目聚合页）；**项目详情** `https://love.alipay.com/donate/itemDetail.htm?name=<项目号>`。
- 什么时候用：要**支付宝公益平台在筹项目**（项目名称、发起机构、筹款目标/进度、捐赠记录）、按项目号取单个项目详情；做互联网公益募捐项目监测与横向对比（与 `gongyi.qq.com.md` 互为补充）。
- 怎么搜：**公开 HTML 页**（免登录），无独立 JSON 检索接口挖到；项目号来自列表页内嵌的 `itemDetail.htm?name=` 链接：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
  # 列表（内含若干 itemDetail.htm?name=… 链接）
  curl -s -A "$UA" 'https://love.alipay.com/donate/index.htm' | iconv -f GBK -t UTF-8 | \
    grep -oE 'itemDetail\.htm\?name=[0-9]+' | sort -u
  # 详情
  curl -s -A "$UA" 'https://love.alipay.com/donate/itemDetail.htm?name=2020111121175295224' | iconv -f GBK -t UTF-8
  ```
  结果形态：**HTML（GBK 编码，须转码）**，页面数据部分由 SeaJS/JS 渲染；标题「支付宝公益平台」。
- 覆盖：支付宝公益平台公开项目（列表页实测内嵌约 18 个 `itemDetail` 项目链接）；项目号形如 `2020111121175295224`（时间戳式 19 位）；粒度=单项目；随平台上线/结项动态变化。
- 门槛：**免费、免登录**（公开项目页）；注意 **GBK 编码**；无 API key。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA，20 s 超时）——`GET https://love.alipay.com/donate/index.htm` → **200**，128 785 B，`Content-Type: text/html; charset=iso-8859-1`（实为 GBK），`iconv -f GBK` 得 `<title>支付宝公益平台…</title>`，页内匹配到 **18** 条 `itemDetail.htm?name=` 链接；`GET …/donate/itemDetail.htm?name=2020111121175295224` → **200**，163 064 B，同为 GBK。
- 上游：支付宝公益平台 `https://love.alipay.com/donate/index.htm`；`https://love.alipay.com/donate/i.htm`（列表页变体）。

## 细节

- 页面通过 `a.alipayobjects.com/charityprod/charityprod.donate-1.5.js` 等 SeaJS 模块加载交互；`love.alipay.com/donate/isgray.vm` 为灰度开关模板。
- 项目号可见样例：`2016011417510049824`、`2017082515405734449`、`2019030418400671389`、`2020091614513349829`、`2020111121175295224`。

## 坑

1. **GBK 编码**：响应头写 `charset=iso-8859-1`，实际 GBK，直接抓会乱码，务必 `iconv -f GBK -t UTF-8`。
2. **无公开检索 API**：本次未挖到匿名 JSON 检索接口，只能「列表页找项目号 → 详情页」；老 `gy.alipay.com`（`HTTP 000`）不可用。
3. 列表页链接数随页面区块加载变化，未必等于全量在筹项目；需多渠道补全。
