variable "location" {
  description = "Azure region for all resources"
  type        = string
  default     = "eastus"
}

# ── Monitoring
variable "law_name" {
  description = "Name of the Log Analytics Workspace"
  type        = string
}

variable "monitoring_resource_group_name" {
  description = "Resource group for monitoring resources"
  type        = string
  default     = "rg-eshoponweb-monitoring"
}

# ── ACR
variable "acr_name" {
  description = "Name of the Azure Container Registry"
  type        = string
}

variable "acr_resource_group_name" {
  description = "Resource group for ACR"
  type        = string
  default     = "rg-eshoponweb-acr"
}

# ── AKS
variable "cluster_name" {
  description = "Name of the AKS cluster"
  type        = string
}

variable "aks_resource_group_name" {
  description = "Resource group for AKS cluster"
  type        = string
  default     = "rg-eshoponweb-aks"
}

variable "dns_prefix" {
  description = "DNS prefix for AKS cluster"
  type        = string
}

variable "node_count" {
  description = "Initial number of nodes"
  type        = number
  default     = 2
}

variable "min_count" {
  description = "Minimum nodes for autoscaling"
  type        = number
  default     = 1
}

variable "max_count" {
  description = "Maximum nodes for autoscaling"
  type        = number
  default     = 3
}

variable "vm_size" {
  description = "VM size for node pool"
  type        = string
  default     = "Standard_D2s_v3"
}

# ── Tags
variable "tags" {
  description = "Tags applied to all resources"
  type        = map(string)
  default = {
    Project     = "Azure-Cloud-CICD-Platform"
    Environment = "dev"
    Owner       = "ravibabuk49"
    ManagedBy   = "Terraform"
  }
}

# ── Key Vault
variable "keyvault_name" {
  description = "Name of the Key Vault (must be globally unique)"
  type        = string
}

variable "infra_resource_group_name" {
  description = "Resource group for infrastructure resources"
  type        = string
  default     = "rg-eshoponweb-infra"
}

variable "tenant_id" {
  description = "Azure AD tenant ID"
  type        = string
}

variable "soft_delete_retention_days" {
  description = "Days to retain soft deleted secrets"
  type        = number
  default     = 90
}

# ── Network
variable "vnet_name" {
  description = "Name of the Virtual Network"
  type        = string
  default     = "vnet-eshoponweb-dev"
}

# ── Provider Authentication
variable "client_id" {
  description = "Azure AD application client ID for OIDC"
  type        = string
  default     = ""
}

variable "subscription_id" {
  description = "Azure subscription ID"
  type        = string
  default     = ""
}
