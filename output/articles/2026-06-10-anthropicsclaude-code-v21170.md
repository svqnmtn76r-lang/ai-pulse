---
category: model_release
date: '2026-06-10'
generated_at: '2026-06-10T05:26:53.022009Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 100
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.170
template_type: breaking
title: anthropics/claude-code v2.1.170
word_count: 297
---

## TL;DR

- **Point 1**: Anthropic releases Claude Fable 5, a Mythos-class model now available to general users through Claude Code v2.1.170
- **Point 2**: Fable 5 represents the most capable model Anthropic has made publicly available, signaling a major capability leap
- **Point 3**: Critical bug fix addresses transcript persistence issues affecting VS Code and inherited shell environments

## What happened

Anthropic has unveiled Claude Fable 5, marking a significant milestone in the company's model release strategy. Available exclusively through the Claude Code v2.1.170 update, Fable 5 is classified as a Mythos-class model—Anthropic's designation for advanced AI systems—and has been optimized for general use without compromising safety standards.

The release represents a substantial capability increase relative to Anthropic's previous publicly accessible offerings. By deploying this model through Claude Code, Anthropic is prioritizing developer access to cutting-edge AI capabilities, particularly for coding and technical workflows.

Beyond the headline feature, the v2.1.170 release addresses a notable technical regression that affected user experience for developers relying on VS Code's integrated terminal. Sessions launched from inherited Claude Code environment variables were failing to persist transcript data, preventing users from resuming prior conversations using the `--resume` flag. This patch restores expected functionality across various shell environments.

## Impact and timeline

The dual-pronged update signals Anthropic's commitment to both advancing model capabilities and maintaining product stability. Developers using Claude Code for development tasks now have access to significantly enhanced AI assistance, while the bug fix removes friction from existing workflows that depend on session continuity.

The v2.1.170 release is immediately available for download and implementation.

## Learn more

- **Claude Fable 5 announcement**: Visit Anthropic's official news post for detailed capability benchmarks and safety measures
- **Claude Code repository**: The GitHub release page contains full changelog details and installation instructions for v2.1.170
*This article does not contain affiliate links.*
