---
category: feature_update
date: '2026-07-19'
generated_at: '2026-07-19T04:27:21.187290Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.215
template_type: breaking
title: anthropics/claude-code v2.1.215
word_count: 304
---

# Anthropic's Claude Code Gets Smarter About When to Auto-Run Skills

## TL;DR

- **User Control**: Claude Code v2.1.215 stops automatically executing verification and code review tasks, requiring explicit `/verify` and `/code-review` commands instead
- **Workflow Impact**: The change reduces unsolicited background processing, giving developers more predictable control over their development pipeline
- **Developer Experience**: Users must now intentionally trigger quality checks rather than having them run passively during coding sessions

## What happened

Anthropic released Claude Code v2.1.215 with a significant shift in how automated code analysis features operate. The update fundamentally changes the behavior of two core skills—verification and code review—by moving them from automatic execution to manual invocation only.

Previously, Claude would autonomously run `/verify` and `/code-review` operations in the background as part of its standard workflow. The new version disables this automatic behavior entirely. Developers must now explicitly invoke these skills when they want Claude to analyze their code, providing granular control over when quality assurance processes execute.

This architectural change reflects a broader design philosophy prioritizing user intent and predictability. Automatically running resource-intensive analysis tasks can slow down development cycles and consume API quota unexpectedly. By requiring explicit commands, developers gain transparency into their tool usage and maintain tighter control over their coding workflow.

The release was published on the [Anthropic Claude Code GitHub repository](https://github.com/anthropics/claude-code/releases/tag/v2.1.215), signaling this is part of the actively maintained development toolkit for Claude-based development workflows.

## What happens next

Teams using Claude Code should update their documentation and developer practices to reflect the new manual-invocation requirement. For development workflows that previously relied on automatic verification, explicit `/verify` and `/code-review` commands will need to be incorporated into standard processes.

This change suggests Anthropic is refining Claude's autonomy boundaries—a pattern likely to continue as the company balances powerful automation with user control in its broader product ecosystem.
*This article does not contain affiliate links.*
