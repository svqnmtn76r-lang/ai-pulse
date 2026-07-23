---
category: sdk_release
date: '2026-07-23'
generated_at: '2026-07-23T04:22:48.032044Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/anthropic-sdk-python
source_url: https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.118.0
template_type: explainer
title: anthropics/anthropic-sdk-python v0.118.0
word_count: 786
---

# Anthropic's Python SDK Gets Managed Agents Upgrade: What's New in v0.118.0

Anthropic has released version 0.118.0 of its Python SDK, introducing significant capabilities for developers working with Managed Agents. The update brings three substantial features designed to enhance agent control, session management, and real-time data streaming—areas critical for building production-grade AI applications.

## TL;DR

- **Model Effort Control**: Developers can now specify computational resource allocation for Managed Agents, enabling fine-grained performance tuning
- **Initial Session Events**: New session initialization events provide deeper visibility into agent startup and configuration
- **Threads Delta Streaming**: Real-time incremental updates to conversation threads reduce latency and improve user experience
- **Impact**: These additions mature the SDK's agent capabilities, moving them closer to production readiness for complex, multi-turn AI applications

## Background

Anthropic's Managed Agents represent a shift in how developers interact with Claude. Rather than manually orchestrating prompts and conversation flows, developers can delegate agent management to Anthropic's infrastructure. However, early versions lacked fine-grained control over how much computational effort agents expended on tasks.

The Python SDK has been steadily evolving to match feature parity with Anthropic's core API. Previous releases focused on basic agent creation and message passing. This update signals a maturation phase, addressing pain points that emerge when moving from prototypes to production systems: resource optimization, debugging visibility, and performance optimization through streaming.

## How it Works

### Model Effort Configuration

The new "model effort" parameter lets developers specify how intensively an agent should work on a given task. Think of it as a dial controlling the computational resources—similar to how you might set inference parameters like temperature, but specifically for planning and reasoning depth.

This addresses a common challenge in AI applications: the trade-off between quality and latency. A developer building a customer support chatbot might use lower effort for simple FAQ-style responses while allocating maximum effort for complex problem-solving. The parameter integrates directly into agent initialization, allowing per-request or per-session configuration.

Technically, this translates to Claude allocating different amounts of tokens and reasoning steps during the agent's planning phase. Higher effort settings make agents more thorough but slower; lower settings optimize for speed. This gives developers explicit control rather than leaving computational intensity as a black box.

### Initial Session Events

When an agent session starts, numerous initialization processes occur behind the scenes—loading context, validating permissions, initializing memory structures. Previously, developers received minimal visibility into this startup phase.

The new initial session events expose this process, providing structured information about what's happening during session creation. This matters for several reasons: debugging connection issues, understanding why a session took longer than expected, and ensuring proper agent configuration before messages arrive.

These events are particularly valuable in production environments where you're running multiple agents concurrently. Observability into session initialization helps identify bottlenecks and catch misconfiguration early. Developers can now log or monitor these events, creating better alerting systems and performance dashboards.

### Threads Delta Streaming

Delta streaming represents a pattern shift in how conversation data flows to applications. Rather than waiting for a complete message to finish before transmitting it, delta streaming sends incremental updates—each token or logical chunk arrives as soon as it's generated.

For conversation threads (Anthropic's term for multi-turn conversations), this means developers no longer wait for an entire agent interaction to complete. Instead, they receive streaming updates to the thread state—new messages appear character by character, thoughts accumulate in real time, and tool calls are visible as they're invoked.

This particularly benefits user-facing applications. Instead of users staring at a loading spinner while waiting for a complex agent to finish its work, they see progress in real time. The UX improves substantially, especially for longer operations. Technically, this requires websocket connections or server-sent events (SSE) rather than simple HTTP polling, which the SDK now handles transparently.

## Technical Integration

For developers, these features integrate into existing workflows with minimal friction. Model effort appears as an optional parameter during agent creation or message submission. Initial session events are accessible through standard event handlers that developers already use for other agent lifecycle events. Delta streaming works automatically when enabled, with the SDK handling the underlying protocol complexity.

The release maintains backward compatibility—existing code continues functioning without modification. These are strictly additive features that developers adopt when their use cases demand them.

## What Happens Next

This release positions Anthropic's Python SDK closer to supporting enterprise-grade agent deployments. The combination of resource control, operational visibility, and performance optimization addresses core requirements for production systems.

Developers interested in upgrading should review the changelog details at the GitHub repository. For those building multi-agent systems or deploying agents to production, these features warrant immediate evaluation. The model effort parameter alone could significantly reduce infrastructure costs by right-sizing computational allocation.
*This article does not contain affiliate links.*
