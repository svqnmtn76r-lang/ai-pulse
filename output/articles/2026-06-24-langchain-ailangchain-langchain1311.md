---
category: sdk_release
date: '2026-06-24'
generated_at: '2026-06-24T05:08:10.621203Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:langchain-ai/langchain
source_url: https://github.com/langchain-ai/langchain/releases/tag/langchain%3D%3D1.3.11
template_type: explainer
title: langchain-ai/langchain langchain==1.3.11
word_count: 797
---

# LangChain 1.3.11 Release: Fixing OpenAI Tool Compatibility

LangChain, the popular framework for building applications with large language models, has released version 1.3.11, addressing a critical compatibility issue with OpenAI-compatible models while introducing several dependency updates. This incremental release focuses on improving reliability and documentation rather than introducing major new features.

## TL;DR

- **Tool Strictness Configuration**: The framework now correctly applies strict parameter settings only to OpenAI-compatible models, preventing incompatibility issues with other provider implementations
- **Dependency Updates**: Multiple core dependencies received security and stability improvements, including pydantic-settings, langsmith, and vcrpy
- **Documentation Enhancement**: Added clearer contracts around summarization prompts to help developers implement custom behaviors
- **Impact**: Practitioners using non-OpenAI models or custom tool implementations will see improved reliability and fewer configuration errors

## Background

As LangChain has matured, one persistent challenge has been maintaining compatibility across different LLM providers while offering provider-specific optimizations. OpenAI's API includes features like structured tool calling with strict schema validation—represented by the `strict=True` parameter in tool definitions. However, not all LLM providers support identical interfaces.

The `ProviderStrategy` pattern in LangChain abstracts away provider-specific behaviors, allowing developers to switch between different models without rewriting application logic. However, when certain provider-specific features get applied universally, it creates incompatibility problems. The previous behavior of applying OpenAI's strict tool requirements to all providers was causing failures when developers used alternative models or self-hosted solutions.

This release represents the incremental refinement work that characterizes mature software maintenance—addressing edge cases and improving the developer experience for users working across heterogeneous model ecosystems.

## How it works

### Provider-Specific Tool Configuration

The core fix in 1.3.11 modifies how LangChain handles tool schema strictness. When you define a tool in LangChain and pass it to a model, the framework needs to translate your tool definition into a format that particular model understands. 

The `strict` parameter tells OpenAI's API to enforce strict adherence to the tool's JSON schema, causing the model to return only valid tool calls that exactly match your specification. This is useful for reliability but adds computational overhead and isn't universally supported across all providers.

Previously, LangChain was applying this strict mode broadly. The updated `ProviderStrategy` now inspects which provider is being used before deciding whether to set `strict=True`. If you're using OpenAI or OpenAI-compatible APIs (which follow the same interface), tools get the strictness guarantee. For other providers, the framework skips this setting, using whatever defaults are appropriate for that particular model's API.

This is a subtle but important distinction: the fix prevents configuration from "leaking" across provider boundaries. Your Anthropic implementation won't try to use OpenAI-specific parameters, and your open-source model deployment won't fail when LangChain attempts to set unsupported configuration options.

### Dependency Maintenance

Three dependency updates landed in this release, each addressing different concerns:

**Pydantic-settings** was bumped from 2.12.0 to 2.14.2, jumping two minor versions. This library handles configuration management through Pydantic models, crucial for LangChain's own settings and environment variable handling. The update likely includes bug fixes and improved type inference that benefit downstream applications.

**LangSmith**, LangChain's observability and tracing companion, advanced from 0.8.9 to 0.8.18. This is a more significant jump across nine patch versions, suggesting either critical bug fixes or important feature enhancements in the tracing infrastructure that LangChain integrates with.

**VCRpy**, used for recording and replaying HTTP interactions in tests, moved from 8.1.1 to 8.2.1. This library is primarily a testing dependency but updating it helps ensure that LangChain's test suite remains stable and that mock HTTP interactions continue working reliably as web standards evolve.

### Documentation Improvements

The release adds formal documentation around summarization prompt contracts. In LangChain, prompts are structured instructions sent to language models. A "contract" in this context means clearly documenting what inputs a summarization prompt expects and what outputs it should produce.

This matters because developers often customize summarization behavior by providing their own prompts, and without clear contracts, they risk creating prompts that don't work as expected with LangChain's summarization chains. By documenting the contract—what variables get injected into the prompt template, what format the model should use for responses—the framework helps developers write compatible customizations.

## What happens next

This release exemplifies the maintenance work that keeps mature frameworks reliable. While 1.3.11 doesn't introduce flashy new capabilities, it removes friction points that affect real practitioners, particularly those working in complex multi-model environments.

Teams using LangChain with non-OpenAI models should upgrade to eliminate potential tool configuration issues. The dependency updates provide security and stability improvements worth capturing, and the documentation enhancement helps prevent future implementation mistakes.

The focus on provider compatibility and careful dependency management suggests LangChain's maintainers are prioritizing ecosystem stability as the framework becomes increasingly critical infrastructure for LLM applications. Expect similar incremental releases focusing on reliability and compatibility to continue as more organizations adopt LangChain in production environments.
*This article does not contain affiliate links.*
