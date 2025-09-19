#!/bin/bash

if [ -n "$GITHUB_ACTIONS" ]; then
    # We're in GitHub Actions, use the current commit
    version=$GITHUB_SHA
else
    # We're not in GitHub Actions, get the most recently pushed commit
    version=$(gh api repos/:owner/:repo/commits --jq '.[0].sha')
fi

# figure out the owner/repo
owner=$(gh api repos/:owner/:repo --jq '.owner.login')
repo=$(gh api repos/:owner/:repo --jq '.name')

mkdir -p test_install_dir

platforms=("hugo" "astro" "jekyll")
fnames=("build-pr.yaml" "build-push.yaml" "prod-cloudflare.yaml" "stage-cloudflare.yaml" "cleanup-cloudflare.yaml")

exitcode=0

for platform in "${platforms[@]}"; do
    echo "Testing platform: $platform"
    python install.py $platform --commit $version --repo $owner/$repo --site-dir example-$platform --output-dir test_install_dir/$platform

    for fname in "${fnames[@]}"; do
        echo "  Checking file: $fname"
        file1=".github/workflows/example-$platform-$fname"
        file2="test_install_dir/$platform/$fname"

        if diff -q $file1 $file2 > /dev/null; then
            echo "    Files are identical."
        else
            echo "    Files differ!"
            exitcode=1
        fi
    done
done

rm -rf test_install_dir

exit $exitcode
