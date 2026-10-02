# stats.gov.cn —— 统计用区划代码页面

- 去哪找：新站结构 `https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/{年份}/{区划代码}.html`；旧站结构 `http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/…`；目录页 `https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/`。
- 什么时候用：想取某年某地区的完整街道/镇/乡名录（含代码）。
- 怎么搜：直接拼年份/区划代码 URL；**但历史年份页面在该站已不可获取**（见下）。
- 覆盖：统计用区划代码页面，按年 × 区划代码；历史年份已下线。
- 门槛：免费；历史年份不可用。
- 实测：原卡未记录日期（本机 curl）；2018 年页面 404/403（见下矩阵）。
- 上游：国家统计局 `https://www.stats.gov.cn/`。

## 细节

### 现状（本机实测）

| 路径 | 状态 |
|---|---|
| `https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2018/11.html`（新站结构） | ❌ 404（历史年份页面已下线） |
| `http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/11.html`（旧站结构） | ❌ 301 → 404 |
| `https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/`（目录页） | ❌ 403 |

结论：**2018 年历史区划页面在该站已不可获取**。当前年份页可能仍按 `/sj/tjbz/tjyqhdmhcxhfdm/{年份}/{区划代码}.html` 存在，但历史年份不要依赖此站。

### 替代获取途径

1. **区划地名网 xzqh.org**（见 `xzqh.org.md`）：逐区页"政区划分"段转载了统计用区划代码表，2019 年与 2018 年北京乡级区划一致，可作底本。
2. **《北京统计年鉴》表 1-1**：`http://nj.tjj.beijing.gov.cn/nj/main/2019-tjnj/zk/e/html/C01-01.jpg`（各区街道/镇/乡个数核对口径，如 2018 全市 街道152+镇143+乡38=333）。
3. **民政部全国行政区划信息查询平台**：`https://xzqh.mca.gov.cn/`（接口需登录/参数，未深测）。
4. 第三方镜像：红黑人口库 hongheiku.com、行政区划网 tcmap.com.cn（内容为转载，需交叉核对）。

### 核对方法

- 逐区求和校验总数（北京 2018：152+143+38=333）；与年鉴表 1-1 对照。
- 归一化名称再比对：去"（地区）"括号、"办事处"后缀、民族乡族名（回族/满族…）、区名前缀。
- 注意"类似乡级单位"（开发区等）不属 街道/镇/乡 口径。
