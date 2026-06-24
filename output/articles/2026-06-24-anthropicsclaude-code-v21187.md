---
category: feature_update
date: '2026-06-24'
generated_at: '2026-06-24T05:07:27.464637Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.187
template_type: breaking
title: anthropics/claude-code v2.1.187
word_count: 314
---

## TL;DR

- **Security hardening**: New sandbox credential-blocking feature and organization-level model restrictions strengthen enterprise governance
- **Reliability improvements**: Critical fixes address structured output loops, MCP tool timeouts, and conversation resumption failures
- **UX refinement**: Mouse click support in fullscreen mode and expanded model picker controls enhance usability

## What happened

Anthropic has released Claude Code v2.1.187, introducing meaningful security, reliability, and user experience improvements across its developer-focused tool. The update addresses several pain points that have affected production deployments and enterprise adoption.

On the security front, a new `sandbox.credentials` setting now blocks sandboxed command execution from accessing credential files and secret environment variables—a critical safeguard for organizations running Claude Code in shared or less-controlled environments. Complementing this, the release introduces organization-configured model restrictions that propagate across the model picker interface, CLI flags (`--model`), slash commands (`/model`), and environment variables (`ANTHROPIC_MODEL`), with clear messaging when restrictions apply.

The stability fixes target persistent issues affecting workflows. The `--resume` flag now correctly handles conversations where the original `-p` run produced no model turns, eliminating "No conversation found" errors. More significantly, structured output has been overhauled: the model can no longer enter infinite `StructuredOutput` re-call loops after successful execution, and follow-up turns now reliably maintain structured formatting.

Remote Model Context Protocol (MCP) tool calls have been made finite—they now timeout with an error after 5 minutes of inactivity rather than blocking indefinitely, with configurable override via `CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT`.

Minor UX improvements include mouse click support for interactive elements like permission prompts and configuration dialogs in fullscreen mode, addressing accessibility gaps for users preferring pointer-based navigation.

## What happens next

These changes position Claude Code as more suitable for regulated environments and long-running agentic workflows. Organizations should prioritize testing the new credential-blocking settings in sandbox configurations and review their model restriction policies. The structured output fix is particularly critical for teams relying on JSON schema validation in multi-turn conversations.
*This article does not contain affiliate links.*
