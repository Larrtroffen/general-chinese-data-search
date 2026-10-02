# kaggle.com —— 竞赛与社区数据集市场

- 去哪找：数据页 `https://www.kaggle.com/datasets?search=<词>`；**列表 API** `https://www.kaggle.com/api/v1/datasets/list?search=<词>`（模型 / 竞赛：`/api/v1/models/list`、`/api/v1/competitions/list`）
- 什么时候用：找**竞赛数据与社区上传数据集**（遥感影像、行业表格、教学数据、NLP 语料）；先看体量与许可再决定要不要下（`totalBytes` / `licenseName` / `downloadCount`）。
- 怎么搜：
  ```bash
  curl -s -A 'kaggle-api/1.6.0' -H 'Accept: application/json' \
    'https://www.kaggle.com/api/v1/datasets/list?search=china&page=1'
  # → [{"id":…,"ref":"…","title":…,"subtitle":…,"description":…,"creatorName":…,
  #     "ownerName":…,"lastUpdated":…,"downloadCount":…,"totalBytes":…,
  #     "licenseName":…,"tags":[…],"files":[…],"url":"https://www.kaggle.com/datasets/…",
  #     "isPrivate":false,…}]
  ```
  - 参数：`search`、`page`、`sortBy`（`hottest` / `updated` / `votes` / `published`…）、`fileType`、`license`（上游声明，未逐项实测）。一页 **20** 条（实测）。
  - 单数据集：`GET /api/v1/datasets/list/{owner}/{name}`（上游声明，未本机实测）。
- 覆盖：数十万条社区数据集，含竞赛、遥感、表格、NLP；条目带 `files[]`（文件名 + 大小）与 `tags`。
- 门槛：**列表接口匿名可读**（实测）；**下载需 Kaggle 账号凭证**（`kaggle.json` / `KAGGLE_USERNAME`+`KAGGLE_KEY`）。
- 实测：2026-10-03，macOS arm64：`curl -A 'kaggle-api/1.6.0' '…/api/v1/datasets/list?search=china&page=1'` → **200**，77,467 B，JSON 数组 20 条（字段见上）；同一 URL 换**桌面浏览器 UA** → 200 但返回 **reCAPTCHA 挑战页**（`/recaptcha/challengepage/`）。
- 上游：`https://www.kaggle.com/`（Google）

## 坑

- 桌面浏览器 UA 会掉进 reCAPTCHA；脚本里用 `kaggle-api/1.6.0` 这类 UA 直接拿 JSON。
- 字段名有 `x` 与 `xNullable` 两套并存（`title` / `titleNullable`、`totalBytes` / `totalBytesNullable`），老字段可能为 `null`；解析时优先取 `x`，缺失再回落。
- 竞赛数据的下载许可与再分发规则各不相同，二次发布前逐条核 license。
