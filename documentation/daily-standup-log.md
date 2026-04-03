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