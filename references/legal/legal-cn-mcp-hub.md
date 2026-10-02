# legal-cn-mcp-hub —— 中国法律 MCP 连接器中心

把多个官方/商业法律源封装成 MCP 的"连接器中心"（MIT）。对我们最有用的是它**逆向出的人民法院案例库（rmfyalk）HTTP API**——这是裁判文书网匿名不可用后的**案例**关键替代通道（需 token）。另含 flk 法规连接器、元典/北大法宝/飞书连接器。

- 去哪找：`https://github.com/hygiene-12/legal-cn-mcp-hub`
  - 关键文件：`servers/rmfyalk/scripts/server.py`（案例库）、`servers/flk-npc/scripts/server.py`（法规库）、`servers/rmfyalk/.env.example`、`PLATFORM_SPEC.md`、`connectors/{yuandian,pkulaw,feishu}.ps1`
- 什么时候用：
  - **要案例**（指导性案例 / 参考性案例，含裁判要点、基本案情、裁判理由、裁判文书正文）→ rmfyalk 逆向 API。
  - 要一个"免自行逆向"的 flk 法规检索 MCP 封装。
  - 要元典/法宝等多源 MCP 的连接器配置样例。
- 怎么取：
  ```bash
  git clone https://github.com/hygiene-12/legal-cn-mcp-hub
  pip install -r legal-cn-mcp-hub/servers/rmfyalk/requirements.txt
  RMFYALK_TOKEN='<浏览器抄的 faxin-cpws-al-token>' \
    python legal-cn-mcp-hub/servers/rmfyalk/scripts/server.py   # MCP，streamable-http
  # 裸调示例：
  curl -s -H 'faxin-cpws-al-token: <TOKEN>' -H 'Content-Type: application/json' \
    -H 'Referer: https://rmfyalk.court.gov.cn/view/list.html' \
    -X POST --data '{"page":1,"size":10,"lib":"qb","searchParams":{"keyTitle":["专利权"],"selectValue":["qw"],"userSearchType":2,"isAdvSearch":"0","lib":"cpwsAl_qb"}}' \
    'https://rmfyalk.court.gov.cn/cpwsAl/search'
  ```
- 覆盖：rmfyalk（官方标称收录 5500+ 篇指导性/参考性案例）；flk 法规库。
- 门槛：
  - rmfyalk **必须有登录 token**，会过期，需重抄；作者称"公开 API / 干净室实现"，非官方文档。
  - 匿名不可用；未见验证码/滑块说明，长跑可能被限流。
  - 本机无账号，**接口真实性未本机验证**（仅验证了匿名失败路径）。
- 实测：2026-10-02，macOS，curl 8.x。① `GET https://rmfyalk.court.gov.cn/` → **HTTP 200**，8,540 B（首页可达）。② 匿名 `POST /cpwsAl/search`（上述 body）→ **HTTP 500**（缺 token，Tomcat 500 页）。③ 匿名 `GET /enum/cpws_fyjb_id.xml` → **HTTP 500**；匿名 `POST /cpwsAl/content` → **HTTP 500**。④ 带 token 的成功路径 **未本机实测**（无账号）。
- 上游：`https://github.com/hygiene-12/legal-cn-mcp-hub`（MIT）

## 细节

### rmfyalk（人民法院案例库）逆向 API

| 项 | 值 |
|---|---|
| Base | `https://rmfyalk.court.gov.cn/` |
| 鉴权 | 请求头 **`faxin-cpws-al-token: <值>`**（登录 rmfyalk → F12 → Cookie/请求头抄取）；env `RMFYALK_TOKEN`。**不是** URL 参数 |
| 检索 | `POST /cpwsAl/search`，JSON body `{"page":1,"size":10,"lib":"qb","searchParams":{…}}` |
| 详情 | `POST /cpwsAl/content`，body `{"gid": <cpws_al_id>}` |
| 统计 | `POST /cpwsAl/statistics`（按年份/法院/案由分布） |
| 枚举 | `GET /enum/<xml>`：`cpal_sort_new1_id.xml`（案由）、`cpal_casesort_id.xml`（案件类型）、`cpws_fyjb_id.xml`（法院级别）、`cpal_slcx_id.xml`（审理程序）、`cpal_fcourt_id.xml`（法院）、`cpal_wsxz_id.xml`（文书类型） |
| 案例类型 `lib` | `cpwsAl_qb`=全部 / `cpwsAl_zx`=指导性 / `cpwsAl_ck`=参考性 |
| `searchParams` | `keyTitle[]`、`selectValue[]`（`qw`=全文 / `title`=标题 / `albh`=案例编号）、`isAdvSearch`(`"0"`/`"1"`)、`lib`、`sort_field`；高级字段键：`cpws_al_no`（案例编号，如 2021-18-2-160-001）、`cpws_al_ajzh`（案号）、`keyContent`、`keyword_cpwsAl`、`sort_id_cpwsAl`、`case_sort_id_cpwsAl`、`fyjb_id_cpwsAl`、`slcx_id_cpwsAl`、`slfy_id_cpwsAl`、`wslx_id_cpwsAl` |
| 返回 | `code=0` 成功（`401`=token 失效）；检索 `data.resultList[] / totalCount`；详情 `data` 含 `cpws_al_id / cpws_al_title / cpws_al_ajzh / cpws_al_no / cpws_al_zs_date / cpws_al_fy / cpws_al_sort / cpws_al_slcx / cpws_al_wsxz / cpws_al_content`（正文 HTML） |
| 请求头 | `Content-Type: application/json`、`Referer: https://rmfyalk.court.gov.cn/view/list.html`、`Origin: https://rmfyalk.court.gov.cn` |

flk 连接器（同 repo）：`API_BASE=https://flk.npc.gov.cn/law-search/`，调用 `search/list`、`flfgDetails`、`search/hitDisplay`、`prompts/search`、`enumData`、`download/pc` 等，与 `flk.npc.gov.cn.md` 一致。
