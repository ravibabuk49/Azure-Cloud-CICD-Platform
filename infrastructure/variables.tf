variable "location" {
  description = "Azure region for all resources"
  type        = string
  default     = "eastus"
}

variable "acr_name" {
  description = "Name of the Azure Container Registry (must be globally unique)"
  type        = string
}

variable "acr_resource_group_name" {
  description = "Resource group for ACR"
  type        = string
  default     = "rg-eshoponweb-acr"
}

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