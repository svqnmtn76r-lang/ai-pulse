---
category: other
date: '2026-05-22'
generated_at: '2026-05-22T21:46:35.326410Z'
generated_by: claude-haiku-4-5-2026-05-22
importance_score: 50
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.146
template_type: breaking
title: anthropics/claude-code v2.1.146
word_count: 373
---

# Anthropic Releases Claude Code v2.1.146 with Refined Developer Tools and Critical Stability Fixes

## TL;DR

- **Command restructuring**: The `/simplify` command has been rebranded to `/code-review` with configurable effort levels, shifting focus toward structured code analysis workflows.
- **Auto mode refinement**: Claude Code's autonomous operation now preserves user prompts and skill dependencies more intelligently, reducing unnecessary context losses during assisted development sessions.
- **Infrastructure stability**: Multiple critical regressions affecting Windows environments, background session management, and MCP protocol handling have been addressed in this maintenance release.

## What happened

Anthropic has shipped v2.1.146 of Claude Code, its AI-assisted development environment, introducing interface improvements alongside a substantial patch addressing platform-specific reliability issues. [The release, available on GitHub](https://github.com/anthropics/claude-code/releases/tag/v2.1.146), marks the third minor iteration in the v2.1 series and signals the team's focus on workflow refinement rather than feature expansion.

The most visible change replaces the `/simplify` command with `/code-review`, now accepting optional effort parameters (e.g., `/code-review high`). This semantic shift suggests Anthropic is repositioning the tool toward comprehensive code analysis rather than mere simplification, aligning with enterprise developer expectations around peer review automation.

A critical fix addresses auto mode behavior, where previously the system would suppress user-initiated questions during skill execution. The updated version now respects explicit user dependencies and skill-level prompts, improving the coherence of extended development workflows.

Windows developers receive particular attention in this release. A regression introduced in v2.1.124 caused PowerShell failures when `pwsh` was installed via Windows Package Manager or Microsoft Store—now resolved. Additional Windows-specific fixes tackle full-screen strobing in Windows Terminal during streaming operations and correct improper NTFS junction traversal when removing background job worktrees.

The Model Context Protocol (MCP) integration gains robustness through fixes to resource pagination, where `resources/list`, `resources/templates/list`, and `prompts/list` operations were discarding data beyond the first page on servers with pagination enabled. Tool permission re-prompting in backgrounded sessions has also been corrected, reducing friction in multi-session workflows.

## What happens next

Users should update immediately if experiencing Windows PowerShell integration or pagination issues. The command rename requires workflow adjustments for existing `/simplify` users, though the added effort-level configuration may justify the transition overhead. Anthropic's emphasis on stability over new features suggests the platform is approaching feature completeness, with engineering resources now focused on reliability at scale.
*Disclosure: This article contains affiliate links. As an affiliate, we earn from qualifying purchases at no extra cost to you.*
