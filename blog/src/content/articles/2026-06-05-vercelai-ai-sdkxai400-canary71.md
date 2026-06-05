---
category: sdk_release
date: '2026-06-05'
generated_at: '2026-06-05T05:26:38.534343Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:vercel/ai
source_url: https://github.com/vercel/ai/releases/tag/%40ai-sdk/xai%404.0.0-canary.71
template_type: explainer
title: vercel/ai @ai-sdk/xai@4.0.0-canary.71
word_count: 891
---

# Vercel's AI SDK Adds Experimental Realtime Voice Support: What Developers Need to Know

Vercel's AI SDK has introduced experimental support for realtime voice conversation APIs across multiple AI providers, marking a significant expansion in the toolkit's capabilities for building interactive voice applications. The latest canary release brings standardized implementations for OpenAI, Google, and xAI's realtime services, enabling developers to build speech-to-speech applications that work in both server and browser environments.

## TL;DR

- **Realtime API abstraction**: The SDK now provides a normalized interface (`Experimental_RealtimeModelV4`) for accessing realtime voice capabilities across different providers, reducing vendor lock-in concerns
- **Multi-provider support**: OpenAI, Google, and xAI implementations are available through unified methods like `openai.experimental_realtime()`, simplifying provider switching
- **React integration**: A new `experimental_useRealtime` hook brings realtime voice conversations to React applications with message handling aligned with existing `useChat` patterns
- **Tool execution**: Built-in support for client-driven tool calling during voice conversations, including a helper function for defining session-specific tools
- **Impact**: Developers can now build sophisticated voice applications with automatic speech transcription, reducing friction in implementing multimodal AI experiences

## Background

Voice-based interfaces have become increasingly important as users expect natural language interactions with applications. However, integrating realtime voice APIs has traditionally required handling provider-specific implementations, authentication mechanisms, and event systems—creating friction for developers wanting to support multiple providers or migrate between them.

Previous approaches to voice integration typically involved point solutions: developers would implement OpenAI's Realtime API directly, then face significant refactoring if they wanted to switch to Google's equivalent service. This fragmentation meant voice capabilities remained a specialized domain rather than mainstream features in web applications.

The AI SDK's historical focus has been on text-based interactions through models like GPT and Claude. By introducing experimental realtime support, Vercel is acknowledging that voice is becoming a first-class interaction paradigm alongside text. This release represents an effort to democratize voice integration similarly to how the SDK simplified text-based AI integration.

## How it works

### Provider-agnostic realtime specification

At the foundation sits the `Experimental_RealtimeModelV4` specification within `@ai-sdk/provider`. This defines a standardized event system and factory pattern that abstracts away provider differences. Rather than developers learning distinct APIs for OpenAI's realtime model versus Google's equivalent, the SDK normalizes the experience through common event types and initialization patterns.

Each provider—OpenAI, Google, and xAI—implements this specification independently, meaning they handle authentication and API calls differently behind the scenes, but the interface developers interact with remains consistent. This approach mirrors successful patterns in the SDK's existing text model abstractions, where Claude and GPT models present unified interfaces despite underlying implementation differences.

### Token generation for secure server-side integration

Security is addressed through a `.getToken()` static method available on each provider's realtime implementation. This allows servers to generate ephemeral tokens that clients can use to establish realtime connections without exposing permanent API credentials. The pattern is crucial for production deployments where browsers or mobile clients shouldn't hold long-lived authentication tokens.

Developers call this method server-side—for instance, through a Next.js API route—and provide the ephemeral token to their client application, which then establishes the realtime connection. This separates the security boundary between credential management (server) and connection handling (client).

### React integration through hooks

The `experimental_useRealtime` hook brings realtime voice into React's component model. Unlike async text-based interactions that resolve once, realtime voice involves bidirectional streaming where both user and model are continuously exchanging audio and events. The hook manages this stateful connection lifecycle while returning data structures (`UIMessage[]`) that align with the familiar `useChat` hook.

This consistency matters: developers already working with `useChat` for text conversations can apply similar patterns to voice interactions. The hook handles the complexity of maintaining connection state, managing audio streams, and sequencing messages—concerns that would otherwise demand substantial custom logic.

### Tool execution during voice conversations

A critical capability for voice applications is enabling the AI to request tool execution during conversations. The release includes `experimental_getRealtimeToolDefinitions`, a helper that converts session-specific tool definitions into formats understood by each provider's realtime API. Additionally, hooks provide `onToolCall` and `addToolOutput` methods, allowing applications to respond when the AI requests a tool invocation—for example, asking the system to look up real-time flight information during a voice conversation.

### Automatic transcription support

The `inputAudioTranscription` session configuration enables providers that support it to transcribe spoken user input into text, which then appears in the message history. This bridges voice and text interfaces: users speak naturally while the application maintains a readable conversation transcript. Not all providers support this feature, so it's offered as optional configuration developers can enable when available.

## What happens next

This release remains experimental, meaning the API may change before reaching general availability. Developers interested in exploring realtime voice should begin testing with one of the three supported providers to provide feedback on usability and completeness.

For those building production voice applications today, these experimental features offer a preview of how voice will be integrated into the SDK's mainstream API surface. The multi-provider approach suggests Vercel intends voice to become as accessible and portable as text-based model access—a significant step toward voice becoming a standard capability rather than a specialized feature.

Documentation and examples will be essential as developers navigate this new territory. Given the SDK's focus on reducing boilerplate and abstracting provider differences, early feedback from practitioners will likely shape how realtime voice moves from experimental to stable within the broader AI SDK ecosystem.
*This article does not contain affiliate links.*
