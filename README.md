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
| 软件工程 | [《软件设计的哲学》第二版中译](books/software-engineering/a-philosophy-of-software-design/) | John Ousterhout | 00–23 共 24 集脚本齐全，音频已登记为 Git LFS 对象 |

来源仓库：[yingang/aposd2e-zh](https://github.com/yingang/aposd2e-zh)（[CC-BY 4.0](https://github.com/yingang/aposd2e-zh/blob/main/LICENSE)）。已完成剧集的脚本文为口语化改编，非原文照搬；请保留署名。请勿编造未出现在来源中的书籍事实。章节标题见该书 `INDEX.md`。

## 获取音频与制作

MP3 通过 Git LFS 保存。克隆后在已安装 Git LFS 的环境中运行 `git lfs pull` 获取音频；
仓库中的 LFS pointer 只表示对象已登记，不代表已试听或验证音质。

制作入口与全部参数见 [生产工具](tools/README.md)：本地 CLI 支持脚本文件、剧集目录和内联文本，
`--dry-run` 只校验、不调用 API。正式制作需要 xAI 凭证，会调用付费 TTS。
GitHub Actions 入口为 **Actions → Produce episode → Run workflow**；推回仓库需显式开启 `commit`。

## 许可

- 生产脚本与仓库脚手架：[MIT](LICENSE)
- 书籍改编内容：遵循原译 CC-BY 4.0，并保留原作者 / 译者署名
