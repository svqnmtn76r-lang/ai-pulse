---
category: feature_update
date: '2026-06-03'
generated_at: '2026-06-03T06:10:57.422784Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.161
template_type: breaking
title: anthropics/claude-code v2.1.161
word_count: 341
---

# Anthropic's Claude Code Gets Better Observability and Parallel Tool Execution in v2.1.161

## TL;DR

- **Observability upgrade**: Custom metric labels now let teams track Claude Code usage by dimension (team, repo, etc.) using OpenTelemetry attributes
- **Improved reliability**: Parallel tool calls now fail gracefully—a broken Bash command won't cascade to cancel other concurrent operations
- **Better UX**: Linux clipboard handling refined, accessibility settings honored across UI components, and agent progress displays show completion status

## What happened

Anthropic released Claude Code v2.1.161, a maintenance and feature release that strengthens operational visibility and execution robustness for teams running Claude-powered coding tasks at scale. The update, posted to [GitHub](https://github.com/anthropics/claude-code/releases/tag/v2.1.161), addresses longstanding requests from enterprise users managing complex workflows.

The standout feature introduces OpenTelemetry resource attributes as metric labels, enabling organizations to segment usage data across meaningful business dimensions. This matters for teams tracking costs or performance across repositories or departments—metrics can now be sliced by whatever custom attributes teams define in `OTEL_RESOURCE_ATTRIBUTES`.

Parallel execution gets more resilient: when Claude Code batches multiple tool calls (like simultaneous Bash commands), a failure in one call no longer cascades to kill siblings. Each tool now returns independent results, improving workflow reliability in multi-step automation scenarios.

The UI layer saw several refinements: agent row displays now show `done/total` progress indicators when work fans out across parallel tasks, peek functionality highlights the longest-running item, and the `/mcp` connector panel collapses unused claude.ai integrations under a disclosure toggle.

Accessibility improvements span motion-sensitive settings—the `/effort` dialog, workflow animations, and prompt keyword effects now properly honor "Reduce motion" preferences. Linux users benefit from improved clipboard handling using `wl-copy`, `xclip`, or `xsel` when available, with better middle-click paste support.

The release notes indicate a partial fix to managed-settings policy handling, though the changelog cuts off mid-sentence on `forceLoginOrgUUID` and `forceLoginMethod` blocks.

## What happens next

Teams using Claude Code in production should review the parallel execution changes if they rely on tool batching. Organizations already monitoring observability metrics will want to configure `OTEL_RESOURCE_ATTRIBUTES` to unlock granular usage breakdowns in their dashboards.
*This article does not contain affiliate links.*
