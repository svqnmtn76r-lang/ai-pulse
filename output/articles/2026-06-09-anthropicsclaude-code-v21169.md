---
category: feature_update
date: '2026-06-09'
generated_at: '2026-06-09T05:13:40.679445Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.169
template_type: breaking
title: anthropics/claude-code v2.1.169
word_count: 327
---

## TL;DR

- **Safe Mode Added**: Claude Code v2.1.169 introduces troubleshooting capabilities that disable all customizations with a single flag, addressing deployment and debugging scenarios
- **Directory Navigation**: New `/cd` command enables mid-session working directory changes while preserving prompt cache, improving workflow flexibility
- **Enterprise Security Fixed**: MCP server policies now consistently enforced across all configuration types and initialization phases, resolving critical compliance gaps

## What happened

Anthropic has released Claude Code v2.1.169, marking a significant maintenance and feature release focused on developer experience and enterprise compliance. The update, published on GitHub, introduces several quality-of-life improvements alongside critical security and performance fixes that enterprise deployments have been awaiting.

The headline feature is a new `--safe-mode` flag that strips away all user customizations—including CLAUDE.md configurations, plugins, skills, hooks, and MCP servers—for troubleshooting purposes. This addresses a long-standing pain point where debugging complex setups required manual intervention. The mode can also be triggered via the `CLAUDE_CODE_SAFE_MODE` environment variable.

A new `/cd` command allows developers to change working directories mid-session without severing the prompt cache, preserving conversation context and reducing latency overhead during extended development sessions. This solves a workflow friction point for projects requiring context switches across multiple directory structures.

On the enterprise front, Anthropic fixed a significant vulnerability where managed MCP (Model Context Protocol) policies weren't consistently enforced across reconnections, IDE-typed configurations, and initial session installations. This inconsistency posed compliance risks for organizations requiring strict server access controls. The fix also addresses performance degradation—cold starts for organizations without remote settings have been accelerated.

Additional improvements include a `disableBundledSkills` setting to prevent the model from accessing built-in workflows, UI fixes resolving arrow-key navigation issues in wrapped command lines, and resolution of a UI stall affecting user experience.

## What happens next

Developers should evaluate whether safe mode simplifies their debugging workflows, while enterprise teams should verify that MCP policies now enforce correctly across their deployment topology. The improvements suggest Anthropic is prioritizing operational stability ahead of further capability expansion.
*This article does not contain affiliate links.*
