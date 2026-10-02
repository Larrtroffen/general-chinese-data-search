# wechat-article-extractor —— 文章状态判定与元数据抽取

Node/JS 技能（`cheerio`+`request-promise`+`dayjs`+`qs`+`lodash.unescape`）：吃 `mp.weixin.qq.com` **URL 或 HTML**，
吐账号信息 + 文章元数据 + 正文 HTML。**⚠️ 无 LICENSE：只作品路参考，不直接引入**（135★）。

- 去哪找：repo https://github.com/freestylefly/wechat-article-extractor-skill ；核心 `scripts/extract.js`、`convert.js`；安装走 `git clone` 后 `npm install`。
- 什么时候用：**已有链接只要正文+元数据**；需要**判定一篇文章当前是什么状态**（还在 / 已删 / 违规 / 过期 / 已迁移 / 过度营销）。
  第二点是我们最缺的：搜狗召回的老文章**很可能已删除**，抓下来是空壳，需要可判定的错误码而不是「正文为空」。
- 怎么取：
  ```js
  const { extract } = require('./scripts/extract.js');
  const r = await extract('https://mp.weixin.qq.com/s?__biz=...', {
    shouldReturnContent: true,        // 返回 HTML 正文
    shouldFollowTransferLink: true,   // 跟进公众号迁移后的新链接
    shouldExtractMpLinks: false,      // 夹带的其它 mp 链接
    shouldExtractTags: false, shouldExtractRepostMeta: false,
  });
  // 也行：const html = await fetch(url).then(r=>r.text()); await extract(html, {url});
  ```
  结果形态：JSON（URL 或 HTML 入参均可）。
- 覆盖：单篇；支持 `post/video/image/voice/text/repost` 多形态；声明可从**搜狗微信结果页 HTML** 提取（未本机验证）。
- 门槛：无（Node/JS，无需 key；⚠️ 无 LICENSE，只作品路参考，不直接引入）
- 实测：2026-10-02 **未安装 npm 依赖、未运行抽取**。已做证据：`gh api repos/freestylefly/wechat-article-extractor-skill --jq '.license.spdx_id,.default_branch,.stargazers_count'` → `null(master) / 135`；`curl https://raw.githubusercontent.com/freestylefly/wechat-article-extractor-skill/master/SKILL.md` → 4586 B（错误码表按原文抄录）。
- 上游：https://github.com/freestylefly/wechat-article-extractor-skill

## 细节

### 返回字段

- 账号 `account_name/account_alias/account_avatar/account_description/account_id/account_biz/account_qr_code`；
- 文章 `msg_title/msg_desc/msg_content(HTML)/msg_cover/msg_author/msg_type(post|video|image|voice|text|repost)/msg_has_copyright/msg_publish_time(_str)`；
- 身份 `msg_mid/msg_idx/msg_sn/msg_link/msg_source_url`（`sn` 可直接做去重主键，与 `wechatspider` 的 `--biz`、`mp.weixin` 通道互通）。

### 状态/错误码表（本卡重点，判定「这篇文章还能不能用」）

`1004 访问过于频繁`（限流，降速重试）｜`1006 公众号已迁移`｜`2002 链接已过期`｜`2003 内容涉嫌侵权`｜`2005 内容已被发布者删除`｜
`2006 内容因违规无法查看`｜`2011 涉嫌过度营销`｜`2012 账号已被屏蔽`｜`2013 账号已自主注销`｜`2014 内容被投诉`｜
`2015 账号处于迁移流程中`｜`2016 冒名侵权`。→ 2003/2005/2006/2012/2013/2016 属**不可恢复**，采集报表里应直接标记而不是反复重试。

## 坑

- 需先有链接（**不能搜索、不能列号内文章**）。
- 依赖较老的 `request-promise`。
- 无 LICENSE（合规风险）。
- 字段随页面结构变化可能为空。
