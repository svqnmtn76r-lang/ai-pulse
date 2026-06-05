---
category: feature_update
date: '2026-06-05'
generated_at: '2026-06-05T05:25:52.844389Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.162
template_type: breaking
title: anthropics/claude-code v2.1.162
word_count: 332
---

# Anthropic Releases Claude Code v2.1.162 With Enhanced Developer Experience

## TL;DR

- **UX Refinement**: Slash commands now require explicit Enter confirmation rather than auto-executing, reducing accidental triggers
- **Debugging Power**: New `waitingFor` JSON output reveals exactly what's blocking agent sessions, streamlining troubleshooting workflows
- **Stability Fix**: Read-only config directories no longer cause silent startup failures—a critical reliability improvement for enterprise deployments

## What happened

Anthropic has pushed Claude Code v2.1.162 to production, introducing a batch of refinements focused on developer ergonomics and system reliability. The update, released via the anthropics/claude-code GitHub repository, addresses friction points in agent orchestration, command execution, and IDE integration.

The most impactful change centers on session debugging: the `claude agents --json` command now surfaces a `waitingFor` field that explicitly identifies what's blocking a waiting session—whether that's a permission prompt, user input, or resource constraint. This transparency significantly reduces the guesswork when diagnosing stalled workflows.

On the command front, slash command behavior has shifted. Previously, selecting a command from autocomplete would execute it immediately. Now it inserts the command into the prompt, requiring an explicit Enter keystroke to run. This prevents accidental execution while keeping quick access intact.

The update also corrects handling of native search tooling. When users explicitly specify Grep and Glob tools via the `--tools` flag, Claude Code now properly activates dedicated search implementations on embedded native builds—a capability that was previously silenced.

Additional refinements include persistent Remote Control status display as a footer pill, confirmation prompts for `/effort` defaults, and critical stability fixes for read-only configuration directories that previously caused blank-screen startup hangs. The release also reflects Anthropic's rebrand of the Windsurf integration, renaming it to Devin Desktop across relevant CLI commands.

## What happens next

Watch for adoption patterns around the new `waitingFor` debugging field in agent-heavy workflows. For teams running Claude Code in restricted environments, the read-only config fix removes a significant deployment blocker. Expect downstream tooling to integrate the enhanced JSON output for better observability.

Learn more: [Claude Code v2.1.162 Release](https://github.com/anthropics/claude-code/releases/tag/v2.1.162)
*This article does not contain affiliate links.*
