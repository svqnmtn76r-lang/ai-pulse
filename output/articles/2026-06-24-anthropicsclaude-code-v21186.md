---
category: sdk_release
date: '2026-06-24'
generated_at: '2026-06-24T05:07:42.957988Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.186
template_type: explainer
title: anthropics/claude-code v2.1.186
word_count: 873
---

# Claude Code v2.1.186: Enhanced MCP Authentication and Workflow Improvements

Anthropic has released an update to Claude Code that streamlines server authentication, improves agent interfaces, and fixes critical streaming issues. The v2.1.186 release focuses on reducing friction in CLI workflows while addressing reliability problems that affected users after system sleep events.

## TL;DR

- **MCP Server Authentication**: New CLI commands allow passwordless authentication of Model Context Protocol servers without opening interactive menus, with SSH-friendly stdin support
- **Workflow Enhancements**: Status filtering and improved UI navigation for agent workflows, plus expanded settings support for terminal integration
- **Auto-Response Behavior**: Bash commands prefixed with `!` now automatically trigger Claude responses, modifiable via settings
- **Stability Fixes**: Resolved critical streaming failures that occurred after machine sleep cycles
- **Impact**: Developers can now authenticate servers more efficiently in remote environments, while gaining better control over agent workflows and improving reliability in always-on development setups

## Background

Claude Code's integration with Model Context Protocol (MCP) servers has grown increasingly important as developers seek to extend Claude's capabilities with custom tools and data sources. However, authentication workflows have traditionally required interactive terminal sessions—a limitation for SSH users, automation scripts, and headless development environments.

Simultaneously, the platform's agent features have expanded across multiple views—workflows, plugins, and integrated assistants—creating navigation complexity. Users needed better filtering and visibility into agent state, particularly when monitoring long-running processes.

The streaming issues represent a more pressing concern. When systems enter sleep mode, connection states can become inconsistent. Previous versions occasionally crashed with cryptic errors about missing content blocks or JSON parsing failures, disrupting development sessions and automated workflows.

## How it works

### MCP Server Authentication Without Browser Interaction

The new `claude mcp login` and `claude mcp logout` commands provide direct CLI access to server authentication flows. Previously, developers had to navigate the interactive `/mcp` menu within Claude Code's interface—workable for local development but problematic in remote SSH sessions where graphical interfaces aren't available.

These commands accept a server name as an argument and handle OAuth or credential-based authentication entirely through the terminal. The `--no-browser` flag enables stdin redirection, allowing authentication credentials to flow through SSH tunnels or automated provisioning systems without requiring a browser on the remote machine. This mirrors patterns already established in cloud CLI tools like AWS and Google Cloud SDKs.

For teams running CI/CD pipelines or deployment systems that invoke Claude Code, this removes a major blocker. Automation can now authenticate servers programmatically rather than failing when interactive prompts are unavailable.

### Workflow and Interface Refinements

The `/workflows` agent detail view now supports status filtering via the `f` key. When monitoring multiple concurrent agent operations, developers can isolate specific status categories—completed, running, failed, queued—without scrolling through unrelated items. This matches common patterns in monitoring dashboards and log viewers.

The `/plugin` Installed tab gained a dedicated "Skills" section, providing clearer visibility into plugin capabilities. As Claude Code's plugin ecosystem grows, users benefit from explicit skill declarations rather than inferring functionality from descriptions or trial-and-error exploration.

Terminal integration improvements include a new `iterm2` option for the `teammateMode` setting. This explicitly supports iTerm2, the popular macOS terminal, with a warning when the system cannot locate the `it2` CLI tool. Previously, users had to rely on generic auto-detection, which could fail silently.

### Credential Refresh for AWS-Hosted Platforms

When Claude Platform deployments run on AWS with temporary credentials, users now see a dedicated "Claude Platform on AWS - refresh credentials" option in the `/login` menu. This streamlines the re-authentication process for teams using AWS IAM-based access controls, eliminating manual credential rotation steps.

### Bash Command Auto-Response Behavior

A behavioral change affects how Claude responds to bash commands. Commands prefixed with `!` now automatically trigger Claude to read and respond to their output, rather than simply executing them silently. This creates a more natural debugging experience where shell output flows back into the conversation.

Teams preferring the previous behavior—where bash output remained context-only—can disable this by setting `"respondToBashCommands": false` in settings.json. This opt-out mechanism preserves backward compatibility for workflows that treat bash execution as separate from Claude's reasoning loop.

### Streaming Stability After Sleep Cycles

The most critical fix addresses failures in streaming requests following system sleep. The error messages "Content block not found" or JSON parse errors indicated a mismatch between expected response structures and what the client received. Root cause analysis pointed to connection state inconsistencies when systems woke from sleep—partial responses were buffered, stream contexts became invalid, or the server-client handshake failed to properly resume.

This release implements more robust recovery logic, likely including connection validation on wake and better handling of partial message buffers. The fix benefits developers with long-lived development environments, particularly those using Claude Code for extended pair-programming sessions.

### Minor UX Fixes

Background task preview flashing has been eliminated, reducing visual noise in the interface. Additionally, subagent transcript scroll position no longer bleeds into the main transcript when exiting—a focus management fix that improves usability when juggling multiple agent contexts.

## What happens next

This update positions Claude Code for better enterprise adoption by solving real pain points in remote development, credential management, and long-running sessions. Watch for further expansions in MCP server ecosystem support and additional terminal emulator integrations as more developers adopt Claude Code in specialized environments.
*This article does not contain affiliate links.*
