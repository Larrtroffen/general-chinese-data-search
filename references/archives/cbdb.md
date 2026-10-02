# CBDB —— 中国历代人物传记资料库

CBDB（China Biographical Database，哈佛/北大/台史所合作）把中国历史人物做成**关系型数据库**（人物、别名、官職、任官地点、親屬、社會關係、科舉、著作…）。`cbdb-project/cbdb_sqlite` 是**官方 SQLite 发行仓**：只放 `latest.json` 元数据 + 后处理脚本，**数据本体在 Hugging Face**。做「官员/人物数据工作流」时，这是**人物身份与官職的标准底板**（可与方志、登科录交叉核对）。

- 去哪找：
  - 元数据仓（版本/文件名/SHA-256/下载链接）：`https://github.com/cbdb-project/cbdb_sqlite`
  - 版本清单（`latest.json`，先取它）：`https://raw.githubusercontent.com/cbdb-project/cbdb_sqlite/master/latest.json`
  - 数据本体（HF dataset，含 `history/` 历史版本）：`https://huggingface.co/datasets/cbdb/cbdb-sqlite`（`latest.zip` 为当前版）
  - 官方站点：`https://cbdb.hsites.harvard.edu/`
  - 后处理脚本（视图/外键/ADDRESSES 表）：仓内 `scripts/`（`create_views.sh`、`add_foreign_keys.py`、`create_addresses_table.py`、`setup_cbdb.ipynb`）
- 什么时候用：
  - 需要**历史人物（唐—清为主）的标准化档案**：别名、生卒、籍贯、官職履历、亲属与社交关系；
  - 要**按人名/地名/官职做关系查询**（SQL 直接查，不是一个网页一个网页点）；
  - 想把方志/名录里的人名**对到权威 ID**（`c_personid`）。
- 怎么取：
  ```bash
  # ① 取版本元数据（务必先看这个，文件名/链接会变）
  curl -s https://raw.githubusercontent.com/cbdb-project/cbdb_sqlite/master/latest.json
  #   当前内容（2026-10-02 实测）：sqlite_filename=cbdb_20260926.sqlite3
  #   sha256=3b8809b2e57d2ab89c837fd45fd53ec1b64779d2b428bd352ddcd8f730a2a62d
  #   huggingface_url=https://huggingface.co/datasets/cbdb/cbdb-sqlite/resolve/main/history/cbdb_202609/cbdb_20260926.zip
  # ② 下载（本机 huggingface.co 不通 → 用镜像，见下）
  URL=$(curl -s .../latest.json | python3 -c "import json,sys;print(json.load(sys.stdin)['huggingface_url'])")
  curl -L --retry 3 -o cbdb.zip "${URL/huggingface.co/hf-mirror.com}"
  # ③ 校验 + 解压
  shasum -a 256 cbdb.zip        # 比对 latest.json 的 sha256
  unzip cbdb.zip                # 得到 cbdb_20260926.sqlite3
  # ④ 可选后处理（视图/外键/ADDRESSES）；脚本若硬编码 huggingface.co，需先替换成 hf-mirror.com
  python scripts/add_foreign_keys.py --db cbdb_20260926.sqlite3
  bash scripts/create_views.sh cbdb_20260926.sqlite3
  ```
  查询示例（`sqlite3` 直接跑）：`SELECT COUNT(*) FROM BIOG_MAIN;`、`SELECT c_personid,c_alt_name_chn FROM ALTNAME_DATA WHERE c_alt_name_chn LIKE '%王%' LIMIT 20;`、`SELECT * FROM BIOG_ADDR_DATA WHERE c_personid=100;`。表结构：`sqlite3 db '.schema BIOG_MAIN'`。
- 覆盖：以**唐代至清代**人物为主（含部分先秦—隋唐），人物量级数十万；字段/表说明见官方 docs。格式：SQLite3（另发布 `latest_ZZZ_tables.7z` 带反规范化表；`ZZZ` 系列已弃用，改由 `create_views.sh` 生成视图）。更新频率：**月度左右**（`generated_at_utc`，实测当前为 2026-09-26）；GitHub 仓里的 .db **已停更**，只认 HF 的 `latest.zip` / `history/`。
- 门槛：体积 ~133 MB（zip）→ 解压后数百 MB，注意磁盘与内存（大表 JOIN 慢，先建索引/视图）。**本机网络**：`huggingface.co` **不通**（实测 TCP 超时，HTTP 000）；**`hf-mirror.com` 可达**且能下载该 zip（实测 HEAD 302 → `cas-bridge.xethub.hf.co`，`content-length=139271640`；带 `-L` 的 Range 请求返回 **206** + 真实 zip 头 `PK`）。备选镜像：`modelscope.cn` 可达（有无 CBDB 副本未核实）。许可/引用：CBDB 数据有官方使用条款与引用要求（学术引用 CBDB + 版本日期）；仓内无 LICENSE 文件 → **以官方站点条款为准，勿直接再分发**。
- 实测：2026-10-02，macOS 27（arm64）。① `curl -s https://raw.githubusercontent.com/cbdb-project/cbdb_sqlite/master/latest.json` → **200**，字段如上（`cbdb_20260926.sqlite3` / sha256 `3b8809b2…a62d` / `generated_at_utc: 2026-09-26T19:14:20Z`）。② `gh api repos/cbdb-project/cbdb_sqlite` → `size=105 KB`、无 license 字段、`pushed_at=2026-09-26`；`releases` 为空。③ 网络：`curl -m 15 https://huggingface.co/` → **HTTP 000**（超时）；`curl -I https://hf-mirror.com/` → **200**；`curl -sIL …/${zip}` → 302 + `Content-Length: 139271640`；`curl -sL -r 0-511 …` → **206 / 512 字节**，`file` 识别为 **Zip archive**。
- 上游：`https://github.com/cbdb-project/cbdb_sqlite`
