---
category: sdk_release
date: '2026-06-30'
generated_at: '2026-06-30T01:49:41.114107Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/anthropic-sdk-python
source_url: https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.113.0
template_type: explainer
title: anthropics/anthropic-sdk-python v0.113.0
word_count: 787
---

# Anthropic's Python SDK v0.113.0: Enhanced Web Capabilities and Token Counting Improvements

Anthropic has released version 0.113.0 of its Python SDK, bringing expanded web integration features and critical bug fixes to its developer toolkit. This update introduces support for newer API models with web fetch and tools capabilities, while addressing a significant issue affecting asynchronous token counting operations.

## TL;DR

- **Web Fetch and Tools Support**: The SDK now supports the 20260318 model variant, enabling Claude to fetch and process web content directly within API calls
- **Async Token Counting Fix**: Resolved a bug where asynchronous token counting operations weren't properly merging output format configurations, which could lead to incomplete API requests
- **User Profile Integration**: Added support for user profile IDs when calculating token usage, enabling more granular usage tracking
- **Impact**: Developers working with web-aware Claude deployments can now leverage these capabilities through the Python SDK, with more reliable token estimation for async workflows

## Background

The Anthropic Python SDK serves as the primary interface for developers integrating Claude AI models into applications. Token counting—the process of estimating how many tokens a message will consume—is critical for cost management and rate limiting in production systems. The async variant of this function had fallen out of sync with recent API changes, creating potential issues for applications relying on non-blocking token calculations.

Web integration represents a significant capability expansion for Claude. By enabling models to fetch and interpret web content, developers can build applications that reference real-time information, access external APIs, and process live web pages without requiring intermediate preprocessing steps.

## How it works

### Web Fetch and Tools Support

The latest update brings compatibility with the 20260318 model version, which includes enhanced web capabilities. This enables Claude to autonomously fetch web content and utilize tools within a single API call. Rather than developers manually retrieving web content and feeding it to the model, Claude can now request web pages and parse them as part of its reasoning process.

This feature works through Anthropic's tools interface, where Claude can invoke web fetch operations similar to how it might call other external functions. The Python SDK now properly exposes these capabilities, allowing developers to define web fetch permissions and let Claude determine when web access is necessary to answer user queries. This is particularly valuable for applications requiring current information—news aggregators, financial analysis tools, or research assistants—where stale information significantly impacts usefulness.

### Asynchronous Token Counting Fix

A previously undetected bug affected developers using the async version of the token counting endpoint. When applications called the asynchronous count_tokens method, the function wasn't properly merging output format and output configuration parameters. This meant that token estimates could be incomplete or inaccurate if developers specified custom output formatting preferences.

The fix ensures that both synchronous and asynchronous token counting paths handle these parameters identically. For teams running production applications that process requests asynchronously—which is standard practice in scalable deployments—this correction prevents unexpected token consumption patterns and more accurate billing predictions. Async operations are increasingly common in modern Python applications using frameworks like FastAPI or asyncio, making this fix particularly timely.

### User Profile ID Integration

The chore update adding user profile ID support to token counting operations enables more sophisticated usage tracking. In enterprise environments where multiple users or teams share API quotas, being able to attribute token consumption to specific user profiles allows for granular billing, quota management, and usage analytics. The SDK now accepts these profile identifiers during token estimation, enabling organizations to forecast costs more accurately per user or team without waiting until actual API calls are made.

## Technical Implementation Details

The SDK maintains backward compatibility with these changes—existing code continues to function without modification. The web fetch support appears as opt-in functionality through the tools parameter, allowing developers to explicitly enable web capabilities when needed. The async token counting fix is transparent, requiring no code changes while improving accuracy.

Documentation updates accompanying this release clarify behavior and provide example values for new parameters, reducing friction for developers implementing these features. The combination of new capabilities and reliability improvements reflects Anthropic's pattern of incremental SDK enhancement, where each release adds functionality while maintaining stability.

## What happens next

Developers should review their token counting implementations, particularly those using async operations, to ensure they're receiving accurate estimates after this update. Teams planning to build web-aware applications can now explore the 20260318 model variant through the updated Python SDK. For enterprise deployments, the user profile ID support in token counting enables more sophisticated cost allocation and quota management strategies going forward.

Anthropic continues regular SDK updates that align with underlying API improvements, so staying current with releases ensures access to the latest model capabilities and reliability enhancements.
*This article does not contain affiliate links.*
