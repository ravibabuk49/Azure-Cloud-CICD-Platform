# Root module — calls all sub-modules


module "monitoring" {
  source              = "./modules/monitoring"
  law_name            = var.law_name
  resource_group_name = var.monitoring_resource_group_name
  location            = var.location
  tags                = var.tags
}

module "acr" {
  source              = "./modules/acr"
  acr_name            = var.acr_name
  resource_group_name = var.acr_resource_group_name
  location            = var.location
  tags                = var.tags
}

module "aks" {
  source                     = "./modules/aks"
  cluster_name               = var.cluster_name
  resource_group_name        = var.aks_resource_group_name
  location                   = var.location
  dns_prefix                 = var.dns_prefix
  node_count                 = var.node_count
  min_count                  = var.min_count
  max_count                  = var.max_count
  vm_size                    = var.vm_size
  log_analytics_workspace_id = module.monitoring.workspace_id
  tags                       = var.tags

  depends_on = [module.monitoring]
}

module "keyvault" {
  source                     = "./modules/keyvault"
  keyvault_name              = var.keyvault_name
  resource_group_name        = var.infra_resource_group_name
  location                   = var.location
  tenant_id                  = var.tenant_id
  soft_delete_retention_days = var.soft_delete_retention_days
  tags                       = var.tags
}