# gongyishibao.com —— 公益时报网与数字报

- 去哪找：**公益时报网** `http://www.gongyishibao.com/`（注意为 **HTTP**，HTTPS 不可达）；栏目列表 `/html/<栏目>/list.html`；文章 `/html/<栏目>/<年>/<月>/<id>.html`；**数字报** `/newdzb/html/<YYYY-MM>/<DD>/node_1.htm`（周报）。
- 什么时候用：要**公益慈善行业新闻与深度报道**、政策解读、企业社会责任/ESG、社会组织、志愿服务、大额捐赠与慈善捐赠动态、研究报道；按周查阅**《公益时报》数字报**原文。
- 怎么搜：**HTML 站点**，无公开检索 API；按栏目路径遍历或用站内文章 URL 规律取详情：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
  curl -s -A "$UA" 'http://www.gongyishibao.com/'                    # 首页
  curl -s -A "$UA" 'http://www.gongyishibao.com/html/yanjiubaogao/list.html'   # 栏目列表
  curl -s -A "$UA" 'http://www.gongyishibao.com/newdzb/html/2026-09/29/node_1.htm'  # 数字报
  ```
  结果形态：**HTML（GBK/UTF-8 混合，提示乱码时先试 UTF-8 再 GBK）**；数字报为分版节点页。
- 覆盖：公益慈善行业新闻与专题，栏目含 公益资讯/公益慈善/政策解读/企业资讯/社会组织/志愿服务/研究报道/ESG/大额捐赠/人物观点/社会创新/信息发布；《公益时报》数字报为**周报**（实测 2026-08、2026-09 每周二一期）；粒度=文章/版面级。
- 门槛：**免费、免登录、无 key**；仅支持 **HTTP**（`https://www.gongyishibao.com/` 连接失败）。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA，20 s 超时）——`GET http://www.gongyishibao.com/` → **200**，48 679 B，`<title>公益时报网</title>`，页内 21 个栏目 `/html/*/list.html` 与数字报链接（最新 `/newdzb/html/2026-09/29/node_1.htm`）；`GET https://www.gongyishibao.com/` → **000**（TLS/连接失败）。
- 上游：公益时报网 `http://www.gongyishibao.com/`；数字报 `http://www.gongyishibao.com/newdzb/`。

## 细节

- 栏目路径（实测）：`yaowen`（要闻）、`gongyizixun`、`cishanjuanzeng`、`daejuanzeng`、`qiyezixun`、`shehuizuzhi`、`zyfw`（志愿服务）、`yanjiubaogao`（研究报道）、`zhengcejiedu`、`ESG`、`redian`、`renwuguandian`、`shehuichuangxin`、`xinxifabu`、`shzl`、`dangjian`。
- 数字报历史：`/newdzb/html/<年>-<月>/<日>/node_1.htm`；旧数字报另有 `/dianzibao/` 入口。

## 坑

1. **仅 HTTP**：该站无有效 HTTPS，脚本里用 `https://` 会直接失败，务必写 `http://`。
2. **无检索接口**：只能按栏目列表页/URL 规律抓，站内无关键词 API；跨年回溯靠数字报日期目录。
3. 媒体内容**二次转载多、原文口径以官方为准**；引用数据请回民政部/基金会中心网等一手源。
