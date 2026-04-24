variable "keyvault_name" {
  description = "Name of the Key Vault (must be globally unique)"
  type        = string
}

variable "resource_group_name" {
  description = "Resource group for Key Vault"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
}

variable "tenant_id" {
  description = "Azure AD tenant ID"
  type        = string
}

variable "soft_delete_retention_days" {
  description = "Number of days to retain soft deleted secrets"
  type        = number
  default     = 90
}

variable "tags" {
  description = "Tags to apply to Key Vault"
  type        = map(string)
  default     = {}
}

variable "pe_subnet_id" {
  description = "Subnet ID for private endpoint"
  type        = string
  default     = ""
}

variable "kv_private_dns_zone_id" {
  description = "Private DNS zone ID for Key Vault"
  type        = string
  default     = ""
}