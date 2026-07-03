---
category: feature_update
date: '2026-07-03'
generated_at: '2026-07-03T04:51:19.111409Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.198
template_type: breaking
title: anthropics/claude-code v2.1.198
word_count: 292
---

## TL;DR

- **Background execution now default**: Anthropic's Claude-code subagents operate asynchronously by default, freeing up the main agent to continue working while background tasks complete
- **Autonomous PR workflows**: Background agents can now independently commit code, push changes, and open draft pull requests without manual intervention
- **Expanded capabilities**: New dataviz skill, Claude in Chrome GA, and AWS gateway support signal broader platform integration

## What happened

Anthropic has released Claude-code v2.1.198 with significant workflow improvements centered on asynchronous operations and agent autonomy. The update transitions subagents from blocking execution to background-by-default operation, allowing Claude to maintain productivity while awaiting agent completion notifications.

The release introduces notification hooks (`agent_needs_input` and `agent_completed`) that alert users when background agents require input or finish tasks. More notably, background agents launched through the `claude agents` interface now autonomously handle the entire code-to-PR workflow—committing changes, pushing to repositories, and opening draft pull requests—eliminating interruption points that previously halted execution.

Additional enhancements include a new `/dataviz` skill for chart and dashboard design guidance with integrated color-palette validation, and general availability of Claude in Chrome. The AWS integration adds anthropicAws as an upstream provider in the gateway system, with improved failover chain handling for model-not-found scenarios.

The Explore agent now inherits the parent session's model configuration (capped at opus-level performance) rather than defaulting to haiku, improving reasoning quality. Subagents and context compaction also now inherit extended thinking configurations from the host session.

## What happens next

These changes position Claude-code toward more autonomous development workflows, where agents can operate with minimal human supervision. Organizations should expect increasing independence in multi-stage code tasks—from exploration through deployment. The PR automation particularly signals movement toward full CI/CD integration. Watch for expanded agent capabilities and potential bidirectional platform integrations in subsequent releases.
*This article does not contain affiliate links.*
