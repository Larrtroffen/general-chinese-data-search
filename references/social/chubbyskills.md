# chubbyskills —— 链接转 Markdown 的采集技能集

MIT，1.1k★，Python 3.11/3.12（macOS/Linux）。一整套「平台链接 → Markdown 原文 + 附件 → 本地搜索 → 带出处资料包」的
Agent Skills + CLI（`tools/chubby.py`），产物落本地 Markdown（可接 Obsidian）。**它把每个平台的「轻量路径/重依赖路径」写得很清楚**，是我们判断「某个平台值不值得采」的现成参考表。

- 去哪找：repo https://github.com/chubbyguan/chubbyskills ；每个平台一个 skill 目录（含 `SKILL.md`+`requirements.txt`+`scripts`）；平台参数在 `platforms/*.yaml`；统一 CLI `python3 tools/chubby.py …`；安装器 `tools/install_skill.py`（拒绝覆盖同名技能）。
- 什么时候用：要给 agent 装**中文平台的采集技能**（触发词：B站字幕、抖音/微博/知乎视频转文字、播客转录、公众号文章转 Markdown、小红书图文、X/Twitter）；或要一份「各平台怎么采、依赖什么、失败怎么办」的**平台状态参考**（`docs/platform-status.md`、`docs/live-verification.md`）。
- 怎么取：
  ```bash
  bash setup.sh light                        # 检查 Python；不装转录依赖
  python3 tools/chubby.py doctor --platform youtube
  python3 tools/chubby.py ingest "<链接>" --no-enrich      # 采集入库（默认不做摘要加工）
  python3 tools/chubby.py import "/path/report.pdf" --no-enrich
  python3 tools/chubby.py run --queue inbox/links.txt --no-enrich ; python3 tools/chubby.py status --failed ; python3 tools/chubby.py retry --all-failed
  python3 tools/install_skill.py --list      # 14 个技能；可 --all --dest <agent skills 目录>
  ```
  结果形态：本地 Markdown 文件（+ 附件）。
- 覆盖：14 个 skill（字幕/转录/文章入库/知识库等）；字幕类依赖 `yt-dlp`/`ffmpeg`/转录模型；**只处理给你的链接，不支持账号扫描**。
- 门槛：无 key（云转录后端需自配凭据且可能计费；重依赖需 ffmpeg + 模型下载）
- 实测：2026-10-02 **未安装、未运行 `chubby.py`**。证据：`gh api repos/chubbyguan/chubbyskills --jq '.license.spdx_id,.stargazers_count,.pushed_at'` → `MIT / 1160 / 2026-10-02`；逐目录核对 `gh api repos/chubbyguan/chubbyskills/contents/<dir> --jq '[.[]|.name]|join(", ")'`：11 个 skill 目录返回 `SKILL.md, requirements.txt, scripts`，`platforms/` 返回 10 个 yaml（bilibili/douyin/podcast/tiktok/wechat/weibo/x/xiaohongshu/youtube/zhihu）。
- 上游：https://github.com/chubbyguan/chubbyskills

## 细节

### Skill 目录（14 个，已核对目录存在）

`bilibili-transcribe`、`youtube-transcribe`、`douyin-transcribe`、`tiktok-transcribe`、
`weibo-transcribe`、`zhihu-transcribe`、`podcast-transcribe`、`wechat-article-ingest`、`xiaohongshu-ingest`、`x-ingest`、
`content-enrich`、`knowledge-base-management`（含 MCP：搜索/语义检索/读原文/最近笔记/重建索引/统计 6 工具）、
`industry-intelligence-radar`、`learning-notes-automation`。

### 平台可用性速览（上游声明，附其轻量路径）

- B站/YouTube **稳定**（字幕优先，仅需 `yt-dlp`）
- 公众号 **测试**（HTML 需 `beautifulsoup4`，PDF 兜底）
- 抖音/TikTok/微博/知乎 **测试·重依赖**（转录音频需 `funasr`+`ffmpeg`）
- 播客 **重依赖**（`faster-whisper`，可选云转录=会计费）
- X/小红书 **手动兜底**（零依赖采正文，失败手补）
- RSS/YouTube 频道订阅 **P0+P1**（首次同步只建基线，审核后再 `auto_ingest`）
- 本地文档 **稳定**（Markdown/TXT/PDF 文字层，不做 OCR）

## 坑

- 字幕/转录依赖重（ffmpeg、模型首次下载）。
- 平台抓取受 Cookie/地区/页面变化影响。
- 小红书/X/抖音/B站/公众号**账号扫描未支持**（只处理给你的链接）。
- 云转录后端需自配凭据且可能计费。
- 上游只保证「声明能力 ≠ 实时可用」，实测结果另记在 docs。
