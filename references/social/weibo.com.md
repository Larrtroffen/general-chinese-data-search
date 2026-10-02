# weibo.com —— 热搜匿名可取，检索需登录

微博是舆情/事件传播的补充源，但**搜索、话题、用户时间线全部需要登录态**。本机（无登录 cookie）实测：唯一可匿名直取的公开数据是**热搜榜 JSON**（`weibo.com/ajax/side/hotSearch`，且**必须带 Referer**）。

- 去哪找：
  - 热搜榜 JSON `https://weibo.com/ajax/side/hotSearch`（需 `Referer: https://weibo.com/`）；
  - 桌面搜索页 `https://s.weibo.com/weibo?q={kw}`、移动搜索 API `https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D{kw}&page_type=searchall`（均需登录）；
  - 访客系统 `https://passport.weibo.com/visitor/genvisitor`、`.../visitor?a=incarnate`。
- 什么时候用：要**当前**微博热搜榜（事件热度、词条）；要事件传播/民间讨论的补充线索（须登录后检索）。
- 怎么搜：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'

  # ① 唯一匿名可用：热搜榜（Referer 必须，否则 403）
  curl -s -m 20 -A "$UA" -H 'Referer: https://weibo.com/' 'https://weibo.com/ajax/side/hotSearch' \
    | python3 -c "import sys,json;d=json.load(sys.stdin);print([(x['realpos'],x['word'],x['num']) for x in d['data']['realtime'][:5]])"

  # ② 访客 cookie 握手（登不上，仅记录流程）
  J=/tmp/wb.txt
  TID=$(curl -s -A "$UA" -c $J -b $J 'https://passport.weibo.com/visitor/genvisitor' \
        -H 'Referer: https://passport.weibo.com/visitor/visitor' -X POST \
        --data-urlencode 'cb=gen_callback' \
        --data-urlencode 'fp={"os":"1","browser":"Chrome124,0,0,0","fonts":"undefined","screenInfo":"1920*1080*24","plugins":""}' \
        | python3 -c "import sys,json,re;print(json.loads(re.search(r'\{.*\}',sys.stdin.read(),re.S).group(0))['data']['tid'])")
  curl -s -A "$UA" -b $J -c $J -o /dev/null -w '%{http_code}\n' \
    "https://passport.weibo.com/visitor/visitor?a=incarnate&t=$TID&w=2&c=095&gc=&cb=cross_domain&from=weibo&_rand=0.123456"

  # ③ 搜索（无登录 cookie 必失败）
  curl -s -m 20 -A "$UA" -H 'X-Requested-With: XMLHttpRequest' -H 'Referer: https://m.weibo.cn/' \
    'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D%E8%A1%97%E4%B9%A1%E5%90%B9%E5%93%A8&page_type=searchall'
  # → {"ok":-100,"url":"https://passport.weibo.com/sso/signin?…"}
  ```
  结果形态：热搜榜 **JSON**；搜索（需登录）JSON。
- 覆盖：热搜榜 51 条**当前**榜（`data.realtime`，同榜位还有 `hotgov`/`hotgovs` 要闻位）；**无历史回溯**；检索（需登录）为微博正文卡，粒度/翻页受登录态限制。
- 门槛：热搜榜无登录（但**必须带 `Referer`**）；**检索需真实登录 cookie**（访客 cookie 不足）
- 实测：2026-10-02，macOS（arm64），curl 8.x（`-m 20`，桌面/iPhone UA，同主机间隔 ≥1.5s）：`weibo.com/ajax/side/hotSearch`（带 Referer）→ 200/21667 B，`ok:1`，`realtime` 51 条，`realtime[0]="Hero战胜AG"`（num=1053704）；不带 Referer → 403/21 B；`weibo.com/ajax/side/search?q=街乡吹哨` → 200 但各数组为空；`s.weibo.com/weibo?q=街乡吹哨` → 302 visitor；`s.weibo.com/top/summary?cate=realtimehot` → 302 visitor；`m.weibo.cn/` → 302 `visitor.passport.weibo.cn`；`m.weibo.cn/api/container/getIndex?...searchall` → 200 `{"ok":-100,…}`（裸请求、带访客 jar、带手工 `SUB` 三种情况结果相同）；`genvisitor`/`incarnate` 均 200 `retcode:20000000`。
- 上游：https://weibo.com/

## 细节

### 可用性矩阵（本机实测 2026-10-02，macOS + curl）

| 通道 | URL | 状态 | 现象 |
|---|---|---|---|
| 热搜榜 JSON | `https://weibo.com/ajax/side/hotSearch`（带 `Referer: https://weibo.com/`） | ✅ 200 | 21667 B JSON，`{"ok":1,"data":{"realtime":[51 条], "hotgov":[…], "hotgovs":[…]}}`，**无需登录** |
| 同上但不带 Referer | 同 URL | ❌ 403 | 21 B `{"error":"Forbidden"}` → **Referer 必需** |
| 桌面搜索页 | `https://s.weibo.com/weibo?q={kw}` | ❌ 302 | → `https://passport.weibo.com/visitor/visitor?entry=miniblog&a=enter&url=…`（`SIZE=0`） |
| 桌面热搜榜页 | `https://s.weibo.com/top/summary?cate=realtimehot` | ❌ 302 | 同上 visitor 跳转 |
| 移动首页 | `https://m.weibo.cn/` | ❌ 302 | → `https://visitor.passport.weibo.cn/visitor/visitor?entry=sinawap&…` |
| 移动搜索 API | `https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D{kw}&page_type=searchall` | ❌ | HTTP **200** 但 body = `{"ok":-100,"url":"https://passport.weibo.com/sso/signin?entry=wapsso&source=wapssowb&…"}` → **需登录** |
| 搜索联想 | `https://weibo.com/ajax/side/search?q={kw}` | ⚠️ 200 | `{"ok":1,"data":{"hotquery":[],"history":[],"real_hot":[],"query_relates":[],"user":[],"users":[]}}` —— 全空数组，**拿不到检索结果** |
| 访客系统·取 tid | `POST https://passport.weibo.com/visitor/genvisitor`（`cb=gen_callback` + `fp={…}`） | ✅ 200 | `gen_callback({"retcode":20000000,"msg":"succ","data":{"tid":"01AZ8_PWqOc7V-L2UAbmtUrQJIH15i2awPGX5MVH7zPe9s","new_tid":true}})` |
| 访客系统·换 cookie | `GET https://passport.weibo.com/visitor/visitor?a=incarnate&t={tid}&w=2&c=095&gc=&cb=cross_domain&from=weibo&_rand=…` | ✅ 200 | `cross_domain({"retcode":20000000,…,"data":{"sub":"_2AkMd…","subp":"0033WrSXqPxfM72-Ws9jqgMF5…"}})`；cookie jar 只落 `SUBP`/`SRF`/`SVB` |

**结论**：访客（visitor）体系只给 `SUBP`/`SUB`，**不足以检索** —— 把 `incarnate` 返回的 `sub` 手工种成 `.weibo.cn` 的 `SUB` cookie 后，`searchall` 仍 `ok:-100`。微博检索必须**真实登录 cookie**。

### 解析要点

- 热搜 JSON（✅ 实测结构）：`data.realtime[]` 共 51 条，条目字段 `word`（词条）、`num`（热度值）、`realpos`（榜位）、`rank`、`label_name`/`icon_desc`（「新」「热」等标记）、`word_scheme`（话题式词条）、`topic_flag`、`flag`、`note`；同级还有 `data.hotgov`/`data.hotgovs`（要闻位）。
- 搜索接口（有登录态时）返回 `data.cards[]`，`card_type=9` 为微博正文卡（`mblog.text` 含 HTML `<a>` 话题标签）——**本机未取得登录态，未实际观察，标注为未验证**。
- 移动搜索 `containerid` 形式：`100103type%3D1%26q%3D{urlencoded_kw}`（`type=1` 综合；其他 `type` 未验证）。

## 坑

1. **别指望匿名检索**：`s.weibo.com` 一律 302 进 visitor 系统；拿到访客 cookie 后仍 302。`m.weibo.cn` 返回的是 **HTTP 200 + `ok:-100` 的登录跳转 JSON** —— 只看状态码会误判「接口可用」。
2. `weibo.com/ajax/side/hotSearch` **必须带 `Referer: https://weibo.com/`**（本机不带即 403 `{"error":"Forbidden"}`）。
3. 访客 `incarnate` 返回的 `sub` 在 **JSON body** 里，curl `-c` 只落 `SUBP/SRF/SVB`；别据此判断「cookie 没拿到」。
4. 时间过滤/翻页参数（`page`、`since_id`）在无登录态下无法验证；热搜接口**只给当前榜，无历史回溯**。
5. 合规与稳定性：微博 ToS 限制自动化抓取；账号 cookie 会过期、高频调用触发风控。长周期语料**不要**以微博为主通道。
6. 未验证：登录 cookie 下 `searchall` 的实际可用性（本次无账号，未试）；`api.weibo.com`（需 App Key）；`s.weibo.com/weibo?q=` 带真实登录 cookie 是否直接可读。
