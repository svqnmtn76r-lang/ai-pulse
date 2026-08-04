---
category: sdk_release
date: '2026-08-04'
generated_at: '2026-08-04T04:20:06.101868Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:vercel/ai
source_url: https://github.com/vercel/ai/releases/tag/%40ai-sdk/xai%404.0.26
template_type: explainer
title: vercel/ai @ai-sdk/xai@4.0.26
word_count: 991
---

# Vercel AI SDK Adds Asynchronous Video Generation: What You Need to Know

Vercel's AI SDK has introduced significant improvements to its experimental video generation capabilities, moving beyond simple synchronous requests to support asynchronous workflows. The latest patch release for the XAI provider introduces a more flexible architecture that accommodates long-running video generation tasks through polling and webhook mechanisms—a critical addition for production applications where generating video content can take minutes or hours.

## TL;DR

- **Async video workflows**: The SDK now supports asynchronous start/status patterns for video generation, allowing applications to handle long-running tasks without blocking
- **Dual completion paths**: Developers can choose between polling (periodic status checks) or webhooks (event-driven notifications) to determine when video generation completes
- **Custom polling strategies**: The polling configuration supports custom delay implementations, enabling integration with durable workflow systems and more sophisticated retry logic
- **Impact**: This modernizes video generation support in the AI SDK, making it practical for real-world applications where video rendering cannot complete within typical HTTP request timeframes

## Background

Video generation represents one of the most computationally intensive tasks in AI workloads. Unlike text generation, which can often complete within seconds, video synthesis—whether creating multi-second clips or processing complex visual transformations—frequently requires substantial processing time. This created a fundamental mismatch between HTTP's request-response model, which typically times out after 30-120 seconds, and the actual time needed to produce video content.

Earlier versions of the AI SDK's video model interface relied on synchronous `doGenerate` methods, meaning developers either had to accept long request timeouts or abandon SDK-based video generation entirely. Many production systems had resorted to building custom wrappers around video APIs, implementing their own polling logic or webhook handlers—essentially duplicating effort across organizations.

The introduction of the `VideoModelV4` experimental interface signals Vercel's recognition that video generation requires architectural patterns typically reserved for async task processing. This aligns with industry practices seen in services like RunwayML, Replicate, and other specialized video platforms that have long required asynchronous workflows.

## How It Works

### The New VideoModelV4 Architecture

The updated video model interface fundamentally changes how providers implement video generation. Rather than forcing everything through a single synchronous path, `VideoModelV4` establishes three optional methods: `doStart`, `doStatus`, and `handleWebhookOption`.

The `doStart` method initiates video generation and returns a handle or identifier—think of it as booking a job in a queue. The actual generation happens server-side while your application receives immediate confirmation. This immediate acknowledgment prevents timeout issues and lets your application move on to other tasks.

The `doStatus` method polls the video generation service to check progress. This enables the client-side polling mechanism built into `experimental_generateVideo`, which repeatedly checks status at configurable intervals until generation completes. Traditional polling works well when you have a limited number of active generations or when you can afford modest latency in learning about completion.

### Polling: Periodic Status Checks

Polling configuration now accepts custom delay implementations, which addresses a major real-world concern. Different applications have different requirements—a web application might check status every 5 seconds, while a backend worker might check every 30 seconds. More importantly, in distributed systems using durable workflows (like Temporal, Durable Functions, or similar platforms), standard `setInterval` calls don't work. The custom delay implementation allows these frameworks to manage retry logic according to their own scheduling rules.

For example, a Next.js application using the AI SDK could configure polling with exponential backoff, starting with 2-second intervals and gradually increasing to avoid overwhelming the generation service. Meanwhile, an Anthropic Workflows user could pass delay logic that respects workflow step timing.

### Webhooks: Event-Driven Notifications

The webhook path inverts the notification model. Rather than repeatedly asking "is it done yet?", the video generation service calls your application when the job completes. This requires your application to expose an HTTP endpoint that can receive these callbacks and process completion events.

The `handleWebhookOption` method on the model implementation specifies how providers handle webhook configuration—essentially declaring "I can validate and process webhooks at this URL." This lets the SDK coordinate between client requests and server callbacks without tightly coupling to any specific provider's webhook format.

Webhooks eliminate polling overhead entirely and provide lower latency notifications, making them ideal for high-volume scenarios or applications where responsiveness matters. However, they require additional infrastructure to handle inbound traffic reliably.

### Dependency Updates

This release also updates supporting packages: the core provider interface (`@ai-sdk/provider@4.0.5`), the generic OpenAI-compatible provider (`@ai-sdk/openai-compatible@3.0.21`), and provider utilities (`@ai-sdk/provider-utils@5.0.19`). These updates ensure that the async patterns work consistently across different provider implementations and that OpenAI-compatible services can leverage the new capabilities.

## Practical Implications

For developers currently building video features with the AI SDK, this changes the equation. Previously, you either had to work around SDK limitations or abandon it entirely for video. Now you can leverage the same SDK primitives used for text and image generation, with proper async support built in.

Building a video editing feature in a Next.js app? Use polling with reasonable intervals to check generation progress. Implementing enterprise batch processing? Use webhooks with a message queue to handle thousands of concurrent generations. Building AI workflows? Use durable workflow support to manage video generation as a proper step in longer processes.

The improvement also suggests that other long-running operations in the AI SDK might follow similar patterns, establishing conventions that developers can expect across different providers.

## What Happens Next

The experimental status remains important—these interfaces may change in response to real-world usage patterns. Early adopters should expect potential breaking changes in minor updates, though Vercel's approach typically provides clear migration paths.

Providers implementing video generation should now consider whether their existing synchronous implementations can be enhanced with async variants. The fact that `doStart` and `doStatus` are optional suggests backward compatibility—providers can continue with synchronous generation while gradually introducing async support.

Developers interested in exploring these features should review the updated AI SDK documentation and experiment with sample implementations for their specific use case—whether that's polling for interactive applications or webhooks for batch processing.
*This article does not contain affiliate links.*
