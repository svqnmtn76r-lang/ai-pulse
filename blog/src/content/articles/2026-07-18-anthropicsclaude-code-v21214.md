---
category: feature_update
date: '2026-07-18'
generated_at: '2026-07-18T04:07:30.531703Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.214
template_type: breaking
title: anthropics/claude-code v2.1.214
word_count: 325
---

## TL;DR

- **Security fixes**: Anthropic addressed multiple permission-check vulnerabilities in Claude Code that could allow unintended command execution across different shells and operating systems
- **Scope creep resolved**: Directory allow-rules were incorrectly permitting writes outside their intended scope, now confined to the current working directory
- **Operational reliability**: Long commands and edge-case shell syntax no longer bypass safety prompts, closing vectors for silent execution

## What happened

Anthropic released version 2.1.214 of Claude Code on GitHub, focusing primarily on security hardening rather than feature additions. The update patches six distinct permission-validation vulnerabilities that could permit unsafe command execution without user approval—a critical concern for an AI coding assistant with shell access.

The most severe issues involved permission-check bypasses across multiple shell environments. Windows PowerShell 5.1 sessions contained a complete permission-check bypass, while Bash implementations failed to properly validate file-descriptor redirects and struggled to parse long commands exceeding 10,000 characters. Additionally, Bash was incorrectly handling zsh variable subscripts and modifiers in conditional statements, treating them as benign when they could execute arbitrary code.

A directory scoping bug allowed single-segment wildcard rules like `Edit(src/**)` to auto-approve file writes to nested directories anywhere in the filesystem, rather than restricting changes to the current working directory tree. This represents a significant containment failure that could expose unintended file modifications.

Permission prompts on remote sessions also had a timing vulnerability where execution could proceed before users confirmed the local dialog—a race condition affecting distributed workflows.

The release notes mention an incomplete entry referencing "EndConv" functionality, suggesting additional changes may be pending documentation.

## What happens next

Users should update immediately, particularly those running Claude Code on Windows PowerShell or executing complex Bash commands. The fixes directly impact the security model developers rely on when delegating code changes to AI agents. This release underscores the ongoing tension between functionality and safety in autonomous coding tools—as AI gains more shell privileges, permission systems become increasingly sophisticated attack surfaces requiring constant vigilance.
*This article does not contain affiliate links.*
