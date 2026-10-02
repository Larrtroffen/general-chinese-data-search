# eurostat —— 欧盟统计局

- 去哪找：门户 `https://ec.europa.eu/eurostat/`；数据浏览器 `https://ec.europa.eu/eurostat/databrowser/`；**API 根** `https://ec.europa.eu/eurostat/api/dissemination/`。
- 什么时候用：欧盟/EFTA/候选国的可比社会经济数据（GDP、就业、通胀、能源、环境、R&D、人口、区域统计）；要免 key 的 JSON/TSV 直取；做欧洲国别/区域对比。
- 怎么搜：
  ```bash
  # ① 取数：数据集码 + 维度过滤，format=JSON|TSV|SDMX
  curl -s 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nama_10_gdp?format=JSON&geo=DE&time=2023&na_item=B1GQ&unit=CP_MEUR'
  # ② 数据集目录（TOC，全量 TSV）
  curl -s 'https://ec.europa.eu/eurostat/api/dissemination/catalogue/toc/txt?lang=en'
  ```
  - 取数 URL：`/statistics/1.0/data/{dataset}?format=JSON&{维度}={值}&…`；同维度多值用重复参数（`&geo=DE&geo=FR`）。
  - JSON 返回：`label`、`source`、`updated`、`id[]`（维度顺序）、`size[]`、`value{}`（**index→值 的字典**）、`status{}`（如 `p`=临时值）。
  - 其他：`.../data/{ds}?format=TSV`、`format=SDMX`（2.1）、`.../metadata/{ds}?format=JSON`（码表与口径）。
- 覆盖：EU-27 + EFTA + 候选国 + 聚合体（EA-20 等）；数据集上万条（TOC 实测 1.97 MB TSV）；年代视表（部分 1960s 起），月/季/年，含 NUTS 区域层。
- 门槛：免费、**无 key、无注册**。
- 实测：2026-10-03，macOS arm64，curl 8.x：`.../data/nama_10_gdp?format=JSON&geo=DE&time=2023&na_item=B1GQ&unit=CP_MEUR` → 200 / 2.97 KB，`value {"0":4254930.0}`、`status {"0":"p"}`、`updated 2026-10-02`；`/catalogue/toc/txt?lang=en` → 200 / 1.97 MB TSV。
- 上游：`https://ec.europa.eu/eurostat/web/main/data/web-services`（上游声明）。

## 细节

### JSON 结构怎么读

```
id:   ["freq","unit","na_item","geo","time"]   ← 维度顺序
size: [1, 1, 1, 1, 1]                          ← 各维度取值个数
value: {"0": 4254930.0}                        ← 扁平下标 → 观测值
```
扁平下标按 `size` 做混合进制解码即可还原 `(freq,unit,na_item,geo,time)` 坐标。

## 坑

1. Python `urllib`/部分容器直连 `ec.europa.eu` 会撞**本地证书链**（`CERTIFICATE_VERIFY_FAILED`）；用 curl（系统信任链）或显式指定 CA。
2. 维度值必须用**码**（`B1GQ` 而非 "GDP"），先查 `.../metadata/{ds}` 的码表。
3. `format=JSON` 是 Eurostat 自有结构（`value` 为字典），不是数组；解析前先按 `id`/`size` 还原坐标。
4. 数据集码会随基准修订改名/合并；脚本里绑死的码要定期对 `updated` 字段复核。
5. 未公布频控，但批量取数请 ≥1.5 s 间隔。
