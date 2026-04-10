"""Build OpenAI-style messages using a Chain-of-Thought template."""

from __future__ import annotations

from prompt_engine.templates import SYSTEM_REFACTOR, USER_COT_PREFIX, USER_COT_SUFFIX


def build_cot_messages(
    *,
    sanitized_payload: str,
    language_hint: str,
) -> list[dict[str, str]]:
    """Return chat messages: system + single user message with CoT structure."""
    # Concatenate payload instead of str.format to avoid interpreting `{`/`}` in source.
    user_content = (
        USER_COT_PREFIX.format(language_hint=language_hint)
        + sanitized_payload
        + USER_COT_SUFFIX
    )
    return [
        {"role": "system", "content": SYSTEM_REFACTOR},
        {"role": "user", "content": user_content},
    ]
