---
category: sdk_release
date: '2026-06-20'
generated_at: '2026-06-20T05:22:59.452920Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/anthropic-sdk-python
source_url: https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.110.0
template_type: explainer
title: anthropics/anthropic-sdk-python v0.110.0
word_count: 770
---

# Anthropic SDK Python v0.110.0: Code Execution Capabilities and Infrastructure Refinements

Anthropic has released version 0.110.0 of its Python SDK, introducing support for a new code execution tool while addressing several underlying infrastructure issues. The update represents incremental but meaningful progress in the toolkit that developers use to integrate Claude AI models into their applications.

## TL;DR

- **Code execution tool**: New `code_execution_20260120` tool enables Claude to execute code as part of its reasoning process
- **Header handling fix**: Corrected how custom headers are merged during API requests, preventing previous values from being overwritten
- **Stream compatibility**: Fixed issues with AWS Bedrock integration where streaming event types were being corrupted
- **Impact**: Developers can now leverage more sophisticated AI reasoning patterns while experiencing more reliable API interactions

## Background

The Anthropic Python SDK serves as the primary interface for developers building applications with Claude. Like most SDKs, it undergoes regular updates to expose new API capabilities and fix bugs discovered in production use. The gap between v0.109.2 and v0.110.0 highlights Anthropic's focus on both feature expansion and quality assurance.

The addition of code execution capabilities represents a significant shift in how Claude can assist with computational tasks. Previously, Claude could analyze code and provide suggestions, but couldn't execute code directly within the API request-response cycle. This new tool changes that dynamic, allowing for more interactive and verification-driven workflows.

## How it works

### New Code Execution Tool

The `code_execution_20260120` tool enables Claude to write and execute Python code during conversations. When a user asks Claude to perform calculations, data transformations, or other computational tasks, the model can now use this tool to run the code and verify results before responding to the user.

This capability is particularly valuable for data analysis, mathematical computations, and debugging scenarios where executing code produces more reliable answers than pure reasoning. The tool uses a timestamp-based versioning scheme (20260120), suggesting it may evolve as Anthropic refines the implementation.

Developers integrating this tool need to handle both the code generation step and the execution response step. The SDK now provides proper marshaling and unmarshaling of code execution requests and responses through the API.

### Header Management Improvements

A subtle but important fix addresses how HTTP headers are handled during API requests. The previous implementation would "clobber" certain headers—overwriting them completely when merging new headers with existing ones. This was particularly problematic for the `x-stainless-helper` header, which tracks SDK usage patterns and helps Anthropic understand how developers interact with the API.

The corrected behavior now appends values to these headers instead of replacing them, creating a more complete audit trail. This appears to stem from the Stainless framework that generates parts of this SDK, ensuring consistency across multiple Anthropic language SDKs.

### AWS Bedrock Stream Compatibility

The Bedrock fix addresses an issue specific to developers using Amazon's Bedrock service to access Claude models. When streaming responses from Claude through Bedrock, the stream event type metadata was being corrupted or lost. This made it difficult for applications to properly handle different types of streaming events—like distinguishing between content blocks, usage information, and other event categories.

The fix preserves this metadata throughout the streaming lifecycle, allowing consuming applications to route and process different event types appropriately.

## What this means for practitioners

For developers using the Anthropic SDK, this release offers concrete benefits:

**Code execution workflows** become viable for applications requiring computational verification. Chatbots can now perform calculations, data scientists can use Claude to help clean datasets with executable code, and debugging assistants can test fixes in real-time.

**More reliable API integration** through proper header handling ensures that usage analytics and debugging information flow correctly to Anthropic's systems, which can help with support and troubleshooting when issues arise.

**Bedrock users** will experience more robust streaming behavior, particularly important for applications processing large responses where stream integrity is critical for proper data handling.

The fixes are backward compatible—existing code will continue to work without modification, though developers may want to upgrade to ensure they're not affected by the header and streaming bugs.

## What happens next

Developers should test the new code execution tool with their existing applications to understand how Claude's expanded capabilities might improve their use cases. The tool integrates seamlessly with the existing conversation API, so adoption is straightforward for current SDK users.

Organizations using Bedrock should prioritize this upgrade to resolve potential stream handling issues, particularly those processing large or complex responses that might be sensitive to data corruption.

As Anthropic continues refining these tools, the timestamp-based versioning of the code execution tool suggests more iterations may arrive as the capability matures and receives real-world testing.
*This article does not contain affiliate links.*
