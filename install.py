import urllib.request
import os
import pathlib


def make_parser():
    """Create a command-line argument parser."""
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("platform", choices=["astro", "hugo", "jekyll"])

    # Mutually exclusive group for version selection
    version_group = parser.add_mutually_exclusive_group()
    version_group.add_argument("--tag", help="Use a specific tag")
    version_group.add_argument("--commit", help="Use a specific commit hash")
    version_group.add_argument("--branch", help="Use a specific branch (default: main)")

    parser.add_argument("--site-dir", default=".")
    parser.add_argument(
        "--output-dir",
        default=".github/workflows",
        help="Directory to save workflow files",
    )
    parser.add_argument("--repo", default="omsf/static-site-tools")
    return parser


def download_file(url: str, destination: os.PathLike):
    """Download a file from a URL to a local destination."""
    print(f"Downloading {url} to {destination}...")
    destination = pathlib.Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, destination)
    print("Download complete.")


def install(
    platform: str,
    ref_type: str = "branch",
    ref_value: str = "main",
    output_dir: str = ".github/workflows",
    site_dir: str = ".",
    repo: str = "omsf/static-site-tools",
):
    workflow_dir = output_dir

    url_base = f"https://raw.githubusercontent.com/{repo}/"
    if ref_type == "tag":
        url_base += f"refs/tags/{ref_value}/"
    elif ref_type == "commit":
        url_base += f"{ref_value}/"
    else:  # branch
        url_base += f"refs/heads/{ref_value}/"
    url_base += ".github/workflows/"
    url_base += f"example-{platform}-"
    files = [
        "build-pr.yaml",
        "build-push.yaml",
        "cleanup-cloudflare.yaml",
        "prod-cloudflare.yaml",
        "stage-cloudflare.yaml",
    ]
    for file in files:
        url = url_base + file
        destination = pathlib.Path(workflow_dir) / file
        download_file(url, destination)

        # Edit the downloaded file to replace the source directory
        edit_source_directory(destination, platform, site_dir)


def edit_source_directory(file_path: os.PathLike, platform: str, site_dir: str):
    """Edit the downloaded workflow file to replace the source directory."""
    file_path = pathlib.Path(file_path)

    # Read the file content
    with open(file_path, "r") as f:
        content = f.read()

    # Replace the platform source directory
    old_value = f'"example-{platform}"'
    new_value = f'"{site_dir}"'
    original_content = content
    content = content.replace(old_value, new_value)

    # Write the modified content back
    with open(file_path, "w") as f:
        f.write(content)

    # Only print message if replacement actually occurred
    if content != original_content:
        print(f"Updated {file_path}: replaced {old_value} with {new_value}")


if __name__ == "__main__":
    parser = make_parser()
    args = parser.parse_args()
    print(f"Selected platform: {args.platform}")

    # Determine which reference type was specified
    if args.tag:
        ref_type = "tag"
        ref_value = args.tag
    elif args.commit:
        ref_type = "commit"
        ref_value = args.commit
    else:
        ref_type = "branch"
        ref_value = args.branch if args.branch else "main"

    install(
        args.platform, ref_type, ref_value, args.output_dir, args.site_dir, args.repo
    )
