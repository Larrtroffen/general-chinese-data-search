# bjdx.gov.cn —— 大兴区政府门户

- 去哪找：
  - 新闻页：`https://www.bjdx.gov.cn/bjsdxqrmzf/zhyw/dxdt13/{id}/index.html`
  - 示例（2018-04-04 大兴报：试点单位 7 个）：`https://www.bjdx.gov.cn/bjsdxqrmzf/zhyw/dxdt13/612689/index.html`
  - 站内检索后端（不可直调）：`api.so-gov.cn`
- 什么时候用：要大兴区区级新闻（《大兴报》转载件）与区级文件，2018 年新闻仍在线上。
- 怎么搜：
  - 站内检索为 JS 异步（`api.so-gov.cn`），直连不可用 → 用搜狗微信搜「大兴组工/大兴报」标题、`web_search site:bjdx.gov.cn`、360 `site:` 定位。
  - 已拿页面可小范围枚举 id（数字递增）试取同栏目文章。
  - 抓取：
    ```bash
    curl -s -m 25 -A 'Mozilla/5.0 …' 'https://www.bjdx.gov.cn/bjsdxqrmzf/zhyw/dxdt13/612689/index.html'
    ```
- 覆盖：大兴区政府门户新闻（区级文件、《大兴报》转载件）。
- 门槛：免费、免登录；静态 HTML，正文全文可取。
- 实测：2026-10-02（站群实测，见 `beijing-districts.md`）：`www.bjdx.gov.cn` 首页 ✅ 200，utf-8。
- 上游：<https://www.bjdx.gov.cn/>

## 细节

与其余 15 区门户（`www.bjhd.gov.cn`、`www.bjfsh.gov.cn` 等）同构，方法通用，见 `bjchy.gov.cn.md` 与 `beijing-districts.md`。

## 坑

1. 站内检索为 JS 异步（`api.so-gov.cn`），不可直连。
2. 文章路径为 `/{id}/index.html`，id 为数字，可小范围枚举。
