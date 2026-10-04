# CLAUDE.md

## Project Overview

A Claude Code slash command skill (`/cb-ralph-wiggum`) that scaffolds the Ralph Wiggum autonomous AI development methodology — a loop technique using fresh context per iteration, with progress stored in files and git history.

## Repository Structure

This is a Claude Code skill repository, not a runnable application.

- `commands/cb-ralph-wiggum.md` — The slash command prompt that Claude Code executes
- `assets/` — README banner and demo GIF. Regenerate the GIF with `assets/demo/make_demo.py` + asciinema's `agg` (see the script's docstring)

## What the Skill Generates

When users run `/cb-ralph-wiggum`, it creates:
- `loop.ps1` / `loop.sh` — Loop orchestrators (PowerShell/Bash)
- `PROMPT_plan.md` / `PROMPT_build.md` — Planning and build mode prompts
- `AGENTS.md` — Operational guide
- `IMPLEMENTATION_PLAN.md` — Task list
- `specs/*.md` — JTBD specifications

## Development

To modify the skill, edit `commands/cb-ralph-wiggum.md`. The command is a Markdown prompt with embedded instructions for Claude.