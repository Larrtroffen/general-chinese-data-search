# amac.org.cn —— 公募私募资管规模数据

- 去哪找：门户 `https://www.amac.org.cn/`；数据统计（资产管理行业总貌）`https://www.amac.org.cn/sjtj/datastatistics/comprehensive/`；统计报告 `https://www.amac.org.cn/sjtj/tjbg/`（公募基金统计 `…/tjbg/gmjj/`）。
- 什么时候用：要**中国证券投资基金业协会口径**的资产管理行业规模——公募基金、证券公司资管计划、基金公司资管计划、基金公司管理的养老金、私募证券/私募股权、期货资管、ABS 等的**产品数与资产规模**；要公募/私募的季度统计报告。
- 怎么搜：**有匿名 JSON 接口**（jQuery ajax，同源，`https://www.amac.org.cn`）：
  - `POST /portal/front/home/findAssetsManageIndustry` → 行业总貌（各业态产品数 + 资产规模，季度）
  - `GET /portal/front/management/assetManage/getAllTimes?dataType=1&productType=1` → 可选季度列表
  - `GET /portal/front/management/assetManage/findDatas?dataType={n}` → 分页表格数据
  - `GET /portal/front/management/assetManage/findDataByTime?dataType=&productType=&time=` → 指定季度时间序列
  结果形态：JSON（`{"data":{"errcode":0,…}}`）；统计报告为 PDF 附件（`P0{时间戳}.pdf`，须解析列表页）。
- 覆盖：资管行业总貌按季度（实测 endDate=2026年一季度；时间轴 2018Q4–2026Q2）；公募基金统计报告、机构与产品备案公示；全国口径。
- 门槛：无（JSON 免 key、免登录）。
- 实测：2026-10-03，桌面 UA curl——`GET https://www.amac.org.cn/` `200/378,476 B`；`GET /sjtj/datastatistics/comprehensive/` `200/354,500 B`；`GET /sjtj/tjbg/gmjj/` `200/328,303 B`；`POST /portal/front/home/findAssetsManageIndustry`（带 Referer）→ `200/995 B`，`application/json`，正文含 `"endDate":"2026年一季度"`、`{"bizType":"公募基金","productCnt":13930,"assetUnderManagement":"375322.31"}`、`证券公司资管计划`、`基金公司资管计划`、`基金公司管理的养老金` 等；`GET /portal/front/management/assetManage/getAllTimes?dataType=1&productType=1` → `200/406 B`，`data` 为 `["2026Q2","2026Q1",…,"2018Q4"]`。
- 上游：`https://www.amac.org.cn/`（中国证券投资基金业协会）。

## 细节

### 接口一览（同源，`https://www.amac.org.cn`）

| 方法 | 路径 | 用途 |
|---|---|---|
| POST | `/portal/front/home/findAssetsManageIndustry` | 资产管理行业总貌（季度） |
| GET | `/portal/front/management/assetManage/getAllTimes?dataType=&productType=` | 可选季度 |
| GET | `/portal/front/management/assetManage/findDatas?dataType=` | 分页表格 |
| GET | `/portal/front/management/assetManage/findDataByTime?dataType=&productType=&time=` | 季度时间序列 |
| GET | `/portal/ESSearch/publicity/autocomplete` | 公示检索联想 |
| GET | `/portal/front/upload/queryAllByCondition?flag=` | 上传/公示列表 |

- 规模单位：`assetUnderManagement` 为**亿元**（如 375322.31 亿元 ≈ 37.53 万亿）。
- 机构/产品/人员公示另有独立子站：`https://gs.amac.org.cn/amac-infodisc/…`。
- 统计报告 PDF 规律：`/…/{栏目}/{YYYYMM}/P0{20位时间戳}.pdf`。

## 坑

1. 行业总貌是**季度**频率，`endDate` 文案（"2026年一季度"）与 `getAllTimes`（"2026Q2"）**口径措辞不一致**，取数时以具体接口返回为准，别按字符串比大小。
2. `findDatas` 的 `dataType` 是**分页/分区编号**（页内 `page`），含义随页面而变，须对照 `comprehensive` 页的表格标题解析。
3. 规模字段是**字符串型数字**，做计算前要转数值；单位为亿元。
4. 公示系统（`gs.amac.org.cn`）与主站**分开**，产品/私募备案明细去子站，别在主站找。
5. 与 `sac.net.cn.md`（证券公司经营数据）、`cfachina.org.md`（期货公司经营数据）分工：资管产品规模看 AMAC，券商/期货公司本体财务看 SAC/中期协。
