# city-data-cn —— 城市数据库与市统计局入口

- 去哪找：
  - **各城市统计局**：直辖市 `tjj.<省>.gov.cn`（北京 `tjj.beijing.gov.cn`、上海 `tjj.sh.gov.cn`、重庆 `tjj.cq.gov.cn`）或专名（天津 `stats.tj.gov.cn`）；地级市 `tjj.<city>.gov.cn`（广州/深圳/杭州/武汉…）或专名（成都 `cdstats.chengdu.gov.cn`）
  - **知城数据平台**（第一财经，含「城市数据库 / 免费数据 / API 开放平台」）`https://www.datayicai.com/`
  - **马克数据网**（「中国城市数据库」整编面板）`https://www.macrodatas.cn/`
  - 中经数据（城市时间序列，订阅）见 `cei-drc.md`
- 什么时候用：要**某个具体城市**的年度/月度指标（GDP、财政、人口、投资、消费…）、该市**统计公报/统计月报**原文；或要「全国地级市 × 多年」的整编面板（自建口径、校验其他源）。
- 怎么搜：
  - **市统计局站**：静态栏目为主，进站找「统计数据 / 统计公报 / 统计月报 / 统计分析」；年度《国民经济和社会发展统计公报》多为 HTML，月度数据多为 xls/xlsx。
    ```bash
    UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    curl -sS -A "$UA" 'https://tjj.sh.gov.cn/'       # 上海市统计局
    curl -sS -A "$UA" 'https://stats.tj.gov.cn/'     # 天津市统计局
    ```
  - **知城数据**：Nuxt SPA，城市指标走 `www.datayicai.com/home#/dataPlatform/…`；其查询接口 `POST /api/cityindex/index/freeQueryIndexTree|freeQueryIndexData|freeQueryAreaData` 需**时间戳/签名**参数（匿名直接调返回 `{"code":"10003","msg":"时间戳不存在"}`）——正常走浏览器页面。
- 覆盖：市统计局 = 本市历年公报/月报（年份跨度各市不同，一般 2000s 至今）；知城数据 = 城市指标/排名（免费体验 + 付费）；马克「中国城市数据库」= 地级市 2000–2024（**站方自述，未逐项核**）。
- 门槛：市统计局 **免费、无登录**（个别市有 WAF）；知城数据 **免费体验（需注册/登录）**；马克数据网 **注册/付费**。
- 实测：2026-10-03，macOS arm64，curl 8.x，桌面 UA，20 s 超时，≥1.5 s 间隔：
  - 市统计局首页：`tjj.sh.gov.cn` → 200；`stats.tj.gov.cn` → 200（`tjj.tj.gov.cn` → 000）；`tjj.cq.gov.cn` → 200；`tjj.gz.gov.cn` → 200；`tjj.sz.gov.cn` → 200；`tjj.hangzhou.gov.cn` → 200；`tjj.wuhan.gov.cn` → 200 ✅
  - `cdstats.chengdu.gov.cn` → **412**（WAF 挑战，curl 不可达，需浏览器）❌
  - `https://www.datayicai.com/` → 200（Nuxt SPA）；`GET /api/cityindex/index/freeQueryIndexTree` → 200 `{"code":"10003","msg":"时间戳不存在"}`（须签名）⚠️
  - `https://www.macrodatas.cn/` → 200（首页小、内容需登录）⚠️
- 上游：各市统计局官网站点（见上）；`datayicai.com`（上海第一财经/新一线）；`macrodatas.cn`。

## 细节

### 市统计局入口规律（2026-10-03 实测子集）

| 城市 | 入口 | 状态 | 站点命名规律 |
|---|---|---|---|
| 北京 | `https://tjj.beijing.gov.cn/` | ✅（见 `tjj.beijing.gov.cn.md`） | `tjj.<省/市>.gov.cn` |
| 上海 | `https://tjj.sh.gov.cn/` | ✅ 200 | 直辖市用省级缩写 `.sh.` |
| 天津 | `https://stats.tj.gov.cn/` | ✅ 200 | 专名 `stats.`；`tjj.tj.gov.cn` 不通 |
| 重庆 | `http://tjj.cq.gov.cn/` | ✅ 200 | `tjj.<省缩写>.gov.cn` |
| 广州 | `http://tjj.gz.gov.cn/` | ✅ 200 | `tjj.<城市简写>.gov.cn` |
| 深圳 | `http://tjj.sz.gov.cn/` | ✅ 200 | 同上 |
| 杭州 | `http://tjj.hangzhou.gov.cn/` | ✅ 200 | `tjj.<全拼>.gov.cn` |
| 武汉 | `http://tjj.wuhan.gov.cn/` | ✅ 200 | 同上 |
| 成都 | `http://cdstats.chengdu.gov.cn/` | ❌ 412 | 专名 `cdstats.` |

- 优先级：① `tjj.<市>.gov.cn` → ② `tjj.<省缩写>.gov.cn` → ③ 专名（`stats.`/`cdstats.`/`tjj.<全拼>.gov.cn`）。政务域名迁移频繁，先在市政府门户底栏「直属机构」里找实时链接，别硬猜。
- 站内栏目名不统一，认这几种：「统计数据 / 统计公报 / 统计月报 / 统计分析 / 数据发布 / 统计年鉴」；年度公报标题固定为「<市>国民经济和社会发展统计公报」。

### 城市面板平台

| 平台 | 入口 | 产品 | 门槛 |
|---|---|---|---|
| 知城数据平台 | `datayicai.com` | 城市数据库、免费指标、城市排名、API 开放平台 | 免费体验 + 付费 |
| 马克数据网 | `macrodatas.cn` | 「中国城市数据库」（地级市 2000–2024 平衡面板） | 注册/付费 |
| 中经数据 | `ceidata.cei.cn`（见 `cei-drc.md`） | 城市/区域时间序列 | 订阅 |
| 国家基础学科公共科学数据中心 | `nbsdc.cn`（见 `city-stat-yearbook.md`） | 城市统计年鉴数据集 | 注册 |

## 坑

1. **`tjj.<市>.gov.cn` 不是万能**：直辖市与部分市用 `stats.`/专名（天津 `stats.tj.gov.cn`、成都 `cdstats.chengdu.gov.cn`）；`tjj.tj.gov.cn` 直接连不上。
2. **部分市有 WAF**：成都 `cdstats.chengdu.gov.cn` 返回 **412**（curl 不可达），须浏览器或带 cookie 会话。
3. **知城数据 API 有签名**：`/api/cityindex/…` 匿名调用报「时间戳不存在」，别把它当免签 JSON 接口；走浏览器页面或申请开放平台 key。
4. 市统计局**月报多为 xls/xlsx、公报为 HTML**；老页面可能 GB2312 编码。
5. **整编面板 ≠ 原始口径**：马克「中国城市数据库」等按年鉴/公报二次加工（含插值填补），正式引用要回到市统计局/年鉴原表；注意「市辖区 vs 全市」口径。
6. 分省/主要城市的**官方数值**已另有卡片 `data.stats.gov.cn.md`，本卡只解决「市级入口 + 整编面板」，不重复国家统计局接口。
