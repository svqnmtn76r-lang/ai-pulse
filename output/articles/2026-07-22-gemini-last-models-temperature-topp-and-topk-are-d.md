---
category: feature_update
date: '2026-07-22'
generated_at: '2026-07-22T04:26:50.219246Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: hackernews
source_url: https://ai.google.dev/gemini-api/docs/latest-model
template_type: breaking
title: 'Gemini last models: temperature, top_p, and top_k are deprecated and ignored'
word_count: 327
---

## TL;DR

- **Parameter Deprecation**: Google has deprecated temperature, top_p, and top_k parameters in its latest Gemini models, marking a shift in how the API handles response generation control.
- **Functional Impact**: These parameters are now ignored by the API, potentially affecting developers who rely on fine-tuning model behavior through sampling configuration.
- **Migration Required**: Developers using affected Gemini models must update their implementations to remove or replace deprecated parameters before they're fully phased out.

## What happened

Google has officially deprecated three core sampling parameters—temperature, top_p, and top_k—across its latest Gemini models, according to documentation updates on the Google AI developer portal. The parameters, which have long been standard tools for controlling randomness and diversity in large language model outputs, are now ignored by the API when specified.

This represents a notable departure from conventional LLM API design patterns. Temperature typically controls output randomness (0 being deterministic, higher values increasing variation), while top_p and top_k implement nucleus and ranked sampling strategies respectively. Their removal suggests Google is either implementing automatic parameter optimization or fundamentally restructuring how the latest Gemini versions handle response generation.

The change affects developers building applications on the Gemini API who have relied on these parameters to adjust model behavior for specific use cases—from highly deterministic customer service responses to more creative content generation. The update has already drawn attention on technical communities, accumulating 17 comments on Hacker News as developers grapple with the implications.

Google hasn't provided explicit timeline details for complete parameter removal or guidance on alternative mechanisms for controlling output behavior, leaving some uncertainty about migration paths for production systems.

## What happens next

Developers should audit their Gemini API implementations to identify deprecated parameter usage and prepare updated code paths. Watch for official Google documentation updates providing either alternative control mechanisms or clarification on whether automatic optimization adequately replaces manual tuning. This could signal a broader industry shift toward removing user-facing sampling controls in favor of internally optimized defaults.
*This article does not contain affiliate links.*
