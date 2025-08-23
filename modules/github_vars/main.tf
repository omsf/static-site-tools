data "github_repository" "repo" {
  full_name = var.github_repository
}

# GitHub Actions secrets
resource "github_actions_secret" "cloudflare_account_id" {
  repository      = data.github_repository.repo.name
  secret_name     = var.cloudflare_account_id_var_name
  plaintext_value = var.cloudflare_account_id
}

resource "github_actions_secret" "cloudflare_token" {
  repository      = data.github_repository.repo.name
  secret_name     = var.cloudflare_token_var_name
  plaintext_value = var.cloudflare_token
}

# GitHub Actions Variables
resource "github_actions_variable" "cloudflare_project_name" {
  repository    = data.github_repository.repo.name
  variable_name = var.cloudflare_project_name_var_name
  value         = var.cloudflare_project_name
}

resource "github_actions_variable" "main_repo" {
  repository    = data.github_repository.repo.name
  variable_name = "MAIN_REPO"
  value         = var.github_repository
}
