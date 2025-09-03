variable "github_repository" {
  description = "GitHub repository name in the format 'owner/repo'"
  type        = string
}

variable "cloudflare_account_id" {
  description = "Cloudflare account ID"
  type        = string
}

variable "cloudflare_token" {
  description = "Cloudflare API token with permissions for pages"
  type        = string
}

variable "cloudflare_project_name" {
  description = "Name of the Cloudflare Pages project"
  type        = string
}

variable "cloudflare_account_id_var_name" {
  description = "Name of the variable for Cloudflare account ID"
  type        = string
  default     = "CLOUDFLARE_ACCOUNT_ID"
}

variable "cloudflare_token_var_name" {
  description = "Name of the variable for Cloudflare API token"
  type        = string
  default     = "CLOUDFLARE_API_TOKEN"
}

variable "cloudflare_project_name_var_name" {
  description = "Name of the variable for Cloudflare project name"
  type        = string
  default     = "CLOUDFLARE_PROJECT_NAME"
}
