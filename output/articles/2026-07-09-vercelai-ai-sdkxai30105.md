---
category: sdk_release
date: '2026-07-09'
generated_at: '2026-07-09T05:02:31.713886Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:vercel/ai
source_url: https://github.com/vercel/ai/releases/tag/%40ai-sdk/xai%403.0.105
template_type: explainer
title: vercel/ai @ai-sdk/xai@3.0.105
word_count: 710
---

# Vercel AI SDK Adds Fine-Grained Image Processing Control with imageDetail Provider Option

Vercel's AI SDK has released an update to its XAI integration that introduces more granular control over how images are processed when sent to language models. The new `imageDetail` provider option allows developers to specify image resolution handling at the file part level, addressing a common challenge in multimodal AI applications where image quality and API costs must be balanced.

## TL;DR

- **imageDetail provider option**: A new configuration parameter that lets developers control image processing resolution on a per-image basis within AI SDK requests
- **File part-level control**: The option applies to individual image file parts rather than globally, offering fine-grained flexibility in mixed-content prompts
- **Impact**: Developers can now optimize inference costs and latency by specifying how images should be downsampled or processed, particularly useful for applications handling multiple images with varying importance levels

## Background

Language models that support vision capabilities typically accept images in multiple formats and resolutions. Most multimodal APIs, including those for vision-enabled LLMs, offer options to control how images are processed before inference. These options typically include settings like "low," "high," or "auto" for image detail levels.

Previously, developers using Vercel's AI SDK with XAI providers often had limited options for controlling this behavior at a granular level. If an API supported detail settings, the configuration might be applied globally across all images in a request, or developers had to work around the limitation through preprocessing.

This patch addresses that limitation by exposing the underlying `imageDetail` capability as a configurable provider option, giving developers the flexibility to treat different images differently within the same request.

## How it works

### Understanding Image Detail Levels

Vision-capable language models typically process images through several stages: receiving the input, potentially resizing or compressing it, encoding it into tokens or embeddings, and finally using those representations in the model's inference pipeline. The "detail" level controls how much of this processing happens.

Lower detail levels reduce the number of tokens consumed and processing time, which directly impacts both latency and cost. High detail levels preserve more visual information, which is beneficial for tasks requiring fine-grained image understanding like reading small text, identifying subtle visual elements, or analyzing detailed diagrams.

The XAI integration now allows developers to specify which approach they want for each image independently. This is particularly valuable in scenarios where a single prompt contains multiple images with different informational requirements.

### Implementing imageDetail in File Parts

In Vercel's AI SDK, images are typically included as part of the message structure using file parts. The new update allows developers to specify `imageDetail` as a property on individual image file parts. This means you can set one image to use "high" detail while another uses "low," all within the same API call.

This pattern aligns with how other provider-specific options are handled in the SDK's architecture. Rather than creating a new top-level configuration section, the option integrates into the existing file part structure, maintaining consistency with the SDK's design patterns.

### Practical implications

For applications that process multiple images in a single request—such as document analysis systems, visual search interfaces, or multimodal AI agents—this feature enables significant optimization opportunities. A document processing pipeline might use high detail for pages containing tables or fine print while using low detail for cover pages or supplementary images.

The implementation also maintains backward compatibility. Existing code without explicit `imageDetail` specifications will continue to function, likely using the provider's default behavior or any previously set global configuration.

## What happens next

This patch represents incremental progress in Vercel's effort to expose granular provider capabilities through its unified AI SDK interface. As language models continue evolving with increasingly sophisticated vision capabilities, we can expect to see similar fine-grained configuration options for other image processing parameters.

For developers currently working with multimodal applications, testing this option on representative workloads can help identify optimization opportunities—particularly in cost-sensitive or latency-constrained applications. The ability to tune image processing per-image provides another lever for balancing quality and performance in production systems.

To learn more about implementing this feature, developers should consult the official Vercel AI SDK documentation and the XAI provider integration guide, which will include examples of setting `imageDetail` on file parts within request payloads.
*This article does not contain affiliate links.*
