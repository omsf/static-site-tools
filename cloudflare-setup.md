# Setting things up in Cloudflare

Here's a quick summary of what needs to be done to set up project in Cloudflare.

* [Account Setup](https://playbooks.omsf.io/cloudflare/account-setup/): Setting up Cloudflare accounts, if you don't
  already have one.
* [Project Setup](#project-setup): Setting up a project for a specific website
  on Cloudflare.

If these instructions are unclear or outdated, please [create an
issue](https://github.com/omsf/static-site-tools/issues/new) in this
repository.

## Project Setup

1. Go to the [Cloudflare dashboard](https://dash.cloudflare.com) and select the
   account that should own the project.
2. Click on "Workers and Pages" in the left sidebar.
3. Click the blue "Create" button at the top.
4. Click the "Pages" tab (instead of "Workers").
5. Click "Upload assets" under "Create using direct upload".
6. Provide a name for the project. This must be unique within all of
   Cloudflare, and the subdomain $PROJECT_NAME.pages.dev will be used.
7. Click "Create project". At this point, your project has been created, but
   has no content deployed. Deploy content using the tools in this repo!

