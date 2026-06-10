---
category: sdk_release
date: '2026-06-10'
generated_at: '2026-06-10T05:27:41.261129Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:langchain-ai/langchain
source_url: https://github.com/langchain-ai/langchain/releases/tag/langchain%3D%3D1.3.5
template_type: explainer
title: langchain-ai/langchain langchain==1.3.5
word_count: 824
---

# LangChain 1.3.5 Released: Middleware Upgrades and OpenAI Tool Support

LangChain, the popular open-source framework for building applications with large language models, has released version 1.3.5, bringing incremental improvements focused on middleware capabilities, OpenAI integration enhancements, and dependency updates. While not a major feature release, this update addresses several technical improvements that affect developers working with summarization workflows and OpenAI's tool ecosystem.

## TL;DR

- **AND-capable trigger conditions**: The SummarizationMiddleware now supports more granular control over when summarization logic executes, enabling complex conditional workflows
- **OpenAI apply_patch tool**: New built-in tooling support expands LangChain's integration with OpenAI's native capabilities
- **Dependency modernization**: Critical updates to core dependencies like PyArrow and aiohttp improve security and performance
- **Impact**: Developers building production LLM applications gain more flexibility in middleware logic and tighter OpenAI integration, while dependency updates address potential vulnerabilities

## Background

LangChain has evolved as the de facto standard framework for orchestrating LLM-powered applications. The framework's middleware system handles cross-cutting concerns—logging, monitoring, request processing, and in this case, summarization—across LLM chains. However, middleware systems typically face a common challenge: determining *when* to execute their logic.

The summarization middleware previously relied on simpler trigger mechanisms. Real-world applications often need sophisticated conditional logic—execute summarization when *both* certain conditions are met, or when specific combinations of states align. The AND-capable conditions feature addresses this gap by allowing developers to chain multiple conditions together with boolean logic.

Meanwhile, OpenAI continuously expands its API surface, introducing new tools and capabilities. The framework needed to keep pace with these additions. The `apply_patch` tool represents OpenAI's expanding toolkit for more advanced use cases, and LangChain's integration ensures developers can leverage these features without manual workarounds.

The dependency updates, though less glamorous, represent critical maintenance. PyArrow's jump from 21.0.0 to 23.0.1 likely includes performance improvements and security patches, while the aiohttp upgrade to 3.14.0 addresses async HTTP handling improvements—crucial for applications making concurrent requests to LLM APIs.

## How it works

### SummarizationMiddleware AND Conditions

Previously, middleware triggers often operated with simple OR logic: "execute if condition A OR condition B is true." The new AND-capable trigger conditions flip this approach, enabling developers to specify: "execute only when condition A AND condition B AND condition C are all satisfied."

This matters because real applications have nuanced requirements. Consider a system that summarizes conversations but only when: the conversation exceeds a certain length *and* the time since the last summary exceeds a threshold *and* the model confidence score surpasses a minimum. Previously, developers would need to encode this logic inside the middleware handler itself, mixing concerns. Now, the framework handles conditional composition, keeping logic cleaner and more declarative.

The implementation ports (transfers) this capability from another component to SummarizationMiddleware, suggesting the pattern was proven elsewhere in the codebase and now receives broader application. This approach reduces code duplication and ensures consistency across middleware types.

### OpenAI apply_patch Tool Integration

LangChain's OpenAI integration has grown increasingly sophisticated. The new `apply_patch` built-in tool support represents deeper integration with OpenAI's expanding API. Built-in tools are native capabilities provided by OpenAI that developers can invoke directly through function calling—without needing to define custom functions.

The `apply_patch` tool likely enables applications to apply incremental updates or modifications through OpenAI's API more seamlessly. By including this as a built-in tool, LangChain developers can now invoke patch operations directly from their chains without additional wrapper logic. This reduces boilerplate and potential integration errors.

### Dependency Updates and Stability

The three dependency updates serve different purposes. PyArrow is fundamental for data serialization and columnar data handling—increasingly important as LLM applications handle larger token streams and batched requests. The upgrade to 23.0.1 likely brings performance optimizations that ripple through any chain using batch operations.

The aiohttp upgrade to 3.14.0 matters for LangChain's async HTTP capabilities. Many LLM applications need concurrent request handling—querying multiple models, parallel chain execution, or making non-blocking API calls. Async HTTP handling directly impacts throughput and latency characteristics of these applications.

A minimum core dependency fix for OpenAI integration ensures compatibility across the LangChain ecosystem, preventing version conflicts that could cause runtime failures in production deployments.

## What happens next

Version 1.3.5 represents the steady cadence of incremental improvements that mature frameworks require. The next logical evolution would likely include:

- Broader middleware capability expansion, potentially bringing AND/OR logic to other middleware types
- Additional OpenAI tool integrations as their API continues expanding
- Performance optimizations flowing downstream from dependency updates
- Community feedback on middleware trigger conditions potentially spawning additional OR/AND combinations

For practitioners, this release warrants a straightforward upgrade—it's backward compatible (point release, not major) and brings tangible benefits for those using summarization workflows or OpenAI integrations. The dependency updates should be applied promptly to receive security and performance improvements, though they may require testing in existing deployments to ensure complete compatibility.

Organizations running LangChain in production should evaluate whether their summarization logic can benefit from more granular conditional triggers, potentially simplifying middleware configuration and improving code clarity.
*This article does not contain affiliate links.*
