---
category: sdk_release
date: '2026-08-05'
generated_at: '2026-08-05T04:17:56.226054Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.222
template_type: explainer
title: anthropics/claude-code v2.1.222
word_count: 897
---

# Claude Code v2.1.222: Anthropic Patches Security and Reliability Issues

Anthropic has released version 2.1.222 of Claude Code, its AI-powered development tool, addressing several security vulnerabilities, reliability concerns, and user experience issues that affected both individual developers and enterprise teams.

## TL;DR

- **Git isolation bypass**: A critical security fix prevents isolated development sessions from executing destructive git commands against the main codebase
- **Tool restriction bypass**: Background tasks can no longer circumvent security restrictions through auto-allow hooks
- **Team/Enterprise blocking issue**: A UI bug preventing users from requesting new usage credits has been resolved
- **Network improvements**: Proxy connectivity and response timeout handling have been significantly improved
- **MCP server attribution**: Usage tracking for Model Context Protocol servers now correctly measures actual consumption rather than inflating metrics

## Background

Claude Code operates in an environment where developers grant AI agents access to run commands, edit files, and interact with version control systems. This power requires robust guardrails—without them, a misbehaving agent or exploited tool could wreak havoc on a developer's codebase.

Worktrees, a Git feature allowing multiple concurrent branches to exist in separate directories, were introduced to isolate experimental work from the main checkout. The premise was sound: dangerous operations within an isolated session couldn't affect production code. However, the isolation wasn't comprehensive enough.

Similarly, Anthropic's system includes "PreToolUse" hooks that can auto-allow certain operations, designed to streamline workflows without requiring constant user confirmation. These hooks, when used for background tasks like session summarization or renaming, were inadvertently bypassing the intended tool restrictions.

For enterprise users, a bug in the `/usage-credits` command created a permanent block: once a user's credit request was dismissed, the system incorrectly prevented them from submitting subsequent requests, locking them out of the process entirely.

## How it works

### Git Command Isolation and Destructive Operation Prevention

The core security fix addresses a gap in worktree isolation. Previously, isolated sessions and their sub-agents could execute git commands that would modify the main checkout—the primary branch or reference repository. This defeats the entire purpose of isolation.

Version 2.1.222 enforces isolation boundaries more strictly across all session types. Now, file editing and Bash command execution are restricted within isolated sessions, preventing agents from running commands like `git push` to the main branch or `git reset --hard` against the primary checkout. This layered approach ensures that isolation isn't just a conceptual boundary but an enforced technical constraint.

### Auto-Allow Hook Restrictions in Background Tasks

PreToolUse hooks streamline workflows by automatically permitting certain tool invocations. However, background processes—tasks that run without direct user interaction, such as generating session summaries or compacting conversation history—were using these hooks to bypass safety restrictions entirely.

The fix ensures that background agent tasks respect the same tool restrictions as foreground operations. Even if a hook is configured to auto-allow a particular action, background processes will still honor the underlying restrictions, preventing unintended tool usage in automated contexts.

### Team and Enterprise Usage Credit Request Flow

Enterprise teams often need to track and manage AI usage through credit systems. The `/usage-credits` command allows members to request additional credits when they've exhausted their allocation.

A bug in this system caused a permanent block after a user's request was dismissed or denied. The system failed to clear the "request pending" flag, causing subsequent attempts to trigger an error message suggesting the user had already submitted an outstanding request. This effectively locked users out of requesting credits again, even after weeks or months had passed.

The fix properly clears this flag when a request is dismissed, allowing users to submit new requests as needed.

### Proxy-Aware Connectivity and Timeout Handling

Claude Code performs a startup connectivity check to verify it can reach Anthropic's services. In corporate environments with HTTPS proxies, this check would hang indefinitely before failing with a vague error message.

The update applies Claude Code's existing proxy-aware transport layer—already used for API requests—to the startup connectivity check. Additionally, the check now implements a clear timeout with an informative error message, allowing users to quickly diagnose proxy configuration issues rather than waiting for a silent failure.

### Response Completion Detection and Error Reporting

Claude Code previously reported "Connection closed mid-response" errors for some API responses that had actually completed successfully. These false positives created confusion and unnecessary troubleshooting by users who believed their requests had failed when they'd actually succeeded.

The fix improves the response completion detection logic, distinguishing between genuinely interrupted responses and those that completed despite network quirks.

### Model Context Protocol Server Attribution

MCP servers extend Claude Code's capabilities by providing specialized tools and context. The usage tracking system was overattributing requests to these servers—counting every conversation turn that followed any MCP server tool invocation, regardless of whether that turn actually consumed the server's output.

The corrected attribution system now only counts usage toward an MCP server when a subsequent turn explicitly uses the results that server provided. This gives developers more accurate visibility into which servers are actually consuming their usage quota.

## What happens next

Organizations deploying Claude Code should prioritize updating to v2.1.222, particularly those with security policies around code modification and those operating in proxy-protected network environments. Teams using MCP servers should review their usage dashboards, as historical attribution may have been inflated.

The security fixes address real attack vectors that could compromise codebase integrity, while the reliability improvements enhance the developer experience in challenging network conditions.
*This article does not contain affiliate links.*
