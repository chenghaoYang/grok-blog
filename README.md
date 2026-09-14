# grok-blog

Grok博客：开源有声博客工坊。按主题 → 书籍 → 剧集组织中文音频，用 Grok Voice 生成可收听章节包（脚本 · 音频）。

本仓库是工坊脚手架：目录、元数据、TTS 命令行与 GitHub Actions。剧集脚本与 MP3 尚未收录。

## 目录结构

```text
catalog.yaml
books/
  software-engineering/
    a-philosophy-of-software-design/
      book.yaml
      INDEX.md
      episodes/          # 占位；每集日后为 <id>/script.md + audio.mp3
tools/
  produce_episode.py     # Grok Voice TTS CLI
  README.md
.github/workflows/
  produce-episode.yml    # workflow_dispatch
```

音频文件通过 Git LFS 跟踪：`**/*.mp3`。

## 当前书目

唯一已编目的书来自开源中文译本，不在此复述原书论点。

| 主题 | 书 | 作者 |
| --- | --- | --- |
| 软件工程 | [A Philosophy of Software Design, 2nd Edition《软件设计的哲学，第二版》](books/software-engineering/a-philosophy-of-software-design/INDEX.md) | John Ousterhout |

章节标题见该书 `INDEX.md`，与译本目录一致。

## 署名

《软件设计的哲学，第二版》中文译本：

- 仓库：[https://github.com/yingang/aposd2e-zh](https://github.com/yingang/aposd2e-zh)
- 许可：[CC-BY 4.0](https://github.com/yingang/aposd2e-zh/blob/main/LICENSE)

使用译本内容时请保留上述署名。请勿编造未出现在来源中的书籍事实。

## 用 Grok Voice 制作一集

需要 [xAI API key](https://docs.x.ai/)（环境变量 / GitHub secret：`XAI_API_KEY`）。默认 `voice_id=ara`，`language=zh`，请求 `https://api.x.ai/v1/tts`。

```sh
export XAI_API_KEY=your-key
python tools/produce_episode.py --script tools/examples/hello-zh.txt --output /tmp/hello.mp3
```

按剧集目录制作（目录内放 `script.md`）：

```sh
python tools/produce_episode.py --episode books/software-engineering/a-philosophy-of-software-design/episodes/ch01
```

仓库已配置 GitHub Actions：`Actions → Produce episode → Run workflow`。详细参数见 [tools/README.md](tools/README.md)。

## 许可

工坊代码与仓库脚手架采用 [MIT](LICENSE)。第三方译本内容仍按其自身许可（CC-BY 4.0）使用。
