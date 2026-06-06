---
category: feature_update
date: '2026-06-06'
generated_at: '2026-06-06T05:00:33.417937Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.166
template_type: breaking
title: anthropics/claude-code v2.1.166
word_count: 313
---

## TL;DR

- **Resilience upgrade**: Claude Code v2.1.166 introduces configurable fallback models and automatic retry logic to handle API overloads gracefully
- **Security hardening**: Cross-session messaging now strips user authority, preventing permission escalation attacks between Claude instances
- **Granular control**: Users gain finer-grained thinking token management and glob pattern support for tool access policies

## What happened

Anthropic has released Claude Code v2.1.166 with significant improvements to reliability, security, and configurability. The update prioritizes handling infrastructure stress through a new fallback model system that automatically tries up to three alternate models when the primary selection becomes unavailable or overloaded. This feature extends to interactive sessions, not just batch operations, addressing a common pain point for users during peak usage periods.

The release also tackles cross-session security vulnerabilities by redesigning how Claude Code instances communicate. Messages relayed between separate sessions no longer inherit the sender's user permissions, and auto mode explicitly blocks relayed permission requests. This prevents a potential attack vector where a compromised or malicious session could escalate privileges through message forwarding.

Technical improvements include glob pattern support for deny rules—administrators can now use wildcards like `"*"` to block all tools at once—and more nuanced control over Claude's extended thinking feature. Users can now disable thinking entirely via `MAX_THINKING_TOKENS=0`, `--thinking disabled` flags, or per-model toggles, applying the setting across all Claude API models that use thinking by default.

The update also enhances error handling by implementing selective retry logic: unexpected non-retryable API errors trigger an automatic fallback attempt, while authentication, rate-limiting, and transport errors surface immediately to avoid cascading failures.

## What happens next

Organizations running Claude Code in production should review the new fallback model configuration to optimize their deployment strategy. Security teams should validate cross-session messaging policies align with their threat models. The thinking token controls warrant testing on models where inference costs or latency are concerns.

Learn more at [github.com/anthropics/claude-code](https://github.com/anthropics/claude-code/releases/tag/v2.1.166)
*This article does not contain affiliate links.*
