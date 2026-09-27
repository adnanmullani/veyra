"""Audio nikaalna aur har second ki loudness (energy) nikaalna."""
import subprocess
import wave
import numpy as np


def extract_audio(video: str, out_wav: str) -> str:
    subprocess.run(
        ["ffmpeg", "-y", "-i", video, "-vn", "-ac", "1", "-ar", "16000", out_wav],
        check=True, capture_output=True,
    )
    return out_wav


def energy_per_second(wav_path: str) -> np.ndarray:
    with wave.open(wav_path, "rb") as w:
        rate = w.getframerate()
        data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)
    secs = len(data) // rate
    if secs == 0:
        return np.zeros(1)
    frames = data[: secs * rate].reshape(secs, rate)
    rms = np.sqrt((frames ** 2).mean(axis=1))
    peak = rms.max() or 1.0
    return rms / peak  # 0 se 1 ke beech
