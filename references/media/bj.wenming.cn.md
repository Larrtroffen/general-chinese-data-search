# bj.wenming.cn —— 中国文明网北京站转载

中央文明办中国文明网的地方频道，常转载北京日报等市级权威稿。

- 去哪找：站点 `http://bj.wenming.cn/`；文章页 `http://bj.wenming.cn/chy/yw/YYYYMM/tYYYYMMDD_{id}.shtml`
- 什么时候用：北京日报等市级权威稿原站旧文不易回捞时，取其可用转载
- 怎么搜：`web_search`：`site:bj.wenming.cn {关键词}`；命中后 curl 直读
- 覆盖：市级权威稿转载；示例含 2018-03-15
- 门槛：无
- 实测：2026-10-02，macOS + curl，文章页静态 HTML 直读（状态见 media/README 索引）
- 上游：<http://bj.wenming.cn/>

## 细节

- 示例（2018-03-15 北京日报"实施方案"稿）：`http://bj.wenming.cn/chy/yw/201803/t20180315_4621383.shtml`。
- 取正文（`http` 非 https 路径）：

  ```bash
  curl -s -m 25 -A 'Mozilla/5.0 …' 'http://bj.wenming.cn/chy/yw/201803/t20180315_4621383.shtml'
  ```
