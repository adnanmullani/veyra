"""Veyra Phase 1: long video do, best Shorts captions ke saath pao (kisi bhi language mein).

Usage:
    python main.py samples/myvideo.mp4
    python main.py samples/myvideo.mp4 --count 4 --preset talking
"""
import argparse
import json
from pathlib import Path

from presets import PRESETS
from pipeline.audio import extract_audio, energy_per_second
from pipeline.transcribe import transcribe
from pipeline.hinglish import needs_hinglish, to_hinglish
from pipeline.highlights import find_highlights
from pipeline.render import render_short


def main():
    ap = argparse.ArgumentParser(description="AI se long video ke best Shorts")
    ap.add_argument("video")
    ap.add_argument("--count", type=int, default=4)
    ap.add_argument("--preset", default="talking", choices=PRESETS.keys())
    ap.add_argument("--out", default="outputs")
    args = ap.parse_args()

    preset = PRESETS[args.preset]
    out = Path(args.out) / Path(args.video).stem
    out.mkdir(parents=True, exist_ok=True)

    print("1/5 Audio nikaal rahe hain...")
    wav = extract_audio(args.video, str(out / "audio.wav"))
    energy = energy_per_second(wav)

    print("2/5 Transcript bana rahe hain (Whisper)...")
    segments, language = transcribe(wav)

    if needs_hinglish(segments, language):
        print("3/5 Captions ko Roman Hinglish mein convert kar rahe hain...")
        segments = to_hinglish(segments)
    else:
        print(f"3/5 Captions original language ({language}) mein hi rahenge...")
    (out / "transcript.json").write_text(json.dumps(segments, ensure_ascii=False, indent=2), encoding="utf-8")

    print("4/5 AI best moments dhund raha hai...")
    clips = find_highlights(segments, energy, preset, args.count, language)
    if not clips:
        print("Koi achha clip nahi mila. Doosra video try karo ya model badlo.")
        return

    print(f"5/5 {len(clips)} Shorts render ho rahe hain...")
    for i, c in enumerate(clips, 1):
        path = render_short(args.video, c, segments, preset, out, i)
        c["file"] = str(path)
        print(f"   #{i} [{c['score']:.0f}] {c['title']}  ->  {path}")

    (out / "clips.json").write_text(json.dumps(clips, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nHo gaya! Output folder: {out}")


if __name__ == "__main__":
    main()
