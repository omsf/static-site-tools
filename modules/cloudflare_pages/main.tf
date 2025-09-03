
data "cloudflare_account_api_token_permission_groups_list" "groups" {
  account_id = var.cloudflare_account_id
  name       = "Pages%20Write"
}

locals {
  pages_edit = sensitive(data.cloudflare_account_api_token_permission_groups_list.groups.result[0].id)
}

# Cloudflare API token
# This is the API token that will have read/write access to your Cloudflare
# pages. It is used within the GitHub Actions. Note that this is different
# from the API token you need to deploy this Terraform configuration.
resource "cloudflare_account_token" "this" {
  name       = var.cloudflare_token_name
  account_id = var.cloudflare_account_id
  policies = [{
    effect = "allow"
    permission_groups = [{
      id = local.pages_edit
    }]
    resources = {
      "com.cloudflare.api.account.${var.cloudflare_account_id}" = "*"
    }
  }]
}

# Setting the compatibility date; without this the pages resource will
# try to edit in place every on every apply. We set it to the first time
# Terraform applies this configuration, unless the user provides a value.
resource "time_static" "cf_compat" {}

locals {
  first_apply_date = formatdate("YYYY-MM-DD", time_static.cf_compat.rfc3339)
  compat_date      = var.cf_compat_date != "" ? var.cf_compat_date : local.first_apply_date
}

# Cloudflare pages project
resource "cloudflare_pages_project" "this" {
  account_id        = var.cloudflare_account_id
  name              = var.cloudflare_project_name
  production_branch = "main"
  build_config      = {}
  deployment_configs = {
    preview = {
      compatibility_date  = local.compat_date
      compatibility_flags = []
    }
    production = {
      compatibility_date  = local.compat_date
      compatibility_flags = []
    }
  }

}
