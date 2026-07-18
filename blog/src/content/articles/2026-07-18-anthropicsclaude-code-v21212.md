---
category: feature_update
date: '2026-07-18'
generated_at: '2026-07-18T04:07:37.193206Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.212
template_type: breaking
title: anthropics/claude-code v2.1.212
word_count: 320
---

# Claude Code v2.1.212 Introduces Workflow Controls and Session Management Upgrades

## TL;DR

- **Runaway safeguards**: New per-session caps on web searches (200 default) and subagent spawns (200 default) prevent resource exhaustion
- **Workflow refinement**: `/fork` now creates background sessions instead of inline subagents; new `/subtask` command replaces old behavior
- **Background processing**: MCP tool calls exceeding 2 minutes automatically move to background, keeping sessions responsive

## What happened

Anthropic has released version 2.1.212 of Claude Code, rolling out operational improvements designed to prevent resource runaway while enhancing multi-threaded workflows. The update, posted to the project's GitHub releases, addresses pain points in agent delegation and external tool integration that users working with complex, iterative tasks have encountered.

The most significant structural change involves session forking. Previously, `/fork` launched an inline subagent within the current session. Now it spawns a dedicated background session visible as a separate row in the `claude agents` interface, allowing users to maintain parallel work streams without interrupting their primary conversation thread. The legacy behavior has been preserved under a new `/subtask` command for users preferring in-session delegation.

To combat cascading delegation failures, Claude Code now enforces dual-budget constraints: a 200-call ceiling on WebSearch operations and a 200-subagent spawn limit per session (both configurable via environment variables). The `/clear` command resets these budgets. Additionally, MCP tool calls that exceed 2 minutes automatically migrate to background execution, preventing session freezes during long-running operations. Users can tune the threshold via `CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS`.

Configuration management has been simplified with `claude auto-mode reset`, which restores default settings with a confirmation prompt—or skipped entirely with the `--yes` flag. Finally, session resumption now offers a picker interface displaying all past sessions, including those removed from the active list, enabling easier recovery workflows.

## What happens next

These changes suggest Anthropic is prioritizing reliability and control in autonomous agent scenarios. The safety caps may guide future evolution toward more sophisticated resource negotiation within multi-agent systems.
*This article does not contain affiliate links.*
