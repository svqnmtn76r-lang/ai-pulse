---
category: other
date: '2026-05-22'
generated_at: '2026-05-22T21:47:12.823402Z'
generated_by: claude-haiku-4-5-2026-05-22
importance_score: 50
products: []
source_name: github:vercel/ai
source_url: https://github.com/vercel/ai/releases/tag/%40ai-sdk/google-vertex%404.0.136
template_type: breaking
title: vercel/ai @ai-sdk/google-vertex@4.0.136
word_count: 331
---

## TL;DR

- **Patch Update Released**: Vercel's AI SDK Google Vertex integration (@ai-sdk/google-vertex) has been updated to version 4.0.136, a maintenance release addressing dependency alignment
- **Anthropic SDK Upgraded**: The patch includes an update to the companion Anthropic SDK package (@ai-sdk/anthropic) to version 3.0.79, ensuring compatibility across the AI toolkit ecosystem
- **Incremental Progress**: This routine update reflects ongoing stabilization efforts in Vercel's modular AI SDK architecture

## What happened

Vercel has released a patch update to its Google Vertex AI integration module as part of the larger AI SDK ecosystem. The 4.0.136 release, published on GitHub's Vercel/ai repository, represents a maintenance update focused on dependency management rather than introducing new features.

The core change involves updating the @ai-sdk/anthropic dependency to version 3.0.79, ensuring that developers using both Google Vertex and Anthropic models through Vercel's unified SDK maintain compatibility across integrated tools. This type of synchronized versioning is critical for teams leveraging multiple LLM providers within a single application architecture.

Vercel's AI SDK has emerged as a significant player in the developer tooling space, offering a unified interface for interacting with various AI model providers including Google Vertex, Anthropic, OpenAI, and others. By maintaining tight dependency management across these provider-specific modules, Vercel reduces integration friction for developers building multi-model AI applications.

The patch-level designation indicates this is not a breaking change, meaning existing implementations should continue functioning without modification. However, developers are generally advised to keep their dependencies current to benefit from security patches and performance improvements that may be bundled in subsidiary updates.

## What happens next

Developers using the Google Vertex module should review their dependency management to ensure they're running compatible versions across the SDK ecosystem. The modular architecture means updates can be adopted independently, but coordinating versions prevents potential compatibility issues in production environments.

Keep monitoring Vercel's AI SDK repository for further updates, particularly as Google and Anthropic continue refining their respective model APIs. Integration updates often follow upstream changes to model providers' APIs or pricing models.
*Disclosure: This article contains affiliate links. As an affiliate, we earn from qualifying purchases at no extra cost to you.*
