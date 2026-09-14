# Grok博客（grok-blog）

开源有声博客工坊：把公开书籍/文章切成可听章节，用 **Grok Voice** 生成中文朗读，并按 **主题 → 书籍 → 集** 归档。

## 目录结构

```
books/
  <主题>/
    <书籍-slug>/
      book.yaml          # 元数据与来源
      INDEX.md           # 发布顺序
      episodes/
        00-.../
          script.md      # 可朗读脚本文
          meta.json
          audio.mp3      # Grok Voice（可能经 Git LFS）
          images/        # 优先原书插图
tools/                   # 本地/CI 生产脚本
.github/workflows/       # 自动化
```

## 当前书目

| 主题 | 书籍 | 状态 |
|------|------|------|
| software-engineering | [《软件设计的哲学》第二版中译](books/software-engineering/a-philosophy-of-software-design/) | 制作中（前言 + 1–22 章 + 总结） |

来源仓库：[yingang/aposd2e-zh](https://github.com/yingang/aposd2e-zh)（CC-BY 4.0）。脚本文为口语化改编，非原文照搬；请保留署名。

## 语音

- 引擎：xAI Grok Voice TTS（`https://api.x.ai/v1/tts`）
- 默认音色：`ara` · 语言：`zh`

## 本地生产

见 [`tools/README.md`](tools/README.md)。需要可用的 xAI 凭证（`XAI_API_KEY` 或本机已登录的 Grok session）。

## 许可

- 生产脚本与仓库脚手架：MIT
- 书籍改编内容：遵循原译 CC-BY 4.0，并保留原作者 / 译者署名
