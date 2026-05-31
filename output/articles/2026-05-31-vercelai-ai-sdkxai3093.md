---
category: sdk_release
date: '2026-05-31'
generated_at: '2026-05-31T05:24:49.497396Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:vercel/ai
source_url: https://github.com/vercel/ai/releases/tag/%40ai-sdk/xai%403.0.93
template_type: explainer
title: vercel/ai @ai-sdk/xai@3.0.93
word_count: 844
---

# Vercel AI SDK xAI 3.0.93: Streamlining Search Tools and Image Capabilities

Vercel has released version 3.0.93 of its xAI provider integration within the AI SDK, introducing refinements to how developers interact with xAI's Web Search capabilities. The update focuses on modernizing the API surface and expanding functionality for developers building AI-powered applications that need comprehensive web search and visual content retrieval.

## TL;DR

- **Deprecated searchParameters**: The legacy `searchParameters` option for xAI live search is being phased out in favor of dedicated web_search and x_search agent tools
- **Image search expansion**: The Web Search tool now supports `enableImageSearch` parameter, allowing developers to retrieve images alongside text results
- **Impact**: Developers using xAI providers should migrate away from older search patterns toward the agent-based tool approach while gaining new visual search capabilities

## Background

The xAI Responses API has evolved to provide more structured ways for AI agents to access external information. Previously, developers could pass `searchParameters` directly to configure live search behavior. However, as the SDK has matured, Vercel has moved toward a more consistent tool-based architecture where capabilities like web search are exposed as discrete agent tools rather than inline parameters.

This architectural shift reflects broader industry trends toward composable, modular AI interfaces. By treating web search as an explicit tool that agents can invoke—rather than an implicit capability—developers gain better control, observability, and composability. The deprecation signals a transition period where existing implementations will continue working but should migrate to the newer approach.

The image search enhancement recognizes that modern web search increasingly requires visual content. Users searching for products, places, or concepts often expect images as part of results. By enabling image retrieval through the Web Search tool, the SDK now provides more complete search results for AI applications that can leverage visual information.

## How it works

### Moving from searchParameters to Agent Tools

The deprecated `searchParameters` approach treated search as an internal implementation detail. Developers would configure search behavior through options passed to the xAI provider, but the search execution happened behind the scenes without explicit agent control.

The new pattern elevates search to first-class citizenship in the agent ecosystem. Rather than configuring search implicitly, developers now define `web_search` and `x_search` tools that agents can invoke during reasoning. This provides several advantages: agents can decide when to search based on their reasoning process, developers can track search usage more precisely, and the pattern aligns with how other tools (like function calling) work in the SDK.

For developers with existing code using `searchParameters`, migration involves moving search configuration into explicit tool definitions. Instead of passing search options to the provider initialization, you'll define search tools that the agent can call. This makes the agent's decision to search visible in logs and traces, improving debugging and optimization.

### enableImageSearch: Expanding Result Types

The Web Search tool now accepts an `enableImageSearch` parameter that maps to the xAI Responses API's `enable_image_search` field. When enabled, search results include images alongside traditional text content.

This parameter addresses a fundamental limitation of text-only search in modern applications. Users frequently need visual information—whether searching for products, locations, artwork, or design inspiration. By enabling image search at the tool level, developers can configure whether their agent should retrieve images on a per-search-tool basis.

The implementation is straightforward: when calling `xai.tools.webSearch()`, developers can pass `enableImageSearch: true` in the configuration. The SDK handles translating this to the correct API parameter format. This gives developers granular control—they could create multiple search tools with different image search settings, allowing agents to choose between image-inclusive and text-only search based on query context.

## Practical implications

For development teams currently using the xAI provider, this release requires attention to migration timelines. While `searchParameters` remains functional in this version, it won't receive future updates or bug fixes. Teams should prioritize migrating to agent-based tools before the option is removed in a future major version.

The image search capability opens new use cases. E-commerce applications can now retrieve product images alongside descriptions. Content creation tools can pull visual references. Research applications can gather illustrative materials. The enabling is optional, so developers working in text-focused domains can continue without image search overhead.

Testing should verify that agents properly invoke web search tools and that image results integrate correctly with downstream processing. Some applications may need adjustment in how they handle mixed text and image content in search results.

## What happens next

Expect the xAI provider integration to continue evolving toward fuller alignment with agent patterns. Future updates may add similar tool-based patterns for other capabilities currently expressed as parameters. Vercel typically maintains deprecation warnings for 2-3 major versions before removing deprecated functionality, giving teams reasonable migration windows.

For xAI integration specifically, monitor the official Vercel AI SDK documentation and release notes for removal timelines for `searchParameters`. The agent tools approach will likely become the standard pattern as the SDK matures, so adopting it now positions applications for long-term maintainability.

Developers should also consider whether `enableImageSearch` aligns with their application's needs—it adds latency and processing overhead, so disabling it when images aren't needed maintains optimal performance.
*This article does not contain affiliate links.*
