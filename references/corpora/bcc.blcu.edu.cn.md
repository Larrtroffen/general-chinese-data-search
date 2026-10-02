# bcc.blcu.edu.cn —— 北语 BCC 多领域语料库

- 去哪找：检索系统 `https://bcc.blcu.edu.cn/`（Vue SPA）；公开数据接口 `https://bcc.blcu.edu.cn/api/datasets`。
- 什么时候用：要**例句/搭配/索引行**，且需要**多领域**覆盖（文学、新闻、口语、科技、微博、古汉语、近代汉语…）；要**现成的字频/词频表**做词表、停用词、统计；比 CCL 更偏"大规模 + 网络语料"。
- 怎么搜：**检索**走 SPA 内部 `POST /api/search`，但**需先过验证码**（`GET /api/captcha/challenge` → 提交 `POST /api/captcha/verify`）；匿名直接 POST 被拒。**字/词频表可匿名直下**，不必登录：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  curl -s -A "$UA" 'https://bcc.blcu.edu.cn/api/datasets'                      # 12 个频表清单（JSON）
  curl -s -A "$UA" -o classical.zip \
    'https://bcc.blcu.edu.cn/api/datasets/classical_chinese_char_freq.txt/download'   # 返回 zip
  ```
- 覆盖：**12 个频表 = 6 频道 × {字频, 词频}**：口语 / 古代汉语 / 多领域 / 文学 / 新闻 / 近代汉语；接口 `updated_at` 统一为 2026-05-22。检索端频道同上（语料总量上游称约数十亿字，**未本机核实**）。
- 门槛：字词频表**免费、免登录**（实测匿名可取）；**在线检索需过验证码**（SPA，可能叠加登录/额度）。
- 实测：2026-10-03，macOS arm64，curl 8.x，桌面 UA，同主机间隔 ≥1.5 s：`GET /` → 200（403 B，Vue 空壳，标题「BCC语料库检索系统」）；`GET /api/datasets` → 200，12 条；`GET /api/datasets/classical_chinese_char_freq.txt/download` → 200 / 82,379 B / `application/zip`（`PK` 头）；`POST /api/search {"q":"经济"}` → **403** `{"detail":"需要验证码验证","captcha_required":true}`。
- 上游：北京语言大学 语料库语言学研究所（BCC = BLCU Chinese Corpus）。入口 `https://bcc.blcu.edu.cn/`。

## 细节

### 频表清单（2026-10-03，`GET /api/datasets` 实测）

| filename | 频道 | 粒度 | size_bytes |
|---|---|---|---|
| `dialogue_char_freq.txt` / `dialogue_word_freq.txt` | 口语 | 字 / 词 | 49,553 / 1,507,322 |
| `classical_chinese_char_freq.txt` / `classical_chinese_word_freq.txt` | 古代汉语 | 字 / 词 | 169,256 / 169,256 |
| `multi_domain_total_char_freq.txt` / `multi_domain_total_word_freq.txt` | 多领域 | 字 / 词 | 68,740 / 5,542,891 |
| `literature_char_freq.txt` / `literature_word_freq.txt` | 文学 | 字 / 词 | 59,429 / 1,989,087 |
| `news_total_char_freq.txt` / `news_total_word_freq.txt` | 新闻 | 字 / 词 | 73,308 / 11,510,206 |
| `modern_chinese_char_freq.txt` / `modern_chinese_word_freq.txt` | 近代汉语 | 字 / 词 | 77,839 / 15,698,705 |

字段：`filename` / `display_name` / `channel` / `token_type`(`char`|`word`) / `freq_type`(`freq`) / `format`(`txt`) / `size_bytes` / `updated_at` / `token_column` / `count_column`。

### 检索接口（未跑通，SPA 逆向）

| 端点 | 方法 | 说明 |
|---|---|---|
| `/api/search` | POST | 关键词检索，**需 captcha token**（实测 403） |
| `/api/captcha/challenge` | GET | 取验证码挑战 |
| `/api/captcha/verify` | POST | 校验验证码，通过后才放行检索 |
| `/api/datasets` | GET | 频表清单（匿名 ✅） |
| `/api/datasets/{filename}/download` | GET | 频表 zip 直下（匿名 ✅） |
| `/api/site/channels-config` | GET | 频道/资源配置 |
| `/api/datasets/{name}/search?token=` | GET | 数据集内检索 |

## 坑

1. 首页是**纯前端 SPA**，curl 只拿到 403 B 空壳，标题在 `<title>` 里；**不要试图解析 HTML 取结果**。
2. `/api/search` 有**验证码墙**，脚本化批量检索不可行；批量取词频请直接下 `/api/datasets/*`。
3. 频表下载返回的是 **zip**（内含同名 `.txt`），不是裸文本；解压后 `token` + `count` 两列。
4. 频表只有"频道汇总"，**不含出处/句子**；要索引行必须走页面检索。
