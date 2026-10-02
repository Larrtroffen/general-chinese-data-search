# religion-publications —— 宗教期刊目录与学术检索

- 去哪找：**中国宗教学术网**（中国社会科学院世界宗教研究所）`http://iwr.cass.cn/`；**期刊年鉴**总入口 `/qknj/`，各刊目录页 `/qknj/<slug>/`（《世界宗教研究》`/qknj/sjzjyj/`、《世界宗教文化》`/qknj/sjzjwh/`、《中国宗教》`/qknj/zgzj/`、《中国道教》`/qknj/zgdj/`、《中国穆斯林》`/qknj/zgmsl/`、《天风》`/qknj/tianfeng/`、《法音》`/qknj/fayin/`）；站内检索 `http://iwr.cssn.cn/was5/web/search?channelid=218937&searchword=<kw>&page=1&catetype=search&searchscope=`。
- 什么时候用：要**宗教学期刊的逐年逐期目录**（论文题名、作者、期号）做文献计量/CSSCI 补录；要找**世界宗教研究所的学者名录与研究领域划分**（佛教/道教/儒教/基督教/伊斯兰教/宗教学理论/数字人文宗教等）；要宗教方向的学术动态、科研项目、征稿公告。
- 怎么搜：站内为**静态 HTML**（`t{YYYYMMDD}_*.shtml`），目录页直接列期次；全文检索走 **TRS WAS5**：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
  # 期刊目录页（以《世界宗教研究》为例）
  curl -sS -A "$UA" --compressed 'http://iwr.cass.cn/qknj/sjzjyj/'
  # 统一检索（返回 HTML 结果页）
  curl -sS -A "$UA" --compressed --get --data-urlencode 'searchword=佛教' \
    'http://iwr.cssn.cn/was5/web/search?channelid=218937&page=1&catetype=search&searchscope='
  ```
  结果形态：**HTML**（目录页与检索结果页）；无 JSON API。各教团体的刊物页为各自官网栏目（见下）。
- 覆盖：期刊目录年代视刊而异——《世界宗教研究》到 2026 年第 6 期，《中国宗教》目录回溯到 2016 年；含《世界宗教文化》《中国宗教学》《基督宗教研究》《中国本土宗教研究》《宗教与哲学》《宗教心理学》《宗教社会学》《中国宗教研究年鉴》等；另设专家学者（荣誉学部委员/学部委员/研究员/副研究员/助理研究员/离退休学者）、学术著作、学术动态、科研项目、讲座。更新随刊物出刊。
- 门槛：**免费、免登录、无 key**（目录页与 WAS5 检索均匿名）。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA——`GET http://iwr.cass.cn/` → 200 `<title>首页-中国宗教学术网</title>`，导航含 `/qknj/sjzjyj/`、`/qknj/zgzj/`、`/qknj/zgdj/`、`/qknj/zgmsl/`、`/qknj/tianfeng/`、`/qknj/fayin/` 等；`GET /qknj/sjzjyj/` → 200 `<title>《世界宗教研究》-中国宗教学术网</title>`，目录 `sjsmulu/202607/t20260701_6057087.shtml`＝「2026年第6期目录」；`GET /qknj/zgzj/` → 200，`mulu/202505/t20250526_5875782.shtml`＝「《中国宗教》2025年目录」（回溯至 2016 年）；`GET iwr.cssn.cn/was5/web/search?...searchword=佛教` → 200 `<title>中国社会科学网统一检索服务平台</title>`，正文「结果， 如下是第 1-10 项」。
- 上游：<http://iwr.cass.cn/qknj/>（中国社会科学院世界宗教研究所·中国宗教学术网）。

## 细节

### 期刊年鉴 slug（首页导航实测）

| slug | 刊物 |
|---|---|
| `sjzjyj` / `sjzjwh` | 《世界宗教研究》/《世界宗教文化》 |
| `zgzj` / `zj` | 《中国宗教》/《宗教》 |
| `zgdj` / `zgmsl` / `tianfeng` / `fayin` | 《中国道教》/《中国穆斯林》/《天风》/《法音》 |
| `dd` / `zjysj` / `hzyj` / `zgtzj` | 《中国宗教学》/《基督宗教研究》/《中国本土宗教研究》/《马克思主义宗教观学刊》 |
| `zjzx` / `zjxlx` / `zjshx` / `ldyj` / `zgzjyjnj` / `zjxyj` | 《宗教与哲学》/《宗教心理学》/《宗教社会学》/《儒道研究》/《中国宗教研究年鉴》/《宗教学研究》 |
| `albsjyj` | 《中国宗教研究》/《Studies in Chinese Religions》（英文刊） |

### 各教团体的刊物官方页

| 刊物 | 官方栏目 |
|---|---|
| 《中国穆斯林》 | `http://www.chinaislam.net.cn/web/whxc/a/list.shtml`（期次目录） |
| 《天风》 | `https://www.ccctspm.org/skywind`（另 `/onlinesky` 天风在线） |
| 《中国天主教》 | `https://www.chinacatholic.cn/ccic/folder/1809/0824-1.htm` |
| 《中国道教》 | `http://taoist.org.cn/zgdjzz.jsp` |
| 《法音》 | `https://www.chinabuddhism.com.cn/web/qk.html` |

### 检索与目录路径规律

- 目录文章路径 `/{栏目}/mulu/或sjsmulu/{YYYYMM}/t{YYYYMMDD}_{id}.shtml`；`t` 前缀为 CASS 站群静态命名，**id 不可猜**（须从列表页解析）。
- `/qknj/` 下另有 `zjxz/`（专家学者）、`xszz/`（学术著作）、`yjly/`（研究领域）、`qt/`（通知公告/学术动态/科研项目/获奖成果）。

## 坑

1. **两域名**：页面在 `iwr.cass.cn`，检索在 `iwr.cssn.cn`（`www.cssn.cn` 站群）；只请求 `cass.cn` 拿不到检索结果。
2. **WAS5 检索为 HTML**：结果经「中国社会科学网统一检索服务平台」渲染，非 JSON，解析正文「第 1-10 项」与结果条目；`searchscope` 留空即全站。
3. **目录页只到「目录」层级**：多数期刊仅列期次题名，正文/PDF 不在此站，需按题名另找（知网/国家哲学社会科学文献中心 `ncpssd.cn`）。
4. **《中国宗教》杂志社无独立官网**：`xueshuzixun.com`、`ndhx.net`、`jyqikan.com` 等均为第三方投稿代发站，**非官方**；要目录以本站 `/qknj/zgzj/` 为准，要正文走文献库。
5. 与 `../academic/` 层不重复：该层无宗教学期刊/机构卡；本卡专收宗教研究刊物目录与学者库。
