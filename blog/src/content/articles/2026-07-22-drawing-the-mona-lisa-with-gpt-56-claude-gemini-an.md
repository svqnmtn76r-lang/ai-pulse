---
category: tutorial
date: '2026-07-22'
generated_at: '2026-07-22T04:26:44.403037Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 40
products: []
source_name: hackernews
source_url: https://www.tryai.dev/blog/ai-drawing-arena-colored-pencils-claude-gpt-grok
template_type: explainer
title: '"Drawing" the Mona Lisa with GPT-5.6, Claude, Gemini, and Grok'
word_count: 879
---

# Drawing the Mona Lisa with AI: How Modern Language Models Visualize Concepts

Researchers and developers have found an intriguing way to test the capabilities of frontier AI models: asking them to "draw" one of history's most iconic paintings using nothing but text. A recent comparison across GPT-5.6, Claude, Gemini, and Grok reveals surprising differences in how these systems approach creative visualization tasks, even when they can't generate images directly.

This experiment, which generated significant discussion in the developer community, highlights a critical gap in how we evaluate large language models—and raises questions about what it means for an AI to "understand" visual concepts.

## TL;DR

- **Text-based visualization**: Modern LLMs can describe how to recreate visual art using ASCII art, coordinate systems, or detailed instructions, revealing different interpretive approaches
- **Model personality differences**: Despite similar underlying architectures, different AI models produce notably different outputs for the same creative prompt, suggesting distinct training and alignment choices
- **Evaluation methodology**: This test demonstrates a creative approach to comparing model capabilities beyond standard benchmarks, useful for developers choosing between platforms
- **Impact**: For practitioners, this suggests that model selection depends not just on raw capability but on how well a model's "creative style" matches your use case

## Background

The challenge of evaluating language models has long frustrated the AI community. While benchmark scores provide quantitative data, they often fail to capture nuanced differences in how models interpret ambiguous or creative tasks. Traditional metrics like MMLU or HellaSwag measure factual knowledge and reasoning, but they don't reveal much about how a model thinks through open-ended problems.

The idea of asking models to reproduce visual art through text emerged as a creative evaluation method that sits at the intersection of several capabilities: comprehension of visual concepts, creative problem-solving, and communication clarity. The Mona Lisa—with its distinctive composition, subtle color gradients, and cultural significance—makes an ideal test subject because most people have a mental image of it, allowing for comparison between model outputs and human expectations.

Previous attempts at similar exercises typically involved simpler images or relied on APIs that convert text descriptions to actual images. This experiment takes a different approach: it evaluates what the models themselves produce when asked to describe or represent the painting without external image generation tools.

## How It Works

### Understanding the Prompt

The fundamental challenge lies in asking a text-only model to handle something inherently visual. The experiment works by posing open-ended prompts like "describe how you would draw the Mona Lisa" or asking models to generate ASCII art representations, coordinate-based descriptions, or step-by-step rendering instructions.

This approach leverages an interesting property of modern language models: they've been trained on vast amounts of text that describe visual concepts, including ASCII art, technical drawing specifications, and detailed artistic descriptions. While they can't see or generate images, they can reason about spatial relationships, colors, and composition through language.

### Model Interpretation Differences

When given identical prompts, GPT-5.6, Claude, Gemini, and Grok produced notably different outputs. Some models favored ASCII art representations, others provided mathematical coordinate systems or SVG-like code, while some delivered dense prose descriptions of the painting's elements.

These differences likely stem from variations in training data, instruction tuning approaches, and constitutional AI methods—the techniques used to align models with specific behaviors. Claude, for instance, tends toward structured and systematic approaches. Grok, with its stated emphasis on maximum truth-seeking, might prioritize technical accuracy. GPT models often balance creativity with clarity.

### Evaluation Metrics

Assessing the quality of these outputs requires considering multiple dimensions: technical accuracy (does the representation match the actual painting?), creativity (does the model go beyond simple description?), clarity (would someone unfamiliar with the Mona Lisa understand it?), and completeness (are key features captured?).

The exercise revealed that no single model dominated across all metrics. This suggests that "better" is contextual—different applications might benefit from different model characteristics.

## Why This Matters

This experiment addresses a real problem in AI evaluation. As language models become more capable, traditional benchmarks reveal less about practical differences between them. A developer choosing between platforms needs more nuanced information than "Model A scores 2% higher on MMLU."

Creative tasks like this provide that granularity. They reveal how models handle ambiguity, make trade-offs between competing priorities, and communicate complex ideas. These capabilities matter for real-world applications like content creation, technical documentation, and design assistance.

The Hacker News discussion surrounding this comparison—which attracted 51 comments—suggests the developer community is hungry for this kind of comparative analysis. Many comments discussed personal preferences for different models based on similar experiences, indicating that subjective model differences are meaningful to practitioners.

## What Happens Next

As LLMs continue to evolve, expect to see more creative evaluation benchmarks emerge. The AI research community is recognizing that traditional metrics capture only part of the story. Future model comparisons will likely incorporate more open-ended, qualitative tests alongside quantitative benchmarks.

For developers, this reinforces an important lesson: benchmark scores tell you part of the story, but hands-on testing with your actual use cases remains essential. Model selection should involve trying prompts similar to what you'll actually need.

The broader implication is that as AI systems become more sophisticated, evaluation must become more sophisticated too—moving beyond single scores toward multi-dimensional assessments that capture what actually matters for human use.
*This article does not contain affiliate links.*
