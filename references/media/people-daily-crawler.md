# people-daily-crawler —— 人民日报电子版/老资料网取数

一个长期维护的人民日报爬虫仓库（作者 2025-01 更新过），提供**两套取数路径的 URL 形态**：①人民日报官方电子版 `paper.people.com.cn`（近年，免费）；②老资料网 `laoziliao.net`（1946–2003 旧报）。作者已把此前公开的全量数据撤下（侵权风险），仓库只留爬虫代码，但 **URL 规律本身很有用**——可直接照抄形态、不必用它的脚本。

- 去哪找：repo <https://github.com/caspiankexin/people-daily-crawler-date>；电子版入口 `http://paper.people.com.cn/rmrb/pc/layout/index.html`（人民网 › 人民日报 › 电子版）；老资料网 <https://www.laoziliao.net/rmrb/>；同作者词频工具 MiYing <https://github.com/caspiankexin/MiYing>
- 什么时候用：要人民日报**历年原文/版面**，尤其 2021 年之前、人民网站内检索（约 2021 起）覆盖不到的旧稿；要人民日报数字报的**版面级**抓取路径；或要研究"电子版 vs 老资料网"两段式取数。
- 怎么取：URL 模板来自其脚本 `人民网人民日报爬虫（第3版）.py` / `老资料网人民日报爬虫.py`。
  - 版面列表（当日某版）`http://paper.people.com.cn/rmrb/pc/layout/YYYYMM/DD/node_NN.html`
  - 正文（某篇）`http://paper.people.com.cn/rmrb/pc/content/YYYYMM/DD/content_<id>.html`
  - 旧报（老资料网，按日）`https://www.laoziliao.net/rmrb/YYYY-MM-DD`
  - 最小复现（本机已验证形态）：

    ```bash
    curl -s 'http://paper.people.com.cn/rmrb/pc/layout/202610/02/node_01.html' | grep -oE 'content_[0-9]+\.html'
    curl -s 'http://paper.people.com.cn/rmrb/pc/content/202610/02/content_30184111.html'
    ```

  - 不想自己解析 → 用 RSSHub `/people/paper`（见 `rsshub.md`），返回当日全部文章 30 条，含标题+正文链接。
  - 三个脚本对应时段：`（第3版）`＝2024-12 至今；`（第2版）`＝2021–2024/11；`老资料网…`＝1946–2003。
- 覆盖：电子版免费看**近年**（更早需官方内部账号）；老资料网覆盖 **1946–2003**；两段拼起来才接近"1946 至今"。
- 门槛：电子版近年免费；更早需官方内部账号；老资料网本机不可达（可能需代理/浏览器）。
- 实测：2026-10-03，macOS + curl，桌面 UA：
  - `paper.people.com.cn/rmrb/pc/layout/202610/02/node_01.html` → **200 / 23,637B**
  - `paper.people.com.cn/rmrb/pc/content/202610/02/content_30184111.html` → **200 / 42,172B**（正文可取）
  - `https://www.laoziliao.net/rmrb/2003-12-31` → **25s 超时 / HTTP 000**（本机不可达，未验证）
- 上游：<https://github.com/caspiankexin/people-daily-crawler-date>（无 LICENSE；仅记 URL 形态与用法）

## 坑

- 仓库**无 LICENSE**；作者明确因**侵权风险**不再公开数据——我们只记 URL 形态与入口，不搬数据、不复制代码。
- 旧资料网本机不可达（见实测），可能需代理/浏览器环境，或该站已反爬。
- 电子版 URL 含日期与稿号，稿号连续但≠版面顺序，须从版面页解析出链接列表后再逐篇取。
- 数字报原版（版面图）另见本层 `epaper/`。
