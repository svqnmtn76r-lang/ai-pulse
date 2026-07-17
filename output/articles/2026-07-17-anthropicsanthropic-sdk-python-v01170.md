---
category: sdk_release
date: '2026-07-17'
generated_at: '2026-07-17T04:14:19.472459Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/anthropic-sdk-python
source_url: https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.117.0
template_type: explainer
title: anthropics/anthropic-sdk-python v0.117.0
word_count: 869
---

# Anthropic Python SDK v0.117.0: Dream Features and Enhanced Security

Anthropic has released version 0.117.0 of its Python SDK, introducing experimental dreaming capabilities and Model Context Protocol (MCP) tunnel support while strengthening credential security. The update reflects the growing sophistication of Claude's integration ecosystem and addresses critical security concerns in production environments.

## TL;DR

- **Dreaming support**: New experimental API enables Claude to explore creative problem-solving through simulated scenarios
- **MCP Tunnels**: Extends the Model Context Protocol with tunnel functionality for more flexible tool integration
- **Security hardening**: Credentials now protected from appearing in Python traceback frames, preventing accidental exposure
- **Impact**: Developers gain more expressive AI capabilities while enjoying stronger safeguards against credential leakage in debugging scenarios

## Background

The Anthropic Python SDK has evolved from a simple API wrapper into a comprehensive toolkit supporting Claude's increasingly complex features. As organizations deploy Claude in production environments, two complementary needs have emerged: expanded reasoning and task execution capabilities on one hand, and stronger security guarantees on the other.

MCP Tunnels build upon Anthropic's commitment to the Model Context Protocol, an open standard for connecting large language models with external tools and data sources. Earlier versions supported direct MCP connections; tunnels add flexibility for scenarios where direct connections aren't practical—think distributed systems or restricted network environments.

The credential security fix addresses a subtle but serious vulnerability class: Python tracebacks sometimes capture local variables in their frames, potentially exposing sensitive authentication material when errors occur and logs are collected.

## How it works

### Dreaming: Exploratory AI Reasoning

The most intriguing addition in this release is "dreaming" support—an experimental feature that enables Claude to simulate scenarios and explore solution spaces without executing real-world actions. Think of it as internal monologue for problem-solving.

Dreaming allows Claude to reason through complex problems by constructing hypothetical scenarios, testing approaches mentally before committing to specific actions. For applications like planning, strategy development, or complex decision-making, this creates a new mode of interaction where the model can show its working more explicitly. Rather than jumping directly to conclusions, Claude can articulate the exploration process itself.

From an API perspective, dreaming is exposed as a new parameter in the message creation workflow. Developers enable it when they want Claude to leverage this exploratory reasoning capacity, particularly useful for open-ended problems where the solution path isn't immediately obvious. The feature remains experimental, indicating Anthropic expects the interface and behavior to evolve based on developer feedback.

### MCP Tunnels: Flexible Tool Integration

Model Context Protocol Tunnels extend MCP's capabilities beyond direct connections. While standard MCP assumes the model and tools communicate directly over a single channel, tunnels decouple this architecture. They enable scenarios like:

- Tools running behind firewalls or in restricted networks accessing Claude through secure tunnels
- Distributed tool deployments where a single tunnel endpoint coordinates access to multiple backend services
- Cross-boundary tool access where tools span different security domains

The tunnel abstraction handles connection complexity transparently. Developers define tunnel endpoints and associate tools with them, letting Claude interact with those tools as though they were directly connected. This architectural flexibility addresses real deployment constraints that direct MCP connections don't accommodate.

For practitioners building Claude integrations at scale—particularly in enterprise environments with complex network topologies—tunnel support dramatically expands what's possible. It moves MCP from a primarily local-development pattern to something deployable in sophisticated production architectures.

### Credential Security: Protecting Secrets from Tracebacks

The security improvement implements a subtle but important protection mechanism. When Python code raises an exception, the traceback captures not just the call stack but also local variables at each frame. This design aids debugging but creates a vector for credential exposure: if an error occurs during authentication or API calls, the traceback frame might contain API keys, tokens, or other secrets.

The fix uses Pydantic's `SecretStr` type to wrap credential material within the SDK. `SecretStr` prevents the actual secret value from appearing in string representations, which Python's traceback system relies on. If an exception occurs, the traceback will show something like `***` instead of the actual credential, keeping sensitive material out of logs and error reports.

This is particularly important for applications deployed to centralized logging systems or error tracking services. Even with careful log sanitization, frame locals are easy to miss. Using `SecretStr` at the SDK level provides defense-in-depth protection regardless of downstream logging practices.

## What happens next

The experimental nature of dreaming suggests continued iteration. Developers should expect the dreaming API to evolve as Anthropic refines the feature based on usage patterns and feedback. Early adoption by adventurous teams will likely inform what becomes stable in future releases.

MCP Tunnels represent the maturation of MCP as a protocol. Expect broader ecosystem adoption as tool developers recognize tunnel support unlocks previously difficult deployment scenarios. This particularly benefits teams building agent frameworks and enterprise AI applications.

The credential security fix is immediately valuable but represents just one layer of protection. Teams should continue practicing defense-in-depth: limiting credential scope, rotating keys regularly, and using environment-specific authentication when possible.

Developers can explore these features by updating to v0.117.0 via pip and consulting Anthropic's documentation for usage examples. The experimental dreaming feature especially warrants experimentation to understand how it performs on your specific use cases.
*This article does not contain affiliate links.*
