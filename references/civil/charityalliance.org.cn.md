# charityalliance.org.cn —— 中慈联官网与慈善行业资讯

- 去哪找：**中国慈善联合会（中慈联）官网** `https://www.charityalliance.org.cn/`；站内栏目含 会员名单、年度报告、会费收支情况、接受捐赠情况、团体标准、慈善研究、中华慈善奖、中国慈善年会等。
- 什么时候用：要**中慈联会员名单/分支机构**、**年度报告与会费/捐赠收支**、**慈善行业标准（团体/国家/职业标准）**、**中华慈善奖获奖名单**、**慈展会/慈善年会资讯**、慈善行业新闻与学术理论文章。
- 怎么搜：**HTML 站点**，无公开检索 API；栏目页与详情页为静态/半静态 HTML，下载件经 `/dl/<加密串>.html` 跳转（前端 `static/index/encryption.js` 解密）：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
  curl -s -A "$UA" 'https://www.charityalliance.org.cn/'            # 首页
  # 栏目/详情为站内相对链接，下载件形如 /dl/<base64-ish>.html
  ```
  结果形态：**HTML（UTF-8）**；部分链接为加密跳转。
- 覆盖：中慈联**会员 1301 个**（自述，2013 年民政部登记、国务院批准成立的全国性社会团体，2019 年获联合国经社理事会特别咨商地位）；栏目覆盖慈善机构/企业/个人捐赠、年度报告、标准、赛事与年会资讯；粒度=机构/届次/文章级。
- 门槛：**免费、免登录**浏览；下载件走加密 `/dl/` 链接。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA，20 s 超时）——`GET https://www.charityalliance.org.cn/` → **200**，129 694 B，`<title>中国慈善联合会_中慈联_中国慈善联合会官网</title>`，`<meta description>` 自述「2013 年…民政部登记…会员 1301 个」；页内栏目含「会员名单/年度报告/会费收支情况/接受捐赠情况/团体标准/中华慈善奖/中国慈善年会」；下载链接形如 `/dl/<加密串>.html`，前端脚本 `static/index/encryption.js`。
- 上游：中国慈善联合会 `https://www.charityalliance.org.cn/`。

## 细节

- 站内主要栏目（首页导航实测）：会员名单/会员风采/分支机构、会领导/常务理事、年度报告/会费收支情况/会费标准、接受捐赠情况、企业慈善、慈善研究、学术理论、中华慈善奖、中国慈善年会、慈展会、团体标准/国家标准/国家职业标准、在线课程/培训项目。
- 前端脚本栈：`static/home/js/jquery.js`、`static/home/js/header.js`、`static/index/encryption.js`、`static/index/js/…`。

## 坑

1. **下载链接加密**：`/dl/<加密串>.html` 需前端 `encryption.js` 还原真实地址；离线抓取拿不到直链。
2. 无站内检索/接口，规模统计与名录以**页面列出**为准，无结构化导出。
3. `gy.alipay.com` 等同族二级域不可达，本卡仅覆盖 `www.charityalliance.org.cn`。
