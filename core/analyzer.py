"""Lightweight static analysis helpers (language hint, file loading)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


_EXT_TO_LANGUAGE: dict[str, str] = {
    ".py": "Python",
    ".pyw": "Python",
    ".js": "JavaScript",
    ".mjs": "JavaScript",
    ".cjs": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".jsx": "JavaScript",
    ".java": "Java",
    ".go": "Go",
    ".rs": "Rust",
    ".rb": "Ruby",
    ".php": "PHP",
    ".cs": "C#",
    ".swift": "Swift",
    ".kt": "Kotlin",
    ".scala": "Scala",
    ".sql": "SQL",
    ".sh": "Shell",
    ".bash": "Shell",
    ".zsh": "Shell",
}


@dataclass(frozen=True)
class SourceBundle:
    """Raw bytes plus a human-readable language hint for prompting."""

    path: Path
    raw: bytes
    language_hint: str


def infer_language_hint(path: Path) -> str:
    suffix = path.suffix.lower()
    return _EXT_TO_LANGUAGE.get(suffix, f"Unknown (suffix {suffix or 'none'})")


def load_source(path: Path) -> SourceBundle:
    if not path.is_file():
        raise FileNotFoundError(f"Not a file: {path}")
    raw = path.read_bytes()
    return SourceBundle(path=path, raw=raw, language_hint=infer_language_hint(path))
