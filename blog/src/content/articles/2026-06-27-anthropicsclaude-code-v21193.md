---
category: feature_update
date: '2026-06-27'
generated_at: '2026-06-27T01:47:33.733199Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.193
template_type: breaking
title: anthropics/claude-code v2.1.193
word_count: 301
---

## TL;DR

- **Enhanced Security Controls**: Claude Code v2.1.193 introduces granular shell command routing through auto-mode classifiers, giving administrators tighter control over code execution patterns.
- **Observability Improvements**: New OpenTelemetry logging captures assistant responses with privacy-conscious defaults that respect existing deployment configurations.
- **User Experience Refinements**: Live file path autocomplete and MCP authentication notices streamline workflows while automatic memory management reduces resource overhead.

## What happened

Anthropic has released Claude Code v2.1.193, a maintenance update that emphasizes security hardening, observability, and operational efficiency. Available via the anthropics/claude-code GitHub repository, the release introduces several notable improvements aimed at enterprise deployments and power users.

The update's most significant addition is the `autoMode.classifyAllShell` setting, which extends the auto-mode classifier to route all Bash and PowerShell commands through security screening—previously limited to arbitrary code execution patterns. This change gives deployment administrators finer-grained control over shell command execution policies.

On the observability front, Claude Code now emits `claude_code.assistant_response` OpenTelemetry events, allowing organizations to monitor model outputs alongside user inputs. Notably, Anthropic designed this feature with privacy-first defaults: response logging is redacted unless explicitly enabled, and follows existing `OTEL_LOG_USER_PROMPTS` settings to prevent unintended data collection during upgrades.

Additional improvements include live file path autocomplete in bash mode (triggered by `!`), startup notifications when MCP servers require authentication, and automatic memory reaping for idle background shell processes—reducing resource exhaustion in long-running sessions.

The release also addresses a UI bug affecting `/model` and client-data-gated interfaces that displayed stale or empty information.

## What happens next

Organizations running Claude Code should review the new `autoMode.classifyAllShell` setting to determine whether stricter shell command classification aligns with their security posture. Those using OpenTelemetry should explicitly configure response logging preferences before upgrading to avoid unintended changes in observability behavior.

Learn more: Visit the GitHub release page for detailed migration guidance and configuration examples.
*This article does not contain affiliate links.*
