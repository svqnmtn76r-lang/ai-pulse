---
category: other
date: '2026-05-22'
generated_at: '2026-05-22T21:48:36.862903Z'
generated_by: claude-haiku-4-5-2026-05-22
importance_score: 50
products: []
source_name: github:anthropics/anthropic-sdk-python
source_url: https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.104.1
template_type: breaking
title: anthropics/anthropic-sdk-python v0.104.1
word_count: 369
---

## TL;DR

- **Bug Fix**: Anthropic patched a streaming data handling issue in its Python SDK affecting encrypted content preservation
- **Impact**: Developers using beta features for message streaming can now reliably maintain encrypted payload integrity
- **Release**: v0.104.1 is now available for immediate deployment

## What happened

Anthropic released version 0.104.1 of its Python SDK on May 21, addressing a critical bug in the streaming message pipeline. The issue centered on encrypted content data being lost during beta feature compaction operations—a process that optimizes streamed responses by consolidating multiple event fragments.

The specific problem occurred when the SDK's streaming accumulator, which assembles partial message chunks into complete responses, failed to properly carry encrypted_content through compaction cycles. This meant developers relying on encryption features during real-time message streaming could experience data loss or corruption, potentially compromising security guarantees.

The one-line fix (commit f7a720c) ensures encrypted payloads are properly threaded through the compaction accumulator, preserving data integrity across the streaming pipeline. For teams building applications that depend on streaming responses with encryption enabled, this patch eliminates a potential vector for silent data degradation.

The fix was isolated to streaming operations within beta features, suggesting Anthropic is actively iterating on experimental functionality while maintaining backward compatibility. The minimal changelog indicates this was a surgical fix rather than a broader architectural change.

## Why this matters

For developers integrating Anthropic's Claude API at scale, streaming represents a critical performance pattern—allowing real-time token delivery rather than waiting for complete response generation. Adding encryption to this flow introduces additional complexity, particularly around state management. This patch resolves a gap where that complexity could cause failures.

Organizations processing sensitive data through streaming channels should prioritize upgrading to ensure compliance with their data protection requirements. The fix directly impacts reliability for production workloads using encrypted streaming features.

## What happens next

Developers should update their dependencies to v0.104.1 immediately if they're using streaming APIs with encryption features. The patch is backward compatible and requires no code changes on the consumer side.

For ongoing tracking of SDK updates, monitor the [anthropic-sdk-python GitHub repository](https://github.com/anthropics/anthropic-sdk-python), where Anthropic publishes releases and maintains detailed changelogs. The full diff between v0.104.0 and v0.104.1 is available for those requiring detailed review before deployment.
*Disclosure: This article contains affiliate links. As an affiliate, we earn from qualifying purchases at no extra cost to you.*
