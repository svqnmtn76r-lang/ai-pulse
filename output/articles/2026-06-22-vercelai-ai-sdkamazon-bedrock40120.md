---
category: sdk_release
date: '2026-06-22'
generated_at: '2026-06-22T06:36:38.632557Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:vercel/ai
source_url: https://github.com/vercel/ai/releases/tag/%40ai-sdk/amazon-bedrock%404.0.120
template_type: explainer
title: vercel/ai @ai-sdk/amazon-bedrock@4.0.120
word_count: 806
---

# Vercel AI SDK Fixes Claude Bedrock Integration: What This Patch Changes

Vercel has released version 4.0.120 of its Amazon Bedrock integration for the AI SDK, addressing a compatibility issue that was causing problems when using Claude Opus models on AWS's foundation model service. The patch resolves a technical mismatch between how the AI SDK was formatting tool specifications and how newer Claude models validate those specifications through Bedrock's Messages API.

## TL;DR

- **Tool specification validation**: Claude Opus 4.7 and 4.8 models reject the `strict` parameter in tool definitions, even though other Claude versions support it
- **Bedrock-specific fix**: This patch removes the `strict` field specifically for these newer Opus variants when they're accessed through AWS Bedrock
- **Broader SDK updates**: The release also pulls in dependency updates from the OpenAI SDK to maintain consistency across providers
- **Impact**: Developers using Claude Opus on Bedrock can now reliably invoke tool-calling workflows without encountering validation errors

## Background

The AI SDK is Vercel's unified interface for building with large language models across different providers—OpenAI, Anthropic, Google, and others. One of its key features is tool calling, where developers define functions or tools that an AI model can invoke to retrieve data, perform calculations, or take actions in external systems.

The `strict` parameter in tool specifications is part of the structured outputs ecosystem. This parameter tells a model to strictly adhere to the provided schema definition when generating tool calls, reducing the chance of malformed outputs. However, different model providers and even different versions of the same model line implement these specifications differently.

Claude Opus represents Anthropic's most capable model family, with version increments indicating improvements and changes to the underlying implementation. When AWS Bedrock added support for Claude Opus 4.7 and later versions, these newer iterations came with stricter validation in their Messages API endpoint—the interface through which developers send requests and receive responses.

The problem emerged when developers attempted to use the AI SDK's tool-calling features with these specific Claude versions through Bedrock. The SDK was including the `strict` field in tool definitions, but Bedrock's implementation of Claude Opus 4.7 and 4.8 didn't recognize or accept this parameter, causing request validation failures.

## How it works

### Understanding the Tool Specification Layer

Tool calling in language models works through a defined specification format. When a developer wants an AI model to use a tool, they provide a schema that describes what the tool does, what inputs it accepts, and what those inputs should look like. The `strict` parameter is an optional modifier within this schema that strengthens validation requirements.

Different inference endpoints interpret these specifications differently. OpenAI's API has one implementation, Anthropic's direct API has another, and when Anthropic's models run through AWS Bedrock's wrapper layer, there's a third interpretation. The AI SDK needs to account for these variations by adapting which parameters it includes depending on the specific provider and model being used.

### The Provider-Specific Fix

This patch implements conditional logic that detects when a request targets Claude Opus 4.7 or 4.8 through Bedrock specifically. When these conditions are met, the SDK strips out the `strict` parameter before constructing the API request. This is a surgical fix—it only affects these two specific model versions in the Bedrock context, leaving the parameter intact for other models or deployment methods.

Other Claude versions, whether accessed directly through Anthropic's API or through Bedrock, continue to include the `strict` parameter as normal. This targeted approach minimizes the risk of unintended side effects while solving the immediate problem. The fix recognizes that Bedrock's Messages API implementation for these newer Opus models has validation rules that diverge from how the models behave elsewhere.

### Dependency Synchronization

The patch also includes an update to the OpenAI SDK integration (bumping it to version 3.0.74). While this might seem unrelated to a Bedrock fix, maintaining synchronized dependency versions across different provider integrations helps prevent subtle incompatibilities and ensures consistent behavior patterns. The specific changes in that OpenAI update likely involve similar API compatibility adjustments or feature parity improvements.

## What happens next

This fix removes a blocker for teams building production systems with Claude Opus on AWS Bedrock who rely on tool-calling capabilities. Tool calling is increasingly central to AI application development—it's how models fetch real-time data, make business decisions, and trigger workflows.

Developers currently encountering validation errors when deploying tool-using applications with Claude Opus 4.7 or 4.8 on Bedrock should update to this version. The fix requires no code changes on their end; the AI SDK handles the adjustment transparently.

For longer-term compatibility, this patch highlights the ongoing fragmentation in how different inference endpoints implement the same underlying model. As the AI landscape matures, standardization efforts may reduce these kinds of provider-specific workarounds, but for now, framework-level abstraction layers like the AI SDK play a crucial role in managing these variations.
*This article does not contain affiliate links.*
