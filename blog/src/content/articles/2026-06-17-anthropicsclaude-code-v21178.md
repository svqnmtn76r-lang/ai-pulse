---
category: sdk_release
date: '2026-06-17'
generated_at: '2026-06-17T06:23:23.525029Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.178
template_type: explainer
title: anthropics/claude-code v2.1.178
word_count: 977
---

# Claude Code v2.1.178: Enhanced Security Controls and Nested Project Structures

Anthropic has released an update to Claude Code that strengthens permission management, improves how the system handles multi-level project directories, and refines the autonomous decision-making capabilities of AI subagents. The release addresses both developer experience and security considerations in collaborative AI coding environments.

## TL;DR

- **Parameter-level permission rules**: Developers can now create granular permission policies that target specific tool inputs, allowing rules like blocking particular AI models from spawning subagents without restricting all subagent creation
- **Nested skill and workflow hierarchies**: Projects can now organize AI capabilities across multiple `.claude/` directories, with the closest directory to the active file taking precedence during naming conflicts
- **Improved subagent governance**: The system now reviews subagent requests before they launch, closing a security gap where blocked actions could be requested without prior review
- **Impact**: Teams working on large projects with multiple subdirectories and complex permission requirements gain better control over AI behavior while maintaining flexibility in shared codebases

## Background

Claude Code operates as an AI-assisted development environment where developers can delegate coding tasks to Claude through various automation tools and workflows. As projects grow more complex, teams face two recurring challenges: managing permissions across different parts of a codebase, and organizing AI skills and workflows in ways that match project structure.

Previous versions used relatively coarse-grained permission rules. Teams could allow or block entire tool categories, but couldn't easily restrict specific configurations. For example, if a permission rule blocked Opus-model subagents, there was no syntax to express "allow subagents, but only with the Claude 3.5 Sonnet model." This limitation forced teams to choose between overly permissive rules or losing functionality.

The nested directory problem emerged as codebases scaled. Large monorepos often contain semi-autonomous subsystems—a backend service, a frontend application, infrastructure code—each potentially requiring different AI skills or workflows. Without native support for hierarchical organization, teams had to choose between centralizing all skills in one location or managing duplicate definitions across multiple directories.

## How it works

### Parameter-Matching Permission Syntax

The new `Tool(param:value)` syntax enables permission rules to match specific input parameters of available tools. The syntax supports wildcard matching with `*` for flexible pattern matching.

The most immediate use case involves controlling which AI models can spawn subagents. Previously, blocking the `Agent` tool entirely prevented any subagent creation. Now a rule like `Agent(model:opus)` can specifically block Opus-based subagents while still allowing Claude 3.5 Sonnet subagents to spawn. Teams building guardrail policies can express constraints like "use faster models for subtasks" or "reserve the most capable models for main tasks" without losing functionality.

This approach extends beyond model selection to any tool parameter. As Claude Code's tool ecosystem grows, teams can craft increasingly specific permission policies that align with their governance requirements. The wildcard support means rules like `API(service:payments-*)` could block tools matching a pattern without requiring explicit enumeration of every matching tool.

### Nested Directory Hierarchies

Claude Code now supports organizing skills and workflows across multiple `.claude/` directories at different nesting levels. When a developer works on files in a subdirectory, the system prioritizes skills and workflows from the nearest `.claude/` directory in the file hierarchy.

This creates a cascading lookup: if you're editing a file deep in a backend service subdirectory, Claude Code first checks for skills in `.claude/skills/` within that subdirectory, then walks up the directory tree toward the project root. When naming conflicts occur—for instance, if both the root project and a backend subdirectory define a skill called "database-migration"—the closer definition wins. To keep both available despite the name clash, the nested skill automatically surfaces as `backend:database-migration`.

Workflow saves follow similar logic. When a developer saves a new workflow while working in a subdirectory, the system targets the closest existing `.claude/workflows/` directory rather than defaulting to the root. This lets different teams within a monorepo maintain their own workflow collections without polluting a shared central location.

### Improved Subagent Launch Review

A significant security enhancement involves how subagent requests are evaluated. Previously, subagents could request actions and have those requests evaluated only after launch. The updated system classifies subagent requests against permission rules before the subagent actually spawns, preventing scenarios where a spawned agent might immediately request a blocked action.

This represents a shift from reactive to proactive governance—the system no longer asks "was that action allowed after the agent started," but rather "is this agent allowed to make its planned requests before we launch it." For teams with strict compliance requirements, this closes a window where policy violations could theoretically occur.

### Enhanced Diagnostic Tools

The `/doctor` command, used for troubleshooting Claude Code configurations, now presents information in a consistent flat-tree layout across all diagnostic sections. Status icons for each section provide at-a-glance visibility into system health. Command names within the diagnostic output are highlighted for easier navigation, improving the developer experience when debugging configuration issues.

The system also improved warnings about skill description truncation, now showing the count of affected skill descriptions rather than just indicating that truncation occurred. This helps developers understand the scope of skill management issues in their configuration.

## What happens next

These changes position Claude Code for more sophisticated permission frameworks. The parameter-matching syntax creates the foundation for attribute-based access control in AI development environments—a concept growing important as organizations move beyond simple allow/deny rules toward nuanced policies reflecting business constraints.

For teams managing large codebases, nested directories and hierarchical skill organization reduce friction in multi-team projects. As development teams increasingly adopt AI-assisted coding, the ability to define team-specific workflows and skills without central coordination becomes a scaling factor.

Developers using Claude Code should review whether their permission rules could benefit from the new parameter-matching syntax, particularly around model selection in subagent spawning. Teams working across multiple project subdirectories might find opportunities to restructure their `.claude/` organization to better reflect actual team boundaries and responsibilities.
*This article does not contain affiliate links.*
