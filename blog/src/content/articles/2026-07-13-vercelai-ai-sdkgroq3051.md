---
category: sdk_release
date: '2026-07-13'
generated_at: '2026-07-13T04:36:28.749957Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:vercel/ai
source_url: https://github.com/vercel/ai/releases/tag/%40ai-sdk/groq%403.0.51
template_type: explainer
title: vercel/ai @ai-sdk/groq@3.0.51
word_count: 798
---

# Groq Prompt Caching Fix: Better Cost Visibility for AI Applications

Vercel's AI SDK has released a patch update for its Groq integration that addresses a critical gap in how cached token usage gets reported. The fix ensures that when Groq's prompt caching feature reduces input processing costs, developers can now see exactly how many tokens were served from cache versus freshly processed—visibility that was previously missing.

## TL;DR

- **Prompt caching oversight**: Groq's implicit prompt caching was working, but the SDK wasn't surfacing cache hit metrics to developers
- **The fix**: Cached token counts now properly appear in usage reports as `cachedInputTokens`, mapped to the standard `cacheRead` field
- **Cost tracking**: This enables accurate accounting of how caching reduces token consumption and inference costs
- **Impact**: Developers can now verify that their prompt caching strategies are actually delivering savings, improving cost optimization visibility

## Background

Prompt caching is an optimization technique where repeated or reusable portions of prompts are stored and reused across requests. Instead of reprocessing identical text sequences, the model can reference cached versions, significantly reducing token consumption and inference latency. Groq, known for its high-speed inference capabilities, built implicit prompt caching into its API—meaning the feature works automatically without explicit developer configuration.

However, when Vercel's AI SDK integrated with Groq, the usage reporting layer wasn't fully exposing cache performance metrics. While Groq's API was returning cached token counts in its response, the SDK's conversion function wasn't reading or surfacing that data. This created a blind spot: developers had no way to verify whether caching was working or how much it was reducing their token consumption.

The problem became apparent when usage reports would show `cacheRead: undefined` and count the entire prompt as non-cached (`noCache`), even when Groq's backend confirmed that portions had been served from cache. For cost-conscious applications processing repetitive prompts at scale, this lack of visibility meant they couldn't accurately track savings or validate their caching assumptions.

## How it works

### Understanding the cache metrics gap

Groq's API response includes a `prompt_tokens_details` object containing a `cached_tokens` field that indicates how many input tokens were successfully retrieved from cache. The SDK's `convertGroqUsage` function had access to this data but wasn't extracting or mapping it to the SDK's standardized usage object.

The standardized AI SDK usage model includes fields like `cacheRead` (tokens from cache), `cacheWrite` (tokens written to cache), and `noCache` (newly processed tokens). These fields provide a unified interface across different model providers, making it easier for developers to compare costs and performance regardless of which AI service they're using.

### The fix in action

The patch modifies how `convertGroqUsage` processes Groq's response data. Now, when `prompt_tokens_details.cached_tokens` is present, it gets mapped to the `cachedInputTokens` field, which aligns with the SDK's `cacheRead` metric. Simultaneously, this cached token count is subtracted from the `noCache` total, ensuring that the math is accurate and avoiding double-counting.

For example, if a request processes 100 prompt tokens and 30 come from cache, the corrected report now shows:
- `cacheRead`: 30 tokens
- `noCache`: 70 tokens  
- `cacheWrite`: undefined (Groq doesn't charge separately for writing to cache)

Previously, the same request would have inaccurately reported all 100 tokens as non-cached.

### Why `cacheWrite` remains undefined

Groq's pricing model doesn't apply a separate charge for writing tokens to cache—cache storage and creation are folded into standard inference costs. Therefore, the `cacheWrite` field appropriately remains `undefined`, distinguishing Groq's approach from providers like Claude that charge differently for cache creation versus cache reads.

## Practical implications

This fix matters most for applications relying on Groq for cost optimization through prompt caching. Teams using repetitive system prompts, reusable document chunks, or multi-turn conversations with fixed context can now:

- **Verify cache effectiveness**: See concrete numbers proving that caching is reducing token consumption
- **Calculate actual savings**: Compare cached vs. non-cached token counts to quantify cost reductions
- **Optimize strategy**: Make data-driven decisions about which prompts or documents are worth caching based on hit rates
- **Monitor performance**: Track cache behavior over time to identify degradation or unexpected patterns

For infrastructure teams building multi-tenant or high-volume AI applications, this transparency becomes critical. Instead of assuming caching works, they can now monitor it in production and adjust their caching strategies based on real usage data.

## What happens next

This patch represents a foundational improvement in observability rather than a breaking architectural change. Existing applications will automatically benefit from more accurate usage reporting when updating to version 3.0.51, though they won't need code changes unless they want to act on the improved metrics.

The fix also sets a pattern for how the AI SDK should handle provider-specific caching features going forward. As more providers implement prompt caching with varying cost structures, consistent metric surfacing becomes increasingly important for developers managing costs across multiple services.
*This article does not contain affiliate links.*
