# Root module — calls all sub-modules
# Modules will be added as we build each component
# For example, to add an Azure Container Registry (ACR) module, we would include it like this:
module "acr" {
  source              = "./modules/acr"
  acr_name            = var.acr_name
  resource_group_name = var.acr_resource_group_name
  location            = var.location
  tags                = var.tags
}