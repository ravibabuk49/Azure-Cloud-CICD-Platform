# Azure Cloud CICD Platform
![CI Pipeline](https://github.com/ravibabuk49/Azure-Cloud-CICD-Platform/actions/workflows/ci.yml/badge.svg)
![Terraform](https://github.com/ravibabuk49/Azure-Cloud-CICD-Platform/actions/workflows/terraform-infra.yml/badge.svg)

> Enterprise CI/CD Platform — eShopOnWeb (.NET 8) deployed to AKS
> GitHub Actions · Terraform · AKS · ACR · ArgoCD · Argo Rollouts · Python Automation

## Tech Stack

| Area | Tools |
|---|---|
| CI/CD | GitHub Actions (OIDC) |
| IaC | Terraform |
| Container Platform | AKS + Helm + ArgoCD |
| Canary Deployments | Argo Rollouts |
| Security | OPA Gatekeeper · cosign · Trivy · Defender |
| Observability | Log Analytics · App Insights · Azure Monitor |
| Automation | Python 3.12 (scripts) |
| Boards | Azure DevOps (Scrum) |

## Project Status

| Week | Focus | Status |
|---|---|---|
| Week 1 | Foundation · Terraform IaC · Core Infrastructure | 🔄 In Progress |
| Week 2 | CI Pipeline · DevSecOps Gates | ⏳ Pending |
| Week 3 | CD Pipeline · Monitoring · Observability · Security | ⏳ Pending |
| Week 4 | Helm · GitOps · Canary · Load Testing · SRE | ⏳ Pending |
| Week 5 | Portfolio Polish · Interview Readiness | ⏳ Pending |

## Architecture

> Architecture diagram will be added after Day 5

## Repository Structure

Azure-Cloud-CICD-Platform/
├── .github/workflows/       # GitHub Actions CI/CD workflows
├── infrastructure/          # Terraform modules (AKS, ACR, KV, VNet, Monitoring)
├── kubernetes/              # K8s manifests, Kustomize overlays, Argo Rollouts
├── helm/eshoponweb/         # Helm chart for eShopOnWeb
├── application/             # eShopOnWeb source (forked from Microsoft)
├── monitoring/              # KQL queries, Workbook templates, alert rules
├── scripts/python/          # Python automation suite (scripts)
└── documentation/           # ADRs, runbooks, standup log, lessons learned

## Daily Journal

- [Daily Standup Log](documentation/daily-standup-log.md)
- [Lessons Learned](documentation/lessons-learned.md)

