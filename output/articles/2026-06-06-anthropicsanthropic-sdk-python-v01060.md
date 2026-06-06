---
category: sdk_release
date: '2026-06-06'
generated_at: '2026-06-06T05:00:26.269569Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/anthropic-sdk-python
source_url: https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.106.0
template_type: explainer
title: anthropics/anthropic-sdk-python v0.106.0
word_count: 812
---

# Anthropic SDK v0.106.0: Model Deprecation and Client Fixes

Anthropic has released version 0.106.0 of its Python SDK, bringing important updates for developers working with Claude models. The release marks a significant milestone by deprecating an older model version while addressing critical client functionality issues that affect enterprise users.

## TL;DR

- **Claude Opus 4.1 deprecation**: The older Opus model is now marked as deprecated, signaling users to migrate toward newer Claude versions
- **Foundry client improvements**: Fixed critical bugs in the copy() and with_options() methods for users leveraging Anthropic's enterprise deployment platform
- **Schema transformation fix**: Resolved an issue where JSON schema definitions were lost during transformation when schemas used $ref pointers
- **Developer impact**: These changes require attention from teams using deprecated models and those relying on Foundry's client duplication features

## Background

The Anthropic SDK for Python serves as the primary interface for developers integrating Claude models into applications. Since its initial releases, the SDK has evolved alongside Anthropic's model releases, creating a situation where multiple model versions exist simultaneously. The deprecation of Claude Opus 4.1 reflects Anthropic's natural progression toward newer model architectures and performance improvements.

The Foundry platform represents Anthropic's enterprise offering, allowing organizations to deploy and manage Claude models in their own infrastructure or through dedicated endpoints. Issues with the copy() and with_options() methods directly impact teams that need to create client variants with different configurations—a common pattern in complex applications requiring multiple model configurations or API keys.

## How it works

### Model Lifecycle and Deprecation Strategy

Claude Opus 4.1's deprecation marks an important shift in Anthropic's model versioning strategy. When a model is marked as deprecated in the SDK, it signals to developers that the model will eventually be removed from available options. This gives development teams a reasonable window to test and migrate their applications to newer Claude versions before the model is fully retired.

Deprecation in SDKs typically manifests as warnings during runtime when deprecated models are called, though the models continue to function. This approach prevents immediate breaking changes while encouraging migration. For teams currently using Opus 4.1, the deprecation serves as a notification to begin testing with successor models, likely Claude 3.5 or another recent variant, and to update their production deployments accordingly.

The deprecation doesn't represent a sudden service discontinuation but rather a formal notice that investment in maintaining this particular model version will decrease over time. Anthropic typically provides several months' notice before fully removing deprecated models from service.

### Foundry Client Duplication Fixes

The fixes to copy() and with_options() methods address critical functionality for Foundry users. These methods are essential patterns in Python for creating modified client instances. The copy() method creates a complete duplicate of a client object, while with_options() creates a new client with modified configuration while preserving other settings.

For Foundry deployments, these methods enable developers to create client variants for different purposes—perhaps one configured for standard requests and another optimized for high-throughput scenarios. When these methods failed, developers couldn't easily create specialized client instances without significant code duplication or manual configuration management.

The bug fix ensures that Foundry clients properly clone their internal state when duplicated, including endpoint configurations, authentication tokens, and other deployment-specific settings. This is particularly important for enterprise teams managing multiple deployment scenarios or API keys across different environments.

### Schema Transformation Improvements

The second bug fix addresses JSON schema handling during transformation operations. Many applications using Claude submit structured data schemas to define expected output formats. Some schemas reference definitions through the $ref mechanism—a pointer to reusable schema components defined elsewhere in the document.

The bug occurred when schemas used $ref pointers at the root level. During transformation (which prepares schemas for use with Claude's API), the system would process the reference but lose the associated $defs section containing the actual definition details. This resulted in incomplete schemas being sent to the API, causing validation failures.

The fix preserves the $defs when transforming schemas, ensuring that referenced definitions remain available throughout the transformation process. This is particularly important for complex schemas used in applications requiring structured outputs from Claude, such as data extraction pipelines or systems that expect Claude to return information in specific formats.

## What happens next

Development teams should begin testing with newer Claude models if they're currently using Opus 4.1, allowing time for validation before the model is fully deprecated. Teams using Foundry should update to v0.106.0 to access the client duplication fixes, particularly if they're implementing patterns that require creating multiple client instances with different configurations.

The schema transformation fix benefits anyone using structured output features with complex, referenced schemas. Updating to this version resolves potential validation issues that may have been causing silent failures in production systems.

Learn more about Claude model options in Anthropic's documentation, or consult the full changelog at the GitHub repository to understand all changes included in this release.
*This article does not contain affiliate links.*
