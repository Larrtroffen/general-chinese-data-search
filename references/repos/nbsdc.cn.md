# nbsdc.cn —— 基础学科数据与 CSTR 检索

- 去哪找：门户 `https://www.nbsdc.cn/`；检索页 `https://www.nbsdc.cn/general/dataSetHome?searchKey=<词>`；**列表 API** `https://www.nbsdc.cn/api/general/v1/getDataLists?pageNum=1&pageSize=10`；**检索 API** `POST https://www.nbsdc.cn/api/general/searchDataSet`
- 什么时候用：找**基础学科（物理 / 化学 / 天文 / 地理 / 生物 / 材料 / 信息）的国内数据集**；核一条数据的 **CSTR** 标识（`CSTR:16666.11.nbsdc.*`）与规范引用；找国内野外台站、图谱、图像类数据。
- 怎么搜：
  ```bash
  # 1) 浏览 / 全量列表（GET，匿名，实测 200）
  curl -s 'https://www.nbsdc.cn/api/general/v1/getDataLists?pageNum=1&pageSize=2'
  # → {"list":{"totalCount":63255,"totalPages":15814,"list":[
  #     {"name":…,"cstr":"CSTR:16666.11.nbsdc.feoakuia","keywords":"农业病虫害；图像；数据集；机器学习",
  #      "subject":[{"subjectCode":"52020","subjectName":"人工智能"}],"description":…,
  #      "downloadCount":…,"viewingCount":…,"authorsName":…,"dataNo":…,"version":…}]}}

  # 2) 检索（POST JSON，必须给全 12 个字段，实测 200）
  curl -s -X POST -H 'Content-Type: application/json' \
    --data-binary '{"pageNum":1,"pageSize":2,"sortCode":"","searchTerms":"数据","searchName":"数据","dataTypeId":1,"subject":"","baseFlag":false,"sharingModel":"","isHighQuality":0,"publishTime":"","dataOtherTypeId":-1,"orgUnitId":""}' \
    'https://www.nbsdc.cn/api/general/searchDataSet'
  # → {"list":[{"cstr":…,"subject":["580"],"description":…,"name":…}],"totalCount":…,"totalPages":…}
  ```
- 覆盖：**63,255** 条数据资源（2026-10-03 `totalCount`），含数据集 / 软件 / 报告 / 论文 / 著作 / 专利 / 标准；按学科分类（`subject`）与中图码组织。
- 门槛：浏览与以上两个接口 **免登录**；下载部分数据需登录或申请。
- 实测：2026-10-03，macOS arm64，curl（桌面 UA，同主机 ≥1.5s 间隔）：`getDataLists?pageNum=1&pageSize=1` → **200**，`totalCount=63255`；`searchDataSet` 完整 body（`searchTerms:"数据"`）→ **200** 有命中；**字段不全时 → 302**；浏览器打开 `dataSetHome?searchKey=气候` → 页面显示「数据资源(30)」。
- 上游：`https://www.nbsdc.cn/`（中科院计算机网络信息中心牵头）

## 坑

- `searchDataSet` **必须一次给全 12 个字段**（`pageNum/pageSize/sortCode/searchTerms/searchName/dataTypeId/subject/baseFlag/sharingModel/isHighQuality/publishTime/dataOtherTypeId/orgUnitId`），少一个就 302 跳转；参数名由站点 JS `basic/modules/dataset/dataSetList.js` 还原。
- `dataTypeId=1` 是数据集；其余类型看检索页 `?tpe=`（3 软件 / 4 报告 / 5 论文 / 6 著作 / 7 专利 / 8 标准）。
- 大范围浏览用 `getDataLists`（GET、字段更全）；关键词收敛用 `searchDataSet`（POST）。两者命中口径不完全一致，找不到时先用全量再本地过滤兜底。
- 数据条目正文在详情页（`/general/dataSetHome` + 条目 id）；接口只给元数据。
