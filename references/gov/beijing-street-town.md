# 北京街乡镇 —— 16区街镇栏目定位

- 去哪找：
  - 街镇子栏目**总入口在区网「机构职能 / 政务公开」目录页**（16 区目录页见 `## 细节` 表首列）；
  - 三种存在形态：① 独立子域名（街镇级**基本不存在**，仅区属部门有）② 区网下的**拼音缩写栏目目录**（主流，13/16 区）③ **不透明数字 id 栏目**或仅在区政务平台（丰台/房山/大兴/密云/门头沟部分）。
- 什么时候用：要按「区 × 街道/乡镇」找该单位自己的公告、预算决算、执法公示、年报、主任/镇长动态；已知街镇名但不知道去哪个 URL；判断某街镇是否还有独立官网。
- 怎么搜：
  - **首选**：进 `## 细节` 表「目录页」→ 找到街镇名 → 跟随链接。目录页是唯一权威映射，别猜。
  - **拼音缩写可猜**（目录页失效时的兜底）：西城 `<abbr>jdbsc.html`、昌平 `/zj/<abbr>/xxgk<NN>/`、平谷 `/xzjd20/<abbr>/zfxxgkzn<NN>/`、顺义 `/zzfhjdbsc/<abbr><NN>/`、延庆 `/xzjd/<abbr>/`、石景山 `/gongkai/<abbr>jdbsc/`、东城 `/jdbscgs/<abbr>jdgs/`、怀柔 `/zxjddh/<abbr>/`。`<NN>` 为随机小数字，需先探测 1–2 个或走目录页。
  - **搜索引擎定位**：`site:<区门户域名> <街镇名> 政府信息公开指南`（web_search / 搜狗微信）；区网站内检索多不可直连（见 `beijing-districts.md`）。
  - **探测命令**：
    ```bash
    UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    curl -sSk -L -o /dev/null -w '%{http_code} %{url_effective}\n' -m 20 -A "$UA" '<url>'
    ```
- 覆盖：北京 16 区共 300+ 街乡镇（抽样名录见 `## 细节`）；形态为区网静态栏目，随年度/改版漂移；内容粒度到「单位级公告/预算/年报」。
- 门槛：免费、免登录；朝阳/延庆仅 http；顺义 `robots.txt` = `Disallow: /`（见 `beijing-districts.md`）。
- 实测：2026-10-03，macOS（arm64），curl（`-sSk -L -m 20`，桌面 UA），约 30 次探测（单主机 ≤3 次）。16 区**各抽 1 个街镇栏目全部 200**（门头沟/东城/石景山为 http→https 301 或 JS 跳转壳）；形态①抽样 10 个 `<街道>.bjX.gov.cn` 子域名**全 000**。明细见 `## 细节`。
- 上游：北京 16 区门户（见 `beijing-districts.md`）；年报树通道 `beijing-xxgk.md`

## 细节

### 16 区街镇栏目定位表（2026-10-03 实测）

| 区 | 目录页（权威映射） | 单街镇 URL 形态 | 单位数 | 备注 |
|---|---|---|---|---|
| 东城 | `https://www.bjdch.gov.cn/ztzl/dcqxzzfgs/jdbscgs/` | `.../jdbscgs/<abbr>jdgs/`（→`./jbxx<abbr>/`） | 17 街道 | 目录页是静态锚点，可直接枚举 |
| 西城 | `https://www.bjxch.gov.cn/xxgk/jgzn.html` | `https://www.bjxch.gov.cn/xxgk/jgzn/qjd/<abbr>jdbsc.html`（部分再嵌 `/jgzn.html`） | 15 街道 | 另有街道动态 `/xcdt/jddt.html` |
| 朝阳 | `http://www.bjchy.gov.cn/affair/govintro/depIndex_hbdw.html?depId=<32hex>` | 每街一个 `depId`；政务公开栏目 `.../dynamic/newspe/ysgkzl/jdbsc/` | 40+ 街乡 | **仅 http、GBK**；街道清单页 `/dynamic/newspe/chyqlqd/jiedb/` |
| 海淀 | `https://zyk.bjhd.gov.cn/jbdt/` | `https://zyk.bjhd.gov.cn/xxgkzl/gkzn/jdbsc/<日期>/t<id>.shtml`（年报 `.../nb/jdbsc/25jdbsc/`） | 20 街道 + 7 镇 | 门户 `www.bjhd.gov.cn` 301→`zyk.` |
| 丰台 | `https://www.bjft.gov.cn/xxfb/xxgk/` | `https://www.bjft.gov.cn/xxfb/xxgk/c100226/c1002XX/`（**数字栏目，无规律**） | 20+ 街镇 | 另有 `/xxfb/xxgk/c100226/<abbr>xxgk/` 变体；不能猜，须走栏目树 |
| 石景山 | `https://www.bjsjs.gov.cn/gongkai/` | `https://www.bjsjs.gov.cn/gongkai/<abbr>jdbsc/jgzn_<N>/` | 9 街道 | 首页为 JS 跳转壳 |
| 门头沟 | `https://www.bjmtg.gov.cn/bjmtg/zwxx/index.shtml` | `https://www.bjmtg.gov.cn/mtg11J<NNN>/zxgk/mtgqbm_list_zxgk.shtml` | 9 镇(J201–209)+4 街道(J210–213) | **J 码制**，http→https 301 |
| 房山 | `https://www.bjfsh.gov.cn/zwgk/xxgkzn/` | `https://www.bjfsh.gov.cn/zwgk/<slug>/fgwj_<n>/zfxxgkzn_<n>/` | 24 乡镇街 | `<slug>` 为历史遗留（如城关=`gjkjd`），**不可猜** |
| 通州 | `https://www.bjtzh.gov.cn/bjtz/zwgk/zcwj67/zfxxgknb/<年目录>/xzjd/index.shtml` | `.../xzjd/<id>/index.shtml`（id 为 19 位时间戳串） | 22 单位 | 按年份分目录（2024n78=2025 年报告） |
| 顺义 | `https://www.bjshy.gov.cn/web/zwgk/jgxx/zzfhjdbsc/index.html` | `.../zzfhjdbsc/<abbr><NN>/index.html` | 6 街道 + 19 镇 | `<NN>` 随机小数字；robots Disallow |
| 昌平 | `https://www.bjchp.gov.cn/cpqzf/xxgk2671/jgzn2024/index.html#zjlink` | `https://www.bjchp.gov.cn/cpqzf/zj/<abbr>/xxgk<NN>/index.html` | 22 单位 | 镇街动态 `/cpqzf/zj/zjxw/` |
| 大兴 | `https://www.bjdx.gov.cn/bjsdxqrmzf/zwfw/zfxxgk/zfxxgkzn/xzjd5/index.html` | `.../xzjd5/<数字id>/index.html` | 20 单位 | 数字 id 连续但不连续递增（723997–735402） |
| 密云 | `https://www.bjmy.gov.cn/zwgk/zfxxgk/zfxxgkzn/` | `.../zfxxgkzn/znxzjd/<日期>/t<id>.html` | 20 单位 | 目录页在 `zfxxgkzn/`，`zfxxgk/` 会 JS 跳转 |
| 平谷 | `https://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/zfxxgkzn53/index.html` | `.../xzjd20/<abbr>/zfxxgkzn<NN>/index.html` | 19 单位 | 街道用 `pgqbhjdbsc`/`pgqxgjdbsc` 全拼 |
| 怀柔 | `https://www.bjhr.gov.cn/zwgk/jgzn/xzjd/` | `https://www.bjhr.gov.cn/zwgk/zfxxgkjg/zxjddh/<abbr>/<abbr>jgzn/`（→`./<abbr>jgzz/`） | 2 街道 + 14 乡镇 | 目录页第二页另有街道 |
| 延庆 | `http://www.bjyq.gov.cn/yanqing/zwgk/zfgs1669/xzjd/index.shtml` | `.../xzjd/<abbr>/index.shtml`（机构另在 `/yanqing/xzjd62/<id>/`） | 3 街道 + 15 乡镇 | **仅 http** |

> 拼音缩写规律：取街镇名前 2–3 字声母（大栅栏=`asljdbsc` 例外、看丹=`kdjd`、熊儿寨乡=`xezx`）。带随机数字后缀的区（顺义/昌平/平谷/石景山/东城/怀柔）**必须先探目录页**。

### 形态① 独立子域名（本轮抽样）

| 抽样主机 | 结果 | 说明 |
|---|---|---|
| `yizhuang.bjdx.gov.cn`、`huangcun.bjdx.gov.cn`、`songzhuang.bjtzh.gov.cn`、`yongledian.bjtzh.gov.cn`、`chengnan.bjchp.gov.cn`、`xisanqi.bjhd.gov.cn`、`wanshoulu.bjhd.gov.cn`、`gulou.bjmy.gov.cn`、`dayu.bjmtg.gov.cn` | ❌ 000 | 街镇级独立子域名**已全部下线/无 DNS** |
| `chpjw.bjchp.gov.cn`（昌平纪检）、`cprd.bjchp.gov.cn`（昌平人大）、`jwjcw.bjshy.gov.cn`（顺义纪检）、`jjw.bjpg.gov.cn`（平谷纪检） | ✅ 200 | **区属部门**仍有独立子域，可继续按此规律猜部门 |
| `xysy.bjshy.gov.cn`（信用顺义） | ⚠️ 301 | 子域存在，跳主域 |

> 结论：按 `<街道>.bjXX.gov.cn` 猜街镇站**不要再用**；部门子域（`<按职能拼音><区简称>`）仍值得探测。

### 区属部门栏目名规律（住建委/规自分局/征收/应急）

| 部门 | 区网栏目形态 | 实例 |
|---|---|---|
| 住建委 | 拼音 `qzfcxjsw`（区住房城乡建设委）或 `zjw`；门头沟用 J 码 | 顺义 `/web/zwgk/jgxx/qzfwbj/qzfcxjsw/`；平谷 `/pgqrmzf/bm/zjw/`；房山 `/zwgk/qzfcxjsw/`；昌平 `/cpqzf/315734/qzfcxjsw/`；门头沟 `J006` |
| 应急局 | J 码 / 部门目录 | 门头沟 `https://www.bjmtg.gov.cn/mtg11J035/zxgk/mtgqbm_list_zxgk.shtml` |
| 规自分局 | 市垂管，区网**少有独立栏目**；规划方案公示挂区网「通知公告」 | 昌平 `/cpqzf/xxgk2671/tzgg30/ghgs/`（规划公示） |
| 征收/房屋征收 | 多并入住建委栏目或「重大建设项目」重点领域 | 昌平 `/cpqzf/xxgk2671/zdlyxxgk57/...` |
| 统一规律 | 区网「机构职能 → 区政府部门」逐一对应栏目；门头沟以 `J0xx` 数字码（J001 政府办 … J006 住建委 … J035 应急局） | 门头沟 `zwxx` 页可一次抓全部门码 |

### 批量定位方法（四步）

1. **走目录页**：区门户首页 → 「政务公开 / 机构职能」→「镇街」或「部门」列表，得权威映射（上表首列）。
2. **搜搜索引擎**：`site:<区门户> <街镇> 政府信息公开指南`，直接拿单街 URL；搜狗微信同理（见 `../engines/`）。
3. **按年树枚举**：政务公开目录树（`gongkai/`、`zfxxgk/`、`zfxxgknb/<年>/xzjd/`）逐年下钻，配合 `beijing-xxgk.md` 的爬取器。
4. **缩写探测兜底**：对上表「可猜」的区，按拼音缩写 + 目录页看到的 `<NN>` 规律批量 `curl` 探测（单主机限速）。

## 坑

1. **街镇栏目首页常是 JS/meta 跳转壳**：东城 `.../jgmjdgs/` → `./jbxxjgm/`、石景山 `/gongkai/lgjdbsc/jgzn_2042/` → `jgxx_2044/`、怀柔 `.../hrjgzn/` → `./hrjgzz/`。`curl` 直接取会只拿到 160b 壳页，**需 `-L` 无效（JS 不执行）→ 读 `location.replace` 目标或直接取列内页**。
2. **slug/id 不透明**：丰台 `c1002XX`、房山历史 slug、门头沟 `J0xx/J2xx`、大兴/密云数字 id、通州时间戳 id —— **一律不可猜**，只能走目录页或搜索引擎。
3. **带随机数字后缀**：顺义/昌平/平谷/石景山/东城/怀柔 的街镇栏目名带 `<NN>`（如 `gmjdbsc89`、`xxgk44`、`zfxxgkzn50`），缩写对但数字错就 404，须先探目录页。
4. **街镇独立子域名已死**：不要再按 `<街道>.bjXX.gov.cn` 猜；部门子域仍可用。
5. **HTTPS/编码**：朝阳、延庆仅 http；朝阳系 GBK（`iconv -f gb18030`）；门头沟/怀柔/东城部分页无 charset 头。
6. **路径漂移**：目录页 URL 随改版/年份变动（通州按年分目录、昌平 `jgzn2024`），脚本勿硬编码，用前先探测。
7. **顺义 robots** `Disallow: /`，批量抓取前自行确认合规。
