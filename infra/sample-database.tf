provider "azurerm" {
  features {}
}

variable "sql_server_name" {
  description = "The name of the SQL Server"
}

variable "sql_server_database_name" {
  description = "The name of the SQL Database"
}

variable "sql_server_username" {
  description = "The username of the SQL Database"
}

variable "sql_server_password" {
  description = "The password of the SQL Database"
}

provider "random" {}

resource "random_id" "sample" {
  byte_length = 8
}

resource "azurerm_resource_group" "sample" {
  name     = "sample-resources-${random_id.sample.hex}"
  location = "eastus"

  tags = {
    deployment_id = random_id.sample.hex
  }
}

resource "azurerm_storage_account" "sample" {
  name                     = "samplesa${random_id.sample.hex}"
  resource_group_name      = azurerm_resource_group.sample.name
  location                 = azurerm_resource_group.sample.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    deployment_id = random_id.sample.hex
  }
}

resource "azurerm_mssql_server" "sample" {
  name                         = var.sql_server_name
  resource_group_name          = azurerm_resource_group.sample.name
  location                     = azurerm_resource_group.sample.location
  version                      = "12.0"
  administrator_login          = var.sql_server_username
  administrator_login_password = var.sql_server_password

  tags = {
    deployment_id = random_id.sample.hex
  }
}

resource "azurerm_mssql_database" "sample" {
  name           = var.sql_server_database_name
  server_id      = azurerm_mssql_server.sample.id
  collation      = "SQL_Latin1_General_CP1_CI_AS"
  license_type   = "LicenseIncluded"
  sku_name       = "S0"
  sample_name = "AdventureWorksLT"

  tags = {
    deployment_id = random_id.sample.hex
  }
}