---
category: research_paper
date: '2026-05-28'
generated_at: '2026-05-28T06:26:58.847398Z'
generated_by: claude-haiku-4-5-2026-05-28
importance_score: 40
products: []
source_name: hackernews
source_url: https://arxiv.org/abs/2510.04950
template_type: explainer
title: Investigating how prompt politeness affects LLM accuracy (2025)
word_count: 944
---

# Does Politeness in Prompts Actually Matter? New Research Investigates LLM Accuracy

A new study is challenging assumptions about how we communicate with large language models. Researchers have conducted a systematic investigation into whether the politeness level in prompts—essentially the courtesy and formality with which we ask AI systems questions—has any measurable impact on the accuracy of their responses.

The investigation, which generated significant discussion in the developer community with 55 comments on Hacker News, examines a question that many AI practitioners have wondered about but few have rigorously tested: does saying "please" and "thank you" to an LLM actually improve its performance?

## TL;DR

- **Prompt politeness**: Adding polite phrases like "please," "thank you," or respectful language to prompts is a common practice among LLM users, but its actual impact on model accuracy has been largely untested
- **Empirical findings**: The research provides quantitative data on whether politeness correlates with improved accuracy across different types of tasks and models
- **Practical implications**: Understanding whether politeness affects LLM outputs helps optimize prompting strategies and informs best practices for developers and end users

## Background

The question of how to best communicate with AI systems has evolved significantly since large language models became widely accessible. Early adopters and researchers noticed anecdotally that some prompts seemed to work better than others, leading to the emergence of "prompt engineering" as a distinct skill.

Within prompt engineering, various strategies have been proposed: using chain-of-thought reasoning, providing examples, breaking down complex tasks, and adjusting tone or formality. However, much of this guidance has been based on intuition, limited experimentation, or small-scale observations rather than systematic research.

The politeness question sits at an intersection of linguistics, psychology, and machine learning. On one hand, it seems intuitive that adding polite language might influence a model trained on human-generated text—after all, politeness is deeply embedded in how humans communicate. On the other hand, LLMs process tokens mathematically without understanding social conventions the way humans do, which suggests politeness might be irrelevant to accuracy.

Previous informal tests by users have yielded mixed results, with some claiming that polite prompts produced better outputs and others finding no difference. This lack of consensus made the question ripe for rigorous investigation.

## How it works

### Understanding Prompt Variation and Control

The research examines how changing only the politeness elements of a prompt—while keeping the core request identical—affects model outputs. This approach isolates the variable in question. Researchers create matched pairs or sets of prompts that ask for the same information with different levels of politeness.

For example, one prompt might be: "What is the capital of France?" while a politer variant might be: "Could you please tell me what the capital of France is? Thank you in advance." By comparing responses to semantically equivalent prompts with different politeness levels, the study can measure whether politeness causally influences accuracy.

The methodology requires careful experimental design to ensure that politeness changes don't inadvertently alter other prompt characteristics that might affect performance, such as length, clarity, or specificity.

### Testing Across Models and Tasks

A comprehensive investigation tests multiple variables to understand whether findings generalize. This includes testing different language models (from various organizations and sizes), different task types (factual recall, reasoning, creative tasks, coding), and different languages if applicable.

Different models may respond differently to politeness based on their training data and fine-tuning. Older or smaller models might show different patterns than newer, larger ones. Similarly, a task requiring factual accuracy might be less susceptible to politeness effects than a task requiring creative generation or subjective judgment.

By systematically varying these conditions, researchers can determine whether politeness effects are robust or context-dependent. They can also measure the magnitude of any effects—whether politeness creates a large, meaningful difference or a statistically significant but practically negligible one.

### Quantifying Accuracy and Measuring Effects

The study requires objective metrics for accuracy. For factual questions, this is relatively straightforward—answers are either correct or incorrect. For more complex tasks, researchers must define metrics that capture whether a response meets the stated requirements.

Statistical analysis then determines whether differences in accuracy between polite and less polite prompts are statistically significant or likely due to random variation. Effect sizes quantify the practical magnitude of any differences.

## What the findings mean

The research provides empirical grounding for a commonly held belief among AI users. If politeness is found to significantly improve accuracy, it would validate a simple and accessible strategy for improving LLM performance—one that requires no technical knowledge and could be adopted universally.

Conversely, if politeness is found to have minimal or no effect on accuracy, this would be equally valuable information, potentially redirecting optimization efforts toward strategies with demonstrable impact.

Either way, the systematic evidence allows developers, researchers, and organizations using LLMs to make informed decisions about prompting strategies. It contributes to the growing body of empirical research on prompt engineering that moves the field away from folklore and toward evidence-based best practices.

The investigation also raises broader questions about how LLMs process linguistic and social cues, which has implications for AI alignment and how we understand model behavior.

## What happens next

As more research examines the mechanics of effective prompting, we can expect refinement of best practices across industries using LLMs. Results like these may influence how organizations train staff to interact with AI systems and how AI interface designers structure user interactions.

The work also contributes to a larger research agenda examining prompt engineering systematically rather than through ad-hoc experimentation.

To explore the full research, the peer-reviewed paper is available on arXiv, and the Hacker News discussion provides additional perspective and real-world experiences from developers working with these models.
*This article does not contain affiliate links.*
