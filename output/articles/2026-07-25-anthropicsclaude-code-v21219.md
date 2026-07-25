---
category: sdk_release
date: '2026-07-25'
generated_at: '2026-07-25T04:17:46.871188Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.219
template_type: explainer
title: anthropics/claude-code v2.1.219
word_count: 844
---

# Claude Code v2.1.219: Enhanced Model Access and Network Controls

Anthropic has released version 2.1.219 of Claude Code, bringing a significant model upgrade and expanded security features for developers working with Claude's code execution environment. The release centers on introducing Claude Opus 5 as the new flagship model and adding granular network access controls for sandboxed command execution.

## TL;DR

- **Claude Opus 5 arrives**: A new large-context model with 1 million token capacity replaces the previous Opus as the default, enabling longer conversations and larger codebase analysis at competitive pricing
- **Network sandboxing**: A new allowlist setting lets developers explicitly control which domains sandboxed commands can access without requiring user approval
- **Directory management**: Fresh hooks enable better real-time control when working directories are added during active sessions
- **Improved error visibility**: Configuration validation failures now surface clearly in both terminal and streaming contexts
- **Impact**: Developers gain more powerful models, tighter security controls, and better visibility into system state—making Claude Code suitable for more production-grade workflows

## Background

Claude Code provides developers with an interface to execute code using Claude as the reasoning engine. Since its introduction, the platform has evolved to balance capability with safety, offering sandboxed execution environments where Claude can write and run code without direct system access.

Previous iterations of Claude Opus supported 200,000-token contexts, which constrained the size of codebases that could be meaningfully analyzed in a single session. Meanwhile, network access in sandboxed environments has traditionally required explicit user confirmation for each external connection, creating friction in automated workflows.

This release addresses both constraints while introducing operational improvements for developers managing complex, multi-step workflows.

## How it works

### Claude Opus 5: More context, same speed

The introduction of Claude Opus 5 (`claude-opus-5`) as the new default Opus model represents a significant capacity expansion. The model supports a 1 million token context window—five times larger than its predecessor—enabling developers to load entire codebases, comprehensive documentation, and extensive conversation histories without truncation.

Pricing remains competitive at $10 per million input tokens and $50 per million output tokens. Critically, the model includes a "fast mode" tier at the same price points, allowing developers to choose between standard and accelerated processing without premium pricing penalties. This structure encourages adoption for long-context tasks that previously required careful token budgeting.

The larger context window proves especially valuable for code analysis workflows. A developer can now reference entire project structures, multiple interrelated files, and detailed architectural documentation simultaneously, allowing Claude to provide more contextually aware code suggestions and refactorings.

### Network sandboxing with strict allowlists

The new `sandbox.network.strictAllowlist` setting introduces explicit control over external connectivity from sandboxed command execution. Previously, any network request from executed code would prompt the user for approval, creating decision fatigue in workflows requiring multiple external API calls.

With strict allowlist enforcement enabled, sandboxed commands can only connect to explicitly approved hosts. Requests to non-allowlisted domains automatically fail rather than triggering user prompts. This approach inverts the security model from opt-in (approve-on-demand) to opt-out (deny-by-default), reducing the attack surface for compromised or malicious code while eliminating permission dialogs for legitimate traffic.

Developers can define allowlists in configuration files, making the settings reusable across projects and team environments.

### Directory registration and workflow hooks

The new `DirectoryAdded` hook fires whenever a working directory is registered mid-session, whether through the `/add-dir` command or the SDK's `register_repo_root` control request. This enables downstream systems to react immediately when new project contexts are introduced during active work, useful for triggering dependency analysis, test suite initialization, or logging.

### Configuration and error visibility

The `mcp_server_errors` field now appears in headless stream-json initialization events, listing any Model Context Protocol (MCP) server entries that were skipped during configuration validation. Terminal runs print startup warnings for these failures, improving visibility into potential misconfigurations. This prevents silent failures where critical external tools fail to load without developer awareness.

The new `workflowSizeGuideline` settings key allows the dynamic workflow size guideline to be configured from any settings file rather than hardcoded defaults. The `/config` command row is hidden when a guideline is set, reducing clutter in the configuration interface.

### Nested subagent forwarding

When using the `--forward-subagent-text` flag, stream-json output now includes subagents spawned at depth 2 or deeper (nested subagent calls). These subagents are keyed by the spawning Agent's `tool_use` id, enabling full observability into complex multi-agent workflows. This improvement helps developers debug agent behavior and understand call chains in sophisticated automation scenarios.

## What happens next

The release of Claude Opus 5 establishes a new baseline for context-heavy development workflows. Teams working with large codebases or complex projects should test the updated model to assess whether the expanded context enables previously infeasible analyses.

For security-conscious deployments, the strict network allowlist feature deserves immediate attention. Organizations running Claude Code in restricted environments—such as enterprises with data sensitivity concerns—can now implement tighter access controls without requiring per-request user intervention.

Developers using MCP servers should verify their configurations are loading correctly via the new error reporting, and those building multi-agent systems should explore the nested subagent forwarding capability to improve observability.
*This article does not contain affiliate links.*
