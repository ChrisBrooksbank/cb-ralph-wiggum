#!/usr/bin/env pwsh
# Ralph Wiggum Loop - Fresh context per iteration (PowerShell 7)
# Usage: .\loop.ps1 [plan|build] [max_iterations]
#
# Examples:
#   .\loop.ps1 plan      # Planning mode, unlimited
#   .\loop.ps1 plan 5    # Planning mode, max 5 iterations
#   .\loop.ps1 build     # Build mode, unlimited
#   .\loop.ps1 build 20  # Build mode, max 20 iterations
#
# Named parameters also work:
#   .\loop.ps1 -Mode plan -MaxIterations 5

param(
    [ValidateSet("plan", "build")]
    [string]$Mode = "build",
    [int]$MaxIterations = 0  # 0 means unlimited
)

$ErrorActionPreference = "Stop"

switch ($Mode) {
    "plan"  { $PromptFile = "PROMPT_plan.md" }
    "build" { $PromptFile = "PROMPT_build.md" }
}

if (-not (Test-Path $PromptFile)) {
    Write-Error "Error: $PromptFile not found"
    exit 1
}

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Ralph Wiggum Loop" -ForegroundColor Cyan
Write-Host "Mode: $Mode" -ForegroundColor Cyan
Write-Host "Prompt: $PromptFile" -ForegroundColor Cyan
if ($MaxIterations -gt 0) {
    Write-Host "Max iterations: $MaxIterations" -ForegroundColor Cyan
}
Write-Host "==========================================" -ForegroundColor Cyan

$Iteration = 0

while ($true) {
    if ($MaxIterations -gt 0 -and $Iteration -ge $MaxIterations) {
        Write-Host ""
        Write-Host "Reached max iterations ($MaxIterations). Stopping." -ForegroundColor Yellow
        break
    }

    $Iteration++
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host "Iteration $Iteration (Mode: $Mode)" -ForegroundColor Green
    Write-Host $Timestamp -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Green

    # Fresh Claude session each iteration - context resets!
    Get-Content $PromptFile -Raw | claude -p --dangerously-skip-permissions --model sonnet

    if ($LASTEXITCODE -ne 0) {
        Write-Host "Claude exited with code $LASTEXITCODE - continuing..." -ForegroundColor Yellow
    }

    # Auto-commit progress after each iteration
    git add -A

    $StagedChanges = git diff --staged --quiet 2>&1
    if ($LASTEXITCODE -ne 0) {
        $CommitMessage = @"
Ralph iteration $Iteration ($Mode mode)

Co-Authored-By: Claude <noreply@anthropic.com>
"@
        git commit -m $CommitMessage
        Write-Host "Changes committed." -ForegroundColor Green
    } else {
        Write-Host "No changes to commit." -ForegroundColor DarkGray
    }

    Write-Host "Iteration $Iteration complete." -ForegroundColor Green
    Start-Sleep -Seconds 2
}

Write-Host ""
Write-Host "Ralph loop finished after $Iteration iterations." -ForegroundColor Cyan
