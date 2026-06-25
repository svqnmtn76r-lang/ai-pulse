---
category: sdk_release
date: '2026-06-25'
generated_at: '2026-06-25T05:11:57.342476Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/anthropic-sdk-python
source_url: https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.112.0
template_type: explainer
title: anthropics/anthropic-sdk-python v0.112.0
word_count: 742
---

# Anthropic Python SDK v0.112.0: Enhanced Streaming and Improved File Handling

Anthropic has released version 0.112.0 of its Python SDK, introducing new streaming capabilities and addressing file system reliability issues. The update focuses on improving real-time communication with Claude AI models and fixing a critical bug in the memory tool that could cause permission errors during file operations.

## TL;DR

- **System message streaming**: The SDK now supports streaming events for system messages, allowing developers to process AI responses in real-time as they're generated
- **Permission fixes**: A bug in the memory tool that created directories with incorrect permissions has been resolved
- **Profile identification**: The SDK can now include User Profile IDs in request headers for better request tracking and analytics
- **Impact**: Developers building interactive applications will see more responsive UX, while file-based memory implementations become more reliable across different system configurations

## Background

Real-time streaming has become increasingly important in AI applications, where latency directly affects user experience. Previously, the Anthropic Python SDK supported streaming for various event types, but system message events—messages that influence the model's behavior—were handled differently from user and assistant message streams. This gap meant developers working on complex, multi-turn conversations couldn't leverage streaming's benefits for all message types.

The memory tool bug represents a common pain point in cross-platform Python development. When the SDK creates directories to store conversation memory or other persistent data, it must handle permission inheritance correctly. Incorrect permissions can cascade into runtime failures, especially in containerized environments or shared hosting scenarios where directory permissions are strictly controlled.

## How it works

### System Message Streaming Events

The primary feature in this release enables streaming for system.message events. System messages in Claude interactions serve as instructions or context that shape how the model responds. Unlike typical user or assistant messages that represent conversational turns, system messages define the operational parameters for the entire interaction.

With streaming support, developers can now observe system message events as they occur rather than waiting for complete buffering. This is particularly valuable in scenarios where system messages are dynamically generated based on runtime conditions. Applications can now process these events immediately, enabling responsive UI updates and real-time logging without artificial delays.

The implementation follows Anthropic's existing streaming architecture, maintaining consistency with how other message types are streamed. This means developers already familiar with the SDK's streaming patterns will find the new functionality intuitive to integrate.

### File System Reliability Improvements

The memory tool bug fix addresses directory creation during initialization. The tool creates parent directories when storing memory artifacts, but was previously setting permissions that didn't match the system's umask or inherited permissions correctly. This caused failures when the SDK ran in environments with restrictive umask settings or specific permission requirements.

The fix ensures directories are created with appropriate permissions that respect the parent directory's configuration and the system's security policies. This is especially important in production deployments where strict permission hierarchies prevent privilege escalation vulnerabilities.

### Request Header Enhancement

The SDK now supports sending User Profile IDs in request headers. This capability enables better attribution and tracking of API requests back to specific user profiles in applications serving multiple users. It's a foundational feature for SaaS applications and multi-tenant systems that need granular analytics about API usage patterns and user behavior.

## What happens next

This update addresses immediate pain points in streaming and file operations, but the broader trend suggests Anthropic continues refining its Python SDK based on developer feedback. The addition of User Profile ID support hints at expanding enterprise capabilities, likely reflecting increased demand from production deployments managing multiple users.

Developers using the memory tool in production should prioritize upgrading to address the permission bug, particularly if running in containerized or shared hosting environments. Those building real-time interactive applications with dynamic system prompts will benefit from testing the new system message streaming capabilities.

The refusal category support mentioned in the changelog indicates ongoing work on content policy enforcement, suggesting future releases may bring more granular control over how the SDK handles requests that violate usage policies.

**For developers**: Update your projects to v0.112.0 and review how system messages are handled in your streaming implementations. Consider whether the new streaming support enables simpler or more responsive code patterns in your current architecture.

**For operators**: If you're running the memory tool in production, test the permission fix in your specific deployment environment before rolling out broadly. The change improves reliability across different system configurations.
*This article does not contain affiliate links.*
