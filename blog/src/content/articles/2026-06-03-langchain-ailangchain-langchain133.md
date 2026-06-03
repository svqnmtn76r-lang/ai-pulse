---
category: sdk_release
date: '2026-06-03'
generated_at: '2026-06-03T06:11:40.105452Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:langchain-ai/langchain
source_url: https://github.com/langchain-ai/langchain/releases/tag/langchain%3D%3D1.3.3
template_type: explainer
title: langchain-ai/langchain langchain==1.3.3
word_count: 894
---

# LangChain 1.3.3 Released: Enhanced Agent Control and Dependency Updates

LangChain, the popular open-source framework for building applications with large language models, has released version 1.3.3, introducing improvements to agent execution, human oversight capabilities, and dependency management. The update reflects the framework's ongoing evolution toward more sophisticated multi-agent workflows and greater developer control over LLM application behavior.

## TL;DR

- **Subagent run projection**: The framework now maps subagent execution data onto a typed channel within the run object, improving visibility into hierarchical agent workflows
- **Enhanced human-in-the-loop**: New interrupt conditions and predicate-based controls give developers finer-grained ability to pause and intervene in agent execution
- **Dependency refinement**: Updates to LangGraph version requirements optimize compatibility and reduce version conflicts for users managing multiple LangChain dependencies
- **Impact**: These changes enable more transparent multi-agent systems and provide better tooling for applications requiring human oversight without rigid control flows

## Background

LangChain has established itself as a foundational library for developers building agent-based systems—applications where language models make decisions, call tools, and coordinate with other systems. As these systems grow more complex, particularly with multi-agent architectures where agents delegate work to subagents, two persistent challenges emerged.

First, visibility into hierarchical execution became opaque. When a primary agent spawned subagents to handle specialized tasks, developers struggled to track what those subagents did and how their outputs fed back into the parent workflow. This created debugging difficulties and made it harder to understand system behavior.

Second, implementing human oversight required either rigid blocking points or complex middleware logic. While LangChain's HumanInTheLoopMiddleware addressed this need, it lacked the flexibility to specify conditional interruption—cases where humans should review only certain types of agent decisions rather than all of them.

Version 1.3.3 addresses both gaps while simultaneously updating underlying dependencies to ensure stability across the broader LangChain ecosystem.

## How it works

### Subagent Run Projection and Visibility

The most significant technical addition involves how LangChain now handles subagent execution tracking. Previously, when a parent agent invoked child agents, the execution results existed in isolated contexts. Developers had to manually correlate the parent's execution trace with subagent outputs to understand the complete workflow.

With version 1.3.3, subagent runs are projected onto a typed `run.subagents` channel within the parent run object. This means the execution data automatically flows into a structured data channel that preserves type information. Rather than untyped dictionaries or raw logs, developers now work with properly typed objects that contain subagent execution details.

This approach leverages LangChain's existing channel architecture, where typed data flows between components in a directed acyclic graph. By treating subagent runs as first-class data on this channel, the framework enables downstream components to reason about subagent behavior programmatically. A parent agent can inspect subagent performance metrics, retry decisions, or adjust its own strategy based on strongly-typed subagent data rather than parsing strings or navigating nested dictionaries.

This particularly benefits complex agent hierarchies where a single parent might coordinate multiple specialized subagents, each with their own tool sets and execution patterns.

### Interrupt Mode and Conditional Human Oversight

The HumanInTheLoopMiddleware expansion introduces two new capabilities: `interrupt_mode` and predicate-based `when` conditions. These additions represent a shift from binary (interrupt or don't interrupt) to nuanced oversight logic.

The `interrupt_mode` parameter allows developers to specify how interruptions should behave. Rather than assuming a single interruption strategy, different application requirements might demand different behaviors—some may want to pause before an agent makes a decision, others after, and still others in response to specific conditions.

More powerfully, the new `when` predicate parameter accepts a callable that evaluates whether an interruption should occur. This enables conditional interruption: a predicate might check if an agent is about to call a sensitive tool, access restricted data, or execute a high-cost operation. Only when the predicate returns true does the system pause for human review. This granular control eliminates unnecessary interruptions while ensuring oversight where it matters.

Combined, these features allow developers to implement sophisticated oversight policies without hardcoding interruption points throughout their agent code. The middleware can externalize interruption logic, making oversight policies easier to test, audit, and modify.

### Dependency Management Refinements

Behind the scenes, version 1.3.3 updates LangGraph, the library underlying LangChain's graph-based agent orchestration. The bump to LangGraph 1.2.4 incorporates fixes and improvements to the graph execution engine, while loosening the dependency range ensures developers aren't forced into brittle version specifications.

Loosening version constraints serves an important purpose in Python package ecosystems: it prevents "dependency hell" scenarios where multiple packages specify exact versions that conflict. By accepting a broader range of compatible LangGraph versions, LangChain becomes easier to integrate into projects that might use LangGraph independently or alongside other tools with their own LangGraph requirements.

## What happens next

As LangChain continues evolving toward production-grade multi-agent systems, expect further refinements to execution transparency and control. The subagent projection feature establishes the pattern; future releases may extend similar typed-channel approaches to other hierarchical relationships.

The human-in-the-loop enhancements position LangChain favorably for regulated industries and high-stakes applications requiring audit trails and human oversight. As more organizations deploy LLM-based agents to production, the ability to specify precisely when and why humans should intervene becomes increasingly critical.

Developers currently using LangChain should evaluate whether these new capabilities improve their application architecture—particularly those building multi-agent systems or implementing human oversight requirements. The release represents incremental but meaningful progress toward more transparent, controllable, and auditable AI agent applications.
*This article does not contain affiliate links.*
