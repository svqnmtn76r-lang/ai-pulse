---
category: feature_update
date: '2026-06-13'
generated_at: '2026-06-13T05:26:16.760332Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.175
template_type: breaking
title: anthropics/claude-code v2.1.175
word_count: 296
---

## TL;DR

- **Point 1**: Anthropic released claude-code v2.1.175 with new enterprise-grade access controls for model availability
- **Point 2**: Organizations can now enforce stricter model constraints that override individual user or project-level settings
- **Point 3**: The `enforceAvailableModels` setting represents a shift toward stricter administrative governance in AI development environments

## What happened

Anthropic has rolled out a significant update to its Claude Code platform, introducing granular administrative controls designed for enterprise deployments. The release, published on GitHub, introduces the `enforceAvailableModels` managed setting—a feature that fundamentally changes how organizations can control which AI models their teams access.

Previously, model availability lists could be circumvented by user or project-level configurations. The new enforcement mechanism prevents this workaround by locking down the allowlist at the organizational level. When activated, any default model selection that would violate the constraints automatically falls back to the first permitted model in the allowlist, ensuring compliance across teams.

This change addresses a critical gap in multi-tenant and regulated environments where IT administrators need absolute certainty that certain models—whether for cost control, compliance, or performance reasons—remain unavailable to end users regardless of individual preference settings.

The update signals Anthropic's growing focus on enterprise adoption, where governance and security controls are prerequisites for organizational deployment. By preventing setting escalation, the company is positioning Claude Code as suitable for sectors with stringent operational requirements, including finance, healthcare, and government institutions.

## What happens next

Organizations using Claude Code in enterprise contexts should evaluate whether to enable `enforceAvailableModels` as part of their access control policies. The feature is available immediately in v2.1.175 and can be implemented through managed settings configurations. Teams relying on model flexibility may need to adjust workflows if their organization enables this enforcement.

Learn more by visiting the [official release page](https://github.com/anthropics/claude-code/releases/tag/v2.1.175) on GitHub.
*This article does not contain affiliate links.*
