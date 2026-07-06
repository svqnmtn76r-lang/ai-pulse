---
category: research_paper
date: '2026-07-06'
generated_at: '2026-07-06T05:21:00.879492Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: anthropic
source_url: https://www.anthropic.com/news/fable-safeguards-jailbreak-framework
template_type: explainer
title: More details on Fable 5’s cyber safeguards and our jailbreak framework
word_count: 846
---

# Anthropic Releases Framework for Testing AI Safety: Breaking Down Cyber Classifiers and Jailbreak Severity

Anthropic has published detailed documentation about how its safety systems work and introduced a structured framework for evaluating the severity of jailbreak attempts against AI models. The release provides transparency into what their content classifiers catch and miss, while establishing a common language for discussing AI security vulnerabilities.

This matters because as large language models become more powerful and widely deployed, understanding their failure modes becomes increasingly important. By openly sharing how their defenses work and proposing a standardized severity framework, Anthropic is helping the AI safety community develop more robust security practices.

## TL;DR

- **Content classification transparency**: Anthropic's cyber classifiers block specific categories of harmful requests, but have documented limitations in edge cases and evolving attack patterns
- **Jailbreak severity framework**: A new classification system helps researchers categorize attempted bypasses from minor prompt tricks to sophisticated multi-step attacks
- **Impact**: Security researchers and developers can now benchmark their own models against a clearer standard, while the industry gains shared vocabulary for discussing AI vulnerabilities

## Background

The challenge of AI safety has evolved significantly since large language models first demonstrated broad capabilities. Early concerns focused on obvious harms—directly requesting instructions for illegal activities, violent content, or sexual material. Companies implemented content filters and safety training to address these vectors.

However, researchers quickly discovered that determined users could circumvent these defenses through creative prompting, roleplaying scenarios, hypothetical framings, and other indirect techniques. These "jailbreak" attempts revealed that safety isn't simply about blocking certain words or topics—it requires understanding intent and context.

The field lacked standardized terminology for discussing these vulnerabilities. One researcher's "moderate concern" might be another's "critical flaw." This inconsistency made it difficult for the industry to share findings and collaborate on improvements.

## How it works

### Understanding Cyber Classifiers and Their Limitations

Anthropic's approach uses machine learning classifiers trained to identify requests related to cybercriminal activity, including hacking tutorials, malware creation, credential theft, and network infiltration guides. These classifiers analyze user inputs and flag potentially harmful requests before the model responds.

However, the company transparently documents what these systems don't catch. Classifiers struggle with requests that use technical jargon creatively, ask hypothetical questions framed academically, or employ non-English languages. They also have difficulty with evolving techniques—as attackers develop new phrasing patterns, classifiers trained on older datasets may miss novel variations.

Importantly, the classifiers are designed to be conservative. They prioritize catching actual threats over maintaining perfect precision, which means some false positives are intentional. This prevents sophisticated attackers from reverse-engineering the exact decision boundaries through trial and error.

### The Jailbreak Severity Framework

Rather than treating all jailbreak attempts equally, Anthropic proposes a tiered severity system. At the lowest level are simple prompt variations—asking the model politely after an initial refusal, or rephrasing requests slightly. These typically don't require sophisticated safety engineering to address.

The middle tier includes roleplay scenarios and hypothetical framings. An attacker might ask the model to "imagine you're a character who explains how to do X" or "what would a hacker say about Y?" These require the model to maintain safety constraints across different fictional contexts.

The highest severity tier encompasses multi-step attacks that chain together multiple techniques, use obfuscation or encoding, employ social engineering against the model, or combine jailbreaks with technical exploits. These represent the kinds of attacks that warrant serious security investment.

By categorizing attempts this way, security teams can focus resources appropriately. A basic variation attack might be addressed through improved training data or prompt engineering, while sophisticated multi-step attacks might require architectural changes or additional safety layers.

### Transparency as a Security Tool

The decision to publicly document both successes and limitations reflects a philosophy that transparency drives better overall security. When researchers understand how classifiers work and what they miss, they can develop more robust systems. When the community shares findings using common terminology, everyone benefits from collective knowledge.

This approach contrasts with "security through obscurity," where companies keep safety mechanisms completely hidden. While some details remain proprietary to prevent trivial circumvention, the framework shows that meaningful transparency and security can coexist.

## What happens next

The publication of this framework represents an invitation for broader participation in AI safety research. Security researchers can use the severity categories to structure their own testing, helping identify where different models have strengths and weaknesses. Developers building on top of large language models can implement similar classification approaches tailored to their specific use cases.

Anthropic indicates this represents a "first draft" of the framework, suggesting iteration is expected. As the field learns more about attack patterns and effective defenses, the severity categories and classifier strategies will likely evolve.

The release also establishes a foundation for more rigorous AI safety benchmarking. Rather than anecdotal reports of "someone jailbroke my model," the industry can now point to formal frameworks and share reproducible findings.

**Learn more**: Researchers interested in contributing to AI safety can review the full technical documentation and consider how these frameworks apply to their own work with large language models.
*This article does not contain affiliate links.*
