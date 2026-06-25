---
category: sdk_release
date: '2026-06-25'
generated_at: '2026-06-25T05:12:33.318193Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:vercel/ai
source_url: https://github.com/vercel/ai/releases/tag/%40ai-sdk/xai%403.0.97
template_type: explainer
title: vercel/ai @ai-sdk/xai@3.0.97
word_count: 829
---

# Vercel AI SDK Adds Support for XAI's Latest Models and Reasoning Controls

Vercel has released a new patch update to its XAI integration within the AI SDK, bringing support for additional Grok models and introducing configurable reasoning effort levels. The update reflects the evolving capabilities of XAI's model lineup and gives developers finer-grained control over how the language models approach problem-solving tasks.

## TL;DR

- **Reasoning effort controls**: Developers can now specify 'none' or 'medium' reasoning effort levels when working with XAI models, allowing optimization between response speed and analytical depth
- **Expanded model lineup**: Three new models have been added to the supported roster: grok-4.3, grok-build-0.1, and grok-imagine-image-quality
- **Impact**: Teams building with the Vercel AI SDK can now access XAI's latest capabilities without waiting for downstream framework updates, with more granular control over inference behavior

## Background

The Vercel AI SDK serves as a unified interface for integrating multiple AI providers into applications. Rather than requiring developers to learn separate APIs for OpenAI, Anthropic, Google, and other providers, the SDK abstracts these differences behind a consistent programming interface. XAI, Elon Musk's AI research company, launched Grok as a conversational AI model available through the SDK's provider ecosystem.

As XAI continues developing new models optimized for different use cases—from general chat to specialized reasoning to image generation—the SDK must stay synchronized with these releases. This patch update addresses that synchronization, ensuring developers can access the latest models without friction.

The concept of "reasoning effort" itself represents an evolution in how modern language models approach tasks. Rather than always thinking at maximum capacity (which increases latency and computational cost), developers can now signal to the model whether a task requires deep analytical reasoning or simpler, faster responses.

## How it works

### Reasoning Effort Levels

XAI's models now support configurable reasoning effort, a parameter that influences how extensively the model explores a problem space before generating responses. The patch introduces support for two distinct settings: 'none' and 'medium'.

When set to 'none', the model prioritizes speed and efficiency, generating responses with minimal internal deliberation. This suits straightforward queries, information retrieval, and real-time applications where latency matters more than exhaustive analysis. When set to 'medium', the model dedicates more computational resources to reasoning through complex problems, considering multiple angles and approaches before responding. This strikes a balance between quality and performance, useful for technical questions, writing tasks, and scenarios requiring moderate analytical depth.

This parameter-driven approach represents a practical implementation of scaling laws in language models. Rather than training separate models at different capability tiers, XAI can deploy a single model that adjusts its inference behavior based on the task requirements. Developers benefit from flexibility: they can use the same model for both quick facts and in-depth analysis, simply by adjusting the reasoning effort parameter in their API calls.

### Updated Model Roster

The patch curates XAI's model identifiers to match the current production lineup. Three models were added: grok-4.3 represents the latest iteration of XAI's flagship conversational model, building on previous versions with architectural improvements and expanded knowledge. Grok-build-0.1 appears specialized for software development tasks, likely trained with emphasis on code generation, debugging assistance, and technical documentation. Grok-imagine-image-quality targets image generation and manipulation, suggesting XAI is expanding beyond text into multimodal capabilities.

The curation step—removing outdated model identifiers and adding current ones—prevents developers from accidentally calling deprecated endpoints. When model identifiers are removed from the supported list, developers attempting to use them receive clear errors rather than ambiguous failures. This maintenance work might seem invisible, but it's essential infrastructure that keeps SDK integrations reliable as upstream providers evolve.

### Integration Points

For developers using Vercel's AI SDK, these changes surface through familiar interfaces. When instantiating an XAI client, developers can now pass reasoning effort as a configuration parameter. Model selection happens through string identifiers matching XAI's official model names. The SDK handles the translation from these standardized identifiers into actual API calls to XAI's infrastructure.

This follows the SDK's established pattern: provide a provider-agnostic interface that shields developers from implementation details, while exposing provider-specific capabilities when needed. A developer might write code that looks identical whether calling OpenAI, XAI, or another provider, with only the model identifier and provider-specific parameters differing.

## What happens next

As XAI continues releasing new models and refining reasoning capabilities, expect further updates to the AI SDK's XAI integration. The pattern established here—supporting new reasoning control parameters and curating model lists—will likely repeat as the field evolves.

Developers building applications with the Vercel AI SDK can immediately benefit from accessing Grok-4.3 and the specialized models, while the reasoning effort parameter enables optimization for their specific use cases. Teams should review their XAI model selections to ensure they're using the latest versions, as older identifiers may eventually be deprecated.

For those not yet integrated with the SDK, this update demonstrates the value of using abstraction layers for AI—they move faster than individual applications in adopting new capabilities, reducing the engineering burden on development teams.
*This article does not contain affiliate links.*
