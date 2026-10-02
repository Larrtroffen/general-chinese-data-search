# IPUMS International —— 中国人口普查微数据

- 去哪找：`https://international.ipums.org/international/`；中国样本页 `https://international.ipums.org/international-action/sample_details/country/cn`。
- 什么时候用：要**中国人口普查的个体级微数据**并做跨国比较（与全球多国同构变量）；人口学、劳动、迁移、教育、家庭结构、性别研究。
- 怎么取：注册 IPUMS 账号 → 在 Select Data 选中国样本与变量 → 在线定制抽取（extract）→ 下载；**是按需定制提取，不是整库下载**。
- 覆盖：实测中国样本有 **1982、1990、2000** 三次全国人口普查（系统抽样，抽样比 **1%**；1982 年样本 **10,039,191** 条个人记录，自加权，expansion factor = 100）。
- 门槛：免费；**需注册并接受使用条款**；单次抽取有样本/变量数上限。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA：`https://international.ipums.org/international/` → 200（13,024 B）；中国样本页 → 200（19,211 B，1982/1990/2000 三个样本 + 抽样设计与记录数）。
- 上游：University of Minnesota 明尼苏达人口中心（IPUMS）。

## 细节

- 样本页给出的 1982 年普查特征：第三次全国人口普查，国家统计局执行，de jure，1982-07-01 0 时点；系统抽样 1%；10,039,191 条个人记录；自加权。
- 变量为**跨国同构（harmonized）**编码，便于与中国国内调查（CFPS/CHIP 等）做对照，但口径与国内原始普查表不同。
- 同一站还有 IPUMS USA / CPS / NHGIS 等姊妹项目（各自独立注册）。

## 坑

- 需**注册 + 接受条款**；抽取任务较大时要排队等候。
- 中国样本仅 3 次普查（实测），**没有近年抽样调查**；与国内「1% 人口抽样调查」不是同一数据。
- 定制抽取的文件格式与变量命名自成体系，合并到国内数据前要读 harmonization 文档。
