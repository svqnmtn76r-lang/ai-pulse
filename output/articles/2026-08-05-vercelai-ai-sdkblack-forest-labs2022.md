---
category: sdk_release
date: '2026-08-05'
generated_at: '2026-08-05T04:18:14.390141Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:vercel/ai
source_url: https://github.com/vercel/ai/releases/tag/%40ai-sdk/black-forest-labs%402.0.22
template_type: explainer
title: vercel/ai @ai-sdk/black-forest-labs@2.0.22
word_count: 770
---

# Vercel AI SDK Fixes FLUX 3 Video Cost Reporting: What Developers Need to Know

The Vercel AI team has released version 2.0.22 of the @ai-sdk/black-forest-labs package, addressing a critical issue with how costs are reported for FLUX 3 video generations. This patch resolves a problem where final pricing information was being lost during the video generation workflow, affecting developers who rely on accurate cost tracking for their AI video generation features.

## TL;DR

- **Cost estimation vs. settlement**: FLUX 3 video generation returns different cost information at different stages—initial submission returns estimates, while final results now properly include actual settled costs
- **SettledCostResultResponse**: The result endpoint now correctly preserves cost data through a dedicated response structure, preventing data loss during the response pipeline
- **Impact**: Developers using FLUX 3 for video generation can now accurately track and bill for completed video generation jobs without losing pricing information

## Background

Implementing AI-powered video generation in production applications introduces complexities around cost tracking and billing. Unlike text or image generation where costs can be determined upfront based on input parameters, video generation presents a unique challenge: the final cost often depends on properties of the finished video—such as duration, resolution, or processing complexity—that aren't known until generation completes.

The FLUX 3 model from Black Forest Labs represents a significant advancement in AI video generation capabilities. However, integrating it into Vercel's AI SDK required careful handling of the asynchronous, multi-stage nature of video generation workflows. The initial implementation had a gap: while the submit response could only provide cost estimates (since the video wasn't yet generated), the final result endpoint contained actual settled costs. Unfortunately, this cost information was being dropped during response processing, creating a blind spot for developers trying to implement proper usage tracking and billing systems.

## How It Works

### Understanding Two-Stage Cost Reporting

FLUX 3 video generation operates in stages, and each stage provides different cost information. When you submit a video generation request, the API returns immediately with a submit response. At this point, the system can only estimate costs based on request parameters—it doesn't yet know the actual computational resources the final video will require.

The estimation phase serves a practical purpose: it allows developers to show users predicted costs before committing to the operation. However, these estimates can vary from actual costs. The real cost emerges only after the video is fully generated, when the system knows exactly how many resources were consumed.

Previously, this final cost data existed in the system but wasn't making it to developers' applications. The cost was being calculated and stored internally but lost somewhere in the response handling pipeline.

### The SettledCostResultResponse Solution

Vercel's patch introduces proper support for `SettledCostResultResponse`—a dedicated response structure designed to carry actual, finalized cost data from the result endpoint. This response type maintains cost information throughout the entire response processing pipeline, ensuring developers receive accurate billing data.

When developers poll the result endpoint to check if their video has finished generating, they now receive this structured response that explicitly includes the settled cost. The term "settled" indicates this is the final, actual cost, not an estimate. This distinction matters for accurate accounting: developers can now differentiate between estimated costs shown during submission and actual costs incurred after completion.

### Integration in Developer Workflows

For developers using the Vercel AI SDK, this fix means the cost tracking workflow becomes more reliable. When implementing video generation features, they can now:

1. Submit a video generation request and display estimated costs to users
2. Poll the result endpoint as the video generates
3. Receive the actual settled cost in the final response
4. Use this accurate cost data for billing, usage tracking, or analytics

This enables more transparent user interactions and accurate backend accounting. Applications can now show users both what was estimated and what actually occurred, building trust and enabling proper cost management.

## What Happens Next

This patch is part of Vercel's ongoing refinement of their AI SDK's integration with various model providers and their specific capabilities. The fix addresses a specific edge case where modern video generation models' cost structures didn't align perfectly with the SDK's initial assumptions.

Developers currently using the @ai-sdk/black-forest-labs package with FLUX 3 video generation should upgrade to version 2.0.22 to ensure they're capturing complete cost data. For new implementations, this version provides the reliable cost tracking infrastructure needed for production deployments.

The broader pattern here reflects a maturing AI development ecosystem: as models become more sophisticated and use cases more complex, SDKs must evolve to handle real-world production requirements like accurate cost reporting, asynchronous workflows, and multi-stage operations.
*This article does not contain affiliate links.*
