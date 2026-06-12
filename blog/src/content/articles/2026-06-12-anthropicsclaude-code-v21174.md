---
category: feature_update
date: '2026-06-12'
generated_at: '2026-06-12T05:56:31.687935Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.174
template_type: breaking
title: anthropics/claude-code v2.1.174
word_count: 302
---

## TL;DR

- **UX Refinements**: Claude Code v2.1.174 addresses multiple interface and configuration issues affecting model selection and scrolling behavior
- **Enterprise Compatibility**: Critical fixes resolve AWS Bedrock GovCloud routing errors and enterprise billing banner mismatches
- **Session Isolation**: Resolved security-relevant issue where background sessions incorrectly inherited provider environment variables from parent shells

## What happened

Anthropic released Claude Code v2.1.174, a maintenance update focused on bug fixes and user experience improvements across the development tool. The release [published on GitHub](https://github.com/anthropics/claude-code/releases/tag/v2.1.174) contains seven distinct fixes addressing model selection visibility, environment variable inheritance, and AWS infrastructure compatibility.

The update resolves a longstanding model picker usability problem where the default model family wasn't displayed distinctly across different plan tiers. Users on Max/Team Premium and Enterprise plans will now see Claude Opus as its own row, Pro/Team users will see Sonnet, and API account holders will see Opus—clarifying which model actually executes when selecting "Default."

A particularly significant fix addresses AWS Bedrock GovCloud deployment issues, where derived model IDs incorrectly used the `global` prefix instead of `us-gov`, causing 400 errors in government cloud regions. This impacts enterprise customers operating in restricted AWS environments.

The release also tackles session isolation concerns, fixing a bug where background daemon sessions inherited another session's custom Anthropic provider environment variables—including gateway URLs and custom headers. This could affect deployments with multiple parallel sessions or complex provider configurations.

Additional improvements include correcting hardcoded Sonnet version labels when environment variables override defaults, removing misleading billing banners for enterprise accounts, disabling mouse-wheel scroll acceleration in fullscreen mode, and eliminating a 1-2 second pause on exit.

## What happens next

Users should upgrade to v2.1.174 to benefit from these stability improvements, particularly those operating in AWS GovCloud environments or managing complex multi-session configurations. Anthropic continues iterating on Claude Code's reliability and enterprise feature support.
*This article does not contain affiliate links.*
