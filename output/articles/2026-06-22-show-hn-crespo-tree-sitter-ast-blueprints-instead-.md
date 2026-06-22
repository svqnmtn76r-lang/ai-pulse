---
category: tool_launch
date: '2026-06-22'
generated_at: '2026-06-22T06:37:15.906239Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 60
products: []
source_name: hackernews
source_url: https://github.com/hrudulmmn/crespo
template_type: breaking
title: 'Show HN: Crespo – Tree-sitter AST blueprints instead of raw code for LLMs'
word_count: 311
---

## TL;DR

- **Point 1**: Crespo introduces a novel approach to feeding code to large language models by converting source code into Tree-sitter AST (Abstract Syntax Tree) blueprints instead of raw text
- **Point 2**: This structured representation could improve LLM accuracy on code analysis tasks by providing semantic context while reducing token consumption
- **Point 3**: Early-stage project now open for community feedback and contributions on GitHub

## What happened

A developer has released Crespo, an experimental tool that transforms the way code is presented to large language models. Rather than feeding LLMs raw source code, Crespo leverages Tree-sitter—a widely-adopted incremental parsing library—to generate Abstract Syntax Tree blueprints that capture code structure in a machine-friendly format.

This approach addresses a fundamental limitation in current LLM-based code analysis workflows: raw code requires models to parse syntax contextually, consuming valuable tokens while potentially losing semantic relationships. By converting code to AST representations first, Crespo provides LLMs with a cleaner, more semantically meaningful input that emphasizes logical structure over textual formatting.

The project was shared on Hacker News as a "Show HN" submission, typically reserved for projects seeking early-stage feedback from the developer community. While the initial post attracted minimal engagement, the core concept addresses a genuine pain point in AI-assisted development—particularly for code generation, refactoring, and bug detection tasks where understanding code intent matters more than preserving whitespace.

Tree-sitter's language-agnostic approach means Crespo could theoretically support multiple programming languages without extensive reengineering. The tool is positioned as a preprocessing layer, sitting between source code repositories and LLM inference pipelines.

## What happens next

The project remains in early development with an open GitHub repository inviting contributions. Success will likely depend on empirical validation—demonstrating measurable improvements in LLM performance on code tasks versus traditional approaches. Next phases probably include benchmarking against standard code datasets and integrating with popular development tools and LLM platforms.
*This article does not contain affiliate links.*
