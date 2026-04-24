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

## Day 3 — AKS Cluster Deployment via Terraform

**Date:** 2026-04-13

**What I did:**
- Wrote Log Analytics Terraform module (main.tf, variables.tf, outputs.tf)
- Wrote AKS Terraform module (main.tf, variables.tf, outputs.tf)
- Updated root main.tf and variables.tf to include monitoring and AKS modules
- Updated dev.tfvars with AKS and Log Analytics values
- Ran terraform init, plan, apply — deployed Log Analytics + AKS in 5m43s
- Connected kubectl to AKS cluster
- Created 3 namespaces: eshoponweb-dev, eshoponweb-staging, eshoponweb-prod
- Installed KEDA via Helm — all 3 pods running
- Attached ACR to AKS via managed identity — no credentials needed
- Verified Container Insights running as ama-logs (renamed from omsagent)
- Wrote and ran aks_health.py — 1 node ready, 3 namespaces checked

**What I learned:**
- Log Analytics must be deployed before AKS — depends_on ensures ordering
- Microsoft renamed omsagent to ama-logs in newer AKS versions
- enable_auto_scaling attribute name varies by AzureRM provider version
- OIDC issuer is automatically enabled on new AKS clusters

**What is next:**
- Day 4 — Key Vault Terraform module
- GitHub OIDC federated credentials setup
- Self-hosted GHA runner inside VNet
- Write kv_expiry_checker.py

## Day 4 — Key Vault, GitHub OIDC & Self-Hosted GHA Runner

**Date:** 2026-04-17

**What I did:**
- Wrote Key Vault Terraform module (main.tf, variables.tf, outputs.tf)
- Deployed Key Vault via terraform apply
- Stored 4 initial secrets in Key Vault (ACR, AKS values)
- Configured GitHub OIDC federated credentials — passwordless Azure auth
- Created App Registration, Service Principal, federated credentials
- Added AZURE_CLIENT_ID, TENANT_ID, SUBSCRIPTION_ID to GitHub secrets
- Tested OIDC via test-oidc.yml workflow — verified passing
- Deployed self-hosted GHA runner as ACI
- Verified runner showing Idle in GitHub Actions settings
- Wrote kv_expiry_checker.py — lists secrets and flags expiry

**What I learned:**
- System node pools cannot scale to 0 — must stop entire cluster
- OIDC federated credentials require separate credentials per branch/event
- Self-hosted runner needs ACCESS_TOKEN as secure environment variable

**What is next:**
- Day 5 — Network infrastructure Terraform module (VNet, NSGs, private endpoints)


## Day 5 — Network Infrastructure Terraform Module

**Date:** 2026-04-17

**What I did:**
- Wrote Network Terraform module (VNet, 3 subnets, NSG, private DNS zones)
- Deployed VNet with 3 subnets: snet-aks, snet-private-endpoints, snet-runner
- Added NSG with deny-internet-inbound and allow-https-outbound rules
- Created private DNS zones for ACR and Key Vault linked to VNet
- Added Key Vault private endpoint successfully
- Skipped ACR private endpoint — Basic SKU does not support it (Premium required)
- AKS modified to reference network module outputs
- Validated all network resources via az CLI

**What I learned:**
- ACR Basic SKU does not support private endpoints — Premium SKU required
- AKS cannot be modified while in stopped state — must be running
- Private DNS zones need VNet links for DNS resolution to work
- Runner subnet needs ACI delegation for Container Instance deployment

**What is next:**
- Day 6 — GitHub Actions IaC pipeline (Terraform workflow)
