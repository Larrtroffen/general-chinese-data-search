# freedomhouse.org —— 自由之家自由度评级

- 去哪找：门户 `https://freedomhouse.org/`；Freedom in the World `https://freedomhouse.org/report/freedom-world`；交互评分 `https://freedomhouse.org/countries/freedom-world/scores`。
- 什么时候用：要 **FIW**（政治权利 PR 1–7、公民自由 CL 1–7、总分 0–100、Status=F/ PF/ NF）以及 Freedom on the Net（FOTN）、Nations in Transit（NIT）；做媒体/政策叙事、或与 V-Dem/Polity 交叉验证。
- 怎么取：报告页下载 `Country and Territory Ratings and Statuses` 的 xlsx/CSV（历年存在 `/sites/default/files/{年-月}/` 下）；FOTN/NIT 各有独立页与数据表。
- 覆盖：FIW 1973–至今，195+ 国家/地区，年度（每年 2–3 月发新版）；FOTN 2011 起；NIT 1995 起（后社会主义国家）；以上为上游声明，未本机实测。
- 门槛：免费、无注册。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA，20 s 超时）：`https://freedomhouse.org/report/freedom-world` → **连接超时**；`https://freedomhouse.org/` → **连接超时**（两次尝试，非 403/验证码）。本机网络（中国）**不可达**，**未取到任何内容**。
- 上游：`https://freedomhouse.org/`。

## 细节

### 本机不可达时的替代取数

| 途径 | 说明 |
|---|---|
| QoG 标准数据集 | 含 `fh_cl`（公民自由）、`fh_pr`（政治权利）、`fh_status`、`fh_rol`、`fh_aor` 等 FH 派生列 → `qogdata.pol.gu.se.md` |
| Our World in Data | 有基于 FH 的图表 CSV（政治权利/公民自由得分）→ `ourworldindata.org.md` |
| V-Dem | 制度连续量替代（`v2x_*`），覆盖面更长 → `v-dem.net.md` |
| 换网络/代理 | 直连官网下官方 xlsx（本机未验证） |

## 坑

1. 本机对 `freedomhouse.org` **连接超时**（首页也超时），不是 403/JS 挑战；如实记录，"不可达"仅指本机当前网络，勿断言站点下线。
2. FIW 评分口径 2006/2017 两次改版（2017 起改 0–100 分制），跨年比较必须按版本对齐。
3. 报告年份 ≠ 数据覆盖年份（报告年通常晚 1 年），引用要写清。
4. 二次转引（QoG/OWID）可能滞后一版；关键论断建议核官方原表。
