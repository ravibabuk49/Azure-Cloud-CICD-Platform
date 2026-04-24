location = "eastus"

# Monitoring
law_name                       = "law-eshoponweb-dev"
monitoring_resource_group_name = "rg-eshoponweb-monitoring"

# ACR
acr_name                = "acreshoponwebdev"
acr_resource_group_name = "rg-eshoponweb-acr"

# AKS
cluster_name            = "aks-eshoponweb-dev"
aks_resource_group_name = "rg-eshoponweb-aks"
dns_prefix              = "eshoponweb-dev"
node_count              = 2
min_count               = 1
max_count               = 3
vm_size                 = "Standard_D2s_v3"

# Tags
tags = {
  Project     = "Azure-Cloud-CICD-Platform"
  Environment = "dev"
  Owner       = "ravibabuk49"
  ManagedBy   = "Terraform"
}

# Key Vault
keyvault_name              = "kv-eshoponweb-dev"
infra_resource_group_name  = "rg-eshoponweb-infra"
tenant_id                  = "1b8dc78a-ea1c-4329-9d68-460d405b5904"
soft_delete_retention_days = 90

# Network
vnet_name = "vnet-eshoponweb-dev" # Pipeline test - Day 6
