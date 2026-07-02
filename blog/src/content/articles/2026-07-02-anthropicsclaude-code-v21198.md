---
category: feature_update
date: '2026-07-02'
generated_at: '2026-07-02T01:50:46.159903Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.198
template_type: breaking
title: anthropics/claude-code v2.1.198
word_count: 343
---

# Anthropic Releases Claude Code v2.1.198 with Major Agent Improvements and Browser Integration

## TL;DR

- **Browser availability**: Claude in Chrome moves to general availability, expanding the AI assistant's reach beyond web interfaces
- **Autonomous workflows**: Background agents now automatically commit code changes and open pull requests, reducing manual handoff steps
- **Enhanced reliability**: Network resilience improvements prevent mid-response failures, addressing a critical user experience pain point

## What happened

Anthropic has released Claude Code v2.1.198, marking a significant expansion in the platform's agent capabilities and accessibility. The update, published on GitHub, rolls Claude in Chrome out of beta into general availability—a milestone suggesting the company is confident in the browser integration's stability and feature completeness.

More substantially, the release overhauls how background agents operate. Previously, autonomous agents running code tasks would pause to request user confirmation before proceeding. Now, agents automatically commit changes, push to repositories, and open draft pull requests when work completes, streamlining development workflows considerably. This automation reduces friction in CI/CD pipelines where agents handle routine coding tasks.

The update introduces a new `/dataviz` skill targeting data visualization work, bundled with a color-palette validator—useful for teams building dashboards or charts programmatically. Infrastructure-wise, Anthropic has added AWS as an upstream provider within its gateway layer, a move suggesting deeper integration with enterprise cloud deployments.

On the technical side, the release addresses reliability gaps. Transient network errors that previously aborted mid-response now trigger automatic retries with exponential backoff, addressing a frustration point for users working with long-running operations. Additionally, subagents and context compaction now inherit extended thinking configurations from parent sessions, improving reasoning quality on delegated tasks.

The Explore agent has been rebalanced to use the main session's model (capped at Claude Opus) instead of defaulting to Haiku, addressing performance concerns for complex exploration tasks.

## What happens next

These changes position Claude Code as a more autonomous, production-grade development tool. Organizations using agents for code generation and CI/CD should expect faster task completion and fewer intervention points. The browser expansion signals Anthropic's push into consumer accessibility alongside enterprise automation capabilities.
*This article does not contain affiliate links.*
