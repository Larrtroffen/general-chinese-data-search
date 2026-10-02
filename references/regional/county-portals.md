# county-portals —— 县级政府网与统计局入口

县级数据没有总入口，得**先定位到县**再进它的「统计公报 / 统计信息」栏。域名以 `www.<县名拼音>.gov.cn` 为主流，但省管差异（安徽加省缩写、湘/川缩拼）与 WAF 使「猜域名」只能当第一步，须逐县验证。

- 去哪找：
  - 县/县级市政府门户：`https://www.<县名拼音>.gov.cn/`（如 `www.ks.gov.cn`、`www.deqing.gov.cn`、`www.shouguang.gov.cn`）；县级市同样用市名。
  - 县统计局（多为县府站部门子站）：`/xtjj/`、`/bmxxgkml/xtjj/`、`/qzfzcbm/tjj/`，栏目名「统计信息 / 统计数据 / 统计分析 / 统计公报 / 统计年鉴」。
  - **地级市统计局整编栏**（一次定位多县）：`https://tjj.<市>.gov.cn/`，如长沙 `…/tjxx/tjsj/tjgb/qxgb/`（区县公报）、湖州 `…/col/1229208256/`（统计公报）。
  - 省级统计局「各市/县公报」栏（如陕西 `tjj.shaanxi.gov.cn/tjsj/ndsj/tjgb/gs/`、湖北 `tjj.hubei.gov.cn/tjsj/tjgb/ndtjgb/sztjgb/`）。
- 什么时候用：要**某个县**的统计公报、年鉴、月/年度指标或财政决算；已有县名/区划码要落到其官网；批量采集前先摸清入口规律。
- 怎么搜（批量定位四步）：
  1. 名录取全称与区划码 → `../stats/mca.gov.cn.md`（县以上静态表）或 `../stats/data_location.md`（离线 JSON）。
  2. 猜域名：`www.<县名拼音无调>.gov.cn`；失败换 `www.<省缩写><县名>.gov.cn`（安徽 `ahfeixi`）、县名缩写（长沙县 `csx`）、`<县名>.gov.cn` 去 www。
  3. 站内找栏：县府站搜「统计局」部门子站 → 「统计公报/统计信息」栏目；或搜索引擎 `site:<县域名> 统计公报`。
  4. 兜底走**地级市统计局**整编栏或县级公报聚合（见 `../stats/county-stats.md`）。
  结果形态：县府门户 + 栏目页为 HTML 目录，公报正文为 HTML（少数为 PDF/docx 附件）；部分浙江站统计栏目为 JS 渲染，需浏览器。
- 覆盖：全国 2800+ 县/县级市/市辖区，官网绝大多数在线；抽查 11 例中 8 例标准域名直达，3 例需换姿势（见实测）。
- 门槛：免费、无需登录；个别站（金堂 412、长沙县 www 418）有 WAF，需换域名/协议或浏览器。
- 实测：2026-10-03，macOS arm64，curl 8.x，桌面 UA，20 s 超时，≥1.5 s 间隔（抽查 11 例）：
  - `https://www.ks.gov.cn/` → 200（100,394 B）✅；`https://www.jinjiang.gov.cn/` → 200 ✅；`https://www.shouguang.gov.cn/` → 200（65,600 B）✅；`https://www.yidu.gov.cn/` → 200（39,443 B）✅；`https://www.lingbao.gov.cn/` → 200（56,695 B）✅；`https://www.deqing.gov.cn/` → 200（84,464 B）✅；`https://www.dege.gov.cn/` → 200 ✅
  - `https://www.csx.gov.cn/` → **SSL 证书主机名不符**；`http://csx.gov.cn/`（去 www + http）→ 200 `长沙县人民政府` ✅；`www.csx.gov.cn` 深页 → 418 WAF
  - `https://www.cixi.gov.cn/` → **410 Gone**；`http://www.cixi.gov.cn/` → 200 `慈溪市人民政府网站` ✅（仅 http 可用）
  - `https://www.jintang.gov.cn/` → **412**（WAF）❌；`https://ahfeixi.gov.cn/`（肥西，域名非 `feixi.gov.cn`）→ 本机 **521**，`feixi.gov.cn` → DNS 不解析
  - 地级市统计局：`https://tjj.changsha.gov.cn/` → 200；`…/tjxx/tjsj/tjgb/qxgb/` 列全下辖区县公报 ✅；`https://tjj.huzhou.gov.cn/` → 200（统计公报栏目 JS 渲染，8,930 B 无静态链接）⚠️；`https://tjj.suzhou.gov.cn/`、`https://tjj.hangzhou.gov.cn/`、`http://tjj.weifang.gov.cn/` → 均 200 ✅
- 上游：各县人民政府门户与统计局子站；地级市统计局；省级统计局地方公报栏目。

## 细节

### 栏目路径词典（实测/常见）

| 栏目 | 路径样例 |
|---|---|
| 统计分析 | `www.ks.gov.cn/kss/tjfx/xxgk_list.shtml` |
| 统计信息 | `www.ks.gov.cn/kss/tongji/xxgk_lists.shtml` |
| 统计年鉴 | `www.ks.gov.cn/kss/tjnj/`（正文页挂 zip 附件） |
| 区县公报（地市整编） | `tjj.changsha.gov.cn/tjxx/tjsj/tjgb/qxgb/` |
| 县统计公报 | `m.csx.gov.cn/zwgk/bmxxgkml/xtjj/sjyfx/tjgb/` |
| 区县公报（省局） | `tjj.hubei.gov.cn/tjsj/tjgb/ndtjgb/sztjgb/` |

- 政府站 CMS 常见两族：**`col/colNNNNN/index.html`**（浙江系）、**`<频道>/<栏目>/index/list.shtml`** 与 **`/xxgk/…/subIndex-1.html`**（江苏/河南系）；翻页多为 `index_N.html` / `page/N` / `subList-N.html`。

## 坑

1. **别硬猜域名**：肥西县是 `ahfeixi.gov.cn`（加省缩写），长沙县是 `csx.gov.cn`（缩拼）；先搜再猜，猜错浪费请求。香港/澳门/台湾另算，不在此规律内。
2. **协议与 www 敏感**：慈溪 `https` → 410、`http` → 200；长沙县 `www` 证书不符、去 `www` 正常。https 失败先试 http / 去 www。
3. **本土 WAF 高发**：四川部分县（金堂）整站 412、湖南长沙县 `www` 深页 418（云 WAF 拦截页带「事件ID」）。换域名/协议、加 `Referer`，或改浏览器；`m.<县>.gov.cn` 移动域名常绕过（注：本机对 `m.csx.gov.cn` 根路径一次超时、深路径一次 200，稳定性一般）。
4. **省级上云后统计局消失**：浙江等省的县级「统计数据」被收进省级政务平台（如 `mapi.zjzwfw.gov.cn/…/2001941911`，SPA 需浏览器），县府站上只剩「统计数据」跳转链接。
5. 县府站栏目多为 SPA/JS 渲染（湖州统计局统计公报栏静态 HTML 无链接），curl 拿到壳时须换浏览器或找其数据接口。
