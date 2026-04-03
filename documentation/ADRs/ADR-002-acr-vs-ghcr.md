# ADR-002: Azure Container Registry vs GitHub Container Registry

**Date:** 2025-04-03
**Status:** Accepted

## Context
We need a container registry to store Docker images built by the CI pipeline.
Two options: Azure Container Registry (ACR) and GitHub Container Registry (ghcr.io).

## Decision
We chose **Azure Container Registry (ACR)**.

## Reasons
- Native AKS integration via managed identity — AcrPull role requires no credentials
- Supports Defender for Containers image scanning
- Supports cosign image signing and SBOM as OCI artifacts
- Private endpoint support for secure VNet-only access
- Geo-replication support for multi-region deployments
- Content trust and retention policies built in

## Consequences
- Costs approximately $5/month for Basic SKU
- Requires private endpoint configuration for VNet-restricted access
- geo-replication not used in this project — Basic SKU limitation