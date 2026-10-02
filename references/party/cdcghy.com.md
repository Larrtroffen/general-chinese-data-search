# cdcghy.com —— 顺义组工镜像站

- 去哪找：首页 `https://cdcghy.com/`（栏目列表：大党建/组织工作/基层动态…）；文章页模板 `https://cdcghy.com/html/webstaticarticlescatalog_<32位hex>article_<32位hex>.html`。
- 什么时候用：要「顺义组工」区级组工号的 2018 年原发文章（原站 `顺义组工.政务.cn` 外部难访问，镜像站是主要通道）。
- 怎么搜：**无站内搜索**，两种定位——
  1. 首页栏目逐栏浏览；
  2. 用搜狗微信搜「顺义组工」拿标题，再到本站/搜狗镜像页找原文。
- 覆盖：顺义区委组织部网站镜像，2018 年稿仍在。
- 门槛：免费，curl 直读。
- 实测：原卡未记录日期（本机 curl）；`curl` 直读可取全文（见下命令）。
- 上游：顺义区委组织部（原站 `顺义组工.政务.cn`）。

## 细节

```bash
curl -s -m 25 'https://cdcghy.com/html/….html'
```

示例（2018-03-23 全市试点街乡专题培训班）：

```
https://cdcghy.com/html/webstaticarticlescatalog_ff80808160b9f2050160c43fbe840015article_ff80818162463ca80162b29404db067fff80818162463ca80162b29404db067f.html
```

- 页面静态 HTML，正文含全文与配图；抓取时注意页面标题为"顺义组工"（镜像壳）。
