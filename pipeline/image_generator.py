from __future__ import annotations

import os
from pathlib import Path

from openai import OpenAI
from PIL import Image

from .common import OUTPUT_DIR, load_prompt
from .llm_client import LLMClient


def _expand_prompt(setting_text: str) -> str:
    client = LLMClient()
    prompt = load_prompt("image_prompt_gen.txt")
    data = client.complete_json(prompt, setting_text, temperature=0.5)
    if isinstance(data, dict) and "image_prompt" in data:
        return str(data["image_prompt"])
    return setting_text


def generate_background(setting_text: str) -> str:
    image_prompt = _expand_prompt(setting_text)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for image generation.")

    client = OpenAI(api_key=api_key)
    model = os.getenv("IMAGE_MODEL", "gpt-image-1")
    output_path = Path(OUTPUT_DIR) / "background.png"

    result = client.images.generate(
        model=model,
        prompt=image_prompt,
        size="1280x720",
    )
    image_base64 = result.data[0].b64_json
    if not image_base64:
        raise RuntimeError("Image API did not return image data.")

    import base64

    image_bytes = base64.b64decode(image_base64)
    output_path.write_bytes(image_bytes)

    # Ensure it is a valid PNG and exactly 1280x720
    with Image.open(output_path) as img:
        if img.size != (1280, 720):
            img = img.resize((1280, 720))
            img.save(output_path)

    return str(output_path)
