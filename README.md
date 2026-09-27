# Veyra 🎬

**Upload. Talk. Post. AI does the editing.**

An AI video editor for creators everywhere: gaming, food, travel, vlogs, podcasts. Give Veyra a long video and it finds the best moments and turns them into ready-to-post Shorts with captions in your language.

## Phase 1 features

* Auto transcript with Whisper, in 90+ languages with automatic language detection
* Captions stay in the language you speak. Hindi videos get Roman-script Hinglish captions, which is how most Hindi creators write online.
* AI (free local Ollama, or Claude) picks and scores the best moments
* Audio energy gives extra weight to reactions and hype moments
* Output: top 4 Shorts, 9:16, captions burned in

## Setup

1. Install Python 3.10+, [FFmpeg](https://ffmpeg.org/download.html) and [Ollama](https://ollama.com)
2. Download the model:
   ```
   ollama pull qwen2.5:7b
   ```
3. Set up the project:
   ```
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   source .venv/bin/activate     # Mac/Linux
   pip install -r requirements.txt
   cp .env.example .env
   ```

## Run

```
python main.py samples/myvideo.mp4
```

Output goes to `outputs/<video name>/`: `short_1.mp4` to `short_4.mp4`, `clips.json` and `transcript.json`.

## Switch to Claude

In `.env`, set `LLM_PROVIDER=claude` and add your `ANTHROPIC_API_KEY`. No code changes needed.

## Architecture

```
video → audio → Whisper transcript → captions (Hinglish if Hindi) → AI highlight scoring (+ audio energy) → FFmpeg 9:16 render
```

## Roadmap

* [x] Phase 1: Core engine, top 4 Shorts (Talking/Vlog)
* [ ] Phase 2: Web app, upload, Drive link, queue, preview
* [ ] Phase 3: Cut a 1 hr video into a 15/30 min version
* [ ] Phase 4: Transitions, 3 style previews, GIFs/stickers
* [ ] Phase 5: Food, Travel, Gaming, Podcast presets
* [ ] Phase 6: Docker + AWS ECS deploy
* [ ] Phase 7: Public launch (demo video, Colab notebook, Hugging Face Space)
* [ ] Later: Chat-based editing ("add a zoom at 2:30"), caption translation, audio cleanup, color correction, B-roll, thumbnail and title suggestions
