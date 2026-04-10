"""Input validation and sanitization to reduce prompt-injection risk."""

from __future__ import annotations

import re
from dataclasses import dataclass

# Phrases often used in prompt-injection attempts (case-insensitive).
_SUSPICIOUS_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(p, re.IGNORECASE)
    for p in (
        r"ignore\s+(all\s+)?(previous|prior)\s+instructions",
        r"disregard\s+(the\s+)?(system|above)",
        r"you\s+are\s+now\s+(DAN|jailbroken|unrestricted)",
        r"new\s+system\s+prompt",
        r"<\s*/?\s*system\s*>",
        r"\[\s*INST\s*\]",
        r"override\s+(safety|policy|rules)",
        r"execute\s+(shell|bash|cmd)",
    )
)

DEFAULT_MAX_CHARS = 120_000


@dataclass(frozen=True)
class SanitizeResult:
    """Outcome of sanitizing user-supplied source text."""

    text: str
    truncated: bool
    suspicious_hits: tuple[str, ...]


class SanitizationError(ValueError):
    """Raised when input cannot be accepted safely."""


def _strip_control_chars(raw: str) -> str:
    # Remove NUL and other C0 controls except common whitespace.
    allowed = {"\t", "\n", "\r"}
    return "".join(ch for ch in raw if (ch >= " " or ch in allowed))


def scan_suspicious(text: str) -> tuple[str, ...]:
    """Return human-readable labels for matched injection-style patterns."""
    hits: list[str] = []
    for pat in _SUSPICIOUS_PATTERNS:
        if pat.search(text):
            hits.append(pat.pattern)
    return tuple(hits)


def sanitize_source(
    raw: bytes,
    *,
    max_chars: int = DEFAULT_MAX_CHARS,
    strict: bool = False,
) -> SanitizeResult:
    """
    Decode, normalize, bound length, and optionally reject injection-like content.

    strict=True raises if suspicious patterns are found; otherwise they are recorded
    but the pipeline continues (still wrapped as untrusted data in the prompt).
    """
    if not raw:
        raise SanitizationError("Empty file.")

    if len(raw) > max_chars * 4:
        # Rough guard for binary blobs before full decode.
        raise SanitizationError("File too large to process safely.")

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SanitizationError("Source must be valid UTF-8 text.") from exc

    text = _strip_control_chars(text)
    suspicious = scan_suspicious(text)
    if strict and suspicious:
        raise SanitizationError(
            "Input rejected in strict mode: possible prompt-injection patterns detected."
        )

    truncated = False
    if len(text) > max_chars:
        text = text[:max_chars]
        truncated = True

    return SanitizeResult(text=text, truncated=truncated, suspicious_hits=suspicious)
