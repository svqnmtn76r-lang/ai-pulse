---
category: sdk_release
date: '2026-06-02'
generated_at: '2026-06-02T05:56:56.099054Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:openai/openai-python
source_url: https://github.com/openai/openai-python/releases/tag/v2.39.0
template_type: explainer
title: openai/openai-python v2.39.0
word_count: 894
---

# OpenAI Python SDK v2.39.0: Enhanced Enterprise Security and API Flexibility

OpenAI has released version 2.39.0 of its official Python SDK, introducing several refinements aimed at improving enterprise security tracking, API response handling, and parameter flexibility. The update addresses authentication transparency in audit environments, streamlines tool-calling responses, and corrects an overly restrictive validation rule that affected action search functionality.

## TL;DR

- **Workload identity in audit logs**: Organizations can now track which workload or service initiated API requests through enhanced audit logging capabilities, critical for compliance and security monitoring in enterprise deployments.
- **Additional tools in responses**: The SDK now properly supports the `additional_tools` field in API responses, enabling better handling of dynamically suggested or recommended tools alongside primary results.
- **ActionSearch.query parameter flexibility**: A previous requirement making the `query` field mandatory in ActionSearch has been relaxed to optional, allowing for more flexible search implementations.
- **Impact**: This release strengthens security observability for enterprise users while making the SDK more adaptable to varied tool-use patterns and search scenarios.

## Background

The OpenAI Python SDK serves as the primary interface for Python developers integrating OpenAI's models and services into applications. As enterprise adoption of large language models has accelerated, the gap between model capabilities and operational visibility has become increasingly problematic. Organizations deploying AI systems in production environments need granular control over audit trails and the ability to trace requests back to specific workloads or service accounts—a requirement driven by regulatory compliance, cost allocation, and security governance.

Similarly, the SDK's response handling has evolved alongside OpenAI's APIs. As the platform introduced richer response structures, including optional tool recommendations and suggestions, the SDK needed to catch up with these new fields to prevent data loss or parsing errors.

The previous iteration of the ActionSearch functionality imposed strict validation rules that didn't account for legitimate use cases where search operations might not require an explicit query parameter—for instance, when searching based on context or filters alone.

## How it Works

### Workload Identity Tracking in Audit Logs

Workload identity represents a mechanism for identifying the specific service, container, or microservice that initiated an API request, separate from the user or organization making the call. In enterprise environments, multiple internal services often share authentication credentials or operate under the same organizational account. Without workload identity, audit logs can only show that "your organization made this request," but not which internal system was responsible.

With v2.39.0, the SDK now propagates and preserves workload identity information when generating audit logs. This enhancement allows organizations to attribute API usage to specific applications, scheduled jobs, or microservices within their infrastructure. For compliance auditing, this means teams can demonstrate exactly which system accessed which data and when. For cost analysis, it enables accurate chargeback models across internal departments. This is particularly valuable for organizations subject to SOC 2, HIPAA, or other regulatory frameworks requiring detailed access logs.

The implementation leverages existing audit logging mechanisms but enriches the metadata payload to include workload identifiers. DevOps and platform engineering teams can configure these identifiers during SDK initialization or through environment variables, making the feature accessible without code changes to individual applications.

### Additional Tools Field Support

OpenAI's API responses sometimes include an `additional_tools` field—a collection of tools, integrations, or capabilities that the model recommends or suggests alongside the primary response. This might include related functions the model thinks could be useful, alternative implementations, or supplementary tools that enhance the primary result.

Previous SDK versions either didn't recognize this field or handled it inconsistently, potentially discarding this auxiliary information. Version 2.39.0 adds proper parsing and object mapping for `additional_tools`, ensuring developers receive complete response data. When the API includes tool recommendations, the SDK now exposes them as structured objects rather than losing them during deserialization.

This matters for applications that want to present users with additional capabilities or options. A task-planning AI, for example, might receive a primary recommended workflow plus suggestions for alternative approaches—and developers can now access both. The consistent handling also future-proofs applications against API changes that might make this field more prominent.

### ActionSearch.query Parameter Flexibility

ActionSearch previously required a `query` field as mandatory, reflecting an assumption that search operations always involve an explicit search string. However, real-world search scenarios often rely on alternative mechanisms—filters, context parameters, sort specifications, or metadata-based retrieval where a traditional query string is unnecessary or redundant.

The v2.39.0 release relaxes this constraint, making the `query` parameter optional. Developers can now construct ActionSearch requests that rely entirely on filters or other parameters, or requests where the query is inferred from context. This particularly benefits applications implementing faceted search, metadata-driven retrieval, or semantic search patterns where the traditional keyword query paradigm doesn't apply.

The change maintains backward compatibility—existing code using explicit queries continues to work unchanged—while unblocking new patterns and use cases.

## What Happens Next

Teams running the OpenAI Python SDK should evaluate whether these features address their current operational challenges. If you're operating at scale and struggling with audit trail attribution, updating to v2.39.0 enables workload identity implementation. If your applications consume the full response structure from OpenAI's APIs, upgrading ensures you're not inadvertently losing data.

The release reflects OpenAI's iterative approach to SDK maturity: stabilizing enterprise features, accommodating diverse API usage patterns, and removing unnecessary constraints that limit flexibility. For continued updates and detailed migration guidance, monitor the official OpenAI Python SDK repository and release notes.
*This article does not contain affiliate links.*
