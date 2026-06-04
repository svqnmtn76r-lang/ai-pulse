---
category: sdk_release
date: '2026-06-03'
generated_at: '2026-06-03T06:10:32.155556Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:openai/openai-python
source_url: https://github.com/openai/openai-python/releases/tag/v2.40.0
template_type: explainer
title: openai/openai-python v2.40.0
word_count: 659
---

# OpenAI Python SDK v2.40.0: AWS Bedrock Integration Arrives

OpenAI has released version 2.40.0 of its official Python SDK, marking a significant step toward multi-cloud AI infrastructure support. The update introduces native compatibility with Amazon Bedrock, AWS's managed service for accessing foundation models, while addressing key configuration challenges developers faced when working across different cloud providers.

## TL;DR

- **Amazon Bedrock Support**: The SDK now natively supports Amazon Bedrock Responses, allowing developers to interact with Bedrock-hosted models through the familiar OpenAI Python interface
- **Simplified Authentication**: Direct API key configuration for Bedrock credentials on the client eliminates workaround configurations
- **Impact**: Developers can now build hybrid AI applications that leverage both OpenAI and AWS Bedrock models without managing separate SDKs or authentication flows

## Background

The OpenAI Python SDK has traditionally focused on OpenAI's own model endpoints. However, the broader AI landscape increasingly features scenarios where organizations need to work with multiple model providers—whether for cost optimization, compliance requirements, or access to specialized models only available through specific platforms.

Amazon Bedrock has emerged as a major player in managed foundation model access, offering a unified interface to models from Anthropic, Meta, Mistral, and others. Until this release, Python developers wanting to use both OpenAI and Bedrock models typically maintained separate client libraries and authentication schemes, creating operational friction and increasing code complexity.

This update reflects a pragmatic shift in how the OpenAI SDK positions itself—not purely as an OpenAI-exclusive tool, but as a flexible interface for Python developers working in multi-model environments. Similar approaches have appeared in other major SDK ecosystems, where vendor-neutral interfaces abstract away provider-specific details.

## How it works

### Amazon Bedrock Response Integration

The new Bedrock Responses feature allows developers to configure the OpenAI Python client to communicate with Amazon Bedrock endpoints. Rather than treating Bedrock as an entirely separate system, the integration mirrors OpenAI's API contract, meaning existing code patterns—like streaming responses, structured outputs, and error handling—work consistently across both providers.

This design choice simplifies migration scenarios. A developer testing Bedrock as an alternative to OpenAI can swap the endpoint configuration without rewriting business logic. The integration handles the protocol translation between Bedrock's API format and the OpenAI SDK's expected interface, creating a seamless experience.

### Direct Credential Management

The second component of this release addresses a practical pain point: authentication. Previously, configuring Bedrock API keys required either environment variables or indirect configuration methods that didn't align with the OpenAI client's native credential handling.

With v2.40.0, developers can now instantiate the OpenAI client and directly supply Bedrock credentials as parameters. This might look like passing AWS access keys, Bedrock-specific API tokens, or region information directly to the client constructor. This change eliminates the need for workarounds or separate credential management libraries, keeping the authentication flow centralized.

### Implementation implications

For practitioners, this means switching between OpenAI and Bedrock involves minimal code changes. Configuration typically becomes a matter of environment variables or initialization parameters rather than architectural rewrites. Error handling, retry logic, and response parsing all benefit from the SDK's established patterns.

Organizations running multi-cloud strategies—perhaps using OpenAI for certain workloads and Bedrock for others—can now maintain simpler, more consistent Python codebases. Teams already familiar with the OpenAI SDK's API surface will find Bedrock integration immediately accessible.

## What happens next

This release likely represents the first phase of broader multi-provider support. Future versions could extend similar integration to other managed model services, creating a truly provider-agnostic Python interface for foundation model access.

The SDK's trajectory suggests OpenAI recognizes that developers increasingly work in heterogeneous environments. Rather than viewing this as fragmentation, treating the Python SDK as a unified development interface creates stickiness through consistency and reduced cognitive overhead.

For AWS customers, this update removes a barrier to OpenAI SDK adoption. Organizations already invested in Bedrock can now leverage OpenAI's mature, well-documented client library instead of juggling multiple tools.

Learn more about the implementation details in the [full GitHub release notes](https://github.com/openai/openai-python/releases/tag/v2.40.0) and the [SDK documentation](https://github.com/openai/openai-python).
*This article does not contain affiliate links.*
