# cb-ralph-wiggum

A Claude Code slash command that scaffolds Geoffrey Huntley's **Ralph Wiggum** methodology - an autonomous AI development loop using fresh context per iteration.

## What is Ralph Wiggum?

Ralph Wiggum is a loop technique that feeds prompts to Claude repeatedly, with each iteration getting **fresh context**. Progress is stored in files and git history, not in the LLM context window.

**Key principles:**
- **Fresh context each iteration** - Unlike plugins that accumulate context, true Ralph spawns new Claude sessions
- **Progress in files/git** - Not in LLM memory
- **Backpressure via tests/lints** - Bad outputs get rejected automatically
- **JTBD-driven specs** - Define what to build in specification files
- **Two modes** - Planning (gap analysis) and Building (implementation)

**Economics:** ~$10/hour autonomous coding at Sonnet pricing.

## Installation

Copy the slash command to your Claude Code commands directory:

```bash
# macOS/Linux
cp commands/cb-ralph-wiggum.md ~/.claude/commands/

# Windows (PowerShell)
copy commands\cb-ralph-wiggum.md $env:USERPROFILE\.claude\commands\

# Windows (CMD)
copy commands\cb-ralph-wiggum.md %USERPROFILE%\.claude\commands\
```

## Usage

In any project, run:

```
/cb-ralph-wiggum
```

This will:
1. Interview you about what you want to build (Jobs To Be Done)
2. Detect existing project configuration (CLAUDE.md)
3. Generate all Ralph Wiggum files:
   - `loop.sh` - Bash loop orchestrator (macOS/Linux/WSL)
   - `loop.ps1` - PowerShell loop orchestrator (Windows)
   - `PROMPT_plan.md` - Planning mode instructions
   - `PROMPT_build.md` - Build mode instructions
   - `AGENTS.md` - Operational guide
   - `IMPLEMENTATION_PLAN.md` - Task list
   - `specs/*.md` - JTBD specifications

### Running the Loop

#### Bash (macOS/Linux/WSL/Git Bash)

```bash
# Make executable (first time only)
chmod +x loop.sh

# Run planning mode - analyzes specs, generates tasks
./loop.sh plan 3

# Review IMPLEMENTATION_PLAN.md

# Run build mode - implements one task per iteration
./loop.sh build 10
```

#### PowerShell (Windows)

```powershell
# Run planning mode - analyzes specs, generates tasks
.\loop.ps1 -Mode plan -MaxIterations 3

# Review IMPLEMENTATION_PLAN.md

# Run build mode - implements one task per iteration
.\loop.ps1 -Mode build -MaxIterations 10
```

**Note:** If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### Loop Arguments

#### Bash
```bash
./loop.sh [mode] [max_iterations]

# Examples:
./loop.sh plan      # Planning mode, unlimited iterations
./loop.sh plan 5    # Planning mode, max 5 iterations
./loop.sh build     # Build mode, unlimited iterations
./loop.sh build 20  # Build mode, max 20 iterations
```

#### PowerShell
```powershell
.\loop.ps1 [-Mode plan|build] [-MaxIterations N]

# Examples:
.\loop.ps1                              # Build mode, unlimited
.\loop.ps1 -Mode plan                   # Planning mode, unlimited
.\loop.ps1 -Mode plan -MaxIterations 5  # Planning mode, max 5
.\loop.ps1 -Mode build -MaxIterations 20
```

## Project Structure After Setup

```
your-project/
├── loop.sh                    # Bash loop (macOS/Linux/WSL)
├── loop.ps1                   # PowerShell loop (Windows)
├── PROMPT_plan.md             # Planning mode prompt
├── PROMPT_build.md            # Build mode prompt
├── AGENTS.md                  # Build/test commands (~60 lines)
├── IMPLEMENTATION_PLAN.md     # Task list (updated each iteration)
├── specs/                     # JTBD specifications
│   ├── feature-a.md
│   └── feature-b.md
└── src/                       # Your existing code
```

## The Three Phases

### Phase 1: Requirements (Human + Claude)
Run `/cb-ralph-wiggum` to define what you want to build. The interview creates spec files in `specs/`.

### Phase 2: Planning (`./loop.sh plan` or `.\loop.ps1 -Mode plan`)
Claude reads specs, analyzes the codebase, and generates a prioritized task list in `IMPLEMENTATION_PLAN.md`.

### Phase 3: Building (`./loop.sh build` or `.\loop.ps1 -Mode build`)
Claude picks the top task, implements it, runs tests, commits, and exits. Loop restarts with fresh context for the next task.

## Safety Notes

- **`--dangerously-skip-permissions`** bypasses Claude's permission prompts for full automation
- **Always set iteration limits** to control costs
- **Run in sandboxed environments** for untrusted projects
- **Review commits** - each iteration auto-commits changes
- **Cost estimate:** ~$0.15-0.30 per iteration with Sonnet

## Regenerating Plans

If Ralph goes in circles or the plan becomes stale:

```bash
./loop.sh plan 1        # Bash
.\loop.ps1 -Mode plan -MaxIterations 1  # PowerShell
```

This runs one planning iteration to refresh the task list.

## Templates

The `templates/` directory contains standalone versions of each file that Ralph generates. Use these as reference or copy them manually:

- `loop.sh` - Bash version
- `loop.ps1` - PowerShell version
- `PROMPT_plan.md` - Planning mode prompt
- `PROMPT_build.md` - Build mode prompt
- `AGENTS.md` - Operational guide template
- `IMPLEMENTATION_PLAN.md` - Task list template

## Attribution

Based on Geoffrey Huntley's Ralph Wiggum technique:

- [Ralph Wiggum as "Software Engineer"](https://ghuntley.com/ralph/) - Original article
- [How to Ralph Wiggum](https://github.com/ghuntley/how-to-ralph-wiggum) - Official playbook
- [The Ralph Wiggum Playbook](https://paddo.dev/blog/ralph-wiggum-playbook/) - Comprehensive guide
- [Awesome Ralph](https://github.com/snwfdhmp/awesome-ralph) - Curated resources

## License

MIT
