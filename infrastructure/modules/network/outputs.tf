output "vnet_id" {
  description = "Resource ID of the VNet"
  value       = azurerm_virtual_network.vnet.id
}

output "vnet_name" {
  description = "Name of the VNet"
  value       = azurerm_virtual_network.vnet.name
}

output "aks_subnet_id" {
  description = "Resource ID of the AKS subnet"
  value       = azurerm_subnet.aks.id
}

output "pe_subnet_id" {
  description = "Resource ID of the private endpoints subnet"
  value       = azurerm_subnet.private_endpoints.id
}

output "runner_subnet_id" {
  description = "Resource ID of the GHA runner subnet"
  value       = azurerm_subnet.runner.id
}

output "acr_private_dns_zone_id" {
  description = "Resource ID of ACR private DNS zone"
  value       = azurerm_private_dns_zone.acr.id
}

output "kv_private_dns_zone_id" {
  description = "Resource ID of Key Vault private DNS zone"
  value       = azurerm_private_dns_zone.keyvault.id
}