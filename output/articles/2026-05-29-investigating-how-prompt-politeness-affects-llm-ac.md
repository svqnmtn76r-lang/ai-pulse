---
category: research_paper
date: '2026-05-29'
generated_at: '2026-05-29T05:21:19.484757Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 40
products: []
source_name: hackernews
source_url: https://arxiv.org/abs/2510.04950
template_type: explainer
title: Investigating how prompt politeness affects LLM accuracy (2025)
word_count: 808
---

# Does Politeness in Prompts Actually Matter for AI Accuracy? A New Study Investigates

A recent research paper has sparked significant discussion in the AI community about whether the way we ask language models questions affects their accuracy. The investigation challenges assumptions about prompt engineering and suggests that politeness—commonly recommended in LLM usage guides—may not influence model performance the way many practitioners believe.

## TL;DR

- **Prompt politeness paradox**: Adding courteous language like "please" and "thank you" to prompts doesn't meaningfully improve LLM accuracy on most tasks, contrary to popular advice.
- **Benchmark performance**: Testing across multiple reasoning and knowledge tasks shows negligible differences between polite and direct prompts.
- **Practical implication**: Users can optimize prompts for clarity and task-specificity rather than wasting cognitive effort on politeness conventions when accuracy is the primary concern.

## Background

The internet is full of prompt engineering advice suggesting that treating AI systems politely—using "please," "thank you," and deferential language—leads to better results. This guidance has become conventional wisdom in AI communities, paralleling how people might naturally communicate with human assistants. The assumption underlying this advice is intuitive: if courtesy improves human cooperation, shouldn't it also work with AI systems?

However, language models operate fundamentally differently from humans. They don't have feelings to hurt or social expectations to meet. They're statistical systems trained to predict token sequences based on patterns in their training data. The question then becomes empirical rather than theoretical: does this popular guidance actually deliver measurable improvements?

Prior research on prompt engineering has focused on techniques like chain-of-chain reasoning, few-shot examples, and task-specific formatting—areas where measurable improvements have been documented. Politeness in prompts, however, remained largely untested despite being widely recommended.

## How it works

### Experimental Design and Methodology

The researchers tested their hypothesis across multiple dimensions. They designed experiments comparing identical prompts with varying levels of politeness, testing them against several state-of-the-art language models. The methodology involved creating paired prompts where the only variable was the inclusion or exclusion of courteous language.

Test categories included mathematical reasoning tasks, factual knowledge questions, code generation, and creative writing. By keeping all other variables constant—the actual question, context, and task requirements—researchers could isolate whether politeness itself influenced outcomes. This controlled approach is critical for distinguishing correlation from causation.

### Measuring Accuracy Impact

The study evaluated performance metrics including answer correctness for factual questions, code functionality for programming tasks, and human evaluation for subjective categories. Across the board, results showed minimal variance between polite and direct prompts. Statistical significance testing revealed that observed differences fell within normal noise margins rather than representing meaningful improvements.

Interestingly, some models showed negligible performance variations regardless of politeness level, while others demonstrated slight fluctuations that appeared random rather than directionally consistent. When directional patterns did emerge, they were small enough to be statistically insignificant.

### Cross-Model Consistency

The researchers tested multiple model architectures and sizes. Larger models like GPT-4 and specialized reasoning models showed virtually no performance difference based on prompt politeness. Smaller models sometimes showed minor variations, but these didn't correlate consistently with politeness presence or absence.

This consistency across different model families suggests the finding isn't an artifact of a particular architecture or training approach. Instead, it reflects something fundamental about how these systems process language: politeness markers don't constitute meaningful signal for task performance.

## Implications for Users and Practitioners

This finding has practical consequences for how people optimize their interaction with language models. If politeness doesn't improve accuracy, practitioners working with tight token budgets—particularly relevant for API usage—could save tokens by omitting courteous phrasing and focusing on clear, specific task instructions instead.

However, this doesn't mean being rude produces better results. The research found no evidence that impolite language *harmed* performance either. The finding is more precisely: politeness is neutral rather than beneficial.

The results also validate a different approach to prompt engineering: focusing on clarity, specificity, and task structure rather than social conventions. Instructions that clearly delineate what the model should do, with explicit constraints and format requirements, appear more impactful than courtesy.

## What happens next

This research joins a growing body of work examining which prompt engineering techniques actually work versus which are cargo-cultish habits. As the field matures, practitioners may shift from arbitrary best practices toward evidence-based optimization strategies.

The 187 comments on the original Hacker News discussion reveal expected skepticism and exploration of edge cases. Some users noted that while politeness doesn't help accuracy, it might affect other dimensions like tone consistency in outputs or perceived safety. Others questioned whether findings generalize across all task types or remain limited to the specific domains tested.

Future research might investigate whether politeness affects other metrics beyond accuracy—like output consistency, creativity, or safety guardrail adherence—even if it doesn't improve core task performance.

For now, the practical takeaway is clear: focus your prompt engineering efforts where evidence shows they matter.
*This article does not contain affiliate links.*
