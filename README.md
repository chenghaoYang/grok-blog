# Grok博客（grok-blog）

开源有声博客工坊：把公开书籍/文章切成可听章节，用 **Grok Voice** 生成中文朗读，并按 **主题 → 书籍 → 剧集** 归档（脚本 · 音频）。

## 目录结构

```text
catalog.yaml
books/
  <主题>/
    <书籍-slug>/
      book.yaml          # 元数据与来源
      INDEX.md           # 发布顺序
      episodes/
        00-.../
          script.md      # 可朗读脚本文
          meta.json
          audio.mp3      # Grok Voice（Git LFS：**/*.mp3）
          images/        # 优先原书插图
tools/
  produce_episode.py     # Grok Voice TTS CLI
  README.md
.github/workflows/
  produce-episode.yml    # workflow_dispatch
```

音频文件通过 Git LFS 跟踪：`**/*.mp3`。

## 当前书目

| 主题 | 书籍 | 作者 | 状态 |
| --- | --- | --- | --- |
| 软件工程 | [《软件设计的哲学》第二版中译](books/software-engineering/a-philosophy-of-software-design/) | John Ousterhout | 制作中（前言 + 1–22 章 + 总结；00–03 已有脚本） |

来源仓库：[yingang/aposd2e-zh](https://github.com/yingang/aposd2e-zh)（[CC-BY 4.0](https://github.com/yingang/aposd2e-zh/blob/main/LICENSE)）。已完成剧集的脚本文为口语化改编，非原文照搬；请保留署名。请勿编造未出现在来源中的书籍事实。章节标题见该书 `INDEX.md`。

## 用 Grok Voice 制作一集

引擎：xAI Grok Voice TTS（`https://api.x.ai/v1/tts`）。默认音色 `ara`，语言 `zh`。

需要 [xAI API key](https://docs.x.ai/)（环境变量 / GitHub secret：`XAI_API_KEY`，或本机 `~/.grok/auth.json`）。

```sh
export XAI_API_KEY=your-key
python tools/produce_episode.py --script tools/examples/hello-zh.txt --output /tmp/hello.mp3

# 与 main 上已有用法兼容：位置参数，默认写出同目录 audio.mp3
python tools/produce_episode.py books/software-engineering/a-philosophy-of-software-design/episodes/00-preface/script.md

python tools/produce_episode.py --episode books/software-engineering/a-philosophy-of-software-design/episodes/00-preface
```

仓库已配置 GitHub Actions：`Actions → Produce episode → Run workflow`。详细参数见 [tools/README.md](tools/README.md)。

## 许可

- 生产脚本与仓库脚手架：[MIT](LICENSE)
- 书籍改编内容：遵循原译 CC-BY 4.0，并保留原作者 / 译者署名
