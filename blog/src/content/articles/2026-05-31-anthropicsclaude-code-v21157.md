---
category: sdk_release
date: '2026-05-31'
generated_at: '2026-05-31T05:24:34.848478Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.157
template_type: explainer
title: anthropics/claude-code v2.1.157
word_count: 842
---

# Claude-Code v2.1.157: Streamlining Plugin Management and Agent Workflows

Anthropic has released version 2.1.157 of Claude-Code, bringing significant improvements to how developers manage plugins, configure agents, and handle edge cases in coding workflows. The update focuses on reducing friction in plugin discovery, enhancing agent configuration flexibility, and improving system reliability when dealing with problematic file inputs.

## TL;DR

- **Local plugin discovery**: Plugins stored in `.claude/skills` directories now load automatically without requiring marketplace registration
- **Plugin scaffolding**: New `claude plugin init` command simplifies creating new plugins with proper structure
- **Agent configuration**: The `settings.json` file now respects agent preferences for dispatched sessions, with CLI override capability
- **Improved reliability**: Image handling now gracefully degrades instead of crashing when files are corrupted or malformed
- **Impact**: Developers can iterate faster on custom tools, maintain consistent agent preferences across workflows, and experience fewer crashes from file errors

## Background

Claude-Code has evolved as a bridge between Claude AI capabilities and local development environments. Previous versions required plugins to be registered through marketplace systems before they could be discovered and used—a friction point for developers building internal or experimental tools. Similarly, agent configuration required command-line arguments rather than persistent settings, making it tedious to maintain preferences across multiple sessions.

The marketplace-first approach made sense for distribution but created barriers for rapid prototyping and organization-specific tooling. Additionally, the system's handling of malformed files represented a reliability gap that could interrupt developer workflows unexpectedly.

## How it Works

### Local Plugin Discovery and Development

The headline feature enables a filesystem-based plugin discovery system. Developers can now create plugins directly in `.claude/skills` directories within their project, and Claude-Code will automatically recognize and load them without any marketplace interaction. This mirrors patterns popularized by other modern development tools that prioritize local customization.

The new `claude plugin init <name>` command scaffolds a new plugin with proper directory structure, boilerplate code, and necessary configuration files. This reduces the barrier to entry for creating custom capabilities. Developers working on internal tools, domain-specific utilities, or experimental features can now iterate entirely locally before—or instead of—publishing to any marketplace.

The plugin system maintains backward compatibility with marketplace-registered plugins while making the local-first workflow the path of least resistance. This architectural choice acknowledges that not all useful tools need to be shared publicly, particularly for enterprise teams with specialized workflows.

### Enhanced Command-Line Completions

To support the expanded plugin ecosystem, Claude-Code v2.1.157 adds intelligent autocomplete for plugin-related commands. The `/plugin` command now offers completion suggestions for subcommands, locally installed plugin names, and plugins available from known marketplaces. This discoverability improvement helps developers understand what's available without manually checking documentation or listing commands.

### Agent Configuration Persistence

The `agent` field in `settings.json` is now honored when dispatching sessions. Previously, developers had to specify agent preferences via command-line flags for each session. Now, projects can define a default agent in their settings file, with the `--agent <name>` flag available as an override mechanism when needed.

This change particularly benefits teams that standardize on specific agent configurations for different project types or stages. A repository's root settings file can enforce consistent behavior without requiring developers to remember specialized command syntax.

### Worktree Management Improvements

Claude-Code manages isolated Git worktrees for safe code modifications. Two improvements target this subsystem: the `EnterWorktree` action can now switch between Claude-managed worktrees mid-session without requiring session restart, and worktrees are left unlocked after agent completion to allow Git's standard cleanup commands (`git worktree remove` or `git worktree prune`) to function properly.

These changes reduce operational overhead when agents work across multiple worktrees and simplify post-session cleanup, which is valuable for CI/CD integration and resource-constrained environments.

### Observability and Telemetry Enhancements

The `tool_decision` telemetry events now include `tool_parameters` when the `OTEL_LOG_TOOL_DETAILS=1` environment variable is set. This means operators and developers can log specific bash commands executed, MCP (Model Context Protocol) names, and skill names for audit trails or debugging purposes. This opt-in approach balances transparency with privacy concerns about sensitive command logging.

### Robust File Input Handling

A critical reliability fix addresses image processing crashes. When developers paste images, provide them via MCP, or upload them through dialogs, Claude-Code now gracefully handles zero-byte files and corrupted data by converting them to text placeholders rather than crashing the entire request. This prevents malformed file attachments from interrupting workflows—a common friction point when dealing with screenshots and dynamically generated images.

An incomplete fix notation in the original release notes ("Fixed sandbox network permission prompts appearing in auto and bypass-") suggests additional work on permission handling continues, though details appear incomplete in this release.

## What Happens Next

The trajectory suggests Anthropic is making Claude-Code more suitable for team environments and CI/CD integration. Local plugin discovery lowers barriers to tooling customization, persistent agent configuration reduces operational overhead, and improved reliability makes the system more robust under imperfect real-world conditions.

Developers should consider migrating custom tools from workaround status to proper plugins using the new scaffolding tools, and teams should document their preferred agent configurations in `settings.json` files to ensure consistent behavior across team members and automation workflows.
*This article does not contain affiliate links.*
