---
category: other
date: '2026-05-22'
generated_at: '2026-05-22T21:46:18.137288Z'
generated_by: claude-haiku-4-5-2026-05-22
importance_score: 50
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.148
template_type: breaking
title: anthropics/claude-code v2.1.148
word_count: 309
---

## TL;DR

- **Critical bug squashed**: Anthropic's claude-code v2.1.148 resolves a regression causing universal command failures in the Bash tool
- **Scope of impact**: Users upgrading to v2.1.147 experienced exit code 127 errors on every shell command, effectively breaking automated code execution
- **Immediate remedy**: The patch is now available, restoring Bash functionality to normal operation

## What happened

Anthropic released claude-code v2.1.148 on GitHub, addressing a critical defect in the preceding version. The update specifically targets a regression introduced in v2.1.147 where the Bash tool was systematically returning exit code 127—the standard Unix error indicating "command not found"—regardless of whether commands executed successfully.

This represents a significant reliability issue for developers relying on claude-code for code generation and execution workflows. Exit code 127 errors would have surfaced across all Bash operations, preventing proper error differentiation and breaking downstream automation that depends on accurate exit codes for conditional logic and debugging.

The regression affected an unknown but potentially substantial user base, with the bug manifesting immediately upon upgrading to 2.1.147. For teams using claude-code in CI/CD pipelines or as part of automated development environments, this would have been a blocking issue requiring immediate rollback or patching.

The fix restores baseline functionality, ensuring the Bash tool properly reports actual command exit statuses. This recovery is particularly important for users leveraging claude-code's code execution capabilities for testing, validation, and shell script generation tasks.

## What happens next

Developers currently running v2.1.147 should upgrade to v2.1.148 immediately to restore normal Bash tool behavior. If you experienced mysterious command failures in the previous version, clearing any workarounds and retesting with the patched version is recommended.

For those still on earlier versions, the update path remains optional unless you require the latest Bash tool improvements. The GitHub releases page provides direct download links and detailed changelog information for version tracking and change management purposes.
*Disclosure: This article contains affiliate links. As an affiliate, we earn from qualifying purchases at no extra cost to you.*
