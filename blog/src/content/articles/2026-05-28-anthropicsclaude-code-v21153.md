---
category: feature_update
date: '2026-05-28'
generated_at: '2026-05-28T05:37:28.084392Z'
generated_by: claude-haiku-4-5-2026-05-28
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.153
template_type: breaking
title: anthropics/claude-code v2.1.153
word_count: 349
---

# Claude Code v2.1.153 Brings Quality-of-Life Improvements and Stability Fixes

## TL;DR

- **Developer Experience**: Claude Code now provides better terminal awareness and clearer diagnostic tools for troubleshooting installation issues
- **Git Efficiency**: New LFS skip option reduces clone times for repositories with large binary assets
- **macOS Stability**: Background agents maintain permissions across upgrades while appearing as a unified application in system settings
- **Agent Capabilities**: Enhanced autocomplete and improved PR tracking in the agents interface streamline workflow management

## What happened

Anthropic has released Claude Code v2.1.153, a maintenance update focused on stability, developer experience, and cross-platform improvements. The release, available on GitHub, introduces several targeted enhancements addressing common developer friction points.

The most significant addition is a `skipLfs` configuration option for Git and GitHub plugin sources, allowing developers to bypass Git Large File System downloads during repository operations. This addresses performance bottlenecks for teams working with large binary assets or models stored in LFS.

Terminal integration has been refined with environment variable support—status line commands now receive `COLUMNS` and `LINES` variables, enabling scripts to intelligently adapt output formatting to terminal dimensions. This prevents text wrapping issues in dynamic shell environments.

The agents feature has received usability improvements: the PR column now displays clearer status indicators distinguishing single PRs from multiple pull requests, while the dispatch input autocomplete has been expanded to surface native slash commands alongside project and bundled skills.

System diagnostics have been enhanced through the `claude doctor` command, which now reports the outcome of the last update attempt, helping users identify installation or permission issues more rapidly. This complements a consolidated authentication notification system that merges separate MCP server and connector prompts into unified messages.

macOS users benefit from improved background agent handling—Claude Code now presents as a single application in Privacy & Security settings while preserving permission grants across version upgrades. This eliminates permission re-requests on updates.

A critical fix addresses stateful MCP server reconnection loops when GET SSE streams are unavailable, improving reliability for complex agent architectures.

## Learn more

For deployment details and configuration options, visit the [official GitHub release page](https://github.com/anthropic/claude-code/releases/tag/v2.1.153).
*This article does not contain affiliate links.*
