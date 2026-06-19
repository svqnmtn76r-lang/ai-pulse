---
category: feature_update
date: '2026-06-19'
generated_at: '2026-06-19T06:26:43.890214Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.183
template_type: breaking
title: anthropics/claude-code v2.1.183
word_count: 345
---

## TL;DR

- **Safety enhancement**: Claude Code v2.1.183 now blocks dangerous operations like `git reset --hard`, `terraform destroy`, and similar destructive commands unless explicitly requested, reducing accidental data loss risks
- **Transparency improvements**: Deprecated model warnings now surface across all interfaces, including agent frontmask configurations, keeping users informed of API changes
- **Privacy feature**: New option to strip Claude.ai session links from commits and pull requests in web-based workflows

## What happened

Anthropic has released Claude Code v2.1.183, introducing significant safety guardrails and usability refinements to its code execution environment. The update addresses a critical pain point in AI-assisted development: preventing unintended destructive operations.

The most substantial change involves expanded protections for version control and infrastructure management. Destructive git operations—including `git reset --hard`, `git checkout -- .`, `git clean -fd`, and `git stash drop`—are now blocked unless the user explicitly requests them. Similarly, infrastructure-as-code destruction commands (`terraform destroy`, `pulumi destroy`, `cdk destroy`) require specific stack confirmation before execution. The system also prevents git commit amendments unless the agent created the original commit in the current session, reducing cross-contamination risks.

Beyond safety, the release emphasizes transparency. Users now receive warnings when Claude Code attempts to use deprecated models or auto-upgrades to newer versions, displayed both in standard output and stderr during print mode operations. This coverage extends to models specified in agent frontmatter configurations.

New configuration utilities also ship with this version. The `/config --help` command now lists available shorthand keys for quick settings adjustments, while the `/config` toggle behavior has been refined to accept both Enter and Space for confirmations, with Escape now saving changes rather than reverting them.

Additionally, a new `attribution.sessionUrl` setting allows developers to omit Claude.ai session links from generated commits and pull requests when working through web interfaces or Remote Control sessions—useful for privacy-conscious teams or automated pipelines.

## What happens next

The enhanced safety features should reduce incident reports related to accidental data deletion in development workflows. Watch for adoption patterns across Anthropic's customer base, particularly among teams using Claude Code in CI/CD pipelines where destructive operations carry significant risk.
*This article does not contain affiliate links.*
