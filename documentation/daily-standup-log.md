## Day 1 — Project Foundation

**Date:** 2025-04-03

**What I did:**
- Created GitHub repo Azure-Cloud-CICD-Platform (public)
- Built full folder structure and .gitignore
- Created ADO organization and project (Scrum process)
- Created Epic, 8 Features, Sprint 1, 5 PBIs
- Logged in to Azure cloud from azure CLI
- Created 4 Azure resource groups with tags in eastus
- Activated Python azure_env, installed 3 missing Azure SDK packages
- Wrote and ran azure_env_check.py — 9/9 checks passing
- Wrote ADR-001 through ADR-005

**What I learned:**
- subprocess.run() requires flags as separate list items not a single string
- ADO Scrum process uses PBIs and Effort — not User Stories and Story Points

**What is next:**
- Day 2 — Write ACR Terraform module and deploy
- Fork eShopOnWeb repository
- Write production Dockerfile
- Write acr_manager.py



## Day 2 — ACR Terraform Module + eShopOnWeb Fork

**Date:** 2026-04-06

**What I did:**
- Created Terraform root configuration (providers.tf, backend.tf, main.tf, variables.tf)
- Wrote ACR Terraform module (main.tf, variables.tf, outputs.tf)
- Created Terraform remote state storage account manually via portal
- Ran terraform init, validate, plan, apply — ACR deployed successfully
- Connected Azure Boards with GitHub — PBI linking working via AB# syntax
- Forked eShopOnWeb into application/ folder
- Written production multi-stage Dockerfile and .dockerignore

**What is next:**
- Build Docker image locally and verify
- Push image to ACR
- Write acr_manager.py
- Enable Defender for Containers

**Blockers:**
- az storage account create failing with SubscriptionNotFound — resolved by creating storage account via portal

