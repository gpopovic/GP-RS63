"""Run local, offline transcription through faster-whisper.

The model download happens only during an explicit warm-up. Once warmed, use
``--offline`` to prevent any network model lookup during transcription.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Iterable

from faster_whisper import WhisperModel

ENGINE_DIR = Path(__file__).resolve().parents[1]
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

from config import LOCAL_TRANSCRIPTION_MODEL_DIR


def format_timestamp(seconds: float, separator: str = ",") -> str:
    """Return an SRT-compatible timestamp."""
    milliseconds = round(seconds * 1_000)
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds_part, milliseconds = divmod(remainder, 1_000)
    return f"{hours:02}:{minutes:02}:{seconds_part:02}{separator}{milliseconds:03}"


def write_transcript(
    segments: Iterable[object], text_path: Path, srt_path: Path
) -> int:
    """Write plain-text and timed SRT outputs without modifying the source audio."""
    text_lines: list[str] = []
    srt_blocks: list[str] = []
    for index, segment in enumerate(segments, start=1):
        text = segment.text.strip()
        if not text:
            continue
        text_lines.append(text)
        srt_blocks.append(
            f"{index}\n"
            f"{format_timestamp(segment.start)} --> {format_timestamp(segment.end)}\n"
            f"{text}\n"
        )
    text_path.write_text("\n".join(text_lines) + "\n", encoding="utf-8")
    srt_path.write_text("\n".join(srt_blocks), encoding="utf-8")
    return len(srt_blocks)


def parse_args() -> argparse.Namespace:
    """Parse a deliberately small, auditable local-transcription interface."""
    parser = argparse.ArgumentParser(description="Transcribe audio locally with faster-whisper.")
    parser.add_argument("audio", nargs="?", type=Path, help="Local audio or video file to transcribe.")
    parser.add_argument("--output-dir", type=Path, help="Destination for .txt and .srt files.")
    parser.add_argument("--model", default="small", help="Whisper model size or approved local model path.")
    parser.add_argument("--language", default="de", help="Spoken language code, or 'auto' for detection.")
    parser.add_argument("--beam-size", type=int, default=5, help="Decoding breadth; use 1 only for a labelled discovery pass.")
    parser.add_argument("--offline", action="store_true", help="Use only a previously downloaded model.")
    parser.add_argument("--warmup", action="store_true", help="Download and validate the selected model only.")
    return parser.parse_args()


def main() -> None:
    """Warm a local model or produce local transcript files."""
    args = parse_args()
    LOCAL_TRANSCRIPTION_MODEL_DIR.mkdir(parents=True, exist_ok=True)
    if not args.warmup and args.audio is None:
        raise SystemExit("Provide an audio path or use --warmup.")
    if args.audio is not None and not args.audio.is_file():
        raise SystemExit(f"Audio file not found: {args.audio}")

    model = WhisperModel(
        args.model,
        device="cpu",
        compute_type="int8",
        cpu_threads=8,
        download_root=str(LOCAL_TRANSCRIPTION_MODEL_DIR),
        local_files_only=args.offline,
    )
    if args.warmup:
        print(f"Local transcription model ready: {args.model}")
        return

    output_dir = args.output_dir or args.audio.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    language = None if args.language.casefold() == "auto" else args.language
    segments, info = model.transcribe(
        str(args.audio),
        language=language,
        beam_size=args.beam_size,
        vad_filter=True,
        condition_on_previous_text=True,
    )
    text_path = output_dir / f"{args.audio.stem}.txt"
    srt_path = output_dir / f"{args.audio.stem}.srt"
    segment_count = write_transcript(segments, text_path, srt_path)
    print(
        f"Transcribed {segment_count} segments ({info.language}, "
        f"probability {info.language_probability:.2f}) to {text_path.name} and {srt_path.name}."
    )


if __name__ == "__main__":
    main()
