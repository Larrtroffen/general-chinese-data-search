# cnipa.gov.cn —— 专利与商标检索公告入口

- 去哪找：
  - 国家知识产权局官网：`https://www.cnipa.gov.cn/`（通知公告、政策法规、统计、各检索库**入口总表**）
  - 国家知识产权公共服务平台：`https://ggfw.cnipa.gov.cn/`（公共服务机构/本地库/专利导航等入口）
  - 专利查询（公众）：`https://cpquery.cponline.cnipa.gov.cn/`
  - 专利检索及分析系统：`https://pss-system.cponline.cnipa.gov.cn/`
  - 专利公布公告：`http://epub.cnipa.gov.cn/`
  - 商标局：`https://sbj.cnipa.gov.cn/`；商标网上检索：`https://wcjs.sbj.cnipa.gov.cn/`
  - 商标公告（公开）：`https://pub.sbj.cnipa.gov.cn/toas-pub-prod/portalui-pub-prod/systemJumpPage`（走 `sso.cnipa.gov.cn` 登录）
  - 智能问答：`https://znwd.cnipa.gov.cn/`（业务问答，非检索库）
- 什么时候用：
  - 关键词：企业名 / 发明人 / 申请人 → **该主体的专利**（专利查询 cpquery、检索分析 pss-system）。
  - 关键词：专利号 / 申请号 / 公开号 → 专利著录项、法律状态、公布公告全文（epub）。
  - 关键词：企业名 → **该主体的商标**（商标公告 pub.sbj、商标检索 wcjs.sbj）。
  - 关键词：商标名称/注册号 → 商标公告（初审公告、注册公告、异议）。
  - 关键词：地理标志产品/专用标志企业 → ggfw 的 `dbQuery` / `zybzqyQuery`。
  - 不适用：论文/期刊（去 `../academic/`）；企业工商与信用（去 `gsxt.md`、`credit-china.md`）。
- 怎么搜：
  - **可用姿势 1：官网通知公告（200，可 curl）**
    ```bash
    UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    curl -sS -m 20 -A "$UA" -H 'Accept-Language: zh-CN,zh;q=0.9' 'https://www.cnipa.gov.cn/' \
      | grep -oE 'https://www\.cnipa\.gov\.cn/(art|col)/[^"]+' | head
    ```
    结果形态：静态 HTML（UTF-8），栏目页/文章页均为服务端渲染，**可直接抓取与入库**。文章/公告 URL 规律：`https://www.cnipa.gov.cn/art/<年>/<月>/<日>/art_<栏目id>_<文章id>.html`；栏目标签页 `https://www.cnipa.gov.cn/col/col<栏目id>/index.html`。
  - **可用姿势 2：公共服务平台（200，SPA）**
    ```bash
    curl -sS -m 20 -A "$UA" 'https://ggfw.cnipa.gov.cn/'            # 200 SPA 壳
    curl -sS -m 20 -A "$UA" 'https://ggfw.cnipa.gov.cn/env.js'      # 运行时配置（接口基址）
    ```
    结果形态：SPA 壳 + JS 渲染（该站同样挂了瑞数 `$_ts`，数据接口需浏览器；`/publish/data/page/front` 疑为 CMS 内容接口，未验证）。前端路由（由 `/js/app.c26fce5a.js` 反查）：`/local-database-query`、`/local-platforms-query`、`/public-service-org-query`（+`/map`）、`/publish/data/list/gateway`、`/publish/data/page/front`；运行时配置在 `/env.js`。
  - **须浏览器 / 登录的检索库（本机 CLI 不可用）**：
    - 专利公布公告 `http://epub.cnipa.gov.cn/`：本机首探 **202**（body 含 `$_ts=window['$_ts']` 瑞数脚本），随后 **000 超时**。上游声明其检索为 `POST /patentoutline.action`（未实测，仅作占位参考，勿直接依赖）。
    - 专利检索及分析系统 `pss-system.cponline.cnipa.gov.cn`：**412**；且**须注册账号登录**才能检索。
    - 专利查询（公众）`cpquery.cponline.cnipa.gov.cn`：**412**（瑞数）。
    - 商标局 / 商标网上检索 / 商标公告 `sbj` 系：https 超时、http 403；商标公告公开平台走 `sso.cnipa.gov.cn` OAuth 登录，**须实名账号**。
- 覆盖：官网覆盖政策法规、通知公告、统计年报、专利/商标/地理标志各库入口（全国、历年）；专利 `pss-system` 为全量（1985 年至今发明专利/实用新型/外观设计）、`epub` 为公布公告全文、`cpquery` 为公众查询（著录项+法律状态），粒度=单件专利，动态更新（每周公布日）；商标 `pub.sbj` 商标公告（初审/注册/异议/无效等）+ `wcjs.sbj` 近似检索，粒度=单件商标。
- 门槛：官网/公共服务平台**免费免登录**；专利与商标**专用检索库需注册登录**（部分免登录但须过 WAF）。
- 实测：2026-10-03，macOS，curl 8.x，Chrome 126 UA，`Accept-Language: zh-CN`。`GET https://www.cnipa.gov.cn/` → **200**，10 954 B，`<title>国家知识产权局</title>`（首页含全部检索库外链）；`GET https://ggfw.cnipa.gov.cn/` → **200**，3 052 B（body 含瑞数 `$_ts`）；`GET …/js/app.c26fce5a.js` → **200**，268 379 B；`GET https://cpquery.cponline.cnipa.gov.cn/` → **412**，2 439 B；`GET https://pss-system.cponline.cnipa.gov.cn/` → **412**，2 455 B；`GET http://epub.cnipa.gov.cn/` → 首探 **202**（2 683 B，含 `$_ts`），再探 **000**（20 s 超时）；`GET https://sbj.cnipa.gov.cn/` 及 `/trademark-query`、`/sbj/sbcx/` → **000**（20 s 超时），`http://sbj.cnipa.gov.cn/` → **403**，1 998 B；`GET https://wcjs.sbj.cnipa.gov.cn/` → **403**，968 B；`GET https://pub.sbj.cnipa.gov.cn/toas-pub-prod/portalui-pub-prod/systemJumpPage` → **403**，996 B；`GET https://znwd.cnipa.gov.cn/` → **200**，33 014 B，`<title>智能问答平台</title>`；`GET http://epub.sipo.gov.cn/`（旧域名）→ **000** DNS 解析失败（已下线）；`GET http://pss-system.cnipa.gov.cn/` → **000** DNS 解析失败。
- 上游：<https://www.cnipa.gov.cn/>、<https://ggfw.cnipa.gov.cn/>、<http://epub.cnipa.gov.cn/>、<https://pss-system.cponline.cnipa.gov.cn>、<https://cpquery.cponline.cnipa.gov.cn/>、<https://sbj.cnipa.gov.cn/>、<https://pub.sbj.cnipa.gov.cn/toas-pub-prod/portalui-pub-prod/systemJumpPage>、<https://sso.cnipa.gov.cn/oauth2/authorize>

## 细节

本卡区分"CLI 可达"与"须浏览器+登录"两类站点：

| 站点 | URL | 用途 | 本机 CLI（2026-10-03） |
|---|---|---|---|
| 国家知识产权局官网 | `https://www.cnipa.gov.cn/` | 通知公告、政策法规、统计、各检索库**入口总表** | ✅ **200** |
| 国家知识产权公共服务平台 | `https://ggfw.cnipa.gov.cn/` | 公共服务机构/本地库/专利导航等**公共服务**入口 | ✅ **200**（SPA） |
| 专利查询（公众） | `https://cpquery.cponline.cnipa.gov.cn/` | 专利著录/法律状态检索 | ❌ 412（WAF） |
| 专利检索及分析系统 | `https://pss-system.cponline.cnipa.gov.cn/` | 全量专利检索分析 | ❌ 412；**须注册登录** |
| 专利公布公告 | `http://epub.cnipa.gov.cn/` | 专利公布/公告全文（对外免费） | ❌ 202→超时（瑞数 WAF） |
| 商标局 | `https://sbj.cnipa.gov.cn/` | 商标业务/查询入口 | ❌ https 超时 / http 403 |
| 商标网上检索 | `https://wcjs.sbj.cnipa.gov.cn/` | 商标近似检索 | ❌ 403 |
| 商标公告（公开） | `https://pub.sbj.cnipa.gov.cn/toas-pub-prod/portalui-pub-prod/systemJumpPage` | 商标公告/异议/注册公开 | ❌ 403；走 `sso.cnipa.gov.cn` 登录 |
| 智能问答 | `https://znwd.cnipa.gov.cn/` | 业务问答（非检索库） | ✅ 200 |

官网首页外链（实测抓取）：

```
https://cpquery.cponline.cnipa.gov.cn/                      # 专利查询
https://pss-system.cponline.cnipa.gov.cn                    # 专利检索及分析系统
http://epub.cnipa.gov.cn/                                   # 专利公布公告
https://sbj.cnipa.gov.cn/  /sbj/sbcx/  /sbj/wssq/  /trademark-query
https://pub.sbj.cnipa.gov.cn/toas-pub-prod/portalui-pub-prod/collectionButtons
https://pub.sbj.cnipa.gov.cn/toas-pub-prod/portalui-pub-prod/systemJumpPage
https://ggfw.cnipa.gov.cn/  （/dlbzsq/dbQuery 地理标志产品查询、/dlbzsq/zybzqyQuery 专用标志企业查询）
https://sso.cnipa.gov.cn/oauth2/authorize?...               # 统一登录（商标业务）
https://tzwh.sbj.cnipa.gov.cn/sbj/sbdl/                     # 商标代理
```

## 坑

1. 三个检索库（cpquery / pss-system / epub）均受瑞数 WAF 限制，pss-system 还需注册登录。
2. 商标系站点 https 超时、http 403，公开平台须经 `sso.cnipa.gov.cn` 实名登录。
3. 旧域名 `epub.sipo.gov.cn`、`pss-system.cnipa.gov.cn` 已下线（DNS 不解析）。
