# CFPS —— 全国家庭与个人双年追踪面板

- 去哪找：项目门户 `https://www.isss.pku.edu.cn/cfps/`；数据中心·公开数据 `https://www.isss.pku.edu.cn/cfps/sjzx/gksj/index.htm`；官方数据平台 `https://cfpsdata.pku.edu.cn/#/home`；备用下载 `https://opendata.pku.edu.cn/dataverse/CFPS`。
- 什么时候用：要**家庭户 + 个人两级的中长期追踪面板**——收入/消费/资产、教育、健康、人口迁移、家庭关系、少儿发展；做代际传递、生命历程、城乡对比等实证。
- 怎么取：在官方数据平台注册 → 填个人信息 → 提交公开数据申请 → 审核通过（官网标注 **3 个工作日**，假期顺延）→ 下载。北大师生可用校园卡登录新版平台，但仍须提交申请。
- 覆盖：基线 2010，其后每两年一轮（2010 / 2012 / 2014 / 2016 / 2018 / 2020 / 2022…）；家庭户与个人两层；基线覆盖 25 个省级单位、约 1.5 万户（样本量为上游声明，未本机核）。
- 门槛：免费；**需注册 + 实名申请 + 审核**；受限数据另走审批；两个数据平台账号不互通。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA：`https://www.isss.pku.edu.cn/cfps/` → 200（10,988 B）；`…/cfps/sjzx/gksj/index.htm` → 200（含申请指南）；`https://cfpsdata.pku.edu.cn/` → 200（SPA，2,105 B）；`http://opendata.pku.edu.cn/` → **403 Forbidden**（本机被拒）。
- 上游：北京大学中国社会科学调查中心（ISSS）`https://www.isss.pku.edu.cn/`。

## 细节

- 数据分「公开数据 / 限制数据」两级：公开数据审核后下载；限制数据（敏感变量、区县码等）需单独申请并说明用途。
- 官方数据平台（`cfpsdata.pku.edu.cn`）与北京大学开放研究数据平台（`opendata.pku.edu.cn/dataverse/CFPS`）**账号不互通**；旧版 CFPS 平台账号可直接登录新版。
- 文档中心（问卷、编码本、用户手册）：`https://www.isss.pku.edu.cn/cfps/wdzx/index.htm`。

## 坑

- `cfps.pku.edu.cn` 有 DNS 记录但无服务，**不是数据入口**；认准 `isss.pku.edu.cn/cfps` 与 `cfpsdata.pku.edu.cn`。
- 数据平台维护期会切到 `opendata.pku.edu.cn`；后者对本机直连返回 403，需真实浏览器或校园网。
- 审核按工作日计算，赶进度要预留时间。
