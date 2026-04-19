from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from urllib import error, request

from .base import ModerationProvider


@dataclass(slots=True)
class OpenAIProvider(ModerationProvider):
    model: str
    api_key: str | None = None
    reasoning_effort: str | None = None
    max_output_tokens: int = 4096
    temperature: float | None = None
    base_url: str = "https://api.openai.com/v1/responses"
    extra_headers: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.api_key is None:
            self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required for OpenAIProvider")

    def complete(self, task: str, prompt: str) -> str:
        del task

        payload: dict[str, object] = {
            "model": self.model,
            "input": prompt,
            "max_output_tokens": self.max_output_tokens,
        }

        if self.temperature is not None:
            payload["temperature"] = self.temperature

        if self.reasoning_effort:
            payload["reasoning"] = {"effort": self.reasoning_effort}

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        headers.update(self.extra_headers)

        req = request.Request(
            self.base_url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=120) as response:
                body = response.read().decode("utf-8")
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"OpenAI request failed: {exc.code} {detail}") from exc
        except error.URLError as exc:
            raise RuntimeError(f"OpenAI request failed: {exc.reason}") from exc

        parsed = json.loads(body)
        text = self._extract_text(parsed)
        if not text.strip():
            raise RuntimeError("OpenAI response did not contain text output")
        return text

    @staticmethod
    def _extract_text(response_json: dict) -> str:
        output = response_json.get("output", [])
        chunks: list[str] = []
        for item in output:
            if item.get("type") != "message":
                continue
            for content in item.get("content", []):
                if content.get("type") == "output_text":
                    chunks.append(content.get("text", ""))
        return "\n".join(chunk for chunk in chunks if chunk)
