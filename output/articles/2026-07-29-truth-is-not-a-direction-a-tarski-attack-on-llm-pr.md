---
category: research_paper
date: '2026-07-29'
generated_at: '2026-07-29T04:20:44.791074Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 40
products: []
source_name: hackernews
source_url: https://abeljansma.nl/2026/07/10/truth-is-not-a-direction.html
template_type: explainer
title: 'Truth is not a direction: a Tarski attack on LLM probes'
word_count: 895
---

# Truth is Not a Direction: Understanding the Limits of LLM Probing Methods

A new research paper challenges a fundamental assumption in how researchers evaluate large language models' understanding of truth. The work, drawing on concepts from mathematical logic, argues that popular "probing" techniques—methods used to understand what knowledge lives inside neural networks—may be fundamentally flawed in their approach to measuring truthfulness.

## TL;DR

- **Probing limitations**: Current methods assume truth can be found in a consistent direction within a model's representation space, an assumption that doesn't hold mathematically
- **Tarski's insight**: The research applies Alfred Tarski's semantic theory of truth to show why treating truth as a geometric property is problematic
- **Practical implications**: Researchers using probing techniques to claim models "know" certain facts may be drawing unreliable conclusions
- **Impact**: This work suggests the field needs fundamentally different approaches to understanding what knowledge LLMs actually possess

## Background

The question of what language models actually "know" versus what they merely predict statistically has become increasingly important as these systems are deployed in high-stakes applications. Over the past few years, researchers developed probing methods—techniques that treat language model representations (the internal numerical patterns that emerge during computation) as geometric objects in high-dimensional space.

The basic intuition seemed sound: if a model truly understands something, that knowledge should be encoded in a consistent, detectable way within its neural representations. Researchers would train simple classifiers on these representations to detect whether a statement was "true" or "false" according to some ground truth. If these classifiers worked well, the interpretation was that the model "encodes" knowledge about that domain.

This approach gained traction because it offered a concrete methodology for investigating model internals. Papers used probing to argue that models understand syntax, semantics, factual knowledge, and more. The assumption underlying this work was geometric: truth was treated as a direction or region in representation space.

## How It Works

### The Conceptual Problem: Truth as Geometry

The core argument of this research draws from Alfred Tarski's semantic theory of truth, developed in the mid-20th century. Tarski established that truth in formal logical systems cannot be uniformly defined within those same systems—there's a fundamental mismatch between the system and its truth conditions.

This creates a problem for the geometric approach. If truth were simply a direction or linear combination in representation space, it would need to be consistent across all statements and contexts. A model couldn't simultaneously encode both "the Earth is round" and "the Earth is flat" as true, for instance. But Tarski's work suggests truth is inherently non-geometric—it's fundamentally a property of the relationship between language and the world, not a property that can be cleanly embedded as a spatial direction.

### Why Probes Appear to Work (When They Don't)

Here's where the research gets interesting: probing methods often produce high accuracy scores, leading researchers to conclude they've found evidence of knowledge. But the paper suggests these successes may reflect something else entirely—the model's ability to classify based on statistical regularities, patterns in training data, or correlates of truth, rather than genuine knowledge.

Consider a simple example: a probe might successfully classify statements about historical facts with 90% accuracy. This seems like evidence the model "knows" history. But the probe might actually be detecting superficial patterns—perhaps true historical statements are phrased differently than false ones, or contain certain word correlations learned during training. The classifier exploits these patterns without the model actually understanding historical truth in any meaningful sense.

### The Mathematical Argument

The research formalizes this intuition mathematically. For truth to exist as a consistent direction in representation space, it would need to satisfy certain geometric properties across all possible inputs. But Tarski's theorem essentially proves this is impossible for any sufficiently complex logical system. An LLM, being a system capable of expressing complex propositions, falls into this category.

This doesn't mean models know nothing. Rather, it means the geometric metaphor breaks down. Truth in a language model—if it exists at all—must be context-dependent, evolving based on what the model is reasoning about. It cannot be a fixed direction.

## What This Means for Practice

For researchers actively using probing methods, this work suggests caution is warranted. A high-accuracy probe is not definitive evidence of knowledge. The field may need to shift toward methods that acknowledge the contextual, non-geometric nature of truth representations.

This could mean developing probes that test consistency across different contexts, examining how representations change during reasoning steps, or using more sophisticated behavioral tests rather than assuming internal geometry corresponds to semantic properties.

The implications extend beyond just methodology. Claims about what LLMs "know" or "understand"—particularly in safety-critical contexts—may rest on shakier foundations than previously thought. If current evaluation methods are fundamentally limited, we may not actually have good answers to key questions about model capabilities and alignment.

## What Happens Next

The research appears to have generated thoughtful discussion in technical communities, as evidenced by engagement on Hacker News. The next phase likely involves the broader research community grappling with whether Tarski's objections truly apply to neural networks (some may argue the non-Euclidean, highly distributed nature of neural representations sidesteps the original problem) and developing alternative frameworks for understanding model knowledge.

This could drive a shift toward more empirically grounded, behavior-based evaluation methods rather than representation-level probing, or toward entirely new theoretical frameworks that account for the geometric impossibility Tarski identified.
*This article does not contain affiliate links.*
