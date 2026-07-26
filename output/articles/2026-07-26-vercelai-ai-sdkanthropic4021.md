---
category: sdk_release
date: '2026-07-26'
generated_at: '2026-07-26T04:34:03.595139Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:vercel/ai
source_url: https://github.com/vercel/ai/releases/tag/%40ai-sdk/anthropic%404.0.21
template_type: explainer
title: vercel/ai @ai-sdk/anthropic@4.0.21
word_count: 766
---

# Anthropic SDK Update Fixes Token Counting for AI Reasoning: What Developers Need to Know

Vercel's AI SDK has released a patch update to its Anthropic integration that addresses how the library reports token usage for Claude's advanced reasoning capabilities. The fix ensures that tokens consumed by Claude's internal thinking process are properly categorized in usage metrics, bringing alignment between how the SDK reports these metrics and how Anthropic's API actually charges for them.

## TL;DR

- **Reasoning tokens**: Claude's thinking process consumes distinct tokens that were previously miscategorized in usage reports
- **Token accounting**: The patch corrects how `@ai-sdk/anthropic` reports these tokens, now properly labeling them as reasoning token usage
- **Impact**: Developers using Claude's extended thinking features now get accurate cost tracking and API usage visibility

## Background

Claude, Anthropic's flagship language model, introduced an extended thinking capability that allows the model to reason through complex problems before generating responses. This thinking process consumes additional tokens beyond the standard input and output tokens that developers traditionally track.

The challenge for SDK maintainers like Vercel's team is ensuring that token usage reporting matches the underlying API's behavior. When Anthropic's API processes requests with extended thinking enabled, it tracks three categories of tokens: input tokens, reasoning tokens (consumed during the thinking phase), and output tokens. Each has distinct pricing implications.

The Vercel AI SDK provides a JavaScript/TypeScript interface for working with various AI providers, including Anthropic. When developers use the SDK to integrate Claude models into their applications, they rely on accurate token counting to monitor costs, set rate limits, and optimize their implementations. If the SDK's token reporting doesn't align with what the API actually processes, developers face a mismatch between expected and actual API costs.

## How it works

### Understanding Token Categories in Claude's Reasoning

Claude's extended thinking feature operates differently from standard inference. When you enable thinking mode on compatible Claude models, the API doesn't just generate a response—it first allocates computational resources to internal reasoning. The tokens consumed during this reasoning phase are distinct from the tokens in the final response.

From Anthropic's perspective, these reasoning tokens are a separate billable category. The API returns usage information that breaks down exactly how many tokens were used for thinking, how many for the input prompt, and how many for the output. This granular tracking lets users understand what's driving their API costs.

### The Bug and Its Impact

Prior to this patch, the `@ai-sdk/anthropic` library wasn't properly mapping these reasoning tokens when it received them from Anthropic's API. Instead of categorizing them as "reasoning tokens" in the usage object returned to developers, the SDK was likely grouping them with another token category or handling them inconsistently.

This created a reporting gap. A developer might enable extended thinking on a Claude model, send a complex reasoning task through the SDK, and receive inaccurate usage data. The actual API charges would reflect the full reasoning token consumption, but the SDK's reported metrics wouldn't. Over time, this discrepancy compounds—developers underestimate their costs, or struggle to attribute API expenses to specific features.

### The Fix

The patch modifies how `@ai-sdk/anthropic` processes the API response. When Anthropic's API returns usage information that includes a reasoning token count, the SDK now correctly exposes this in its usage reporting. Developers who call the SDK will see a distinct "reasoningTokens" field (or equivalent) in the usage metrics returned alongside their AI inference results.

This aligns the SDK's abstraction with the underlying API reality. The fix is minimal but important—it's a matter of correctly parsing and re-exposing data that Anthropic's API already provides, ensuring transparency flows from the provider through the SDK to the application developer.

## What this means for you

If you're building applications with Claude using Vercel's AI SDK, this patch improves your observability. You can now accurately track reasoning token consumption in your monitoring dashboards, cost analysis tools, and billing systems. This is especially relevant if you're using Claude's extended thinking for complex tasks like multi-step reasoning, code analysis, or research synthesis—scenarios where reasoning tokens often represent a significant portion of total API costs.

For teams operating at scale, accurate token accounting is critical for unit economics. This fix eliminates a blind spot that could lead to budget surprises or incorrect cost attribution across different features in your product.

## Learn more

Review the commit details in the Vercel AI SDK repository to understand the exact changes. If you're using `@ai-sdk/anthropic` version 4.0.21 or later, you'll automatically receive the corrected token reporting. For applications running on earlier versions, upgrading is recommended if you're using Anthropic's reasoning capabilities.
*This article does not contain affiliate links.*
