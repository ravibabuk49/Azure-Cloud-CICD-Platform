data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "kv" {
  name                = var.keyvault_name
  resource_group_name = var.resource_group_name
  location            = var.location
  tenant_id           = var.tenant_id
  sku_name            = "standard"

  # Add this line to enforce RBAC instead of Access Policies
  enable_rbac_authorization = true

  # Security settings
  soft_delete_retention_days = var.soft_delete_retention_days
  purge_protection_enabled   = false

  tags = var.tags
}

# Grant current user Key Vault Secrets Officer role
resource "azurerm_role_assignment" "kv_secrets_officer" {
  scope                = azurerm_key_vault.kv.id
  role_definition_name = "Key Vault Secrets Officer"
  principal_id         = data.azurerm_client_config.current.object_id
}


# ── Private Endpoint for Key Vault
resource "azurerm_private_endpoint" "kv_pe" {
  name                = "pe-kv-eshoponweb"
  resource_group_name = var.resource_group_name
  location            = var.location
  subnet_id           = var.pe_subnet_id

  private_service_connection {
    name                           = "psc-kv"
    private_connection_resource_id = azurerm_key_vault.kv.id
    subresource_names              = ["vault"]
    is_manual_connection           = false
  }

  private_dns_zone_group {
    name                 = "kv-dns-zone-group"
    private_dns_zone_ids = [var.kv_private_dns_zone_id]
  }

  tags = var.tags
}