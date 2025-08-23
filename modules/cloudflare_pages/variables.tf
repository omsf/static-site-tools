variable "cloudflare_token_name" {
  description = "Name of the Cloudflare API token"
  type        = string
}

variable "cloudflare_project_name" {
  description = "Name of the Cloudflare Pages project"
  type        = string
}

variable "cloudflare_account_id" {
  description = "Cloudflare account ID"
  type        = string
  sensitive   = true
}

variable "cf_compat_date" {
  description = "Optional override for Cloudflare compatibility date (YYYY-MM-DD). Leave empty to use first-apply date."
  type        = string
  default     = ""
  validation {
    condition     = var.cf_compat_date == "" || can(regex("^\\d{4}-\\d{2}-\\d{2}$", var.cf_compat_date))
    error_message = "cf_compat_date must be empty or in YYYY-MM-DD format."
  }
}

