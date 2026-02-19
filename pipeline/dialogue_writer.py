from __future__ import annotations

from typing import Any, Dict, List

from .common import load_prompt
from .llm_client import LLMClient


def write_dialogue(scene_data: Dict[str, Any]) -> List[Dict[str, str]]:
    client = LLMClient()
    prompt = load_prompt("dialogue_gen.txt")
    data = client.complete_json(prompt, scene_data, temperature=0.7)

    if isinstance(data, dict) and "dialogue" in data:
        data = data["dialogue"]

    if not isinstance(data, list):
        raise ValueError("Dialogue writer must return a JSON array of dialogue items.")

    cleaned: List[Dict[str, str]] = []
    for item in data[:4]:
        if not isinstance(item, dict):
            continue
        character = str(item.get("character", "")).strip()
        line = str(item.get("line", "")).strip()
        if character and line:
            words = line.split()
            cleaned.append({"character": character, "line": " ".join(words[:15])})

    if len(cleaned) < 2:
        raise ValueError("Dialogue writer produced fewer than 2 usable lines.")
    return cleaned
