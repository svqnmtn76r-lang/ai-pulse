---
category: sdk_release
date: '2026-06-24'
generated_at: '2026-06-24T05:08:56.091664Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:vercel/ai
source_url: https://github.com/vercel/ai/releases/tag/%40ai-sdk/xai%403.0.97
template_type: explainer
title: vercel/ai @ai-sdk/xai@3.0.97
word_count: 848
---

# Vercel's AI SDK Expands Xai Support: New Reasoning Modes and Model Updates

Vercel has released version 3.0.97 of its Xai integration for the AI SDK, introducing enhanced reasoning capabilities and updated model support that reflects Xai's evolving product lineup. This patch update brings developers closer alignment with the latest reasoning models available from Xai, Elon Musk's artificial intelligence company.

## TL;DR

- **Reasoning effort levels**: The SDK now supports 'none' and 'medium' reasoning effort settings, giving developers granular control over inference speed and computational cost
- **Updated model roster**: Three new models added to the supported lineup—grok-4.3, grok-build-0.1, and grok-imagine-image-quality—replacing outdated model identifiers
- **Impact**: Developers using Vercel's AI SDK can now better utilize Xai's reasoning capabilities while maintaining compatibility with the latest available models

## Background

Vercel's AI SDK serves as a unified interface for developers to integrate multiple AI model providers—including OpenAI, Anthropic, Google, and others—into their applications. The Xai provider module enables developers to access Xai's Grok models through a consistent API, eliminating the need to learn provider-specific implementations.

Reasoning models, a category that gained prominence with OpenAI's o1 release, allow language models to perform extended computation before generating responses. This approach trades latency for accuracy on complex tasks, making it valuable for coding assistance, mathematical problem-solving, and logical reasoning tasks.

Prior to this update, the Xai integration had limited granularity in controlling reasoning behavior. Developers needed more flexibility to balance quality against inference costs and latency—a critical consideration in production systems where every millisecond and compute token matters.

## How it works

### Reasoning Effort Configuration

The update introduces support for 'none' and 'medium' reasoning effort levels, extending the control developers have over model behavior. When set to 'none', the model operates in standard mode without extended reasoning—faster but less capable on complex reasoning tasks. The 'medium' setting enables reasoning capabilities at a moderate computational cost, positioning itself between fast inference and maximum reasoning depth.

This tiered approach acknowledges a fundamental tradeoff in AI systems: more reasoning compute improves answer quality but increases latency and token consumption. Developers can now select the appropriate level based on their use case. A customer support chatbot might use 'none' for real-time responses, while a code review tool could leverage 'medium' reasoning for deeper analysis.

The implementation allows developers to specify reasoning effort at runtime, enabling dynamic selection based on query complexity or system load. Some frameworks might detect a particularly difficult user question and automatically escalate to medium reasoning, while simpler queries use standard processing.

### Updated Model Identifiers

The patch curates the available model list to reflect Xai's current offerings. Three models now appear in the supported lineup: grok-4.3, grok-build-0.1, and grok-imagine-image-quality. These additions suggest Xai's strategic direction toward specialized model variants.

Grok-4.3 likely represents an incremental improvement over the previous generation, incorporating refinements from user feedback and additional training. Grok-build-0.1 appears positioned as a model specialized for software development tasks, aligning with industry trends toward code-specific models. Grok-imagine-image-quality targets image generation or manipulation workflows, expanding Xai's multimodal capabilities.

The update removes older model identifiers from the curated list, signaling deprecation without breaking existing implementations. Developers referencing legacy model names will receive clear errors rather than silent failures, prompting necessary updates.

### Integration with Vercel's SDK architecture

The changes integrate seamlessly with Vercel's existing abstraction layer. Developers using the AI SDK don't need to learn Xai-specific syntax; instead, they specify reasoning effort through standard parameters that work across multiple providers (where supported). This consistency reduces cognitive load when working with multiple model providers.

The SDK handles parameter mapping internally—converting 'medium' to whatever internal parameter Xai expects, managing differences between providers' implementations, and handling version compatibility. This abstraction layer is particularly valuable as providers evolve their APIs independently.

## Practical implications

For developers actively using Xai models, this update removes friction from accessing the latest available options. Applications built with outdated model identifiers can migrate to grok-4.3 and other new models without rewriting integration code.

The reasoning effort settings enable more sophisticated deployment strategies. Teams can implement adaptive selection logic: detect question complexity, select appropriate reasoning level, and optimize for either speed or accuracy. This is particularly relevant for applications serving diverse user needs—real-time chat versus batch analysis workflows.

The addition of grok-build-0.1 and grok-imagine-image-quality signals Xai's commitment to specialized models, suggesting the company is moving beyond general-purpose chat toward domain-specific applications. Developers should monitor whether these models receive the same performance and reliability characteristics as the flagship Grok model.

## What happens next

Developers using the @ai-sdk/xai package should update their dependencies to access these new models and reasoning capabilities. Teams relying on deprecated model identifiers should test compatibility with the new model roster and adjust their deployment accordingly.

As reasoning models mature across the industry, expect further refinements to the reasoning effort abstraction. Additional levels (such as 'high' for maximum reasoning compute) may appear in future releases, following standardization efforts across AI providers.

Watch for additional models joining Xai's lineup that might address new use cases—specialized variants for analysis, code generation, or creative tasks would align with the strategic direction suggested by this update.
*This article does not contain affiliate links.*
