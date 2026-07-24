---
category: sdk_release
date: '2026-07-24'
generated_at: '2026-07-24T04:22:42.168625Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/anthropic-sdk-python
source_url: https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.118.0
template_type: explainer
title: anthropics/anthropic-sdk-python v0.118.0
word_count: 826
---

# Anthropic SDK Python v0.118.0: Enhancing Managed Agents with Streaming and Control Features

Anthropic has released version 0.118.0 of its Python SDK, introducing significant enhancements to its Managed Agents capabilities. This update focuses on expanding how developers can monitor, control, and interact with AI agents in production environments through improved streaming mechanisms and session management features.

## TL;DR

- **Model Effort Control**: New support for specifying computational effort levels in Managed Agents, allowing developers to balance speed and reasoning capability
- **Initial Session Events**: Early visibility into agent session state and configuration when conversations begin
- **Threads Delta Streaming**: Real-time incremental updates to agent thread activity, enabling responsive client applications
- **Impact**: Developers building production AI agent systems gain finer-grained control over agent behavior and better observability into agent execution

## Background

Managed Agents represent Anthropic's approach to handling complex, multi-step AI workflows where Claude operates autonomously within defined boundaries. Previous SDK versions provided basic agent functionality, but lacked granular control over resource allocation and limited streaming capabilities for monitoring agent behavior in real-time.

The challenge developers faced was twofold: first, understanding what an agent was doing when it started processing a request; and second, receiving updates about agent progress without waiting for complete task completion. These limitations made it harder to build responsive applications and optimize computational costs.

This release addresses these gaps by introducing three interconnected features that improve visibility and control over agent operations.

## How it works

### Model Effort and Computational Resource Management

The new model effort parameter allows developers to explicitly configure how much computational resources Claude should dedicate to reasoning within a Managed Agent. This represents a practical implementation of effort-based inference—a concept where models can allocate different levels of thinking capacity based on task complexity and requirements.

In practice, developers can now specify effort levels when initializing or calling Managed Agents, enabling them to optimize for different scenarios. A straightforward customer service query might use minimal effort, routing to a faster response path, while complex analytical tasks could request maximum effort, triggering deeper reasoning. This granular control helps organizations manage API costs while maintaining quality for high-stakes decisions.

The effort parameter integrates with Anthropic's existing model capabilities, allowing the underlying Claude model to adjust its inference strategy accordingly. This isn't simply a timeout mechanism—it's a semantic instruction to the model about how to allocate its computational budget.

### Initial Session Events for Immediate Context

When a Managed Agent begins processing, developers now receive initial session events that provide immediate context about the agent's state and configuration. This addresses a critical gap in observability: previously, developers had limited insight into what an agent was doing during its startup phase.

These events fire as soon as a session initializes, providing metadata about the agent's tools, system configuration, and initial parameters. For developers building monitoring dashboards or logging systems, this means they can track agent lifecycle from the very beginning rather than waiting for the first substantive action event.

The practical benefit is clearer audit trails and better debugging capabilities. If an agent session fails, developers can now examine what configuration state existed at initialization time, making root cause analysis significantly easier.

### Threads Delta Streaming for Real-Time Updates

Threads delta streaming represents a shift toward truly streaming agent updates. Rather than receiving complete state snapshots or waiting for operations to complete, developers now receive incremental changes—deltas—to agent thread state as they occur.

This streaming approach mirrors advances in other domains like real-time collaborative editing, where sending only changes rather than full states improves efficiency and responsiveness. For Managed Agents, this means client applications can update their UI or trigger reactions to agent progress immediately, rather than polling or waiting.

Developers receive delta events describing what changed in the agent's thread—new messages added, state modifications, or metadata updates. Applications can reconstruct full thread state by applying these deltas sequentially, or simply react to specific change types.

## Practical Implementation Considerations

These features work together to provide developers with a complete control and observability story for Managed Agents. When initializing an agent with effort parameters, initial session events immediately surface the agent's running configuration. As the agent executes, threads delta streaming provides real-time updates without overwhelming applications with redundant information.

The SDK update maintains backward compatibility—existing code continues working, while new parameters and event types are optional. Developers can adopt these features incrementally, starting with effort control to optimize resource usage, adding initial event handling for better logging, and finally implementing delta streaming for fully responsive applications.

## Learn more

Developers using Anthropic's Python SDK should consult the updated documentation for specific guidance on implementing these features. The GitHub repository contains implementation examples and detailed API documentation for model effort parameters, session event handling, and delta streaming subscription patterns.

These enhancements reflect Anthropic's focus on production-grade AI agent tooling, addressing real-world needs around observability, cost management, and application responsiveness that emerge as developers move beyond simple chat interfaces to complex agentic workflows.
*This article does not contain affiliate links.*
