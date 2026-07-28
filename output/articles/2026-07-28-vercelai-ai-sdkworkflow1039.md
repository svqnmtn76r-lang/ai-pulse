---
category: sdk_release
date: '2026-07-28'
generated_at: '2026-07-28T04:16:49.610433Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:vercel/ai
source_url: https://github.com/vercel/ai/releases/tag/%40ai-sdk/workflow%401.0.39
template_type: explainer
title: vercel/ai @ai-sdk/workflow@1.0.39
word_count: 903
---

# AI SDK Workflow Gets Enhanced Tool Configuration in Latest Update: What You Need to Know

Vercel has released version 1.0.39 of its AI SDK Workflow package, introducing several refinements to how developers define and manage AI agent tools. The update focuses on improving flexibility and consistency in tool configuration, addressing developer feedback about streamlining workflow setup and execution patterns.

## TL;DR

- **Dynamic tool descriptions**: Tools can now have descriptions that adapt based on runtime context, rather than being static strings
- **Stream instructions and prepare inputs**: New capabilities for controlling initial data flow and setup steps in workflow execution
- **Configuration parity**: The `prepareCall` setting now works consistently across different workflow components
- **Simplified overrides**: Developer-facing API for step preparation has been refactored to reduce boilerplate and cognitive overhead
- **Impact**: These changes make it easier to build sophisticated AI agents that need context-aware tool selection and more granular control over execution stages

## Background

The AI SDK Workflow represents Vercel's approach to building structured, multi-step AI agent systems. Unlike simple prompt-completion patterns, workflows allow developers to define complex agent behaviors where large language models interact with multiple tools, databases, and external services in a coordinated fashion.

Previous versions of the workflow package provided basic tool integration, but developers working on production agents frequently encountered limitations. Tool descriptions were typically hardcoded at definition time, making it difficult to customize tool availability or presentation based on user context, request metadata, or runtime state. Additionally, the setup and execution phases of workflows lacked consistent configuration patterns, requiring different approaches depending on whether developers wanted to customize initial inputs or prepare function calls.

This update represents an iterative refinement rather than a major architectural shift—the kind of incremental improvement that accumulates into significantly better developer experience over time.

## How It Works

### Dynamic Tool Descriptions

One of the more practical improvements in this release addresses a real-world pain point: tools often need different descriptions depending on context. Consider an e-commerce agent that accesses different product catalogs based on user region, or a document search tool that should describe different capabilities based on available data sources.

Previously, developers had to either define multiple versions of the same tool or implement workarounds at the prompt level to convey context-dependent capabilities. The new dynamic description support allows tool definitions to compute descriptions at runtime. This means the LLM receives accurate information about what a tool can actually do in the current execution context, improving decision-making quality and reducing hallucinations where the model assumes capabilities the tool doesn't currently have.

This is particularly valuable for multi-tenant systems where different users have access to different features, or systems where tool capabilities degrade gracefully when upstream services are unavailable.

### Stream Instructions and Prepare Step Inputs

The addition of stream instructions and initial `prepareStep` inputs provides finer-grained control over workflow initialization. Stream instructions allow developers to send guidance or context to the LLM before tool selection begins, effectively priming the agent's behavior without modifying the system prompt.

The `prepareStep` inputs feature enables data to flow into workflow steps at initialization time, rather than only through tool calls or previous step outputs. This is useful for injecting configuration, user context, or cached data that should be available to all subsequent steps without requiring explicit tool invocations. For example, you might prepare a step with the current user's permissions, timezone, or feature flags, making this information immediately available to any tools that step executes.

### PrepareCall Setting Parity

Previously, the `prepareCall` configuration option—which allows developers to intercept and modify function calls before execution—worked inconsistently across different workflow components. Some parts of the system respected it while others didn't, creating confusion and requiring defensive coding patterns.

This update brings consistency by ensuring `prepareCall` works uniformly across all relevant workflow components. This means developers can now confidently implement cross-cutting concerns like logging, cost tracking, permission validation, or call modification in a single location, knowing the configuration will apply everywhere.

### Simplified PrepareStep Overrides

The refactoring of `prepareStep` overrides removes unnecessary complexity from the API. Developers frequently needed to override step preparation logic to implement custom initialization, but the previous API required understanding multiple abstraction layers and override points.

The simplified approach consolidates these into a cleaner interface that's easier to reason about and reduces the code needed for common customization patterns. This is reflected in both the framework's internal implementation and how developers interact with it.

## Dependency Updates

The release includes updated dependencies for `@ai-sdk/provider-utils` (bumped to 5.0.14) and the core `ai` package (5.0.14 to 5.0.39). These updates typically contain bug fixes, performance improvements, and compatibility updates for the various AI model providers that Vercel's SDK supports.

## What Happens Next

These improvements set the foundation for more advanced agent patterns. As the workflow system matures, expect to see higher-level abstractions and templates that leverage these capabilities—pre-built agent architectures for common use cases like customer support, document analysis, or code generation.

For developers currently using the AI SDK, evaluating these features makes sense if you're building agents that need context awareness, complex initialization logic, or precise control over tool selection. The changes are backward compatible, so existing code continues working while new patterns become available to those who need them.

Start by reviewing your current tool definitions to identify places where dynamic descriptions would improve agent decision-making, then explore using `prepareStep` inputs to simplify how you manage context flow through multi-step workflows.
*This article does not contain affiliate links.*
