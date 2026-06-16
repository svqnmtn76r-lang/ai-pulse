---
category: sdk_release
date: '2026-06-16'
generated_at: '2026-06-16T06:39:03.615896Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.178
template_type: explainer
title: anthropics/claude-code v2.1.178
word_count: 855
---

# Claude Code v2.1.178: Enhanced Permission Controls and Nested Directory Support

Anthropic has released version 2.1.178 of Claude Code, its AI-powered development environment, introducing several refinements to permission management, skill organization, and agent behavior evaluation. The update focuses on giving developers more granular control over how Claude agents operate within their projects while improving the tool's ability to manage complex, multi-level directory structures.

## TL;DR

- **Parameter-based permission rules**: A new syntax lets developers block specific tool actions based on input parameters, such as preventing certain model versions from spawning subagents
- **Hierarchical skill loading**: Skills now respect nested directory structures, with local skills taking precedence and name conflicts resolved through explicit labeling
- **Improved agent safety**: The auto mode classifier now reviews subagent requests before they launch, closing a potential gap in permission enforcement
- **Better diagnostics**: The `/doctor` command received a visual overhaul with clearer status indicators and improved information hierarchy

## Background

Permission management in AI development tools has traditionally operated at a coarse level—either a tool is allowed or it isn't. However, real-world development workflows often require more nuanced control. Teams may want to allow certain capabilities in specific contexts while blocking them in others. For instance, a project might permit spawning subagents with Claude 3.5 Sonnet but restrict more expensive or experimental models.

Similarly, as projects grow in complexity, organizing development rules and capabilities across multiple directories becomes challenging. Previous versions of Claude Code handled skills and configuration at a single project level, creating bottlenecks when working across nested directories or when different parts of a project required different agent configurations.

The safety evaluation gap in auto mode also represented an architectural vulnerability. While permission rules existed to block certain actions, subagents could theoretically request blocked operations before those rules were evaluated, creating a window where unauthorized actions might execute.

## How it works

### Parameter-Specific Permission Rules

The new `Tool(param:value)` syntax extends Claude Code's permission system from binary allow/deny decisions to parameter-aware filtering. Developers can now craft rules that examine what arguments a tool receives before deciding whether to allow its execution.

For example, `Agent(model:opus)` blocks any attempt to spawn a subagent configured with Opus models, while other models remain available. This syntax supports wildcard matching through the `*` character, enabling rules like `APICall(endpoint:*/admin/*)` to block API calls to administrative endpoints while allowing access to public APIs.

This approach preserves backward compatibility—existing permission rules continue functioning unchanged—while adding expression power for teams that need it. The parameter inspection happens at rule evaluation time, with no performance impact for rules that don't use the new syntax.

### Hierarchical Directory Support for Skills and Agents

Modern development projects often use nested directory structures to organize different features, modules, or services. Version 2.1.178 extends Claude Code's configuration system to respect this hierarchy. When working on files within a subdirectory, the agent now searches for `.claude/` configuration folders starting from that directory and moving outward, using the closest matching configuration it finds.

This means a nested `.claude/skills/` directory now loads its skills when you're working on files in that subdirectory. If both the project root and a nested directory define a skill with the same name, the tool displays them as `<dir>:name`, allowing both to coexist and letting developers explicitly choose which version to use.

The same hierarchical principle applies to agents and workflows. When a configuration name collision occurs, the closest definition to your working directory takes precedence. Workflow saves now target the closest existing `.claude/workflows/` directory, preventing accidental modifications to project-level configurations when working in subdirectories.

### Enhanced Auto Mode Safety Evaluation

The auto mode feature, which allows Claude to execute actions without explicit human approval in lower-risk scenarios, previously had a sequencing issue. Subagents could submit action requests before those requests underwent permission review, creating a timing gap.

The updated version inserts permission classification before subagent launch. This means any request from a spawned subagent now passes through the permission rule evaluator before the subagent receives confirmation to execute, closing this evaluation window. The change requires no configuration from developers and applies automatically to all projects.

### Diagnostic Tool Improvements

The `/doctor` command, used to troubleshoot Claude Code installations and configurations, received a substantial interface refresh. The output now uses a consistent flat tree layout across all sections, replacing previous hierarchical inconsistencies that sometimes made information harder to scan. Status indicators now employ clearer iconography to quickly signal whether each configuration element is functioning properly, misconfigured, or missing.

Command names within the diagnostic output now appear highlighted, making it easier to copy or reference specific commands when troubleshooting or sharing diagnostic information with support teams.

## What happens next

These changes reflect Anthropic's iterative approach to Claude Code, prioritizing both developer control and safety guardrails. The parameter-based permissions syntax suggests future enhancements may add additional context-aware filtering capabilities. The hierarchical directory support aligns with how modern development tools handle large, complex projects.

Developers using Claude Code should review their permission configurations to identify opportunities where parameter-specific rules could replace broader restrictions. Teams managing multi-directory projects can now confidently use nested `.claude/` structures to apply module-specific rules without affecting project-wide settings.
*This article does not contain affiliate links.*
