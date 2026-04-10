"""OpenAI-compatible chat client (OpenAI and Groq endpoints)."""

from __future__ import annotations

from typing import Any

from openai import OpenAI


def _default_model(provider: str) -> str:
    if provider == "groq":
        return "llama-3.3-70b-versatile"
    return "gpt-4o-mini"


def chat_completion(
    *,
    provider: str,
    api_key: str,
    messages: list[dict[str, str]],
    model: str | None = None,
    temperature: float = 0.2,
) -> str:
    """
    Return assistant text for a chat completion.

    provider: "openai" | "groq"
    """
    resolved_model = model or _default_model(provider)
    if provider == "groq":
        client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
    elif provider == "openai":
        client = OpenAI(api_key=api_key)
    else:
        raise ValueError(f"Unknown provider: {provider}")

    kwargs: dict[str, Any] = {
        "model": resolved_model,
        "messages": messages,
        "temperature": temperature,
    }
    response = client.chat.completions.create(**kwargs)
    choice = response.choices[0]
    content = choice.message.content
    if not content:
        raise RuntimeError("LLM returned empty content.")
    return content
