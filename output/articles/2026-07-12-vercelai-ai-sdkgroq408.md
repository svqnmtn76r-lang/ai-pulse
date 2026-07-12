---
category: sdk_release
date: '2026-07-12'
generated_at: '2026-07-12T04:31:21.306161Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:vercel/ai
source_url: https://github.com/vercel/ai/releases/tag/%40ai-sdk/groq%404.0.8
template_type: explainer
title: vercel/ai @ai-sdk/groq@4.0.8
word_count: 828
---

# Groq AI SDK Update Fixes Prompt Caching Visibility: What This Means for Your LLM Costs

Vercel's AI SDK has released a critical patch for its Groq provider integration that addresses how prompt caching metrics are reported. This fix ensures developers can now accurately see when Groq's implicit caching is reducing their token consumption—an important detail for understanding and optimizing API costs when using Groq's language models.

## TL;DR

- **Prompt caching wasn't visible**: The previous version accepted cached token data from Groq but failed to surface it in usage reports, making it impossible to track cache hits.
- **New metric transparency**: Cached input tokens are now properly reported as `cachedInputTokens` in usage data, helping developers understand their actual token consumption.
- **Cost optimization insight**: Groq charges for cache creation, but this update clarifies that cache reads have no additional charge—only the initial caching incurs costs.
- **Impact**: Developers using Groq through Vercel's AI SDK can now accurately monitor caching efficiency and understand true API expenses.

## Background

Token counting in large language model APIs has become increasingly complex as caching mechanisms enter the picture. Groq, a provider known for fast LLM inference, implements implicit prompt caching—a feature that automatically caches repeated prompt segments to reduce latency and token costs.

However, when developers use Groq through Vercel's AI SDK, they rely on the SDK to properly surface usage metrics. The problem came down to data handling: while the SDK's `convertGroqUsage` function was technically receiving cached token information from Groq's API responses, it wasn't actually reading or reporting this data to users. This created a blind spot where developers couldn't verify whether caching was working, making it difficult to understand their true API consumption patterns.

The challenge reflects a broader issue in AI infrastructure: as optimization features become standard, the tooling must transparently expose their effects. Without visibility into caching behavior, developers can't make informed decisions about prompt engineering or infrastructure choices.

## How it works

### Understanding Groq's Implicit Prompt Caching

Groq's caching system works automatically in the background. When you send a request to Groq's API, the service examines your prompt and checks if portions of it have been cached in previous requests. If cached content exists, Groq reuses it rather than reprocessing those tokens, which saves computation time and reduces token charges.

The key distinction in Groq's model is that cached tokens don't incur the same charges as fresh tokens. When content is initially cached, there's a "cache write" operation with associated costs. However, subsequent reads from cache have no additional token charge—you only pay once for initial caching, then benefit from repeated use without extra costs. This differs from some other providers' caching implementations.

### The Reporting Problem and Solution

Previously, Groq's API responses included a field called `prompt_tokens_details.cached_tokens`, indicating how many tokens were served from cache in a given request. The AI SDK was receiving this field but not processing it—essentially ignoring valuable diagnostic information.

The fix implements proper data extraction and normalization. Cached tokens are now:

1. **Extracted** from Groq's response structure (`prompt_tokens_details.cached_tokens`)
2. **Mapped** to the SDK's standard usage metric `cachedInputTokens`
3. **Aligned** with the broader AI SDK convention where `cachedInputTokens` corresponds to the `cacheRead` usage field
4. **Subtracted** from the `noCache` count to avoid double-counting tokens

This adjustment ensures that when you review usage reports, you see an accurate breakdown: X tokens from cache, Y tokens computed fresh. Previously, all tokens were incorrectly attributed to `noCache`, obscuring the true impact of Groq's caching optimization.

### Cost Implications and Transparency

The patch also clarifies Groq's cost model by noting that `cacheWrite` remains undefined in usage reports. This reflects Groq's pricing structure where cache creation is charged once, but reads incur no additional cost. Other providers might structure this differently—some charge per cache write operation, some charge for both writes and reads. By explicitly documenting that Groq has no cache-read charge, the SDK helps developers understand their actual spending.

For practical purposes, this means:
- Your first mention of a particular prompt segment costs tokens (cache write)
- Subsequent reuses of that segment cost zero additional tokens (cache read)
- Usage reports now correctly reflect this distinction

## What happens next

This patch makes monitoring and optimization easier for developers using Groq through Vercel's AI SDK. Teams can now audit their applications to identify which prompts benefit most from caching and make architectural decisions based on actual data rather than assumptions.

For those building production applications, accurate usage tracking is foundational for cost management. With this fix, you can run cache performance analyses on your applications and establish baselines for token consumption. This is particularly valuable for applications with repetitive prompts or shared system instructions—exactly the scenarios where Groq's implicit caching provides the most benefit.

The update is available in `@ai-sdk/groq@4.0.8`. If you're using Groq through Vercel's AI SDK and want to verify your caching efficiency, update to this version and review your usage metrics to see the cached versus fresh token breakdown.
*This article does not contain affiliate links.*
