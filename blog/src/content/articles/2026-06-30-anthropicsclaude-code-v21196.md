---
category: feature_update
date: '2026-06-30'
generated_at: '2026-06-30T01:49:47.445537Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.196
template_type: breaking
title: anthropics/claude-code v2.1.196
word_count: 311
---

# Anthropic Releases Claude Code v2.1.196 with Enterprise Features and Critical Fixes

## TL;DR

- **Enterprise control**: Organization admins can now set default AI models across workspaces, streamlining team configuration
- **Security hardening**: MCP server spawning restricted in untrusted repos; workspace approval status now visible
- **Stability improvements**: Fixed critical bugs affecting background jobs, rate-limiting, and transcript handling

## What happened

Anthropic has pushed Claude Code v2.1.196, introducing organizational governance features alongside several stability fixes addressing edge cases that affected user workflows. The release [available on GitHub](https://github.com/anthropics/claude-code/releases/tag/v2.1.196) reflects a maturing product balancing enterprise requirements with developer experience.

The headliner is organizational default models—administrators can now establish baseline AI models through the org console, reducing friction for teams standardized on specific Claude versions. Sessions also receive human-readable default names, improving discoverability when users manage multiple concurrent conversations.

Security enhancements tighten the threat surface. The `claude mcp list` and `get` commands no longer automatically spawn Model Context Protocol servers from self-approved repositories via committed `.claude/settings.json` files. Untrusted workspaces now display a `⏸ Pending approval` indicator, making permission status explicit.

Behind the scenes, engineers addressed three significant bugs: a transcript parsing failure that permanently deleted background job conversations and re-executed original prompts, flickering rate-limit warnings during parallel requests, and duplicate recap lines in certain job scenarios. These fixes suggest the tool handles high-concurrency scenarios with growing robustness.

The file attachment enhancement—clickable references that reveal files in native file explorers via Cmd/Ctrl-click—addresses a usability gap for developers context-switching between editor and chat.

## What happens next

This release signals Anthropic's push toward enterprise adoption, particularly through org-level model controls and improved security transparency. Development teams should review workspace approval status in their deployments. The security changes may affect CI/CD pipelines relying on implicit MCP server execution—admins should audit existing `.claude/settings.json` configurations.

For deployment timelines and migration guidance, check the official documentation or contact Anthropic support.
*This article does not contain affiliate links.*
