---
category: sdk_release
date: '2026-05-30'
generated_at: '2026-05-30T04:58:54.988341Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:vercel/ai
source_url: https://github.com/vercel/ai/releases/tag/%40ai-sdk/xai%404.0.0-canary.69
template_type: explainer
title: vercel/ai @ai-sdk/xai@4.0.0-canary.69
word_count: 917
---

# Vercel AI SDK xAI Update: Deprecating Search Parameters in Favor of Agent Tools

Vercel's AI SDK has released a new canary version for its xAI provider integration, bringing important changes to how developers implement web search functionality. Version 4.0.0-canary.69 marks a shift in the SDK's approach to search capabilities, moving away from direct search parameters toward a more flexible agent-based tool architecture.

## TL;DR

- **SearchParameters deprecation**: The SDK is phasing out the `searchParameters` configuration option for xAI's live search feature, directing developers toward dedicated web search agent tools instead
- **Enhanced image search**: The xAI Web Search tool now includes `enableImageSearch` support, allowing developers to include image results in search responses through the xAI Responses API
- **Impact**: Developers using current xAI integration will need to migrate to the new agent tool pattern, gaining more granular control and flexibility in the process

## Background

Web search capabilities in AI applications have traditionally been implemented through direct API parameters—a straightforward but somewhat rigid approach. As AI SDK matured and the xAI Responses API evolved, the framework's maintainers recognized that agent-based tools provide a more composable and extensible pattern for handling searches alongside other operations.

The previous `searchParameters` implementation worked, but it represented an older paradigm where search was tightly coupled to the provider configuration. The shift toward web search and x_search agent tools aligns with broader trends in AI development where distinct capabilities are exposed as discrete, chainable components rather than monolithic feature sets.

This evolution reflects lessons learned from supporting multiple AI providers and use cases. Agent tools enable developers to conditionally use search, combine it with other tools, and maintain cleaner separation of concerns in their applications.

## How it works

### Moving from SearchParameters to Agent Tools

The deprecation of `searchParameters` in favor of web search and x_search agent tools represents a fundamental architectural improvement. Rather than configuring search at the provider level, developers now explicitly add search as an available tool their AI agent can invoke.

This agent-based approach provides several advantages. First, it makes search capabilities discoverable and declarable—your AI application explicitly registers which tools are available. Second, it enables better control flow: the model can decide whether to search, how many times, and for what information. Third, it integrates seamlessly with tool-use patterns already established in the AI SDK, creating consistency across different types of agent interactions.

The migration path is straightforward: instead of setting search parameters during xAI provider initialization, developers now call `xai.tools.webSearch()` or `xai.tools.xSearch()` to create tool definitions that can be passed to their model. This declarative pattern scales better as applications add more capabilities and become more complex.

### Enhanced Image Search Capabilities

The addition of `enableImageSearch` to the Web Search tool opens new possibilities for applications requiring visual content alongside traditional search results. The xAI Responses API already supported image search through its `enable_image_search` parameter, but the AI SDK's xAI provider now exposes this functionality directly.

Developers can now pass `enableImageSearch: true` when creating a web search tool, and the SDK automatically translates this to the appropriate API parameter. This is a minor but meaningful enhancement—it removes the need for manual API calls and ensures image search requests flow through the established tool pipeline.

This feature proves particularly valuable for applications that need to provide comprehensive responses combining text and visual information. Search results with images can significantly improve user experience in research tools, content discovery applications, or any system where visual context matters alongside textual information.

### The Broader Agent Tools Pattern

Understanding why this change matters requires context about how the AI SDK structures agent interactions. Agent tools in this framework represent distinct capabilities that language models can invoke during task execution. Each tool has defined inputs, outputs, and behaviors.

By treating web search as an agent tool rather than a provider configuration, the SDK achieves several benefits. Tools can be versioned independently, composed together, and conditionally made available based on application state. A model might access web search, a database lookup tool, and a calculation tool simultaneously, choosing which to invoke based on the task at hand.

This architecture also improves testing and debugging. Tool invocations appear explicitly in execution logs and traces, making it easier to understand why a model made particular decisions. Developers can monitor tool usage, implement rate limiting on specific tools, and implement fallback behaviors when tools fail.

## What happens next

Developers currently using the xAI provider with `searchParameters` should plan a migration to the new agent tools approach. While the deprecation warning indicates the old pattern still works in canary versions, final removal will likely come in a future stable release.

The good news: the migration is typically a small code change. Instead of provider-level configuration, you'll define your tools upfront and pass them to your model calls. This often results in cleaner, more maintainable code since tool availability is explicit rather than implicit.

For new projects using xAI, start with the web search and x_search agent tools directly. There's no reason to use the deprecated pattern, and you'll immediately benefit from the more flexible agent-based architecture.

Developers should also consider whether enabling image search aligns with their use cases. For many applications, visual search results add meaningful value—particularly in content creation, research, or user-facing search interfaces.

The xAI provider continues maturing within the Vercel AI SDK ecosystem, and these changes demonstrate the framework's commitment to providing flexible, composable abstractions rather than feature-specific configurations. As the SDK evolves, expect similar patterns across other providers and capabilities.
*This article does not contain affiliate links.*
