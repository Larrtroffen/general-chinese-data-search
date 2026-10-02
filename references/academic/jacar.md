# jacar —— 日本近代亚洲关系档案检索与图像

- 去哪找：
  - 检索（日文）：`https://www.jacar.archives.go.jp/aj/search`（详细检索表单与结果同页）
  - 检索（英文界面）：`https://www.jacar.archives.go.jp/aj/search-en`
  - 门户：`https://www.jacar.go.jp/`；国立公文书馆跨库检索：`https://www.digital.archives.go.jp/crosssearch`
- 什么时候用：要找**近代中日关系**的一手档案——满蒙/满洲、日中战争、外务省与陆海军文书、明治以降条约与公文、占领期资料；需要「件名级目录 + 原件图像」时首选。
- 怎么搜：GET，结果**服务端渲染 HTML**（可 curl、免登录）。最小模板：
  `https://www.jacar.archives.go.jp/aj/search?kl0=AND&ks0=kw_all&kw0=<URL编码词>&rows=20&sf=seq_a`
  翻页加 `&page=N`（`page=1` 即第 1 页）；结果行「閲覧」按钮 → 国立公文书馆 IIIF 图像查看器。
- 覆盖：国立公文书馆、外务省外交史料馆、防卫省防卫研究所等所藏机关（`inst` 共 **13 个代码**：01–04、06–14）的近代档案；年代以明治—昭和前期为主（命中里见到昭和 21 年＝1946 年文书）；粒度=件名/册/图像；「満州」命中 **99,121 件**，量级十万级。
- 门槛：免费、免登录、无 key（图像同理）。
- 实测：2026-10-03，`curl 'https://www.jacar.archives.go.jp/aj/search?kl0=AND&ks0=kw_all&kw0=%E6%BA%80%E5%B7%9E&rows=20&sf=seq_a'` → **200 / 378,688 B**，`<span class="count-number" data-count="99121">99121` 件。同词改走浏览器提交，落点 URL 完全一致。
- 上游：<https://www.jacar.go.jp/>、<https://www.digital.archives.go.jp/>

## 细节

> 探测纪律（本机实测 2026-10-03）：桌面 Chrome UA、20s 超时、间隔 ≥1.5s；`✅`=200，`⚠️`=需浏览器/有条件，`❌`=被拦。检索类实测用 `curl`，图像类实测用无头 Chromium。

### 检索参数（`/aj/search`，GET）

参数名由页面 JS `search-cond.js` 动态拼装（表单里 `name=""`，故直接看 HTML 看不到）：

| 参数 | 含义 | 取值 |
|---|---|---|
| `kw0`,`kw1`… | 关键词（可多组） | 任意词 |
| `kl0`,`kl1`… | 组间逻辑 | `AND`（默认）、`NOT` |
| `ks0`,`ks1`… | 检索范围 | `kw_all` すべて / `kw_title` 標題 / `kw_creator` 作成者 / `kw_content` 内容 / `kw_hist` 組織歴 / `kw_referrence` レファレンスコード |
| `rows` | 每页条数 | `20`(默认) / `50` / `100` / `200` |
| `sf` | 显示顺序 | `seq_a` 指定無し(默认) / `reference_a` / `date_a` / `date_d` / `inst_a` |
| `page` | 页码 | 1,2,3… |
| `type` | 目录种别 | `aj21` / `aj22` / `aj23`（多选） |
| `inst` | 所藏机关 | `01`–`04`、`06`–`14`（多选，无 05） |
| `datatype` | 资料种别 | `01` / `02` / `04` |
| `lng` | 语言 | `chi` `jpn` `eng` `rus` `ger` `fre` … |
| `confidential` | 机密区分 | `1`–`7` |
| `date_e_from`/`date_y_from`/`date_m_from`/`date_d_from`（及 `_to`） | 年月日范围 | 数字 |
| `fond` | 全宗 | 由 `/aj/ajax/search/fond` 返回 |

- `kl0`+`ks0`+`kw0`+`rows`+`sf` **要成套给**：只给 `kw0`+`ks0`（缺 `sf`）→ 200 但 **0 件**；`sf` 给非法值（如 `score`）同样 → 0 件。
- 旧参数 `?kw=<词>`（首页表单原始写法）→ **200 但恒 0 件**，勿用。

### 端点表

| 用途 | 端点 | 形态 |
|---|---|---|
| 件名详细目录 | `https://www.jacar.archives.go.jp/das/meta/<レファレンスコード>`（英文 `/das/meta-en/<code>`） | ✅ 200 / 66,724 B，`<title>`=件名 |
| 图像查看器 | `https://www.digital.archives.go.jp/img/<id>`（结果行「閲覧」链接、`target=_blank`） | ✅ 200；`data-download-base-path="/contentDownload/<id>"` |
| IIIF Manifest | `https://www.digital.archives.go.jp/api/iiif/<id>/manifest.json` | ✅ 200 JSON，IIIF Presentation **2.1**（`sc:Manifest`），`license` 指二次利用规则页 |
| IIIF 图像（免登录） | `…/api/content/item/<bundle>/<code>/iiif/<canvas>.jp2/full/max/0/native.jpg` | ⚠️ 浏览器内 ✅ 200 `image/jpeg` 457,612 B；curl 直连 → ❌ 403「アクセス制限のお知らせ」 |
| 缩略图/浏览按钮延迟加载 | `POST /aj/ajax/search/view`，body `aipid=aj11/A17110886300` | 200 JSON（`thumbPathContent` 等） |
| 检索结果 CSV 导出 | `POST /aj/ajax/search/csv`，body `isall=1&idaction=…` | CSV |
| 勾选/取消 | `POST /aj/ajax/search/select` / `/unselect` | 200 |
| 全宗树 | `GET /aj/ajax/search/fond` | JSON |

- レファレンスコード形如 `A17110886300`（A/B/C 前缀对应不同机关群）；结果行复选框 `value` 形如 `aj11/A17110886300`（即 aipid）。
- 图像实际托管在**国立公文书馆デジタルアーカイブ**（`digital.archives.go.jp`），JACAR 只给跳转。

## 坑

1. **必须带 `sf`**：缺 `sf` 或值非法时搜索结果恒为空，很容易误判「JACAR 搜不到」。
2. **图像 API 限速**：`digital.archives.go.jp` 的 JSON/图像接口对「短时间大量访问」直接返 403（页面标题「アクセス制限のお知らせ」）。批量取图要放慢，或用真实浏览器会话。
3. **JACAR 站点内没有图像文件**：`https://www.jacar.archives.go.jp/das/image/<code>` → 404；图像只在 `digital.archives.go.jp`。
4. 界面日文为主，英文界面靠 `/aj/search-en`、`/das/meta-en/` 后缀切换（参数名不变）。
5. 二次利用（转载/出版）受各机关规则约束，见 manifest 的 `license` 链接（`https://www.digital.archives.go.jp/secondary-use`）。
