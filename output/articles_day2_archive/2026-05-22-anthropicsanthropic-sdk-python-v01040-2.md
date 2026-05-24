---
category: other
date: '2026-05-22'
generated_at: '2026-05-22T21:48:45.145925Z'
generated_by: claude-haiku-4-5-2026-05-22
importance_score: 50
products: []
source_name: github:anthropics/anthropic-sdk-python
source_url: https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.104.0
template_type: breaking
title: anthropics/anthropic-sdk-python v0.104.0
word_count: 392
---

# Anthropic Releases Python SDK v0.104.0 with Enhanced Streaming Token Estimation

## TL;DR

- **Token counting arrives for thinking blocks**: Anthropic's Python SDK now supports real-time estimation of tokens consumed during model reasoning phases via streaming
- **Beta feature enables cost optimization**: Developers can now track computational expenses of Claude's extended thinking in real-time, improving budget forecasting
- **Incremental rollout underway**: Feature ships as a beta capability, signaling broader platform expansion for advanced reasoning workflows

## What happened

Anthropic has rolled out version 0.104.0 of its official Python SDK, introducing support for thinking-token-count beta functionality that allows developers to monitor token consumption during streaming operations. The update, released May 21, 2026, adds granular visibility into how many tokens Claude consumes while processing requests through its thinking blocks—the model's internal reasoning phase.

Previously, developers relying on streaming responses lacked real-time feedback on tokens used during these thinking phases. This created blind spots in cost estimation and resource planning for applications using Claude's extended thinking capabilities. The new feature provides token-count deltas within streaming responses, enabling developers to calculate cumulative token usage as responses are generated rather than waiting for final metrics.

The change targets the growing ecosystem of developers building applications around Claude's reasoning capabilities. With thinking blocks representing a computationally intensive feature, precise token accounting becomes critical for production deployments where costs scale with model complexity and reasoning depth.

The implementation ships as a beta feature, suggesting Anthropic is testing the mechanism before broader integration. This cautious approach aligns with the company's typical rollout pattern for experimental capabilities, allowing for refinement based on developer feedback before general availability.

## What happens next

Developers currently using Anthropic's Python SDK should update to v0.104.0 to access this beta functionality. Integration requires minimal code changes—primarily accessing the new thinking-token-count fields in streaming response deltas. The feature enables more sophisticated token budgeting logic, particularly important for applications combining multiple Claude API calls with reasoning-heavy workloads.

Anthropic typically graduates beta features to stable status within 2-4 release cycles, suggesting this capability should reach general availability within the next 6-8 weeks. Organizations planning to expand their use of extended thinking should begin testing token estimation in development environments immediately.

The broader implication points toward Anthropic's continued investment in fine-grained observability for its API consumers, essential as Claude's capabilities expand and usage patterns become more complex across enterprise deployments.
*Disclosure: This article contains affiliate links. As an affiliate, we earn from qualifying purchases at no extra cost to you.*
