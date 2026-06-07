---
category: feature_update
date: '2026-06-07'
generated_at: '2026-06-07T05:46:12.609084Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.166
template_type: breaking
title: anthropics/claude-code v2.1.166
word_count: 323
---

## TL;DR

- **Resilience boost**: Claude Code v2.1.166 introduces fallback model configuration, allowing developers to specify up to three backup models when primary instances become overloaded or unavailable
- **Security hardening**: Cross-session messaging now strips user authority from relayed messages, preventing permission escalation attacks between Claude sessions
- **Flexibility in reasoning**: New controls disable extended thinking on Claude 3 models by default, while maintaining provider-specific behavior for third-party implementations

## What happened

Anthropic has released Claude Code v2.1.166, a maintenance update focused on reliability, security, and operational flexibility. The release introduces several substantial improvements to model failover handling and session isolation, addressing pain points developers encounter in production environments.

The headline feature enables configurable fallback models via a new `fallbackModel` setting, allowing users to specify up to three alternative models attempted sequentially when the primary model reaches capacity or becomes unavailable. This extends the `--fallback-model` CLI argument to interactive sessions, improving availability for long-running workflows.

Security receives particular attention through hardened cross-session messaging protocols. Messages relayed between Claude sessions via the `SendMessage` tool no longer inherit the original user's permissions—a critical security boundary. Receivers now explicitly refuse relayed permission requests, and auto mode blocks them entirely, preventing potential privilege escalation scenarios.

Additional changes address operational control. Developers can now use glob patterns (`*`) in deny rule tool-name positions to block entire tool categories simultaneously. The update also refines thinking token behavior: setting `MAX_THINKING_TOKENS=0`, using `--thinking disabled`, or toggling the per-model thinking switch now disables extended thinking on Claude 3 models accessed via the Claude API, while preserving third-party provider configurations.

Error handling improvements include single-turn retries on fallback models for unexpected non-retryable API errors, though authentication, rate-limit, request-size, and transport errors surface immediately without retry.

## What happens next

Users should review fallback model configurations for critical applications and audit cross-session message patterns for security implications. The thinking token controls merit testing against reasoning-dependent workflows to ensure expected performance characteristics.

Learn more: [github.com/anthropics/claude-code](https://github.com/anthropics/claude-code/releases/tag/v2.1.166)
*This article does not contain affiliate links.*
