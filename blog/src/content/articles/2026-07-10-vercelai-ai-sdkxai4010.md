---
category: sdk_release
date: '2026-07-10'
generated_at: '2026-07-10T05:02:03.393512Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:vercel/ai
source_url: https://github.com/vercel/ai/releases/tag/%40ai-sdk/xai%404.0.10
template_type: explainer
title: vercel/ai @ai-sdk/xai@4.0.10
word_count: 762
---

# Vercel AI SDK Adds Video Support and Grok 4.5 Model: What's New

Vercel has released version 4.0.10 of its @ai-sdk/xai package, introducing meaningful updates to its AI integration toolkit. The patch brings expanded media capabilities and support for xAI's latest language model, marking incremental but significant progress for developers building AI-powered applications.

## TL;DR

- **Video reference inputs**: The AI SDK now supports video files in addition to images for reference-based generation tasks, expanding creative possibilities
- **Grok 4.5 integration**: xAI's newest model is now available through the SDK, giving developers access to improved reasoning and capabilities
- **Dependency updates**: Supporting packages were bumped to ensure compatibility and stability across the ecosystem
- **Impact**: Developers can now build more sophisticated multimodal applications and leverage cutting-edge model capabilities without waiting for manual integrations

## Background

The Vercel AI SDK exists to simplify integration between applications and various AI providers. Rather than developers managing individual APIs, authentication, and model-specific configurations, the SDK provides a unified abstraction layer. This approach reduces friction and allows teams to switch providers or models with minimal code changes.

Video generation and processing represent an emerging frontier in generative AI. Previously, most AI toolkits focused on image generation or text, with video support lagging behind. As models become increasingly capable of understanding and generating video content, SDKs need to evolve to expose these capabilities. Similarly, xAI—the AI company founded by Elon Musk—has been iterating on its Grok model family, with each version bringing improvements to reasoning, context understanding, and response quality.

## How it works

### Multimodal reference inputs: Beyond images

The most significant change in this release extends the `inputReferences` parameter to accept video files alongside images. Previously, developers could pass image references to guide generation tasks—providing visual context for image-to-image transformation or other reference-based operations. This limitation meant developers couldn't leverage video context or temporal information.

Video reference inputs enable a new class of applications. A developer might use a video clip as reference material for generating new frames, maintaining consistency with the source video's style, lighting, or composition. This is particularly valuable for content creators working on visual consistency across projects or for building tools that extend or remix existing video content. The implementation appears to be handled through the `inputReferences` API, meaning developers won't need to learn entirely new interfaces—the SDK handles video processing transparently.

The supporting package updates (`@ai-sdk/provider@4.0.3` and `@ai-sdk/openai-compatible@3.0.7`) suggest this feature required refactoring how the SDK abstracts provider capabilities, ensuring video handling works consistently across different model providers.

### Grok 4.5: The newest reasoning engine

xAI's Grok model family has positioned itself as a competitive alternative to other large language models, with particular emphasis on reasoning capabilities and real-time information access. The addition of Grok 4.5 to the SDK makes this latest iteration immediately available to developers without requiring manual API configuration.

Model additions to the SDK typically indicate the model has reached sufficient maturity for production use and that xAI has committed to maintaining stable API support. Developers can now instantiate Grok 4.5 through familiar SDK methods, enabling it as an option alongside other providers like OpenAI, Anthropic, and others. This is particularly useful for teams evaluating multiple models or wanting to implement provider redundancy—if one service experiences issues, switching to Grok requires changing a single configuration value rather than rewriting integration logic.

### Dependency stability

The updates to `@ai-sdk/provider-utils@5.0.7` represent maintenance work to ensure the entire ecosystem remains coherent. As the core provider abstraction changes to support video, all dependent packages need compatible versions. This cascading update approach prevents situations where using the latest features causes conflicts with other SDK components—a common pain point in rapidly evolving toolkits.

## What happens next

These changes represent steady progress in expanding the Vercel AI SDK's capabilities. Video support will likely drive adoption in content creation and media industries, where reference-based generation is increasingly valuable. The Grok 4.5 addition continues the trend of rapid model iteration, with users gaining immediate access to improvements without waiting for manual SDK updates.

For developers currently using the SDK, upgrading carries minimal risk—patch versions typically introduce features without breaking changes. Teams working on multimodal applications or evaluating xAI as a provider should prioritize updating. Those still on older versions may want to plan an upgrade to access these capabilities.

The broader pattern suggests Vercel is maintaining tight integration with the AI model ecosystem, updating the SDK quickly as new capabilities emerge. This responsiveness to upstream changes positions the toolkit as a practical choice for teams that want access to cutting-edge models without managing provider integrations independently.
*This article does not contain affiliate links.*
