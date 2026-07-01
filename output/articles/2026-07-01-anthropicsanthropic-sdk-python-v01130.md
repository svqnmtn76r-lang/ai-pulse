---
category: sdk_release
date: '2026-07-01'
generated_at: '2026-07-01T01:54:39.285753Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/anthropic-sdk-python
source_url: https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.113.0
template_type: explainer
title: anthropics/anthropic-sdk-python v0.113.0
word_count: 899
---

# Anthropic Python SDK v0.113.0: Web Fetch and Tool Support Enable More Dynamic AI Interactions

Anthropic has released version 0.113.0 of its Python SDK, marking a notable expansion in the toolkit's capabilities for developers building applications with Claude. The update introduces support for web fetching functionality and tool integration through the newly supported 20260318 API model version, while also addressing technical debt through bug fixes and refinements to the token counting system.

## TL;DR

- **Web fetch and tools support**: The SDK now integrates with a newer API model that enables Claude to retrieve and process web content, expanding beyond text-only interactions
- **Token counting fixes**: Async token counting operations now properly merge output format specifications, resolving reliability issues
- **User profile integration**: The token counting system now accepts user profile identifiers, enabling more granular usage tracking and billing scenarios
- **Impact**: Developers can now build more sophisticated multi-modal applications where Claude can actively retrieve external information and execute tools, while enjoying more accurate token accounting for production deployments

## Background

Token counting has been a critical feature in the Anthropic SDK since its early releases, allowing developers to understand API costs before making requests and optimize prompt engineering. However, the async implementation of this feature lagged behind the synchronous version in important ways. The previous version's async `count_tokens` method didn't properly handle the merge of output formatting specifications, creating inconsistencies when developers attempted to predict token usage for structured output scenarios.

Meanwhile, Claude's capabilities have expanded significantly beyond pure text generation. The introduction of tool use in earlier SDK versions allowed developers to define functions that Claude could call, but the platform couldn't independently retrieve external information. Web fetching changes this equation—Claude can now proactively search for and integrate current information during conversations, a critical capability for applications requiring real-time data.

## How it works

### Web Fetch and Tool Support Through Updated API

The headline feature of v0.113.0 centers on support for the 20260318 API model version, which introduces integrated web fetching capabilities. Rather than requiring developers to build custom retrieval systems, Claude can now natively fetch web content when needed during conversations.

This works alongside the existing tool use framework. Previously, if an application needed Claude to access current information, developers had to either pre-fetch data and include it in the prompt, or implement a loop where Claude returns tool calls that the application must handle and feed back. With web fetch support, Claude can autonomously decide when to retrieve information from the internet, check current prices, verify recent news, or gather context—then incorporate these findings directly into responses.

The implementation maintains backward compatibility. Existing SDK users won't experience disruptions, but those targeting the new API version gain access to these enhanced capabilities. This gradual approach allows development teams to upgrade at their own pace while maintaining stability in production systems.

### Async Token Counting Refinement

The bug fix addressing async token counting resolves a subtle but important issue. When developers request token counts for scenarios involving structured outputs—where Claude returns responses in specific formats like JSON—the system needs to merge specifications for output formatting with other request parameters.

The async version was missing this merge operation in certain code paths, potentially returning incorrect token estimates. This matters because developers often rely on token counts for budget estimation and prompt optimization. An underestimate could lead to unexpected costs or rate-limiting surprises in production; an overestimate wastes optimization efforts.

The fix ensures parity between async and synchronous token counting, making the behavior consistent regardless of which implementation path a developer chooses. For applications built with async patterns—increasingly common in modern Python development—this delivers the accuracy they need.

### User Profile Support in Token Counting

A companion improvement adds user profile identifiers as parameters to the token counting system. This reflects Anthropic's recognition that different users within an organization might have different pricing tiers, quotas, or usage policies. By accepting profile IDs during token counting, developers can now calculate costs specific to a particular user before initiating expensive API calls.

This becomes particularly valuable in multi-tenant applications or platforms where cost allocation matters. A SaaS platform using Claude could now estimate what an API call will cost user A versus user B, enabling more sophisticated rate-limiting and usage tracking at the individual level rather than globally.

### Documentation and API Refinement

Beyond functional changes, the release includes documentation updates clarifying descriptions and example values across the SDK. This housekeeping matters more than it might appear—clear, accurate documentation reduces integration friction and helps developers implement features correctly on the first attempt, reducing support overhead and improving adoption.

## What happens next

Teams currently running production applications with the Anthropic Python SDK should evaluate whether the new web fetch capabilities align with their roadmap. If your application currently requires custom information retrieval systems, the built-in web fetch functionality could simplify architecture significantly. However, careful evaluation of web fetch behavior, latency implications, and relevance filtering will be important before adopting in latency-sensitive applications.

The token counting improvements are relatively low-risk upgrades that should be adopted broadly, particularly for teams relying on async patterns. The fixes eliminate a category of subtle bugs that could cause cost estimation errors.

For developers not yet on v0.113.0, updating represents a straightforward path to accessing Claude's newest capabilities while benefiting from reliability improvements. As always, thorough testing in development environments before production rollout remains essential practice.
*This article does not contain affiliate links.*
