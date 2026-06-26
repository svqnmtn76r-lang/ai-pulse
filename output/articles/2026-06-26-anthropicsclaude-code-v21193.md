---
category: feature_update
date: '2026-06-26'
generated_at: '2026-06-26T05:16:58.013904Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.193
template_type: breaking
title: anthropics/claude-code v2.1.193
word_count: 299
---

## TL;DR

- **Enhanced Security Controls**: Claude Code v2.1.193 introduces granular shell command classification and improved denial tracking for better auditability in auto-mode operations
- **Operational Transparency**: New OpenTelemetry logging for assistant responses enables comprehensive audit trails while respecting existing privacy configurations
- **Performance & UX Improvements**: Live file path autocomplete and automatic memory management reduce friction for developers using the code execution environment

## What happened

Anthropic has released Claude Code v2.1.193, a maintenance update that strengthens security governance and operational visibility in the code execution platform. [Per the official GitHub release](https://github.com/anthropics/claude-code/releases/tag/v2.1.193), the update focuses on three core areas: enhanced command routing, expanded telemetry capabilities, and resource optimization.

The most significant security enhancement is the new `autoMode.classifyAllShell` setting, which routes all Bash and PowerShell commands through the auto-mode classifier rather than only flagging arbitrary code execution patterns. This represents a shift toward more conservative command validation, allowing administrators to enforce stricter controls over shell operations enterprise-wide.

On the observability front, Anthropic has added OpenTelemetry logging for assistant responses through the `claude_code.assistant_response` event. Notably, the feature includes intelligent defaults: unless explicitly configured otherwise, deployments already logging user prompts will automatically begin capturing response content on upgrade. Organizations concerned about response logging can disable this via the `OTEL_LOG_ASSISTANT_RESPONSES=0` environment variable.

Additional usability improvements include live file path autocomplete in bash mode, a startup notification system for MCP servers requiring authentication, and automatic garbage collection for idle background shell processes to prevent memory bloat.

The release also addresses a UI regression affecting the `/model` endpoint and other client-data-gated interfaces that were displaying stale or empty values.

## What happens next

Teams deploying v2.1.193 should review their telemetry configurations immediately, particularly the new `OTEL_LOG_ASSISTANT_RESPONSES` behavior. Organizations requiring strict response privacy should explicitly set the opt-out flag before upgrading to prevent unintended logging.
*This article does not contain affiliate links.*
