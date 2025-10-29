## Purpose

This repository contains a small demo Flask-like Python app for resume parsing, scoring
and report generation. These instructions help AI coding agents get productive quickly
by pointing to the important files, developer commands, project conventions, and safe-edit rules.

## Quick facts

- Language: Python 3.x
- Entry point: `app.py` (runs the web app / demo)
- Dependencies: listed in `requirements.txt`
- Tests: pytest tests under `tests/`

## Primary files and what to inspect first

- `app.py` — application entrypoint and basic runtime wiring.
- `config.py` — runtime configuration values used across modules.
- `database/` — `db.py` (DB session/wiring) and `models.py` (ORM models).
- `core/` — domain code:
  - `parser.py` — resume parsing logic (start here for parsing flows)
  - `scorer.py` — scoring logic (uses parsed output)
  - `skills.py`, `matcher.py`, `sections.py`, `feedback.py`, `ats.py` — helpers and domain pieces
- `data/skills_taxonomy.json` — canonical skills taxonomy the matcher/scorer uses
- `templates/` and `static/` — Jinja templates and static assets for reporting
- `uploads/` — file upload landing location used by the web UI (contains `.gitkeep`)
- `tests/` — unit tests and `sample_resume.pdf` used by parser tests

## Developer commands (zsh)

Create a venv and install deps:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the app (simple development run):

```bash
python app.py
```

Run tests:

```bash
python -m pytest -q
```

If tests need to target a specific file:

```bash
python -m pytest tests/test_parser.py -q
```

## Project-specific conventions & patterns

- Minimal, single-module services: each domain responsibility lives under `core/` in a focused module.
- Data-driven matching: `data/skills_taxonomy.json` is the canonical source for skill matching—changes here affect matcher/scorer behavior.
- Templates follow standard Jinja usage in `templates/` — rendering is performed by the app to create the HTML report.
- Tests include a binary sample file (`tests/sample_resume.pdf`) — be careful when modifying test fixtures.

## Integration points and external dependencies

- Database: `database/db.py` contains DB/session wiring. Check `database/models.py` to understand schema used by scoring/feedback.
- File I/O: uploaded resumes are saved under `uploads/` and read by the parser. Keep path handling relative and testable.
- Taxonomy data: `data/skills_taxonomy.json` is loaded at runtime by matcher/scorer — prefer small-tooling changes that keep JSON format stable.

## Editing and PR guidance for agents

- Preserve public APIs and function signatures when possible — project is small and tests exercise core flows.
- Keep changes small and focused; add or update unit tests in `tests/` for any behavior change (parser/scorer are most critical).
- Do not commit secrets or environment tokens. If you find any, redact and notify maintainers.
- If you change `data/skills_taxonomy.json`, update or add tests that validate matcher/scorer output for at least one sample.

## Merge / update policy for this file

- If `.github/copilot-instructions.md` already exists: preserve high-quality hand-written sections and only append an "Auto-updated by agent" note.

## Auto-updated by agent

- Generated/updated by an AI agent on 2025-10-29 — review and edit for project-specific nuance (ownership, CI steps, env variables).
## Purpose
This file tells AI coding agents how to get productive in this repository. It documents the discovery steps, conventions to follow, where to look for important signals, and safe merge behavior when updating these instructions.

## Quick facts (auto-detected)
- Repo root currently has no discoverable source files or READMEs. Agents should verify this before making code changes.

## First steps for any agent
1. Run a repo scan for common entry points: `README.md`, `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `Dockerfile`, `Makefile`, `src/`, `cmd/`, `app/`, `scripts/`, `.github/workflows/`.
2. If no source is found, ask the user whether you're operating on an empty workspace or whether you should initialize a project skeleton.
3. If a README or CI files exist, extract setup/build/test commands from them and run them (or present them to the user) before making further changes.

## What to document in this file (keep concise)
- High-level architecture (major services, languages, data flows).
- Primary developer commands: build, test, run, lint, docker build/run, and where to find them (file path or CI step).
- Project-specific coding patterns or anti-patterns (naming, file layout, error handling style).
- Sensitive state: where secrets/config live (env files, vault, not in repo).

## Merge strategy for agents updating this file
- If `.github/copilot-instructions.md` already exists: keep unchanged sections unless you can verify and augment them with direct repository evidence. Always preserve human-authored notes and examples.
- Add a single "Auto-updated by agent" section at the end with a short summary of changes and a timestamp.

## Examples of actionable heuristics (search & infer)
- Python: if `pyproject.toml` or `requirements.txt` found, prefer virtualenv/poetry flows. Look for `scripts/` or `Makefile` for exact commands.
- Node: if `package.json` exists, prefer `npm run build` / `npm test`. Look at `engines` and `scripts` fields for conventions.
- Go: if `go.mod` present, prefer `go test ./...` and `go build ./...` in module root.
- Containers: if `Dockerfile` present check for multi-stage builds and preferred runtime tag (e.g., `python:3.x-slim`).

## Useful file pointers to look for in this repo (if added later)
- `README.md` — source of truth for dev setup and common commands.
- `docs/` — architecture diagrams, API specs, decision records.
- `src/`, `pkg/`, `cmd/`, `internal/` — primary code directories.
- `.github/workflows/` or `scripts/ci/` — canonical build/test commands and environment variables.

## Safety & scope rules for automated edits
- Do not commit secrets or environment tokens. If you find them, warn the user and redact before committing.
- For non-trivial design changes, create a PR with a descriptive title and link to relevant issue or decision note.
- Keep edits minimal and well-scoped. Prefer adding tests or a small runner for new code.

## If you need clarification
- Add a short, focused question to the user referencing exact file paths (e.g., "Where should I put configuration: `config/` or `env/`?").

---
_If this file was created by an agent and the repository actually contains code, please update the "Quick facts" and add 3–5 concrete examples (file paths + commands) from the codebase._
