resource "azurerm_kubernetes_cluster" "aks" {
  name                = var.cluster_name
  resource_group_name = var.resource_group_name
  location            = var.location
  dns_prefix          = var.dns_prefix

  # System node pool
  default_node_pool {
    name                = "system"
    node_count          = var.node_count
    vm_size             = var.vm_size
    enable_auto_scaling  = true
    min_count           = var.min_count
    max_count           = var.max_count

    upgrade_settings {
      max_surge = "10%"
    }
  }

  # Managed identity — no service principal needed
  identity {
    type = "SystemAssigned"
  }

  # Container Insights — linked to Log Analytics
  oms_agent {
    log_analytics_workspace_id = var.log_analytics_workspace_id
  }

  # Network configuration
  network_profile {
    network_plugin    = "kubenet"
    load_balancer_sku = "standard"
  }

  # RBAC enabled
  role_based_access_control_enabled = true

  tags = var.tags
}