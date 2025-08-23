# GitHub Variables Module

This Terraform module manages GitHub Actions secrets and variables for Cloudflare Pages integration. It sets up the necessary credentials and configuration variables in a GitHub repository to enable automated deployments to Cloudflare Pages.

## Features

- Creates GitHub Actions secrets for sensitive Cloudflare credentials
- Sets up GitHub Actions variables for non-sensitive configuration
- Configurable variable names for flexibility
- Automatic repository validation

## Usage

```hcl
module "github_vars" {
  source = "./modules/github_vars"

  github_repository         = "owner/repository-name"
  cloudflare_account_id     = "your-cloudflare-account-id"
  cloudflare_token          = "your-cloudflare-api-token"
  cloudflare_project_name   = "your-pages-project-name"
  
  # Optional: customize variable names
  cloudflare_account_id_var_name   = "CLOUDFLARE_ACCOUNT_ID"
  cloudflare_token_var_name        = "CLOUDFLARE_API_TOKEN"
  cloudflare_project_name_var_name = "CLOUDFLARE_PROJECT_NAME"
}
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| github_repository | GitHub repository name in the format 'owner/repo' | `string` | n/a | yes |
| cloudflare_account_id | Cloudflare account ID | `string` | n/a | yes |
| cloudflare_token | Cloudflare API token with permissions for pages | `string` | n/a | yes |
| cloudflare_project_name | Name of the Cloudflare Pages project | `string` | n/a | yes |
| cloudflare_account_id_var_name | Name of the variable for Cloudflare account ID | `string` | `"CLOUDFLARE_ACCOUNT_ID"` | no |
| cloudflare_token_var_name | Name of the variable for Cloudflare API token | `string` | `"CLOUDFLARE_API_TOKEN"` | no |
| cloudflare_project_name_var_name | Name of the variable for Cloudflare project name | `string` | `"CLOUDFLARE_PROJECT_NAME"` | no |

## Outputs

No outputs. Secrets are not preserved in the state file for security reasons.

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.0 |
| github | ~> 5.0 |
| cloudflare | ~> 4.0 |

## Resources Created

### Secrets (Sensitive)
- `CLOUDFLARE_ACCOUNT_ID` - Cloudflare account ID
- `CLOUDFLARE_API_TOKEN` - Cloudflare API token with Pages permissions

### Variables (Non-sensitive)
- `CLOUDFLARE_PROJECT_NAME` - Name of the Cloudflare Pages project
- `MAIN_REPO` - GitHub repository name for reference

## Notes

- Secrets are encrypted and not visible in the GitHub UI after creation
- Variables are visible in the GitHub UI and should not contain sensitive data
- The module validates the repository exists before creating secrets/variables
- Variable names can be customized to match your workflow requirements
