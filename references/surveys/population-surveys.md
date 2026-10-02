# population-surveys —— 人口与流动人口专项调查

- 去哪找：中国人口与发展研究中心（人发中心）`https://www.cpdrc.org.cn/sjzw/`（数据资源）→ 调查数据 `https://www.cpdrc.org.cn/sjzw/dcsj/`、数据实验 `https://www.cpdrc.org.cn/sjzw/yjgj/`；**CMDS 现行数据出口**在国家人口健康科学数据中心 `https://www.ncmi.cn/phda/browse.html?type=2`；老龄专项在中国老龄科学研究中心 `http://www.crca.cn/index.php/73-data-resource.html`。
- 什么时候用：要**流动人口/农民工个体级监测数据（CMDS）**、生育与家庭专项调查、全国及分省人口预测、老年人生活状况抽样调查；做人口迁移/城镇化/生育意愿/托育/老龄实证。
- 怎么搜：见「细节」——NCMI 走 **JSON 检索接口**（POST `search_data.do`）；人发中心调查数据是**静态大表**（按 `<tr>` 解析）；老龄中心各波次为 HTML 简报 + `数据使用申请表.docx`。
- 覆盖：CMDS 2009–2018（年度，全国 31 省+兵团，年样本≈20 万户）及多个专题；人发中心调查数据目录 111 项（含 1982/1990/2000 三次普查个案、1982–2006 全国生育类调查、家庭发展追踪、生育意愿、流动人口流出地监测、托育需求）；老龄抽样调查 2000/2006/2010/2015/2021。
- 门槛：NCMI 注册/登录后申请下载；人发中心目录页免费浏览、数据本身不公开下载；**CMDS 线上免费通道已于 2023-09-25 关闭**，现走数据交换/课题合作或 NCMI；老龄中心需单位填表邮件申请。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA（`-L`、20s 超时）——`cpdrc.org.cn/` 200（35,129 B）、`/sjzw/` 200（20,712 B）、`/sjfw/dcsj/` 200（467,925 B，`<title>调查数据`）、`/sjzw/yjgj/` 200（21,829 B）、`/tzgg/202401/t20240124_17628.html` 200（31,738 B）；`ncmi.cn/phda/browse.html?type=2` 200（94,959 B）、POST `ncmi.cn/dataSearch/search_data.do` 200 返回 JSON（`count=10`）；`crca.cn/` 200（21,530 B）、`/index.php/19-data-resource/life.html` 200（10,756 B）、`/index.php/76-data-resource/data-service.html` 200（9,169 B）；`geodata.cn/wjw/` 200（54,829 B）；`http://www.chinaldrk.org.cn/wjw/` **连接失败（000）**。
- 上游：国家卫生健康委（`https://www.nhc.gov.cn/`）、中国人口与发展研究中心、国家人口健康科学数据中心、中国老龄科学研究中心。

## 细节

### 一、CMDS：找数据的三个口

| 入口 | URL / 方式 | 形态 | 实测 |
|---|---|---|---|
| 国家人口健康科学数据中心（现行） | `https://www.ncmi.cn/phda/browse.html?type=2` | JS 页面 + JSON API | ✅ 200 |
| 数据检索 API | `POST https://www.ncmi.cn/dataSearch/search_data.do` | JSON | ✅ 200 |
| 地球系统科学数据中心（专题库） | `https://www.geodata.cn/wjw/`、`https://www.geodata.cn/thematicView/Population.html?typeid=627254088304`（流动人口专题数据库） | JS 页面 | ✅ 200 |
| 流动人口数据平台（原免费通道） | `http://www.chinaldrk.org.cn/wjw/#/home`（SPA） | 已闭 | ❌ 本机不通 |

NCMI 检索（`keyword` 明文，`searchField=name_ch` 为按标题检索，缺它则命中 0）：

```bash
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
curl -s -A "$UA" -X POST 'https://www.ncmi.cn/dataSearch/search_data.do' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'Referer: https://www.ncmi.cn/phda/browse.html?type=2' \
  --data-urlencode 'solrCore=all_dataset' --data-urlencode 'pageNumber=1' \
  --data-urlencode 'pageSize=10' --data-urlencode 'searchField=name_ch' \
  --data-urlencode 'keyword=流动人口'
```

返回 JSON：`data[].name_ch`（标题，含 `<em>` 高亮）、`data[].source`（多为「国家卫生健康委流动人口服务中心」）、`data[].type`（`data_set`）、`data[].open_time`；`count`/`pageSize` 分页。2026-10-03 命中 10 条，含：

- 中国流动人口动态监测调查数据（2017 年）／2018 年
- 中国流动人口卫生计生动态监测健康数据（2009–2017 年）
- 6 城市专题（2010）、8 城市社会融合（2013、2014）、6 省市流出地（2014）
- 2016 年流动人口健康素养专题、8 城市重点疾病流行因素（2017）
- 流动人口基层调查联系点调查数据（2017–2020）

数据详情页 `/phda/dataDetails.do?id=<数字id>`（如 `id=3144` = 2018 年 CMDS）为 **JS 渲染**，正文由接口注入，需浏览器或登录后下载。

### 二、人发中心（CPDCR）调查数据目录

`/sjfw/dcsj/`（旧「数据服务」，467 KB，Word 粘贴的 HTML 大表）→ `/sjzw/dcsj/`（新「数据资源」）逐项解析 `<tr>`，列：序号 · 名称 · 数据来源 · 数据类型 · 时间 · 地点 · 样本量 · 组织者 · 实施者。目录 111 项包括：

- 普查个案：1982 三次、1990 四次、2000 五次全国人口普查（个案数据）
- 生育类全国调查：1982 1‰ 生育率、1988 生育节育、1992 计生管理信息系统、1997 人口与生殖健康、2001 计生/生殖健康、2006 人口和计划生育
- 流动人口监测：2009（5 城市 4.7 万）～2016（全国 16.9 万）；2013/2015 流出地监测；2011/2012 三类地区
- 家庭与生育意愿：2013 试调查/2014 中国家庭发展追踪调查；2013/2015 生育意愿；2016 城市 3 岁以下婴幼儿托育服务需求调查
- 汇总数据集：中国常用人口数据集、生育/婚姻/死亡/迁移/年龄性别结构/分省/分县数据集、「人口与计划生育常用数据手册」1999–2015 逐年

新栏目「数据实验」`/sjzw/yjgj/`：PADIS-INT 人口预测（全国及各地预测结果浏览/查询）。

人发中心 2024 年起自组「**中国人口与发展抽样调查**」（公告 `/tzgg/202401/t20240124_17628.html`，2024-01-24）：全国样本 6 万人、3000 个村（居）级样本点、300 个监测县，分层随机抽样，含生育/托育成本/婚育文化/迁移等模块。

### 三、老龄专项：中国老龄科学研究中心（crca.cn）

- 数据资源总览 `/index.php/73-data-resource.html`（抽样调查 / 数据发布 / 数据平台三块）。
- 抽样调查 `/index.php/19-data-resource/life.html`：中国城乡老年人生活状况抽样调查 2000、2006、2010、2015、2021（每 5 年一次，60+ 全国 31 省），各波次有 HTML 数据简报。
- 申请：`/index.php/76-data-resource/data-service.html`「数据使用须知」——范围含上述五波 + 老年金融消费者权益、养老服务人才、老年人体质与跌倒风险、居家社区养老服务供给等专项；填《数据使用申请表》（`/images/20241104sjsysq.docx`）发 `crca2021@163.com`。

### 四、人口普查个体级数据（不重复，转引）

- 国家统计局微观数据（普查/1% 抽样现场使用）→ `microdata.stats.gov.cn.md`。
- 普查年鉴分省/分县汇总（图片表）→ [`../health/stats.gov.cn-census.md`](../health/stats.gov.cn-census.md)。
- 可下载的中国普查微数据（1982/1990/2000，跨国可比）→ `ipums.org.md`。
- 上海市人口数据研究中心 `https://popdata.fudan.edu.cn/home/application/`：面向课题立项团队的上海人口数据实验室申请（2026-10-03 实测 200 / 9,045 B）。

## 坑

1. **CMDS 线上免费通道已关**：国家卫健委流动人口服务中心 2023-09-25 起停止线上免费开放，申请通道同日关闭；2023-09-24 前提交的申请受理至 11-10。后期「可通过数据交换、课题合作等方式提供服务」；数据更新至 2018 年（2018 年机构改革后流动人口司撤销，无新调查）。旧的免费模式（2014 年通知口径：可按 申请使用 / 数据交换 两种方式，须单位主体、不接受个人，模板表 `.doc`）仅作历史参考。
2. **NCMI 检索必须带 `searchField=name_ch`**；只给 `keyword` 会返回 `count=0`。参数不全或高频请求会落到 `/modules/error/` 错误页，且可能短暂连接失败（000），放慢重试。
3. NCMI 数据详情页与 geodata 数据集页均为 **JS 渲染**，`curl` 拿不到标题/摘要主体；下载基本要登录/申请。
4. `chinaldrk.org.cn` 本机连不上（000）；`ldrk.org.cn` 同属旧平台，勿在脚本里写死。
5. 人发中心目录页把表整段贴在 HTML 里（含大量内联 Word 样式），解析要按 `<tr>/<td>` 去标签并 `html.unescape`，不要按行切。
6. 人发中心「调查数据」与「数据实验」「旧数据服务」三套栏目并存（`/sjzw/`、`/sjfw/` 路径不同），目录页年份子目录形如 `/sjzw/dcsj/2023dcsj/`、`/sjzw/dcsj/2022dcsj/`；改版后老路径易 404。
7. 老龄中心页面为 HTTP（非 HTTPS），正文在 `index.php` 路由下；申请表是 `.docx` 附件，邮箱在页面里用反爬插件隐藏（须看源码或 `crca2021@163.com`）。
