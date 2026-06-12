---
category: feature_update
date: '2026-06-12'
generated_at: '2026-06-12T05:56:26.282749Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.175
template_type: breaking
title: anthropics/claude-code v2.1.175
word_count: 314
---

## TL;DR

- **Enterprise control strengthened**: Anthropic's Claude Code now allows administrators to enforce model availability constraints globally, preventing users from circumventing organizational policies
- **Policy enforcement tightened**: The new `enforceAvailableModels` setting prevents default model selections from bypassing allowlists and blocks user-level overrides
- **Security implications**: Organizations gain stricter governance over AI model usage, addressing concerns about compliance and cost control in distributed teams

## What happened

Anthropic has released Claude Code v2.1.175 with a significant administrative control enhancement. The update introduces the `enforceAvailableModels` managed setting, which fundamentally strengthens how organizations can govern model access across their deployments.

Previously, teams using Claude Code could specify an `availableModels` allowlist, but users could potentially circumvent these restrictions through default model selections or local configuration overrides. The new version closes these gaps by enforcing the allowlist more rigorously.

When `enforceAvailableModels` is enabled, any default model configuration that would resolve to a disallowed option automatically cascades to the first permitted model in the allowlist. Critically, individual users and project-level settings can no longer expand the managed allowlist, preventing end-runs around administrator policies.

This reflects enterprise demand for tighter AI governance. As organizations integrate Claude into production workflows, security and compliance teams increasingly need assurance that only approved models are being used—whether for cost management, data residency requirements, or regulatory adherence.

The change is particularly relevant for organizations running multiple teams or departments with varying entitlements. Administrators can now confidently restrict access to experimental or resource-intensive models while knowing users cannot override these boundaries through configuration tricks.

## What happens next

Organizations using Claude Code's team or enterprise features should review their existing `availableModels` configurations. The update is backward compatible—existing allowlists remain functional—but teams relying on flexible model selection may need to adjust policies.

For enterprises managing compliance-sensitive workloads, this release enables more defensible access control auditing. Teams should consider enabling `enforceAvailableModels` as part of broader AI governance frameworks.
*This article does not contain affiliate links.*
