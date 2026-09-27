"""FFmpeg se 9:16 Short banana, captions burn karke."""
import subprocess
from pathlib import Path


def _ts(sec: float) -> str:
    ms = int(round(max(0.0, sec) * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def write_srt(segments, start, end, path: Path):
    lines, n = [], 1
    for s in segments:
        if s["end"] <= start or s["start"] >= end:
            continue
        a, b = max(s["start"], start) - start, min(s["end"], end) - start
        lines.append(f"{n}\n{_ts(a)} --> {_ts(b)}\n{s['text']}\n")
        n += 1
    path.write_text("\n".join(lines), encoding="utf-8")


def render_short(video: str, clip: dict, segments, preset: dict, out_dir: Path, idx: int) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    srt_name = f"short_{idx}.srt"
    write_srt(segments, clip["start"], clip["end"], out_dir / srt_name)
    out_name = f"short_{idx}.mp4"

    vf = (
        "crop='min(iw,ih*9/16)':ih,"
        "scale=1080:1920,"
        f"subtitles={srt_name}:force_style='{preset['caption_style']}'"
    )
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(clip["start"]), "-to", str(clip["end"]),
        "-i", str(Path(video).resolve()),
        "-vf", vf,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
        "-c:a", "aac", "-b:a", "160k",
        out_name,
    ]
    subprocess.run(cmd, check=True, capture_output=True, cwd=out_dir)
    return out_dir / out_name
