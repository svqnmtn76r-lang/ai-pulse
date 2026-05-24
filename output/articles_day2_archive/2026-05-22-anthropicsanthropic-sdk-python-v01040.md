---
category: other
date: '2026-05-22'
generated_at: '2026-05-22T21:46:10.847305Z'
generated_by: claude-haiku-4-5-2026-05-22
importance_score: 50
products: []
source_name: github:anthropics/anthropic-sdk-python
source_url: https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.104.0
template_type: breaking
title: anthropics/anthropic-sdk-python v0.104.0
word_count: 378
---

## TL;DR

- **Streaming Intelligence**: Anthropic's Python SDK now tracks token consumption within AI thinking blocks during stream operations, enabling real-time cost monitoring
- **Developer Control**: The thinking-token-count beta feature provides granular visibility into how many tokens models consume during internal reasoning phases
- **Production Ready**: The update arrives as part of v0.104.0, allowing developers to implement smarter resource management in applications leveraging extended thinking

## What happened

Anthropic released version 0.104.0 of its Python SDK on May 21, 2026, introducing native support for tracking thinking token counts during streaming operations. The update specifically targets the beta thinking-token-count feature, which measures token consumption within thinking block deltas—the intermediate outputs generated when AI models engage in extended reasoning processes.

Previously, developers using Anthropic's Claude models had limited visibility into token usage during the thinking phase when streaming responses. This new capability solves a critical gap for production deployments: it allows teams to monitor and estimate computational costs in real-time as models work through complex reasoning tasks, rather than discovering token consumption retrospectively.

The implementation integrates directly into Anthropic's streaming architecture, meaning developers can now access thinking token metrics through standard SDK methods without architectural changes. This is particularly valuable for applications where extended thinking drives significant token consumption—scenarios like complex problem-solving, multi-step analysis, or detailed content generation where Claude's reasoning capabilities provide measurable value.

The feature arrives as a beta offering, indicating Anthropic is still refining the API surface while allowing early adopters to build integration patterns. This staged rollout approach lets production teams experiment with token tracking before the feature stabilizes into a general release.

For organizations running Claude-powered applications at scale, this update directly impacts budget forecasting and workload optimization. Teams can now implement intelligent rate-limiting, request routing, or user feedback based on actual thinking-phase token consumption rather than estimates.

## What happens next

Developers should update to v0.104.0 to access this functionality. The Python SDK maintainers expect feedback from the beta period to inform the final feature design. Watch for this capability to graduate from beta status in subsequent releases, potentially accompanied by additional refinements based on real-world usage patterns.

Teams currently managing high-volume Claude deployments should prioritize evaluation of the thinking-token-count metrics to establish baseline consumption patterns and refine cost models for extended thinking workloads.
*Disclosure: This article contains affiliate links. As an affiliate, we earn from qualifying purchases at no extra cost to you.*
