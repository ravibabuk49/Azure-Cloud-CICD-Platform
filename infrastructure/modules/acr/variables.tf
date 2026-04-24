variable "acr_name" {
  description = "Name of the Azure Container Registry"
  type        = string
}

variable "resource_group_name" {
  description = "Resource group where ACR will be created"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
}

variable "sku" {
  description = "ACR SKU tier"
  type        = string
  default     = "Basic"
}

variable "tags" {
  description = "Tags to apply to ACR"
  type        = map(string)
  default     = {}
}

variable "pe_subnet_id" {
  description = "Subnet ID for private endpoint"
  type        = string
  default     = ""
}

variable "acr_private_dns_zone_id" {
  description = "Private DNS zone ID for ACR"
  type        = string
  default     = ""
}

variable "enable_private_endpoint" {
  description = "Whether to create a private endpoint for ACR"
  type        = bool
  default     = false
}