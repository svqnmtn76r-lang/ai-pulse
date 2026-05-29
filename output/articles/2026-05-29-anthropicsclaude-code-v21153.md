---
category: feature_update
date: '2026-05-29'
generated_at: '2026-05-29T05:19:37.525058Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.153
template_type: breaking
title: anthropics/claude-code v2.1.153
word_count: 308
---

# Claude Code v2.1.153: Enhanced Developer Experience with LFS Controls and Agent Improvements

## TL;DR

- **Git LFS optimization**: New `skipLfs` option lets developers bypass large file downloads during repository operations, reducing clone and update times
- **Developer visibility improvements**: Enhanced diagnostics through `/doctor` command and clearer status messaging for authentication and update issues
- **Terminal-aware scripting**: Status line commands now receive environment variables for responsive output sizing

## What happened

Anthropic has released Claude Code v2.1.153, introducing a suite of refinements aimed at streamlining developer workflows and improving the tool's integration with version control systems. The update, [available on GitHub](https://github.com/anthropics/claude-code/releases/tag/v2.1.153), addresses friction points in common development scenarios while enhancing observability into system health.

The marquee addition is the `skipLfs` option for GitHub and Git plugin sources, enabling developers to bypass Git Large File Storage downloads during clone and update operations. This addresses a known pain point where LFS bandwidth consumption can significantly slow repository operations, particularly valuable for teams working with machine learning models or large datasets.

Diagnostic capabilities have been strengthened: the newly enhanced `/doctor` command now displays results from the last update attempt, helping users troubleshoot installation issues independently. Alongside this, npm global install notifications consolidate previously scattered messaging around auto-update failures into actionable guidance.

The `claude agents` feature receives multiple refinements, including autocomplete suggestions that now encompass native slash commands and bundled skills alongside project-specific options. PR column formatting has been clarified to distinguish between single and multiple pull requests at a glance.

Additional improvements include terminal-aware environment variable passing (`COLUMNS` and `LINES`) for status line scripts, unified authentication prompts for MCP servers and connectors, and platform-specific enhancements for macOS—background agents now integrate more cleanly with Privacy & Security settings while maintaining permissions across upgrades.

## Learn more

For implementation details and the complete changelog, visit the [v2.1.153 release page](https://github.com/anthropics/claude-code/releases/tag/v2.1.153) on the Anthropic repository.
*This article does not contain affiliate links.*
