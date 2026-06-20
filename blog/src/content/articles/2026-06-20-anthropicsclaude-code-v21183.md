---
category: feature_update
date: '2026-06-20'
generated_at: '2026-06-20T05:23:05.473133Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.183
template_type: breaking
title: anthropics/claude-code v2.1.183
word_count: 337
---

## TL;DR

- **Safety guardrails expanded**: Claude Code v2.1.183 now blocks dangerous infrastructure and version control operations unless explicitly authorized, preventing accidental data loss
- **Deprecation transparency**: Users receive warnings when requested models are outdated or auto-upgraded, improving session clarity across web and Remote Control interfaces
- **Privacy controls added**: New settings allow developers to remove session links from commits and pull requests in collaborative environments

## What happened

Anthropic released Claude Code v2.1.183 with substantial safety improvements targeting destructive operations that could compromise development workflows. The update introduces intelligent blocking mechanisms for high-risk git commands—including `git reset --hard`, `git checkout -- .`, `git clean -fd`, and `git stash drop`—which now require explicit user authorization rather than executing on implicit requests.

Infrastructure-as-code deployments received equivalent protection, with `terraform destroy`, `pulumi destroy`, and `cdk destroy` commands blocked unless users specifically request stack destruction. Notably, `git commit --amend` is now restricted to commits created during the current session, preventing unintended modification of prior work.

The release also addresses transparency concerns. Users now receive stderr warnings when requested AI models are deprecated or automatically upgraded to newer versions—functionality that previously only applied to print mode but now extends to agent frontmatter configurations. This ensures developers maintain awareness of model changes mid-session.

Privacy features expanded with a new `attribution.sessionUrl` setting enabling developers to omit Claude.ai session links from commits and pull requests, addressing concerns in organizations with stricter privacy or audit requirements.

Interface improvements include expanded `/config` command functionality with a `--help` flag displaying all available shorthand keys, plus revised toggle behavior allowing both Enter and Space to modify settings while Esc now saves changes instead of reverting them.

## What happens next

These safety enhancements suggest Anthropic is prioritizing preventing unintended infrastructure damage as Claude Code sees increased adoption in production environments. Organizations deploying this version should familiarize teams with new blocking behavior to avoid workflow disruptions. The transparency improvements around model deprecation address concerns raised in previous AI tool deployments where silent model changes affected reproducibility.

For context: [github.com/anthropics/claude-code/releases/tag/v2.1.183](https://github.com/anthropics/claude-code/releases/tag/v2.1.183)
*This article does not contain affiliate links.*
