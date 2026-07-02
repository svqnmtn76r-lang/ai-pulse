---
category: sdk_release
date: '2026-07-02'
generated_at: '2026-07-02T01:51:05.000034Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:vercel/ai
source_url: https://github.com/vercel/ai/releases/tag/%40ai-sdk/google%404.0.6
template_type: explainer
title: vercel/ai @ai-sdk/google@4.0.6
word_count: 750
---

# Vercel AI SDK Adds Vertex AI Interactions Support: What You Need to Know

Vercel has released a new patch for its AI SDK's Google integration, introducing support for Google Cloud's Vertex AI Interactions API. This update enables developers to access advanced multimodal capabilities through Vertex AI's infrastructure, including video output models that weren't previously available through the standard Google AI SDK integration.

## TL;DR

- **Vertex Interactions API**: New method `vertex.interactions()` connects the AI SDK directly to Google Cloud's specialized interactions endpoint for enhanced model capabilities
- **Multimodal video output**: Developers can now use models like `gemini-omni-flash-preview` that produce video, audio, and other rich media types alongside text
- **Enterprise authentication**: Leverages existing Vertex OAuth credentials, maintaining security practices for production environments
- **Impact**: Teams using Google Cloud can access cutting-edge multimodal AI models without switching providers or managing separate API connections

## Background

Google's AI capabilities exist across multiple platforms with different feature sets. The standard Google AI API handles most text and image use cases, but Google Cloud's Vertex AI platform—the enterprise-grade machine learning service—offers specialized endpoints for advanced scenarios.

The Interactions API represents one such specialized endpoint. Rather than following the standard request-response pattern of typical API calls, interactions provide a more sophisticated protocol designed for complex, stateful conversations and multimodal exchanges. Previously, the AI SDK provided full support for Vertex AI's prediction API but lacked direct integration with the interactions endpoint.

This gap mattered because Google started rolling out advanced models like Gemini 1.5 Omni and its preview variants through the interactions API first. These models can produce not just text responses but video, audio, and other media types—capabilities increasingly important for applications like video generation, interactive media creation, and complex multimodal AI workflows.

## How it works

### The Vertex Interactions Endpoint

The interactions endpoint exists within Vertex AI's location-scoped resource hierarchy. Rather than calling a generic endpoint, developers now target a specific regional resource: `.../locations/{region}/interactions`. This architecture allows Vertex AI to manage compute resources efficiently and comply with data residency requirements.

The new `vertex.interactions()` method in the AI SDK abstracts away this complexity. When called, it automatically constructs the correct resource path, routes requests to the appropriate region, and handles the protocol differences between standard and interactions APIs.

### Authentication and Credentials

A key advantage of this implementation is that it reuses existing Vertex OAuth credentials. Developers who have already authenticated with Google Cloud for other Vertex AI services don't need separate credentials. The SDK's authentication layer recognizes when the interactions endpoint is being used and applies the same OAuth tokens, reducing operational overhead.

This approach also maintains security boundaries. Organizations can continue using the same IAM policies that govern other Vertex AI access, ensuring consistent permission management across their AI infrastructure.

### Accessing Multimodal Models

The `gemini-omni-flash-preview` model and similar variants represent a new generation of AI models that produce multiple output types. Traditional text-only models return a string. These models can return text, video frames, audio streams, or combinations thereof.

Developers call these models through the familiar AI SDK interface—the same functions and patterns used for text-based interactions—but the underlying interactions API handles the complexity of streaming video data, managing state across multiple modality exchanges, and coordinating multimodal outputs.

### Internal API Exports

The patch also exports `GoogleInteractionsLanguageModel` from `@ai-sdk/google/internal`. This allows other providers and custom implementations to build atop the interactions infrastructure. Framework developers and companies building specialized AI layers can now reference this model class when creating their own integrations or provider wrappers.

## What this means for practitioners

For developers building applications on Google Cloud, this update removes a significant barrier. Previously, accessing cutting-edge multimodal models meant stepping outside the AI SDK ecosystem, integrating raw Google Cloud APIs, and managing authentication separately.

Now, teams using Vercel's framework can stay within the unified AI SDK environment while accessing the latest models. This simplifies codebases, reduces the number of dependencies, and makes it easier to mix standard and advanced models within the same application.

The location-scoped resource approach also matters for compliance-heavy industries. Applications requiring data to remain in specific geographic regions can now specify Vertex AI locations through the SDK, making it practical to use advanced models in regulated environments.

## Learn more

The full implementation is available in the `@ai-sdk/google` package version 4.0.6 and later. Developers should review Vercel's AI SDK documentation for the specific `vertex.interactions()` method signature and examples, along with Google Cloud's documentation on which models support the interactions API and which regions they're available in.
*This article does not contain affiliate links.*
