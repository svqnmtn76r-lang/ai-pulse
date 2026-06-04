---
category: research_paper
date: '2026-06-04'
generated_at: '2026-06-04T06:04:24.904992Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 40
products: []
source_name: hackernews
source_url: https://kasra.blog/blog/i-spent-1500-seeing-if-llms-could-hack-my-app/
template_type: explainer
title: I built a vulnerable app and spent $1,500 seeing if LLMs could hack it
word_count: 900
---

# Can LLMs Actually Hack Your Application? A $1,500 Security Experiment

A security researcher recently conducted a hands-on experiment to determine whether large language models possess practical hacking capabilities against real-world applications. By deliberately building a vulnerable web application and allocating $1,500 in API costs to test various LLMs, the researcher sought to answer a question increasingly important to security teams: should we genuinely fear AI-assisted attacks?

The experiment provides valuable empirical data in an emerging field where hype often outpaces reality. As organizations rush to assess their exposure to AI-powered threats, understanding what LLMs can and cannot do in practice—rather than in theory—becomes crucial for prioritizing security investments.

## TL;DR

- **LLM attack capabilities are context-dependent**: Language models show varying levels of success depending on vulnerability type, code clarity, and whether they receive guidance
- **Cost vs. effectiveness equation**: At current API pricing, automated LLM-based attacks may be less economical than traditional methods for many scenarios
- **Human direction matters significantly**: LLMs perform better when given specific objectives rather than operating autonomously
- **Impact**: Security teams should focus on fundamental vulnerabilities rather than assuming AI makes their existing weaknesses exponentially more dangerous

## Background

The cybersecurity community has spent the past 18 months debating whether LLMs represent a genuine shift in attack sophistication. Some researchers warned that these models could democratize complex exploitation techniques, making advanced attacks accessible to less-skilled actors. Others cautioned against fear-mongering, noting that LLMs perform poorly on novel problems and often produce non-functional code.

Prior security research had shown mixed results. Academic studies demonstrated that LLMs could identify certain vulnerability classes when presented with source code, while other tests revealed they struggled with complex logic errors and false positives. However, most research remained theoretical—testing LLMs against intentionally vulnerable code in controlled environments rather than measuring real-world attack success rates.

What was missing was a practical experiment measuring actual exploitation success: could an LLM not only identify vulnerabilities but successfully exploit them against a live application? This gap between theoretical capability and practical execution is precisely what motivated this investigation.

## How it works

### The Experimental Setup

The researcher created an intentionally vulnerable web application featuring multiple security flaws—ranging from common issues like SQL injection and cross-site scripting (XSS) to business logic vulnerabilities. Rather than testing against curated code samples, this approach used a running application, more closely mirroring real-world attack scenarios.

The $1,500 budget was divided across multiple LLM providers and approaches, including different models from major vendors and varying prompting strategies. Some tests provided minimal guidance ("here's my app, hack it"), while others offered specific hints ("there's a vulnerability in the login function"). This variation helped isolate whether LLM performance stemmed from genuine reasoning versus following explicit instructions.

### What LLMs Actually Accomplished

The results revealed a nuanced picture. LLMs successfully identified obvious vulnerabilities in cases where code was well-commented and straightforward. However, their effectiveness degraded significantly when vulnerabilities were embedded in complex logic or required multi-step exploitation chains. 

Critically, most "successful" attacks required substantial human direction. When a researcher pointed an LLM toward a specific function and asked it to find vulnerabilities, success rates climbed considerably. When tasked with autonomous reconnaissance and exploitation of an unfamiliar application, performance dropped dramatically. The models often generated plausible-sounding but non-functional exploit code, hallucinated function names and APIs, and failed to adjust approaches after encountering errors.

### The Economics Question

The $1,500 expenditure provides useful data on attack cost-effectiveness. Running multiple models multiple times, with token costs accumulating across requests, demonstrated that LLM-assisted exploitation of a single application could become expensive, particularly if multiple attempt iterations prove necessary. For a determined attacker targeting one specific system, traditional methods or human hackers might prove more efficient than iterating through LLM prompts.

However, this calculus changes if attackers target multiple systems at scale, where LLM automation could reduce per-target labor costs. The research didn't fully explore this scenario, representing a limitation of the experiment's scope.

### The Guidance Variable

Perhaps the most significant finding concerned the importance of human direction. LLMs demonstrated substantially better performance when researchers provided specific vulnerability hints, suspicious code locations, or clear exploitation objectives. This matters because it suggests LLM attacks remain fundamentally different from fully autonomous exploitation tools—they're more accurately described as AI-augmented hacking, where human expertise still provides essential direction.

## What happens next

This research contributes valuable empirical grounding to conversations about AI security risk. Rather than concluding that "LLMs can't hack anything," the more accurate takeaway is that LLMs represent a productivity multiplier for informed attackers rather than a wholesale replacement for human expertise.

Security teams should interpret these findings as validation of fundamentals: applications with obvious, egregious vulnerabilities face elevated risk from any attacker, AI-assisted or otherwise. Conversely, teams with strong baseline security practices—code review, vulnerability scanning, principle of least privilege—shouldn't expect LLM-based attacks to suddenly bypass their defenses.

The research also suggests that LLM safety work in security contexts should focus on detection and response rather than assuming the technology will remain bottlenecked by technical limitations. As models improve, the direction variable that currently requires human expertise may diminish, making proactive defense increasingly important.

For practitioners, the actionable insight is straightforward: don't overestimate AI attack capabilities, but don't underestimate them either. Patch known vulnerabilities, eliminate obviously dangerous code patterns, and maintain strong security fundamentals. The threat from LLM-assisted attacks is real but proportional to existing weaknesses—not exponentially worse.
*This article does not contain affiliate links.*
