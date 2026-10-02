# rmzxw.com.cn —— 人民政协网转载

全国政协机关网，转载新华社等央媒稿；东城"3 街道试点"样本文即出自此处。

- 去哪找：站点 `http://www.rmzxw.com.cn/`；文章页 `http://www.rmzxw.com.cn/c/YYYY-MM-DD/{id}.shtml`
- 什么时候用：新华社/人民政协报稿的稳定转载点；样本类长文（"XX 区试点 N 个街道"）常在此留存
- 怎么搜：`web_search`：`site:rmzxw.com.cn {关键词}`；或按标题反查
- 覆盖：新华社/人民政协报稿转载；示例含 2018-10-30
- 门槛：无
- 实测：2026-10-02，macOS + curl，文章页 `http` 直连（状态见 media/README 索引）
- 上游：<http://www.rmzxw.com.cn/>

## 细节

- 示例（2018-10-30 东城区街道管理体制改革样本调查）：`http://www.rmzxw.com.cn/c/2018-10-30/2204420.shtml`。
- 取正文：

  ```bash
  curl -s -m 25 -A 'Mozilla/5.0 …' 'http://www.rmzxw.com.cn/c/2018-10-30/2204420.shtml'
  ```

## 坑

- 编码 UTF-8/GB2312 视页面（`iconv -f gb18030` 兜底）。
