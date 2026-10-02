# cpema.org —— 医药企业管理协会动态

- 去哪找：`https://www.cpema.org/`；详情页 `/index.php?m=content&c=index&a=show&catid={栏目}&id={文}`
- 什么时候用：查中国医药企业管理协会的会议/活动与政策转载；**不要在这里取统计数据**。
- 怎么搜：PHP CMS（PHPCMS 系），栏目按 `catid` 区分，站内检索可用；无 API。
- 覆盖：协会动态、政策与统计文件转载。
- 门槛：免费、无需登录。
- 实测：2026-10-03 `https://www.cpema.org/` → 200，42.8 KB，title「中国医药企业管理协会」✅；整页检索「统计」仅命中 **1 条转载的卫健委统计文件**，另有友情链接「中国医药统计网 `www.yytj.org.cn`」。
- 上游：中国医药企业管理协会。

## 坑

1. **只有协会动态，无统计数据**：医药工业数值请转 `yytj.org.cn.md`（中国医药统计网）或工信部消费品工业司运行数据。
2. 详情页是 `index.php?…&id=N` 查询串形式，没有 `/article/N` 之类的 RESTful URL，抓取时注意 URL 编码。
