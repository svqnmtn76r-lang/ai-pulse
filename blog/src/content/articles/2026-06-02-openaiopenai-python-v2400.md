---
category: sdk_release
date: '2026-06-02'
generated_at: '2026-06-02T05:56:40.121610Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:openai/openai-python
source_url: https://github.com/openai/openai-python/releases/tag/v2.40.0
template_type: explainer
title: openai/openai-python v2.40.0
word_count: 756
---

# OpenAI Python SDK v2.40.0: Expanding AWS Integration with Bedrock Support

OpenAI has released version 2.40.0 of its Python SDK, introducing native support for Amazon Bedrock responses and improving credential management for AWS integrations. This update reflects a broader trend of AI framework providers deepening their compatibility with major cloud platforms, enabling developers to leverage multiple model providers through unified interfaces.

## TL;DR

- **Bedrock Responses Support**: The SDK now natively handles response formats from Amazon's Bedrock service, a managed AI service offering access to multiple foundation models
- **Simplified Credential Management**: Developers can now configure Bedrock API credentials directly within the OpenAI Python client, eliminating the need for external configuration
- **Impact**: Teams using AWS infrastructure can more seamlessly integrate Bedrock models into existing OpenAI-based workflows, reducing friction in multi-provider AI architectures

## Background

The OpenAI Python library has long served as a primary interface for developers building applications with OpenAI's models. However, the modern AI landscape increasingly involves polyglot architectures where teams leverage multiple model providers—OpenAI, Anthropic, Cohere, and others—often through AWS services.

Amazon Bedrock, launched in 2023, provides a managed API layer for accessing various foundation models including Claude, Llama, Stable Diffusion, and others. The challenge for developers has been managing separate SDKs and credential systems for each provider. By adding Bedrock response support to its Python client, OpenAI acknowledges this reality and removes a meaningful integration barrier.

This release also addresses a specific pain point: AWS credential management. Previously, developers needed to maintain separate authentication flows for Bedrock, typically through environment variables or AWS credential files. Direct client-level credential configuration streamlines this process within the OpenAI SDK's existing patterns.

## How it works

### Amazon Bedrock Response Integration

Bedrock responses follow similar structural patterns to OpenAI's API responses but include AWS-specific metadata and formatting conventions. The Python SDK v2.40.0 now includes deserialization logic that properly parses Bedrock response payloads, converting them into the same object types developers use for OpenAI models.

This means conditional code branches or provider-specific parsing logic become unnecessary. A developer can configure their client to use Bedrock, make API calls using familiar OpenAI SDK methods, and receive properly-typed response objects—whether the underlying model comes from OpenAI, Anthropic, or another Bedrock-supported provider.

The implementation handles differences in how Bedrock structures token counting, usage metrics, and model identifiers, normalizing these into OpenAI's conventions. This abstraction enables cleaner, more maintainable code when working with multiple providers.

### Credential Management Improvements

Previously, Bedrock credentials typically lived in AWS configuration files or environment variables like `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`. Version 2.40.0 extends the OpenAI client's initialization parameters to accept Bedrock-specific credentials directly.

Developers can now instantiate the client with code like:

```python
client = OpenAI(
    bedrock_access_key="...",
    bedrock_secret_key="..."
)
```

This approach offers several advantages: credentials remain scoped to specific client instances rather than globally affecting all AWS SDK calls, enabling fine-grained permission management within applications. It also reduces cognitive overhead—developers manage all API credentials in one place within their application initialization code.

The implementation maintains backward compatibility with environment variable and AWS credential file configurations, so existing deployments continue functioning without modification.

## What this means in practice

These changes lower the barrier for teams adopting multi-model strategies. Previously, switching between OpenAI and Bedrock APIs required significant code refactoring or implementing custom abstraction layers. With native Bedrock support in the Python SDK, the switching cost drops dramatically.

For organizations already invested in AWS infrastructure, this update makes OpenAI models more accessible within their existing toolchains. Teams running on EC2, Lambda, or ECS can now treat OpenAI APIs as just another service accessible through their standard AWS authentication mechanisms.

The credentials-in-client-initialization pattern also improves security posture for containerized deployments. Instead of relying on environment variables (which can leak through Docker image inspection or logs), credentials can be injected at runtime through application configuration systems, reducing exposure surface area.

## What happens next

As AI frameworks mature, we should expect similar integrations across the ecosystem. The pattern emerging here—where providers extend SDKs to interoperate with cloud platforms—suggests that cross-provider compatibility will become standard rather than exceptional.

For developers, this release justifies reviewing your AI infrastructure decisions. If you've avoided multi-provider architectures due to integration complexity, these friction points are steadily disappearing. The Python SDK now makes Bedrock a viable alternative within existing OpenAI-based codebases, useful for cost optimization, model selection, or compliance requirements.

Watch for similar updates in other SDKs (JavaScript, Go) following this lead, and for reverse integrations where AWS SDKs gain tighter OpenAI compatibility. The era of single-provider lock-in in AI is definitively ending.
*This article does not contain affiliate links.*
