---
category: feature_update
date: '2026-06-18'
generated_at: '2026-06-18T06:03:14.240642Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.181
template_type: breaking
title: anthropics/claude-code v2.1.181
word_count: 314
---

## TL;DR

- **Command-line configuration**: Users can now toggle settings like thinking mode directly from prompts using `/config` syntax across all Claude Code interfaces
- **Enhanced macOS integration**: New sandbox permissions enable Apple Events for automated control, expanding automation capabilities on macOS
- **Improved reliability and UX**: Auto-retry logic now handles mid-thinking disconnections, streaming performance improved, and subagent panels refined for better usability

## What happened

Anthropic has released Claude Code v2.1.181, introducing streamlined configuration controls and enhanced reliability features that address both power-user workflows and stability concerns. [The update, posted on GitHub](https://github.com/anthropics/claude-code/releases/tag/v2.1.181), brings several notable improvements to the AI coding assistant's interface and backend behavior.

The headline feature is the new `/config` syntax, allowing users to adjust settings inline—such as disabling extended thinking with `/config thinking=false`—without navigating menus. This works consistently across interactive mode, prompt injection (`-p`), and Remote Control, reducing friction for rapid experimentation.

For macOS users, the addition of `sandbox.allowAppleEvents` represents a meaningful expansion of local automation possibilities. Previously, sandboxed commands couldn't trigger native Apple Events; now users can explicitly opt-in, enabling deeper system integration for workflows requiring UI automation or inter-app communication.

Behind the scenes, connection handling has improved significantly. The client now automatically retries when API connections drop mid-thinking rather than surfacing opaque "Connection closed" errors—a quality-of-life fix for users on unstable networks. Streaming performance has also been refined; long paragraphs now render line-by-line instead of batching at line breaks, improving perceived responsiveness.

The Bun runtime upgrade to 1.4 and refined subagent panel management (auto-hiding idle agents, scroll hints, and UI polish) round out the release. The MCP OAuth browser page now visually coheres with Claude Code's design and auto-closes on authentication success, reducing manual steps.

## What happens next

Monitor for continued focus on stability and configuration flexibility. The emphasis on auto-retry and streaming suggests Anthropic is prioritizing reliability as more users integrate Claude Code into production workflows.
*This article does not contain affiliate links.*
