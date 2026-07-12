---
category: sdk_release
date: '2026-07-12'
generated_at: '2026-07-12T04:31:03.917057Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:langchain-ai/langchain
source_url: https://github.com/langchain-ai/langchain/releases/tag/langchain-openai%3D%3D1.3.5
template_type: explainer
title: langchain-ai/langchain langchain-openai==1.3.5
word_count: 751
---

# LangChain OpenAI 1.3.5 Release: What You Need to Know

LangChain has released version 1.3.5 of its OpenAI integration package, introducing support for OpenAI's prompt caching feature alongside routine model profile updates. This incremental release represents a meaningful step forward for developers building applications that leverage large language models, particularly those looking to optimize costs and reduce latency in production environments.

## TL;DR

- **Prompt Caching Support**: The release adds explicit support for OpenAI's prompt caching capability, allowing developers to cache frequently-used context and reduce redundant API calls
- **Model Profile Refresh**: Updated model profile data ensures compatibility with the latest OpenAI models and their specifications
- **Impact**: Teams building LangChain applications can now implement more efficient LLM workflows with lower operational costs and faster response times

## Background

LangChain has established itself as a foundational framework for building applications powered by large language models. The library abstracts away low-level API complexity, enabling developers to focus on application logic rather than integration details. However, as LLM applications scale, operational efficiency becomes critical—API costs accumulate quickly, and latency can undermine user experience.

OpenAI introduced prompt caching as a mechanism to address these challenges. The feature allows applications to cache static or semi-static portions of prompts, reducing the number of tokens processed on each request. For example, a customer service application that includes a lengthy company knowledge base in every prompt can cache that content, paying only once for the initial cache write, then leveraging the cached tokens at a discounted rate for subsequent requests.

Until this release, LangChain's OpenAI integration lacked explicit support for this capability, requiring developers to manually implement caching logic or use lower-level APIs directly. This created friction for teams wanting to optimize their LangChain applications.

## How it works

### Explicit Prompt Caching Implementation

The new version introduces first-class support for prompt caching within LangChain's OpenAI integration layer. Developers can now define which portions of their prompts should be cached, and the integration handles the caching logic transparently.

This works by marking specific sections of prompts with caching directives. When LangChain constructs API requests to OpenAI, it includes the necessary cache control parameters. On the first request, OpenAI processes all tokens normally. Subsequent requests that reference the same cached content incur lower token costs—typically 10% of the standard token price for cached input tokens, compared to standard pricing for regular input tokens.

The implementation is particularly valuable for applications using chain-of-thought prompting, system instructions, or retrieval-augmented generation (RAG) patterns, where large static contexts are prepended to user queries. By caching these contexts, teams can achieve cost reductions of 20-40% in typical production scenarios, depending on the ratio of cached to non-cached content.

### Model Profile Data Refresh

Alongside caching support, this release updates LangChain's internal model profile data. Model profiles define the capabilities, token limits, and pricing information for each OpenAI model. This refresh ensures that LangChain accurately reflects the current OpenAI model ecosystem, including recently released variants or parameter changes.

Keeping model profiles current is essential for production applications. When LangChain doesn't have accurate information about a model's context window or cost structure, it can make suboptimal routing decisions or incorrect cost calculations. Teams relying on LangChain's built-in cost tracking or token counting features depend on these profiles being accurate.

## Integration considerations

For existing LangChain users, this release is backward compatible. Applications built on previous versions will continue to function without modification. However, teams looking to implement prompt caching should review their use cases for caching opportunities.

The most straightforward candidates for caching include:
- System prompts and instructions that remain constant across requests
- Large static knowledge bases or context documents in RAG systems
- Retrieved context from vector databases that may be reused across multiple user queries
- Multi-turn conversation histories in chat applications

Implementation requires minimal code changes in most cases—typically just setting cache configuration parameters when initializing OpenAI models through LangChain.

## What happens next

This release reflects LangChain's ongoing effort to keep pace with OpenAI's evolving capabilities. As OpenAI introduces new features—whether performance improvements, cost optimization tools, or architectural enhancements—LangChain aims to expose them to developers with minimal friction.

For practitioners building LangChain applications, the immediate opportunity lies in auditing existing deployments for prompt caching potential. Teams running high-volume inference workloads against static contexts should prioritize implementing caching to reduce operational costs.

The broader trajectory suggests LangChain will continue serving as a bridge between rapid model innovation and production application needs, helping developers adopt new capabilities without rewriting their application logic.
*This article does not contain affiliate links.*
