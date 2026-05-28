---
category: sdk_release
date: '2026-05-28'
generated_at: '2026-05-28T05:38:07.671981Z'
generated_by: claude-haiku-4-5-2026-05-28
importance_score: 80
products: []
source_name: github:langchain-ai/langchain
source_url: https://github.com/langchain-ai/langchain/releases/tag/langchain%3D%3D1.3.2
template_type: explainer
title: langchain-ai/langchain langchain==1.3.2
word_count: 914
---

# LangChain 1.3.2 Release: Enhanced Middleware, Security Improvements, and Dependency Updates

LangChain, the popular framework for building AI applications with large language models, has released version 1.3.2. This incremental update focuses on middleware enhancements, security improvements around personally identifiable information (PII) handling, and critical dependency updates. The release comes as developers increasingly rely on middleware patterns to control agent behavior and data processing pipelines.

## TL;DR

- **PII Redaction in Streaming**: New capability to automatically redact sensitive information as it streams through middleware, addressing privacy concerns in real-time applications
- **Enhanced Agent Control**: The TodoListMiddleware now properly captures final answers in AI messages, improving agent orchestration and task completion tracking
- **Stream Transformation Registration**: Developers can now register custom stream transformers directly on middleware, enabling greater flexibility in data processing pipelines
- **Impact**: These changes make LangChain safer for production deployments handling sensitive data while improving control over agent execution flow

## Background

Middleware has become increasingly important in LangChain applications as developers build more complex agent systems. Middleware provides a mechanism to intercept and modify messages flowing through AI agents, enabling logging, validation, and transformation at critical points. However, two persistent challenges have limited wider adoption: difficulty managing sensitive data in streaming contexts and limited flexibility in how stream processing hooks are registered.

The previous release, 1.3.1, established the foundational middleware architecture. Version 1.3.2 builds on this foundation by addressing specific pain points that teams encounter when deploying LangChain agents to production environments where data privacy and execution control matter significantly.

## How it Works

### PII Redaction in Flight with PIIMiddleware

The most significant feature addition is the ability to redact personally identifiable information directly within the PIIMiddleware as data streams through the system. Previously, PII detection was largely a post-hoc analysis step, meaning sensitive information would flow through the application before being identified and logged.

The new streaming redaction capability intercepts data at the middleware layer before it reaches downstream consumers. This works by analyzing message content as it streams—whether that's token-by-token output from language model calls or structured data flowing between agents. When potential PII is detected (names, email addresses, phone numbers, social security numbers, etc.), the middleware redacts it in real-time rather than storing it for later filtering.

This approach provides several practical benefits. First, it reduces the window of exposure for sensitive data. Second, it simplifies compliance with regulations like GDPR and HIPAA by ensuring data never persists in logs or memory in unredacted form. Third, it integrates seamlessly into existing LangChain applications without requiring architectural changes to downstream components.

### TodoListMiddleware Final Answer Handling

The TodoListMiddleware, used for managing structured task lists in agent workflows, received a critical fix in this release. Previously, when an agent completed its work and generated a final answer, this conclusion wasn't always properly captured within the AIMessage object that tracks agent responses.

This fix ensures the final answer gets landed directly in the last AIMessage, which is crucial for downstream systems that parse agent responses. Applications relying on TodoListMiddleware for project management, task automation, or structured planning workflows benefit from this improvement because they can now reliably extract completion status and final results without additional post-processing logic.

### Stream Transformer Registration on Middleware

Version 1.3.2 introduces the ability to register stream transformers directly on middleware objects. Stream transformers are functions that modify how data flows through the system—they can filter messages, batch them, aggregate results, or apply custom logic to message sequences.

Previously, developers had to manage stream transformers separately from their middleware configuration, creating additional coupling and making code harder to maintain. By allowing registration directly on middleware, LangChain enables a more composable and testable architecture. Developers can now package data transformation logic alongside the middleware that uses it, improving code organization and reducing context switching when debugging pipeline issues.

### Dependency Ecosystem Updates

The release bumps the required LangGraph version to 1.3.2 or higher. LangGraph, LangChain's companion library for building graph-based agent workflows, provides critical orchestration capabilities. The version constraint ensures compatibility between the core LangChain functionality and the graph execution engine that powers multi-step agent systems.

Additional updates include refreshing OpenAI model references, updating the langsmith dependency from 0.7.31 to 0.8.0, and addressing security concerns with the idna library. These dependency updates ensure the framework remains compatible with current LLM APIs while maintaining security posture against known vulnerabilities.

### Infrastructure and Quality Improvements

The release also includes infrastructure hardening, specifically improvements to how Dependabot handles version-bound preservation in dependency updates. This prevents accidental over-specification or under-specification of dependency versions that could lead to compatibility issues down the line.

File search functionality received optimization through sorting glob search results by modification time, ensuring the most recently modified files appear first. This seemingly minor change significantly improves developer experience when working with large codebases containing many similar files.

## What Happens Next

LangChain's trajectory continues toward production-ready agent systems. The focus on middleware enhancements and security features suggests the framework is maturing beyond proof-of-concept applications toward enterprise deployments where data handling and execution control are critical requirements.

Teams currently using LangChain should evaluate whether the PII redaction capabilities align with their compliance requirements and whether stream transformer registration simplifies their current architecture. Those using TodoListMiddleware should upgrade to ensure proper task completion tracking.

The ecosystem continues evolving in tandem—staying current with LangGraph and other dependencies ensures access to the latest improvements in agent orchestration and execution efficiency. As with any incremental release, the upgrade path is straightforward for existing deployments.
*This article does not contain affiliate links.*
