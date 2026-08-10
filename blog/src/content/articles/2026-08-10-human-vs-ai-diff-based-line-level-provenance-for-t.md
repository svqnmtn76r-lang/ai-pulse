---
category: research_paper
date: '2026-08-10'
generated_at: '2026-08-10T03:15:56.665950Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 40
products: []
source_name: hackernews
source_url: https://github.com/eighttrigrams/us-vs-them
template_type: explainer
title: Human vs. AI – Diff-based line-level provenance for text under agentic editing
word_count: 898
---

# Tracking AI Edits in Text: A New Approach to Understanding Machine-Generated Content

A GitHub project has surfaced on Hacker News that tackles a growing challenge in the age of AI writing assistants: how to distinguish between human and AI-generated edits at the line level, and track the provenance of text modifications as documents evolve through agentic editing workflows.

This matters because as AI tools become embedded in content creation pipelines—from code repositories to collaborative documents—there's increasing need for transparency about who (or what) changed what, and when. The project demonstrates a diff-based approach to maintaining fine-grained attribution records as text undergoes transformations by both human and machine agents.

## TL;DR

- **Diff-based provenance**: A method for tracking changes line-by-line to identify whether modifications came from human or AI sources
- **Agentic editing**: Workflows where both humans and AI agents iteratively edit documents, requiring clear attribution trails
- **Impact**: Organizations using AI-assisted writing tools gain better visibility into content evolution, quality control, and accountability—critical for regulated industries and transparent collaboration

## Background

The intersection of human writers and AI writing assistants has created an attribution problem. When a document passes through multiple editing stages—some by humans, some by language models, some by specialized AI agents—the question "who wrote this?" becomes harder to answer.

Traditional version control systems like Git track changes at commit-level granularity, but this approach struggles with AI integration. A single commit might contain hundreds of AI-suggested edits mixed with human revisions. Without finer-grained tracking, teams lose visibility into which specific passages were AI-generated versus human-written, complicating quality assurance, compliance reviews, and accountability.

This challenge has become acute in enterprise settings where regulatory requirements mandate understanding content provenance. News organizations, legal firms, and technical documentation teams increasingly want to audit how AI touched their work. Meanwhile, collaborative platforms struggle to provide transparency when multiple agents—human and artificial—contribute to the same document.

## How it works

### Line-level Diff Analysis

The core concept involves analyzing document changes at the individual line level rather than the document or paragraph level. When a document is edited, instead of just recording "this file changed," the system identifies exactly which lines were added, modified, or removed, then attributes each change to its source.

This becomes particularly valuable in diff format, where additions and deletions are explicitly marked. By analyzing these diffs and correlating them with edit metadata—timestamps, user agents, editing tool signatures—it becomes possible to probabilistically determine whether a change originated from human interaction or an AI system. Human edits typically show different patterns: variable line lengths, incremental revisions, contextual adjustments. AI-generated edits often exhibit characteristic patterns in syntax, reformatting consistency, and the types of changes made.

### Provenance Attribution

The provenance layer builds on diff analysis by maintaining a record of not just what changed, but where each change came from. This creates an attribution graph: line X was written by human Y at timestamp Z, then modified by AI agent A at timestamp Z+1, then revised by human B at timestamp Z+2.

This history becomes especially important in agentic workflows where multiple AI systems might process the same text sequentially—a content planning agent creates an outline, a writing agent generates first draft text, an editing agent refines prose, a fact-checking agent validates claims. Each stage leaves traces that careful diff analysis can detect and record.

### Agentic Editing Workflows

Agentic editing represents a paradigm where documents flow through multiple processing stages, each potentially handled by different agents (human or machine). Unlike simple human-AI collaboration where a person writes and an AI suggests improvements, agentic workflows involve autonomous agents taking active editorial roles.

A practical example: A research team might use an AI agent to synthesize source material into initial drafts, a human editor to fact-check and refine, another AI agent to optimize for readability, and finally human reviewers to approve. Each stage modifies the text, and tracking which agent did what enables both quality control and understanding of how the document evolved.

## Implications and Adoption

The project's approach addresses several practical concerns simultaneously. From a compliance perspective, regulated organizations can audit AI's influence on sensitive documents. From a quality control angle, teams can identify which edits correlate with quality improvements or degradation. From a transparency standpoint, readers and stakeholders can understand whether specific passages are human-crafted, AI-generated, or hybrid.

The method also has limitations. Distinguishing human from AI edits becomes harder as AI systems become more sophisticated and capable of mimicking human writing patterns. The approach requires baseline data about how different agents typically edit to build accurate attribution models. And it works best when edit history is preserved—scenarios involving copy-paste or wholesale text replacement lose fine-grained traceability.

## What happens next

As AI writing tools proliferate across enterprise workflows, finer-grained attribution mechanisms will become increasingly important. This project represents one engineering approach to the problem; similar solutions will likely emerge as companies and standards bodies grapple with AI transparency requirements.

The practical adoption depends partly on tooling integration—getting these provenance-tracking capabilities into actual writing platforms and IDEs where people work. It also depends on standardization: if different organizations develop different attribution schemes, interoperability suffers.

For teams currently deploying AI-assisted writing tools, the underlying concepts suggest useful questions to ask: Can we track which edits came from which sources? Do our workflows preserve enough information to answer this later? What level of provenance detail do we actually need?
*This article does not contain affiliate links.*
