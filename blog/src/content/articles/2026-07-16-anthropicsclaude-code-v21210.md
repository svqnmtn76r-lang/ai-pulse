---
category: feature_update
date: '2026-07-16'
generated_at: '2026-07-16T04:14:57.375029Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.210
template_type: breaking
title: anthropics/claude-code v2.1.210
word_count: 313
---

# Claude Code v2.1.210 Brings UX Improvements and Critical Security Fixes

## TL;DR

- **Live feedback**: Tool execution now displays real-time elapsed-time counters, eliminating the appearance of frozen operations
- **Security hardened**: Fixed critical isolation bypass where subagents could mutate the main repository, plus patched permission rule vulnerabilities
- **Polish push**: Multiple UI and integration fixes address external editor compatibility and session stability issues

## What happened

Anthropic released v2.1.210 of Claude Code, its AI-powered development toolkit, rolling out a maintenance update focused on user experience refinement and security hardening. [Available on GitHub](https://github.com/anthropics/claude-code/releases/tag/v2.1.210), the release addresses nine distinct issues spanning interface responsiveness, permission enforcement, and system reliability.

The most visible change targets a longstanding UX pain point: long-running tool executions now display animated elapsed-time counters on the collapsed tool summary line. This addresses user feedback that extended operations appeared unresponsive, improving confidence in tool execution status.

On the security front, the update patches a meaningful isolation vulnerability where subagents configured with `isolation: 'worktree'` could execute git-mutating commands against the main repository checkout instead of their isolated workspaces. The release also adds startup warnings for deprecated permission rules (`Write(path)`, `NotebookEdit(path)`, `Glob(path)`), nudging developers toward safer alternatives like `Edit(path)` and `Read(path)`.

Additional fixes target the `ultracode` keyword opt-in mechanism, which was incorrectly firing on non-human inputs like webhook payloads and relay PR comments, potentially triggering unintended automation. The update also resolves text rendering and clipboard issues that caused È/É characters to leak into external editors and UI components to contaminate crash telemetry.

Session reliability received attention with improvements to the `claude attach` command, which previously failed intermittently during daemon transitions with "job not found" or "agent is still starting" errors.

## What happens next

Users should upgrade to capture the security isolation fix immediately. The quality-of-life improvements—particularly the live elapsed-time feedback—enhance developer workflows, while permission deprecation warnings signal breaking changes likely coming in future releases.
*This article does not contain affiliate links.*
