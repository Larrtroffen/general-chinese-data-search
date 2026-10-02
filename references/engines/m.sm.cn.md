# m.sm.cn —— 神马移动综搜（可翻页）

阿里/UC 的神马搜索。移动版 `m.sm.cn` 直出 HTML、含真实条目、可翻页；但夸克入口 `quark.sm.cn` 有反爬 punish 页。

- 去哪找：`https://m.sm.cn/s?q={q}`（别名 `https://so.m.sm.cn/s?q={q}`）
- 什么时候用：移动综搜召回、需要翻页的补充通道；要结构化卡片（`qk-card`）的信息流
- 怎么搜：`curl -s -m 20 -A "$MUA" "https://m.sm.cn/s?q=$Q&page=1"`。参数 `q` 关键词、`page` 页码（1、2、3…，实测生效）。结果形态：直出 HTML（SSR）
- 覆盖：移动综搜（网页/资讯条目）；无时间过滤参数（用「年份词」放量）
- 门槛：无（未带 cookie 即拿到结果；连发时用 cookie jar 更稳）
- 实测：2026-10-02，macOS + curl（iPhone UA）——移动检索/别名域/翻页均 200，夸克入口跳 punish；完整记录见下
- 上游：站点自身入口（无 repo/Skill 出处）

## 细节

### 可用性矩阵（本机实测 2026-10-02，iPhone UA）

| 通道 | URL | 状态 | 现象 |
|---|---|---|---|
| 移动检索 | `https://m.sm.cn/s?q={q}` | ✅ | 200，457053 B，`text/html;charset=utf-8`；`{q}` 出现 139 次；命中真实文章 `https://news.sina.cn/2018-05-07/detail-ihacuuvu2613816.d.html` |
| 别名域 | `https://so.m.sm.cn/s?q={q}` | ✅ | 200，457205 B，与 `m.sm.cn` 同内容 |
| 翻页 | `https://m.sm.cn/s?q={q}&page=2` | ✅ | 200，386189 B；页面元数据 `"pg":2`；外链与首页低重叠（overlap 2） |
| 夸克入口 | `https://quark.sm.cn/s?q={q}` | ❌ | 200，1090 B，反爬页：`window.location.replace("https://quark.sm.cn//s/_____tmd_____/punish?x5secdata=…")` |

### 请求模板

```bash
MUA='Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
Q='%E8%A1%97%E4%B9%A1%E5%90%B9%E5%93%A8'   # 街乡吹哨
curl -s -m 20 -A "$MUA" "https://m.sm.cn/s?q=$Q&page=1"
```

### 解析要点

- **直出 HTML**（SSR），无需 JS。
- 结果卡片：`div.qk-card`（`data-tpl="structure_template_normal"`）；标题/链接 `a.qk-link-wrapper[href]`，标题文本在 `.qk-title`（含 `qk-title-content`）。
- 元数据在属性里：`data-sc` JSON 含 `q`(查询词) / `pg`(页码) / `pos`(位次) / `hid`；`data-reco` JSON 含 `article_title` / `host_name`（来源）/ `norm_url`（归一化原始 URL）。
- 落地 `href` 常是**移动归一化 URL**（如 `news.sina.cn/.../detail-xxx.d.html`），原始 URL 见 `data-reco.norm_url`；做去重时以归一化域名为准。

### 实测记录（2026-10-02）

macOS + curl（iPhone UA）：

- `m.sm.cn/s?q=街乡吹哨` → 200，457053 B，`text/html;charset=utf-8`；命中 `news.sina.cn/2018-05-07/…`。
- `so.m.sm.cn/s?q=街乡吹哨` → 200，457205 B（同内容）。
- `m.sm.cn/s?q=街乡吹哨&page=2` → 200，386189 B，`"pg":2`。
- `quark.sm.cn/s?q=街乡吹哨` → 200，1090 B，`/s/_____tmd_____/punish` 跳转。

## 坑

- `quark.sm.cn` 会跳到 `punish` 反爬页，**别用它**；只用 `m.sm.cn` / `so.m.sm.cn`。
- 结果项里混有广告，`href` 为 `so.m.sm.cn/adclick?…` 或 `b.dailyact.cn/apps/…` 跳转，需按域名过滤。
- 长结果页含大段内联 CSS/JS（400+ KB），解析时只扫 `div.qk-card` 区域。
- 无时间过滤参数，时间范围同样用「年份词」放量。
