---
category: feature_update
date: '2026-07-20'
generated_at: '2026-07-20T04:42:19.383197Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.215
template_type: breaking
title: anthropics/claude-code v2.1.215
word_count: 323
---

# Anthropic's Claude Code Gets User Control Update with v2.1.215 Release

## TL;DR

- **Shift in automation**: Claude Code no longer automatically executes verification and code review functions—users must now explicitly invoke them
- **Enhanced user agency**: The change gives developers more control over their workflows and reduces unsolicited automated processes
- **Available now**: v2.1.215 is live on GitHub, requiring manual invocation via `/verify` and `/code-review` commands

## What happened

Anthropic has rolled out a significant behavioral adjustment to its Claude Code tool with the v2.1.215 release, fundamentally altering how automated code assistance functions are triggered. Previously, the platform would autonomously run verification and code review processes, but the latest update requires explicit user intervention to activate these capabilities.

The change reflects a broader design philosophy prioritizing user control and workflow transparency. Rather than having the AI proactively scan code for issues, developers must now consciously request these operations by issuing the `/verify` or `/code-review` commands within their development environment.

This architectural shift has practical implications for development teams. While some users may appreciate reduced background processing and clearer audit trails of when and why analyses occur, others might experience workflow disruptions if they relied on automatic verification. The modification also potentially reduces computational overhead and API calls, which could have cost implications for enterprises using the tool at scale.

The release, documented on [Anthropic's GitHub repository](https://github.com/anthropic/claude-code/releases/tag/v2.1.215), represents incremental refinement rather than feature expansion—typical of mature developer tools evolving based on user feedback and operational requirements.

## What happens next

Development teams currently using Claude Code should review their existing workflows and adjust processes to explicitly trigger verification and code review steps. Organizations should communicate this change to their engineering teams to prevent workflow confusion during the transition period.

For those evaluating Claude Code as a development assistant, this user-driven approach may appeal to teams prioritizing explicit control over automated processes. The change underscores Anthropic's iterative approach to balancing convenience with developer agency.
*This article does not contain affiliate links.*
