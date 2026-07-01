---
category: sdk_release
date: '2026-07-01'
generated_at: '2026-07-01T01:55:46.027429Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:vercel/ai
source_url: https://github.com/vercel/ai/releases/tag/%40ai-sdk/xai%404.0.3
template_type: explainer
title: vercel/ai @ai-sdk/xai@4.0.3
word_count: 801
---

# Vercel AI SDK Enhances Video Generation with Native Frame and Reference Support

Vercel's AI SDK has released version 4.0.3 of its XAI integration, introducing dedicated support for video generation workflows through two new first-class call options: `frameImages` and `inputReferences`. This update signals a growing focus on multimodal capabilities within the SDK ecosystem, enabling developers to work more intuitively with video-based AI models.

## TL;DR

- **Frame Images Support**: Developers can now pass video frames directly as native parameters, streamlining workflows for video analysis and generation tasks
- **Input References**: A new option allows developers to reference external media inputs, enabling more complex video generation scenarios
- **Dependency Updates**: The release includes synchronized updates across related provider packages, ensuring consistency across the AI SDK ecosystem
- **Impact**: Video generation becomes more accessible and ergonomic for developers building AI applications, reducing boilerplate code and improving developer experience

## Background

The AI SDK, maintained by Vercel, has evolved from a primarily text-focused framework into a comprehensive solution for multimodal AI interactions. Earlier iterations focused on language model integration, but the emergence of capable video generation models has created demand for native support in the SDK.

Previously, developers working with video generation had to implement custom solutions to pass visual data to AI models. This typically involved manual preprocessing of video frames, external reference handling, and custom data transformation logic. By introducing `frameImages` and `inputReferences` as first-class options, the SDK eliminates this friction point.

The XAI provider specifically handles integration with XAI's model offerings, making it a natural place for video generation enhancements. This update reflects broader industry trends toward integrated multimodal frameworks rather than bolt-on video support.

## How it works

### First-Class Frame Images Support

The `frameImages` option represents a significant usability improvement for developers working with video content. Instead of manually extracting frames and transforming them into compatible formats, developers can now pass frame data directly through standard API calls. The option integrates seamlessly with the existing parameter structure of the SDK's generation functions.

This approach acknowledges that video generation often requires visual context. Whether analyzing existing video content or generating new frames based on visual references, having native frame support reduces the gap between conceptual workflow and actual implementation. The option is "first-class" because it receives the same treatment as core parameters, rather than being handled as a special case or edge functionality.

Developers benefit from type safety, validation, and IDE autocomplete support—improvements that matter significantly when working with complex media pipelines. The implementation maintains consistency with how the SDK handles other input types, ensuring a shallow learning curve for developers already familiar with the framework.

### Input References for Contextual Generation

The `inputReferences` option introduces a complementary capability for scenarios where video generation depends on external media sources. Rather than embedding all necessary data in a single request, developers can reference external content, enabling more sophisticated workflows.

This becomes particularly valuable in production scenarios where video generation might depend on multiple source materials, brand assets, or user-provided content. Instead of embedding potentially large media files in API requests, developers can reference them by identifier or URL, reducing payload sizes and improving network efficiency.

The input references capability also enables use cases where the same source material feeds multiple generation requests, allowing for consistent visual styling or composition across a batch of generated content.

## Technical Integration Details

The release includes coordinated updates across the broader AI SDK ecosystem. Three companion packages received updates: `@ai-sdk/provider@4.0.1`, `@ai-sdk/openai-compatible@3.0.2`, and `@ai-sdk/provider-utils@5.0.2`. These synchronized updates ensure that video generation features work reliably across different deployment contexts and that the provider layer maintains compatibility with both XAI-specific and OpenAI-compatible implementations.

The openai-compatible update is particularly significant, suggesting that video generation support may be available across multiple model providers through unified interfaces. This reduces vendor lock-in and allows developers to experiment with different models without rewriting integration code.

## What this means for developers

For teams building video-focused AI applications, this release removes several implementation barriers. Previously, integrating video generation required understanding both the AI SDK patterns and video processing details. Now, developers can focus on business logic while the SDK handles the technical friction.

Teams building workflows that combine text, images, and video generation benefit from a more coherent API surface. Instead of context-switching between different libraries or implementing custom wrappers, all modalities can be handled through the unified SDK.

The timing matters as video generation capabilities mature across the model provider landscape. With native support now available, adoption barriers decrease, potentially accelerating development of video-first AI applications.

## Learn more

Developers interested in exploring video generation capabilities should consult the updated SDK documentation and review the specific call option signatures for `frameImages` and `inputReferences`. The coordinated package updates suggest exploring how video generation integrates with existing text and image workflows in your application architecture.
*This article does not contain affiliate links.*
