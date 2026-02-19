from __future__ import annotations

from typing import Any, Dict

from .common import load_prompt
from .llm_client import LLMClient


def analyze_scene(scene_text: str) -> Dict[str, Any]:
    client = LLMClient()
    prompt = load_prompt("scene_analysis.txt")
    data = client.complete_json(prompt, scene_text, temperature=0.2)

    if not isinstance(data, dict):
        raise ValueError("Scene analyzer must return a JSON object.")
    if "characters" not in data or not isinstance(data["characters"], list):
        raise ValueError("Scene analyzer output missing `characters` list.")
    if "setting" not in data:
        raise ValueError("Scene analyzer output missing `setting`.")
    if "mood" not in data:
        raise ValueError("Scene analyzer output missing `mood`.")
    return data
