# neeq.com.cn —— 新三板挂牌与信息披露

- 去哪找：门户 `https://www.neeq.com.cn/`；**挂牌公司公告/信息披露**（栏目在门户导航内）；行情与公司查询接口域同 `www.neeq.com.cn`。
- 什么时候用：要**全国中小企业股份转让系统（新三板）**的挂牌公司名录、公告、定向发行、行情/交易数据；新三板企业样本与"专精特新"交叉研究。
- 怎么搜：官网本机匿名**过不了反爬**（JS 挑战 + 接口重定向环）。绕行：挂牌公司**公告**可经 `../business/cninfo.com.cn.md`（新三板代码 `400/430/83x/87x` 部分在 cninfo 覆盖内）；主体登记走 `../gov/gsxt.md`。
- 覆盖：新三板挂牌公司名录/公告/发行/行情（栏目范围，未逐项枚举）。
- 门槛：官网**需浏览器**；cninfo / 工商走免登录路径。
- 实测：2026-10-03，macOS arm64 curl 8.x（桌面 UA）——`GET https://www.neeq.com.cn/` → `200` 但仅 **345 B**，正文为 JS 挑战（`window.open("/","_self"); document.cookie="C3VK=b594c1; …"`）；补 `Cookie: C3VK=b594c1` 仍 345 B；`GET https://www.neeq.com.cn/nqxxController/nqxxCnzq.do?callback=jQuery&page=0&typejb=T…` → `302` 且超过 50 次重定向（curl 中止）。
- 上游：`https://www.neeq.com.cn/`（全国中小企业股份转让系统有限责任公司）。

## 细节

### 现象拆解

| 请求 | 观察 |
|---|---|
| `GET https://www.neeq.com.cn/` | `200` / 345 B，JS 设 `C3VK` Cookie |
| 同上 + `Cookie: C3VK=b594c1` | 仍 345 B 挑战页 |
| `GET /nqxxController/nqxxCnzq.do?…` | `302` 无限重定向 |

- 与 `../business/bse.cn.md` 同一套"创宇盾"C3VK 挑战；静态 Cookie 无效，须真实浏览器执行首跳 JS。

### 绕行

- 挂牌公司公告 → `../business/cninfo.com.cn.md`（免登录 JSON）。
- 主体登记/名称核验 → `../gov/gsxt.md`。
- 省级"专精特新"/股交中心名单 → `../business/enterprise-certifications.md`。

## 坑

1. 遇到 `Maximum (50) redirects followed` 即该站反爬签名；不要加大 `-L` 或做重试轰炸（会封 IP）。
2. `C3VK` 值随机、按会话变化，硬编码无效。
3. 需要新三板**官方精确名录/行情表**时，只能在真实浏览器里人工导出；研究批量样本优先走 cninfo。
