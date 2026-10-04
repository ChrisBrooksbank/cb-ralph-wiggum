#!/usr/bin/env python3
"""Generate the README demo as an asciinema (asciicast v2) recording.

The demo is a scripted, time-compressed re-enactment of a typical Ralph session:
scaffold with /cb-ralph-wiggum, plan once, then build with fresh context per
iteration. A real build iteration takes minutes; here each one takes seconds.

Regenerate the GIF with asciinema's `agg` renderer:

    python3 assets/demo/make_demo.py > assets/demo/demo.cast
    agg --theme dracula --font-size 16 --idle-time-limit 3 \
        assets/demo/demo.cast assets/demo/demo.gif
"""
import json
import random
import sys

random.seed(7)  # deterministic typing rhythm

W, H = 92, 28

R = "\x1b[0m"
B = "\x1b[1m"
DIM = "\x1b[2m"
RED = "\x1b[31m"
GRN = "\x1b[32m"
YEL = "\x1b[33m"
BLU = "\x1b[34m"
MAG = "\x1b[35m"
CYN = "\x1b[36m"
GRY = "\x1b[90m"

PROMPT = f"{GRN}{B}~/todo-cli{R} {MAG}main{R} {CYN}❯{R} "

t = 0.0
events = []


def emit(s):
    events.append([round(t, 3), "o", s])


def wait(sec):
    global t
    t += sec


def out(s="", delay=0.06):
    emit(s + "\r\n")
    wait(delay)


def typed(cmd, prompt=PROMPT, pre=0.5, post=0.45):
    emit(prompt)
    wait(pre)
    for ch in cmd:
        emit(ch)
        wait(random.uniform(0.035, 0.085))
    wait(post)
    emit("\r\n")
    wait(0.15)


def spin(label, secs, done):
    frames = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    n = int(secs / 0.08)
    for i in range(n):
        emit(f"\r  {CYN}{frames[i % len(frames)]}{R} {label}\x1b[K")
        wait(0.08)
    emit(f"\r  {done}\x1b[K\r\n")
    wait(0.12)


def ok(msg):
    return f"{GRN}✓{R} {msg}"


def banner(mode, prompt_file, max_it):
    out(f"{YEL}=========================================={R}", 0.03)
    out(f"{YEL}{B}Ralph Wiggum Loop{R}", 0.03)
    out(f"Mode: {B}{mode}{R}", 0.03)
    out(f"Prompt: {prompt_file}", 0.03)
    out(f"Max iterations: {max_it}", 0.03)
    out(f"{YEL}=========================================={R}", 0.5)


def iteration(n, mode, clock):
    out("", 0.05)
    out(f"{BLU}=========================================={R}", 0.03)
    out(f"{BLU}{B}Iteration {n}{R} {GRY}(Mode: {mode})  2026-10-04 {clock}{R}", 0.03)
    out(f"{BLU}=========================================={R}", 0.3)
    why = "clean slate" if n == 1 else f"zero memory of iteration {n - 1}"
    out(f"  {MAG}↻ fresh context{R} {GRY}— new claude session, {why}{R}", 0.5)


def clear():
    emit("\x1b[2J\x1b[H")
    wait(0.1)


# ── Scene 1: scaffold ───────────────────────────────────────────────────────
wait(0.6)
out(f"{GRY}# 1. Describe the job. Ralph scaffolds the rest.{R}", 0.4)
typed("claude")
out(f"{GRY}╭──────────────────────────────────────────────╮{R}", 0.02)
out(f"{GRY}│{R} {B}✻ Claude Code{R}{' ' * 32}{GRY}│{R}", 0.02)
out(f"{GRY}╰──────────────────────────────────────────────╯{R}", 0.4)
typed("/cb-ralph-wiggum", prompt=f"{B}>{R} ", pre=0.4)
out("", 0.2)
out(f"{CYN}?{R} {B}What do you want to build?{R}", 0.5)
typed("A CLI todo app with tags, due dates and JSON storage",
      prompt=f"  {CYN}›{R} ", pre=0.3, post=0.3)
out(f"{CYN}?{R} {B}Jobs to be done? (2–5 topics){R}", 0.5)
typed("task-management, tagging, persistence",
      prompt=f"  {CYN}›{R} ", pre=0.3, post=0.3)
out(f"{CYN}?{R} {B}How will you know it's done?{R}", 0.4)
typed("All tests pass", prompt=f"  {CYN}›{R} ", pre=0.3, post=0.3)
out("", 0.1)
spin("Reading CLAUDE.md for build & test commands…", 1.0, ok("Detected: npm test · npm run lint"))
spin("Writing specs and loop tooling…", 1.4, ok("Scaffolded Ralph Wiggum"))
for f, note in [
    ("loop.sh / loop.ps1", "fresh-context loop"),
    ("PROMPT_plan.md", "planning mode"),
    ("PROMPT_build.md", "build mode"),
    ("AGENTS.md", "how to build & test"),
    ("IMPLEMENTATION_PLAN.md", "shared task list"),
    ("specs/task-management.md", "JTBD spec"),
    ("specs/tagging.md", "JTBD spec"),
    ("specs/persistence.md", "JTBD spec"),
]:
    out(f"    {GRN}+{R} {f:<28}{GRY}{note}{R}", 0.09)
wait(2.2)

# ── Scene 2: plan ───────────────────────────────────────────────────────────
clear()
out(f"{GRY}# 2. Plan: gap analysis of specs vs. code → prioritised tasks.{R}", 0.4)
typed("./loop.sh plan 1")
banner("plan", "PROMPT_plan.md", 1)
iteration(1, "plan", "09:00:02")
spin("Studying specs/*.md …", 0.9, ok("3 specs, 14 requirements"))
spin("Comparing against src/ …", 0.9, ok("0 of 14 implemented"))
spin("Writing IMPLEMENTATION_PLAN.md …", 0.8, ok("7 tasks, highest priority first"))
for i, task in enumerate([
    "Task model + in-memory store",
    "`todo add` / `todo list` commands",
    "JSON file persistence",
    "Tags: add, remove, filter",
    "Due dates + overdue highlighting",
], 1):
    out(f"    {GRY}{i}.{R} [ ] {task}", 0.07)
out(f"    {GRY}   …and 2 more{R}", 0.3)
out(f"  {GRY}[main 3f1c2a0] Ralph iteration 1 (plan mode){R}", 0.3)
out(f"{B}Ralph loop finished after 1 iterations.{R}", 2.0)

# ── Scene 3: build ──────────────────────────────────────────────────────────
clear()
out(f"{GRY}# 3. Build: one task per iteration. Tests are the backpressure.{R}", 0.4)
typed("./loop.sh build 3")
banner("build", "PROMPT_build.md", 3)

iteration(1, "build", "09:03:41")
out(f"  {B}→ Task 1:{R} Task model + in-memory store", 0.3)
spin("Implementing src/task.ts …", 1.0, ok("src/task.ts, src/store.ts"))
spin("npm test …", 0.8, ok(f"tests {GRN}6 passed{R}"))
out(f"  {GRY}[main 8a7e51d] Ralph iteration 1 (build mode){R}", 0.9)

iteration(2, "build", "09:07:12")
out(f"  {B}→ Task 2:{R} `todo add` / `todo list` commands", 0.3)
spin("Implementing src/cli.ts …", 1.0, ok("src/cli.ts"))
spin("npm test …", 0.8, f"{RED}✗{R} tests {RED}1 failed{R}, 9 passed")
out(f"    {RED}list › sorts tasks by due date{R}", 0.05)
out(f"    {GRY}expected [\"b\",\"a\"] received [\"a\",\"b\"]{R}", 0.6)
out(f"  {YEL}↺ backpressure:{R} not done until tests are green — fixing…", 0.4)
spin("Patching sort comparator …", 0.9, ok("src/cli.ts"))
spin("npm test …", 0.8, ok(f"tests {GRN}10 passed{R}"))
out(f"  {GRY}[main c42d9be] Ralph iteration 2 (build mode){R}", 0.9)

iteration(3, "build", "09:12:55")
out(f"  {B}→ Task 3:{R} JSON file persistence", 0.3)
spin("Implementing src/storage.ts …", 1.0, ok("src/storage.ts"))
spin("npm test && npm run lint …", 0.9, ok(f"tests {GRN}15 passed{R} · lint clean"))
out(f"  {GRY}[main 51be0f3] Ralph iteration 3 (build mode){R}", 0.5)
out("", 0.05)
out(f"Reached max iterations (3). Stopping.", 0.1)
out(f"{B}Ralph loop finished after 3 iterations.{R}", 1.6)

# ── Scene 4: the receipts ───────────────────────────────────────────────────
typed("git log --oneline -4")
for sha, msg in [
    ("51be0f3", "Ralph iteration 3 (build mode)"),
    ("c42d9be", "Ralph iteration 2 (build mode)"),
    ("8a7e51d", "Ralph iteration 1 (build mode)"),
    ("3f1c2a0", "Ralph iteration 1 (plan mode)"),
]:
    out(f"{YEL}{sha}{R} {msg}", 0.08)
out("", 0.3)
out(f"{GRN}{B}3 tasks shipped · 15 tests green · every step is a commit you can review.{R}", 0.2)
emit(PROMPT)
wait(4.0)
emit("")

header = {"version": 2, "width": W, "height": H, "timestamp": 1791100800,
          "title": "cb-ralph-wiggum demo",
          "env": {"SHELL": "/bin/bash", "TERM": "xterm-256color"}}
sys.stdout.write(json.dumps(header) + "\n")
for e in events:
    sys.stdout.write(json.dumps(e, ensure_ascii=False) + "\n")
