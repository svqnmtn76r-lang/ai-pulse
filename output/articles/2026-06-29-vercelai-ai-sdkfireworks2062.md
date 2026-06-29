---
category: sdk_release
date: '2026-06-29'
generated_at: '2026-06-29T01:53:35.783234Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:vercel/ai
source_url: https://github.com/vercel/ai/releases/tag/%40ai-sdk/fireworks%402.0.62
template_type: explainer
title: vercel/ai @ai-sdk/fireworks@2.0.62
word_count: 682
---

# Fireworks AI Integration Gets Granular Control with Service Tier Option

Vercel's AI SDK has rolled out an incremental update to its Fireworks provider integration, introducing the ability to specify service tier configurations at the provider level. The patch release (v2.0.62) addresses a gap in how developers interact with Fireworks' infrastructure options, giving them more fine-grained control over model deployment and resource allocation.

## TL;DR

- **Service Tier Option**: Developers can now specify a `serviceTier` parameter when configuring Fireworks chat models through the AI SDK
- **Provider-Level Configuration**: This setting is applied at the provider initialization stage, allowing consistent tier selection across multiple model calls
- **Impact**: Teams using Fireworks can optimize for performance, cost, or resource availability by selecting appropriate service tiers without modifying individual requests

## Background

Fireworks.ai, an inference platform specializing in open-source model deployment, offers multiple service tier options that allow developers to balance between performance characteristics, cost structures, and resource availability. Different tiers can provide varying levels of throughput, latency guarantees, and feature access.

The Vercel AI SDK serves as a unified interface for integrating multiple AI model providers—including OpenAI, Anthropic, Cohere, and others—into applications. Before this update, while the SDK supported Fireworks integration, it lacked a mechanism to configure service tier preferences at the provider level. This meant developers either had to work with Fireworks' default tier configuration or manage tier selection outside the SDK's abstraction layer.

The addition of this configuration option reflects the SDK's ongoing effort to expose provider-specific capabilities that matter to production deployments while maintaining a consistent API surface.

## How it works

### Understanding Service Tiers in Fireworks

Fireworks offers different service tier options that cater to different use cases and requirements. A service tier typically defines the resource class and performance characteristics of the infrastructure running your model inference. By allowing developers to specify a tier during provider initialization, the SDK enables them to make infrastructure-level decisions upfront rather than managing them reactively.

This approach aligns with how other AI platforms expose infrastructure choices—think instance types in cloud providers or model variants in different model families. Rather than treating service tier as an implementation detail, the SDK now elevates it to a first-class configuration option.

### Implementation Pattern

When initializing the Fireworks provider in the AI SDK, developers can now pass a `serviceTier` parameter alongside other configuration options. This parameter becomes part of the provider's baseline settings and applies to subsequent chat model operations unless overridden at a lower level. The pattern mirrors how other provider-specific settings work within the SDK ecosystem.

```
const provider = fireworks({
  serviceTier: "tier-name"
})
```

This declarative approach means teams can create different provider instances for different use cases—perhaps a high-performance tier for latency-sensitive operations and an economical tier for batch processing—and switch between them by instantiating different provider objects.

### Why This Matters for Production Deployments

Service tier selection is rarely a one-size-fits-all decision. Applications handling real-time user interactions might prioritize low-latency tiers, while background jobs processing large datasets might favor throughput or cost optimization. By exposing this choice within the SDK, developers avoid the friction of managing Fireworks configuration outside their application code.

This update represents a small but meaningful expansion of the SDK's capability surface. Rather than requiring developers to drop down to direct API calls for tier-specific behavior, they can stay within the abstraction layer that Vercel's SDK provides, improving code cohesion and maintainability.

## What happens next

This patch is immediately available through npm for projects using the `@ai-sdk/fireworks` package. Teams currently integrating Fireworks through the Vercel AI SDK can adopt the `serviceTier` option at their own pace—it's additive and doesn't affect existing configurations.

For developers evaluating Fireworks or comparing inference providers, this addition demonstrates how the Vercel AI SDK continues to deepen its integrations with model providers, enabling more sophisticated deployment patterns without breaking compatibility.

To implement this in your project, check the official Vercel AI documentation for Fireworks integration and consult Fireworks' own tier documentation to understand which tier options are available and which suits your use case. The combination of these resources will guide optimal configuration.
*This article does not contain affiliate links.*
