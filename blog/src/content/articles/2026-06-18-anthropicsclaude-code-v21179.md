---
category: feature_update
date: '2026-06-18'
generated_at: '2026-06-18T06:03:20.162753Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.179
template_type: breaking
title: anthropics/claude-code v2.1.179
word_count: 293
---

## TL;DR

- **Stability improvements**: Claude Code v2.1.179 fixes critical connection handling and UI responsiveness issues that degraded user experience
- **Cross-platform fixes**: Windows Terminal and VS Code WSL2 users regain mouse-wheel scrolling functionality after a regression in the previous build
- **Performance gains**: Remote session plugin loading receives optimization alongside resolution of background task visibility issues

## What happened

Anthropic has released Claude Code v2.1.179, a maintenance update addressing multiple stability and usability regressions affecting the AI-powered code assistant. The update, released via GitHub's official Anthropic repository, prioritizes connection resilience and interface responsiveness across different operating environments.

The most critical fix addresses mid-stream connection drops, a particularly problematic scenario where network interruptions previously resulted in raw error messages and frozen UI spinners. The new version preserves partial responses during disconnections, allowing users to retain work progress and view meaningful feedback rather than cryptic error states.

A significant regression introduced in version 2.1.172 caused mouse-wheel scrolling failures in WSL2 environments running Windows Terminal and VS Code—this has been remedied. The update also resolves a Linux-specific issue where overly permissive sandbox glob patterns on large directory trees generated oversized Bash tool descriptions, rendering sessions effectively unusable due to performance degradation.

Additional fixes target user experience friction: the feedback survey no longer triggers unintended session ratings from single-digit inputs, promotional banner stacking has been eliminated, and keyboard navigation (Ctrl+O) now properly displays subagent transcripts. Focus management improvements ensure the prompt input properly regains attention when clicked away from footer panels.

Remote session users benefit from background task visibility fixes—tasks no longer appear permanently "stuck" between turns—alongside improved plugin loading performance that should reduce latency in cloud-based workflows.

## Learn more

For implementation details and complete changelog, visit the [official Claude Code releases page](https://github.com/anthropics/claude-code/releases/tag/v2.1.179) on GitHub.
*This article does not contain affiliate links.*
