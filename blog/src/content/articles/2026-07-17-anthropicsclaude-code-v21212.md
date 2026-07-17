---
category: feature_update
date: '2026-07-17'
generated_at: '2026-07-17T04:14:25.893462Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.212
template_type: breaking
title: anthropics/claude-code v2.1.212
word_count: 308
---

## TL;DR

- **Conversation forking now spawns background sessions**: The `/fork` command creates independent parallel work streams instead of inline subagents, improving workflow flexibility
- **Runaway loops are now contained**: New safeguards cap WebSearch calls (200/session) and subagent spawns (200/session) to prevent resource exhaustion
- **Long-running tools move to background automatically**: MCP operations exceeding 2 minutes shift background-ward, keeping the main session responsive

## What happened

Anthropic has released Claude Code v2.1.212, introducing significant workflow and stability improvements to its agent-based development environment. The update fundamentally restructures how conversation branching works while adding multiple guardrails against cascading delegation loops—a persistent challenge in agentic systems.

The most visible change redefines the `/fork` command. Previously, forking launched inline subagents within the current session. Now it copies the conversation into a separate background session that appears as its own row in the `claude agents` interface, allowing parallel independent work streams while the user continues in the original session. The old behavior has been renamed `/subtask` for users who need inline delegation.

To prevent runaway behavior, Anthropic implemented two configurable caps: a session-wide limit of 200 WebSearch tool calls (tunable via `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION`) and a subagent spawn ceiling of 200 per session (`CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION`). Both limits reset with `/clear`, giving users explicit control over computational budgets.

The release also addresses responsiveness. MCP tool calls exceeding a 2-minute threshold now automatically transition to background execution, configurable via `CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS`, keeping interactive sessions from blocking. Additionally, `/resume` now opens a session picker including previously deleted sessions, improving recoverability.

Finally, `claude auto-mode reset` restores default configuration with optional `--yes` flag to bypass confirmation—useful for troubleshooting misconfigured automation states.

## What happens next

These changes suggest Anthropic is optimizing Claude Code for longer-running, multi-threaded development workflows while learning from production incidents involving resource exhaustion. The session recovery features hint at expanding use cases in interrupted or exploratory development scenarios.
*This article does not contain affiliate links.*
