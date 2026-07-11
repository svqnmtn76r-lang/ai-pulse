---
category: sdk_release
date: '2026-07-11'
generated_at: '2026-07-11T04:20:27.876301Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:langchain-ai/langchain
source_url: https://github.com/langchain-ai/langchain/releases/tag/langchain-openai%3D%3D1.3.5
template_type: explainer
title: langchain-ai/langchain langchain-openai==1.3.5
word_count: 803
---

# LangChain OpenAI 1.3.5 Release: Prompt Caching Support Arrives

LangChain has rolled out version 1.3.5 of its OpenAI integration package, introducing explicit prompt caching capabilities alongside routine maintenance updates. This incremental release represents a meaningful step forward for developers building cost-conscious AI applications, particularly those leveraging OpenAI's latest models.

## TL;DR

- **Prompt Caching Support**: The update adds explicit prompt caching functionality, allowing developers to cache repeated prompt content and reduce API costs and latency
- **Model Profile Updates**: Backend model information has been refreshed to reflect the latest OpenAI model capabilities and parameters
- **Impact**: Applications processing repetitive prompts or working with long context windows can now achieve significant performance improvements and lower operational expenses

## Background

LangChain has positioned itself as a critical abstraction layer between applications and large language models, handling the complexity of prompt engineering, chain orchestration, and model integration. As LangChain's ecosystem matured, OpenAI remained a primary integration target—the langchain-openai package serves as the official bridge between LangChain's framework and OpenAI's API endpoints.

Prompt caching itself isn't entirely new; OpenAI introduced this feature to their API months earlier as a mechanism to reduce costs for applications with repetitive prompt structures. However, LangChain's explicit support required thoughtful integration into the framework's architecture. Prior to this release, developers could theoretically access caching through raw API calls, but doing so meant bypassing LangChain's abstraction layers and handling cache headers manually.

The need for caching support became increasingly apparent as enterprises deployed LangChain applications at scale. Consider a customer service chatbot that prepends the same system prompt and company documentation to every user query. Without caching, each API call incurs the full token cost for that static context. With caching, OpenAI's infrastructure stores this content server-side, requiring payment only on the first request while subsequent requests reference the cached content at a significant discount.

## How it Works

### Explicit Prompt Caching Implementation

The 1.3.5 release enables developers to explicitly mark which portions of their prompts should be cached. Rather than relying on OpenAI's automatic caching heuristics, explicit caching gives developers fine-grained control over what gets cached and when.

When a prompt is cached, OpenAI stores the token representation on their infrastructure. The cache persists for five minutes by default, during which time identical requests can reference it. From an API perspective, cached tokens cost 90% less than regular tokens—a substantial reduction for applications processing similar prompts repeatedly. The implementation within LangChain abstracts away the complexity of cache headers (such as `cache_control` parameters) that developers would otherwise need to manage directly.

This approach particularly benefits applications processing long context windows. A RAG (Retrieval-Augmented Generation) system that consistently includes large document chunks before user queries becomes exponentially more cost-efficient. The same applies to few-shot learning scenarios where example prompts remain constant while only user input varies.

### Model Profile Refresh

The model profile update ensures LangChain's internal knowledge about OpenAI's model lineup remains current. These profiles contain crucial metadata: token limits, pricing information, supported features, and capability flags. As OpenAI releases new models or modifies existing ones, these profiles must be updated to reflect current specifications.

Stale model profiles can cause subtle issues. Applications might attempt to use features unsupported by the actual model, rely on incorrect token limit calculations, or experience pricing surprises due to outdated rate information. By refreshing these profiles regularly, LangChain maintains alignment with OpenAI's actual offerings and prevents these discrepancies from affecting production systems.

## Technical Implementation Details

The explicit caching feature integrates with LangChain's existing prompt template and model integration systems. Developers can specify caching directives at multiple levels: on individual prompt components, across entire chains, or within custom LLM wrappers.

When implementing caching, the framework must handle several considerations. Cache validity periods require careful management—too short and the cache frequently expires between requests, defeating its purpose; too long and outdated content might be served. LangChain's implementation provides sensible defaults while allowing customization for specific use cases.

Cost calculation also becomes more nuanced with caching enabled. Tools that estimate prompt costs must distinguish between cached and non-cached tokens. The release includes updates to cost calculation utilities to properly account for cache hits versus misses, providing accurate financial forecasting for deployed applications.

## What Happens Next

Developers using LangChain with OpenAI should evaluate whether their applications have repetitive prompt patterns suitable for caching. Common candidates include chatbots with consistent system prompts, RAG systems with stable document contexts, and batch processing pipelines that repeatedly use the same instructions.

The framework will likely continue refining cache management in future releases—potential improvements could include automatic cache lifecycle management, cache performance monitoring, and enhanced debugging tools for cache-related issues.

Teams should also monitor OpenAI's model updates to ensure their LangChain installations benefit from the latest model profile information. Regular dependency updates remain the best practice for maintaining optimal performance and cost efficiency.
*This article does not contain affiliate links.*
