---
category: sdk_release
date: '2026-05-31'
generated_at: '2026-05-31T05:25:02.647250Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:vercel/ai
source_url: https://github.com/vercel/ai/releases/tag/%40ai-sdk/xai%404.0.0-canary.69
template_type: explainer
title: vercel/ai @ai-sdk/xai@4.0.0-canary.69
word_count: 763
---

# Vercel AI SDK Updates xAI Integration with Improved Search Tools: What You Need to Know

Vercel has released a new canary version of its xAI provider package for the AI SDK, bringing refinements to how developers integrate xAI's search capabilities into their applications. The update addresses the evolution of xAI's API design, moving away from deprecated search parameters toward a more flexible agent-based tool architecture while adding enhanced image search functionality.

## TL;DR

- **Deprecated searchParameters**: The xAI provider is retiring the `searchParameters` field for live search functionality in favor of dedicated web search and x-search agent tools, modernizing the API surface.
- **Image search expansion**: The `xai.tools.webSearch()` method now supports an `enableImageSearch` parameter, allowing developers to include image results alongside traditional web search results.
- **Impact**: Developers using the xAI provider need to migrate away from the old search parameters approach, but gain access to more granular control over search behavior and capabilities.

## Background

The xAI Responses API has evolved significantly as Vercel's AI SDK matured. Initially, search functionality was integrated directly into request parameters—a straightforward but limiting approach. As xAI's capabilities expanded, the team recognized that treating search as a composable tool rather than a built-in parameter offered greater flexibility and consistency with modern AI framework patterns.

Agent tools represent a paradigm shift in how AI systems access external capabilities. Rather than hardcoding search into the API call itself, tools are composed dynamically, allowing models to decide whether to invoke search, which search type to use, and how to interpret results. This aligns with how other AI providers and frameworks approach extending model capabilities.

The deprecation of `searchParameters` signals that Vercel is consolidating around this tool-based approach, while the addition of image search capabilities reflects xAI's continued expansion of what its search tools can retrieve.

## How it Works

### Migrating from searchParameters to Agent Tools

The older approach embedded search directly in API calls through `searchParameters`. This worked but created tight coupling between the core API and search functionality. The new pattern leverages xAI's agent tools—specifically `xai.tools.webSearch()` and `xai.tools.xSearch()`—which models can invoke as needed during inference.

Rather than sending a search request upfront, developers now pass available tools to the model, and it determines whether searching is necessary. This enables more intelligent behavior: the model might skip search for questions it can answer from training data, use web search for current information, or employ x-search (likely optimized for X/Twitter data) for social context. Developers migrating their code should move from direct `searchParameters` configuration to registering tools in their model initialization.

### Enhanced Image Search Capability

The addition of `enableImageSearch` to the web search tool expands xAI's search versatility. Web search traditionally returns text-based results—articles, pages, snippets. By enabling image search, developers can now retrieve visual content alongside textual information, useful for queries where images provide essential context or directly answer the user's question.

Implementation is straightforward: when calling `xai.tools.webSearch()`, developers can pass `enableImageSearch: true`. The SDK automatically translates this to xAI's API specification as `enable_image_search`. This parameter works transparently; if a user queries something like "latest iPhone design," the model can retrieve both written reviews and product imagery, synthesizing a more complete response.

## Technical Considerations

**Backward Compatibility**: The deprecation of `searchParameters` doesn't remove it immediately—canary versions allow for gradual migration periods. However, developers should plan updates soon, as deprecations eventually become removals in stable releases.

**Tool Composition**: Using separate web search and x-search tools requires developers to understand when each is appropriate. Web search suits general information needs; x-search likely performs better for trending topics, social sentiment, and real-time discussions on X.

**API Cost and Latency**: Image search may increase API costs and response latency compared to text-only search, so it should be enabled deliberately rather than by default for all queries.

## What Happens Next

This update positions the xAI provider for broader capability expansion. As xAI's API continues developing, the tool-based architecture allows new search variants, filtering options, or specialized search types to be added without fundamental restructuring. The image search addition suggests Vercel and xAI are focusing on multimodal search experiences—an increasingly important frontier as AI applications demand richer information retrieval.

Developers using the xAI provider should test their applications against this canary release, validate that tool-based search works for their use cases, and begin deprecating any legacy `searchParameters` usage. The migration is technical but straightforward, offering an opportunity to embrace more flexible search patterns in AI applications.

For teams building with Vercel's AI SDK targeting xAI models, now is the time to understand these changes and plan migration timelines before these APIs stabilize.
*This article does not contain affiliate links.*
