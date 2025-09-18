#!/usr/bin/env python3
"""
Unit tests for install.py

This module contains comprehensive tests for the install script functions,
including argument parsing, file downloading, and file editing functionality.
"""

import unittest
import tempfile
import pathlib
import shutil
from unittest.mock import patch
import argparse

# Import the functions we want to test
from install import make_parser, download_file, install, edit_source_directory


class TestMakeParser(unittest.TestCase):
    """Test the command-line argument parser."""

    def setUp(self):
        self.parser = make_parser()

    def test_parser_creation(self):
        """Test that parser is created successfully."""
        self.assertIsInstance(self.parser, argparse.ArgumentParser)

    def test_platform_choices(self):
        """Test that platform argument accepts valid choices."""
        # Test valid platforms
        for platform in ["astro", "hugo", "jekyll"]:
            args = self.parser.parse_args([platform])
            self.assertEqual(args.platform, platform)

    def test_invalid_platform(self):
        """Test that invalid platform raises SystemExit."""
        with self.assertRaises(SystemExit):
            self.parser.parse_args(["invalid"])

    def test_default_values(self):
        """Test default values for optional arguments."""
        args = self.parser.parse_args(["hugo"])
        self.assertIsNone(args.branch)
        self.assertIsNone(args.tag)
        self.assertIsNone(args.commit)
        self.assertEqual(args.site_dir, ".")
        self.assertEqual(args.output_dir, ".github/workflows")
        self.assertEqual(args.repo, "omsf/static-site-tools")

    def test_custom_values(self):
        """Test custom values for optional arguments."""
        args = self.parser.parse_args(
            [
                "astro",
                "--tag",
                "v1.0.0",
                "--site-dir",
                "my-site",
                "--output-dir",
                "custom/workflows",
                "--repo",
                "myorg/my-repo",
            ]
        )
        self.assertEqual(args.platform, "astro")
        self.assertEqual(args.tag, "v1.0.0")
        self.assertIsNone(args.branch)
        self.assertIsNone(args.commit)
        self.assertEqual(args.site_dir, "my-site")
        self.assertEqual(args.output_dir, "custom/workflows")
        self.assertEqual(args.repo, "myorg/my-repo")

    def test_tag_argument(self):
        """Test tag argument works."""
        args = self.parser.parse_args(["hugo", "--tag", "v2.0.0"])
        self.assertEqual(args.tag, "v2.0.0")
        self.assertIsNone(args.branch)
        self.assertIsNone(args.commit)

    def test_commit_argument(self):
        """Test commit argument works."""
        args = self.parser.parse_args(["astro", "--commit", "abc123"])
        self.assertEqual(args.commit, "abc123")
        self.assertIsNone(args.branch)
        self.assertIsNone(args.tag)

    def test_branch_argument(self):
        """Test branch argument works."""
        args = self.parser.parse_args(["jekyll", "--branch", "develop"])
        self.assertEqual(args.branch, "develop")
        self.assertIsNone(args.tag)
        self.assertIsNone(args.commit)

    def test_mutually_exclusive_arguments(self):
        """Test that version arguments are mutually exclusive."""
        with self.assertRaises(SystemExit):
            self.parser.parse_args(["hugo", "--tag", "v1.0.0", "--branch", "main"])

        with self.assertRaises(SystemExit):
            self.parser.parse_args(["astro", "--commit", "abc123", "--tag", "v1.0.0"])

        with self.assertRaises(SystemExit):
            self.parser.parse_args(
                ["jekyll", "--branch", "develop", "--commit", "abc123"]
            )

    def test_custom_repo(self):
        """Test custom repository argument."""
        args = self.parser.parse_args(["jekyll", "--repo", "custom/repository"])
        self.assertEqual(args.repo, "custom/repository")


class TestDownloadFile(unittest.TestCase):
    """Test the file download functionality."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.temp_dir)

    @patch("install.urllib.request.urlretrieve")
    @patch("install.print")
    def test_download_file_success(self, mock_print, mock_urlretrieve):
        """Test successful file download."""
        url = "https://example.com/file.yaml"
        destination = pathlib.Path(self.temp_dir) / "test.yaml"

        download_file(url, destination)

        # Check that urlretrieve was called with correct arguments
        mock_urlretrieve.assert_called_once_with(url, destination)

        # Check that appropriate messages were printed
        mock_print.assert_any_call(f"Downloading {url} to {destination}...")
        mock_print.assert_any_call("Download complete.")

    @patch("install.urllib.request.urlretrieve")
    def test_download_file_creates_directory(self, mock_urlretrieve):
        """Test that download_file creates parent directories."""
        url = "https://example.com/file.yaml"
        nested_path = pathlib.Path(self.temp_dir) / "nested" / "dir" / "test.yaml"

        download_file(url, nested_path)

        # Check that parent directory was created
        self.assertTrue(nested_path.parent.exists())
        mock_urlretrieve.assert_called_once_with(url, nested_path)


class TestEditSourceDirectory(unittest.TestCase):
    """Test the file editing functionality."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.temp_dir)

    def test_edit_source_directory_hugo(self):
        """Test editing Hugo workflow file."""
        content = """name: Build Hugo site from PR

env:
  HUGO_SOURCE_DIR: "example-hugo"
  HUGO_BASE_URL: ""
  HUGO_OUTPUT_DIR: "public"
"""
        expected = """name: Build Hugo site from PR

env:
  HUGO_SOURCE_DIR: "my-hugo-site"
  HUGO_BASE_URL: ""
  HUGO_OUTPUT_DIR: "public"
"""

        file_path = pathlib.Path(self.temp_dir) / "test.yaml"
        with open(file_path, "w") as f:
            f.write(content)

        with patch("install.print") as mock_print:
            edit_source_directory(file_path, "hugo", "my-hugo-site")

        with open(file_path, "r") as f:
            result = f.read()

        self.assertEqual(result, expected)
        mock_print.assert_called_once_with(
            f'Updated {file_path}: replaced "example-hugo" with "my-hugo-site"'
        )

    def test_edit_source_directory_astro(self):
        """Test editing Astro workflow file."""
        content = """name: Build Astro site from PR

env:
  ASTRO_SOURCE_DIR: "example-astro"
  ASTRO_BASE_URL: ""
"""
        expected = """name: Build Astro site from PR

env:
  ASTRO_SOURCE_DIR: "my-astro-app"
  ASTRO_BASE_URL: ""
"""

        file_path = pathlib.Path(self.temp_dir) / "test.yaml"
        with open(file_path, "w") as f:
            f.write(content)

        edit_source_directory(file_path, "astro", "my-astro-app")

        with open(file_path, "r") as f:
            result = f.read()

        self.assertEqual(result, expected)

    def test_edit_source_directory_jekyll(self):
        """Test editing Jekyll workflow file."""
        content = """name: Build Jekyll site from PR

env:
  JEKYLL_SOURCE_DIR: "example-jekyll"
  JEKYLL_BASE_URL: ""
"""
        expected = """name: Build Jekyll site from PR

env:
  JEKYLL_SOURCE_DIR: "docs"
  JEKYLL_BASE_URL: ""
"""

        file_path = pathlib.Path(self.temp_dir) / "test.yaml"
        with open(file_path, "w") as f:
            f.write(content)

        edit_source_directory(file_path, "jekyll", "docs")

        with open(file_path, "r") as f:
            result = f.read()

        self.assertEqual(result, expected)

    def test_edit_source_directory_no_match(self):
        """Test editing file with no matching pattern."""
        content = """name: Some other workflow

env:
  OTHER_DIR: "something"
"""

        file_path = pathlib.Path(self.temp_dir) / "test.yaml"
        with open(file_path, "w") as f:
            f.write(content)

        original_content = content
        edit_source_directory(file_path, "hugo", "my-site")

        with open(file_path, "r") as f:
            result = f.read()

        # Content should remain unchanged
        self.assertEqual(result, original_content)

    def test_edit_source_directory_multiple_occurrences(self):
        """Test editing file with multiple occurrences of the pattern."""
        content = """name: Test workflow

env:
  HUGO_SOURCE_DIR: "example-hugo"

jobs:
  test:
    steps:
      - name: Test with "example-hugo" directory
        run: echo "example-hugo"
"""
        expected = """name: Test workflow

env:
  HUGO_SOURCE_DIR: "my-site"

jobs:
  test:
    steps:
      - name: Test with "my-site" directory
        run: echo "my-site"
"""

        file_path = pathlib.Path(self.temp_dir) / "test.yaml"
        with open(file_path, "w") as f:
            f.write(content)

        edit_source_directory(file_path, "hugo", "my-site")

        with open(file_path, "r") as f:
            result = f.read()

        self.assertEqual(result, expected)


class TestInstall(unittest.TestCase):
    """Test the main install function."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.temp_dir)

    @patch("install.edit_source_directory")
    @patch("install.download_file")
    def test_install_default_parameters(self, mock_download, mock_edit):
        """Test install function with default parameters."""
        install("hugo", "branch", "main")

        # Check that download_file was called for each expected file
        expected_files = [
            "build-pr.yaml",
            "build-push.yaml",
            "cleanup-cloudflare.yaml",
            "prod-cloudflare.yaml",
            "stage-cloudflare.yaml",
        ]

        self.assertEqual(mock_download.call_count, len(expected_files))
        self.assertEqual(mock_edit.call_count, len(expected_files))

        # Check URLs and destinations
        for i, file in enumerate(expected_files):
            expected_url = f"https://raw.githubusercontent.com/omsf/static-site-tools/refs/heads/main/.github/workflows/example-hugo-{file}"
            expected_dest = pathlib.Path(".github/workflows") / file

            args, _ = mock_download.call_args_list[i]
            self.assertEqual(args[0], expected_url)
            self.assertEqual(args[1], expected_dest)

    @patch("install.edit_source_directory")
    @patch("install.download_file")
    def test_install_custom_parameters(self, mock_download, mock_edit):
        """Test install function with custom parameters."""
        install("astro", "tag", "v1.0.0", "custom/workflows", "my-astro-site")

        expected_files = [
            "build-pr.yaml",
            "build-push.yaml",
            "cleanup-cloudflare.yaml",
            "prod-cloudflare.yaml",
            "stage-cloudflare.yaml",
        ]

        # Check that files are downloaded to custom directory
        for i, file in enumerate(expected_files):
            expected_url = f"https://raw.githubusercontent.com/omsf/static-site-tools/refs/tags/v1.0.0/.github/workflows/example-astro-{file}"
            expected_dest = pathlib.Path("custom/workflows") / file

            download_args, _ = mock_download.call_args_list[i]
            self.assertEqual(download_args[0], expected_url)
            self.assertEqual(download_args[1], expected_dest)

            edit_args, _ = mock_edit.call_args_list[i]
            self.assertEqual(edit_args[0], expected_dest)
            self.assertEqual(edit_args[1], "astro")
            self.assertEqual(edit_args[2], "my-astro-site")

    @patch("install.edit_source_directory")
    @patch("install.download_file")
    def test_install_custom_repo(self, mock_download, mock_edit):
        """Test install function with custom repository."""
        install(
            "hugo", "branch", "main", ".github/workflows", ".", "myorg/my-static-tools"
        )

        expected_files = [
            "build-pr.yaml",
            "build-push.yaml",
            "cleanup-cloudflare.yaml",
            "prod-cloudflare.yaml",
            "stage-cloudflare.yaml",
        ]

        # Check that files are downloaded from custom repository
        for i, file in enumerate(expected_files):
            expected_url = f"https://raw.githubusercontent.com/myorg/my-static-tools/refs/heads/main/.github/workflows/example-hugo-{file}"
            expected_dest = pathlib.Path(".github/workflows") / file

            download_args, _ = mock_download.call_args_list[i]
            self.assertEqual(download_args[0], expected_url)
            self.assertEqual(download_args[1], expected_dest)

    @patch("install.edit_source_directory")
    @patch("install.download_file")
    def test_install_tag_version(self, mock_download, mock_edit):
        """Test install function with tag version."""
        install("jekyll", "tag", "v2.1.0")

        # Check that URL uses tags path for tag version
        expected_url = "https://raw.githubusercontent.com/omsf/static-site-tools/refs/tags/v2.1.0/.github/workflows/example-jekyll-build-pr.yaml"

        first_call_args, _ = mock_download.call_args_list[0]
        first_call_url = first_call_args[0]
        self.assertEqual(first_call_url, expected_url)

    @patch("install.edit_source_directory")
    @patch("install.download_file")
    def test_install_branch_version(self, mock_download, mock_edit):
        """Test install function with branch version."""
        install("hugo", "branch", "main")

        # Check that URL uses heads/main path for branch version
        expected_url = "https://raw.githubusercontent.com/omsf/static-site-tools/refs/heads/main/.github/workflows/example-hugo-build-pr.yaml"

        first_call_args, _ = mock_download.call_args_list[0]
        first_call_url = first_call_args[0]
        self.assertEqual(first_call_url, expected_url)

    @patch("install.edit_source_directory")
    @patch("install.download_file")
    def test_install_commit_version(self, mock_download, mock_edit):
        """Test install function with commit version."""
        install("astro", "commit", "abc123def456")

        # Check that URL uses commit hash directly
        expected_url = "https://raw.githubusercontent.com/omsf/static-site-tools/abc123def456/.github/workflows/example-astro-build-pr.yaml"

        first_call_args, _ = mock_download.call_args_list[0]
        first_call_url = first_call_args[0]
        self.assertEqual(first_call_url, expected_url)

    @patch("install.edit_source_directory")
    @patch("install.download_file")
    def test_install_custom_branch(self, mock_download, mock_edit):
        """Test install function with custom branch."""
        install("hugo", "branch", "develop")

        # Check that URL uses heads/develop path for custom branch
        expected_url = "https://raw.githubusercontent.com/omsf/static-site-tools/refs/heads/develop/.github/workflows/example-hugo-build-pr.yaml"

        first_call_args, _ = mock_download.call_args_list[0]
        first_call_url = first_call_args[0]
        self.assertEqual(first_call_url, expected_url)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete workflow."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.temp_dir)

    @patch("install.urllib.request.urlretrieve")
    def test_full_workflow_simulation(self, mock_urlretrieve):
        """Test the complete workflow with mocked HTTP requests."""
        # Mock file content that would be downloaded
        mock_content = """name: Build Hugo site from PR

env:
  HUGO_SOURCE_DIR: "example-hugo"
  HUGO_BASE_URL: ""
"""

        def mock_retrieve(url, destination):
            with open(destination, "w") as f:
                f.write(mock_content)

        mock_urlretrieve.side_effect = mock_retrieve

        output_dir = pathlib.Path(self.temp_dir) / "workflows"

        with patch("install.print"):
            install(
                "hugo",
                "branch",
                "main",
                str(output_dir),
                "my-hugo-site",
                "omsf/static-site-tools",
            )

        # Check that files were created and edited
        build_pr_file = output_dir / "build-pr.yaml"
        self.assertTrue(build_pr_file.exists())

        with open(build_pr_file, "r") as f:
            content = f.read()

        # Verify that the content was properly edited
        self.assertIn('HUGO_SOURCE_DIR: "my-hugo-site"', content)
        self.assertNotIn('HUGO_SOURCE_DIR: "example-hugo"', content)


if __name__ == "__main__":
    # Run the tests
    unittest.main(verbosity=2)
