# yuandian-law-search —— 元典智库付费法律检索

`cat-xierluo/legal-skills` 中的法律检索 Skill：优先走元典 MCP，无 MCP 时走 `open.chineselaw.com` 的 **API**。覆盖法规语义/关键词、普通案例/权威案例、企业画像与"法规引用幻觉检测"。**需付费 API Key**，作为免费源的备选。

- 去哪找：
  - Skill：`https://github.com/cat-xierluo/legal-skills/tree/main/skills/yuandian-law-search`（上游仓内：`SKILL.md`、`endpoints/*.md`、`references/09-api-usage.md`、`scripts/yd-run`）
  - 平台/取 Key：`https://open.chineselaw.com`
  - 仓库根目录**无 LICENSE 文件**（GitHub 404），但 skill 目录含 `LICENSE.txt`（作者标 MIT，见 SKILL.md frontmatter）。
- 什么时候用：
  - 免费源（flk / chinese-law-corpus / cn-law-hub）**不够**时：需要**语义检索**、**权威案例**、**案由/效力级别/地域过滤**、**企业画像**，或需要对已有文本做**引用幻觉检测**。
  - 明确知道法名条号时不必用它，直接 flk / corpus 更省。
- 怎么取：
  ```bash
  export YD_API_KEY='<open.chineselaw.com 签发>'
  # Skill 自带 CLI（Python3 标准库，无第三方依赖）
  scripts/yd-run --no-report detail "中华人民共和国民法典" --ft-name "第六百九十二条"
  scripts/yd-run --no-report search "普通房屋租赁中履约保证金的性质及违约金调减"
  scripts/yd-run --no-report case "房屋买卖 过户 尾款 同时履行"
  # 裸调：
  curl -s -H "Authorization: Bearer $YD_API_KEY" -H 'Content-Type: application/json' \
    -X POST --data '{"keyword":"行政处罚","search_mode":"AND","top_k":10}' \
    'https://open.chineselaw.com/open/rh_ft_search'
  ```
  MCP 路径：客户端配好元典工具即可，无需本地 Key/CLI。
- 覆盖：
  - 法规侧：`fatiao{ftid,fgid,fgtitle,num,content,sxx,effect1,effect2,dy,location,start,end,score}`；`effect1` 效力级别含宪法/法律/司法解释/行政法规/监察法规/部门规章/党内法规/地方性法规/地方政府规章/地方规范性文件等 17 类。
  - 案例侧：`scid,spcx,ajlb,jbdw,title,jand,jaDate,wszl,ah,content,xzqh_p,cj,anyou,score`（语义）；关键词侧 `data.total/lst`。
  - 幻觉检测返回 `regulations[]`（`law_exists`、`semantic_compare{结论,语义相似度,要点}`）与 `cases[]`。
- 门槛：**需付费 Key**（缺失时 401）；调用耗积分（10/次，检测 50/次），批量前先确认预算；请求发往 `open.chineselaw.com`，来源链接可能在 `ydzk.chineselaw.com`。数据留存：CLI 默认写 `archive/`（可用 `--no-report`/`--no-archive` 调整）。
- 实测：2026-10-02，macOS，curl 8.x。① `GET https://open.chineselaw.com` → **HTTP 200**，15,412 B（平台可达）。② 无 Key `POST /open/rh_ft_search`（body `{"keyword":"行政处罚"}`）→ **HTTP 401**。③ **有 Key 的成功调用未本机实测**（无付费账号）；端点/字段来自 skill 的 `endpoints/*.md` 文档（作者 2026-09-22 核对官方 api-square）。
- 上游：`https://github.com/cat-xierluo/legal-skills`（`skills/yuandian-law-search/`）

## 细节

### 端点（Base `https://open.chineselaw.com`，多数计费 10 积分/次）

| 端点 | 方法 | 用途 | 计费 |
|---|---|---|---|
| `/open/law_vector_search` | POST | 法规**语义**检索（`query`，`fatiao_filter{sxx,effect1,law_start,law_end}`，`return_num`/`rewrite_flag`） | 10 |
| `/open/rh_ft_search` | POST | 法条**关键词**检索（`keyword`，`fgmc`/`xljb_1`/`sxx`/`fbrq_*`/`ssrq_*`，`top_k`≤50） | 10 |
| `/open/rh_ft_detail` | POST | 法条详情（`id` 或 `fgmc`+`ftnum`，`refer_date`） | 10 |
| `/open/case_vector_search` | POST | 案例**语义**检索（`wenshu_filter{wenshu_type,wszl,ja_*,dianxing,fayuan,cj,xzqh_*}`） | 10 |
| `/open/rh_ptal_search` | POST | **普通案例**关键词（`qw/fxgc/ah/ay/jbdw/xzqh_p/wszl/ajlb/yyft`，`top_k`≤50） | 10 |
| `/open/rh_qwal_search` | POST | **权威案例**关键词（同普通，无 `fxgc`/`yyft`） | 10 |
| `/open/rh_case_details` | GET | 案例详情（`type=ptal|qwal`，`id` 或 `ah`） | 10 |
| `/open/rh_company_info` | GET | 企业名称检索（`name`，`num`≤50） | 10 |
| `/open/hall_detect` | POST | 法规/法条/案例**幻觉检测**（`text`） | **50** |

另有约 22 个企业画像端点（`/open/…`：聚合/对外投资/商标/专利/软著/ICP/变更/裁判文书/开庭公告/被执行/失信/税务/严重违法等），按需查 `endpoints/*.md`。
