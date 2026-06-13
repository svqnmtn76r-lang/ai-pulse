---
category: feature_update
date: '2026-06-13'
generated_at: '2026-06-13T05:26:22.297768Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.174
template_type: breaking
title: anthropics/claude-code v2.1.174
word_count: 291
---

## TL;DR

- **UI and Model Selection**: Claude Code v2.1.174 fixes critical display issues in the model picker, ensuring users see accurate default model assignments across different plan tiers
- **Infrastructure Stability**: Resolution of Bedrock GovCloud routing errors and environment variable inheritance bugs eliminates deployment blockers for enterprise users
- **User Experience**: New scroll acceleration toggle and performance improvements enhance reliability in fullscreen mode and session management

## What happened

Anthropic released Claude Code v2.1.174, a maintenance update addressing eight distinct technical issues affecting model selection, infrastructure routing, and user experience. [Available on GitHub](https://github.com/anthropics/claude-code/releases/tag/v2.1.174), this version focuses on fixing display inconsistencies and backend configuration problems that impacted both individual developers and enterprise deployments.

The update resolves a longstanding model picker bug where the default Claude model wasn't properly displayed. Previously, users on Max/Team Premium/Enterprise plans would see Sonnet listed instead of Opus, while the actual default behavior differed. The fix ensures transparency—Opus now correctly appears on premium tiers, Sonnet on Pro/Team plans, and Opus on pay-as-you-go accounts.

A critical fix addresses Bedrock GovCloud deployments, where regions designated `us-gov-*` were incorrectly deriving inference profile prefixes as "global" instead of "us-gov," resulting in 400 errors. This issue directly impacted government and compliance-sensitive deployments.

Additional improvements include preventing environment variable inheritance issues in background sessions, which previously caused custom gateway URLs and provider configurations to leak between sessions. A new `wheelScrollAccelerationEnabled` setting lets users disable mouse-wheel acceleration in fullscreen mode, while false billing notifications for Fable 5 on enterprise accounts were eliminated.

## Learn more

- **Claude Code Repository**: Explore the [full release notes](https://github.com/anthropics/claude-code/releases/tag/v2.1.174) for implementation details
- **Anthropic Documentation**: Review model defaults and plan-specific configurations in the official documentation
- **Bedrock Integration**: Check AWS documentation for GovCloud region specifications if using government deployments
*This article does not contain affiliate links.*
