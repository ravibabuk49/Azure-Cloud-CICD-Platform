variable "cluster_name" {
  description = "Name of the AKS cluster"
  type        = string
}

variable "resource_group_name" {
  description = "Resource group for AKS cluster"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
}

variable "dns_prefix" {
  description = "DNS prefix for AKS cluster"
  type        = string
}

variable "node_count" {
  description = "Initial number of nodes in system node pool"
  type        = number
  default     = 2
}

variable "min_count" {
  description = "Minimum number of nodes for autoscaling"
  type        = number
  default     = 1
}

variable "max_count" {
  description = "Maximum number of nodes for autoscaling"
  type        = number
  default     = 3
}

variable "vm_size" {
  description = "VM size for system node pool"
  type        = string
  default     = "Standard_D2s_v3"
}

variable "log_analytics_workspace_id" {
  description = "Resource ID of Log Analytics Workspace for Container Insights"
  type        = string
}

variable "tags" {
  description = "Tags to apply to AKS cluster"
  type        = map(string)
  default     = {}
}