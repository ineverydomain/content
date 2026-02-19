from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parents[1]
PROMPTS_DIR = ROOT_DIR / "prompts"
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", ROOT_DIR / "outputs"))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_prompt(filename: str) -> str:
    return (PROMPTS_DIR / filename).read_text(encoding="utf-8")


def parse_json_response(text: str) -> Any:
    """Parse a model response into JSON, with light guardrails."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        stripped = text.strip()
        if "```" in stripped:
            stripped = stripped.replace("```json", "").replace("```", "").strip()
            return json.loads(stripped)
        start = stripped.find("{")
        end = stripped.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(stripped[start : end + 1])
        raise ValueError(f"Model response is not valid JSON: {text}")
