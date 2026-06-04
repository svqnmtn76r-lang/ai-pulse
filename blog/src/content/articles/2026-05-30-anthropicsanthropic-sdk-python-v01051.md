---
category: sdk_release
date: '2026-05-30'
generated_at: '2026-05-30T04:57:28.607513Z'
generated_by: claude-haiku-4-5-20251001
importance_score: 80
products: []
source_name: github:anthropics/anthropic-sdk-python
source_url: https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.105.1
template_type: explainer
title: anthropics/anthropic-sdk-python v0.105.1
word_count: 836
---

# Anthropic's Python SDK Adopts Trusted Publishing: What This Security Shift Means

Anthropic has released version 0.105.1 of its official Python SDK, marking a subtle but significant change in how the library reaches developers. The update implements Trusted Publishing for PyPI releases—a security enhancement that fundamentally changes the authentication mechanism for package deployment. While this might seem like an internal housekeeping detail, it represents an important step in modernizing software supply chain security practices.

## TL;DR

- **Trusted Publishing**: A new PyPI authentication method that replaces traditional API tokens with cryptographic identity verification through OIDC (OpenID Connect)
- **Zero token management**: Eliminates the need to store and manage long-lived API credentials in CI/CD environments
- **Supply chain security**: Reduces vulnerability to credential theft and unauthorized package releases
- **Impact**: Developers using the Anthropic Python SDK benefit from stronger assurances that packages they install are genuinely from Anthropic, not compromised through credential leaks

## Background

For years, Python package distribution has relied on a familiar pattern: developers generate API tokens, store them in CI/CD pipeline secrets, and use those credentials to authenticate when uploading packages to PyPI. This approach works but introduces friction and risk. Long-lived tokens must be stored somewhere, rotated periodically, and protected from exposure. If a token leaks—through a compromised CI/CD system, an accident in logs, or a supply chain attack—an attacker could potentially upload malicious packages under the legitimate project's identity.

Trusted Publishing addresses this architectural weakness by leveraging OpenID Connect (OIDC), a modern identity standard already in use across major cloud platforms and CI/CD systems. Rather than using a persistent credential, projects can now prove their identity through the CI/CD platform itself, using cryptographic verification that a specific workflow is running in an authorized context.

Major Python projects and infrastructure maintainers have advocated for this shift for several years. Python's own infrastructure switched to Trusted Publishing, along with projects like Django, Flask, and many others. Anthropic's adoption signals broader industry movement toward this more secure paradigm.

## How it works

### The Traditional Token Approach

Under the previous system, Anthropic would generate a PyPI API token and securely store it in GitHub Actions secrets. When the release workflow ran, it would retrieve this token and pass it to the PyPI upload tool. The system trusts that whoever possesses the token has authority to release new versions. This works, but creates a persistent attack surface—the token exists in multiple places (token generation interface, GitHub secrets storage, CI/CD memory during execution) and remains valid for months or years.

### Trusted Publishing with OIDC

With Trusted Publishing, the workflow is fundamentally different. When Anthropic's CI/CD system initiates a release, it doesn't retrieve a stored credential. Instead, the GitHub Actions runner generates a short-lived OIDC token that proves "I am GitHub Actions running the anthropic-sdk-python repository, in the official release workflow." PyPI validates this cryptographic proof directly with GitHub's identity provider. The entire exchange happens through standards-based cryptography, with no persistent secrets involved.

The benefits are substantial. Each release uses a unique, single-use credential valid for minutes rather than months. There's nothing to steal because the token is generated on-the-fly and immediately consumed. There's nothing to rotate or manage. And the chain of custody is cryptographically verifiable—PyPI can prove the exact repository, workflow, and conditions under which the package was released.

### Implementation Details

Anthropic's implementation required changes to their GitHub Actions configuration—specifically updating the release workflow to use OIDC token authentication rather than traditional API keys. PyPI's side already supported this functionality, so the primary work involved configuration and testing. The actual Python SDK code itself didn't change; this is purely about the deployment pipeline.

This update also assumes Anthropic has already configured PyPI to recognize their GitHub repository as a trusted publisher. PyPI maintains a list of OIDC identity providers and their authorized repositories, preventing unauthorized repositories from impersonating legitimate projects.

## What This Means for Users

For developers using the anthropic-sdk-python library, this change is largely transparent but meaningful. The security posture improves without requiring any action on their part. Package installations carry stronger guarantees about origin verification. If someone attempted to publish a malicious package under Anthropic's name, they would need to compromise Anthropic's GitHub infrastructure itself rather than simply obtaining a leaked token.

The change also sets an example in the Python AI/ML ecosystem. As AI becomes more critical infrastructure, the tools that deliver it deserve stronger security practices. Anthropic's move may encourage other AI/ML libraries to adopt similar standards.

## What Happens Next

As more projects adopt Trusted Publishing, PyPI's ecosystem becomes incrementally more resilient to supply chain attacks. The Python Packaging Authority has prioritized this transition, and most major projects have either adopted it or plan to.

For projects still using traditional tokens, the trajectory is clear: token-based authentication will eventually be deprecated. Adopting Trusted Publishing sooner rather than later makes sense, reducing future migration pressure.

**Learn more**: Detailed documentation on Trusted Publishing is available on PyPI's official guides, and GitHub's documentation covers OIDC token generation for CI/CD workflows.
*This article does not contain affiliate links.*
