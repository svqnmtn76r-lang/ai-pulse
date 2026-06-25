---
category: feature_update
date: '2026-06-25'
generated_at: '2026-06-25T05:12:18.828562Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.187
template_type: breaking
title: anthropics/claude-code v2.1.187
word_count: 319
---

## TL;DR

- **Security hardening**: Anthropic's Claude Code now blocks sandboxed commands from accessing credential files and secret environment variables through a new `sandbox.credentials` setting
- **Enterprise controls**: Organizations can now restrict which AI models developers can use within Claude Code, with enforcement across the CLI and UI
- **Reliability improvements**: Critical fixes address remote tool timeouts, structured output loops, and session resumption bugs affecting production workflows

## What happened

Anthropic shipped Claude Code v2.1.187, a maintenance release focusing on security, enterprise governance, and stability improvements across its AI-assisted coding environment. The update arrives as enterprises increasingly integrate Claude into development workflows and require stronger controls over model access and data handling.

The most significant addition is a `sandbox.credentials` configuration option that prevents sandboxed code execution from reading sensitive files like `.ssh`, `.aws`, and environment variables containing secrets. This addresses a critical gap in credential isolation—previously, code running in Claude Code's execution sandbox could potentially access authentication material.

On the enterprise side, organizations can now enforce model restrictions organization-wide. When restricted models are selected via the model picker, CLI flag (`--model`), or environment variable (`ANTHROPIC_MODEL`), users see a "restricted by your organization's settings" message, giving IT teams centralized control over which Claude variants developers can access.

The release also fixes several reliability issues: the `--resume` flag no longer fails when prior runs produced no model interactions; structured output no longer loops indefinitely after successful schema calls; and remote Model Context Protocol (MCP) tool calls that previously hung for five minutes now properly abort with errors (configurable via `CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT`).

These changes suggest Anthropic is prioritizing Claude Code's readiness for enterprise adoption, where security isolation, compliance controls, and production reliability are non-negotiable requirements.

## What happens next

Developers should review the `sandbox.credentials` documentation if deploying Claude Code in shared or untrusted environments. Enterprise customers should check their organization's model configuration to understand which Claude variants their teams can access going forward.
*This article does not contain affiliate links.*
