# Configs Agents

Personal configuration repo for AI coding tools:

- **OpenCode** — agent definitions, prompts, and TUI keybindings under `.config/opencode/`
- **Claude Code** — instructions and API settings under `.claude/`

## Agent workflow

| Agent | Mode | Use |
|---|---|---|
| `build` | primary | Code generation and editing (DeepSeek v4 Pro) |
| `plan` | primary | Read-only planning and architecture (Qwen 3.7 Plus) |
| `code-reviewer` | subagent | Automated code review (Qwen 3.7 Plus) |

## Key files

| File | Purpose |
|---|---|
| `.config/opencode/opencode.jsonc` | Agent definitions, models, permissions |
| `.config/opencode/prompts/Software_Engineering_Principles.md` | Engineering prompt (shared by `build` and `plan`) |
| `.config/opencode/prompts/code_reviewer.md` | Code reviewer subagent prompt |
| `.config/opencode/tui.json` | TUI keybind overrides (`ctrl+o` for commands) |
| `.claude/CLAUDE.md` | Claude Code instructions |
| `.claude/settings.json` | Claude Code API and model settings |
| `AGENTS.md` | Guidance for future OpenCode sessions in this repo |

## Setup

Clone to your machine and the tools will pick up the config automatically — OpenCode from `.config/opencode/` and Claude Code from `.claude/`.
