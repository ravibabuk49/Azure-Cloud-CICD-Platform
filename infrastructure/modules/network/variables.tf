variable "vnet_name" {
  description = "Name of the Virtual Network"
  type        = string
}

variable "resource_group_name" {
  description = "Resource group for network resources"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
}

variable "vnet_address_space" {
  description = "Address space for the VNet"
  type        = list(string)
  default     = ["10.0.0.0/16"]
}

variable "aks_subnet_prefix" {
  description = "Address prefix for AKS subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "pe_subnet_prefix" {
  description = "Address prefix for private endpoints subnet"
  type        = string
  default     = "10.0.2.0/24"
}

variable "runner_subnet_prefix" {
  description = "Address prefix for GHA runner subnet"
  type        = string
  default     = "10.0.3.0/24"
}

variable "tags" {
  description = "Tags to apply to network resources"
  type        = map(string)
  default     = {}
}