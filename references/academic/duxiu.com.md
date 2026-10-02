# duxiu.com —— 读秀图书与章节检索

超星系图书发现系统。**本机 IP 不在服务范围内，一切入口强制跳登录页，不可匿名抓取。**

- 去哪找：`https://www.duxiu.com/`；检索 `https://www.duxiu.com/search?sw={关键词}`；登录页 `https://www.duxiu.com/login.jsp`
- 什么时候用：要读秀的图书/章节检索；有机构账号或读秀卡时取图书章节
- 怎么搜：无匿名通道——入口一律 302 到 `login.jsp?backurl=…`；有权限时走机构账号/CARSI 登录（登录页提供"机构用户/读秀卡/个人用户/CARSI"四类入口），或图书馆代理 IP
- 覆盖：读秀图书/章节检索；全文/章节阅读需机构账号或读秀卡且 IP 在授权范围
- 门槛：须 IP 白名单或机构账号/CARSI 登录（非授权 IP 一律登录墙）
- 实测：2026-10-02，macOS + curl 8.x（desktop UA）：
  - `GET https://www.duxiu.com/` → 最终 `url=https://www.duxiu.com/login.jsp`，`HTTP 200 size=18767`，正文含"系统登录 / 机构用户 / 读秀卡用户 / 个人用户 / CARSI登录 / 当前机器ip：114.253.37.92 对不起，您当前的IP不在我们服务的范围内，请使用账号进行登录。"
  - `GET https://www.duxiu.com/search?sw=基层治理` → 最终 `url=https://www.duxiu.com/login.jsp?backurl=…book.duxiu.com%2Fsearch%3Fsw%3D…`
- 上游：`https://www.duxiu.com/`

## 细节

| 入口 | 状态 | 现象 |
|---|---|---|
| `https://www.duxiu.com/` | ❌→登录 | 200 但 302 落到 `https://www.duxiu.com/login.jsp`，正文含"对不起，您当前的IP不在我们服务的范围内，请使用账号进行登录。" |
| `https://www.duxiu.com/search?sw=…` | ❌→登录 | 302 → `https://www.duxiu.com/login.jsp?backurl=https%3A%2F%2Fbook.duxiu.com%2Fsearch%3Fsw%3D…` |
| 全文/章节阅读 | ❌ | 需机构账号或读秀卡，且 IP 需在授权范围 |

- 图书书目核对可改用公开 OPAC（如 `references/academic/opac.bac.gov.cn.md`）；图书章节全文另见超星发现 `references/academic/chaoxing.com.md`（同为登录墙）。

## 坑

- 登录页本身可 200 打开，且含用户名/密码表单，**容易误以为"能访问"**；判据是 URL 是否被重写到 `login.jsp` 且正文出现"IP 不在我们服务的范围内"。
- 站点返回的 `当前机器ip` 是真实出口 IP，说明其按 IP 白名单放行。
