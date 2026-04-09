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



## Day 2 — ACR Terraform Module + Docker + ACR Push

**Date:** 2026-04-06 to 2026-04-09

**What I did:**
- Created Terraform root configuration (providers.tf, backend.tf, main.tf, variables.tf)
- Wrote ACR Terraform module (main.tf, variables.tf, outputs.tf)
- Created Terraform remote state storage account manually via portal
- Ran terraform init, validate, plan -out=tfplan, apply — ACR deployed successfully
- Connected Azure Boards with GitHub — PBI linking working via AB# syntax
- Forked eShopOnWeb into application/ folder
- Fixed Dockerfile — root cause was missing Directory.Packages.props
  and global.json in Docker build context
- Built eshoponweb:local image successfully (430MB runtime image)
- Pushed eshoponweb:v1 to ACR successfully
- Wrote and ran acr_manager.py — confirmed v1 tag visible in ACR
- Enabled Defender for Containers (29 days free trial active)
- Created scripts/python/README.md documenting all 8 scripts

**What I learned:**
- eShopOnWeb uses central package management via Directory.Packages.props
- Multi-stage Docker build discards 2.23GB build stage, keeps 430MB runtime image
- Azure Boards + GitHub integration links commits to PBIs via AB# syntax
- Defender for Containers provides 3 layers of protection: image scanning,
  runtime threat detection, and security posture recommendations

**Blockers:**
- az storage account create failed with SubscriptionNotFound despite correct
  subscription being active — resolved by creating storage account via portal
- Dockerfile failed 3 times before identifying Directory.Packages.props
  as the missing file in build context

**What is next:**
- Day 3 — Write AKS and Log Analytics Terraform modules
- Deploy AKS cluster via terraform apply
- Connect kubectl to AKS
- Create 3 namespaces, install KEDA
- Write aks_health.py

