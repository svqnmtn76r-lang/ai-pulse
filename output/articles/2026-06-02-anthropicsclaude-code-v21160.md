---
category: sdk_release
date: '2026-06-02'
generated_at: '2026-06-02T05:57:10.728262Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.160
template_type: explainer
title: anthropics/claude-code v2.1.160
word_count: 857
---

# Claude Code v2.1.160: Safer AI-Assisted Development Through Enhanced Prompts

Anthropic has released version 2.1.160 of Claude Code, its AI-powered development assistant, with a focus on preventing unintended code execution and improving reliability across multiple workflows. The update addresses security vulnerabilities related to automatic file modifications while also fixing several user experience issues affecting session management and clipboard operations.

## TL;DR

- **Security-first prompting**: The tool now requires explicit user confirmation before modifying critical system and configuration files that could enable unintended command execution
- **Improved read verification**: Single-file grep operations now satisfy safety checks for file reading before editing, reducing unnecessary friction
- **Cross-platform clipboard fixes**: Windows Subsystem for Linux (WSL) users will experience more reliable copy-on-select functionality through PowerShell interoperability
- **Session persistence improvements**: Background agents and resumed sessions now maintain conversation history and avoid redundant re-execution
- **Impact**: Developers using Claude Code can work with greater confidence that AI modifications won't accidentally alter critical infrastructure files or lose progress during multi-day development sessions

## Background

AI-assisted coding tools face a fundamental tension: they must be capable enough to make meaningful code changes, yet safe enough to prevent catastrophic mistakes. Claude Code operates in environments where the AI can execute shell commands and modify files, creating scenarios where a small error in interpretation could lead to unintended modifications of system configuration files.

Prior to this release, the tool lacked comprehensive safeguards around certain high-risk files. Shell startup files like `.zshenv` and `.bash_login` are sourced automatically when terminals launch, making them attractive targets for malicious or erroneous modifications. Similarly, build tool configuration files like `.npmrc` and `.bazelrc` can grant arbitrary code execution privileges, essentially giving the tool a way to run commands with elevated capabilities.

The `acceptEdits` mode—designed to streamline workflows by automatically accepting AI-suggested changes—amplified these risks by reducing human review opportunities.

## How it works

### Guarding Shell and Configuration Files

The update introduces a critical safeguard: before Claude Code writes to shell startup files (`.zshenv`, `.zlogin`, `.bash_login`) or Git configuration directories (`~/.config/git/`), the tool now prompts the user for explicit confirmation. This interruption is intentional—while it adds a small friction point, it prevents scenarios where automated modifications could alter shell behavior in ways that affect every future terminal session.

The same protection extends to `acceptEdits` mode for build tool configurations. Files like `.npmrc`, `.yarnrc*`, `bunfig.toml`, and `.bazelrc` are now flagged for manual review before modification. Pre-commit hooks (`.pre-commit-config.yaml`) and development container configurations (`.devcontainer/`) receive similar treatment. This approach balances automation with safety by distinguishing between ordinary source code changes (which can proceed automatically in trusted scenarios) and infrastructure configuration (which warrants human oversight).

### Streamlining File Reading Verification

One challenge in AI-assisted editing is ensuring the model has actually read file contents before modifying them. Previously, Claude Code required a dedicated read operation even after using grep to search a file. This created unnecessary busy work: if a developer asked the tool to find a function with grep and then modify it, the tool would need to read the entire file again despite already having examined its contents.

Version 2.1.160 recognizes that single-file grep operations (`grep`, `egrep`, `fgrep`) on a particular file now satisfy the read-before-edit safety check. This reduces friction without compromising safety, since grepping a file necessarily involves reading its content.

### Fixing Cross-Platform Clipboard Behavior

WSL users—developers running Linux environments on Windows machines—previously experienced clipboard failures when copying selected text. The tool had relied on OSC 52, a terminal escape sequence standard for clipboard access. However, certain terminal emulators like MobaXterm don't support this protocol, causing copies to silently fail.

The fix delegates to PowerShell interoperability instead, leveraging Windows' native clipboard mechanisms even when running in a Linux environment. This approach is more reliable across the diverse terminal ecosystem that WSL users employ.

### Preserving Session State

Background sessions managed through `claude agents` and long-running sessions that survive overnight restarts occasionally lost their conversation history and re-executed the original prompt. This was particularly frustrating for multi-day development projects where a user might leave a session running, then return the next day to find their progress lost.

The fixes ensure that session state persists correctly through both explicit session restoration and automatic recovery after system retirement events. Users can now confidently leave Claude Code running in the background, knowing their full conversation context will be available when they reconnect.

## What happens next

These improvements represent Anthropic's iterative approach to making AI development tools safer and more reliable. The security-focused changes—particularly around shell and build configuration files—establish patterns that will likely influence how other AI coding assistants handle dangerous file modifications.

For practitioners, the immediate impact is straightforward: you can deploy Claude Code with greater confidence in production-adjacent environments. The tool now explicitly surfaces decisions about modifying system-critical files rather than proceeding silently, aligning with principle of least surprise that characterizes good development tooling.

Teams interested in adopting Claude Code should review the full changelog to understand which files now require explicit confirmation, allowing them to calibrate their use of `acceptEdits` mode accordingly. The combination of enhanced prompting and improved session reliability makes this release particularly suitable for sustained development work.
*This article does not contain affiliate links.*
