---
category: sdk_release
date: '2026-05-30'
generated_at: '2026-05-30T04:57:42.296395Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/anthropic-sdk-python
source_url: https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.105.0
template_type: explainer
title: anthropics/anthropic-sdk-python v0.105.0
word_count: 840
---

# Anthropic SDK Python v0.105.0: Enhanced Model Support and Fine-Grained Token Tracking

Anthropic has released version 0.105.0 of its Python SDK, bringing expanded model capabilities and improved observability features for developers building applications with Claude. The update introduces support for a new model variant, enhanced system prompt flexibility, and granular token usage reporting—changes that address common developer needs around model selection, conversation management, and cost tracking.

## TL;DR

- **Claude Opus 4.8 support**: New model variant now available through the SDK for applications requiring the latest capabilities
- **Mid-conversation system blocks**: System prompts can now be injected at any point in a conversation, not just at the beginning
- **Detailed token metrics**: Output token usage is now broken down by category for better cost visibility
- **Custom file size limits**: Developers can configure file upload constraints to match their infrastructure
- **Impact**: These features give developers more control over model behavior, better cost tracking, and greater flexibility in conversation design

## Background

Python SDK updates in the Anthropic ecosystem typically ship incrementally, with each release addressing specific use cases identified by the developer community. Token tracking has been an increasingly requested feature as organizations scale their Claude deployments—understanding exactly where tokens are consumed helps optimize costs and diagnose performance issues. Similarly, the ability to inject system instructions mid-conversation addresses a gap in conversational AI design, where initial system prompts may not cover all interaction patterns.

The introduction of new model variants like Claude Opus 4.8 reflects Anthropic's ongoing model development cycle, where improved versions of existing architectures are rolled out to SDK users shortly after release. File upload configuration, meanwhile, solves a practical infrastructure problem: different deployment environments have different constraints around payload size.

## How it works

### Claude Opus 4.8: The Latest Model Variant

The new claude-opus-4-8 model is now available as an option when initializing client calls. This follows Anthropic's naming convention where version numbers reflect incremental improvements to existing model families. Developers can select this model by specifying it in their API calls, similar to how they would choose between Claude 3.5 Sonnet or Haiku variants.

The availability of a new Opus variant matters for applications requiring maximum capability. Opus models serve as Anthropic's most powerful option, designed for complex reasoning tasks, code generation, and nuanced analysis. By making version 4.8 available in the SDK, Anthropic ensures that Python developers have immediate access to improvements without waiting for a separate SDK cycle.

### Mid-Conversation System Blocks

Previously, system prompts in Claude conversations were locked in at the beginning of an exchange. Version 0.105.0 removes this constraint by allowing system instructions to be injected at any point during a multi-turn conversation.

This capability unlocks several use cases. For instance, an application might want to adjust tone or instruction emphasis after detecting user confusion. A customer service bot could shift into escalation mode with different system guidance when sentiment analysis flags frustration. Educational applications could introduce new context or constraints as lessons progress.

Technically, mid-conversation system blocks work by allowing system role messages to appear anywhere in the message array, not just at index zero. The API backend processes these as context shifts that apply to subsequent model outputs without disrupting conversation coherence.

### Granular Token Usage Reporting

The addition of `usage.output_tokens_details` provides a breakdown of how output tokens are distributed across different categories—a significant improvement for cost analysis. Rather than receiving a single output token count, developers now see itemized usage that reveals how tokens are spent on different types of generation.

This granularity helps identify optimization opportunities. If detailed metrics show that a significant portion of tokens goes toward formatting or repeated explanations, developers can refine prompts to be more efficient. For organizations billing customers based on usage, detailed token reporting enables transparent, itemized invoicing.

### Custom File Size Caps

The ability to configure custom file size limits addresses deployment variability. Cloud environments, on-premises installations, and edge deployments often have different constraints around maximum request payload size. Rather than a fixed upper limit, developers can now tune this parameter to match their infrastructure.

This is particularly useful for applications processing documents or images. A developer running the SDK in a memory-constrained environment might set a lower cap, while another operating in a well-resourced data center could increase limits to handle larger batch operations.

## What happens next

As Anthropic continues developing Claude models and the SDK matures, expect ongoing refinements to token tracking—potentially including per-token pricing breakdowns or real-time usage monitoring. Mid-conversation system blocks may inspire higher-level abstractions in the SDK, such as built-in conversation state management that automatically applies system blocks based on conversation flow.

For developers currently using older SDK versions, upgrading to 0.105.0 is straightforward and backward-compatible. The new features are opt-in, meaning existing code continues to work without modification. However, teams managing significant Claude deployments should prioritize the token details feature for improved cost visibility.

The release also includes documentation improvements and internal refactoring (the managed-agents example was renamed from private-sandbox-worker to self-hosted-sandbox-worker), signaling Anthropic's focus on clearer terminology around deployment models.
*This article does not contain affiliate links.*
