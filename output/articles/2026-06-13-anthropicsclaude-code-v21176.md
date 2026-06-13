---
category: feature_update
date: '2026-06-13'
generated_at: '2026-06-13T05:26:11.031814Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.176
template_type: breaking
title: anthropics/claude-code v2.1.176
word_count: 322
---

# Claude Code v2.1.176 Brings Multilingual Sessions and Enhanced Security Controls

## TL;DR

- **Localization arrives**: Session titles now auto-generate in your conversation language, improving UX for non-English users
- **Security tightened**: Model allowlist enforcement now blocks environment variable workarounds; AWS credential caching optimized for dynamic environments
- **Reliability fixes**: Auto mode classifier improved to handle organizations with limited model access; sandbox and tool path matching bugs resolved

## What happened

Anthropic has released version 2.1.176 of Claude Code, its AI-assisted development platform, introducing localization features alongside meaningful security and reliability improvements. The update addresses long-standing friction points for international users and organizations managing strict model access policies.

The headline feature is intelligent session titling—the system now generates descriptive session names in whatever language you're conversing in, rather than defaulting to English. Users can optionally pin a specific language via settings to maintain consistency across teams.

On the infrastructure side, Anthropic has hardened model access controls. The update closes a potential security gap where environment variables like `ANTHROPIC_DEFAULT_*_MODEL` could redirect users to blocked models through alias picking. The `/fast` mode toggle now refuses operations that would switch to unavailable models, preventing confusion in restricted environments.

AWS credential handling has been optimized for modern cloud practices. Previously, temporary credentials were cached for a fixed one-hour window. The system now respects the credential's actual `Expiration` field, reducing authentication friction while maintaining security in dynamic cloud environments.

The release also tackles reliability issues affecting smaller organizations. Auto mode's model classifier previously failed when users lacked access to Opus 4.8—it now intelligently falls back to the best available Opus variant. Tool path regex matching has been corrected to properly handle documented patterns like `Edit(src/**)` and `Read(~/.ssh/**)`.

## What happens next

Teams using Claude Code should review their model allowlist configurations to ensure the stricter enforcement aligns with intended access policies. International teams may want to verify that conversation language detection works as expected in their setup.
*This article does not contain affiliate links.*
