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
    enable_auto_scaling = true
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

  # FIX: Tell Terraform the OIDC issuer is enabled so it stops trying to disable it
  oidc_issuer_enabled = true

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

  # This tells Terraform to stop trying to manage the node count now that auto-scaling is on.
  # Without this, every plan/apply after the initial creation would show changes to the node count as the cluster scales up/down.
  # In a real project, you might want to manage this differently, but for simplicity in this example we'll just ignore changes to the node count.
  # Note: This means Terraform won't be able to detect manual changes to the node count, so use with caution in production environments.
  # For more advanced management, consider using the azurerm_kubernetes_cluster_node_pool resource to manage node pools separately.
  lifecycle {
    ignore_changes = [
      default_node_pool[0].node_count
    ]
  }

}