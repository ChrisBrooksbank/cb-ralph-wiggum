#!/usr/bin/env python3
"""Generate the second README demo as an asciinema (asciicast v2) recording.

Same scripted, time-compressed style as make_demo.py, but a different job: a CLI
that turns a House of Lords business paper PDF into a plain-English briefing.
The paper content is real (Lords Business No. 77, Wednesday 15 January 2025).

Regenerate the GIF with asciinema's `agg` renderer:

    python3 assets/demo/make_demo_lords.py > assets/demo/demo-lords.cast
    agg --theme dracula --font-size 16 --idle-time-limit 3 \
        assets/demo/demo-lords.cast assets/demo/demo-lords.gif
"""
import json
import random
import sys

random.seed(11)  # deterministic typing rhythm
sys.stdout.reconfigure(encoding="utf-8", newline="\n")  # box-drawing chars; no CRLF on Windows

W, H = 92, 28

R = "\x1b[0m"
B = "\x1b[1m"
RED = "\x1b[31m"
GRN = "\x1b[32m"
YEL = "\x1b[33m"
BLU = "\x1b[34m"
MAG = "\x1b[35m"
CYN = "\x1b[36m"
GRY = "\x1b[90m"

PROMPT = f"{GRN}{B}~/lords-brief{R} {MAG}main{R} {CYN}❯{R} "

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
    out(f"{BLU}{B}Iteration {n}{R} {GRY}(Mode: {mode})  2026-10-22 {clock}{R}", 0.03)
    out(f"{BLU}=========================================={R}", 0.3)
    why = "clean slate" if n == 1 else f"zero memory of iteration {n - 1}"
    out(f"  {MAG}↻ fresh context{R} {GRY}— new claude session, {why}{R}", 0.5)


def clear():
    emit("\x1b[2J\x1b[H")
    wait(0.1)


# ── Scene 1: scaffold ───────────────────────────────────────────────────────
wait(0.6)
out(f"{GRY}# 1. A different job, the same loop: Lords business paper → briefing.{R}", 0.4)
typed("claude")
out(f"{GRY}╭──────────────────────────────────────────────╮{R}", 0.02)
out(f"{GRY}│{R} {B}✻ Claude Code{R}{' ' * 32}{GRY}│{R}", 0.02)
out(f"{GRY}╰──────────────────────────────────────────────╯{R}", 0.4)
typed("/cb-ralph-wiggum", prompt=f"{B}>{R} ", pre=0.4)
out("", 0.2)
out(f"{CYN}?{R} {B}What do you want to build?{R}", 0.5)
typed("A CLI that reads a House of Lords business paper PDF and prints a briefing",
      prompt=f"  {CYN}›{R} ", pre=0.3, post=0.3)
out(f"{CYN}?{R} {B}Jobs to be done? (2–5 topics){R}", 0.5)
typed("pdf-extraction, item-parsing, briefing-output",
      prompt=f"  {CYN}›{R} ", pre=0.3, post=0.3)
out(f"{CYN}?{R} {B}How will you know it's done?{R}", 0.4)
typed("Tests pass against the real 15 Jan 2025 paper",
      prompt=f"  {CYN}›{R} ", pre=0.3, post=0.3)
out("", 0.1)
spin("Reading CLAUDE.md for build & test commands…", 1.0, ok("Detected: npm test · npm run lint"))
spin("Writing specs and loop tooling…", 1.4, ok("Scaffolded Ralph Wiggum"))
for f, note in [
    ("loop.sh / loop.ps1", "fresh-context loop"),
    ("PROMPT_plan.md", "planning mode"),
    ("PROMPT_build.md", "build mode"),
    ("IMPLEMENTATION_PLAN.md", "shared task list"),
    ("specs/pdf-extraction.md", "JTBD spec"),
    ("specs/item-parsing.md", "JTBD spec"),
    ("specs/briefing-output.md", "JTBD spec"),
    ("fixtures/order-paper-2025-01-15.pdf", "real paper"),
]:
    out(f"    {GRN}+{R} {f:<38}{GRY}{note}{R}", 0.09)
wait(2.2)

# ── Scene 2: plan ───────────────────────────────────────────────────────────
clear()
out(f"{GRY}# 2. Plan: read the specs and the fixture, write the task list.{R}", 0.4)
typed("./loop.sh plan 1")
banner("plan", "PROMPT_plan.md", 1)
iteration(1, "plan", "09:00:02")
spin("Studying specs/*.md …", 0.9, ok("3 specs, 11 requirements"))
spin("Inspecting fixtures/order-paper-2025-01-15.pdf …", 1.0, ok("2 pages, 5 business sections"))
spin("Writing IMPLEMENTATION_PLAN.md …", 0.8, ok("5 tasks, highest priority first"))
for i, task in enumerate([
    "Extract PDF text with pdftotext -layout",
    "Parse oral questions (member, question)",
    "Parse bills and stages (Report, Committee day N)",
    "Parse draft Regulations and who moves them",
    "Grand Committee section + plain-English output",
], 1):
    out(f"    {GRY}{i}.{R} [ ] {task}", 0.07)
out(f"  {GRY}[main 9d20b4e] Ralph iteration 1 (plan mode){R}", 0.3)
out(f"{B}Ralph loop finished after 1 iterations.{R}", 2.0)

# ── Scene 3: build ──────────────────────────────────────────────────────────
clear()
out(f"{GRY}# 3. Build: the real PDF fights back. Tests are the backpressure.{R}", 0.4)
typed("./loop.sh build 3")
banner("build", "PROMPT_build.md", 3)

iteration(1, "build", "09:03:41")
out(f"  {B}→ Task 1:{R} Extract PDF text with pdftotext -layout", 0.3)
spin("Implementing src/extract.ts …", 1.0, ok("src/extract.ts"))
spin("npm test …", 0.8, ok(f"tests {GRN}4 passed{R}"))
out(f"  {GRY}[main 2c61f08] Ralph iteration 1 (build mode){R}", 0.9)

iteration(2, "build", "09:07:12")
out(f"  {B}→ Task 2:{R} Parse oral questions (member, question)", 0.3)
spin("Implementing src/questions.ts …", 1.0, ok("src/questions.ts"))
spin("npm test …", 0.8, f"{RED}✗{R} tests {RED}1 failed{R}, 8 passed")
out(f"    {RED}questions › finds 4 oral questions{R}", 0.05)
out(f"    {GRY}expected 4 received 3: question wraps across lines, member lost{R}", 0.6)
out(f"  {YEL}↺ backpressure:{R} not done until tests are green — fixing…", 0.4)
spin("Joining wrapped lines before matching …", 0.9, ok("src/questions.ts"))
spin("npm test …", 0.8, ok(f"tests {GRN}9 passed{R}"))
out(f"  {GRY}[main e83a4c7] Ralph iteration 2 (build mode){R}", 0.9)

iteration(3, "build", "09:12:55")
out(f"  {B}→ Task 3:{R} Parse bills and stages", 0.3)
spin("Implementing src/bills.ts …", 1.0, ok("src/bills.ts"))
spin("npm test && npm run lint …", 0.9, ok(f"tests {GRN}15 passed{R} · lint clean"))
out(f"  {GRY}[main 70fd2b9] Ralph iteration 3 (build mode){R}", 0.5)
out("", 0.05)
out("Reached max iterations (3). Stopping.", 0.1)
out(f"{B}Ralph loop finished after 3 iterations.{R}", 1.8)

# ── Scene 4: the result ─────────────────────────────────────────────────────
clear()
out(f"{GRY}# 4. The payoff: run it on the real paper.{R}", 0.4)
typed("npx lords-brief fixtures/order-paper-2025-01-15.pdf")
wait(0.5)
out(f"{B}House of Lords · Wednesday 15 January 2025 · sits 3.00pm{R}", 0.3)
out("", 0.1)
out(f"{YEL}{B}Oral questions{R} {GRY}(40 minutes){R}", 0.15)
for who, q in [
    ("Lord Blunkett", "foreign funding of political parties"),
    ("Baroness Keeley", "school visits to theatres and museums"),
    ("Baroness Hazarika", "court backlogs and trial by jury"),
    ("Lord Hain", "Israeli–Palestinian peace talks"),
]:
    out(f"  {CYN}•{R} {who:<19}{q}", 0.2)
out("", 0.1)
out(f"{YEL}{B}Legislation{R}", 0.15)
for name, stage in [
    ("Data (Use and Access) Bill [HL]", "Report stage"),
    ("Financial Assistance to Ukraine Bill", "Second Reading + remaining stages"),
    ("Football Governance Bill [HL]", "Committee, day 7"),
    ("4 draft Regulations", "approval motions"),
]:
    out(f"  {CYN}•{R} {name:<39}{GRY}{stage}{R}", 0.2)
out("", 0.1)
out(f"{YEL}{B}Grand Committee{R} {GRY}(Moses Room, 4.15pm){R}", 0.15)
out(f"  {CYN}•{R} {'Great British Energy Bill':<39}{GRY}Committee, day 4{R}", 0.6)
out("", 0.3)
typed("git log --oneline -4")
for sha, msg in [
    ("70fd2b9", "Ralph iteration 3 (build mode)"),
    ("e83a4c7", "Ralph iteration 2 (build mode)"),
    ("2c61f08", "Ralph iteration 1 (build mode)"),
    ("9d20b4e", "Ralph iteration 1 (plan mode)"),
]:
    out(f"{YEL}{sha}{R} {msg}", 0.08)
out("", 0.3)
out(f"{GRN}{B}Same loop, new job: a dense PDF became a briefing in three reviewable commits.{R}", 0.2)
emit(PROMPT)
wait(4.0)
emit("")

header = {"version": 2, "width": W, "height": H, "timestamp": 1791100800,
          "title": "cb-ralph-wiggum demo: Lords business paper",
          "env": {"SHELL": "/bin/bash", "TERM": "xterm-256color"}}
sys.stdout.write(json.dumps(header) + "\n")
for e in events:
    sys.stdout.write(json.dumps(e, ensure_ascii=False) + "\n")
