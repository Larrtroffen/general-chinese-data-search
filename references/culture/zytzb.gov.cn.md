# zytzb.gov.cn —— 统战部宗教工作与政策

- 去哪找：**中共中央统一战线工作部网站**`https://www.zytzb.gov.cn/`；站内搜索跳转 `https://zytzb.chinanews.com/search?q=<关键词>`（中新网托管）。
- 什么时候用：要**宗教工作、宗教中国化、宗教政策法规、宗教团体管理**的中央口径原文（国家宗教事务局政务职能自 2018 年起并入中央统战部）；要民族宗教领域统一战线的政策解读；作为 `sara.gov.cn.md` 的政策侧补充。
- 怎么搜：站内搜索**外包给中新网**，URL 模板：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
  curl -sS -A "$UA" --compressed 'https://zytzb.chinanews.com/search?q=%E5%AE%97%E6%95%99'
  # → 200 HTML，正文「共为您找到约1704篇相关的网页」
  ```
  结果形态：**HTML**（标题 + 摘要 + 发布日期，含分页）；官网首页为静态栏目页。
- 覆盖：中央统战部及宗教工作口径的要闻、政策、理论文章；检索覆盖站内（含历史稿件）。更新按日发稿。
- 门槛：**免费、免登录、无 key**。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA + Chromium 无头——`GET https://www.zytzb.gov.cn/` → **200**（18 KB，`<title>中共中央统一战线工作部网站</title>`）；Chromium 打开 `/zytzb/search.html?keyword=宗教` → 跳转 `https://zytzb.chinanews.com/search`；`GET https://zytzb.chinanews.com/search?q=宗教` → **200**，「共为您找到约1704篇相关的网页」；`?keyword=`/`?words=` 参数被忽略（恒显示约10000篇）——**正确参数是 `q`**。
- 上游：<https://www.zytzb.gov.cn/>（中共中央统一战线工作部）；检索 <https://zytzb.chinanews.com/search>。

## 细节

- 官网栏目含要闻、多党合作、民族工作、宗教工作、非公经济、党外知识分子、新的社会阶层、港澳台海外等；宗教政策原文多在此发布。
- 搜索为中新网 `zytzb.chinanews.com` 子域，参数 `q`；结果页为 HTML，无 JSON 端点。
- 与国家宗教事务局 `sara.gov.cn` 为**同领域两站点**：政策口径以统战部为主，宗教基础信息（场所/院校/教职人员）以 `sara.gov.cn.md` 为准。

## 坑

1. 搜索参数只认 **`q`**：`keyword`/`words` 会被忽略并返回约 10000 篇的泛结果，易误判为「命中很多」。
2. 搜索域是 **chinanews.com** 子域（异地托管），直连 `www.zytzb.gov.cn/zytzb/search.html` 会 302 过去，需跟随重定向。
3. 与 `sara.gov.cn`、`neac.gov.cn` 内容可能重复转载，引用以首发方为准。
4. 版权归中央统战部/中新网，勿批量再分发正文。
