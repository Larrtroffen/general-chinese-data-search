# gdass.org —— 广东省社会科学院（本机不可达）

- 去哪找：`https://www.gdass.org/`（含 `/index.shtml`）。
- 什么时候用：要广东省级智库成果与专家；线索指向「广东省社会科学院**智慧社科平台**」。
- 怎么搜：站点为静态 `.shtml`（`MessageInfo_*.shtml`、`BriefIntroduction_*.shtml`、`expert.shtml`）；**本机（境外出口）无 HTTP 响应**，需在大陆网络或浏览器访问。
- 覆盖：广东省社科院动态、专家、机构；智慧社科平台为院内数据与科研管理平台（上游声明，见 2026–2028 运维磋商公告 `MessageInfo_10882.shtml`）。
- 门槛：未知（站点不可达）；智慧社科平台预计需账号。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA：`https://www.gdass.org/`、`http://www.gdass.org/`、`https://www.gdass.org/index.shtml` **均 → 000**；`curl -v` 显示 DNS 解析 `120.197.34.8`、TLSv1.3 握手**成功**（`CHACHA20-POLY1305`），但此后 30 s 内无任何 HTTP 响应。
- 上游：`https://www.gdass.org/`；智慧社科平台运维磋商公告（搜索结果快照）。

## 坑

1. **TLS 通、HTTP 不通**：不是证书问题，是源站对境外/该出口无响应——换大陆网络或浏览器再试。
2. 同名的「广州市社会科学院」是另一家，入口不同（见 `local-research-platforms.md`）。
3. 智慧社科平台的用户入口 URL 本机未探到（站点不可达），引用前先自行探测。
