---
category: feature_update
date: '2026-06-27'
generated_at: '2026-06-27T01:47:28.099045Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.195
template_type: breaking
title: anthropics/claude-code v2.1.195
word_count: 309
---

## TL;DR

- **Bug fixes dominate**: Claude Code v2.1.195 addresses seven critical issues affecting core functionality, from voice dictation to plugin management
- **Developer experience improvements**: Hook matchers now use exact-matching instead of substring-matching, preventing unintended tool conflicts
- **macOS and multilingual support enhanced**: Voice dictation stability improved across different input devices and non-space-delimited languages

## What happened

Anthropic released Claude Code v2.1.195, a maintenance update focusing on stability and developer usability. The release, published on GitHub at anthropics/claude-code, targets recurring pain points identified in production environments.

The update introduces a new environment variable, `CLAUDE_CODE_DISABLE_MOUSE_CLICKS`, allowing users to disable mouse interactions in fullscreen mode while preserving scroll functionality—useful for accessibility and workflow automation scenarios.

A significant fix addresses hook matcher behavior: hyphenated identifiers in MCP (Model Context Protocol) servers were accidentally triggering substring matches, causing unintended tool invocations. The update enforces exact-matching by default, with wildcard patterns (`.*`) available for intentional broad matching. This change prevents conflicts when multiple tools share naming conventions.

Voice dictation receives multiple improvements. macOS users facing silence capture after input device changes will see stabilized behavior, while support for space-less languages (Japanese, Chinese, Thai) now correctly triggers auto-submit functionality.

Plugin management also receives attention. External plugins loaded via project `.claude/settings.json` no longer prompt for install consent on every session, reducing friction. Additionally, the `/plugin` command now correctly handles mismatches between plugin JSON names and marketplace entries.

Finally, the release addresses data integrity issues where background jobs could disappear when written by newer Claude Code versions, protecting user workflows from unexpected data loss.

## What happens next

Developers should review the environment variable options if managing fullscreen interactions. Teams using MCP servers with hyphenated names should audit their hook configurations to verify exact-match behavior aligns with their needs. The changes suggest Anthropic is prioritizing production stability and cross-platform compatibility as Claude Code sees broader adoption.
*This article does not contain affiliate links.*
