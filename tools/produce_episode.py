#!/usr/bin/env python3
"""Generate audio.mp3 from an episode script.md via xAI Grok Voice TTS."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

API = "https://api.x.ai/v1/tts"
DEFAULT_VOICE = "ara"
DEFAULT_LANG = "zh"
MAX_CHARS = 14000


def load_bearer() -> str:
    env = os.environ.get("XAI_API_KEY")
    if env:
        return env
    auth_path = Path.home() / ".grok" / "auth.json"
    data = json.loads(auth_path.read_text())
    entry = next(iter(data.values()))
    return entry["key"]


def script_to_speech_text(md: str) -> str:
    lines = []
    for line in md.splitlines():
        if line.startswith("#"):
            continue
        lines.append(line)
    text = "\n".join(lines).strip()
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def chunk_text(text: str, limit: int = MAX_CHARS) -> list[str]:
    if len(text) <= limit:
        return [text]
    parts: list[str] = []
    buf: list[str] = []
    n = 0
    for para in re.split(r"(\n\n+)", text):
        if n + len(para) > limit and buf:
            parts.append("".join(buf).strip())
            buf, n = [], 0
        buf.append(para)
        n += len(para)
    if buf:
        parts.append("".join(buf).strip())
    return [p for p in parts if p]


def tts(text: str, voice: str, language: str, bearer: str) -> bytes:
    payload = json.dumps(
        {
            "text": text,
            "voice_id": voice,
            "language": language,
            "output_format": {
                "codec": "mp3",
                "sample_rate": 44100,
                "bit_rate": 192000,
            },
        }
    ).encode()
    req = urllib.request.Request(
        API,
        data=payload,
        headers={
            "Authorization": f"Bearer {bearer}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            body = e.read()[:300]
            if e.code in (429, 500, 503) and attempt < 3:
                time.sleep(2**attempt)
                continue
            raise RuntimeError(f"TTS HTTP {e.code}: {body!r}") from e
    raise RuntimeError("TTS failed")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("script", type=Path, help="path to script.md")
    ap.add_argument("--voice", default=DEFAULT_VOICE)
    ap.add_argument("--language", default=DEFAULT_LANG)
    ap.add_argument("-o", "--output", type=Path, default=None)
    args = ap.parse_args()
    script_path = args.script
    out = args.output or (script_path.parent / "audio.mp3")
    text = script_to_speech_text(script_path.read_text(encoding="utf-8"))
    if not text:
        print("empty script", file=sys.stderr)
        return 1
    bearer = load_bearer()
    chunks = chunk_text(text)
    audio = bytearray()
    for i, chunk in enumerate(chunks):
        print(f"TTS chunk {i+1}/{len(chunks)} chars={len(chunk)}", file=sys.stderr)
        audio.extend(tts(chunk, args.voice, args.language, bearer))
    out.write_bytes(audio)
    print(f"wrote {out} ({len(audio)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
