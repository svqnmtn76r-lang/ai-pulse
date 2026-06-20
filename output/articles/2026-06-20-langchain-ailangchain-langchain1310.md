---
category: sdk_release
date: '2026-06-20'
generated_at: '2026-06-20T05:23:18.950596Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:langchain-ai/langchain
source_url: https://github.com/langchain-ai/langchain/releases/tag/langchain%3D%3D1.3.10
template_type: explainer
title: langchain-ai/langchain langchain==1.3.10
word_count: 778
---

# LangChain 1.3.10 Release: Dependency Updates and Provider Detection Improvements

LangChain, the popular framework for building applications with large language models, has released version 1.3.10, bringing security updates, bug fixes, and improved model detection capabilities. The release represents the latest incremental advancement in the 1.3.x series, focusing on stability and reliability rather than new features.

## TL;DR

- **Security patches**: Critical dependency updates including cryptography and JWT library bumps address potential vulnerabilities
- **Provider detection fix**: Improved handling of dated GPT snapshot models ensures correct provider identification
- **Format improvements**: Summary format switching resolves output consistency issues
- **Impact**: Users should upgrade to benefit from security patches and more reliable model routing, particularly those working with multiple model providers and OpenAI API variants

## Background

The LangChain project operates as a modular ecosystem across multiple libraries—core, langchain, OpenAI integrations, and Anthropic integrations—each with their own versioning and release cycles. Version 1.3.10 represents a coordinated release across several of these packages, including core 1.4.7, OpenAI integration 1.4.0, and Anthropic integration 1.4.6.

Previous versions in the 1.3.x series have focused on stabilizing the API after major breaking changes in 1.0, improving serialization and deserialization mechanisms, and expanding provider support. The 1.3.9 release that preceded this version included similar maintenance updates.

The release cycle reflects a broader pattern in LangChain development: frequent, small-batch updates that address specific issues rather than large feature drops. This approach allows the framework to remain responsive to security concerns and bug reports while maintaining API stability.

## How it works

### Security Dependency Updates

The release includes three significant dependency upgrades. The cryptography library jumped from version 46.0.7 to 48.0.1, a substantial two-point version increase that typically indicates important security patches or breaking changes requiring mitigation at the LangChain level.

Similarly, PyJWT (Python JWT library) updated from 2.12.0 to 2.13.0. These JWT libraries are critical in LangChain deployments that interact with external APIs requiring authentication tokens, particularly for OpenAI and other commercial LLM providers.

The aiohttp library, used for asynchronous HTTP requests throughout LangChain's async operations, received a minor patch bump from 3.14.0 to 3.14.1. While seemingly small, these patch updates often address connection pooling issues, SSL/TLS handling, or timeout behaviors that could cause reliability problems in production systems.

These dependency updates represent what the development team considers necessary maintenance to keep LangChain's dependency tree secure and compatible with the broader Python ecosystem. Users running older versions face potential security exposure or compatibility issues with newer versions of dependent packages.

### Model Provider Detection Enhancement

One of the more technically interesting fixes addresses how LangChain identifies which provider to use for certain model identifiers. The framework previously struggled with "dated snapshots" of GPT models—versions like `gpt-5.2` and `gpt-5.4` that include decimal-based version numbers.

The provider detection strategy relies on parsing model names to determine whether a request should route to OpenAI, Anthropic, or other backends. When encountering unexpected version formats, the system could fail to properly identify the provider, resulting in routing errors or incorrect API calls.

This fix implements improved logic to recognize these dated snapshot formats and correctly map them to their corresponding providers. For developers working with experimental or snapshot model versions, this ensures their applications won't break or misbehave when encountering non-standard version identifiers.

### Summary Format Corrections

The framework made adjustments to how summaries are formatted in outputs. This change, while less visible than provider detection fixes, affects any application using LangChain's summarization capabilities or components that generate summary outputs. Format consistency matters when these summaries feed into downstream processing, APIs, or user-facing interfaces.

### Test Infrastructure Improvements

Accompanying the user-facing fixes, the development team improved type hints in tests and updated test cases for explicit deserialization allowlists. These infrastructure improvements make the codebase more maintainable and reduce the surface area for type-related bugs in future releases.

The deserialization allowlist changes reflect LangChain's ongoing security hardening around serialization. By being explicit about which classes can be deserialized, the framework reduces risks from untrusted input that could otherwise execute arbitrary code.

## What happens next

Users of LangChain should evaluate whether the security updates warrant an immediate upgrade, particularly those in production environments or handling sensitive authentication credentials. The cryptography and PyJWT updates should be considered higher priority than the aiohttp patch.

The provider detection fix is especially relevant for teams experimenting with snapshot or beta model versions. Testing the upgrade in staging environments first ensures no unexpected routing behavior changes in production.

The LangChain team continues this pattern of frequent, focused releases. Monitoring the release notes for security-related updates remains important, as dependency vulnerabilities affecting cryptography or HTTP libraries could impact any LangChain deployment handling sensitive API interactions or user data.
*This article does not contain affiliate links.*
