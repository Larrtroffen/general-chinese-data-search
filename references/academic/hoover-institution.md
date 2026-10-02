# hoover-institution —— 民国档案与两蒋日记馆藏

- 去哪找：
  - 馆藏总入口：`https://www.hoover.org/library-archives`
  - 数字馆藏（海报/照片/手稿/音像）：`https://digitalcollections.hoover.org/`
  - 书目检索（含 Hoover 馆藏的斯坦福联合目录）：`https://searchworks.stanford.edu/`
  - 档案查找工具（加州在线档案 OAC）：`https://oac.cdlib.org/`
  - 两蒋日记专页：`https://www.hoover.org/library-archives/collections/featured/chiang-diaries`；使用条件页：`…/featured/using-chiang-diaries`
- 什么时候用：找**民国/近代中国**一手史料——蒋介石、蒋经国日记，民国政要文书，中共党史与共产国际资料，20 世纪政治宣传画与照片，海外华人报刊；需要美国所藏中国近现代档案时。
- 怎么搜：入口站均按**浏览器**处理（本机 `curl` 不通，见坑）。
  1. 数字馆藏：`https://digitalcollections.hoover.org/`（JS 站，页内检索）。
  2. 书目：`https://searchworks.stanford.edu/?q=<词>&search_field=search`；结果页可切 JSON（`…/catalog.json?q=<词>`）。
  3. 档案：OAC 查找工具，如两蒋日记 `https://oac.cdlib.org/findaid/ark:/13030/kt438nc7np`。
- 覆盖：Hoover 图书馆与档案馆 20 世纪政治/经济/社会史料（美国保守主义、冷战、共产主义、中国革命与民国文献）；数字馆藏含海报、照片、手稿、动影像、录音，按主题（Communism 1590、Cold War 5611、Diplomacy 1020…）与格式聚合；粒度=件/册/图像。
- 门槛：网站检索免费、免登录；**两蒋日记复印件仅限馆内阅览室使用**——需提前 7 个工作日线上预约、每次限一个 folder、阅前须签协议（Hoover 不拥有版权，禁止引用/出版/广播/传播）；调阅档案走 Aeon 系统，需注册。
- 实测：2026-10-03，`curl https://www.hoover.org/library-archives` → **HTTP 000**（本机把 `www.hoover.org`/`digitalcollections.hoover.org` 解析到 `128.242.240.149`、`104.244.46.21` 等无关 IP）；同 URL 用无头 Chromium → **200**，标题「Hoover Institution Library & Archives」；`digitalcollections.hoover.org` 浏览器 → 200「Digital Collections Home」。`https://oac.cdlib.org/findaid/ark:/13030/kt438nc7np` curl → 200（42 KB HTML，Blacklight）。
- 上游：<https://www.hoover.org/library-archives>、<https://library.stanford.edu/>

## 细节

- SearchWorks 是斯坦福图书馆的 Blacklight 目录，**包含 Hoover 馆藏**；`catalog.json` 为 Blacklight 的 JSON 视图（本机需浏览器）。
- OAC（Online Archive of California）是加州各馆查找工具的聚合：`findaid` 直链本机 curl 200；但 `https://oac.cdlib.org/search?query=…` curl 返 **202 空体**，需浏览器。
- `digitalcollections.hoover.org` 与斯坦福 Digital Collections 同平台（页面标题即「Digital Collections」）；`/catalog.json` → 404（非 Blacklight 结构），检索走页内 JS。
- 两蒋日记事实（据专页/使用页，2026-10-03 浏览器读取）：原件 2005 年底由蒋家暂存 Hoover；蒋经国日记复印件 2020 年春起对全世界读者开放；两蒋日记复印件在 Hoover 阅览室开放，每卷宗夹以一个月为单位，每次阅览限一份，需提前 7 个工作日线上预约并签协议。

## 坑

1. **本机 curl 不通**：`www.hoover.org`、`digitalcollections.hoover.org` DNS 被解析到无关 IP，curl 一律 HTTP 000；`searchworks.stanford.edu` 亦 curl HTTP 000。**全部改无头 Chromium**（实测可正常访问）。
2. 两蒋日记**不能匿名下载**：仅馆内阅览 + 预约 + 协议，且不得引用/出版/传播。
3. 调阅/预约系统 `https://hoover.aeon.atlas-sys.com/aeon.dll` 本机 curl → 403 Cloudflare，需浏览器。
4. 检索与查找工具分离：书目在 SearchWorks、档案在 OAC、数字图像在 digitalcollections，三处都要查。
