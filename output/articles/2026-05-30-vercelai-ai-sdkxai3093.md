---
category: sdk_release
date: '2026-05-30'
generated_at: '2026-05-30T04:58:40.021639Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:vercel/ai
source_url: https://github.com/vercel/ai/releases/tag/%40ai-sdk/xai%403.0.93
template_type: explainer
title: vercel/ai @ai-sdk/xai@3.0.93
word_count: 814
---

# Vercel AI SDK xAI Update: Evolving Search Capabilities and Agent Tools

Vercel has released version 3.0.93 of its xAI integration for the AI SDK, introducing refinements to how developers implement web search functionality within AI applications. The update reflects a broader shift toward agent-based architectures for search, moving away from direct API parameters in favor of composable tool patterns.

## TL;DR

- **Agent tools over parameters**: Web search functionality transitions from deprecated `searchParameters` to dedicated `web_search` and `x_search` agent tools, aligning with modern AI agent patterns
- **Image search support**: The xAI Web Search tool now supports image search capabilities through the new `enableImageSearch` parameter, enabling richer search results
- **Impact**: Developers building AI applications with xAI integration need to refactor existing search implementations to use the new tool-based approach, gaining more flexibility and consistency with agent-based AI workflows

## Background

Search integration in AI SDKs has historically followed different patterns across providers. Early implementations often relied on passing parameters directly to API calls, which worked but created tight coupling between the application logic and provider-specific API details. As AI applications have evolved toward agent-based architectures—where models can autonomously choose from available tools to accomplish tasks—the need for a more composable approach became apparent.

Vercel's AI SDK has been moving its provider integrations toward this tool-based paradigm, where capabilities like web search are exposed as distinct, callable tools that agents can invoke. This approach offers several advantages: it makes the model's reasoning transparent (you can see which tools it selects), enables better error handling, and allows for consistent patterns across different providers.

The previous `searchParameters` approach for xAI represented an older pattern. While functional, it didn't align with how modern AI agents work. This update deprecates that approach in favor of explicit tool definitions, bringing xAI integration in line with contemporary best practices.

## How it Works

### Transitioning from Parameters to Tools

The deprecation of `searchParameters` marks a shift in how developers configure search functionality. Rather than passing configuration through a generic parameters object, web search is now implemented as a dedicated tool that the AI model can invoke during its reasoning process.

With the tool-based approach, developers explicitly expose `web_search` or `x_search` as available actions. When an AI model encounters a task requiring current information or web results, it can autonomously select one of these tools and invoke it with appropriate parameters. This creates a clearer, more auditable flow compared to implicit parameter passing.

The migration involves minimal conceptual change but requires code updates. Instead of configuring search through initialization parameters, developers now define search tools and pass them to their agent or model invocation. This also means developers can control more granularly when and how search is available—for instance, making it conditional based on user permissions or query context.

### Image Search Capabilities

The addition of `enableImageSearch` to the xAI Web Search tool extends functionality beyond traditional text-based web results. The xAI Responses API (the underlying service) supports an `enable_image_search` parameter that filters results to include relevant images alongside text content.

The updated SDK now exposes this capability at the tool level. When developers construct their `webSearch()` tool configuration, they can set `enableImageSearch` to true, which instructs the underlying xAI API to include image results. This is particularly valuable for queries seeking visual information—product comparisons, design inspiration, technical diagrams, or documentation screenshots.

The implementation details matter here: the parameter flows through as `enable_image_search` in the actual API request, maintaining consistency with xAI's API conventions while providing a more JavaScript-idiomatic naming (`enableImageSearch`) at the SDK level. This abstraction layer is standard practice in SDKs, as it allows for language-specific naming conventions while preserving backend compatibility.

### Practical Implementation Implications

For developers currently using the deprecated `searchParameters`, the update path involves refactoring to declare tools explicitly. Rather than a breaking change that immediately stops working, deprecation gives developers a transition period. Existing code continues to function but should be updated before the deprecated path is removed in a future major version.

The tool-based approach provides additional benefits beyond API alignment. Tools can be conditionally included based on application state, can have rate limiting or usage tracking applied at the tool invocation level, and integrate naturally with agent frameworks that expect a standardized tool interface.

## What Happens Next

Developers using xAI integration should plan to update their implementations to the new tool-based pattern. This isn't urgent—deprecated functionality remains supported—but updating sooner rather than later ensures compatibility with future SDK versions and aligns with current AI development best practices.

For those building new applications, the tool-based approach should be the default choice. The `web_search` and `x_search` tools provide the same underlying functionality with better composability and clearer reasoning traces.

Consider reviewing your search configurations if you've previously set `enableImageSearch` capabilities separately or worked around limitations in text-only search. The updated tool now natively supports this, potentially simplifying implementation in applications requiring image results.
*This article does not contain affiliate links.*
