# navi.cnki.net —— 知网年鉴卷详情页

知网年鉴库的"年鉴导航"详情页：单卷年鉴的基本信息、内容简介、全卷目录，以及整刊在线浏览入口。**《北京朝阳年鉴(2019)》即在此页获取全部元数据。** 检索与详情均需过滑块验证码，得走可见 Chrome 人工过码。

- 去哪找：详情页 `https://navi.cnki.net/knavi/detail?p={加密参数}`（`p` 为站点自加密串，不可离线还原，从知网年鉴库的检索结果/导航链接点入获得）；年鉴库总入口 `https://kns.cnki.net/res/cyfd`
- 什么时候用：要单卷年鉴的基本信息/内容简介/全卷目录；要从年鉴里取区级栏目与页码区间
- 怎么搜：curl 与 headless 均被挡，须可见 Chrome 人工过滑块：
  ```javascript
  const tab = await browser.open({ name: "cnki_manual", url: "<knavi 链接>", headed: true, persist: true, timeout: 120000 });
  // → 用户在弹出的可见 Chrome 窗口里把滑块拖到位 → 页面自动跳转到年鉴导航页
  ```
  要点：`headed: true`（可见窗口）+ `persist: true`（跨回合保活）；用户在系统层面手动完成滑块后，页面即正常渲染。
- 覆盖：知网年鉴库单卷（基本信息/内容简介/全卷目录/整刊浏览）；条目级全文另走 kns.cnki.net 年鉴库
- 门槛：过滑块验证码；整刊在线浏览/下载须 CNKI 登录（个人账号或机构 IP 权限）
- 实测：2026-10-03，macOS + curl（desktop UA）：`GET https://navi.cnki.net/knavi/` → 302 → `https://kns.cnki.net/verify/home?captchaType=blockPuzzle&ident=…&returnUrl=…`，`HTTP 200 size=2154`，`<title>安全验证</title>`（与 curl 直连详情页返回的"安全验证"JS 壳一致）
- 上游：`https://navi.cnki.net/`

## 细节

### URL 形态

```
https://navi.cnki.net/knavi/detail?p={加密参数}
```

- `p` 是站点自加密串（不可离线还原），从知网年鉴库的检索结果/导航链接点入获得。
- 同一页内含年份切换列表（如 2013–2022），可跳到该年鉴其他卷。

### 反爬与过码（实测方法）

| 方式 | 结果 |
|---|---|
| curl 直连 | ❌ 返回"安全验证"JS 壳（2154 字节） |
| headless Chromium | ❌ 落到 `kns.cnki.net/verify/home?captchaType=blockPuzzle…`，出现"向右滑动完成验证"拼图滑块 |
| **可见 Chrome + 人工拖滑块** | ✅ 过码后直达导航详情页 |

### 页面可提取内容

- **基本信息**：年鉴年份、ISBN、责任说明（主编）、主编单位、出版者、出版日期、页数、字数、定价、主题词、中图分类号。
- **内容简介**：全文可取（编辑说明/凡例）。
- **全卷目录**：栏目浏览区含全部栏目名+页码区间（如"街道 地区(乡) 339-437"）。
- 隐藏字段（供程序取用）：
  - `#njCataViewUrl` = 整刊在线浏览目标 URL（见下）
  - `#pykm` = 年鉴拼音码（如 YBJCY）
  - `#pCode` = CYFD（年鉴库代码）、`#knsResource` = ALMANAC

### 统一入口：整刊在线浏览/下载

页面"整刊在线浏览"按钮的点击逻辑（页内 JS）：

```javascript
$(".preview").click(function (e) {
    if (isHaveLogin()) {
        window.open($('#njCataViewUrl').val());   // 登录后才打开
    } else {
        // 弹 layer.msg 登录提示，不打开
        return;
    }
});
```

- **必须 CNKI 登录**（个人账号或机构 IP 权限）。
- 目标地址形如：
  `https://bar.cnki.net/bar/download/order?id={加密串}`
  → 知网整刊下载服务（bar.cnki.net）：登录后在此下单获取整本 CAJ 文件，用 **CAJViewer**（`http://cajviewer.cnki.net/`）阅读。

## 关联

- 通用知网检索与验证码情况：见 `references/academic/cnki.net.md`。
- 若需系统性地读区级年鉴：另一官方渠道是京网/数字方志馆（见 `references/archives/bjdsdfz.cn.md`、`references/archives/bjsfzg.bjdsdfz.cn.md`）。
