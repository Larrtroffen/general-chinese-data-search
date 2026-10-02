# wechatspider —— 客户端抓包按号全量采集

本地私有工具，源码在 `~/Research_Assistant/wechatspider/`（macOS，Python ≥3.11，uv 管理）。
用途：在**本机已登录的微信桌面客户端**里打开目标公众号主页，从客户端流量里静默抓取会话凭据
（`key` / `pass_ticket` / `Cookies` / `poc_token` / `appmsg_token`），再调官方接口**按公众号枚举
历史文章、抓正文、取阅读与点赞数**，落 CSV / MySQL。

**与搜狗的互补关系**：搜狗微信（`weixin.sogou.com.md`）是**关键词索引子集**——只能搜到被索引的文章，
拿不到阅读数，且链接 token 时效极短；本工具按**公众号全量**拉取（含 2018 及更早的号内文章）+ **阅读/点赞数**，
但需要本机微信客户端在线、且每个号要在客户端里打开一次主页。

2026 年微信收紧接口后，「登录公众平台后台枚举任意公众号文章」的路线（`appmsgpublish` / `searchbiz`）
已被官方关闭；本工具走的是当前仍可用的**客户端会话凭据**链路（见 repo README「工作原理」）。

- 去哪找：本机 `~/Research_Assistant/wechatspider/`；入口 `wechatspider-capture`（抓包与凭据）、`wechatspider-pipeline`（一条命令跑完）；凭据库默认 `~/.wechatspider/credentials.json`。
- 什么时候用：要**按公众号全量**历史列表 + 正文 + **阅读/点赞数**时；有本机 macOS + 微信桌面客户端可人工配合时。
  **不可用**：无客户端 / 纯服务器环境。
- 怎么取：
  ```bash
  cd ~/Research_Assistant/wechatspider
  uv sync
  uv run wechatspider-capture ca --trust          # 生成并信任 mitmproxy CA（要管理员密码）
  uv run wechatspider-pipeline --account 中央政法委长安剑 --name-id changan-j \
      --number-id 1 --out changan.csv --readers
  ```
  结果形态：CSV / MySQL（可 `--sql-*` 落库）。
- 覆盖：公众号级（历史文章列表：标题/链接/封面/发布时间）+ 文章级（正文、阅读/点赞数）；多号排队；可落 CSV / MySQL（列表表 + `_details` 表）。
- 门槛：需 **macOS + 微信桌面客户端已登录 + 终端辅助功能权限 + mitmproxy CA**（本机私有工具，无公开 repo）
- 实测：2026-10-02——单测 `Ran 58 tests ... OK`（58 个全过）、环境已装；但**真实抓包链路本次未复现**（见「坑·未验证」）。
- 上游：本机私有工具，源码 `~/Research_Assistant/wechatspider/`（无公开 repo）

## 细节

### 可用性矩阵

| 能力 | 支持 | 实现 / 证据 |
|---|---|---|
| 历史文章列表 | ✅ | `profile_ext?action=getmsg`（JSON 模式，`f=json`），含标题/链接/封面/发布时间 |
| 文章正文 | ✅ | 抓 `/s?` 页 `rich_media_content` / `#js_content`(见 `get_content.py`) |
| 阅读/点赞数 | ✅ | `POST /mp/getappmsgext`（需有效 key；`appmsgstat=null` 时给修复提示） |
| 多号排队 | ✅ | `--accounts accounts.txt`，一次抓包会话轮流服务所有号 |
| 自动打开主页 | ✅（macOS） | `wechat_ui.py`：⌘F 搜索主页 URL → ↓ → Enter → 合成点击「访问网页」 |
| MySQL 落库 | ✅ | 列表表 + `_details` 表，建表 SQL 见 `save_to.create_sqltable` |
| 单测 | ✅ 58 个全过 | `uv run --no-sync python -m unittest discover -s tests -t .` → `Ran 58 tests ... OK` |
| Windows 抓包 | ⚠️ 遗留 | `get_par.py`（pywinauto + mitmdump）为旧路线，未在 macOS 验证 |
| 无客户端 / 纯服务器跑 | ❌ | 必须有本机微信客户端并提供会话；无客户端不可用 |

### 安装（uv）

```bash
cd ~/Research_Assistant/wechatspider
uv sync                      # 按 uv.lock 创建 .venv 并安装依赖
uv run python -m unittest discover -s tests -t .   # 跑测试（58 个）
```

依赖（`pyproject.toml`）：`requests` `beautifulsoup4` `pandas` `pymysql` `mitmproxy`，
以及 macOS 专有的 `pyobjc-framework-Quartz` / `pyobjc-framework-ApplicationServices`（合成键鼠事件用）。

一次性准备（需管理员密码；证书信任写入 `~/.mitmproxy/`）：

```bash
uv run wechatspider-capture ca --trust     # 生成并信任 mitmproxy CA
```

同时确认「辅助功能」权限：运行本工具的终端 App（Orca / iTerm / Terminal）需在
**系统设置 → 隐私与安全性 → 辅助功能**里勾选（自动打开主页要合成键鼠事件）。

CA 卸载：`sudo security remove-trusted-cert -d ~/.mitmproxy/mitmproxy-ca-cert.pem`

### CLI 1：`wechatspider-capture`（抓包与凭据）

入口 `wechatspider.capture_cli:main`。**全局 `--store` 写在子命令之前**：
`uv run wechatspider-capture --store /path/creds.json status`

| 子命令 | 参数 | 说明 |
|---|---|---|
| `ca` | `--trust` | 生成 mitmproxy CA；`--trust` 直接执行信任命令（要管理员密码） |
| `proxy-on` | `--port`（默认 8080） | 把各网络服务代理指向 mitmdump，并备份原配置 |
| `proxy-off` | — | 按备份恢复系统代理配置 |
| `run` | `--port`（8080）、`--upstream http://127.0.0.1:7890`、`--quiet` | 启动 mitmdump 抓包；`--upstream` 用于本机需经既有代理才能出网 |
| `status` | — | 查看已抓到的凭据（`[OK/fresh]` 表示可用于拉列表；`--` 标记的来自文章页） |
| `clear` | `--biz`（必填） | 删除某公众号的凭据 |

抓包取凭据（终端 A 保持前台；终端 B 查状态）：

```bash
# 终端 A
uv run wechatspider-capture proxy-on --port 8080
uv run wechatspider-capture run --port 8080
# 需经既有代理出网时：
#   uv run wechatspider-capture run --port 8080 --upstream http://127.0.0.1:7890
# 切到微信客户端：进入目标公众号 → 查看历史消息（主页），停留几秒
# 终端 B
uv run wechatspider-capture status
# 抓完 Ctrl-C 停止 run，再恢复代理：
uv run wechatspider-capture proxy-off
```

关键事实（代码已确认，决定流程设计）：

- **key 与公众号绑定**：`key`/`pass_ticket` 只在某个 `__biz` 的会话里有效，跨号调用必被拒（`ret=-3`）。
- **必须打开「公众号主页」**：只有 `/mp/profile_ext?action=home` 建立的会话才能拉列表；
  只打开某篇文章拿到的凭证以 `invalid_session` 被拒（`get_list.fetch_articles_page` 提前拦截）。
  来源标记 `profile_ext > article > other`，存储时**只升不降**（`credential.SOURCE_RANK`）。
- **key 寿命约 2 小时**：`credential.KEY_TTL_SECONDS = 2*60*60`；过期后 pipeline 自动重开主页续跑。
- **错误分类**（`errors.WeChatAccessError.kind`）：`blocked`（风控验证页）/ `invalid_session`
  （ret `-3/-4/-5/-6/200003`）/ `freq_control`（`200013`，冷却而非硬重试）/ `parse` / `network`。

凭据库：默认 `~/.wechatspider/credentials.json`，写入时 `os.chmod(tmp, 0o600)`；
可用环境变量 `WECHATSPIDER_CRED_FILE` 或 `--store` 改位置。

### CLI 2：`wechatspider-pipeline`（一条命令跑完）

入口 `wechatspider.pipeline:main`（也等价于 `uv run python -m wechatspider.pipeline`）。
自动：启动 mitmdump → 备份并接管系统代理 → 自动在微信里打开该号主页 → 检测到凭据立即翻页抓列表
→ 逐篇补正文 → `--readers` 时再抓阅读/点赞 → 退出时恢复代理、关闭 mitmdump。

```bash
uv run wechatspider-pipeline --account 中央政法委长安剑 --name-id changan-j \
    --number-id 1 --out changan.csv --readers
```

完整参数（逐项来自 `pipeline.build_parser`）：

| 参数 | 默认 | 说明 |
|---|---|---|
| `--account` | — | 公众号显示名（写入 CSV `account` 列） |
| `--name-id` | — | 公众号标识（写入 CSV `name_id` 列） |
| `--number-id` | 1 | 自定义编号 |
| `--biz` | — | 目标 `__biz`；省略则采用抓到的第一个可用凭据 |
| `--accounts FILE` | — | 多号排队清单，每行 `name_id,account[,number_id[,biz]]`，`#` 为注释 |
| `--out` | `wechat_articles.csv` | CSV 输出；多号可用 `{name_id}` 占位，如 `data/{name_id}.csv` |
| `--store` | `~/.wechatspider/credentials.json` | 凭据库路径 |
| `--pages` | 300 | 最多翻多少页（每页 10 篇） |
| `--end-time` | `0` | 截止时间 `YYYY-MM-DD`（抓到更早的即停止） |
| `--interval` | 1.5 | 翻页间隔秒数 |
| `--queue-delay` | 3.0 | 两个号之间的间隔秒数 |
| `--no-content` | off | 只抓列表，不补正文 |
| `--readers` | off | 抓阅读/点赞（较慢） |
| `--reader-interval` | 2.2 | 阅读数请求间隔秒数 |
| `--reader-start` | 0 | 阅读数从第几条开始（续跑用） |
| `--capture-timeout` | 600 | 等待凭据的超时秒数 |
| `--port` | 8080 | mitmdump 端口 |
| `--upstream` | — | 抓包时链路到已有代理，如 `http://127.0.0.1:7890` |
| `--no-proxy` | off | 不修改系统代理（自行配置代理时用） |
| `--no-capture` | off | 跳过抓包，直接用凭据库中已有的凭据 |
| `--no-auto-open` | off | 不自动让微信打开主页（改为人工打开） |
| `--refresh` | off | 强制重新抓一次凭据（不复用旧凭据） |
| `--click-offsets` | `166,200,235,270,305` | 自动点击「访问网页」的候选纵向偏移，逗号分隔 |
| `--per-click-timeout` | 25 | 每次自动点击后等待凭据的秒数 |
| `--sql-table/--sql-host/--sql-user/--sql-password/--sql-db` | — | MySQL 输出（列表+正文+阅读数） |
| `--sql-port` / `--sql-charset` | 3306 / `utf8` | MySQL 端口与字符集 |

#### 多号排队

`accounts.txt`：

```
changan-j,中央政法委长安剑,1,MzkxNzUxOTU0MA==
rmfyb,人民法院报,2,MjM5OTI0MzU4NQ==
```

```bash
uv run wechatspider-pipeline --accounts accounts.txt --out 'data/{name_id}.csv' --readers
```

对每个号自动在微信里打开该号主页，拿到凭据后立刻开爬，再自动切下一个号。点击位置随「搜一搜」
页面状态上下浮动，脚本按 `--click-offsets` 逐个候选偏移尝试，**以「凭据是否抓到」为成功判据**，
所以不需要精确坐标。`biz`（`__biz`）可从任意一篇该号文章链接里取 `__biz=` 参数。

### 接口与解析要点（源码确认）

列表接口（`get_list.py`）——`GET https://mp.weixin.qq.com/mp/profile_ext`，参数：

```
action=getmsg & __biz=… & f=json & offset=N & count=10 & is_ok=1 & scene=124
& uin=base64(wxuin) & key=… & pass_ticket=… & wxtoken=… & poc_token=… & x5=0
```

- 请求头带客户端原始 UA（兜底 Chrome 131 macOS UA）+ `Cookie`；默认 `NO_PROXY`（抓包期间避免二次代理）。
- 响应优先按 JSON 解析 `general_msg_list`（字段 `comm_msg_info.datetime`、`app_msg_ext_info.title/content_url/cover`）；
  HTML 形态（`var msgList = '…'`）作兜底，`&quot;` 先 unescape 再 json。
- 风控页特征：HTTP 200 + 含 `环境异常`/`去验证`/`weui-msg`/`wx_alert` 等 → `blocked`。
- 分类：`can_msg_continue` 控制翻页；`ret=0` 但无 `general_msg_list` → `invalid_session`。

阅读数（`get_details.py`）——`POST https://mp.weixin.qq.com/mp/getappmsgext`：

- 有 `appmsg_token` 时用新形态 `?appmsg_token=…&x5=0`，`__biz/mid/sn/idx` 放 body；
  否则退回旧形态 `?uin=…&key=…&__biz=…`（`mid/sn/idx` 作 query）。
- body 必带 `is_only_read=1`（否则拿不到 `like_num`）、`appmsg_type=9`。
- `appmsgstat` 含 `read_num` / `like_num` / `old_like_num`；为 `null` 说明 key 过期或该号无文章页会话。
- `mid/sn/idx/__biz` 从文章 URL 用 `urlparse`+`parse_qs` 解析（旧正则对 URL 末尾参数会崩，已修）。

正文（`get_content.py`）：`GET` 文章 URL，UA 用现代桌面浏览器（Chrome 131 macOS）——python-requests
默认 UA 与旧版微信内置浏览器 UA（MicroMessenger/6.5.2）会触发风控验证页（`wappoc_appmsgcaptcha`/「环境异常」）。
正文节点 `.rich_media_content` 或 `#js_content`；取纯文本，`\u3000` 去掉、空行去掉。
CSV 增量补正文时失败行保持空以便重试（`update_csvcontent`）。

MySQL 建表（`save_to.create_sqltable`，表名 `{name}` 与 `{name}_details`）：

```sql
-- 列表+正文
CREATE TABLE IF NOT EXISTS {name} (
  name_id CHAR(25) NOT NULL, account CHAR(50) NOT NULL, number_id INT NOT NULL,
  time BIGINT NOT NULL, title MEDIUMTEXT NOT NULL, url MEDIUMTEXT, cover MEDIUMTEXT,
  num TINYINT NOT NULL, headline TINYINT NOT NULL, content MEDIUMBLOB,
  id INT AUTO_INCREMENT, PRIMARY KEY(number_id, num, time), KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
-- 阅读数
CREATE TABLE IF NOT EXISTS {name}_details (
  number_id INT NOT NULL, time BIGINT NOT NULL, num TINYINT NOT NULL,
  title MEDIUMTEXT NOT NULL, readers INT NOT NULL, likes INT NOT NULL,
  old_likes INT NOT NULL, id INT AUTO_INCREMENT,
  PRIMARY KEY(number_id, num, time), KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### Python API（脚本内调用）

```python
from wechatspider.credential import CredentialStore
from wechatspider import history, information, save_to

store = CredentialStore()                      # 读 ~/.wechatspider/credentials.json
target = information.target('changan-j', '中央政法委长安剑', 1, '<__biz>')
save_target = information.file('changan-j.csv')
history.full_history(None, target, save_target, store=store, save_to='csv',
                     threshold=300, page=0, end_time=0)   # 传 store 时 user 可省略

from wechatspider import reader_like
reader_like.reader_likes(0, df, save_to='csv', name=save_target,
                         cred=store.get('<__biz>'), sn=2.2)
```

### 系统代理接管（`macos_proxy.py`）

`proxy-on` 用 `networksetup` 逐个网络服务设置 HTTP/HTTPS 代理指向 mitmdump，并把原 HTTP/HTTPS 代理与
PAC 状态完整备份到 `~/.wechatspider/proxy-backup.json`；`proxy-off` 按备份恢复（未备份的服务则关闭代理）。
配置变更需管理员权限：先直接执行，失败后试 `sudo -n`（免密），再失败抛错提示 `sudo -v`。
**异常退出后务必手动 `uv run wechatspider-capture proxy-off`**，否则系统代理挂在 mitmdump 上。

### 状态证据（2026-10-02 实测）

本会话实际执行过的命令与结果：

| 检查 | 命令 | 结果 |
|---|---|---|
| 单测数量与通过 | `uv run --no-sync python -m unittest discover -s tests -t .` | `Ran 58 tests in 1.027s` → `OK`（README 称 58 个，**核实为 58**） |
| 测试函数计数（静态） | AST 统计 `tests/test_*.py` 中 `test_*` 函数 | 58 个（capture 10 / credential 12 / get_list 12 / pipeline 9 / wechat_ui 15） |
| git 提交 | `git log -1` | `9bcc263 2026-10-02 feat: 微信公众号采集工具（macOS 客户端凭据路线）`（当前 HEAD） |
| 依赖环境 | `ls .venv/bin` | `.venv` 存在，含 `mitmdump`/`mitmproxy`/`python` 等，依赖已装 |
| uv | `which uv` | `/opt/homebrew/bin/uv` |
| 凭据库是否已用过 | `test -e ~/.wechatspider` | **不存在**——本机尚未完成过一次真实凭据抓取（工具从未端到端跑过） |

## 坑

- **仅 macOS**：自动打开主页依赖 Quartz 合成键鼠 + `networksetup`；Windows 路线（`get_par.py`）遗留、未验证。
- **必须微信客户端已登录并运行**（`wechat_ui.is_running()` 以 `pgrep -f MacOS/WeChat` 判定）。
- **每个号都要在客户端打开一次主页**才能拿列表凭据；只有文章页凭据会 `invalid_session`。
- **key ~2h 过期**；`--no-capture` 复用旧凭据前先用 `status` 确认 `[fresh]`。
- **频控**：`ret=200013` 会直接中止（不硬重试），需冷却数十分钟到数小时；默认翻页 1.5s、阅读数 2.2s。
- **合规**：采集的是自己账号可见的公开内容；抓包 + 高频请求存在账号被风控风险，出现频控立即停手。
  卸载 CA（见上）并确认系统代理已恢复。
- 自动点击没反应：搜一搜页面布局变化 → 调 `--click-offsets` 或 `--no-auto-open` 手动打开。

### 未验证（需人工操作微信客户端，本次未执行）

- 真实抓包链路：CA 信任、系统代理接管、客户端打开主页后能否抓到凭据——**未验证**。
- 自动打开主页的点击偏移在本机当前微信版本是否命中——**未验证**（代码注释标为「本机实测标定」，但本次未复现）。
- `profile_ext?action=getmsg` / `getappmsgext` 在 2026-10 的真实可用性、阅读数是否仍返回——**未验证**。
  以上需运行 `wechatspider-pipeline` 并人工配合打开公众号主页后方可确认。
