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