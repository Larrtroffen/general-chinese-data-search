# stats.gov.cn-census —— 国家统计局人口普查数据

- 去哪找：人口普查数据栏目 `https://www.stats.gov.cn/sj/pcsj/rkpc/`（JS 跳 `./d7c/`）；第七次全国人口普查主要数据 `https://www.stats.gov.cn/sj/pcsj/rkpc/d7c/`；《中国人口普查年鉴-2020》 `https://www.stats.gov.cn/sj/pcsj/rkpc/7rp/`；人口普查公报 `https://www.stats.gov.cn/sj/tjgb/rkpcgb/`（未本机验证）。年度人口数值走国家数据 `../stats/data.stats.gov.cn.md`。
- 什么时候用：要**人口普查口径**的分省/分县人口、性别比、年龄结构、民族、受教育程度、家庭户、迁移流动；要《中国人口普查年鉴》整表；要区分普查（十年一次）与年度人口抽查口径。
- 怎么取：普查栏目是**静态 HTML 目录 + 扫描图片表**，无 API——
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # 年鉴目录（GB2312，条目指向 zk/html/*.jpg 图片表）
  curl -s -A "$UA" 'https://www.stats.gov.cn/sj/pcsj/rkpc/7rp/left.htm' | iconv -f gb2312 -t utf-8 | grep -o "href='zk/html/[^']*'"
  ```
  形态：`d7c/` 等主要数据页为 JS 渲染；年鉴表为**扫描 JPG**（如 `7rp/zk/html/A0101.jpg` =「1-1 各地区户数、人口数和性别比」）。
- 覆盖：历次普查栏目（`d1c`…`d7c`）；第七次（2020）主要数据 + 《中国人口普查年鉴-2020》（上/下册，图片表）；年鉴 `7rp/`。
- 门槛：免费；无 API；老页 **GB2312** 编码、表为 **JPEG 图片**（需 OCR）。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA）：`https://www.stats.gov.cn/sj/pcsj/rkpc/` 200（417 B，JS `location.href="./d7c/"`）；`/sj/pcsj/rkpc/d7c/` 200（61,923 B，`<title>第七次人口普查主要数据 - 国家统计局`，正文 JS 渲染）；`/sj/pcsj/rkpc/7rp/indexch.htm` 200（897 B，frameset，标题「中国人口普查年鉴-2020」）；`/sj/pcsj/rkpc/7rp/left.htm` 200（48,340 B，GB2312，含 `zk/html/A0101.jpg` 等条目）；`http://…/7rp/left.htm` 301（WAF `CWAP-waf`）。
- 上游：国家统计局 `https://www.stats.gov.cn/`。

## 细节

### 入口与形态

| 内容 | URL | 形态 | 实测 |
|---|---|---|---|
| 人口普查数据总栏 | `/sj/pcsj/rkpc/` | JS 跳转 | ✅ 200（跳 `d7c/`） |
| 第七次主要数据 | `/sj/pcsj/rkpc/d7c/` | JS 渲染 HTML | ✅ 200 |
| 人口普查年鉴-2020 | `/sj/pcsj/rkpc/7rp/` | frameset + JPG 表 | ✅ 200 |
| 年鉴目录 | `/sj/pcsj/rkpc/7rp/left.htm` | GB2312 HTML | ✅ 200 |
| 年鉴表图 | `/sj/pcsj/rkpc/7rp/zk/html/A0101.jpg` | JPEG | — |

- 年鉴结构：上册 = 全部数据资料（第一卷 概要 …）；表号形如 `A0101`（1-1 各地区户数、人口数和性别比），另有 `a/b/c` 后缀对应城市/镇/乡村。
- 历年普查路径同构：`d1c`/`d2c`/…/`d7c` 对应第一至第七次。

## 坑

1. 栏目页是 **JS 跳转壳**（`rkpc/` → `d7c/`），别直接抓 `rkpc/` 当目录。
2. 年鉴表是**扫描图片**，无结构化数据；批量取数需 OCR，且分城市/镇/乡村三套。
3. 编码为 **GB2312**（老页），抓取后需 `iconv` 转码。
4. `http://` 老路径会 301（WAF `CWAP-waf`），统一用 `https://`。
5. 普查口径≠年度人口抽样/估算，混用会出错；年度数值回 `../stats/`。
