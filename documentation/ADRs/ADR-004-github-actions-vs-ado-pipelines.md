# ADR-004: GitHub Actions vs Azure DevOps Pipelines for CI/CD

**Date:** 2025-04-03
**Status:** Accepted

## Context
We need a CI/CD tool to automate build, test, security scanning,
and deployment pipelines. Two options: GitHub Actions and Azure DevOps Pipelines.

## Decision
We chose **GitHub Actions as primary CI/CD**.
Azure DevOps is used for Boards (sprint and work item management) only.

## Reasons
- OIDC federated credentials enable passwordless Azure authentication
- Reusable workflows reduce YAML duplication across pipelines
- Matrix builds enable parallel testing across OS and runtime versions
- GitHub Environments provide deployment protection rules and approval gates
- Native integration with GitHub repository events (push, PR, release)
- Workflow dispatch enables manual deployment triggers with input parameters

## Consequences
- Self-hosted runner required for private Azure resource access inside VNet
- ADO Pipelines experience is not demonstrated through working pipelines
- Public repository required to maximise runner availability
- Runner must be managed and kept online during active development
