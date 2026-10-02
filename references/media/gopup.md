# gopup —— 指数/热榜/新闻联播接口库

`pip install gopup` 即用的 Python 库，把百度/微博/头条/谷歌/搜狗**指数**、中国宏观/利率、新经济公司、热搜榜（百度风云榜/微博热搜/微信热词/知乎/豆瓣/电竞）、生活数据（油价/迁徙/诗词/火车/票房）、疫情等打包成统一函数（底层直连各站或经第三方转发）。对我们主要是**"指数 + 热搜榜 + 新闻联播"这类另类数据入口清单 + 已知接口 URL**。

- 去哪找：repo <https://github.com/justinzm/gopup>；文档/注册 <http://www.gopup.cn>；PyPI `gopup`
- 什么时候用：要**搜索/资讯/媒体指数**（百度指数、微博指数、头条算数、谷歌趋势、搜狗指数）做关注度；要**热榜**（百度风云榜、微博热搜、微信热词、知乎、豆瓣）；或想找"新闻联播文字稿"的历史接口。
- 怎么取：

  ```python
  pip install gopup
  import gopup as gp
  df = gp.weibo_index(word="疫情", time_type="1hour")   # 官方 README 示例
  ```

  部分接口需先 `gp.set_token("<gopup.cn 的 TOKEN>")`。
- 覆盖：多为上游公开接口封装，实时/日更，取决于源站。
- 门槛：部分接口需 TOKEN（gopup.cn 注册）；百度指数系列必须自带有效 cookie。
- 实测：2026-10-03，macOS：通过 `gh api` 读取 README、`gopup/__init__.py`、`gopup/event/hot_list.py`、`gopup/event/history_daily.py`、`gopup/index/index_baidu.py`、`gopup/index/index_weibo.py` 与代码树，确认上述函数与 URL；**未 pip 安装或运行**（纪律：不执行第三方脚本/依赖）。索引接口可用性为"上游声明/源码所示，未本机实测"。
- 上游：<https://github.com/justinzm/gopup>（无 LICENSE）

## 细节

### 接口清单（README「数据仓库」+ `gopup/__init__.py` 导出）

- **指数**：百度 `baidu_search_index / baidu_info_index / baidu_media_index / baidu_interest_index / baidu_age_index / baidu_gender_index / baidu_atlas_index`；微博 `weibo_index`；搜狗 `sogou_index`；头条 `toutiao_index / toutiao_relation / toutiao_province / toutiao_city / toutiao_age / toutiao_gender / toutiao_interest_category`；谷歌 `google_index / google_fact_check`
- **宏观 / 利率**：`marco_cn`（GDP/CPI/PPI/PMI/货币供应/外汇储备/工业增加值/财政…）、`shibor`（Shibor 报价/均值、LPR）
- **信息数据**：**新闻联播文字稿**（README 列出）、`history_daily`（历史上的今日）、百度风云榜、微博热搜、微信热词、知乎热搜、豆瓣榜、电竞价值榜
- **生活 / 其他**：老黄历、油价、百度迁徙（`migration_area_baidu / migration_scale_baidu`）、诗词、火车（`station_name / train_time_table`）、票房/电视剧综艺指数、高校名单、疫情（网易/丁香园）

### 已知底层 URL（源码）

- `hot_list.py` 各热榜几乎全调第三方 `https://www.bjsoubang.com/api/getChannelData`；`history_daily.py` 调 `https://www.bjsoubang.com/api/getHistoryDaily`。
- 微博指数 `https://data.weibo.com/index/ajax/newindex/searchword` + `getchartdata`。
- 百度指数 `http://index.baidu.com/api/...` + 需**百度 index cookie** 解密（`baidu_decrypt.py`）。

## 坑

- 仓库**无 LICENSE**；README 声明"仅供学术研究，注意商业风险"。
- **部分接口需 TOKEN**（gopup.cn 注册）；百度指数系列必须自带**有效 cookie**，维护成本高。
- 大量热榜经**第三方 `bjsoubang.com`** 转发，第三方一旦停服即整体失效。
- **"新闻联播文字稿"存疑**：README 数据目录列出该项，但 GitHub 代码检索 "联播"/"lianbo"/"cctv" 在 `gopup/` 内**均无命中**（只命中 README），代码树也无 news 模块——实际能否调用需自行验证；要联播文字稿优先用 `xinwenlianbo-archive.md`。
