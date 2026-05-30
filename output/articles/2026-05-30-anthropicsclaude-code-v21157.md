---
category: sdk_release
date: '2026-05-30'
generated_at: '2026-05-30T04:58:05.262579Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.157
template_type: explainer
title: anthropics/claude-code v2.1.157
word_count: 995
---

# Claude Code v2.1.157: Streamlining Plugin Management and Agent Workflows

Anthropic has released Claude Code v2.1.157, a maintenance update that focuses on improving the developer experience around plugin management, agent configuration, and session handling. The release addresses several friction points in the CLI tool, making it easier for developers to create, manage, and deploy plugins while giving more control over how agents handle complex tasks.

## TL;DR

- **Local plugin discovery**: Plugins stored in `.claude/skills` directories now load automatically without requiring marketplace registration
- **Plugin scaffolding**: New `claude plugin init` command generates boilerplate for custom plugin development
- **Enhanced CLI autocomplete**: The `/plugin` command now offers intelligent suggestions for subcommands and plugin names
- **Agent field persistence**: The `settings.json` configuration now properly respects agent preferences across dispatched sessions
- **Worktree improvements**: Claude-managed Git worktrees are now left in an unlocked state for easier cleanup
- **Impact**: Developers gain faster iteration cycles for local plugin development, more flexible agent routing, and better sandbox management for multi-session projects

## Background

Claude Code operates as an AI-powered command-line interface that allows developers to integrate Claude's capabilities directly into their development workflows. A key feature has been the ability to extend functionality through plugins—custom tools that enhance what Claude can do within development environments.

Previously, the plugin ecosystem required developers to publish plugins to a marketplace before they could be used, creating friction during development and testing. This extra step made rapid iteration difficult and added unnecessary complexity for experimental or internal tools. Similarly, agent configuration in multi-session scenarios has been limited, and Git worktree management—which Claude uses to isolate work contexts—often left artifacts requiring manual cleanup.

## How it works

### Local Plugin Loading and Development

The most significant change is the introduction of automatic plugin discovery from `.claude/skills` directories. This eliminates the marketplace publication requirement for development and testing phases. Developers can now place plugin files directly in a local `.claude/skills` folder, and Claude Code will recognize and load them without additional configuration steps.

To accelerate plugin creation, the `claude plugin init <name>` command generates scaffolding code with the necessary structure and boilerplate. This reduces the barrier to entry for developers wanting to create custom integrations. The scaffolding likely includes basic handler functions, configuration templates, and documentation stubs that developers can populate with their specific functionality.

This approach follows a familiar pattern in modern development tooling—local-first development with marketplace publishing as an optional later step. It's particularly valuable for teams developing internal tools or experimenting with new plugin concepts before committing to public release.

### Enhanced Autocomplete and Command Discovery

The `/plugin` command now includes context-aware autocomplete that suggests available subcommands, names of installed plugins, and plugins from known marketplaces. This quality-of-life improvement reduces the mental load of remembering exact plugin names and command syntax, especially valuable when working with multiple custom plugins simultaneously.

Autocomplete suggestions come from three sources: the immediate command structure, locally installed plugins (both from `.claude/skills` and global installations), and remote marketplace registries. This three-tiered approach ensures developers see relevant suggestions whether they're using entirely local tools or drawing from published plugin ecosystems.

### Agent Configuration and Session Dispatch

Claude Code now honors the `agent` field specified in `settings.json` when dispatching sessions. This allows teams to define default agent preferences at the project level while still permitting override via the `--agent <name>` command-line flag. The behavior provides sensible defaults without sacrificing flexibility—developers can establish team preferences while individual contributors retain the ability to substitute a different agent when needed.

This feature matters for larger teams coordinating on shared codebases, where consistent tool usage and behavior across team members can improve collaboration and debugging efficiency.

### Worktree Management Improvements

Claude frequently uses Git worktrees to isolate different work contexts and prevent interference between concurrent tasks. Previously, when Claude finished with a worktree, it remained locked, blocking cleanup operations like `git worktree remove` or `git worktree prune`. This forced developers to manually unlock worktrees or use more aggressive removal techniques.

The update leaves Claude-managed worktrees in an unlocked state upon completion, enabling standard Git commands to clean them up naturally. This eliminates orphaned worktrees accumulating on disk and simplifies workspace hygiene, particularly important for long-running development sessions or CI/CD environments where worktree proliferation can become problematic.

### Telemetry and Debugging

For developers who need visibility into Claude's decision-making processes, the `tool_decision` telemetry events now include `tool_parameters` when the environment variable `OTEL_LOG_TOOL_DETAILS=1` is set. This captures the actual parameters Claude passes—bash commands, MCP (Model Context Protocol) handler names, and skill names—enabling better analysis of tool execution patterns. Teams using observability platforms can correlate these detailed logs with broader system behavior to optimize tool usage or debug unexpected outcomes.

### Robustness Improvements

The release addresses a crash that occurred when developers attached invalid images (zero-byte files, corrupted data) through paste operations, MCP integrations, or dialogs. Rather than failing the entire request, invalid images now become text placeholders with appropriate error messaging, allowing sessions to continue. This prevents minor attachment errors from derailing development workflows and provides clearer feedback about which resources failed to process.

Additionally, network permission prompts in auto-bypass mode have been fixed, reducing unnecessary user interactions in environments where network policies are pre-configured.

## What happens next

With local plugin development now first-class in Claude Code, we should expect to see more experimental plugins and internal tools emerging in development teams. The scaffolding command and improved autocomplete make plugin creation more accessible to developers without deep tooling expertise. As teams adopt local plugin workflows alongside traditional marketplace publishing, we'll likely see patterns emerge around plugin organization, versioning, and sharing within organizations.

The agent field persistence and worktree improvements focus on enabling more sophisticated multi-session workflows, suggesting Anthropic's roadmap includes increasingly complex orchestration scenarios where Claude coordinates multiple concurrent development tasks.

For teams currently using Claude Code, this release is a straightforward upgrade that removes friction points without requiring configuration changes. For teams evaluating Claude Code, the local plugin system now removes a significant adoption barrier.
*This article does not contain affiliate links.*
