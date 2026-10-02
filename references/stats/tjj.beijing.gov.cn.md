# tjj.beijing.gov.cn —— 北京统计年鉴公报与月季度数据

- 去哪找：统计数据总入口 `https://tjj.beijing.gov.cn/tjsj_31433/`；北京统计年鉴 `https://tjj.beijing.gov.cn/tjsj_31433/tjnj_31441/bjtjnj_31442/`（跳 `nj.tjj.beijing.gov.cn`）；统计公报 `https://tjj.beijing.gov.cn/tjsj_31433/tjgb_31445/ndgb_31446/`；月/季度数据 `https://tjj.beijing.gov.cn/tjsj_31433/yjdsj_31440/`。
- 什么时候用：要北京**统计年鉴**（图片版）、**国民经济和社会发展统计公报**（HTML 正文）、**月/季度数据**（HTML 正文 + `.xls/.xlsx` 附件）的官方口径数据。
- 怎么搜：三类数据各有入口——
  - 年鉴：壳页跳 `nj.tjj.beijing.gov.cn/nj/main/{年份}-tjnj/zk/indexch.htm`，表格是扫描图片；
  - 公报：列表页静态 HTML 里有逐年链接，正文纯 HTML；
  - 月/季度：`…/yjdsj_31440/{系列}/index.html → ./{年}/index.html → ./{yyyymm}/t{...}.html`，正文附 xls/xlsx。
- 覆盖：北京市统计局·国家统计局北京调查总队官网；年鉴年份 2019/2020/2023/2024/2025 等的 `zk/indexch.htm` 均 200（2021、2022 未逐一验证）；公报 2003 起；月/季度数据按年×期。
- 门槛：免费，无需登录。
- 实测：2026-10-02，macOS（arm64），curl 8.x：首页 200；年鉴壳页跳转 `nj.tjj.beijing.gov.cn/nj/main/2025-tjnj/zk/indexch.htm`；2025 `C0101.jpg`(200/59 KB)、2024 `C01-01.jpg`(200/68 KB)、2019 `C01-01.jpg`(200/68 KB)；统计公报列表含 2019–2025 链接，2025 公报文章 200/47 KB；月/季度 GDP 与工业文章的 `.xlsx`/`.xls` 附件均 200 且 MIME 正确。
- 上游：北京市统计局 `https://tjj.beijing.gov.cn/`。

## 细节

### 栏目与入口（实测 200）

| 栏目 | URL | 说明 |
|---|---|---|
| 统计数据总入口 | `https://tjj.beijing.gov.cn/tjsj_31433/` | 列出全部子栏目 |
| 月/季度数据 | `https://tjj.beijing.gov.cn/tjsj_31433/yjdsj_31440/` | JS 跳转 → `gdp_31750/index.html` → `./{年}/index.html` |
| 数据解读 | `https://tjj.beijing.gov.cn/tjsj_31433/sjjd_31444/` | 月度运行情况快讯 |
| 北京统计年鉴 | `https://tjj.beijing.gov.cn/tjsj_31433/tjnj_31441/bjtjnj_31442/` | JS 跳转 → `nj.tjj.beijing.gov.cn` |
| 统计公报 | `https://tjj.beijing.gov.cn/tjsj_31433/tjgb_31445/ndgb_31446/` | 逐年公报列表（2003 起） |

⚠️ **多个栏目页是 `window.location.replace(...)` 跳转壳**，curl 拿到的是 100 字节左右的 `<script>` 片段；要跟到真实地址（见下）。

### 一、北京统计年鉴（图片版）

```
主站壳页  https://tjj.beijing.gov.cn/tjsj_31433/tjnj_31441/bjtjnj_31442/
        → https://nj.tjj.beijing.gov.cn/nj/main/{年份}-tjnj/zk/indexch.htm
```

- `indexch.htm` 是 frameset：`e/indexch.htm`（目录页）→ `e/frameset`：`e/left.htm`（左侧目录）+ `main`。
- **表格是扫描图片**，路径规则随年份变化（实测差异！）：

| 年鉴版本 | 表格路径样例 | 状态 |
|---|---|---|
| 2025-tjnj | `nj/main/2025-tjnj/zk/e/html/C0101.jpg`（1-1 行政区划(2024年)） | ✅ 200 59 KB，注意**无短横线** |
| 2024-tjnj | `nj/main/2024-tjnj/zk/e/html/C01-01.jpg`（1-1 行政区划(2023年)） | ✅ 200 68 KB，**有短横线** |
| 2019-tjnj | `nj/main/2019-tjnj/zk/e/html/C01-01.jpg` | ✅ 200 68 KB |

- 可在线访问的年份：2019 / 2020 / 2023 / 2024 / 2025 的 `zk/indexch.htm` 均 200（2021、2022 未逐一验证）。
- 目录里另有 `html/sm01.pdf`（简要说明）与 `html/tu01.jpg`（图表）。

```bash
# 拿某年鉴某表的图片
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
curl -s -A "$UA" -o C01-01.jpg \
  'https://nj.tjj.beijing.gov.cn/nj/main/2024-tjnj/zk/e/html/C01-01.jpg'

# 解析目录，拿全部表名+路径（GBK 编码）
curl -s -A "$UA" 'https://nj.tjj.beijing.gov.cn/nj/main/2024-tjnj/zk/e/left.htm' \
  | iconv -f gb18030 -t utf-8 | grep -oE "href='html/C[^']+'>[^<]+"
```

**坑**：站点是 **GBK/GB2312**（`iconv -f gb18030` 兜底）；图片无法检索文字，需要 OCR 才能取数——**要数值请优先用「月/季度数据」的 xls 附件或 `data.stats.gov.cn`**。

### 二、统计公报（HTML 正文，无需附件）

列表页 `…/tjgb_31445/ndgb_31446/` 静态 HTML 里有逐年链接：

```
2025 公报  ./202603/t20260326_4566469.html   （2026-03-26 发布）
2024 公报  ./202503/t20250319_4038820.html
2023 公报  ./202403/t20240321_3595860.html
…（2003 起）
```

正文为纯 HTML（含表格文字），直接抓 `https://tjj.beijing.gov.cn/tjsj_31433/tjgb_31445/ndgb_31446/{yyyymm}/t{...}.html` 后去标签即可。页内**无 xls/pdf 附件**（实测 2025 公报页面）。

### 三、月/季度数据（含 xls/xlsx 附件）

```
https://tjj.beijing.gov.cn/tjsj_31433/yjdsj_31440/{系列}/index.html
        → ./{年}/index.html          （列出该年各期文章）
        → ./{yyyymm}/t{yyyymmdd}_{id}.html   （正文，附 xls/xlsx）
```

系列代码（实测）：

```
gdp_31750  GDP          wh         文化产业      ly_32068  旅游        yf_32084  研发
xwqy_31906 中小微企业    jy_32008   就业          rk_32024  人口        jmsz_32036 居民收支
xxzs_31950 消费者信心指数 ny_31766   农业          gy_31782  工业        jzy_31798 建筑业
dscy_31862 第三产业      sy_31814   商业          ysyd_31830 运输邮电    tz_32052  固定资产投资
fdc_31846 房地产开发     cpi        CPI           sczjg_31966 生产价格指数 fj       房价指数
ldgd_31982 高端产业功能区 zgcsfq_31994 中关村示范区
```

- 年度索引页用 JS 排期：`title="2026-06-20;2026-03-20;"; link="./202607/t20260720_4770990.html;…"; reportMixQuarter(title, link, "1111")`，需正则取 `link`。
- 正文页附件：
  - GDP 季度：`./P020260720350553629493.xlsx`（✅ 200，13.6 KB，`application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`）
  - 工业月度：`./P020260916360913749250.xls`（✅ 200，22.5 KB，`application/vnd.ms-excel`）
- **附件是表格数据的正道**（xls 可直接用 stdlib `zipfile`/`xml` 或转发给 pandas 环境解析）。

```bash
# 例：抓 2026 年 1-8 月工业数据 xls（实测可下）
cd /tmp
curl -s -A "$UA" -O \
 'https://tjj.beijing.gov.cn/tjsj_31433/yjdsj_31440/gy_31782/2026/202609/P020260916360913749250.xls'
```

## 坑

1. 栏目壳页是 JS 跳转，别把 100 字节的 `<script>` 当正文。
2. 年鉴表格图片的命名规则**逐年变化**（2025 无短横线、2024/2019 有短横线）；必须现读 `left.htm`，不要套模板。
3. 年鉴站 `nj.tjj.beijing.gov.cn` 编码为 GBK。
4. 月/季度文章附件名是随机 `P020…`，**必须先抓文章页再解析附件名**，无法预测。
5. 公报页无附件，需自己解析 HTML 表格。
6. 礼貌抓取：站点响应正常，建议 ≥1.5s 间隔。
