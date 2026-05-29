---
category: sdk_release
date: '2026-05-29'
generated_at: '2026-05-29T05:19:25.434511Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/anthropic-sdk-python
source_url: https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.105.0
template_type: explainer
title: anthropics/anthropic-sdk-python v0.105.0
word_count: 912
---

# Anthropic Python SDK v0.105.0: New Claude Model and Advanced System Prompt Controls

Anthropic has released version 0.105.0 of its Python SDK, introducing support for the latest Claude Opus 4 variant alongside significant enhancements to conversation management and token tracking capabilities. This update expands developer flexibility when building AI applications while providing more granular control over how system instructions are applied during multi-turn conversations.

## TL;DR

- **Claude Opus 4-8 Support**: Access to Anthropic's newest large language model variant with enhanced capabilities
- **Mid-Conversation System Blocks**: Ability to inject or modify system prompts mid-conversation, enabling dynamic instruction updates without restarting dialogue threads
- **Detailed Token Metrics**: New `usage.output_tokens_details` tracking for granular visibility into token consumption patterns
- **Custom File Size Caps**: Developers can now configure maximum file upload sizes to align with application requirements
- **Impact**: Enhanced control over conversation flows and token budgeting makes the SDK more suitable for production applications requiring fine-grained cost management and complex multi-step interactions

## Background

The Anthropic Python SDK serves as the primary interface for developers integrating Claude into Python applications. Since its initial releases, the SDK has evolved to match Claude's expanding capabilities, from basic chat interfaces to complex agent systems. Previous versions established foundational conversation management, file handling, and token counting features.

The mid-conversation system prompt limitation represented a notable constraint for developers building sophisticated AI systems. Previously, if developers wanted to change system instructions mid-conversation, they would need to restart the dialogue entirely, losing conversation history and context. This forced developers into architectural workarounds when building applications requiring dynamic instruction changes—such as role-shifting chatbots, progressive instruction refinement, or conditional system behaviors based on conversation state.

Similarly, token tracking had been somewhat opaque. While developers could see total token usage, understanding exactly where tokens were consumed (particularly in output generation) was difficult, making cost optimization and budget forecasting challenging for high-volume applications.

## How it Works

### Claude Opus 4-8: The Latest Generation

The release introduces support for `claude-opus-4-8`, Anthropic's newest flagship model in the Opus line. This represents the continuation of Anthropic's model evolution strategy, which has progressively expanded Claude's capabilities while addressing performance and cost optimization. The Opus 4-8 designation suggests further refinement over previous iterations, likely incorporating improvements in reasoning, coding, and multi-domain understanding.

Developers can access this model by specifying it in their model parameter when making API calls through the SDK. The model integrates seamlessly with existing SDK features, meaning developers upgrading to v0.105.0 gain immediate access to Opus 4-8's capabilities without requiring architectural changes to their applications.

### Mid-Conversation System Blocks: Dynamic Instruction Control

Perhaps the most significant feature addition is support for mid-conversation system blocks. This allows developers to modify, add, or replace system prompts while maintaining conversation continuity. In practical terms, this means a conversation thread no longer needs to restart when system instructions must change.

Consider a customer support chatbot that begins in a general-assistance mode but needs to shift to a specialized billing-inquiry mode based on conversation content. Previously, this would require terminating the conversation and starting fresh. With mid-conversation system blocks, the bot can smoothly transition by injecting new system instructions mid-stream, preserving all prior context and messages.

This capability is particularly valuable for adaptive AI systems that need to dynamically adjust behavior based on conversation progression, user preferences, or detected conversation type. Multi-stage reasoning systems that refine their approach iteratively can now update their instructions between stages without context loss.

### Output Token Details: Granular Usage Tracking

The new `usage.output_tokens_details` field provides developers with detailed breakdowns of how tokens are consumed in model outputs. Rather than receiving a single output token count, developers can now see which components consumed tokens—such as text generation versus tool use versus reasoning steps.

For organizations optimizing API costs or managing token budgets across multiple applications, this granularity is invaluable. Teams can identify which features or conversation patterns consume disproportionate tokens, then optimize accordingly. A development team might discover that certain reasoning patterns generate extensive tokens and adjust prompting strategies to reduce consumption.

### Custom File Size Caps: Flexible Upload Management

The ability to configure custom file size caps provides developers with greater control over file handling constraints. Different applications have different requirements—a lightweight chatbot might enforce small file sizes to prevent abuse, while a research application might need to process larger documents.

Rather than accepting Anthropic's default size limits, developers can now set their own caps aligned with their application's resource constraints, security policies, and use cases. This prevents unexpected upload rejections and enables developers to design file handling strategies specific to their needs.

## What Happens Next

This release positions the Python SDK for more sophisticated, production-grade applications. The combination of dynamic system prompts, detailed token tracking, and model expansion creates an environment where developers can build complex, cost-optimized AI systems with greater visibility into their behavior.

Developers currently on earlier SDK versions should plan migration paths, particularly those building multi-turn applications that would benefit from mid-conversation instruction changes. The detailed token metrics will likely influence cost management strategies for production deployments.

Organizations using Claude should evaluate whether the Opus 4-8 model aligns with their performance and cost requirements, especially given the potential efficiency improvements in newer model versions. As with all model upgrades, testing compatibility with existing prompts and applications is recommended before production deployment.

For developers interested in deeper integration capabilities and custom configurations, reviewing the full changelog and Anthropic's documentation will provide additional context on all modifications included in this release.
*This article does not contain affiliate links.*
