# AGENTS.md

## What this repo is
A configuration-only repo for OpenCode and Claude Code settings. There is **no application code**, no build/test/lint commands, and no dev server. Do not attempt to run anything.

## Instruction sources
The same engineering-principles content appears in two places — keep them in sync when editing:
- `.claude/CLAUDE.md` (used by Claude Code)
- `.config/opencode/prompts/Software_Engineering_Principles.md` (used by OpenCode agents `build` and `plan`)

## OpenCode agent configuration (`.config/opencode/opencode.jsonc`)
Three agents are defined:

| Agent | Mode | Model | Permissions |
|---|---|---|---|
| `build` | primary (default) | `opencode-go/deepseek-v4-pro` | edit: allow, bash: allow |
| `plan` | primary | `opencode-go/qwen3.7-plus` | edit: deny, bash: deny |
| `code-reviewer` | subagent | `opencode-go/qwen3.7-plus` | edit: deny |

- The `code-reviewer` subagent prompt lives at `.config/opencode/prompts/code_reviewer.md`.
- The `agents/` subdirectory is empty; custom subagents documented in `opencode.jsonc` are sufficient.

## API quirk
Claude Code's `settings.json` (`.claude/settings.json`) points to `https://api.deepseek.com/anthropic` — DeepSeek's Anthropic-compatible endpoint. The `ANTHROPIC_MODEL` is `deepseek-v4-pro[1m]`. This is **not** a standard Anthropic API configuration.

## TUI
Keybinding override in `.config/opencode/tui.json`: `ctrl+o` opens the command list.

## Git
Remote: `https://github.com/yasirerkam/Configs_Agents.git` (branch `main`). Single commit so far; this is a personal config repo.
