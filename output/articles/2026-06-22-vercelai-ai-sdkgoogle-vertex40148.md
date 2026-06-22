---
category: sdk_release
date: '2026-06-22'
generated_at: '2026-06-22T06:36:12.793494Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:vercel/ai
source_url: https://github.com/vercel/ai/releases/tag/%40ai-sdk/google-vertex%404.0.148
template_type: explainer
title: vercel/ai @ai-sdk/google-vertex@4.0.148
word_count: 806
---

# Google Vertex AI SDK Fix: Correcting Gemini Embedding Model Routing

Vercel's AI SDK has released a patch update for its Google Vertex AI integration that addresses a critical routing issue affecting Gemini embedding models. The fix ensures that newer embedding models are directed to the correct API endpoint, resolving errors that previously prevented these models from functioning properly.

## TL;DR

- **Embedding endpoint routing**: Gemini embedding models now correctly route through the `:embedContent` endpoint instead of the `:predict` endpoint
- **Affected models**: The patch specifically targets `gemini-embedding-2` and `gemini-embedding-2-preview` model versions
- **Error resolution**: This eliminates FAILED_PRECONDITION errors (HTTP 400) that occurred when using these models
- **Impact**: Developers using Google Vertex AI embeddings can now reliably generate text embeddings without workaround configurations

## Background

The Vercel AI SDK provides a unified interface for developers to integrate various AI models and services into their applications. Google Vertex AI is one of these supported providers, offering access to Google's advanced AI models including embedding models used for semantic search, similarity matching, and other vector-based operations.

Embedding models convert text into numerical vector representations—high-dimensional arrays of numbers that capture semantic meaning. This process is essential for modern AI applications requiring document retrieval, recommendation systems, and similarity searches.

The Gemini embedding models represent Google's latest generation of embedding technology, offering improved performance over previous versions. However, Google Vertex AI exposes these models through different endpoints depending on their purpose. The `:predict` endpoint is a general-purpose inference interface, while `:embedContent` is specifically optimized for embedding operations with dedicated request and response formats.

Prior to this patch, the SDK's routing logic didn't distinguish between different model capabilities, attempting to send embedding requests to the generic `:predict` endpoint. This created a mismatch: the endpoint expected different input/output structures than what embedding models provide, resulting in FAILED_PRECONDITION errors that blocked legitimate requests.

## How it works

### Understanding API Endpoints and Model Capabilities

Google Vertex AI provides multiple inference endpoints, each designed for specific use cases. The `:predict` endpoint is a catch-all interface supporting numerous model types and configurations, accepting flexible request formats. In contrast, the `:embedContent` endpoint is purpose-built for embedding models, with a specialized schema optimized for text-to-vector conversion.

The distinction exists because embedding models have unique requirements and response patterns. They accept text input and return numerical vectors of fixed dimensions. Other models might accept images, audio, or structured data with different output formats. By providing specialized endpoints, Google Vertex AI can optimize performance, validation, and response handling for each use case.

The Gemini embedding models—both the stable `gemini-embedding-2` and its preview version—are designed to work exclusively through the `:embedContent` endpoint. When requests reached the `:predict` endpoint instead, the service rejected them with a FAILED_PRECONDITION error, preventing any embedding operations.

### The Fix: Intelligent Routing Logic

The patch implements model-specific routing rules within the Vercel AI SDK. When developers request embedding operations using `gemini-embedding-2` or `gemini-embedding-2-preview` models, the SDK now explicitly directs these requests to the `:embedContent` endpoint rather than the generic `:predict` path.

This represents a targeted solution that adds minimal overhead while solving the compatibility problem. The SDK maintains a list of models requiring special endpoint routing, checking model identifiers against this list during request construction. For affected models, the SDK constructs properly formatted requests compatible with the embedding-specific endpoint's schema.

This approach preserves backward compatibility with other models that continue using the `:predict` endpoint while ensuring newer embedding models function correctly. Developers don't need to modify their code or add conditional logic—the routing happens transparently within the SDK.

### Practical Implications for Developers

The patch removes a significant barrier to using Google's latest embedding models within Vercel's AI framework. Previously, attempts to generate embeddings with `gemini-embedding-2` would fail immediately. Now, developers can use these models seamlessly within their applications, leveraging their improved semantic understanding capabilities.

The fix also prevents the need for workarounds, such as calling Google Vertex AI directly instead of through the SDK, or using older embedding model versions. This maintains the SDK's value proposition: providing a consistent, unified interface across multiple AI providers.

For teams already using the Vercel AI SDK, upgrading to version 4.0.148 of the Google Vertex integration is straightforward and provides immediate access to the fixed routing behavior. The change is entirely backward compatible—existing code continues functioning without modification.

## What happens next

Developers using the Vercel AI SDK with Google Vertex AI can update their dependencies to receive this fix. The patch is particularly valuable for teams planning to migrate to newer Google embedding models or those experiencing the FAILED_PRECONDITION errors during embedding operations.

For those implementing semantic search, recommendation engines, or other vector-based features using Google's infrastructure, this update removes a technical hurdle and enables reliable access to Google's latest embedding technology. As embedding models continue evolving, similar routing patches may be necessary for other models or providers.
*This article does not contain affiliate links.*
