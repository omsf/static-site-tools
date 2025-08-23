# Cloudflare Pages Module

This Terraform module creates a Cloudflare Pages project and generates an API token with the necessary permissions to manage the project.

## Features

- Creates a Cloudflare Pages project with configurable name and production branch
- Generates a dedicated API token with minimal required permissions for Pages management
- Supports custom compatibility dates or uses the first apply date as default
- Configures both preview and production deployment environments

## Usage

```hcl
module "cloudflare_pages" {
  source = "./modules/cloudflare_pages"

  cloudflare_token_name   = "my-pages-token"
  cloudflare_project_name = "my-awesome-site"
  cloudflare_account_id   = "your-cloudflare-account-id"
  
  # Optional: specify a custom compatibility date
  cf_compat_date = "2024-01-01"
}
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| cloudflare_token_name | Name of the Cloudflare API token | `string` | n/a | yes |
| cloudflare_project_name | Name of the Cloudflare Pages project | `string` | n/a | yes |
| cloudflare_account_id | Cloudflare account ID | `string` | n/a | yes |
| cf_compat_date | Optional override for Cloudflare compatibility date (YYYY-MM-DD). Leave empty to use first-apply date. | `string` | `""` | no |

## Outputs

| Name | Description |
|------|-------------|
| cloudflare_token | The Cloudflare API token ID with read/write access to your Cloudflare pages (sensitive) |
| cloudflare_subdomain | The subdomain of the Cloudflare Pages project |

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.0 |
| cloudflare | ~> 4.0 |
| time | ~> 0.13 |

## Notes

- The generated API token has minimal permissions (Pages Write only) for security
- The compatibility date is automatically set to prevent unwanted in-place updates
- The module uses a time resource to capture the first apply date if no custom date is provided
- The API token is marked as sensitive and will not be displayed in Terraform output