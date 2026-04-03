# ADR-005: Namespace-Per-Environment Strategy on AKS

**Date:** 2025-04-03
**Status:** Accepted

## Context
We need to decide how to separate dev, staging, and production environments
on AKS. Options: separate clusters per environment, or namespaces on one cluster.

## Decision
We chose **namespace-per-environment on a single AKS cluster**.

## Reasons
- ResourceQuotas and LimitRanges enforce resource boundaries per namespace
- NetworkPolicies prevent cross-namespace communication
- OPA Gatekeeper and Pod Security Standards apply at namespace level
- Single control plane simplifies cluster management and monitoring
- ArgoCD manages all three environments from one installation

## Consequences
- Shared control plane — not as isolated as separate clusters
- ResourceQuotas must be correctly sized to prevent namespace resource starvation
- NetworkPolicies required to enforce namespace isolation
- Single cluster failure affects all environments simultaneously
- A single production cluster usually consists of multiple worker nodes across different availability zones (AZs) for high availability

