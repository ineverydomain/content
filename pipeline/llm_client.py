from __future__ import annotations

import json
import os
from typing import Any

from anthropic import Anthropic
from openai import OpenAI

from .common import parse_json_response


class LLMClient:
    def __init__(self) -> None:
        self.provider = os.getenv("LLM_PROVIDER", "openai").lower()
        self.model = os.getenv("LLM_MODEL", "gpt-4o-mini")

        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) if os.getenv("OPENAI_API_KEY") else None
        self.anthropic_client = (
            Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY")) if os.getenv("ANTHROPIC_API_KEY") else None
        )

    def complete_json(self, system_prompt: str, user_payload: Any, temperature: float = 0.2) -> Any:
        payload_text = user_payload if isinstance(user_payload, str) else json.dumps(user_payload, ensure_ascii=False)
        if self.provider == "anthropic":
            if not self.anthropic_client:
                raise RuntimeError("ANTHROPIC_API_KEY is not set.")
            response = self.anthropic_client.messages.create(
                model=self.model,
                max_tokens=800,
                temperature=temperature,
                system=system_prompt,
                messages=[{"role": "user", "content": payload_text}],
            )
            text = "".join(chunk.text for chunk in response.content if hasattr(chunk, "text"))
            return parse_json_response(text)

        if not self.openai_client:
            raise RuntimeError("OPENAI_API_KEY is not set.")
        response = self.openai_client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": payload_text},
            ],
        )
        text = response.choices[0].message.content or "{}"
        return parse_json_response(text)
