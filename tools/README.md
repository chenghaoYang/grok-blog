# 生产工具

## `produce_episode.py`

从脚本文调用 Grok Voice TTS，写出 `audio.mp3`。

```bash
export XAI_API_KEY=...   # 或依赖本机 ~/.grok/auth.json
python tools/produce_episode.py path/to/episode/script.md
```

## GitHub Actions

`.github/workflows/produce-episode.yml`：`workflow_dispatch` 指定书籍与集号后生成音频（需仓库 Secret `XAI_API_KEY`）。
