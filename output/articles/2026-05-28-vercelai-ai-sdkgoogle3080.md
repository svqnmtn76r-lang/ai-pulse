---
category: sdk_release
date: '2026-05-28'
generated_at: '2026-05-28T05:39:08.693014Z'
generated_by: claude-haiku-4-5-2026-05-28
importance_score: 80
products: []
source_name: github:vercel/ai
source_url: https://github.com/vercel/ai/releases/tag/%40ai-sdk/google%403.0.80
template_type: explainer
title: vercel/ai @ai-sdk/google@3.0.80
word_count: 763
---

# Vercel AI SDK Fixes Gemini 3 Tool-Call Serialization Issues: What Developers Need to Know

Vercel has released version 3.0.80 of its Google AI provider module, addressing a critical compatibility issue that emerges when developers persist or serialize conversation messages with Gemini 3 models. The fix automatically handles missing thought signatures—a new security requirement in Gemini 3—preventing HTTP 400 errors that previously broke application workflows.

## TL;DR

- **Gemini 3 signature requirement**: The latest Gemini models require a `thoughtSignature` field in function call requests, rejecting calls without it
- **Serialization problem**: When applications save and reload conversations (common in databases, server routes, or synthetic workflows), custom metadata like signatures often gets dropped
- **Automatic mitigation**: The updated provider detects missing signatures and injects a documented sentinel value (`skip_thought_signature_validator`) while warning developers about the issue
- **Impact**: Applications using Gemini 3 with persisted messages will now function without crashes, though developers should still implement proper signature handling upstream

## Background

Gemini 3 introduced thought signatures as part of enhanced security validation for tool calls. These signatures represent cryptographic verification that function calls originated from the model itself rather than being injected by external code. For new conversations, the Vercel AI SDK handles this transparently—the model generates signatures automatically as part of its response.

The problem emerges in real-world applications that don't work with single-turn conversations. When developers store conversation history in databases, serialize messages to JSON for transmission across service boundaries, or reconstruct messages programmatically, the `providerOptions.google.thoughtSignature` field frequently gets lost. Custom database schemas might not include this nested property, server-side chat implementations might rebuild message objects without it, or synthetic tool-call injection (where developers manually create tool calls for testing) never includes it.

Prior to this patch, hitting this scenario would result in a direct rejection from Google's API: `"Function call is missing a thought_signature in functionCall parts."` This created a subtle but serious bug—applications would work fine initially, then break unpredictably once persisted conversations were loaded and replayed.

## How it Works

### Automatic Detection and Injection

The provider now includes detection logic that identifies when Gemini 3 models are being used without required signatures. When this condition is detected, instead of passing the request to Google's API immediately, the SDK injects the `skip_thought_signature_validator` sentinel value into the function call. This documented value tells Google's validation layer to skip signature checking for that specific call.

This approach works across all Google provider namespaces: `google`, `googleVertex`, and `vertex`. The detection is model-aware—non-Gemini-3 models are completely unaffected by this logic, maintaining backward compatibility.

### Developer Visibility

Alongside the automatic injection, the SDK generates a one-shot warning per request that surfaces which tool names are affected by missing signatures. Rather than silently fixing the problem, the warning gives developers actionable information: they can identify which tools are triggering the issue and trace back to the source of the serialization problem. This is crucial because while the automatic fix prevents crashes, properly implementing signature persistence upstream remains the correct long-term solution.

### Signature Precedence

The implementation respects genuine signatures when they're present. If `thoughtSignature` is actually provided in the persisted data, that real signature takes precedence over the injected sentinel. This ensures that applications that already handle signature persistence correctly see no change in behavior.

## Real-World Impact

This patch addresses a class of bugs that are easy to hit but hard to debug. A developer building a chatbot application might implement message persistence, write it all correctly, and have everything work in testing. But once they deploy and users start having conversations longer than a single message exchange, the application crashes with a cryptic API error. With this fix, the application continues functioning while the warning guides them toward the actual issue.

The fix is particularly valuable for frameworks and libraries built on top of the Vercel AI SDK that reconstruct messages without full provider metadata. Server-side implementations of the `useChat` hook that rebuild message objects from stored data, for example, would previously have encountered this issue silently.

## What Happens Next

While this patch prevents breaking errors, it's not a permanent solution for production applications. The warning message will help guide developers toward implementing proper signature handling. Teams should audit their message serialization logic to understand whether they're preserving the full message object including provider-specific options, and adjust their persistence layer accordingly.

For new projects, the immediate fix means less concern about Gemini 3 compatibility when starting to implement message persistence. For existing applications already deployed with Gemini 3, this becomes a high-priority patch that will immediately resolve any "missing thought_signature" errors in production.
*This article does not contain affiliate links.*
