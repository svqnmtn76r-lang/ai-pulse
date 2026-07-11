---
category: sdk_release
date: '2026-07-11'
generated_at: '2026-07-11T04:20:41.679232Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:langchain-ai/langchain
source_url: https://github.com/langchain-ai/langchain/releases/tag/langchain-fireworks%3D%3D1.4.4
template_type: explainer
title: langchain-ai/langchain langchain-fireworks==1.4.4
word_count: 856
---

# LangChain Fireworks 1.4.4 Release: Improved Token Accounting and Stability Updates

LangChain has released version 1.4.4 of its Fireworks integration, a maintenance update focused on fixing token usage reporting for cached prompts and introducing several stability improvements. While this is a point release rather than a major feature launch, the changes address important issues for developers working with large language models at scale, particularly those leveraging prompt caching to optimize costs and latency.

## TL;DR

- **Cached token reporting fix**: The release corrects how token usage is tracked when prompt caching is active, ensuring accurate cost accounting in production applications
- **Dependency updates**: LangSmith upgraded from 0.8.18 to 0.9.5, improving observability and monitoring capabilities
- **Enhanced documentation**: New guidance clarifies how to configure prompt-cache session affinity for optimal performance
- **Impact**: Developers can now accurately track API costs when using cached prompts and benefit from improved observability tooling and test coverage

## Background

Prompt caching represents one of the most significant cost-saving mechanisms available to developers working with large language models. By storing frequently-accessed context (like system prompts, documents, or conversation history) at the inference service level, organizations can reduce token processing costs and improve response latency. However, caching introduces complexity in how tokens are counted and billed.

When a prompt is cached, not all tokens are processed identically. The first request populates the cache, consuming full token costs. Subsequent requests that hit the cache incur lower token charges—typically a 10% surcharge on cached tokens versus full price on new tokens. This distinction is critical for accurate cost tracking and billing, especially in high-volume production deployments.

Prior to this release, the LangChain Fireworks integration wasn't properly accounting for this differentiation, potentially leading to inaccurate token usage metrics. Developers relying on LangChain's usage reporting for billing, cost analysis, or performance monitoring would have received misleading data when caching was active.

## How it works

### Token Usage Reporting for Cached Prompts

The primary fix in 1.4.4 addresses how the Fireworks integration reports token consumption when prompt caching is enabled. The Fireworks API returns granular token usage data that distinguishes between cache-creation tokens (paid at full rate), cache-hit tokens (paid at reduced rate), and new prompt tokens. 

Previously, this distinction wasn't being properly surfaced through LangChain's standard token usage interface. The fix ensures that the integration now correctly parses and reports cached token metrics, allowing developers to see exactly how many tokens were served from cache versus computed fresh. This transparency is essential for understanding the actual economic value of caching in your specific workload.

The fix particularly matters for applications making multiple requests with overlapping context. A document analysis system, for instance, might cache a large technical document and then run multiple queries against it. With accurate reporting, teams can see their actual token consumption decrease with each subsequent query, validating the investment in implementing caching.

### Dependency and Observability Improvements

The LangSmith upgrade from 0.8.18 to 0.9.5 brings improvements to the observability layer that integrates with LangChain. LangSmith is the companion monitoring and debugging platform from the LangChain team, providing tracing, logging, and performance analytics for LLM applications. The version bump likely includes enhanced support for cost tracking and new observability features that work in concert with the token usage fixes.

These observability improvements become more valuable with the token reporting fix, as developers can now track not just that caching is happening, but precisely measure its impact on their token consumption and costs through LangSmith's dashboard.

### Documentation and Configuration Guidance

The release includes clarified documentation around prompt-cache session affinity—a configuration setting that determines how cached prompts are distributed across inference service instances. Session affinity ensures that requests using the same cached content are routed to the same underlying inference instance where the cache resides, maximizing cache hit rates.

The guidance helps teams avoid a subtle performance trap: without proper session affinity configuration, a request might hit a different inference instance without access to the cache, forcing a cache miss and full token re-processing. The clearer documentation helps developers configure this correctly from the start.

### Testing and Quality Improvements

The release includes expanded test coverage for request-level extra headers functionality. This ensures that custom HTTP headers can be properly passed through to the Fireworks API without interfering with caching or other core functionality. Test improvements also reflect the pytest bump to 9.1.1, part of ongoing quality assurance improvements.

## What happens next

For teams currently using LangChain with Fireworks, the primary value from this update is accurate cost tracking when caching is enabled. If you're already using prompt caching, upgrading to 1.4.4 will give you visibility into your actual token costs for the first time. This data should inform decisions about whether to expand caching across more use cases.

The improved documentation is worth reviewing even if you're not currently using caching, as it may reveal optimization opportunities in your existing deployments. The dependency updates, particularly the LangSmith improvements, benefit all users through better observability.

This release exemplifies incremental but important maintenance work in production AI systems—the fixes aren't flashy, but they address real issues that affect cost accuracy and debugging capabilities at scale.
*This article does not contain affiliate links.*
