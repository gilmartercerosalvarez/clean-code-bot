"""Orchestrates sanitize → CoT prompt → LLM → optional persistence."""

from __future__ import annotations

from pathlib import Path

from core.analyzer import SourceBundle, load_source
from core.sanitizer import SanitizeResult, sanitize_source
from llm.openai_client import chat_completion
from prompt_engine.cot_prompt import build_cot_messages


class Refactorer:
    """High-level entry used by the CLI."""

    def __init__(
        self,
        *,
        provider: str,
        api_key: str,
        model: str | None,
        max_input_chars: int,
        strict_sanitize: bool,
        temperature: float = 0.2,
    ) -> None:
        self._provider = provider
        self._api_key = api_key
        self._model = model
        self._max_input_chars = max_input_chars
        self._strict_sanitize = strict_sanitize
        self._temperature = temperature

    def refactor_path(self, path: Path) -> tuple[str, SanitizeResult]:
        bundle = load_source(path)
        return self.refactor_bundle(bundle)

    def refactor_bundle(self, bundle: SourceBundle) -> tuple[str, SanitizeResult]:
        sanitized = sanitize_source(
            bundle.raw,
            max_chars=self._max_input_chars,
            strict=self._strict_sanitize,
        )
        messages = build_cot_messages(
            sanitized_payload=sanitized.text,
            language_hint=bundle.language_hint,
        )
        output = chat_completion(
            provider=self._provider,
            api_key=self._api_key,
            messages=messages,
            model=self._model,
            temperature=self._temperature,
        )
        return output, sanitized
