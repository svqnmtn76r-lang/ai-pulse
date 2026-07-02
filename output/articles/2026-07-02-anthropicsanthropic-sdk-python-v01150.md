---
category: sdk_release
date: '2026-07-02'
generated_at: '2026-07-02T01:50:28.404047Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/anthropic-sdk-python
source_url: https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.115.0
template_type: explainer
title: anthropics/anthropic-sdk-python v0.115.0
word_count: 956
---

# Anthropic's Python SDK Gets Major Agent Streaming and Webhook Updates: What's New in v0.115.0

Anthropic has released version 0.115.0 of its Python SDK, introducing significant enhancements to agentic capabilities with a focus on real-time event streaming, operational flexibility, and system integration. The update represents a meaningful expansion of the framework's enterprise-readiness, particularly for teams building autonomous agent systems that require sophisticated event handling and third-party integrations.

## TL;DR

- **Event Delta Streaming**: Developers can now receive granular, real-time updates from Managed Agents as they execute, enabling more responsive client applications and better observability into agent behavior
- **Agent Overrides**: New configuration options allow runtime modifications to agent behavior without requiring redeployment, improving flexibility in multi-tenant and production environments
- **Reverse Pagination**: API queries now support backward iteration through results, addressing common use cases where the most recent data needs to be accessed first
- **Vault Credential Scoping**: Enhanced security controls let developers restrict credential injection to specific agent contexts, reducing attack surface and improving secrets management
- **Webhook Events**: Deployments and agents can now emit events through webhooks, enabling real-time notifications and integration with external systems
- **Impact**: These features collectively mature Anthropic's agent framework for production deployment scenarios, particularly in regulated industries and complex distributed systems where operational transparency and security controls are paramount

## Background

Anthropic's Managed Agents represent a shift toward frameworks where large language models can autonomously perform multi-step tasks with external tool integration. However, early versions faced limitations common to emerging agentic platforms: limited visibility into execution, inflexible configuration models, and insufficient security boundaries for sensitive credentials.

The Python SDK has evolved as the primary interface for developers integrating Claude's capabilities into applications. Previous iterations focused on core functionality—basic agent execution and tool calling. However, production deployments revealed gaps: operators couldn't observe agent execution granularly, teams struggled with credential management at scale, and audit trails remained incomplete.

This release directly addresses these operational concerns by layering enterprise features atop the existing agent framework.

## How it works

### Event Delta Streaming for Real-Time Agent Monitoring

Traditional agent execution returns final results after completion. Event delta streaming inverts this model: agents emit discrete events throughout their lifecycle, with clients receiving incremental updates as they occur.

This matters because agent execution involves multiple stages—planning, tool invocation, reasoning about results—and observing these intermediate states enables several capabilities. Client applications can display progress updates to users, implement dynamic timeout logic based on observed execution patterns, or terminate agents early when certain conditions are detected. For debugging, engineers gain insight into decision-making chains that would otherwise remain opaque.

The implementation streams events in delta format, meaning each message contains only what changed since the previous event. This reduces bandwidth, improves latency, and allows efficient client-side state management. A monitoring dashboard, for example, could update its UI incrementally rather than waiting for full execution completion.

### Agent Overrides for Runtime Configuration

Agent behavior is typically defined during creation: instructions, available tools, and system parameters. Overrides extend this model by allowing certain configurations to be modified at invocation time, without creating new agent definitions.

This proves valuable in multi-tenant scenarios where a base agent serves multiple customers with slightly different requirements. Rather than maintaining separate agent instances per tenant, a single agent can accept overrides specifying tenant-specific instructions or tool constraints. Similarly, A/B testing different agent behaviors becomes simpler—route requests to the same agent with different override parameters.

Overrides maintain backward compatibility: existing code invoking agents without overrides continues working unchanged. But new deployments can leverage this flexibility to reduce configuration complexity and improve operational agility.

### Reverse Pagination for Data Access Patterns

Standard pagination iterates forward: retrieve results 1-100, then 101-200, then 201-300. Reverse pagination inverts this, supporting backward iteration through datasets.

This addresses real-world access patterns where recent data takes priority. Audit logs, execution histories, and event streams often need reverse chronological access. Previously, developers had to fetch all results and reverse them locally, which proved inefficient for large datasets. Native reverse pagination eliminates this inefficiency by allowing the API to return results in reverse order directly.

### Vault Credential Injection Scoping

Credentials—API keys, database passwords, authentication tokens—represent security-sensitive information that agents sometimes need to access external systems. Credential injection allows agents to automatically include these secrets when making calls.

The new scoping mechanism restricts which agents can access which credentials. An agent handling customer support might only access customer database credentials, not payment processing credentials. This principle of least privilege reduces blast radius if an agent's instructions are compromised or behave unexpectedly.

Scoping works at multiple levels: credential injection can be restricted to specific agents, deployments, or operational contexts. This granularity enables security policies that align with organizational responsibility boundaries.

### Webhook Events for External Integrations

Agents and deployments now emit events through webhooks—HTTP callbacks to external systems when significant actions occur. An agent completing a task, encountering an error, or being invoked could trigger webhook notifications to monitoring systems, ticketing platforms, or custom business logic.

Webhook events enable real-time integration without continuous polling. An observability platform can immediately be notified when an agent deployment starts or stops. A workflow automation system can trigger subsequent tasks when agent execution completes. These integrations happen independently of the application code invoking the agent, improving separation of concerns.

## What happens next

Teams building production agent systems should evaluate whether these features address operational gaps in their current deployments. Event delta streaming particularly benefits applications with user-facing progress indicators or sophisticated error handling. Credential scoping should be prioritized for any agent touching sensitive data or multiple external systems.

The release suggests Anthropic's product roadmap increasingly emphasizes operational maturity over pure capability expansion, signaling that the company views agentic systems as approaching production readiness in mainstream enterprise environments.
*This article does not contain affiliate links.*
