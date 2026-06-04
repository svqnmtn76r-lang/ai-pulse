---
category: feature_update
date: '2026-05-31'
generated_at: '2026-05-31T05:24:20.736193Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/claude-code
source_url: https://github.com/anthropics/claude-code/releases/tag/v2.1.158
template_type: breaking
title: anthropics/claude-code v2.1.158
word_count: 300
---

## TL;DR

- **Auto Mode Expansion**: Anthropic's Claude Code now supports autonomous execution across multiple enterprise AI platforms, significantly broadening accessibility
- **Multi-Model Support**: The feature works with both Opus 4.7 and the newly released Opus 4.8, giving developers flexibility in model selection
- **Simple Activation**: Developers can enable the capability immediately via a single environment variable

## What happened

Anthropic has expanded the availability of Claude Code's autonomous execution capabilities in version 2.1.158, rolling out auto mode support to AWS Bedrock, Google Vertex AI, and Anthropic's own Foundry platform. Previously limited in scope, this update allows developers working within enterprise cloud ecosystems to leverage autonomous code generation and execution without additional infrastructure constraints.

The feature now operates with both Opus 4.7 and the latest Opus 4.8 model variants, providing developers with recent model capabilities. Adoption is frictionless—engineers simply set the environment variable `CLAUDE_CODE_ENABLE_AUTO_MODE=1` to activate autonomous functionality, eliminating complex configuration workflows.

This represents a significant shift in how Anthropic distributes Claude's code generation features. By integrating with Bedrock, Vertex, and Foundry simultaneously, the company removes vendor lock-in concerns and enables organizations already committed to specific cloud providers to implement Claude-powered code automation without architectural changes. The move particularly benefits enterprises using AWS or Google Cloud platforms, who can now access autonomous capabilities within their existing security and compliance frameworks.

Auto mode's expansion signals Anthropic's commitment to competing directly with OpenAI's Code Interpreter and competing code generation tools by making advanced features accessible across multiple deployment pathways.

## What happens next

Organizations currently evaluating Claude Code should test auto mode functionality in their preferred cloud environment immediately. The feature's availability across three major platforms suggests broader rollouts may follow. Developers should monitor upcoming releases for additional platform support and potential refinements to autonomous execution capabilities as real-world usage patterns emerge.
*This article does not contain affiliate links.*
