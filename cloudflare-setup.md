# Setting things up in Cloudflare

Here's a quick summary of what needs to be done to set up project in Cloudflare.

* [Account Setup](#account-setup): Setting up Cloudflare accounts, if you don't
  already have one.
* [Project Setup](#project-setup): Setting up a project for a specific website
  on Cloudflare.

If these instructions are unclear or outdated, please [create an
issue](https://github.com/omsf/static-site-tools/issues/new) in this
repository.

## Account Setup

We recommend creating a project-level Cloudflare account to host Cloudflare
Pages projects, and using individual user accounts for development and debug.


1. Go to https://dash.cloudflare.com/sign-up, fill in an organizational
   email/password (i.e., not your individual email account), and do the sign-up
   process.

2. Once you're signed in as the organization, invite your work email to become
   a member:

   a. Scroll down on the left side until you see "Manage Account". Clicking on
      that will open the "Members" management.
   b. Click "Invite" to start inviting a member, and fill in your work email address.
   c. For scope, choose "All domains."
   d. For role, the main administrator should probably be "Super Administrator"
      (the other option being "Administrator", where the only difference is
      that as Administrator, you wouldn't be able to manage members.)
   e. Scroll to the bottom and click "Continue to Summary"
   f. Double check that everything is correct, then click "Invite"

3. Log out of the org's Cloudflare account. (Otherwise you'll get an error when
   you click on the invitation.)

4. You'll get the invitation in your work email. Accept the invitation. The
   first time, this will also take you through the sign-up process for the
   account associated with your work email.

5. Log out and log back into your individual account. When you log in, it
   should show you the accounts page, and you should be able to choose your own
   or the org account. We'll create the "project" for the website in the org
   account.

To add other users to the project, follow the process described in step 2. To
limit permissions, you might select "Workers Admin" or "Administrator
Read-Only", depending on what you want the user to be able to do.


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

