---
category: sdk_release
date: '2026-06-25'
generated_at: '2026-06-25T05:12:12.976637Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.191
template_type: explainer
title: anthropics/claude-code v2.1.191
word_count: 979
---

# Claude Code v2.1.191: Bug Fixes and Workflow Improvements

Anthropic has released version 2.1.191 of Claude Code, its command-line interface for interacting with Claude AI models. The update focuses on stability improvements and user experience refinements rather than major feature additions, addressing a range of issues that affected conversation management, background agent handling, and platform-specific functionality.

## TL;DR

- **Conversation resumption**: The `/rewind` command now allows users to restore conversations that were interrupted by the `/clear` command, improving workflow continuity
- **Agent reliability**: Background agents no longer restart unexpectedly after being stopped, fixing a persistent state management issue
- **Display fixes**: Multiple UI and rendering issues have been corrected across different platforms and terminal emulators, including Windows Terminal and Ghostty
- **Policy communication**: Better error messaging now explains when features like `/voice` are disabled by organizational restrictions rather than displaying generic unavailability notices
- **Impact**: These fixes reduce friction in daily workflows, particularly for teams using Claude Code in enterprise environments with organizational policies and users managing multiple concurrent AI agent sessions

## Background

Claude Code serves as a command-line interface that enables developers to interact with Claude AI through terminal-based workflows. As AI coding assistants become more integrated into development environments, the tool has grown to support increasingly complex features like background agents, voice interactions, and multi-session management.

Previous versions of Claude Code introduced features like the `/clear` command for resetting conversation state and background agents for running tasks asynchronously. However, these features created edge cases and usability challenges. The `/clear` command was particularly problematic because it provided no way to recover deleted conversation history, and background agents sometimes persisted after users attempted to stop them—leading to orphaned processes consuming resources or generating unexpected outputs.

Additionally, the tool's cross-platform nature created compatibility issues. Windows Terminal, Ghostty over SSH/tmux, and other terminal emulators each handle rendering, text wrapping, and user interactions differently, requiring targeted fixes for each platform.

## How it works

### Conversation State Management and Recovery

The `/rewind` command addresses a fundamental workflow problem: users who accidentally ran `/clear` had no way to recover their conversation history. With this update, conversations can be resumed from checkpoints created before the clear operation was executed. This is particularly valuable in development scenarios where a conversation thread contains important context, debugging steps, or generated code snippets.

The implementation appears to maintain conversation snapshots at key points, allowing the rewind operation to restore not just the message history but also the execution context and variable state. This mirrors similar functionality in debugging tools and REPL environments, where users expect to be able to step backward through their interactions.

### Background Agent Lifecycle Management

Background agents—processes that run tasks independently from the main conversation thread—previously exhibited a resurrection problem. When users stopped an agent through the tasks panel UI, the agent would sometimes restart automatically, either due to incomplete cleanup routines or state synchronization issues. Version 2.1.191 fixes this by ensuring that the stopped state is properly persisted and respected.

The fix likely involves improving the agent lifecycle tracking mechanism, ensuring that stopped agents don't respond to residual signals or automatic restart triggers. This is critical for users managing multiple concurrent AI agents, as uncontrolled agent behavior can lead to resource exhaustion or unexpected modifications to project files.

### Enhanced Error Messaging and Organizational Policies

When organizational policies restrict features like voice interaction, the previous version displayed a generic "not available" message that didn't explain why the feature was disabled. The updated version now provides contextual information about policy restrictions, helping users understand whether a feature is unavailable due to system limitations or administrative configuration.

This improved messaging reduces support burden and clarifies the distinction between technical unavailability and policy-driven restrictions—an important distinction for enterprise users who may need to request policy changes through proper channels.

### Platform-Specific Rendering and Terminal Compatibility

Several fixes address terminal-specific issues. The Windows Terminal `/login` URL truncation problem occurred when URLs were wrapped across multiple lines, preventing users from clicking or copying the complete login link. The Ghostty SSH/tmux Cmd+click link handling ensures that keyboard shortcuts work correctly across terminal multiplexers and remote connections.

The scroll position jumping issue during streaming responses affected readability when users tried to review earlier output while new content was being generated. This fix likely involved decoupling the scroll position management from the streaming input handler, allowing independent user control over viewport position during active streaming.

### Slash Command and File Path Handling

The `/permissions` command and other builtin slash commands were being incorrectly forwarded to background sessions as literal text rather than being processed as commands. The fix ensures that the CLI properly distinguishes between commands intended for the main interface versus content intended for agent sessions.

Additionally, when users paste images into jobs, the system now displays the standardized `[Image #N]` placeholder notation instead of full filesystem paths, improving readability and reducing clutter in job output displays.

### Hook Configuration Parsing

Hooks with comma-separated matchers—such as configurations specifying `"Bash,PowerShell"` to trigger on multiple shell types—were silently failing to fire. This type of silent failure is particularly problematic in automation scenarios where users don't immediately notice that conditional logic isn't executing. The fix ensures that matcher parsing properly handles comma-delimited values.

## What happens next

Version 2.1.191 represents a consolidation release focused on reliability and edge case handling rather than new capabilities. Organizations using Claude Code in production environments should expect improved stability, particularly around agent management and cross-platform compatibility.

For enterprise users, the improved policy messaging means clearer communication about feature restrictions, potentially reducing miscommunication between developers and administrators. The conversation recovery feature may shift user behavior toward more experimental prompting, since accidental `/clear` operations are now recoverable.

The cumulative effect of these fixes suggests that future versions will likely build on this stability foundation with additional agent management features, expanded organizational policy controls, and deeper terminal multiplexer support.
*This article does not contain affiliate links.*
