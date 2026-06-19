---
category: feature_update
date: '2026-06-19'
generated_at: '2026-06-19T06:26:49.997461Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.181
template_type: breaking
title: anthropics/claude-code v2.1.181
word_count: 338
---

# Claude Code v2.1.181 Brings Prompt-Based Config and Enhanced Streaming

## TL;DR

- **Flexible configuration**: New `/config` syntax lets developers toggle settings like thinking mode directly from prompts, streamlining workflows across all interaction modes
- **Better UX at scale**: Improved streaming, auto-retry logic, and refined subagent panel management signal Anthropic's focus on production reliability
- **Platform expansion**: macOS Apple Events sandbox access and notification suppression features indicate deepening integration with native system capabilities

## What happened

Anthropic released v2.1.181 of Claude Code, introducing developer-friendly configuration shortcuts and addressing longstanding user experience pain points. The release, published on GitHub, represents an incremental but meaningful update to the company's code-focused AI interface.

The headline feature—dynamic `/config` syntax—allows developers to modify any setting via natural language prompt without menu navigation. Users can now type `/config thinking=false` directly in interactive sessions, prompt mode, or Remote Control to instantly adjust Claude's reasoning behavior. This single-command approach works across all interaction methods, reducing friction for power users managing complex workflows.

Under the hood, Anthropic upgraded the bundled Bun JavaScript runtime to version 1.4, improving performance for code execution environments. The streaming engine now displays long paragraphs line-by-line rather than buffering until the first line break, creating the perception of faster responses and smoother reading experiences.

Reliability improvements include automatic retry logic for API connection interruptions that previously surfaced as "Connection closed while thinking" errors. The subagent panel received notable refinement: idle agents now auto-hide after 30 seconds, with list capping at five scrollable rows and keyboard hints in the footer.

New macOS support via `sandbox.allowAppleEvents` opt-in setting enables sandboxed commands to send Apple Events, expanding integration possibilities on Apple platforms. A `CLAUDE_CLIENT_PRESENCE_FILE` environment variable lets users suppress mobile notifications when actively working at their machine.

The MCP OAuth browser interface was restyled to match Claude Code's visual identity and now auto-closes on successful authentication.

## What happens next

Developers should explore the `/config` syntax for streamlined workflow optimization. The subagent improvements suggest Anthropic is preparing for more complex multi-agent coordination scenarios in future releases.
*This article does not contain affiliate links.*
