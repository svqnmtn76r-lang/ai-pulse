---
category: tutorial
date: '2026-06-29'
generated_at: '2026-06-29T01:54:23.667984Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 60
products: []
source_name: hackernews
source_url: https://antoine.fi/mri-analysis-using-claude-code-opus
template_type: explainer
title: I used Claude Code to get a second opinion on my MRI
word_count: 924
---

# Using AI to Review Medical Imaging: What Happens When You Run an MRI Through Claude Code

An engineer recently experimented with Claude Code, Anthropic's latest AI capability, to analyze their own MRI scan—essentially asking an AI for a second opinion on medical imaging. The project sparked significant discussion in the tech community, with 452 comments on Hacker News debating the promise and peril of AI-assisted medical image analysis.

This experiment sits at the intersection of generative AI capabilities and healthcare, raising practical questions about how AI models can assist with medical analysis without replacing professional radiologists.

## TL;DR

- **Claude Code execution**: The latest version of Claude can analyze images programmatically, enabling detailed medical image inspection
- **Pattern recognition at scale**: AI models trained on vast datasets can identify anatomical features and potential anomalies in medical images
- **Supplementary tool**: This approach works best as a preliminary screening or verification tool, not as a replacement for professional medical interpretation
- **Impact**: Demonstrates accessible pathways for AI-assisted analysis while highlighting the importance of human validation in healthcare contexts

## Background

Medical image analysis has long been a challenging domain for automation. Radiologists spend years training to interpret CT scans, MRIs, and X-rays, developing intuition for distinguishing normal anatomy from pathology. Traditional machine learning approaches showed promise in narrow domains—detecting specific conditions like pneumonia or certain cancers—but struggled with the nuance required for comprehensive image review.

The emergence of large vision models changed this landscape. Models trained on billions of images developed stronger pattern recognition capabilities. However, medical imaging presents unique challenges: images require interpretation within specific clinical contexts, stakes are high, and regulatory frameworks demand clear accountability.

Previous attempts at AI-assisted diagnosis have shown both promise and limitations. IBM's Watson for Oncology, for instance, generated significant hype but faced real-world challenges translating general intelligence into reliable clinical decision support. More successful approaches have focused on narrow applications with clear metrics—detecting specific abnormalities in defined anatomical regions.

## How it works

### Image Analysis as a Programmatic Task

Claude Code represents a different approach: rather than a specialized medical AI tool, it's a general-purpose AI with vision capabilities that can be programmed to analyze images systematically. The engineer's experiment involved uploading an MRI scan and writing code that guided Claude through structured analysis steps.

This approach treats medical image analysis as a code execution problem. Claude reads the image, identifies anatomical structures, notes potential areas of concern, and can even generate detailed reports following clinical conventions. The programmatic aspect matters significantly—rather than getting a single response, the user can instruct the AI to follow specific protocols, compare regions, and organize findings logically.

### Pattern Recognition in Medical Context

Large vision models achieve medical image competency through training on massive image collections, though exactly which medical datasets train models like Claude remains proprietary. These models learn to recognize anatomical landmarks—bone structures, tissue interfaces, fluid levels—that radiologists use to navigate complex three-dimensional anatomy in two-dimensional slices.

MRI scans present particular challenges because they're high-resolution, complex, and require understanding tissue signal characteristics. Different MRI sequences highlight different tissues; what appears bright on one sequence might appear dark on another. Claude's ability to contextualize these variations—recognizing that T1 and T2 sequences show different contrast patterns—suggests sophisticated learned understanding of MRI physics and anatomy.

### The Verification Workflow

The practical value emerges in workflow integration. Rather than replacing radiologist interpretation, this approach creates a systematic second opinion. The process might involve:

- Initial AI review identifying anatomical landmarks and potential areas requiring attention
- Structured reporting of findings in standard medical terminology
- Highlighting regions that deviate from normal anatomy
- Flagging areas where radiologist expertise would be particularly valuable

This differs fundamentally from autonomous diagnosis. The AI isn't claiming certainty; it's providing systematic analysis that a qualified human can then evaluate, verify, or challenge with their own expertise and clinical context.

## Limitations and Considerations

The experiment underscores important constraints. AI vision models, however sophisticated, lack the training context radiologists develop—understanding how imaging findings relate to patient symptoms, medical history, and clinical outcomes. They also lack accountability mechanisms; regulatory frameworks require clear responsibility chains in medical decision-making.

There's also a distinction between identifying that something *looks different* versus understanding whether that difference matters clinically. Radiologists integrate pattern recognition with differential diagnosis—the reasoning about what conditions could explain observed findings. Current AI systems excel at the former but struggle with the latter.

Additionally, liability and regulatory questions remain unsettled. Medical imaging interpretation falls under medical practice regulations in most jurisdictions. Tools that assist radiologists operate in a different regulatory category than tools intended for independent diagnosis.

## What happens next

This experiment reflects a broader trend: moving from specialized medical AI systems toward general AI tools that can be adapted for medical contexts. Rather than training purpose-built models for specific diagnoses, organizations can now use capable general models programmed for particular workflows.

This likely accelerates integration of AI into clinical practice, but through incremental augmentation rather than wholesale replacement. Radiologists gain tools for preliminary screening, quality assurance, and documentation rather than losing their role.

The real validation for this approach will come from clinical studies demonstrating whether AI-assisted review improves diagnostic accuracy, reduces radiologist burden, or both. Individual experiments provide intriguing proof-of-concept, but scaled deployment requires systematic evidence.

For practitioners exploring similar approaches, the key lesson is methodological: treat AI image analysis as a component of clinical workflow, not an alternative to it. The second opinion is valuable precisely because it comes before, and remains subject to, expert human judgment.
*This article does not contain affiliate links.*
