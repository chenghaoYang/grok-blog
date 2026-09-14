# 生产工具

`produce_episode.py` 把 UTF-8 剧集脚本合成 MP3，调用
[xAI Text to Speech API](https://docs.x.ai/developers/model-capabilities/audio/text-to-speech)。

## 要求

- Python 3.9+（仅标准库）
- 凭证：环境变量 `XAI_API_KEY`，或本机 `~/.grok/auth.json`

默认合成参数：

| Field | Value |
| --- | --- |
| Endpoint | `https://api.x.ai/v1/tts` |
| `voice_id` | `ara` |
| `language` | `zh` |
| Output | MP3 |

超过约 14,000 字的脚本会按段落/句子切开，再按顺序拼接 MP3。Markdown 标题行（`#`）不会送进 TTS。

## 本地用法

```sh
export XAI_API_KEY=your-key

# 位置参数（写出 script.md 同目录的 audio.mp3）
python tools/produce_episode.py path/to/episode/script.md

# 显式 --script
python tools/produce_episode.py --script path/to/script.md

# 剧集目录（内含 script.md）
python tools/produce_episode.py --episode books/software-engineering/a-philosophy-of-software-design/episodes/00-preface

# 内联文本
python tools/produce_episode.py --text "你好，欢迎收听 Grok博客。" -o /tmp/hello.mp3

# 不调用 API，只校验
python tools/produce_episode.py --script path/to/script.md --dry-run
```

冒烟测试文案（非书籍内容）在 `tools/examples/hello-zh.txt`。

## GitHub Actions

工作流：[`.github/workflows/produce-episode.yml`](../.github/workflows/produce-episode.yml)。

1. 添加仓库 Secret `XAI_API_KEY`。
2. 打开 **Actions → Produce episode → Run workflow**。
3. 填写 `episode_path`（含 `script.md` 的目录）或 `script_path`。
4. 任务会上传 MP3 artifact。将 `commit` 设为 true 时，会用 Git LFS（`**/*.mp3`）推回仓库。
