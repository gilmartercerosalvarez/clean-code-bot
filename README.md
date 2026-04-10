# The Clean Code Bot

CLI tool that reads a “dirty” or under-documented source file and asks an LLM to return a refactor that favors **SOLID** structure and **solid documentation** (Python docstrings, JSDoc for JS/TS, and so on). The pipeline uses a **Chain-of-Thought** prompt so the model analyzes the code before proposing changes, and includes **sanitization** to reduce **prompt injection** risk.

## Requirements

- Python 3.10+
- An API key for [OpenAI](https://platform.openai.com/) and/or [Groq](https://console.groq.com/) (Groq exposes an OpenAI-compatible HTTP API).

## Setup

```bash
cd clean-code-bot
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=...   # or GROQ_API_KEY when using --provider groq
export GROQ_API_KEY=...     # only needed if using --provider groq
```
### API keys

- **Get the API key (from OpenAI)**:
  Steps:
  1. Go to the OpenAI platform: https://platform.openai.com/
  2. Log in or create an account
  3. Navigate to:
  4. Dashboard → API keys
  5. Click: “Create new secret key”
  6. Copy the key (it looks like):

- **Get the API key (GROQ)**:
  1. Open https://console.groq.com/keys 
  2. Click “Create API Key”
  3. Copy the key (it looks like):

Alternatively, put either variable in a `.env` file in the project directory (or your current working directory). Values from the cwd `.env` override the project `.env`. Add `.env` to `.gitignore` so keys are never committed.

## Usage

```bash
python cli.py examples/before.py
// Requied OPENAI_API_KEY
python cli.py examples/before.py -o refactored.py
// required GROQ_API_KEY
python cli.py examples/before.py --provider groq --model llama-3.3-70b-versatile
python cli.py examples/before.py --strict
```

- **`--strict`**: reject files that match heuristic “instruction override” patterns instead of only flagging them.
- **`--max-input-chars`**: hard cap on how much UTF-8 text is sent after sanitization.

## Project layout

```
clean-code-bot/
├── cli.py
├── prompt_engine/
│   ├── templates.py      # system + user scaffolding
│   └── cot_prompt.py     # builds CoT-structured messages
├── core/
│   ├── analyzer.py       # load file + language hint from extension
│   ├── refactorer.py     # orchestration
│   └── sanitizer.py      # UTF-8, length bounds, injection heuristics
├── llm/
│   └── openai_client.py  # OpenAI + Groq (OpenAI-compatible)
├── examples/
│   ├── before.py         # intentionally messy sample
│   └── after.py          # hand-written “target style” illustration
├── requirements.txt
└── README.md
```

## Security note

This tool **cannot guarantee** immunity to prompt injection: user-controlled code is inherently ambiguous. Mitigations here include delimiter framing, explicit system rules, UTF-8 validation, size limits, and optional strict rejection of suspicious patterns. Treat API keys and outbound traffic like any other production secret.

