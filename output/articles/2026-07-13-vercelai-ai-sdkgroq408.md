---
category: sdk_release
date: '2026-07-13'
generated_at: '2026-07-13T04:36:16.010429Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:vercel/ai
source_url: https://github.com/vercel/ai/releases/tag/%40ai-sdk/groq%404.0.8
template_type: explainer
title: vercel/ai @ai-sdk/groq@4.0.8
word_count: 715
---

# Groq Provider Update: Fixing Prompt Cache Visibility in AI SDK

Vercel's AI SDK has released version 4.0.8 of its Groq provider package, addressing a critical bug that prevented developers from accurately tracking prompt cache performance. The fix ensures that cached token usage is properly reported, giving developers visibility into cost savings and performance improvements from Groq's implicit prompt caching feature.

## TL;DR

- **Prompt cache tracking was broken**: The Groq provider was receiving cache hit data but not surfacing it to developers, making cached tokens appear as non-cached
- **Usage metrics now accurate**: Cached input tokens are now properly mapped to the `cacheRead` field, with non-cached tokens recalculated accordingly
- **Impact**: Developers can now accurately measure the effectiveness of prompt caching and understand their actual token costs with Groq

## Background

Groq's implicit prompt caching is a performance optimization that stores frequently-used prompt sections, reducing latency and input token processing. When a prompt hits the cache, Groq charges differently than for fresh tokens—in fact, Groq doesn't charge for cache creation, only for cache reads at a reduced rate.

However, the Vercel AI SDK wasn't properly exposing this information. While the underlying `convertGroqUsage` function was receiving the `cached_tokens` data from Groq's API response, it wasn't reading or surfacing that information to end users. This meant developers had no visibility into whether their prompts were actually benefiting from caching, and they couldn't distinguish between cached and non-cached token consumption in their usage reports.

This is particularly problematic for cost optimization. If developers can't see cache hits, they can't measure the ROI of structuring their prompts for caching, and they have an incomplete picture of their actual token expenditure.

## How it works

### Understanding Groq's Caching Architecture

Groq implements implicit prompt caching transparently within its API. When you send a request with repeated prompt content, Groq automatically detects and caches portions of it. The API response includes granular usage information that distinguishes between cached tokens and freshly-processed ones through the `prompt_tokens_details.cached_tokens` field.

The challenge wasn't that Groq wasn't providing this data—it was that the SDK wasn't reading it. The `convertGroqUsage` function was receiving the cache information but had no logic to extract and map it to the standardized usage object that developers actually interact with.

### The Fix: Proper Cache Metrics Mapping

The patch implements proper extraction and mapping of cached token data. When Groq returns `prompt_tokens_details.cached_tokens`, this value is now:

1. **Extracted and mapped to `cachedInputTokens`**: This represents tokens that hit the cache
2. **Surfaced as `cacheRead`**: The standardized AI SDK field name for reporting cache hits
3. **Subtracted from `noCache`**: The total non-cached token count is recalculated to exclude cached tokens, ensuring accurate cost accounting

Previously, a request that benefited from cache hits would show all tokens as `noCache` with `cacheRead: undefined`, making the cache optimization invisible. Now, developers can see exactly how many tokens were served from cache versus freshly processed.

### What Remains Unchanged

Since Groq's pricing model doesn't charge for creating cached prompts—only for reading from cache—the `cacheWrite` field remains undefined. This accurately reflects Groq's cost structure and prevents developers from being double-counted on cache creation expenses.

## Why This Matters

This fix has practical implications across several areas:

**Cost visibility**: Developers can now calculate actual token costs by separating cached reads (lower cost) from regular processing. For applications with repetitive prompts, this can represent significant savings that were previously invisible.

**Performance measurement**: Cache effectiveness can now be quantified. Developers can measure how many tokens are hitting cache across different prompt patterns and optimize accordingly.

**Provider comparison**: When evaluating LLM providers, accurate cache metrics enable proper comparison of effective costs and performance characteristics.

**Billing accuracy**: For teams tracking costs per request or feature, having accurate cache reporting prevents overestimating actual expenditure.

## Learn more

For developers using the Vercel AI SDK with Groq, upgrading to version 4.0.8 will immediately start providing accurate cache usage metrics in production. The change is backward-compatible—existing code will continue to work, but usage reports will now show the previously-hidden cache performance data.

To see these metrics in action, check the usage object returned after making requests to Groq through the SDK. You'll find cache read data properly segmented from non-cached token counts, giving you the visibility needed to optimize prompt design and understand true per-request costs.
*This article does not contain affiliate links.*
