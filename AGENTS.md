# AGENTS.md

## What this repo is
Personal config repo for AI coding tools (OpenCode, Claude Code) **with Python utility scripts**. Not config-only — there are runnable subprojects in `OpenCode_Ecosystem/` and `g4f.space/`.

## Directory layout
- `.config/opencode/` — OpenCode agent definitions, prompts, TUI keybindings
- `.claude/` — Claude Code instructions and API settings
- `OpenCode_Ecosystem/` — Python (uv) project: awesome-opencode README star sorter
- `g4f.space/` — PEP 723 script: generates OpenCode model config from g4f.space API
- `AI Compare/` — Screenshots and reference data for model comparisons

## Instruction sources
The same engineering-principles content appears in two places — **keep them in sync** when editing:
- `.claude/CLAUDE.md` (used by Claude Code)
- `.config/opencode/prompts/Software_Engineering_Principles.md` (used by OpenCode agents via `opencode.jsonc` `instructions`)

## OpenCode agents (`.config/opencode/opencode.jsonc`)

| Agent | Mode | Model | Notes |
|---|---|---|---|
| `build` | primary (default) | `opencode-go/minimax-m3` | edit/bash: allow |
| `plan` | primary | `opencode-go/qwen3.7-plus` | read-only |
| `explore` | subagent | `opencode-go/mimo-v2.5` | |
| `code-reviewer` | subagent | `opencode-go/mimo-v2.5-pro` | prompt: `prompts/code_reviewer.md` |
| `committer` | subagent | `opencode-go/mimo-v2.5` | prompt: `prompts/committer.md`; bash limited to `git status/diff/add/commit` |

## Python subprojects

### `OpenCode_Ecosystem/`
- **Manager:** uv (`pyproject.toml`, `uv.lock`). Requires Python ≥ 3.13.
- **Run sorter:** `uv run sorter.py` (from `OpenCode_Ecosystem/`)
- **Env:** loads `.env` from project root. Set `GITHUB_TOKEN` to avoid 60 req/hr anonymous API limit.
- **Caches:** `data/raw/README.md` (6h TTL), `data/raw/stars_cache.json` (24h TTL).
- **Output:** `data/processed/README_SORTED.md`

### `g4f.space/`
- **Run:** `uv run generate_config.py` (PEP 723 inline deps — no venv needed)
- **Output:** `opencode_models.json` (filtered), `raw_models.json` (raw API, 5min cache)
- **Config:** edit `TARGET_MODELS` list in the script to change which models are fetched.

## API quirk
Claude Code's `settings.json` (`.claude/settings.json`) points to `https://api.deepseek.com/anthropic` — DeepSeek's Anthropic-compatible endpoint. The `ANTHROPIC_MODEL` is `deepseek-v4-pro[1m]`. This is **not** a standard Anthropic API configuration.

## TUI
Keybinding override in `.config/opencode/tui.json`: `ctrl+o` opens the command list.

## Git
Remote: `https://github.com/yasirerkam/Configs_Agents.git` (branch `main`). Personal config repo.
