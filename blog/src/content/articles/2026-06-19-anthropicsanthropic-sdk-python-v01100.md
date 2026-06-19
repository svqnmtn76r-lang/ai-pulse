---
category: sdk_release
date: '2026-06-19'
generated_at: '2026-06-19T06:26:38.007836Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/anthropic-sdk-python
source_url: https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.110.0
template_type: explainer
title: anthropics/anthropic-sdk-python v0.110.0
word_count: 848
---

# Anthropic's Python SDK v0.110.0: Code Execution Capabilities Expand with New Tool Support

Anthropic has released version 0.110.0 of its Python SDK, marking another incremental update to the widely-used library that enables developers to integrate Claude AI models into Python applications. The release introduces support for a new code execution tool while addressing several underlying technical issues that affect how the SDK communicates with Anthropic's API infrastructure.

## TL;DR

- **New code execution tool**: The SDK now supports the `code_execution_20260120` tool, enabling more sophisticated AI-driven code generation and execution workflows
- **Header management improvements**: Bug fixes address how the SDK handles HTTP headers during API requests, preventing critical metadata from being lost during header merges
- **Bedrock compatibility**: AWS Bedrock integration now correctly preserves stream event types, ensuring proper data handling in streaming scenarios
- **Impact**: Developers using code generation features, custom integrations, or streaming APIs will see improved reliability and expanded capabilities

## Background

The Anthropic Python SDK serves as the primary interface for developers building applications with Claude, Anthropic's large language model. Since its initial release, the SDK has evolved to support various deployment scenarios, from direct API calls to cloud provider integrations like AWS Bedrock. Each update typically balances two competing priorities: introducing new capabilities aligned with Claude's evolving features, and fixing subtle bugs that emerge from real-world usage patterns.

The code execution tool represents a natural extension of Claude's abilities. As language models become increasingly capable at writing code, the infrastructure supporting that capability must mature alongside it. The `code_execution_20260120` designation suggests this is a refined version of earlier code execution implementations, incorporating lessons learned from previous iterations.

## How it works

### Code Execution Tool Integration

The primary feature addition in v0.110.0 brings formal SDK support for the `code_execution_20260120` tool. This tool enables Claude to not merely suggest code, but to execute it in a controlled sandbox environment and receive results that inform subsequent responses.

This capability transforms Claude from a code suggestion engine into something more interactive. When a developer enables this tool in their API calls, Claude can write Python code, execute it within Anthropic's secure infrastructure, and access the output—all within a single conversation. This proves particularly valuable for data analysis tasks, mathematical computations, and scenarios where code correctness can be verified immediately rather than assumed.

The naming convention `20260120` likely represents a version identifier using the format YYYYMMDD, suggesting this tool implementation was finalized on January 20, 2026. This precision in versioning helps developers track which specific tool version they're working with, important for reproducibility and debugging.

### Header Management and API Reliability

Behind the scenes, v0.110.0 addresses a subtle but important bug affecting how HTTP headers are merged during API requests. The issue centers on the `x-stainless-helper` header, internal metadata that Anthropic uses for instrumentation and debugging purposes.

Previously, when the SDK needed to merge headers from different sources—perhaps combining user-specified headers with SDK defaults—the merge operation could inadvertently "clobber" or overwrite the `x-stainless-helper` header rather than append to it. This meant diagnostic information was lost, making it harder for both developers and Anthropic engineers to trace issues through the system.

The fix implements a smarter merge strategy that preserves all `x-stainless-helper` values across multiple header objects. Additionally, the update establishes a single source of truth for this header key and defines a closed vocabulary for its values, preventing inconsistent or malformed entries from polluting the instrumentation stream.

### Bedrock Stream Event Integrity

AWS Bedrock, Amazon's managed service for accessing multiple AI models including Claude, integrates with the Anthropic SDK through a compatibility layer. When developers use Bedrock instead of calling Anthropic's API directly, they gain AWS's security, compliance, and infrastructure benefits.

The v0.110.0 release fixes an issue where streaming responses through Bedrock would lose track of event type information. In streaming scenarios, the API delivers responses incrementally, with each chunk labeled by its event type—perhaps "content_block_delta" for new text, or "message_stop" for completion. This metadata helps developers route incoming data to the appropriate handlers.

The bug caused these event type labels to be dropped or misassigned during Bedrock integration. The fix ensures event types remain intact throughout the streaming pipeline, allowing applications to properly handle each chunk according to its semantic meaning rather than falling back to heuristics or causing parsing errors.

## What happens next

For most developers, upgrading to v0.110.0 is straightforward: update the package via pip and existing code should continue working unchanged. Those specifically interested in code execution can begin exploring the new tool by including it in their model requests.

The header management fix particularly benefits large-scale deployments or those requiring detailed API diagnostics. Teams that have been troubleshooting mysterious issues in production should note that improved header tracking may surface previously invisible problems, providing opportunities to strengthen system reliability.

The Bedrock improvements are essential for teams standardizing on AWS infrastructure, eliminating a potential source of data loss in production streaming pipelines.

As Anthropic continues maturing Claude's capabilities, expect continued iterations on code execution safety, availability, and integration breadth. The Python SDK will remain the primary vehicle for these improvements reaching developers.
*This article does not contain affiliate links.*
