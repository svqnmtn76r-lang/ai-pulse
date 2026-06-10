---
category: feature_update
date: '2026-06-10'
generated_at: '2026-06-10T05:26:59.505336Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.169
template_type: breaking
title: anthropics/claude-code v2.1.169
word_count: 308
---

## TL;DR

- **Safe Mode Added**: Claude Code v2.1.169 introduces a `--safe-mode` flag to disable all customizations for troubleshooting, addressing a critical need for diagnostic workflows
- **Directory Navigation**: New `/cd` command allows session migration to different working directories while preserving prompt cache, reducing friction in multi-project environments
- **Enterprise Security Tightened**: MCP server policies now properly enforced across all connection scenarios, fixing a notable gap in organization-level access controls

## What happened

Anthropic has released Claude Code v2.1.169, introducing several quality-of-life improvements and critical bug fixes for developers relying on the AI-assisted coding platform. The update, published on GitHub, targets both individual developers and enterprise deployments with enhanced troubleshooting capabilities and stricter security enforcement.

The headline feature is the new safe mode, which strips away all user customizations—including CLAUDE.md configurations, plugins, skills, hooks, and MCP servers—in a single flag. This addresses a long-standing pain point: isolating whether issues stem from core functionality or custom extensions without manual teardown.

Equally significant for multi-project workflows is the `/cd` command, enabling developers to change working directories mid-session without severing the prompt cache. This preserves context continuity, which is particularly valuable given Claude's reliance on cached interactions for performance.

On the enterprise front, Anthropic fixed enforcement gaps in managed MCP (Model Context Protocol) policies. Previously, organization-level server allowlists and denylists weren't reliably applied during reconnections, IDE-typed configurations, or initial post-install sessions. The patch also addresses cold-start latency issues for organizations lacking remote policy settings.

The update includes refinements to terminal UX—arrow key navigation through command history now respects wrapped text rows rather than jumping erratically—and a new `disableBundledSkills` setting to reduce noise in the model's available actions.

## Learn more

For implementation details and migration guidance, consult the [official GitHub release page](https://github.com/anthropics/claude-code/releases/tag/v2.1.169). Enterprise administrators should prioritize testing the MCP policy enforcement fixes in staging environments before rolling out to production instances.
*This article does not contain affiliate links.*
