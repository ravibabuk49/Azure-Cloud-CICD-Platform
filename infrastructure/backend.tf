terraform {
  backend "azurerm" {
    resource_group_name  = "rg-eshoponweb-infra"
    storage_account_name = "tfstateeshoponweb"
    container_name       = "tfstate"
    key                  = "eshoponweb.tfstate"
  }
}