---
category: feature_update
date: '2026-06-28'
generated_at: '2026-06-28T01:50:20.774377Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.195
template_type: breaking
title: anthropics/claude-code v2.1.195
word_count: 333
---

## TL;DR

- **Stability focus**: Claude Code v2.1.195 addresses seven critical bugs affecting core functionality, from voice dictation to plugin management
- **Developer experience**: Hook matchers now use exact matching instead of substring matching, preventing accidental tool conflicts in multi-MCP environments
- **Cross-platform fixes**: macOS voice input and plugin consent flows receive targeted improvements for production reliability

## What happened

Anthropic has released Claude Code v2.1.195, a maintenance update focused on stability and developer experience improvements rather than new features. The release addresses a range of intermittent issues that have affected users relying on voice input, plugin management, and multi-tool integration [github.com/anthropics/claude-code].

The most impactful change involves how hook matchers identify tools and plugins. Previously, identifiers like `mcp__brave-search` could accidentally match similar hyphenated names through substring matching. The fix enforces exact matching, eliminating false positives when working with multiple MCP (Model Context Protocol) servers. Developers needing broader pattern matching can now use explicit regex patterns like `mcp__brave-search__.*`.

Voice dictation users on macOS receive particular attention in this release. The update fixes a persistent issue where background silence was captured during long-running sessions after audio input device changes, degrading transcription quality. Additionally, auto-submit functionality now works correctly for logographic languages like Japanese, Chinese, and Thai that don't use spaces as word delimiters—a critical fix for non-Latin script users.

Plugin management has been refined with several fixes: external plugins no longer prompt for installation consent on every loader invocation, and enable/disable operations now correctly handle plugins whose internal names differ from marketplace identifiers. Background jobs persist reliably across version upgrades, preventing data loss when users update to newer Claude Code releases.

A final fix addresses a crash recovery issue, though the release notes appear truncated on this point.

## What happens next

Users experiencing voice input issues, plugin loading problems, or working with multiple MCP servers should upgrade immediately. The exact-matching behavior for hooks represents a breaking change for any custom configurations relying on substring patterns and may require updates to existing MCP server configurations.
*This article does not contain affiliate links.*
