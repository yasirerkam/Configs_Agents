# Repository Guidelines

## Project Overview

Personal dotfiles-style configuration repo for AI coding harnesses — not an application. It holds cloud (dev) and air-gapped (intranet) provider/model/agent configs for three harnesses under `HARNESS/`, each mirroring the tool's real home-directory path under `USER/`:

1. **OMP (Oh-My-Pi)** — `HARNESS/Omp/USER/.omp/agent/`
2. **OpenCode** (+ `oh-my-openagent` plugin) — `HARNESS/OpenCode/USER/.config/opencode/`
3. **Claude Code** — `HARNESS/Claude/.claude/`

Plus one small Python tool (`HARNESS/OpenCode/OpenCode_Ecosystem/`) and reference docs (`MCPs/`, guides in Turkish).

## Architecture & Data Flow

Three parallel harness config trees share one conceptual pipeline:
**prompt/task → agent or model-role selection → model id → provider/gateway (baseURL + apiKey)**.
Cloud vs intranet is expressed by parallel file variants, not runtime branches.

- **OMP**: `config.yml` maps 9 intent roles (`modelRoles`: default, smol, tiny, slow, vision, commit, plan, advisor, task) to `provider/model:thinkingLevel` strings. `models.yml` declares providers (`9router` → `http://localhost:20128/v1`, discovery via proxy). Intranet twins point at `OpenWebUI-yeo`/`LiteLLM-yeo` gateways and add `modelProviderOrder` fallback.
- **OpenCode**: `opencode.jsonc` is the entry surface (agents `build`/`plan`/`explore`, MCP, plugins); heavy lifting is delegated to the `oh-my-openagent` plugin configured in `oh-my-openagent.jsonc` (`agents{}`, `categories{}`, `runtime_fallback`, `team_mode`). Extra subagents are Markdown+YAML-frontmatter files in `agents/`. Two-layer fallback: per-agent `fallback_models[]` + plugin-level `runtime_fallback` (retries on 400/401/403/404/429/500/502/503/504, restores primary after cooldown).
- **Claude Code**: no per-agent files; routing is env-based in `settings.json` (DeepSeek Anthropic-compatible endpoint, tier remaps via `ANTHROPIC_*` env keys).
- **Generation flow**: `generate-intranet.ps1` consumes live cloud configs and emits `*.intranet.*` siblings, swapping `opencode-go/*` ids for local gateways and appending an air-gapped rules block.

## Key Directories

| Directory | Purpose |
|---|---|
| `HARNESS/Omp/` | OMP guides + `USER/.omp/agent/` config tree |
| `HARNESS/OpenCode/` | OpenCode configs, prompts, agents, themes, plugin |
| `HARNESS/OpenCode/USER/.config/opencode/agents/` | Custom subagents (architect, reviewer, committer) |
| `HARNESS/OpenCode/USER/.config/opencode/scripts/` | `generate-intranet.ps1` |
| `HARNESS/OpenCode/OpenCode_Ecosystem/` | Python/uv tool sorting awesome-opencode README by stars |
| `HARNESS/Claude/.claude/` | Claude Code `settings.json` + `CLAUDE.md` |
| `MCPs/` | `codebase-memory-guide.md` — CLI/MCP reference for `codebase-memory-mcp` |

## Development Commands

No global build system. Windows/PowerShell is mandatory (see conventions below).

```powershell
# Python tool (cwd matters — sorter.py uses CWD-relative paths)
cd HARNESS/OpenCode/OpenCode_Ecosystem
uv sync                      # refresh .venv from uv.lock
uv run sorter.py             # regenerate data/processed/README_SORTED.md (needs network; optional GITHUB_TOKEN in .env)

# Intranet variant generation (config root derived from script location, not cwd)
cd HARNESS/OpenCode/USER/.config/opencode
.\scripts\generate-intranet.ps1            # write *.intranet.* variants
.\scripts\generate-intranet.ps1 -WhatIf    # dry run
.\scripts\generate-intranet.ps1 -Apply -Backup   # overwrite live configs (intranet machines)

# codebase-memory MCP (binary must be on PATH)
codebase-memory-mcp cli list_projects
codebase-memory-mcp cli index_repository --repo-path "D:/path/to/repo"
```

## Code Conventions & Common Patterns

- **Generated artifacts**: `*.intranet.*` files are machine-generated; manual edits are overwritten. Always edit the source (no-suffix) files. `agents/committer_gitFlow.md` deliberately has **no** intranet variant.
- **Intranet marker block**: air-gapped rules live between exact `<!-- INTRANET-BEGIN -->` / `<!-- INTRANET-END -->` comments, appended at end of file.
- **Model roles** (OMP): fixed 9-role intent naming; value format `provider/model:level`.
- **Agent definitions** (OpenCode): one Markdown file per subagent with YAML frontmatter (`description`, `mode: primary|subagent`, `model`, `reasoningEffort`, `permission{edit,bash,read,websearch,webfetch}`); bash permissions expressed as glob maps.
- **Agent naming** (oh-my-openagent): Greek-mythology names for agents (sisyphus, atlas, oracle…), workload-intent names for categories (ultrabrain, quick, writing…).
- **Provider naming**: `opencode-go/<model>` = paid Go subscription; `opencode/<model>-free` = Zen free tier; intranet gateways suffixed `-yeo` (OpenWebUI-yeo, LiteLLM-ada-yeo…); OMP uses `9router/ocg/<model>`.
- **Env-var-first auth**: OMP `apiKey` values are treated as env-var *names* first (`NINE_ROUTER_API_KEY`, `OPENWEBUI_API_KEY`, `LITELLM_API_KEY`), literal token as fallback. Env names must be valid shell identifiers (`9ROUTER_API_KEY` is invalid). Real `.env` files are gitignored; `.example.env` documents the load cascade.
- **Docs language**: user-facing docs/filenames are Turkish; config keys and prompts are English.
- **Prompt rules shared verbatim** across OpenCode `AGENTS.md` and Claude `CLAUDE.md`: SOLID/YAGNI/KISS/DRY + Fail-Fast ("Break the Loop": after 4 failed fixes, abandon approach). Git operations follow Git Flow + Conventional Commits (see `skills/git-flow/SKILL.md`); never autonomously resolve merge conflicts, never bypass hooks with `--no-verify`.

## Important Files

- `HARNESS/Omp/USER/.omp/agent/config.yml` / `models.yml` — OMP roles and providers (`.intranet` variants aside)
- `HARNESS/Omp/USER/.omp/agent/.example.env` — env naming rules, load precedence, `OMP_`→`PI_` mirroring
- `HARNESS/OpenCode/USER/.config/opencode/opencode.jsonc` — agent definitions, MCP, plugins
- `HARNESS/OpenCode/USER/.config/opencode/oh-my-openagent.jsonc` — plugin agents/categories, fallback chains
- `HARNESS/OpenCode/USER/.config/opencode/scripts/generate-intranet.ps1` — intranet generator with self-checks
- `HARNESS/OpenCode/USER/.config/opencode/OMO-Model-Strategy.md` — 5-tier cost/intelligence model strategy
- `HARNESS/Claude/.claude/settings.json` — Claude Code model routing via env
- `HARNESS/OpenCode/OpenCode_Ecosystem/sorter.py` — the only real "program" in the repo
- `MCPs/codebase-memory-guide.md` — MCP CLI reference (project names are exact-match)

## Runtime/Tooling Preferences

- **OS/Shell**: Windows + PowerShell only. Use `Select-String` (not grep), `Get-ChildItem` (not ls), `Remove-Item` (not rm). Never emit Unix/Bash commands unless explicitly asked.
- **Python**: 3.13 managed by **uv** (`.python-version`, `uv.lock`); deps: `requests`, `python-dotenv`.
- **Config formats**: JSONC for OpenCode (keep comments), YAML for OMP; PowerShell scripts target 5.1+, write UTF-8 without BOM, preserve original line endings.
- **Gitignore**: root ignores `.omo`, `*.bak`, `.env`; OpenCode_Ecosystem ignores `.env`. Never commit secrets.

## Testing & QA

- **No automated test suite exists** — no pytest/jest config, no CI workflows. Any verification task here means manual or script-based checks.
- De-facto QA is embedded in `generate-intranet.ps1`: `Assert-NoCloudModels` (fails if `opencode-go/` survives conversion), JSON round-trip assertions on agent/category counts and `fallback_models` shape, idempotency SKIP check, `-WhatIf` support. Re-running the script and observing `YAZILDI` vs `SKIP (degismemis)` is the drift check for tracked generated artifacts.
- Config correctness is otherwise validated implicitly by the consuming harnesses loading the files; when editing configs, verify by loading the tool or running a lint/parse (e.g. PowerShell `ConvertFrom-Json`) rather than assuming.
