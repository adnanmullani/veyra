"""Whisper se transcript with timestamps. Laptop pe free chalta hai."""
from faster_whisper import WhisperModel
import config


def transcribe(audio_path: str) -> tuple[list[dict], str]:
    """Segments aur detected language code (jaise 'en', 'hi', 'es') dono return karta hai."""
    model = WhisperModel(config.WHISPER_MODEL, device="auto", compute_type="int8")
    segments, info = model.transcribe(audio_path, vad_filter=True)
    print(f"   language detect hui: {info.language} ({info.language_probability:.0%})")
    segments = [
        {"id": i, "start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip()}
        for i, s in enumerate(segments)
        if s.text.strip()
    ]
    return segments, info.language
