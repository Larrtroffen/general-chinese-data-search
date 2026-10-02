# regional-data-cn —— 长三角/粤港澳区域数据入口

跨省域（长三角、粤港澳大湾区）没有单一权威「区域数据库」；数据主要散在**牵头省市的统计局、区域指数发布与第三方年鉴**里。本卡收罗实测可达的入口。

- 去哪找：
  - **长三角**：上海市统计局「统计要闻/区域发展指数」`https://tjj.sh.gov.cn/tjxw/`；长三角政府数据开放一体化研究 `http://ifopendata.fudan.edu.cn/`；长三角双碳网统计年鉴库 `http://www.yrdcpcn.com/c45784/index_1.phtml`。
  - **粤港澳大湾区**：广东省统计局广东统计年鉴 `https://stats.gd.gov.cn/gdtjnj/`（上游声明，未本机请求）；广州市统计局年鉴（含「粤港澳大湾区主要经济指标」附表）`https://tjj.gz.gov.cn/`；数字广东「数据资源一网共享」`https://www.digitalgd.com.cn/`。
- 什么时候用：要**长三角/大湾区**的跨区域指标、区域发展指数、区域年鉴或数据开放评估；做区域比较研究。
- 怎么搜：先在牵头省市统计局站内找「区域/指数/年鉴」栏目；区域年鉴多为 PDF/EXCEL 附件；第三方平台（tjnjw/tjcn/nianjiandata）有整理版但需核对口径。
- 覆盖：长三角四地（沪苏浙皖）区域发展指数（上海市统计局发布，转载至国家统计局）；粤港澳大湾区主要经济指标（广州统计年鉴附表，2024 年值见 2025 卷 PDF）；区域年鉴第三方整理 2010–2023。
- 门槛：官方站免费；第三方年鉴站部分需**会员/付费**。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA：`https://tjj.sh.gov.cn/` → 200（52,059 B）；`http://www.yrdcpcn.com/c45784/index_1.phtml` → 200（51,800 B，`<title>统计年鉴`，GBK）；`https://stats.gd.gov.cn/` → 200（69,035 B）；`https://tjj.gz.gov.cn/` → 200（57,832 B）；`https://www.digitalgd.com.cn/` → 200（48,880 B，`<title>数字广东`）；`http://ifopendata.fudan.edu.cn/` → 200（240,104 B）。
- 上游：上海市统计局、广东省统计局、广州市统计局、数字广东；第三方 `yrdcpcn.com`（长三角双碳网）。

## 细节

- **粤港澳大湾区主要经济指标**示例（广州市统计局 2025 年鉴 PDF，来自搜索结果，未本机下载）：`https://tjj.gz.gov.cn/datav/admin/home/www_nj/2025/pdfs/附件5  粤港澳大湾区主要经济指标 (2024年).pdf`。
- 区域年鉴的第三方整理：`http://nianjiandata.com/books-yuegangaodawanqu-chengshiqun-nianjian.html`、`https://www.tongjinianjian.com/urban-agglomeration-in-guangdong-hongkong-macao-greater-bay-area-yearbook.html`（上游声明，付费/会员制待核）。
- 长三角区域发展指数由国家统计局口径发布、上海市统计局转载（如 `tjj.sh.gov.cn/tjxw/20251223/…`）。

## 坑

1. **无统一区域库**：长三角指数由**上海市统计局**发布（转载至国家统计局），大湾区指标主要靠**广州/广东统计年鉴**附表，别指望一个站全给。
2. `yrdcpcn.com` 是「长三角**双碳**网」，年鉴库只是其中一块，且为 GBK 编码 + 第三方内容。
3. 第三方年鉴站（tjnjw/tjcn/nianjiandata/tongjinianjian）**非官方**，部分要会员；正式引用须回官方统计年鉴核对。
4. 政府开放数据平台的区域版（如 `data.sh.gov.cn`）见 `../gov/gov_opendata.md`，本卡不重复。
