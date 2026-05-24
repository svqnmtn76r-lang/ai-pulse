---
category: other
date: '2026-05-22'
generated_at: '2026-05-22T21:46:26.420091Z'
generated_by: claude-haiku-4-5-2026-05-22
importance_score: 50
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.147
template_type: breaking
title: anthropics/claude-code v2.1.147
word_count: 351
---

# Anthropic's Claude Code Gets Major UX Overhaul With v2.1.147

## TL;DR

- **Session management refined**: Pinned background sessions now persist intelligently, restarting only to apply updates while shedding gracefully under memory constraints
- **Code review tool replaces simplify**: New `/code-review` command with configurable effort levels and GitHub PR integration replaces the previous cleanup functionality
- **Developer experience polished**: Auto-updater improvements, better diff rendering for large files, and cleaner prompt history reduce friction in daily workflows

## What happened

Anthropic has released Claude Code v2.1.147, introducing a suite of refinements aimed at improving session stability and code analysis workflows. The update, available on GitHub, signals the team's focus on production-grade reliability for developers relying on Claude's agent capabilities.

The most significant change involves intelligent session management. Pinned background sessions—activated via `Ctrl+T` in claude agents—now remain active during idle periods and automatically restart to incorporate Claude Code updates without user intervention. Critically, when memory pressure increases, the system prioritizes keeping pinned sessions alive while shedding non-pinned sessions first, giving developers predictable behavior for their primary workflows.

Perhaps more immediately impactful is the `/simplify` command deprecation. The tool has been renamed to `/code-review` with fundamentally different behavior. Rather than performing automatic cleanup and fixes, it now conducts correctness analysis at user-specified effort levels (e.g., `/code-review high`). Developers can pass a `--comment` flag to automatically post findings as inline comments on GitHub pull requests, streamlining code quality workflows directly into existing review processes.

Under the hood, Anthropic has strengthened the auto-updater mechanism with transient network failure retries, detailed error reporting including OS-specific codes, and version information display on failure—addressing real-world deployment pain points where updates sometimes fail silently.

The release also includes performance optimizations for diff rendering when handling large file modifications, and a deduplication feature preventing consecutive identical prompt entries in history, reducing noise when developers repeatedly recall and resubmit commands.

## What happens next

Users upgrading to v2.1.147 should expect smoother background session handling and should adjust workflows that previously relied on `/simplify` for automatic code cleanup. The GitHub PR integration suggests Anthropic is positioning Claude Code deeper within standard development pipelines.
*Disclosure: This article contains affiliate links. As an affiliate, we earn from qualifying purchases at no extra cost to you.*
