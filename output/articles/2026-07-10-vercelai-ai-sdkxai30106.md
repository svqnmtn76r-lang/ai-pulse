---
category: sdk_release
date: '2026-07-10'
generated_at: '2026-07-10T05:02:18.680397Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:vercel/ai
source_url: https://github.com/vercel/ai/releases/tag/%40ai-sdk/xai%403.0.106
template_type: explainer
title: vercel/ai @ai-sdk/xai@3.0.106
word_count: 796
---

# Vercel AI SDK Adds Video Support and New Grok Model: What Developers Need to Know

Vercel has released version 3.0.106 of its XAI provider for the AI SDK, introducing capabilities for video processing alongside the previously supported image inputs, plus a new model integration. This incremental update reflects the growing demand for multimodal AI applications that can process diverse content types beyond static images.

## TL;DR

- **Video Reference Inputs**: Developers can now pass video files through the `inputReferences` parameter for generation tasks, expanding beyond image-only workflows
- **Grok-4.5 Model**: XAI's latest model identifier is now available through the Vercel AI SDK, giving developers access to improved reasoning capabilities
- **Impact**: Teams building content generation, analysis, or transformation applications gain more flexible input options and access to a newer model iteration, with minimal integration changes required

## Background

The Vercel AI SDK serves as a unified interface for developers to work with multiple AI providers—OpenAI, Anthropic, Google, and others—without rewriting code when switching backends. The XAI provider specifically handles integration with xAI's models, including the Grok series known for their reasoning capabilities and occasionally irreverent personality.

Reference inputs, introduced in earlier SDK versions, allowed developers to pass context materials alongside their prompts. Previously, this was limited to image files—developers could upload screenshots, diagrams, or photos to influence generation tasks. However, modern AI applications increasingly require processing video content: analyzing surveillance footage, extracting information from recorded presentations, generating descriptions of video clips, or using videos as reference material for creative generation.

The addition of video support addresses a real friction point. Developers previously had two choices: pre-process videos into frame sequences and handle them as images (inefficient and lossy), or use external APIs to convert videos before passing them to the AI SDK (adding latency and complexity). Direct video support streamlines this workflow.

## How It Works

### Video Reference Inputs

The `inputReferences` parameter, which previously accepted only image data, now accommodates video files. The implementation maintains backward compatibility—existing code using images continues functioning unchanged. When developers pass video content, the SDK handles the necessary serialization and sends it to the xAI backend using compatible formats.

This is particularly relevant for applications like educational content summarization (extracting key points from lecture videos), accessibility features (generating transcripts or descriptions from video), quality assurance (analyzing recorded user sessions), and content recommendation systems (understanding video content for categorization). The SDK abstracts away the protocol details, allowing developers to focus on their application logic rather than video encoding specifics.

### Grok-4.5 Model Access

The second change adds the `grok-4.5` model identifier to the XAI provider. This represents xAI's latest iteration in their Grok family of models. The Grok series emphasizes reasoning over raw information recall, making it particularly useful for complex problem-solving tasks, code generation, and multi-step analysis.

By adding this model identifier, Vercel ensures developers using the AI SDK can immediately leverage the latest xAI capabilities without waiting for wrapper library updates. This follows standard practice: when providers release new models, SDK teams quickly expose them through version updates. The patch also updated three related dependencies (`@ai-sdk/provider`, `@ai-sdk/openai-compatible`, and `@ai-sdk/provider-utils`), suggesting infrastructure improvements supporting these new features.

## Practical Implications

For teams already using the Vercel AI SDK with XAI, the upgrade is straightforward. Video processing requires minimal code changes—the same function signatures accept video now, detected through content type or file extension. No authentication changes or new environment variables are needed.

The timing is strategic. Video processing has become table-stakes for AI applications. Whether you're building chatbots that analyze user-submitted videos, content management systems that understand video libraries, or creative tools leveraging video as reference material, direct SDK support reduces engineering overhead.

The Grok-4.5 model addition matters less dramatically but still meaningfully. XAI continuously improves their models; developers who've committed to using Grok benefit from accessing the latest version immediately. For those evaluating which provider to use, having current models available via a single SDK integration point becomes a small but meaningful advantage.

## What Happens Next

This patch release signals Vercel's commitment to tracking AI provider releases closely and exposing new capabilities quickly. Expect similar incremental updates as other providers (OpenAI, Anthropic, Google) release model updates or feature additions.

The video support feature may see future expansion—additional formats, streaming input for very large files, or batch processing capabilities could land in subsequent versions. For now, the implementation focuses on core functionality: reliable video transmission and processing through the established `inputReferences` interface.

Developers interested in these features should update their `@ai-sdk/xai` dependency to 3.0.106 or later. If you're building applications requiring video understanding or planning to standardize on Grok models, this update removes friction from your integration. For those still evaluating AI SDK providers, multi-modal input support (now including video) strengthens Vercel's position as a flexible, feature-complete option.
*This article does not contain affiliate links.*
