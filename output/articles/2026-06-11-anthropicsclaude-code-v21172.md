---
category: feature_update
date: '2026-06-11'
generated_at: '2026-06-11T20:43:25.686145Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.172
template_type: breaking
title: anthropics/claude-code v2.1.172
word_count: 332
---

# Anthropic Releases Claude-Code v2.1.172 with Nested Sub-Agent Support and Critical Bug Fixes

## TL;DR

- **Hierarchical agents now supported**: Claude-Code enables sub-agents to spawn their own subordinate agents up to five levels deep, expanding automation capabilities for complex workflows
- **Infrastructure improvements**: AWS Bedrock integration now respects standard AWS SDK configuration precedence, while critical context management bugs prevent session lockups
- **Developer experience enhancements**: UI improvements include plugin marketplace search functionality and better visibility into configuration sources

## What happened

Anthropic has released Claude-Code v2.1.172, introducing significant expansions to agent capabilities alongside critical stability improvements. The headline feature enables recursive agent spawning—sub-agents can now create their own child agents up to five levels deep—allowing developers to architect more sophisticated multi-tier automation systems.

The update addresses infrastructure integration gaps: Amazon Bedrock deployments now automatically read AWS region configurations from `~/.aws` files when environment variables aren't explicitly set, aligning with standard AWS SDK behavior. A new `/status` endpoint surfaces which configuration source provided the region, improving transparency for troubleshooting.

Several critical bugs were resolved that previously impacted production deployments. Sessions utilizing the expanded 1M context window without sufficient usage credits experienced permanent hangs; the system now automatically compacts contexts back to standard limits. A recurring error plaguing conversations with multiple images—where the system repeatedly reported image processing failures—has been eliminated. Additionally, the agents view UI no longer keeps sessions artificially marked as "Working" for up to 30 seconds post-completion, reducing false status indicators.

Security and isolation improvements prevent cross-project configuration leakage: background agents on pre-warmed workers no longer inadvertently access another project's `.mcp.json` approval settings and trust configurations.

The update also adds granular observability through a new `model` attribute in the `claude_code.lines_of_code.count` OpenTelemetry metric, enabling better performance tracking across different model variants.

## What happens next

Teams should upgrade to capture stability improvements and architectural flexibility. The nested sub-agent capability opens new possibilities for orchestrating complex automation tasks, though developers should carefully design hierarchies respecting the five-level limit to avoid excessive nesting complexity.
*This article does not contain affiliate links.*
