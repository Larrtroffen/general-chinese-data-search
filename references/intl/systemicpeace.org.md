# systemicpeace.org —— Polity5 政体数据

- 去哪找：数据页 `https://www.systemicpeace.org/inscrdata.html`（title "INSCR Data Page"）；文件目录 `http://www.systemicpeace.org/inscr/`（**仅 HTTP**）。
- 什么时候用：要经典 `polity2`（-10…+10 政体分值）、政体类型（民主/专制/过渡）、政体变迁与断裂年份；做与 V-Dem 对照的制度变量；沿用"政体 × 冲突"老派量化框架。
- 怎么取：
  ```bash
  # 年表：SPSS / Excel（1=年表 2018 终版；ch=政体变迁）
  curl -sLO 'http://www.systemicpeace.org/inscr/p5v2018.sav'
  curl -sLO 'http://www.systemicpeace.org/inscr/p5ch2018.xls'
  curl -sLO 'http://www.systemicpeace.org/inscr/p5manualv2018.pdf'
  ```
  - 同页配套数据集：CSP 政变年表（`CSPCoupsAnnualv2021.xls`）、PITF 国家失败/种族战争/革命战争/种族灭绝、MEPV、SFI 等，均为 `/inscr/{名}.sav|xls`。
- 覆盖：**1800–2018**（Polity5 终版 v2018，项目 2018 年后停更）；~167 个政体；年度。
- 门槛：免费、**无注册、无 key**。
- 实测：2026-10-03，macOS arm64，curl 8.x：`https://www.systemicpeace.org/inscrdata.html` → 200 / 41 KB；页内链接实测指向 `http://www.systemicpeace.org/inscr/p5v2018.sav`、`p5ch2018.xls`、`p5manualv2018.pdf`、`CSPCoupsAnnualv2021.xls` 等（**仅验证页面与链接存在，未下文件本体**）。
- 上游：Center for Systemic Peace / INSCR。

## 坑

1. **Polity5 已停更**（终版覆盖到 2018）；2019 年后的政体分值要另找（V-Dem、Freedom House、EIU）。
2. 链接是 **http 不是 https**；脚本用 https 会连不上。
3. Polity 对"过渡期/无政府/占领"有特殊码（`-66`/`-77`/`-88`），**不能直接当连续变量**，先读手册。
4. `.sav` 是 SPSS 格式（Python 用 `pyreadstat`）；`.xls` 是老 Excel 格式（`pandas` 需 `xlrd`）。
5. 站点老旧、无频控提示，但请节制并发。
