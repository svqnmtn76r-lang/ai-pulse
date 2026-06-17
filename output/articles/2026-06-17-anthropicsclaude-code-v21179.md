---
category: feature_update
date: '2026-06-17'
generated_at: '2026-06-17T06:23:06.613965Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.179
template_type: breaking
title: anthropics/claude-code v2.1.179
word_count: 314
---

## TL;DR

- **Stability improvements**: Claude Code v2.1.179 addresses critical connection reliability issues that were causing partial data loss and UI lockups during tool execution
- **Cross-platform fixes**: Targeted regression fixes for Windows Subsystem for Linux (WSL2) environments and improved remote session performance
- **User experience refinements**: Nine distinct bug fixes focused on interface responsiveness, focus management, and session stability

## What happened

Anthropic has released Claude Code v2.1.179, a maintenance update focused on stability and reliability improvements across the development tool. Released on GitHub, this version tackles several high-impact issues that were degrading user experience, particularly for developers working in complex environments.

The headline fix addresses mid-stream connection drops—a critical issue where interrupted API responses previously displayed raw errors instead of gracefully preserving partial results. This was compounded by a UI state bug that left the tool execution spinner frozen at "running tool," creating confusion about actual session status.

The update also remedies a WSL2 regression introduced in v2.1.172 that broke mouse-wheel scrolling compatibility in Windows Terminal and VS Code—a significant pain point for Windows-based developers using Linux environments. Additionally, a Linux-specific bug causing sandbox permission glob patterns to generate enormous Bash tool descriptions has been resolved, preventing session crashes on systems with large directory trees.

Several interface usability improvements round out the release: fixing premature survey feedback interpretation, consolidating redundant promotional banners, restoring keyboard shortcuts (Ctrl+O) for subagent transcript viewing, and improving focus management between UI panels. Remote session users will benefit from corrected background task status displays and faster plugin loading times.

## What happens next

Developers using Claude Code should update to v2.1.179 immediately if experiencing connection instability or working in WSL2 environments. The fixes prioritize reliability over feature additions, suggesting Anthropic is consolidating the tool's foundation before future capability expansions. Teams relying on remote collaborative sessions will particularly want to verify the background task status improvements in their workflows.
*This article does not contain affiliate links.*
