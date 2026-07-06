---
category: sdk_release
date: '2026-07-06'
generated_at: '2026-07-06T05:20:05.804433Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:vercel/ai
source_url: https://github.com/vercel/ai/releases/tag/%40ai-sdk/anthropic%403.0.93
template_type: explainer
title: vercel/ai @ai-sdk/anthropic@3.0.93
word_count: 816
---

# Anthropic SDK Patch Fixes Silent Thinking Model Bug: What Developers Need to Know

Vercel's AI SDK has released a patch for its Anthropic integration that addresses a critical issue where explicit requests to disable the extended thinking feature were being ignored. The bug affected developers using newer Claude models that have thinking capabilities enabled by default, potentially wasting token budgets on unwanted cognitive processing.

## TL;DR

- **Extended thinking controls**: Anthropic's Claude models (particularly Sonnet 5) can perform extended reasoning, but this feature consumes tokens and may not always be needed
- **Configuration mismatch**: The SDK previously accepted disable requests in code but failed to send them to Anthropic's API, leaving thinking enabled anyway
- **Token waste problem**: When thinking remained enabled despite developer intent, it could consume significant portions of the maximum token budget
- **Impact**: Developers relying on the SDK to respect their thinking configuration settings will now see those preferences correctly enforced

## Background

Anthropic's Claude models, especially newer versions like Sonnet 5, introduced extended thinking capabilities—a feature that allows models to reason through problems more thoroughly before responding. While powerful, this thinking process consumes tokens from the user's allocated budget.

The AI SDK from Vercel provides a standardized interface for developers to work with multiple AI providers, including Anthropic. As part of this abstraction layer, it accepts configuration options through the `providerOptions` parameter, allowing fine-grained control over provider-specific features.

The problem emerged as developers attempted to disable thinking for specific use cases where it wasn't beneficial—perhaps for straightforward queries that don't need extended reasoning, or in cost-sensitive scenarios where every token matters. They could set `providerOptions.anthropic.thinking = { type: 'disabled' }` in their code, and the schema validation would accept it. However, the request never actually reached Anthropic's API.

## How it works

### The Silent Discard Issue

The bug represented a classic integration problem: configuration validation at one layer (the SDK) didn't match actual implementation at another layer (the API request). When developers specified that thinking should be disabled, the SDK validated the parameter syntax and accepted it as valid input. However, during request construction, the code path that built the actual HTTP request to Anthropic's Messages API would strip out or ignore the `disabled` value entirely.

This created a false sense of control for developers. Their code appeared correct, their configuration was schema-valid, but the runtime behavior differed from their expectations. The thinking feature remained active, consuming tokens according to Anthropic's defaults for that model.

### Why This Matters for Token Economics

Claude models with thinking enabled can use substantial portions of a request's token budget. When a model defaults to thinking-enabled and a developer specifically wants to disable it, they typically have a reason: reducing latency, minimizing cost, or ensuring deterministic behavior for specific tasks.

Consider a scenario where `max_tokens` is set to 1,000. With thinking enabled by default and running unchecked, the model might use 300-500 tokens just for its internal reasoning process, leaving only 500-700 tokens for the actual response. If the developer disabled thinking to reclaim that budget, they'd expect the full 1,000 tokens available for the response instead. But with the bug, thinking continued consuming tokens anyway, making the `disabled` configuration utterly useless.

### The Fix

The patch modifies the request-building logic to actually forward the `thinking: { type: 'disabled' }` parameter to Anthropic's API, rather than stripping it out. Now when developers explicitly configure thinking as disabled, that instruction travels through the entire request chain and lands in the actual API call.

This aligns the SDK's behavior with developer intent and with what Anthropic's API actually supports. Anthropic's Messages API has always accepted thinking configuration parameters; the gap was purely in Vercel's integration layer.

## What This Means in Practice

For developers currently using the Anthropic SDK to interact with Claude models, this patch restores configuration reliability. If you've set thinking to disabled in your code, that preference now actually takes effect. You'll see the expected token allocation and latency improvements.

The fix is particularly valuable for production systems where token budgets are carefully managed and response latency is critical. Teams using Claude Sonnet 5 or other thinking-capable models can now confidently disable the feature when their use case doesn't require extended reasoning.

For anyone who specifically *wants* thinking enabled, the behavior remains unchanged—you can still request it explicitly or rely on model defaults. This patch only affects the disable case that was previously broken.

## What Happens Next

This patch is version 3.0.93 of the @ai-sdk/anthropic package, indicating it's a maintenance release in the broader AI SDK ecosystem. Developers should update their dependencies to receive the fix and immediately gain correct thinking configuration behavior.

For teams actively working with extended thinking features, reviewing your current configuration is worthwhile. You may discover that thinking is running in places where you disabled it, and you might reclaim meaningful token budget by applying this update.
*This article does not contain affiliate links.*
