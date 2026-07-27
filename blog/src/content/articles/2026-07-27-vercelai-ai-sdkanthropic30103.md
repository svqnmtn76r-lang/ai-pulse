---
category: sdk_release
date: '2026-07-27'
generated_at: '2026-07-27T04:43:21.725330Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:vercel/ai
source_url: https://github.com/vercel/ai/releases/tag/%40ai-sdk/anthropic%403.0.103
template_type: explainer
title: vercel/ai @ai-sdk/anthropic@3.0.103
word_count: 816
---

# Anthropic SDK Update Fixes Token Counting for AI Reasoning: What Developers Need to Know

Vercel has released a patch update to its Anthropic integration within the AI SDK, addressing a critical issue in how token usage is tracked for Claude's extended thinking capabilities. The fix ensures that when Claude uses its reasoning features—a premium capability that allows the model to "think" through complex problems—these computational tokens are now properly categorized and reported to developers.

## TL;DR

- **Thinking tokens clarified**: Claude's reasoning process tokens are now correctly labeled as "reasoning token usage" instead of generic thinking tokens, improving transparency in API billing and performance monitoring
- **SDK accuracy improved**: The @ai-sdk/anthropic package (version 3.0.103) now provides accurate token accounting that aligns with Anthropic's official token classification system
- **Developer impact**: Teams using Claude's extended thinking features can now accurately track costs and optimize their prompting strategies based on correct usage metrics

## Background

Token counting has become increasingly important as large language models have grown more sophisticated. Every API call to models like Claude consumes tokens—discrete units of text that the model processes. Developers are charged based on token consumption, making accurate tracking essential for budgeting and cost optimization.

Claude's extended thinking feature, which allows the model to reason through complex problems before providing answers, introduced a new category of token usage. Unlike regular input and output tokens, "thinking tokens" or "reasoning tokens" represent the computational work happening during the model's internal reasoning phase. This reasoning capability is particularly valuable for complex analytical tasks, coding problems, and multi-step reasoning scenarios.

However, the integration between Vercel's AI SDK and Anthropic's API had a discrepancy in how these reasoning tokens were being reported. The SDK was categorizing them under a generic "thinking tokens" label rather than properly identifying them as "reasoning token usage"—the official terminology Anthropic uses in its billing and documentation.

## How it works

### Understanding Token Categories in Modern AI APIs

Modern language model APIs typically break down token usage into several categories. Standard tokens cover the model's input processing and output generation. However, extended thinking models like Claude add intermediate computational work that happens between receiving a prompt and generating a response.

This reasoning phase isn't wasted computation—it's valuable work that the model performs to improve answer quality. When Claude tackles a complex coding problem or performs detailed analysis, it can "think out loud" internally before crafting its response. This internal reasoning consumes tokens just like regular processing does, but it serves a different purpose in the pipeline.

Anthropic's API documentation specifies that these intermediate reasoning tokens should be reported separately as "reasoning token usage" to help developers understand the true computational cost of their requests. This categorization allows developers to see at a glance how much computation is being devoted to reasoning versus other tasks.

### The Fix in Context

The patch update corrects a mapping issue in how the SDK translates Anthropic's API response data into the token usage object that developers receive. Previously, when the Anthropic API returned information about tokens consumed during reasoning, the SDK was applying an incorrect label or placing them in the wrong category.

By updating the labeling mechanism, the patch ensures that when developers call Claude with extended thinking enabled, they receive accurate reporting that explicitly identifies reasoning tokens. This becomes crucial for several practical reasons: accurate cost tracking, understanding model behavior patterns, and optimizing which requests should use extended thinking versus standard processing.

The fix is minimal in scope—it's a patch update rather than a major version change—indicating this is a surgical correction to existing functionality rather than new capabilities being added. The change applies to the @ai-sdk/anthropic package specifically, which is Vercel's maintained wrapper around Anthropic's official API.

### Practical Implications for Development

For developers using Vercel's AI SDK with Claude models, this update means their token usage dashboards and monitoring systems will now show more accurate and detailed information. If you've been tracking token consumption in your applications, you'll now see proper categorization that distinguishes between reasoning work and standard processing.

This becomes particularly relevant for applications that intelligently route requests—some queries might benefit from Claude's extended thinking while others don't need it. With accurate token reporting, developers can analyze whether the additional reasoning tokens are worth the cost for particular types of requests.

## What happens next

The immediate action for teams using the Anthropic SDK is to update to version 3.0.103 or later to ensure accurate token tracking. This is especially important if you're using extended thinking features and relying on token metrics for billing, cost optimization, or performance analysis.

Going forward, this correction establishes a clearer foundation for how Vercel's AI SDK reports usage metrics from Anthropic's extended thinking capabilities. As Claude's reasoning abilities continue to evolve, having accurate token categorization from the start ensures developers can make informed decisions about when to employ these more computationally intensive features.
*This article does not contain affiliate links.*
