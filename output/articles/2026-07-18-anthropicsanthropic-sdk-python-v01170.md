---
category: sdk_release
date: '2026-07-18'
generated_at: '2026-07-18T04:07:24.182724Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/anthropic-sdk-python
source_url: https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.117.0
template_type: explainer
title: anthropics/anthropic-sdk-python v0.117.0
word_count: 839
---

# Anthropic SDK Python v0.117.0: Dreaming and MCP Tunnels Come to Python Developers

Anthropic has released version 0.117.0 of its Python SDK, introducing two significant capabilities that expand what developers can do with Claude through Python applications. The update brings support for a new "dreaming" feature and Model Context Protocol (MCP) Tunnels, while also addressing security concerns around credential exposure in error logs.

## TL;DR

- **Dreaming support**: A new API feature now accessible to Python developers, though specifics about its functionality remain limited in available documentation
- **MCP Tunnels**: Enables secure communication pathways between Claude and external tools and data sources through the Model Context Protocol
- **Security hardening**: Credentials are now protected from appearing in Python traceback frames, reducing exposure risk in error scenarios
- **Impact**: Python developers gain parity with other SDK implementations and enhanced security posture for production deployments

## Background

Anthropic's SDKs serve as the primary interface between developers and Claude, the company's large language model. The Python SDK has been a critical tool for machine learning engineers and Python developers building AI applications. Each release typically brings new API capabilities that Claude's backend has already introduced, ensuring all language implementations stay synchronized.

The inclusion of MCP support reflects a broader ecosystem strategy. MCP is a protocol Anthropic developed to standardize how AI systems interact with external tools, databases, and services. Previous SDK versions already supported basic MCP functionality, but the addition of Tunnels represents a more sophisticated implementation pattern for complex integrations.

The security fix addresses a class of vulnerabilities common in error handling: sensitive credentials inadvertently leaking into stack traces. This is particularly important for production systems where logs might be aggregated, searched, or reviewed by multiple team members.

## How it works

### Understanding Dreaming

The dreaming feature added in this release appears to be an advanced capability, though Anthropic's release notes provide minimal implementation details. Based on context from Anthropic's broader research, dreaming likely refers to an inference technique where Claude can engage in extended reasoning or exploratory processing before responding to queries. This internal "thinking" phase allows the model to work through complex problems more thoroughly, similar to how humans might think through a problem before articulating an answer.

For Python developers, this means new parameters or API methods to invoke this feature when making requests to Claude. The exact interface requirements would be found in the updated SDK documentation, but typical patterns involve adding flags to request objects or creating specialized message types that trigger this behavior.

### MCP Tunnels: Secure Tool Integration

MCP Tunnels represent a more sophisticated connection model than direct tool integration. Rather than having Claude directly call external services, Tunnels create secure communication channels that can handle complex scenarios: authentication, firewalls, rate limiting, and multi-step protocols that simple function calls cannot manage.

When you implement MCP Tunnels in Python, you're establishing a secure conduit between Claude and your backend systems. This is particularly valuable for enterprises where direct model-to-service connections may violate security policies. The tunnel can run on your infrastructure, applying your organization's authentication, logging, and governance policies while Claude makes requests through it.

### Credential Security Improvements

The bug fix addressing credential exposure in traceback frames uses Pydantic's `SecretStr` type to wrap sensitive strings. When Python raises an exception, the traceback includes local variables from each frame. Previously, API keys or credentials stored as plain strings would appear in these logs. By using `SecretStr`, the SDK ensures credentials are masked in string representations, appearing as `***` in logs rather than exposing actual values.

This protection is particularly important in containerized environments where logs are automatically collected, or in organizations using centralized logging systems. A developer debugging an unrelated error shouldn't inadvertently expose production credentials in their error logs.

## Implementation considerations

For teams updating to v0.117.0, the changes are largely additive. Existing code continues to work without modification, but you may want to explore the new features if your applications would benefit from them.

If you're building applications that need to access databases, APIs, or proprietary services alongside Claude, the MCP Tunnels support enables more robust integration patterns. You can now implement tunnel servers that handle authentication and access control, then point Claude to these tunnels rather than giving the model direct service access.

The dreaming feature should be evaluated based on your use case. For applications requiring complex reasoning—research tasks, multi-step problem solving, or nuanced decision making—enabling dreaming may improve response quality, though it will increase latency and API costs due to extended processing.

The credential security fix is transparent and beneficial to all users, particularly those running applications in shared environments or with centralized log aggregation.

## What happens next

Developers should review the full changelog and updated documentation at the GitHub repository to understand the complete API surface for these features. If you're maintaining production applications, prioritizing the update for security benefits is advisable. For new features, prototype with dreaming and MCP Tunnels to determine if they provide value for your specific use cases before rolling out to production.
*This article does not contain affiliate links.*
