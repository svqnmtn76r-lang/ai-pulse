---
category: sdk_release
date: '2026-07-22'
generated_at: '2026-07-22T04:23:43.481507Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/anthropic-sdk-python
source_url: https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.117.1
template_type: explainer
title: anthropics/anthropic-sdk-python v0.117.1
word_count: 778
---

# Anthropic Python SDK v0.117.1: AWS Credential Handling and API Updates

Anthropic has released version 0.117.1 of its Python SDK, a maintenance update focused on resolving credential management issues for AWS deployments and extending API capabilities. While relatively modest in scope, this release addresses a critical bug that could have impacted developers using the AWS variant of the client.

## TL;DR

- **AWS Credential Bug**: Fixed improper credential handling when using the `AnthropicAWS.copy()` method, which could cause authentication failures in cloned client instances
- **Refusal Categories Expanded**: The API now supports an additional refusal category, giving developers more granular control over how to handle content moderation responses
- **Dependency Updates**: Routine maintenance on HTTP-related dependencies to improve stability and compatibility
- **Impact**: Essential for AWS users who rely on client cloning patterns; beneficial for applications requiring more detailed refusal categorization

## Background

The Anthropic Python SDK provides developers with a programmatic interface to Claude, Anthropic's AI assistant. Over recent releases, the SDK has evolved to support multiple deployment scenarios, including standard API access and AWS-hosted alternatives through the `AnthropicAWS` client variant.

One common pattern in modern Python applications is duplicating client instances with modified configurations—the `.copy()` method. This allows developers to maintain separate client configurations for different use cases without reinstantializing the entire SDK. However, when credentials are involved, this process becomes complex, particularly in AWS environments where credentials follow specific management protocols.

The previous implementation apparently did not properly propagate AWS credentials when developers called `.copy()` on an `AnthropicAWS` instance, potentially causing authentication failures in downstream operations.

## How It Works

### AWS Credential Propagation in Client Copies

AWS credentials operate differently than standard API keys. Rather than static tokens, AWS uses a credential chain that can include temporary credentials from STS (Security Token Service), IAM roles, or explicitly provided credentials. The SDK must handle this complexity transparently.

When a developer creates an `AnthropicAWS` client, the SDK initializes AWS credential resolution following the standard AWS SDK credential provider chain. This chain checks multiple sources in order: environment variables, credential files, IAM role metadata, and other providers.

The bug manifested when calling `.copy()` on an authenticated `AnthropicAWS` instance. Rather than preserving the original credentials or their chain context, the copying mechanism apparently lost this state. This meant a cloned client would need to re-resolve credentials independently, which could fail if the original resolution context wasn't available—particularly problematic in containerized or lambda environments where credentials are time-limited.

The fix ensures that when `.copy()` is invoked, credential state transfers correctly to the new instance, maintaining the original authentication context and preventing redundant or failed credential resolution attempts.

### Extended Refusal Categories

Content moderation is a critical concern for AI applications. Anthropic's Claude models can refuse to respond to certain requests based on content policies. Previously, the SDK supported a discrete set of refusal categories that developers could query to understand why a response was declined.

This release adds support for an additional refusal category. While the changelog doesn't specify which new category was added, this typically indicates either:

- A new safety threshold or concern that Claude now explicitly categorizes
- Greater granularity in distinguishing between different types of harmful requests
- Support for region-specific or context-dependent refusal categories

For developers building applications that interact with refused responses, this expanded taxonomy provides more actionable information. Rather than receiving a generic "refused" status, applications can now distinguish between more specific denial reasons and respond appropriately—for example, logging different categories differently or providing more contextual user feedback.

### Dependency and Documentation Maintenance

Like most SDK releases, v0.117.1 includes housekeeping updates. The `http-snapshot` dependency was bumped to version 0.1.9, likely addressing bug fixes or performance improvements in HTTP request recording and testing utilities. The `httpx_aiohttp` dependency was pinned to a specific major version, preventing breaking changes from automatic updates.

Documentation was also refreshed, reflecting API changes and improving clarity for developers consulting the client reference.

## What Happens Next

This release represents Anthropic's ongoing commitment to SDK stability and feature parity with API capabilities. For AWS-focused deployments, the credential handling fix is essential—teams should prioritize updating, particularly if they use the client copying pattern.

Developers working with refusal handling should review the new category and determine whether their existing response logic needs adjustment to leverage the additional granularity. In most cases, existing code will continue functioning, but new applications can immediately benefit from the improved categorization.

The maintenance nature of this release suggests the SDK is stabilizing around core functionality, with future updates likely focused on supporting new Claude models or API features rather than foundational fixes. Teams should keep their SDK versions current to ensure compatibility with the latest Claude API developments.
*This article does not contain affiliate links.*
