output "cloudflare_token" {
  value       = cloudflare_account_token.this.value
  description = "The Cloudflare API token ID with read/write access to your Cloudflare pages."
  sensitive   = true
}

output "cloudflare_subdomain" {
  value       = cloudflare_pages_project.this.subdomain
  description = "The subdomain of the Cloudflare Pages project."
}
