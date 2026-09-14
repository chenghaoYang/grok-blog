# TTS tools

`produce_episode.py` turns a UTF-8 episode script into an MP3 via the
[xAI Text to Speech API](https://docs.x.ai/developers/model-capabilities/audio/text-to-speech).

## Requirements

- Python 3.9+ (stdlib only; no `pip` packages)
- Environment variable `XAI_API_KEY`

Default synthesis settings:

| Field | Value |
| --- | --- |
| Endpoint | `https://api.x.ai/v1/tts` |
| `voice_id` | `ara` |
| `language` | `zh` |
| Output | MP3 |

Scripts longer than 15,000 characters are split on paragraph/sentence
boundaries and the MP3 parts are concatenated in order.

## Local usage

```sh
export XAI_API_KEY=your-key

# From a script file (writes audio.mp3 next to the script)
python tools/produce_episode.py --script path/to/script.md

# From an episode directory that contains script.md
python tools/produce_episode.py --episode books/software-engineering/a-philosophy-of-software-design/episodes/ch01

# Inline text and explicit output path
python tools/produce_episode.py --text "你好，欢迎收听 Grok博客。" --output /tmp/hello.mp3

# Validate without calling the API
python tools/produce_episode.py --script path/to/script.md --dry-run
```

Smoke-test copy (not book content) lives at `tools/examples/hello-zh.txt`.

## GitHub Actions

Workflow: [`.github/workflows/produce-episode.yml`](../.github/workflows/produce-episode.yml).

1. Add repository secret `XAI_API_KEY`.
2. Run **Actions → Produce episode → Run workflow**.
3. Provide either `episode_path` (directory with `script.md`) or `script_path`.
4. The job uploads the MP3 as an artifact. Set `commit` to true to push the
   file back with Git LFS (`**/*.mp3`).
