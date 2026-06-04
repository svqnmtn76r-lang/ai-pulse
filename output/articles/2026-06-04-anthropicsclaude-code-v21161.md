---
category: feature_update
date: '2026-06-04'
generated_at: '2026-06-04T06:02:31.604894Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.161
template_type: breaking
title: anthropics/claude-code v2.1.161
word_count: 348
---

# Anthropic Releases Claude Code v2.1.161 With Enhanced Observability and Parallel Tool Execution

## TL;DR

- **Observability upgrade**: Custom resource attributes now propagate as metric labels, enabling fine-grained usage tracking by team or repository
- **Improved reliability**: Parallel tool execution now fails independently—one broken command won't cascade failures across batch operations
- **UX refinements**: Terminal clipboard handling improved on Linux, accessibility fixes for motion-sensitive users, and cleaner connector management

## What happened

Anthropic has shipped Claude Code v2.1.161, introducing operational and reliability improvements focused on enterprise deployment scenarios. The release prioritizes observability for teams tracking usage across organizational units and fixes a critical parallel execution limitation that previously caused cascading failures.

The most significant change addresses observability: `OTEL_RESOURCE_ATTRIBUTES` values now surface as labels on metric datapoints, allowing organizations to slice usage analytics by custom dimensions—critical for multi-team deployments needing cost allocation or performance attribution. This extends Anthropic's push toward production-grade monitoring capabilities for Claude-powered applications.

On the execution side, the update decouples parallel tool call failures. Previously, when Claude Code fanned out work across multiple bash commands or API calls, a single failed command would abort the entire batch. Version 2.1.161 returns individual results for each tool, allowing workflows to handle partial failures gracefully—a standard requirement for robust automation pipelines.

The release also refines the user experience: the `/mcp` connector management now hides unused connectors behind a collapsible row, reducing interface clutter. Terminal clipboard operations on Linux now intelligently select between `wl-copy`, `xclip`, and `xsel` depending on availability, addressing fragmentation across Linux desktop environments. The update fixes accessibility regressions where motion-reduction settings weren't honored in dialogs, animations, and UI elements.

Minor fixes include corrections to `forceLoginOrgUUID` and `forceLoginMethod` managed-settings policies that had blocked certain authentication flows. The `claude agents` command now displays work distribution as `done/total` when parallelizing tasks, with peek mode highlighting the longest-running item for bottleneck identification.

## What happens next

Teams using Claude Code should evaluate whether the parallel execution reliability improvements warrant upgrading, particularly those running multi-step automation workflows. The metrics observability enhancements merit immediate adoption for organizations implementing chargeback or usage governance models.
*This article does not contain affiliate links.*
