# ADR-003: Terraform vs Bicep for Infrastructure as Code

**Date:** 2025-04-03
**Status:** Accepted

## Context
We need an IaC tool to define and deploy all Azure infrastructure.
Two primary options: HashiCorp Terraform and Microsoft Bicep.

## Decision
We chose **Terraform**.

## Reasons
- Multi-cloud provider support — not locked to Azure
- Remote state management with locking via Azure Blob Storage backend
- Large provider ecosystem and community module registry
- terraform plan produces explicit diff of changes before apply
- Drift detection easier to implement via scheduled plan runs
- Workspace support for environment separation

## Consequences
- Requires separate state storage — Azure Blob Storage backend
- State file must be protected — contains sensitive resource metadata
- HCL syntax differs from ARM/Bicep — separate learning curve
- Provider version pinning required to prevent unexpected breaking changes
