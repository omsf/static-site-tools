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

platforms=("hugo" "astro" "jekyll" "generic")
fnames=("build-pr.yaml" "build-push.yaml" "prod-cloudflare.yaml" "stage-cloudflare.yaml" "cleanup-cloudflare.yaml")

exitcode=0

for platform in "${platforms[@]}"; do
    echo "Testing platform: $platform"
    python install.py "$platform" --commit "$version" --repo "$owner/$repo" --site-dir "example-$platform" --output-dir "test_install_dir/$platform"

    for fname in "${fnames[@]}"; do
        echo "  Checking file: $fname"
        file1=".github/workflows/example-$platform-$fname"
        file2="test_install_dir/$platform/$fname"

        temp_expected=$(mktemp)
        cp "$file1" "$temp_expected"

        python - "$temp_expected" "$owner/$repo" "$version" <<'PY'
import sys
from install import update_reusable_workflow_references

update_reusable_workflow_references(sys.argv[1], sys.argv[2], sys.argv[3])
PY

        if diff -q "$temp_expected" "$file2" > /dev/null; then
            echo "    Files match expected pinned content."
        else
            echo "    Files differ from expected pinned content!"
            diff "$temp_expected" "$file2" || true
            exitcode=1
        fi

        if ! grep -q "@$version" "$file2"; then
            echo "    Missing pinned reference @$version in $file2"
            exitcode=1
        fi

        rm -f "$temp_expected"
    done
done

rm -rf test_install_dir

exit $exitcode
