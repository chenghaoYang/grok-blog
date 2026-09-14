#!/usr/bin/env python3
"""Produce a Grok博客 episode MP3 via the xAI Grok Voice TTS API.

Calls https://api.x.ai/v1/tts with voice_id=ara and language=zh by default.
Auth: environment variable XAI_API_KEY (GitHub Actions secret of the same name).

Stdlib only. Example:

    export XAI_API_KEY=...
    python tools/produce_episode.py --script path/to/script.md
    python tools/produce_episode.py --episode books/.../episodes/ch01
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

TTS_URL = "https://api.x.ai/v1/tts"
DEFAULT_VOICE_ID = "ara"
DEFAULT_LANGUAGE = "zh"
MAX_CHARS = 15_000
DEFAULT_TIMEOUT_S = 180
RETRYABLE_STATUS = frozenset({429, 500, 502, 503, 504})


class ProduceError(RuntimeError):
    """User-facing production failure."""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Synthesize a Grok博客 episode with xAI Grok Voice TTS.",
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--script", type=Path, help="Path to a UTF-8 script file.")
    source.add_argument("--text", help="Inline text to synthesize.")
    source.add_argument(
        "--episode",
        type=Path,
        help="Episode directory containing script.md (or script.txt).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output MP3 path. Default: next to the script as audio.mp3.",
    )
    parser.add_argument("--voice-id", default=DEFAULT_VOICE_ID, help="TTS voice_id.")
    parser.add_argument("--language", default=DEFAULT_LANGUAGE, help="BCP-47 language.")
    parser.add_argument(
        "--speed",
        type=float,
        default=None,
        help="Optional speech speed multiplier (API range 0.7–1.5).",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT_S,
        help=f"HTTP timeout in seconds (default {DEFAULT_TIMEOUT_S}).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate input and print request metadata without calling the API.",
    )
    return parser.parse_args(argv)


def resolve_script_path(args: argparse.Namespace) -> Path | None:
    if args.script is not None:
        return args.script
    if args.episode is not None:
        for name in ("script.md", "script.txt", "script"):
            candidate = args.episode / name
            if candidate.is_file():
                return candidate
        raise ProduceError(
            f"No script.md or script.txt found in episode directory: {args.episode}"
        )
    return None


def load_text(args: argparse.Namespace) -> str:
    if args.text is not None:
        text = args.text
    else:
        script_path = resolve_script_path(args)
        assert script_path is not None
        try:
            text = script_path.read_text(encoding="utf-8")
        except OSError as exc:
            raise ProduceError(f"Cannot read script {script_path}: {exc}") from exc
    text = text.strip()
    if not text:
        raise ProduceError("Script text is empty.")
    return text


def resolve_output(args: argparse.Namespace) -> Path:
    if args.output is not None:
        return args.output
    if args.episode is not None:
        return args.episode / "audio.mp3"
    if args.script is not None:
        return args.script.with_name("audio.mp3")
    return Path("audio.mp3")


def require_api_key() -> str:
    api_key = os.environ.get("XAI_API_KEY", "").strip()
    if not api_key:
        raise ProduceError(
            "Missing XAI_API_KEY. Export it in your shell or set the "
            "GitHub Actions secret of the same name."
        )
    return api_key


def split_chunks(text: str, max_chars: int = MAX_CHARS) -> list[str]:
    """Split text into TTS-sized chunks on paragraph/sentence boundaries."""
    if len(text) <= max_chars:
        return [text]

    chunks: list[str] = []
    remaining = text
    while remaining:
        if len(remaining) <= max_chars:
            chunks.append(remaining)
            break
        window = remaining[:max_chars]
        cut = -1
        for separator in ("\n\n", "\n", "。", "！", "？", "；", ".", "!", "?", ";", " "):
            cut = window.rfind(separator)
            if cut >= max_chars // 4:
                cut += len(separator)
                break
            cut = -1
        if cut <= 0:
            cut = max_chars
        piece = remaining[:cut].strip()
        if not piece:
            raise ProduceError("Unable to split script into non-empty TTS chunks.")
        chunks.append(piece)
        remaining = remaining[cut:].lstrip()
    return chunks


def build_payload(
    text: str,
    *,
    voice_id: str,
    language: str,
    speed: float | None,
) -> dict:
    payload: dict = {
        "text": text,
        "voice_id": voice_id,
        "language": language,
        "output_format": {
            "codec": "mp3",
            "sample_rate": 44100,
            "bit_rate": 192000,
        },
    }
    if speed is not None:
        payload["speed"] = speed
    return payload


def synthesize_chunk(
    payload: dict,
    *,
    api_key: str,
    timeout: int,
    retries: int = 3,
) -> bytes:
    body = json.dumps(payload).encode("utf-8")
    last_error: Exception | None = None
    for attempt in range(retries):
        request = urllib.request.Request(
            TTS_URL,
            data=body,
            method="POST",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "audio/mpeg, application/octet-stream, */*",
                "User-Agent": "grok-blog/produce_episode",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                audio = response.read()
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            last_error = ProduceError(
                f"TTS HTTP {exc.code} {exc.reason}: {detail[:800]}"
            )
            if exc.code in RETRYABLE_STATUS and attempt < retries - 1:
                time.sleep(2**attempt)
                continue
            raise last_error from exc
        except urllib.error.URLError as exc:
            last_error = ProduceError(f"TTS request failed: {exc.reason}")
            if attempt < retries - 1:
                time.sleep(2**attempt)
                continue
            raise last_error from exc
        if not audio:
            raise ProduceError("TTS returned an empty body.")
        return audio
    raise last_error or ProduceError("TTS request failed.")


def write_mp3(path: Path, parts: list[bytes]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as handle:
        for part in parts:
            handle.write(part)


def produce(args: argparse.Namespace) -> Path:
    text = load_text(args)
    output = resolve_output(args)
    chunks = split_chunks(text)

    if args.dry_run:
        print(
            json.dumps(
                {
                    "url": TTS_URL,
                    "voice_id": args.voice_id,
                    "language": args.language,
                    "chars": len(text),
                    "chunks": len(chunks),
                    "chunk_sizes": [len(chunk) for chunk in chunks],
                    "output": str(output),
                    "has_api_key": bool(os.environ.get("XAI_API_KEY", "").strip()),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return output

    api_key = require_api_key()
    parts: list[bytes] = []
    for index, chunk in enumerate(chunks, start=1):
        print(
            f"Synthesizing chunk {index}/{len(chunks)} ({len(chunk)} chars) → {TTS_URL}",
            file=sys.stderr,
        )
        payload = build_payload(
            chunk,
            voice_id=args.voice_id,
            language=args.language,
            speed=args.speed,
        )
        parts.append(
            synthesize_chunk(payload, api_key=api_key, timeout=args.timeout)
        )

    write_mp3(output, parts)
    size = output.stat().st_size
    print(f"Wrote {size:,} bytes to {output}", file=sys.stderr)
    print(output.resolve())
    return output


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        produce(args)
    except ProduceError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
