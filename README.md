# GenAI Scene-to-Video Pipeline

AI-powered prototype that converts a short scene text into a 5–10 second MP4 with:
- generated dialogue,
- generated background image,
- per-line character speech,
- subtitle overlays.

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install ffmpeg (system dependency), then configure environment:
```bash
cp .env.example .env
```

3. Run:
```bash
python main.py "Romeo stands under Juliet's balcony at night and confesses his love."
```

Output is saved to `outputs/final_video.mp4`.

## Project Structure

```text
genai-scene-pipeline/
├── README.md
├── .env.example
├── requirements.txt
├── main.py
├── pipeline/
│   ├── __init__.py
│   ├── common.py
│   ├── llm_client.py
│   ├── scene_analyzer.py
│   ├── dialogue_writer.py
│   ├── image_generator.py
│   ├── tts_generator.py
│   └── video_assembler.py
├── prompts/
│   ├── scene_analysis.txt
│   ├── dialogue_gen.txt
│   └── image_prompt_gen.txt
└── outputs/
```

## Configuration

Set keys in `.env`:
- `OPENAI_API_KEY` (required for image generation, optional for LLM/TTS if using alternatives)
- `ANTHROPIC_API_KEY` (optional if `LLM_PROVIDER=anthropic`)
- `ELEVENLABS_API_KEY` (optional, used for TTS if present)

Optional tuning:
- `LLM_PROVIDER`: `openai` or `anthropic`
- `LLM_MODEL`: e.g. `gpt-4o-mini`
- `IMAGE_MODEL`: e.g. `gpt-image-1`
- `OPENAI_TTS_MODEL`, voice env vars
- output/video sizing env vars

## Pipeline Steps

1. **Scene Analyzer** (`pipeline/scene_analyzer.py`) extracts setting, mood, characters as JSON.
2. **Dialogue Writer** (`pipeline/dialogue_writer.py`) produces 2–4 concise lines.
3. **Image Generator** (`pipeline/image_generator.py`) expands a visual prompt and generates `background.png`.
4. **TTS Generator** (`pipeline/tts_generator.py`) creates one MP3 per line.
5. **Video Assembler** (`pipeline/video_assembler.py`) combines static background + concatenated audio + subtitle overlays into final MP4.

## Notes

- Prompts are editable in `/prompts` without changing Python code.
- Prototype limitation: no avatars, no lip sync, static background only.
