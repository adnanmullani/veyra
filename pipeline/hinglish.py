"""Captions ko Roman Hinglish mein convert karna. Devanagari ek bhi nahi bachegi."""
import json
import re
from indic_transliteration import sanscript
from llm.client import chat_json

DEVANAGARI = re.compile(r"[\u0900-\u097F]")

SYSTEM = """You convert subtitle lines into natural Roman script Hinglish, the way Indian creators write on Instagram and YouTube.
Rules:
1. English words stay exactly as English.
2. Hindi words are written in English letters with common casual spelling (hai, bahut, kya, nahi, mast, ekdum).
3. Never output Devanagari characters.
4. Do not translate Hindi into English. Keep the meaning and words as spoken.
5. Keep it short, no extra words.
Return JSON: {"lines": [{"id": <id>, "text": "<converted>"}]}"""


def _fallback(text: str) -> str:
    out = sanscript.transliterate(text, sanscript.DEVANAGARI, sanscript.ITRANS)
    return DEVANAGARI.sub("", out).lower()


def _convert_batch(batch: list[dict]) -> dict[int, str]:
    payload = json.dumps([{"id": s["id"], "text": s["text"]} for s in batch], ensure_ascii=False)
    try:
        data = chat_json(SYSTEM, "Convert these lines:\n" + payload)
        return {int(x["id"]): str(x["text"]).strip() for x in data.get("lines", [])}
    except Exception as e:
        print(f"   LLM batch fail hua ({e}), fallback use kar rahe hain")
        return {}


def needs_hinglish(segments: list[dict], language: str) -> bool:
    """Sirf Hindi/Hinglish videos ko convert karo. Baaki languages waise hi rahengi."""
    return language == "hi" or any(DEVANAGARI.search(s["text"]) for s in segments)


def to_hinglish(segments: list[dict], batch_size: int = 30) -> list[dict]:
    result = {s["id"]: s["text"] for s in segments}

    for i in range(0, len(segments), batch_size):
        converted = _convert_batch(segments[i : i + batch_size])
        result.update({k: v for k, v in converted.items() if k in result and v})

    # Check: jisme abhi bhi Devanagari hai, usko ek baar aur try karo, phir fallback
    bad = [s for s in segments if DEVANAGARI.search(result[s["id"]])]
    if bad:
        converted = _convert_batch([{**s, "text": result[s["id"]]} for s in bad])
        result.update({k: v for k, v in converted.items() if k in result and v})
        for s in bad:
            if DEVANAGARI.search(result[s["id"]]):
                result[s["id"]] = _fallback(result[s["id"]])

    return [{**s, "text": result[s["id"]]} for s in segments]
