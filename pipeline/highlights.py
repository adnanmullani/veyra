"""AI best moments dhundta hai, score deta hai, aur top N clips choose karta hai."""
import numpy as np
from llm.client import chat_json

WINDOW_SEC = 600  # 10 min ke tukde, taaki chhota local model bhi handle kar sake

SYSTEM = """You are an expert short form video editor for creators around the world.
From a timestamped transcript, pick the best standalone clips for YouTube Shorts, Instagram Reels and TikTok.
{hint}
Each clip must be between {min_sec} and {max_sec} seconds and must start and end at sentence boundaries.
Write each title in {title_lang}.
Return JSON: {{"clips": [{{"start": <sec>, "end": <sec>, "score": <1 to 100>, "title": "<short catchy title>", "reason": "<why this works>"}}]}}
Return at most 5 clips for this part. If nothing is good, return {{"clips": []}}."""


def _windows(segments):
    if not segments:
        return
    cur, start = [], segments[0]["start"]
    for s in segments:
        if s["start"] - start > WINDOW_SEC and cur:
            yield cur
            cur, start = [], s["start"]
        cur.append(s)
    if cur:
        yield cur


def _overlap(a, b):
    return max(0, min(a["end"], b["end"]) - max(a["start"], b["start"]))


def find_highlights(segments, energy: np.ndarray, preset: dict, count: int = 4, language: str = "en"):
    title_lang = ("Roman script Hinglish (never Devanagari)" if language == "hi"
                  else "the same language as the transcript")
    system = SYSTEM.format(hint=preset["ai_hint"], min_sec=preset["min_sec"],
                           max_sec=preset["max_sec"], title_lang=title_lang)
    candidates = []

    for n, win in enumerate(_windows(segments), 1):
        text = "\n".join(f'[{s["start"]:.1f} to {s["end"]:.1f}] {s["text"]}' for s in win)
        print(f"   part {n} analyse ho raha hai...")
        try:
            data = chat_json(system, text)
        except Exception as e:
            print(f"   part {n} skip ({e})")
            continue
        for c in data.get("clips", []):
            try:
                start, end = float(c["start"]), float(c["end"])
            except (KeyError, TypeError, ValueError):
                continue
            if end <= start:
                continue
            end = min(end, start + preset["max_sec"])
            if end - start < preset["min_sec"] * 0.75:
                continue
            e = energy[int(start) : max(int(start) + 1, int(end))]
            audio_bonus = float(e.mean()) * 15 if len(e) else 0.0
            candidates.append({
                "start": start, "end": end,
                "score": float(c.get("score", 50)) + audio_bonus,
                "title": c.get("title", "Clip"),
                "reason": c.get("reason", ""),
            })

    candidates.sort(key=lambda c: c["score"], reverse=True)
    picked = []
    for c in candidates:
        if all(_overlap(c, p) < 3 for p in picked):
            picked.append(c)
        if len(picked) == count:
            break
    return picked
