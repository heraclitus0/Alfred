# Alfred v0.1

Alfred is a **mission-centered, consultation-driven, loop-based, laptop-embodied executive agent**.

This repository implements the **first real organism** of Alfred:

- persistent runtime with modes
- structured memory
- consultation manager
- multi-session research threads
- prompt engineering
- browser opening for ChatGPT
- bounded self-improvement loop in sandbox
- approval/safety/audit foundations

## Current scope

This is not the full final Alfred. It is the **buildable v0.1 nucleus** aligned to the doctrine we defined:

- Alfred can boot and persist state
- Alfred can create and continue consultation threads
- Alfred can frame concrete prompts for betterment, awareness, and mission refinement
- Alfred can open ChatGPT in the browser and prepare prompts
- Alfred can use an LLM API when configured
- Alfred can propose a localized rewrite, sandbox it, and promote it after validation

## Not yet production-complete

The following are intentionally partial or scaffolded:

- full browser UI automation for ChatGPT thread selection
- world/news watchers beyond a basic scaffold
- finance execution
- advanced narrative/trajectory modeling
- full self-rewriting across many modules

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python scripts/bootstrap.py
python scripts/run_cli.py
```

## Environment

Set `OPENAI_API_KEY` if you want API-backed consultation.
Without it, Alfred falls back to a local stub response and still exercises the loop.

## First real organism

The intended first loop is:

1. Alfred detects weakness / curiosity / strategic gap
2. Alfred creates or resumes a consultation thread
3. Alfred builds a high-quality prompt
4. Alfred optionally opens ChatGPT in browser and/or calls the API
5. Alfred stores the result
6. Alfred creates a sandbox rewrite if relevant
7. Alfred validates and promotes only bounded changes

## CLI controls

- `888` → ACTIVE
- `999` → PASSIVE
- `666` → HALT
- `status` → current runtime status
- `consult <topic>` → create/open consultation
- `improve <target>` → run self-improvement loop for a safe target
- `open-chatgpt [topic]` → open ChatGPT in browser for a thread
