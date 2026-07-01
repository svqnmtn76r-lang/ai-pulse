---
category: feature_update
date: '2026-07-01'
generated_at: '2026-07-01T01:54:51.111537Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.196
template_type: breaking
title: anthropics/claude-code v2.1.196
word_count: 328
---

# Claude Code v2.1.196 Brings Enterprise Controls and Stability Fixes

## TL;DR

- **Enterprise governance**: Organization admins can now set default AI models across teams, visible in the CLI with "Org default" or "Role default" designations
- **Security hardening**: MCP server spawn restrictions prevent malicious repos from auto-executing trusted integrations without explicit approval
- **UX polish**: Sessions get readable default names, file attachments become clickable, and critical bugs around background job management are resolved

## What happened

Anthropic has released v2.1.196 of Claude Code, its AI-powered development environment, introducing enterprise-grade administrative controls alongside critical stability improvements. The update, published on the project's GitHub releases page, addresses workflow friction points that have plagued teams managing shared development environments.

The headline feature targets organizations deploying Claude Code across multiple teams: administrators can now configure organization-wide default models through the org console, eliminating repeated manual model selection. This cascades into role-based defaults as well, streamlining onboarding for new developers.

Beyond governance, this release tightens security posture significantly. The `claude mcp list` and `claude mcp get` commands no longer automatically spawn MCP servers that were pre-approved via committed `.claude/settings.json` files in repositories—a critical prevention against supply-chain attacks where malicious repos could execute integrations without user consent. Untrusted workspaces now display a `⏹ Pending approval` indicator, forcing explicit human authorization.

The update also crushes several high-impact bugs: a catastrophic flaw where background job resumption would permanently delete conversation transcripts and replay original prompts is fixed. Rate-limit warnings that were flickering erratically during parallel requests are now stable, and telemetry over-counting during concurrent usage limit hits has been corrected.

Quality-of-life improvements include readable default session names for easier identification and Cmd/Ctrl-clickable file attachments in chat that reveal files in native file explorers.

## What happens next

Teams using Claude Code in production environments should prioritize this update for the security fixes alone. The enterprise model defaults feature makes this particularly valuable for organizations managing large developer teams or multiple projects with different model requirements.
*This article does not contain affiliate links.*
