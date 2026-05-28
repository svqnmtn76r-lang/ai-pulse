---
category: feature_update
date: '2026-05-28'
generated_at: '2026-05-28T05:37:35.647954Z'
generated_by: claude-haiku-4-5-2026-05-28
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.152
template_type: breaking
title: anthropics/claude-code v2.1.152
word_count: 338
---

# Anthropic's Claude-Code v2.1.152 Expands Developer Automation with Intelligent Code Fixing

## TL;DR

- **Automated code improvements**: The `/code-review --fix` command now automatically applies suggested fixes, simplifications, and efficiency improvements directly to working trees
- **Enhanced plugin architecture**: New hooks and administrative controls give organizations finer-grained security and customization over Claude-Code's behavior within enterprise environments
- **Skill system modernization**: Runtime skill reloading eliminates the need to restart sessions when installing or updating development skills

## What happened

Anthropic released Claude-Code v2.1.152, introducing substantial upgrades to its code assistance platform's automation and extensibility capabilities. The update fundamentally transforms how developers interact with code review functionality, allowing AI-suggested improvements to flow directly into active projects rather than requiring manual implementation.

The centerpiece of this release is the enhanced `/code-review --fix` command, which now moves beyond identifying issues to actively applying refinements. This addresses a significant friction point in developer workflows—the gap between receiving code suggestions and implementing them. By automatically surfacing reuse opportunities, simplification opportunities, and efficiency improvements, the tool aims to accelerate code quality improvements across development teams.

Equally significant are improvements to Claude-Code's plugin and skills framework. Organizations can now implement fine-grained tool restrictions through updated frontmatter capabilities, allowing skill developers and administrators to explicitly disable certain tools during specific skill execution. The addition of a `/reload-skills` command enables dynamic skill management without session interruption, particularly valuable for enterprises managing multiple integrated development environments.

The release introduces new hook capabilities—including `SessionStart` hooks that can trigger skill reloads and set custom session titles—plus a `MessageDisplay` hook that gives administrators control over how assistant responses appear to users. These additions address enterprise deployment scenarios where organizations need visibility and control over Claude-Code's behavior and output formatting.

A new `pluginSuggestionMarketplaces` setting empowers administrators to curate which plugin marketplaces can suggest extensions, reducing security surface area in managed environments.

## What happens next

Developers using Claude-Code should expect faster code optimization cycles. Enterprise customers may want to audit their skill configurations to leverage the new tool-restriction and hook capabilities for enhanced governance.
*This article does not contain affiliate links.*
