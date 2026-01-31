---
name: cb-ralph-wiggum
author: ChrisBrooksbank
description: Scaffold Ralph Wiggum autonomous AI development - JTBD specs, prompts, and bash loop for fresh-context iterations
---

# Ralph Wiggum Setup

This skill scaffolds Geoffrey Huntley's Ralph Wiggum methodology - an autonomous AI development loop that uses **fresh context per iteration** via a bash loop.

## What is Ralph Wiggum?

Ralph Wiggum is a technique where a bash loop repeatedly feeds prompts to Claude, with each iteration getting fresh context. Progress is stored in files and git history, not in the LLM context window. This enables autonomous development at ~$10/hour compute cost.

**Key principles:**
- Fresh context each iteration (not accumulated like the Anthropic plugin)
- Progress lives in files/git, not LLM memory
- Backpressure via tests/lints rejects bad outputs automatically
- JTBD-driven specs define what to build
- Two modes: Planning (gap analysis) and Building (implementation)

## When to Use

- Starting a new feature that can be broken into discrete tasks
- Automating implementation of a well-defined specification
- Running overnight builds with iteration limits
- Any project where you want AI to work autonomously

## Before Scaffolding

**Step 1: Detect existing project state**

First, check if the project has existing configuration:
- Read CLAUDE.md if it exists (extract build/test commands for AGENTS.md)
- Check for existing specs/ directory
- Check for existing IMPLEMENTATION_PLAN.md

**Step 2: Interview the user**

Use AskUserQuestion to gather requirements:

1. **Project Goal**: "What do you want to build or accomplish? (One sentence describing the end goal)"

2. **JTBD Topics**: "What are the main jobs/outcomes users need? Break into 2-5 distinct topics. Each topic should pass the 'one sentence without and' test."
   - Example: For a todo app: "task-management", "persistence", "filtering", "sharing"

3. **Completion Criteria**: "How will you know when it's done?"
   - Options: "All tests pass", "Manual verification", "Specific features working", "Other"

**Step 3: Generate files based on answers**

---

## Files to Generate

### 1. loop.sh

Create this file with executable permissions:

```bash
#!/bin/bash
# Ralph Wiggum Loop - Fresh context per iteration
# Usage: ./loop.sh [plan|build] [max_iterations]
#
# Examples:
#   ./loop.sh plan      # Planning mode, unlimited
#   ./loop.sh plan 5    # Planning mode, max 5 iterations
#   ./loop.sh build     # Build mode, unlimited
#   ./loop.sh build 20  # Build mode, max 20 iterations

set -e

MODE="${1:-build}"
MAX_ITERATIONS="${2:-0}"
ITERATION=0

if [ "$MODE" = "plan" ]; then
  PROMPT_FILE="PROMPT_plan.md"
elif [ "$MODE" = "build" ]; then
  PROMPT_FILE="PROMPT_build.md"
else
  echo "Usage: ./loop.sh [plan|build] [max_iterations]"
  exit 1
fi

if [ ! -f "$PROMPT_FILE" ]; then
  echo "Error: $PROMPT_FILE not found"
  exit 1
fi

echo "=========================================="
echo "Ralph Wiggum Loop"
echo "Mode: $MODE"
echo "Prompt: $PROMPT_FILE"
[ $MAX_ITERATIONS -gt 0 ] && echo "Max iterations: $MAX_ITERATIONS"
echo "=========================================="

while true; do
  if [ $MAX_ITERATIONS -gt 0 ] && [ $ITERATION -ge $MAX_ITERATIONS ]; then
    echo ""
    echo "Reached max iterations ($MAX_ITERATIONS). Stopping."
    break
  fi

  ITERATION=$((ITERATION + 1))
  echo ""
  echo "=========================================="
  echo "Iteration $ITERATION (Mode: $MODE)"
  echo "$(date '+%Y-%m-%d %H:%M:%S')"
  echo "=========================================="

  # Fresh Claude session each iteration - context resets!
  cat "$PROMPT_FILE" | claude -p \
    --dangerously-skip-permissions \
    --model sonnet

  # Auto-commit progress after each iteration
  git add -A
  if ! git diff --staged --quiet; then
    git commit -m "Ralph iteration $ITERATION ($MODE mode)

Co-Authored-By: Claude <noreply@anthropic.com>"
    echo "Changes committed."
  else
    echo "No changes to commit."
  fi

  echo "Iteration $ITERATION complete."
  sleep 2
done

echo ""
echo "Ralph loop finished after $ITERATION iterations."
```

After creating, make executable: `chmod +x loop.sh`

### 2. PROMPT_plan.md

```markdown
# PLANNING MODE

You are in planning mode. Your job is to analyze specifications and update the implementation plan. DO NOT write any code.

## 0a. Study Specifications

Using parallel subagents, read and understand each file in the specs/ directory. These define what needs to be built.

## 0b. Review Current Plan

Read IMPLEMENTATION_PLAN.md to understand what tasks exist and their status.

## 0c. Examine Codebase

Using parallel subagents, explore the existing codebase to understand:
- What's already implemented
- Code patterns and conventions
- Test structure

## 1. Gap Analysis

Compare the specifications against the existing codebase:
- What requirements are fully implemented?
- What requirements are partially implemented?
- What requirements have no implementation?

## 2. Update Implementation Plan

Update IMPLEMENTATION_PLAN.md with:
- New tasks for unimplemented requirements
- Refined tasks based on what you learned
- Clear priority order (most important first)
- Mark any completed tasks as done

Format tasks as:
```
- [ ] Task description (spec: filename.md)
- [x] Completed task
```

## 3. Exit

After updating the plan, your work is done. Exit cleanly. The loop will restart with fresh context for the next iteration.

---

## 99999. GUARDRAILS - READ CAREFULLY

- **DON'T assume code doesn't exist** - always verify by reading files first
- **DON'T write any implementation code** - planning mode is for planning only
- **DON'T modify source files** - only modify IMPLEMENTATION_PLAN.md
- **DO capture architectural decisions** in the plan
- **DO prioritize tasks logically** (dependencies first)
- **DO keep tasks small** - one task = one iteration in build mode
```

### 3. PROMPT_build.md

```markdown
# BUILD MODE

You are in build mode. Your job is to implement ONE task from the plan, then exit.

## 0a. Read AGENTS.md

Read AGENTS.md to understand build/test/lint commands for this project.

## 0b. Read Implementation Plan

Read IMPLEMENTATION_PLAN.md. Find the first uncompleted task (marked with `- [ ]`).

## 0c. Study Relevant Specs

Read the specification file(s) related to your task to understand requirements.

## 0d. Understand Existing Code

Read relevant existing code to understand patterns and conventions.

## 1. Implement the Task

Write code to complete the task:
- Follow existing code patterns
- Write tests for new functionality
- Keep changes focused on the single task

## 2. Validate

Run the validation command from AGENTS.md (typically `npm run check` or similar).

If validation fails:
- Fix the issues
- Run validation again
- Repeat until passing

## 3. Update Plan and Exit

After validation passes:
1. Mark the task complete in IMPLEMENTATION_PLAN.md: `- [ ]` becomes `- [x]`
2. Exit cleanly

The loop will restart with fresh context for the next task.

---

## 99999. GUARDRAILS - READ CAREFULLY

- **DON'T skip validation** - always run tests/lint before finishing
- **DON'T implement multiple tasks** - one task per iteration
- **DON'T modify unrelated code** - stay focused on the current task
- **DO follow existing code patterns** - consistency matters
- **DO write tests** for new functionality
- **DO update IMPLEMENTATION_PLAN.md** before exiting
```

### 4. AGENTS.md

Generate this by extracting commands from existing CLAUDE.md, or ask the user. Template:

```markdown
# AGENTS.md - Operational Guide

Keep this file under 60 lines. It's loaded every iteration.

## Build Commands

```bash
npm run build          # Production build
npm run dev            # Development server
```

## Test Commands

```bash
npm test               # Run tests (watch mode)
npm run test:run       # Run tests once
npm run test:coverage  # Coverage report
```

## Validation (run before committing)

```bash
npm run check          # Run ALL checks (typecheck, lint, format, tests)
```

## Project Notes

- [Add project-specific patterns here]
- [Add learnings from iterations here]
```

### 5. IMPLEMENTATION_PLAN.md

Start with an empty or minimal template:

```markdown
# Implementation Plan

## Status

- Planning iterations: 0
- Build iterations: 0
- Last updated: [date]

## Tasks

<!-- Tasks will be added by planning mode -->
<!-- Format: - [ ] Task description (spec: filename.md) -->

## Completed

<!-- Completed tasks move here -->

## Notes

<!-- Architectural decisions and learnings -->
```

### 6. specs/ Directory

Create one markdown file per JTBD topic. Template:

```markdown
# [Topic Name]

## Overview

[One sentence describing this topic]

## User Stories

- As a [user], I want to [action] so that [benefit]

## Requirements

- [ ] Requirement 1
- [ ] Requirement 2

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Out of Scope

- [What this spec does NOT cover]
```

---

## Post-Setup Instructions

After generating all files, provide these instructions to the user:

### Quick Start

```bash
# Make loop executable
chmod +x loop.sh

# Run planning mode (generates tasks from specs)
./loop.sh plan 3

# Review the generated IMPLEMENTATION_PLAN.md

# Run build mode (implements tasks one by one)
./loop.sh build 10
```

### Safety Notes

- `--dangerously-skip-permissions` bypasses Claude's permission system
- Always run in a sandboxed environment or review commits
- Set iteration limits to control costs (~$0.15-0.30 per iteration with Sonnet)
- Monitor the loop - stop if it goes off track

### Regenerating the Plan

If the plan becomes stale or Ralph goes in circles:
```bash
./loop.sh plan 1
```
This regenerates the plan with fresh analysis.

---

## Attribution

Based on Geoffrey Huntley's Ralph Wiggum technique:
- [Ralph Wiggum as "Software Engineer"](https://ghuntley.com/ralph/)
- [How to Ralph Wiggum](https://github.com/ghuntley/how-to-ralph-wiggum)
- [The Ralph Wiggum Playbook](https://paddo.dev/blog/ralph-wiggum-playbook/)
