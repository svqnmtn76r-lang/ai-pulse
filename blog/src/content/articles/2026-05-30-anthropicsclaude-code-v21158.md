---
category: feature_update
date: '2026-05-30'
generated_at: '2026-05-30T04:57:48.513965Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.158
template_type: breaking
title: anthropics/claude-code v2.1.158
word_count: 284
---

## TL;DR

- **Expanded availability**: Claude Code's autonomous mode now runs across Anthropic's major cloud partnerships—Bedrock, Vertex, and Foundry—supporting Opus 4.7 and 4.8 models
- **Developer control**: Teams can activate the feature immediately via a single environment variable, lowering friction for adoption
- **Automation scaling**: The move enables broader enterprise access to agentic code generation without requiring model switching or platform migration

## What happened

Anthropic has significantly expanded the reach of Claude Code's autonomous capabilities with version 2.1.158, making auto mode available across three major cloud infrastructure partners simultaneously. The update, released on GitHub, enables developers using Amazon Bedrock, Google Vertex AI, and Anthropic's Foundry platform to activate hands-off code generation for both Opus 4.7 and 4.8 models.

Previously, auto mode—which allows Claude to execute, test, and iterate on code without human intervention between steps—had limited availability. This rollout represents a critical expansion for enterprises standardized on different cloud ecosystems, removing a key barrier to adoption. Users can enable the feature by setting a single environment variable: `CLAUDE_CODE_ENABLE_AUTO_MODE=1`.

The timing suggests Anthropic is betting on autonomous coding becoming a standard enterprise capability. By supporting both older (4.7) and newer (4.8) model versions across competing cloud providers, the company is signaling platform-agnostic ambitions while maintaining backward compatibility—a strategic move for organizations with heterogeneous infrastructure.

## What happens next

Early adopters should test the feature in staging environments to assess code quality and safety guardrails specific to their workflows. Teams standardized on Bedrock, Vertex, or Foundry can now consolidate tooling rather than fragment across multiple code generation platforms.

**Learn more:**
- View the [full release on GitHub](https://github.com/anthropic/claude-code/releases/tag/v2.1.158)
- Review Anthropic's documentation on autonomous mode configuration
- Monitor upcoming releases for performance metrics and safety updates
*This article does not contain affiliate links.*
