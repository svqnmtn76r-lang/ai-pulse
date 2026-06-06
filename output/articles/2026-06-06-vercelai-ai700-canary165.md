---
category: sdk_release
date: '2026-06-06'
generated_at: '2026-06-06T05:01:07.270351Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:vercel/ai
source_url: https://github.com/vercel/ai/releases/tag/ai%407.0.0-canary.165
template_type: explainer
title: vercel/ai ai@7.0.0-canary.165
word_count: 816
---

# Vercel AI SDK 7.0 Adds Real-Time Voice Conversation Support: What You Need to Know

Vercel has released a new canary version of its AI SDK with experimental support for real-time voice conversations. This update introduces first-class integrations with speech-to-speech APIs from major providers like OpenAI, Google, and xAI, enabling developers to build applications that can process and respond to voice input with minimal latency.

## TL;DR

- **Real-time voice APIs**: The SDK now provides normalized abstractions for speech conversation handling across multiple providers, reducing integration complexity
- **Multi-provider support**: OpenAI, Google, and xAI all have experimental real-time implementations, with consistent APIs across platforms
- **Browser and server compatibility**: Real-time functionality works in both frontend and backend environments, with server-side token generation for security
- **Tool calling in conversations**: The SDK includes helpers for integrating tool definitions and executing client-driven tool calls within voice sessions
- **React integration**: A new `experimental_useRealtime` hook provides voice conversation state management similar to existing `useChat`

## Background

Real-time voice interaction has emerged as a critical capability for modern AI applications. Previously, developers building voice-enabled features had to directly manage provider-specific APIs, handle event normalization, and build custom UI state management. This fragmentation meant duplicating logic across different provider implementations and maintaining separate code paths for voice versus text conversations.

The AI SDK has historically abstracted away provider differences for text-based interactions through normalized interfaces. This update extends that philosophy to voice conversations, allowing developers to write provider-agnostic code and switch between implementations without significant refactoring.

## How it works

### The Real-time Model Specification

At the foundation, Vercel has defined `Experimental_RealtimeModelV4`—a standardized specification for real-time voice models within the `@ai-sdk/provider` package. This spec establishes a consistent event model and interface that all participating providers implement.

Rather than developers learning the unique event types and data structures of each provider's WebSocket protocol, the SDK normalizes these into a unified format. This factory pattern approach means OpenAI's realtime events, Google's voice API events, and xAI's implementations all flow through the same developer interface, significantly reducing cognitive load and code duplication.

### Provider-Specific Implementation

Each major provider—OpenAI, Google, and xAI—now includes experimental real-time methods accessible directly from their provider instances. Developers can instantiate a real-time connection with `openai.experimental_realtime()` or equivalent calls for other providers. Importantly, these methods work identically whether called from Node.js server contexts or browser environments, making it viable to handle voice sessions anywhere in a full-stack application.

A critical security consideration emerges here: managing authentication tokens for long-lived WebSocket connections. The SDK addresses this with a static `.getToken()` method on each provider that creates ephemeral tokens server-side. This pattern prevents exposing permanent API keys to the browser while still enabling client-side voice sessions—the browser receives a short-lived token from your backend, uses it to establish the real-time connection, and the token expires after use.

### Tool Integration and State Management

The canary release includes `experimental_getRealtimeToolDefinitions`, a helper for serializing tool definitions in the format expected by provider session configurations. This enables voice assistants to call functions, matching capabilities available in text-based conversations.

On the React side, `experimental_useRealtime` provides a hook that manages voice conversation state, returning `UIMessage[]` data structures aligned with the existing `useChat` hook. This consistency reduces friction for developers already familiar with the SDK's chat abstractions. The hook exposes `onToolCall` callbacks and `addToolOutput` methods, enabling applications to intercept tool invocations, execute them client-side, and feed results back into the conversation.

An additional refinement: when providers support it, the `inputAudioTranscription` session configuration option displays transcribed versions of user audio messages within the conversation history. This improves UX by showing users what the system heard, rather than leaving voice input opaque.

## Practical Implications

This release democratizes voice capabilities for JavaScript developers. Previously, implementing speech-to-speech conversations required deep provider-specific knowledge or building custom abstraction layers. With normalized APIs, developers can prototype voice features quickly and experiment with multiple providers to find the best fit for latency, accuracy, or cost requirements.

The alignment between voice and text APIs—through consistent hook signatures and message formats—also means teams can more easily add voice as a channel to existing chat applications. Feature parity becomes more achievable when the underlying abstractions mirror each other.

The experimental status is important to note: these APIs will likely evolve before stabilization. Developers using these features should anticipate minor breaking changes and stay engaged with the SDK's releases during this phase.

## What happens next

Real-time voice support will likely become a stable feature in upcoming SDK versions as feedback from early adopters shapes refinements. Watch for expansions to additional providers, improved tool-calling semantics, and potentially native mobile support. The SDK's approach here—normalizing across providers while maintaining flexibility—establishes a pattern likely to extend to other emerging AI capabilities.

Developers interested in experimenting should review the Vercel AI SDK documentation and provider-specific real-time API references to understand token management, connection lifecycle, and tool definition syntax specific to their chosen provider.
*This article does not contain affiliate links.*
