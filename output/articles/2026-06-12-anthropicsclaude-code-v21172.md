---
category: feature_update
date: '2026-06-12'
generated_at: '2026-06-12T05:56:38.320382Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.172
template_type: breaking
title: anthropics/claude-code v2.1.172
word_count: 325
---

# Claude Code v2.1.172: Recursive Agent Architecture and Critical Bug Fixes

## TL;DR

- **Hierarchical agents now enabled**: Sub-agents can spawn their own sub-agents up to 5 levels deep, expanding autonomous task delegation capabilities
- **AWS configuration handling improved**: Bedrock now respects AWS SDK precedence rules for region detection, reducing configuration friction
- **Multiple stability fixes**: Critical bug patches addressing context limits, image processing errors, and project isolation prevent session degradation and data leakage

## What happened

Anthropic released Claude Code v2.1.172, a maintenance and capability update to its code execution platform [via GitHub](https://github.com/anthropics/claude-code/releases/tag/v2.1.172). The release introduces nested agent spawning—allowing autonomous agents to delegate work to child agents recursively—while addressing several production stability issues.

The recursive agent feature represents a significant architectural shift, enabling multi-level task decomposition where agents can partition complex workflows across five hierarchical levels. This capability enhances parallel processing and specialized task handling for enterprise workflows.

AWS Bedrock integration improvements align configuration handling with standard AWS SDK behavior, automatically reading region preferences from `~/.aws` config files when environment variables aren't explicitly set. A new `/status` endpoint surfaces configuration provenance for debugging.

The release addresses critical regressions: sessions consuming the full 1M context window previously got stuck without usage credits; they now auto-compact to standard limits. Image processing errors that repeated indefinitely across multi-image conversations have been resolved. The agents view no longer hangs with spinner states lasting 30+ seconds post-execution.

Security-focused fixes include preventing background agents from reading another directory's project approval settings and trust configurations from pre-warmed workers—a potential data isolation vulnerability.

The marketplace plugin search bar improves UX for discovering extensions, while new OTEL metrics (including a `model` attribute in lines-of-code counting) enable better observability into platform usage.

## What happens next

Organizations leveraging Claude Code for complex automation workflows should review the nested agent capabilities for potential workflow optimization. The stability fixes suggest immediate upgrade recommendations for production deployments, particularly those using high context windows or processing multi-image inputs.
*This article does not contain affiliate links.*
