#!/usr/bin/env python3
"""CLI for The Clean Code Bot — automated refactor + documentation pass."""

from __future__ import annotations

import os
from pathlib import Path

import click
from dotenv import load_dotenv

from core.refactorer import Refactorer
from core.sanitizer import SanitizationError


def _load_env_files() -> None:
    """Load `.env` from the project root (next to this file) then cwd (cwd overrides)."""
    project_root = Path(__file__).resolve().parent
    load_dotenv(project_root / ".env")
    load_dotenv(Path.cwd() / ".env", override=True)


def _resolve_api_key(provider: str, api_key: str | None) -> str:
    if api_key:
        return api_key
    if provider == "groq":
        key = os.environ.get("GROQ_API_KEY")
        if not key:
            raise click.ClickException(
                "Missing Groq API key.\n\n"
                "  export GROQ_API_KEY='gsk_...'\n\n"
                "Or pass it explicitly (may be stored in shell history):\n\n"
                "  python3 cli.py ... --provider groq --api-key gsk_...\n\n"
                "Create a key at https://console.groq.com/keys\n\n"
                "You can also put GROQ_API_KEY=... in a `.env` file in this project "
                "(loaded automatically on startup)."
            )
        return key
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise click.ClickException(
            "Missing OpenAI API key.\n\n"
            "  export OPENAI_API_KEY='sk-...'\n\n"
            "Or use --api-key, or add OPENAI_API_KEY to a `.env` file in this project."
        )
    return key


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("input_path", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option(
    "-o",
    "--output",
    "output_path",
    type=click.Path(dir_okay=False, path_type=Path),
    help="Write result to this file. If omitted, print to stdout.",
)
@click.option(
    "--provider",
    type=click.Choice(["openai", "groq"], case_sensitive=False),
    default="openai",
    show_default=True,
    help="LLM backend (Groq uses an OpenAI-compatible endpoint).",
)
@click.option(
    "--model",
    type=str,
    default=None,
    help="Override default model (OpenAI: gpt-4o-mini, Groq: llama-3.3-70b-versatile).",
)
@click.option(
    "--api-key",
    type=str,
    default=None,
    help="API key. Defaults to OPENAI_API_KEY or GROQ_API_KEY based on provider.",
)
@click.option(
    "--max-input-chars",
    type=int,
    default=120_000,
    show_default=True,
    help="Hard cap on UTF-8 characters sent after sanitization.",
)
@click.option(
    "--strict",
    is_flag=True,
    help="Reject inputs that match known prompt-injection heuristics.",
)
@click.option(
    "--temperature",
    type=float,
    default=0.2,
    show_default=True,
    help="Sampling temperature for the chat completion.",
)
def main(
    input_path: Path,
    output_path: Path | None,
    provider: str,
    model: str | None,
    api_key: str | None,
    max_input_chars: int,
    strict: bool,
    temperature: float,
) -> None:
    """Refactor INPUT_PATH with SOLID-aware guidance and documentation."""
    _load_env_files()
    provider = provider.lower()
    key = _resolve_api_key(provider, api_key)
    refactorer = Refactorer(
        provider=provider,
        api_key=key,
        model=model,
        max_input_chars=max_input_chars,
        strict_sanitize=strict,
        temperature=temperature,
    )
    try:
        text, meta = refactorer.refactor_path(input_path)
    except SanitizationError as exc:
        raise click.ClickException(str(exc)) from exc
    except Exception as exc:  # noqa: BLE001 — surface provider errors to CLI users
        raise click.ClickException(str(exc)) from exc

    if meta.truncated:
        click.echo(
            "Warning: input was truncated to --max-input-chars.",
            err=True,
        )
    if meta.suspicious_hits:
        click.echo(
            "Warning: suspicious patterns were detected in the source "
            f"({len(meta.suspicious_hits)}). They were still treated as data.",
            err=True,
        )

    if output_path is not None:
        output_path.write_text(text, encoding="utf-8")
        click.echo(f"Wrote {output_path}")
    else:
        click.echo(text)


if __name__ == "__main__":
    main()
