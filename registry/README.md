# registry —— 源注册表（机器可读大索引）

`references/` 是人工写的**来源卡**（一源一卡，讲怎么用）；`registry/` 是**全量源表**（一条一行，
只回答"这个源在哪、什么状态"）。两者互补：卡是精讲，表是索引。

## 文件

- `registry/<tier>.csv` —— 按层切分的源表（tier 名同 `references/` 的层名）。
- `registry/<批次>.csv` —— 批量枚举的中间文件（如 `gov-provinces.csv`、`gov-counties.csv`、`crawlers.csv`）；与层文件同 schema，`ref` 注明枚举批次。
- `registry/all.csv` —— 汇总表（由 `scripts/registry_merge.py` 生成，勿手改）。

## 字段（全表统一）

| 列 | 说明 |
|---|---|
| `id` | 稳定标识：默认 `tier:host`，同主机多路径时用 `tier:host+path摘要` |
| `tier` | 归属层（`gov`/`wechat`/`stats`…；爬虫仓一律 `crawlers`） |
| `name` | 简短名称（机构名/站点名/仓库名） |
| `url` | 入口 URL（尽量给主页或检索入口） |
| `host` | 主机名（探活用） |
| `status` | `probed-2xx` / `probed-3xx` / `probed-000`（不可达）/ `declared`（上游声明未测）/ `unprobed` |
| `http_code` | 最近一次探活的状态码（未探为空） |
| `probe_date` | 探活日期（YYYY-MM-DD） |
| `note` | 一句话说明（层级/门槛/别名） |
| `ref` | 来源：卡片文件路径、清单出处或枚举批次的说明 |

## 维护流程

```bash
# 1) 从现有卡片抽取 URL（生成/刷新 registry/<tier>.csv 中 ref 指向卡片的行；幂等去重）
python3 scripts/registry_extract.py

# 2) 批量探活（并发 8、每主机 1 次、超时 12s；回填 status/http_code/probe_date）
python3 scripts/registry_probe.py --workers 8 --timeout 12

# 3) 汇总
python3 scripts/registry_merge.py   # 生成 registry/all.csv + 打印各层计数
```

- **一行 = 一个源**；同一主机多个用途可多行，但 `id` 必须唯一。
- 探活只做一次轻量 GET（`-o /dev/null -w '%{http_code}'`），不做深挖；深挖细节写回对应对卡片。
- 状态会漂移：`probe_date` 超过 90 天的行优先重测。
