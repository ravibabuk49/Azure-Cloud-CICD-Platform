# ADR-001: AKS vs App Service for Container Hosting

**Date:** 2025-04-03
**Status:** Accepted

## Context
We need a container hosting platform for eShopOnWeb (.NET 8).
Two primary options: Azure Kubernetes Service (AKS) and Azure App Service.

## Decision
We chose **AKS**.

## Reasons
- Supports advanced deployment patterns: canary, blue/green, rolling updates
- Native GitOps support via ArgoCD and Argo Rollouts
- Namespace isolation for dev/staging/prod on a single cluster
- Fine-grained RBAC, Network Policies, and Pod Security Standards
- Event-driven autoscaling via KEDA
- Full control over networking, ingress, and service mesh

## Consequences
- Higher operational complexity — requires kubectl, Helm, ArgoCD
- Node VM costs are the primary expense — mitigated via spot nodes and auto-shutdown
- More configuration required vs App Service managed platform