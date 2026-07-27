---
category: sdk_release
date: '2026-07-27'
generated_at: '2026-07-27T04:43:07.629967Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:vercel/ai
source_url: https://github.com/vercel/ai/releases/tag/%40ai-sdk/anthropic%404.0.21
template_type: explainer
title: vercel/ai @ai-sdk/anthropic@4.0.21
word_count: 876
---

# Anthropic SDK Update Fixes Token Counting for AI Reasoning: What You Need to Know

Vercel's AI SDK has released a patch update to its Anthropic integration that addresses how the library reports token usage when using Claude's extended thinking capabilities. Version 4.0.21 of @ai-sdk/anthropic corrects a measurement issue where tokens consumed by the model's internal reasoning process were being miscategorized in usage reports.

This seemingly small fix has practical implications for developers building AI applications with Claude, particularly those leveraging the model's ability to think through complex problems before generating responses.

## TL;DR

- **Thinking tokens vs. reasoning tokens**: Claude's extended thinking feature consumes tokens during an internal reasoning phase that should be tracked separately from standard input/output tokens
- **Measurement correction**: The SDK was previously reporting these "thinking" tokens using the wrong category name, potentially causing confusion in cost tracking and usage monitoring
- **Impact**: Developers using Claude's reasoning features will now see accurate token usage reports, making it easier to understand costs and optimize API calls

## Background

Anthropic's Claude models introduced extended thinking as a capability that allows the AI to work through problems internally before responding. This internal deliberation consumes tokens—the basic units of text that language models process—but these tokens represent computational work happening "behind the scenes" rather than visible input or output text.

The Vercel AI SDK serves as a bridge between developer applications and various AI model providers, including Anthropic's Claude. It abstracts away provider-specific details while offering a unified interface for common operations like making API calls and tracking usage metrics.

Token counting is more than a technical detail—it directly impacts billing. Major AI providers charge based on token consumption, often with different rates for input tokens, output tokens, and in Claude's case, tokens used during the reasoning process. Accurate categorization ensures developers understand their actual costs and can make informed decisions about which models and features to use.

When extended thinking tokens weren't being reported correctly, developers couldn't accurately track expenses or optimize their usage patterns. The fix ensures that the reasoning tokens—the tokens consumed during Claude's thinking phase—are properly labeled in the usage metrics returned to the application.

## How it works

### Understanding Token Categories in AI Pricing

Modern language models break down text into tokens, with typical patterns showing that one token roughly equals four characters of English text. Different providers organize token counts differently. OpenAI separates prompt tokens from completion tokens. Anthropic's Claude, particularly with extended thinking enabled, introduces a third category: tokens consumed during the reasoning phase.

When you enable extended thinking on Claude, the model dedicates computational resources to working through a problem before formulating its response. These internal reasoning steps consume tokens, but they're distinct from the tokens in your actual prompt or the model's final output. This separation matters because reasoning tokens represent pure computation cost without corresponding visible text in the response.

### The Reporting Issue

The SDK was treating these reasoning tokens as a different metric than how Anthropic's API actually reported them. When developers called the API through the SDK and checked the token usage metrics, they would see the data labeled differently than what Anthropic's documentation indicated. This created a disconnect between what the underlying API reported and what developers saw in their application logs and monitoring systems.

The fix standardizes the terminology: thinking tokens—what the SDK was calling them—are now correctly reported as reasoning tokens, matching Anthropic's API documentation and making it easier for developers to correlate usage data across their systems.

### Practical Implications for Usage Tracking

For developers integrating Claude with extended thinking into their applications, this fix simplifies billing reconciliation. When you review your Anthropic bill or analyze token consumption patterns, the metrics from the SDK will now align precisely with what appears in your API dashboard. 

If you're monitoring costs in real-time or setting up alerts for token usage spikes, the corrected reporting ensures your systems respond to accurate data. Teams building multi-model AI applications will also benefit from consistent terminology—they can now document and discuss token usage for Claude using the same language across their codebase and external documentation.

### Implementation Details

The change was implemented through commit e29788d in the repository, a targeted fix that touches the token usage reporting logic without affecting the underlying API integration or other functionality. Developers using version 4.0.21 or later will automatically benefit from the correction, though existing applications will continue to function without modification—only the reported metrics change.

## What happens next

For most developers, this update requires no action beyond upgrading to the latest version when convenient. However, if you've built custom billing or cost-tracking systems that parse token usage data from the SDK, you may want to review how you're handling the reasoning token field to ensure consistency with the new naming convention.

Teams actively using Claude's extended thinking feature should prioritize this update to ensure their cost analysis tools reflect accurate data. For those considering whether extended thinking makes sense for their use case, this fix confirms that token usage will be transparently reported, supporting better decision-making around implementation.

This patch exemplifies how SDK maintenance work—often invisible but important—enables developers to build production systems with confidence. Accurate metrics provide the visibility needed to optimize AI applications effectively.
*This article does not contain affiliate links.*
