---
category: sdk_release
date: '2026-06-05'
generated_at: '2026-06-05T05:26:20.801034Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:vercel/ai
source_url: https://github.com/vercel/ai/releases/tag/ai%407.0.0-canary.165
template_type: explainer
title: vercel/ai ai@7.0.0-canary.165
word_count: 883
---

# Vercel's AI SDK Gains Real-Time Voice Conversation Support: What Developers Need to Know

Vercel has released a significant expansion to its AI SDK with experimental support for real-time voice APIs, marking a major step toward making speech-based AI interactions a first-class feature in modern web applications. The canary release (version 7.0.0-canary.165) introduces comprehensive tooling for building voice-enabled applications that work seamlessly across server and browser environments.

## TL;DR

- **Unified Real-Time Spec**: The SDK now defines a standardized `Experimental_RealtimeModelV4` specification that normalizes how different AI providers handle real-time voice conversations
- **Multi-Provider Support**: OpenAI, Google, and xAI have all received native real-time implementations within the SDK, with both server-side token generation and browser-based functionality
- **React Integration**: A new `experimental_useRealtime` hook brings voice conversations into React applications with familiar patterns similar to existing `useChat` functionality
- **Tool Support**: Developers can now define and execute tools within real-time voice sessions, enabling voice-driven function calls and dynamic interactions
- **Impact**: This democratizes voice AI development, allowing developers to build sophisticated speech-to-speech applications without managing provider-specific implementations

## Background

Real-time voice APIs have emerged as one of the most demanded features in modern AI development, yet implementation has remained fragmented. Each provider—whether OpenAI, Google, or others—offered proprietary APIs with different event models, authentication mechanisms, and connection paradigms. Developers building voice applications faced a choice: either lock into a single provider or build complex abstraction layers to support multiple backends.

The Vercel AI SDK has positioned itself as a provider-agnostic layer, abstracting away these differences. This release extends that philosophy into the real-time domain, recognizing that voice interactions represent a fundamental shift in how users engage with AI applications. Previous releases focused primarily on text-based completions and streaming responses. Real-time voice conversations require a different architectural approach—maintaining persistent connections, handling audio streams bidirectionally, and managing state across multiple message types.

## How it works

### Standardized Real-Time Architecture

At the core of this release is the `Experimental_RealtimeModelV4` specification, a normalized interface that sits atop provider-specific implementations. This specification defines a common language for real-time interactions, including how events are structured, what message types exist, and how the system should handle various scenarios like user interruptions, tool calls, and session management.

Rather than forcing developers to learn three different APIs, the SDK translates this standardized spec into provider-specific protocols. When you call `openai.experimental_realtime()`, `google.experimental_realtime()`, or `xai.experimental_realtime()`, you're receiving an implementation that adheres to the unified spec while handling all the provider-specific complexity behind the scenes.

This approach mirrors how the SDK handles text-based models—the same conceptual interface works across different providers, but each provider implements it according to their architecture.

### Authentication and Token Generation

Real-time voice APIs typically require ephemeral tokens for security, especially in browser environments where you cannot safely expose long-lived API credentials. The SDK addresses this with a `.getToken()` static method on each provider, enabling server-side token generation.

The typical flow involves your backend server generating a short-lived token that a browser client then uses to establish a direct connection to the real-time API. This maintains security boundaries while enabling responsive voice interactions without unnecessary server intermediaries. The token generation happens on your infrastructure, giving you control over rate limiting, user authentication, and access control.

### React Integration and Message Handling

For React developers, the new `experimental_useRealtime` hook provides a familiar abstraction. It returns `UIMessage[]` objects, maintaining consistency with the existing `useChat` hook's message format. This means developers can leverage existing patterns and tooling they've already built around chat applications.

The hook includes support for `onToolCall` callbacks and `addToolOutput` methods, enabling client-driven tool execution. When the voice model decides it needs to call a tool—say, fetching weather data or updating a calendar—it communicates this through the standardized event system. Your client code can respond by executing the tool and feeding the results back into the conversation, all within the same real-time stream.

### Tool Definitions and Execution

The SDK provides an `experimental_getRealtimeToolDefinitions` helper that converts your standard tool definitions into the format expected by real-time sessions. Tools maintain feature parity with text-based conversations, meaning you can design once and deploy across multiple modalities.

This is particularly powerful for voice applications because it enables users to accomplish complex tasks through natural speech. Instead of navigating menus or typing queries, users can simply say "book me a meeting for Thursday at 2 PM" and the voice system handles tool invocation, parameter extraction, and execution coordination.

### Audio Transcription Integration

An often-overlooked feature is the `inputAudioTranscription` session configuration, which automatically surfaces transcribed user audio as messages in the conversation. When supported by the provider, users see both what they said (transcribed text) and the AI's understanding, improving transparency and enabling conversation review.

## What happens next

This experimental release sets the stage for real-time voice becoming a standard feature in AI applications. As the SDK matures the specification and providers optimize their implementations, we should expect broader adoption in customer-facing applications. The combination of unified APIs, React integration, and tool support removes major barriers to entry.

Developers interested in exploring this should start with the React hook for browser-based implementations, ensure their server-side infrastructure can generate ephemeral tokens securely, and consider how tool execution fits their application's architecture. The experimental label indicates this will evolve, so expect refinements in upcoming releases as real-world usage patterns emerge.
*This article does not contain affiliate links.*
