---
category: sdk_release
date: '2026-07-23'
generated_at: '2026-07-23T04:23:01.658583Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/anthropic-sdk-python
source_url: https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.117.1
template_type: explainer
title: anthropics/anthropic-sdk-python v0.117.1
word_count: 774
---

# Anthropic Python SDK v0.117.1: Credential Handling and API Improvements

Anthropic has released version 0.117.1 of its Python SDK, a maintenance update focused on resolving credential management issues for AWS users and adding support for new API capabilities. While modest in scope, this release addresses critical infrastructure concerns for developers integrating Claude through Amazon Web Services.

## TL;DR

- **AWS Credential Bug Fix**: The `AnthropicAWS.copy()` method now correctly preserves AWS credentials during client cloning operations
- **Refusal Category Expansion**: New API support allows more granular classification of model refusals
- **Dependency Updates**: Minor package dependency bumps improve compatibility and security

## Background

The Anthropic Python SDK serves as the primary interface for developers building applications with Claude models. Anthropic offers multiple deployment paths, including direct API access and integration through AWS Bedrock, which allows customers to run Claude through their existing AWS infrastructure.

The AWS integration path is particularly important for enterprises that standardize on AWS for compliance, billing, or operational reasons. However, SDK clients often need to be copied or cloned during application lifecycle—whether for creating isolated instances for different API calls, spawning parallel processing threads, or managing complex multi-tenant scenarios.

Previous versions had a gap: when developers copied an `AnthropicAWS` client instance, the underlying AWS credentials weren't properly transferred to the new instance. This meant the cloned client would fail authentication, forcing developers to either recreate clients from scratch or work around the limitation with workarounds.

## How it works

### AWS Credentials and the Copy Method

The `AnthropicAWS` class extends the base Anthropic client with AWS-specific authentication. Unlike standard API key authentication, AWS credentials involve multiple components: an access key ID, secret access key, optional session token, and region information. These credentials follow AWS's standard signature protocol for verifying requests.

When a Python SDK client is copied using the `.copy()` method, the SDK creates a shallow duplicate of the client's configuration. The bug existed because the credential components specific to AWS weren't included in the copy operation. The new version now properly transfers all credential data when cloning AWS client instances, ensuring the copied client maintains full authentication capability.

This fix is particularly relevant for developers using asynchronous patterns or worker pool architectures, where multiple client instances operating in parallel require consistent authentication.

### Refusal Category Enhancement

The chore update adding support for a new refusal category reflects evolution in how Claude communicates when it cannot fulfill requests. The model distinguishes between different reasons for declining tasks—whether due to safety guidelines, capability limitations, or policy constraints. Enhanced categorization allows developers to implement more sophisticated error handling and user communication strategies.

When Claude refuses a request, the SDK now provides more detailed classification information. Applications can examine these categories to provide targeted feedback to end users, adjust their prompting strategy, or route requests through alternative pathways. This granularity improves the developer experience when building robust, production-grade applications.

### Dependency and Documentation Updates

The release includes dependency bumps, specifically pinning the `httpx_aiohttp` major version and updating `http-snapshot` to version 0.1.9. These updates ensure compatibility with the Python ecosystem's evolving HTTP libraries, particularly for asynchronous operations where `httpx` and `aiohttp` play critical roles.

Concurrent with these technical changes, the SDK documentation received updates clarifying client usage patterns and configuration options.

## Impact for practitioners

For developers using `AnthropicAWS`, this release eliminates a significant friction point. Applications that previously required workarounds to manage multiple client instances can now safely clone clients without reimplementing authentication logic. This is especially valuable in microservices architectures or serverless environments where creating fresh client instances for each request isn't practical.

The refusal category expansion enables more sophisticated error handling. Production applications can now respond more intelligently when Claude declines requests, distinguishing between different refusal types and providing users with contextually appropriate messages.

The dependency updates address a common pain point in Python development—maintaining compatible versions across the HTTP client ecosystem. By pinning major versions, the SDK reduces the likelihood of breaking changes from dependency upgrades.

## What happens next

Organizations running Claude through AWS should prioritize updating to this version, particularly if they use client copying patterns in their applications. The fix is backwards compatible, meaning existing code continues to work without modification while gaining the credential handling improvements.

Developers building against the new refusal categories should review Anthropic's API documentation to understand the expanded classification scheme and consider how their applications might benefit from more granular error handling.

The steady stream of incremental improvements in the SDK suggests Anthropic's commitment to maintaining a stable, enterprise-grade developer experience. While major feature releases capture headlines, these maintenance updates address the real-world operational concerns that determine whether tools succeed in production environments.
*This article does not contain affiliate links.*
