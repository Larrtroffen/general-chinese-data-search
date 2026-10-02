# osint-china —— 英文 OSINT 方法的中文迁移

- 去哪找：`UseOSINT/Skills` 仓库（只读下载：`gh api repos/UseOSINT/Skills/tarball | tar xz -C /tmp/osint`）—— 29 个 skill（各 `skills/<名>/SKILL.md`）+ 51 个 reference（`skills/<名>/reference/*.md`）。
- 什么时候用：想借鉴英文 OSINT 工作流的**通用方法**（检索操作符保真度、档案 CDX、身份分级、平台 ID 机制、图像地理定位）；注意**该库无中国专章**，中国源仍走本库 `gov/`、`stats/`、`legal/`。
- 怎么取：`gh api repos/UseOSINT/Skills/tarball | tar xz -C /tmp/osint`；按「我们能吸收的 5 个方法」（见「细节」）提炼，**只吸收方法 + 它提到的源，不复制其正文/代码**。
- 覆盖：29 个 skill + 51 个 reference（共 85 个 md）；中国相关条目稀少（登记处目录中国仅 1 行、人物源目录无中国）。
- 门槛：上游 **MIT**（`Copyright (c) 2026 osint-skills contributors`），可自由用；下载需 `gh`；本卡未安装其依赖、未运行其代码。
- 实测：2026-10-03，macOS（arm64），`gh api repos/UseOSINT/Skills/tarball` → 301731 B tarball，解包 `UseOSINT-Skills-06243a5`；29 个 `SKILL.md`、51 个 `reference/*.md`、总 md 85。
- 上游：https://github.com/UseOSINT/Skills（MIT；实际下载 commit `06243a5`）。

## 细节

### 来源与许可（实测）

- 仓库：`UseOSINT/Skills`；本机用 `gh api repos/UseOSINT/Skills/tarball | tar xz -C /tmp/osint` 只读下载，落地 `UseOSINT-Skills-06243a5`。
- 规模：**29 个 skill**（各 `skills/<名>/SKILL.md`）+ **51 个 reference**（`skills/<名>/reference/*.md`），共 85 个 md。
- 许可：**MIT**（`LICENSE`，`Copyright (c) 2026 osint-skills contributors`）。
- 版本/出处不一致（照实记）：`.claude-plugin/plugin.json` 写 `repository: github.com/useosint/osint-skills`、`homepage: docs.useosint.com`，但实际下载的是 `UseOSINT/Skills`——**名字大小写/仓库名不一致**。
- **不直接引用其代码**：本卡只吸收方法，源站列表另行核对后再进对应层的源卡。

### 精选清单（skill → 一句话方法 → 其中提到的源）

| skill | 方法（一句话） | 提到的源 / 与中文的接口 |
|---|---|---|
| `google-like-a-spy` | 多引擎操作符与查询改写规避；`site:` 枚举用必应、Verbatim 才可信 | Google/Bing/DDG/Yandex/Startpage/Mojeek/Marginalia/Brave；`engine-operators.md` 是全网最细的操作符对照表 |
| `read-deleted-pages` | 用档案**反向枚举**旧 URL：CDX `collapse=digest` 看内容何时变、`matchType=domain` 翻旧子域 | Wayback CDX、archive.today、Common Crawl、Memento；**方法与我们 `historical-web.md` 直接互补** |
| `find-anyone` | 先给「要证明的结论」再选源；source grading：primary/secondary/self-asserted/derived | 民事登记、讣告、职业执照、专利、公司注册、法院/物业卷宗 —— 中国项未列（**缺口**） |
| `who-really-owns-it` | 企业→法代/股东/UBO 的登记处目录 | **China：国家企业信用信息公示系统（+商业转售商），免费基础、中文；字号匹配必须用中文，罗马字不解析** |
| `x-ray-a-company` | 品牌/网站 → 注册主体 → 集团/受益所有人 → 官员/董事 → 数字资产 → 诉讼/制裁筛查 | OpenCorporates、Companies House、SEC EDGAR 等（无中国登记处） |
| `hunt-a-handle` | 用户名跨平台枚举（sherlock/maigret/WhatsMyName）+ 变体表（`_92`=年份后缀、leet 替换表） | `platform-leakage.md`：**snowflake 型 ID 直接嵌注册时间**；句柄可变、数字 ID 不变 |
| `pattern-of-life-from-socials` | 按**平台族**（微博类/短视频/专业网络/匿名论坛/IM）取元数据、网络、发帖时段 | Instagram/FB/X/TikTok/LinkedIn/Reddit/Telegram/Discord —— 换名即适用微博/知乎/贴吧 |
| `find-the-original-image` | 反向图搜矩阵：**中文/中国内容 → 百度图搜 `image.baidu.com`**（其他引擎覆盖不到） | Yandex（中/俄/土内容强）、Google Lens、TinEye（按最旧排序）、Bing Visual、**Baidu** |
| `geolocate-from-pixels` | 纯视觉定位/定时：车牌、插座、路面、标线、太阳能热水器 + SunCalc | `regional-indicators.md` 含**中国专属条目**（见下）；社区站 geohints.com、plonkit.net |
| `is-this-photo-real` | 图像真伪：ELA、噪声/JPEG 压缩、copy-move、光照一致性、C2PA | 工具目录型 |
| `secrets-in-file-metadata` | exiftool 挖 `Author`/`LastModifiedBy`/模板路径（**政府 PDF/Office 同法**） | EXIF/XMP/IPTC/PDF/Office 属性 |
| `secrets-in-git-history` | git 考古：commit 作者邮箱、`code search`、`.patch` 端点、trufflehog | GitHub/GitLab；邮箱域名→身份 |
| `recon-a-domain-passively` / `find-hidden-subdomains` | 不碰目标的资产盘点：**CT 日志**枚举子域、passive DNS | crt.sh、CT log、subfinder/amass —— 对 `.gov.cn` 资产面 |
| `find-exposed-servers` | 只读扫描库查暴露服务 | Shodan/Censys；`ssl.cert.subject.CN:`、favicon hash 等查询语法 |
| `find-leaks-in-the-wild` | paste/泄漏频道的 `site:` 搜，判断真假 | paste 聚合站、Telegram 频道索引 |
| `whose-number-is-this` | 手机号 E.164 归一 + 运营商/线路类型 + 反查 | `format-permutations.md`：**China `138 0013 8000`**（+86 分段） |
| `what-an-email-reveals` | 邮箱→机构格式推断、Gravatar、邮件头 Received/SPF/DKIM 链 | MX、邮件头分析 |
| `who-owns-this-domain` / `track-planes-and-ships` / `follow-the-crypto` / `what-leaked-about-you` / `graph-the-network` / `write-the-intel-brief` / `investigate-without-getting-made` / `investigate-anything` / `useosint` / `dig-through-data-brokers` | WHOIS/RDAP、ADS-B/AIS、链上追踪、泄露查询、关系图、情报报告、OPSEC、总路由 | `registry-catalogue.md` 是**以管辖区分组的登记处目录**，但中国只 1 行（同上） |

### 我们能吸收的 5 个方法

1. **「按要证明的结论选源」+ 四级来源标注**（`primary` / `secondary` / `self-asserted` / `derived`，两条 primary 相互印证才算定案）。
   → 官员数据可直接落地：干部任免公示=primary，媒体报道=secondary，百科/聚合站=derived；写进我们的汇总口径，替代现在的「来源层级」模糊表述。
2. **档案 CDX 的 `collapse=digest` 时间线法**：把某页 400 次抓取坍缩成「内容真正变过」的 6 行，用变更日期反推**任免/部门调整的时间点**；`matchType=domain` 还能翻出已消失的子域。
   → 中文站点自身无历史版本时，这是唯一可枚举的路子（网络可达性见 `historical-web.md`）。
3. **引擎分工 + 保真度自检**：`site:` 穷举放必应、正文/精确串放 Google Verbatim、非拉丁/图搜放 Yandex、老冷门放 Mojeek/Marginalia/Brave；**脚本请求会静默降级**，任何依赖的操作符先做一次「已知答案」对照。
   → 直接搬进 `search-syntax.md` 的引擎选择原则。
4. **平台 ID 机制 = 时间锚**：snowflake/顺序 ID 可从帖子或用户 ID 反推注册/发帖时间；句柄会改、数字 ID 不变 → 记录 ID 而非只记昵称。
   → 微博/B 站/抖音的 ID 都是 snowflake，可给账号「独立于其所声称」的时间边界；配合 `hunt-a-handle` 的 `_92` 后缀/leet 变体表做跨平台同人判定。
5. **图像定位的中国视觉指标**：简体汉字=大陆/新加坡；车牌**蓝底白字=普通车、绿牌=新能源、黄牌=货车/大巴/教练**；I 型插座=中国；屋面太阳能热水器（中国/以色列常见）；中国国道盾形标志 + 社区站 geohints.com / plonkit.net。
   → 官员调研中的活动照/会议照可做地点核验（**只作「缩小范围」，不作证明**）。

### 实测

2026-10-03，macOS（arm64），`gh api repos/UseOSINT/Skills/tarball` → 301731 B tarball，解包 `UseOSINT-Skills-06243a5`；`find skills -name SKILL.md | wc -l` = 29，`find skills -path '*/reference/*.md'` = 51，总 md = 85；`LICENSE` 首行 `MIT License`；`plugin.json` → `name: useosint` v1.0.0，`repository: github.com/useosint/osint-skills`，`license: MIT`；China 相关命中：`who-really-owns-it/reference/registry-catalogue.md:86`（国家企业信用信息公示系统）、`find-the-original-image/SKILL.md:38` 与 `reference/engine-matrix.md:69`（百度图搜）、`geolocate-from-pixels/reference/regional-indicators.md:35,82`（简体字/车牌底色）、`:259`（太阳能热水器）、`:267`（I 型插座）、`whose-number-is-this/reference/format-permutations.md:64`（+86 号段）。

## 坑

- **该库是英文/欧美优先**：登记处目录里中国只有 1 行（国家企业信用信息公示系统），人物源目录**没有中国**（户籍/人事/事业单位公示等缺失）→ 它给方法，不给中国源；中国源仍走我们的 `gov/`、`stats/`、`legal/`。
- 它默认网络环境是「Google/Wayback 可达」，而**本机都不可达**（见 `historical-web.md`、`search-syntax.md`）→ 抄方法可以，抄命令前先 `nc -z` 判活。
- 仓库名/出处不一致（`UseOSINT/Skills` vs `useosint/osint-skills`），引用时写明实际下载到的 commit `06243a5`。
