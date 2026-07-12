---
category: sdk_release
date: '2026-07-12'
generated_at: '2026-07-12T04:31:33.172228Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:vercel/ai
source_url: https://github.com/vercel/ai/releases/tag/%40ai-sdk/groq%403.0.51
template_type: explainer
title: vercel/ai @ai-sdk/groq@3.0.51
word_count: 706
---

# Groq Provider Update: Fixing Prompt Cache Usage Reporting in Vercel AI SDK

Vercel has released version 3.0.51 of its Groq provider integration for the AI SDK, addressing a critical issue where prompt caching metrics were not being properly surfaced to developers. The patch fix ensures that when Groq's implicit prompt caching system reduces token consumption, those savings are now accurately reflected in usage reports.

## TL;DR

- **Prompt cache detection was broken**: The Groq provider was receiving cache hit data but failing to process it, causing cached tokens to be invisible in usage metrics
- **Cache reads now properly surfaced**: Cached input tokens are now mapped to the `cacheRead` metric and subtracted from the `noCache` count
- **Impact**: Developers can now accurately track cost savings from prompt caching and make informed decisions about cache-eligible workloads

## Background

Prompt caching is an increasingly important optimization technique in large language model workflows. By caching frequently accessed prompt data—such as system instructions, documents, or conversation history—providers can reduce redundant token processing and lower inference costs.

Groq, known for its high-speed inference capabilities, implements an implicit prompt caching mechanism that automatically identifies and caches reusable prompt segments. When a request reuses cached content, Groq applies reduced token counts to those segments, reflected in a `cached_tokens` field within the usage response.

However, the Vercel AI SDK's Groq provider integration had a structural problem: while the code acknowledged the existence of `prompt_tokens_details.cached_tokens` in responses, it wasn't actually reading or processing this data. This meant that even when Groq's system detected cache hits and charged fewer tokens, developers had no visibility into these savings through the SDK's usage reporting interface.

This gap was particularly problematic because developers rely on usage metrics to understand their token consumption, optimize costs, and measure the effectiveness of their caching strategies. Without accurate cache reporting, they couldn't determine whether their prompt caching implementation was delivering expected cost benefits.

## How it works

### The Caching Data Flow

When you make a request to Groq through the Vercel AI SDK, Groq's API returns detailed usage information, including a breakdown of prompt token consumption. For prompts that include cached segments, the response includes a `cached_tokens` field nested within `prompt_tokens_details`. This field represents tokens that were served from cache rather than processed fresh.

The fix ensures this data travels through the entire metrics pipeline. Previously, it stopped at the parsing stage. Now, the `convertGroqUsage` function—responsible for translating Groq's native usage format into the SDK's standardized metrics—actively extracts and processes cached token counts.

### Usage Metric Mapping

The SDK maps provider-specific metrics to its own standardized interface. For Groq's cached tokens, they're now properly mapped to the `cachedInputTokens` field, which corresponds to the broader `cacheRead` metric in the SDK's usage object. This aligns Groq's reporting with how other providers expose caching data within Vercel's ecosystem.

Simultaneously, the fix applies a crucial accounting adjustment: cached input tokens are subtracted from the `noCache` count. This ensures that your total token accounting remains mathematically consistent. A token that was read from cache isn't counted in the "non-cached" bucket; it's counted only in the cache read metric.

### Cache Write Charges

Notably, this update clarifies that Groq does not currently charge for cache creation operations. Therefore, the `cacheWrite` field in usage metrics remains undefined for Groq requests. This is an important distinction from some other providers that charge for the act of writing to cache. With Groq, you only see costs associated with cache reads (served from cache) and non-cached token processing.

## What happens next

This fix primarily benefits teams using Groq through Vercel's AI SDK who rely on prompt caching to optimize their inference costs. If you're currently using the Groq provider, upgrading to 3.0.51 will provide accurate visibility into your cache performance.

The more immediate value comes when analyzing patterns: by correctly tracking `cachedInputTokens`, you can now calculate actual cost savings from caching, compare performance across different prompt caching strategies, and make data-driven decisions about which workloads benefit most from optimization.

For teams evaluating prompt caching decisions or troubleshooting why expected cost reductions aren't materializing, this update provides the diagnostic data you need. You'll be able to confirm whether Groq is actually detecting and caching your prompts, and quantify the efficiency gains.
*This article does not contain affiliate links.*
