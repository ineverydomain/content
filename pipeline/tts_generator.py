from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List

import requests
from openai import OpenAI

from .common import OUTPUT_DIR


def _voice_for_gender(gender: str) -> str:
    male = os.getenv("OPENAI_TTS_VOICE_MALE", "alloy")
    female = os.getenv("OPENAI_TTS_VOICE_FEMALE", "verse")
    gender = (gender or "").lower()
    if gender == "male":
        return male
    if gender == "female":
        return female
    return male


def _gender_map(characters: List[Dict[str, str]]) -> Dict[str, str]:
    return {c.get("name", ""): c.get("gender", "unknown") for c in characters if c.get("name")}


def _generate_openai_tts(text: str, voice: str, output_path: Path) -> None:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
    with client.audio.speech.with_streaming_response.create(model=model, voice=voice, input=text) as response:
        response.stream_to_file(str(output_path))


def _generate_elevenlabs_tts(text: str, voice_id: str, output_path: Path) -> None:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY is not configured.")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    resp = requests.post(
        url,
        headers={"xi-api-key": api_key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
        json={
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.4, "similarity_boost": 0.7},
        },
        timeout=90,
    )
    resp.raise_for_status()
    output_path.write_bytes(resp.content)


def generate_audio(dialogue: List[Dict[str, str]], characters: List[Dict[str, str]]) -> List[str]:
    provider = "elevenlabs" if os.getenv("ELEVENLABS_API_KEY") else "openai"
    output_files: List[str] = []
    genders = _gender_map(characters)

    for idx, item in enumerate(dialogue, start=1):
        character = item["character"]
        text = item["line"]
        gender = genders.get(character, "unknown")

        output_path = Path(OUTPUT_DIR) / f"line_{idx}.mp3"
        if provider == "elevenlabs":
            male_voice = os.getenv("ELEVENLABS_VOICE_MALE", "21m00Tcm4TlvDq8ikWAM")
            female_voice = os.getenv("ELEVENLABS_VOICE_FEMALE", "EXAVITQu4vr4xnSDxMaL")
            voice_id = male_voice if gender == "male" else female_voice
            _generate_elevenlabs_tts(text, voice_id, output_path)
        else:
            voice = _voice_for_gender(gender)
            _generate_openai_tts(text, voice, output_path)

        output_files.append(str(output_path))

    return output_files
