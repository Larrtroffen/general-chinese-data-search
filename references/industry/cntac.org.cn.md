# cntac.org.cn —— 纺织行业数据分析栏目

- 去哪找：官网 `https://www.cntac.org.cn/`；数据分析栏目 `https://www.cntac.org.cn/zixun/shuju/`；行业栏目 `https://www.cntac.org.cn/zixun/hangye/`（三条 URL 来自检索结果，**未本机实测**）
- 什么时候用：要中国纺织工业联合会口径的行业运行分析、纺织经济数据解读时。
- 怎么搜：栏目页 + 年月目录，形如 `…/zixun/shuju/{YYYYMM}/t{YYYYMMDD}_{id}.html`（由检索结果条目 URL 归纳，未本机验证）：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  curl -sS -L -A "$UA" 'https://www.cntac.org.cn/zixun/shuju/'
  ```
- 覆盖：未知（本机不可达）；检索结果中「数据分析」栏目内含 2026-02、2026-08 等条目。
- 门槛：未知。
- 实测：2026-10-03 本机（macOS arm64，curl 8.x，桌面 UA，20 s 超时）**四次尝试全部失败 ❌**——`https://www.cntac.org.cn/` 与 `https://cntac.org.cn/zixun/shuju/` → `SSL_ERROR_SYSCALL`（TLS 握手被中断）；`http://www.cntac.org.cn/` 与 `http://cntac.org.cn/` → `Empty reply from server`；同体系门户 `https://www.ctei.cn/`（中国纺织经济信息网）→ 443 也无法建立连接。
- 上游：中国纺织工业联合会。

## 坑

1. **本机网络不可达**（TLS 中断 / 空响应），可能是站点侧限制或链路问题——不要据此判定站点下线；换网络/浏览器再试。
2. 用浏览器确认入口前，别把 `cntac.org.cn` 写进自动化脚本的必跑链路。
3. 替代线索：纺织运行数据可先用国家统计局与工信部消费品工业司口径兜底（`../stats/ministry-stats.md`）。
