#!/usr/bin/env python3
"""
GitHub Repository Creation Script for feishu-tools

This script helps create a GitHub repository for feishu-tools.

Usage:
    python create_github_repo.py --token YOUR_GITHUB_TOKEN

Requirements:
    - PyPI: pip install requests
    - GitHub personal access token with repo scope
"""

import os
import sys
import io
import argparse
import requests
import subprocess
from pathlib import Path

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def create_github_repo(token, repo_name="feishu-tools", private=False):
    """Create GitHub repository via API"""

    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    data = {
        "name": repo_name,
        "description": "Feishu (Lark) integration skill for Claude Code - Create, read, edit and manage documents with rich text formatting support",
        "private": private,
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True,
        "auto_init": False
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        repo_data = response.json()
        return True, repo_data
    else:
        return False, response.json()


def setup_git_remote(repo_url):
    """Setup git remote and push"""

    try:
        # Add remote only if repo_url is provided
        if repo_url:
            subprocess.run(
                ["git", "remote", "add", "origin", repo_url],
                check=True,
                capture_output=True
            )

        # Push to GitHub
        subprocess.run(
            ["git", "push", "-u", "origin", "master"],
            check=True
        )

        return True, "Successfully pushed to GitHub"
    except subprocess.CalledProcessError as e:
        return False, str(e)


def main():
    parser = argparse.ArgumentParser(
        description="Create GitHub repository for feishu-tools"
    )
    parser.add_argument("--token", help="GitHub personal access token")
    parser.add_argument("--private", action="store_true", help="Create private repository")
    parser.add_argument("--setup-only", action="store_true", help="Only setup git remote (repo already exists)")

    args = parser.parse_args()

    token = args.token or os.getenv("GITHUB_TOKEN")

    if not token and not args.setup_only:
        print("=" * 60)
        print("GitHub Token Required")
        print("=" * 60)
        print()
        print("To create a GitHub repository, you need a personal access token:")
        print()
        print("1. Go to: https://github.com/settings/tokens")
        print("2. Click 'Generate new token (classic)'")
        print("3. Select 'repo' scope")
        print("4. Generate and copy the token")
        print()
        print("Then run:")
        print(f"  python {sys.argv[0]} --token YOUR_TOKEN")
        print()
        print("Or set environment variable:")
        print("  export GITHUB_TOKEN=YOUR_TOKEN  # Linux/Mac")
        print("  set GITHUB_TOKEN=YOUR_TOKEN     # Windows")
        print()
        print("=" * 60)
        print()
        print("Manual Creation Steps:")
        print("-" * 60)
        print("1. Visit: https://github.com/new")
        print("2. Repository name: feishu-tools")
        print("3. Description: Feishu (Lark) integration skill for Claude Code")
        print("4. Set as Public")
        print("5. Click 'Create repository'")
        print("6. Run this script with --setup-only to push existing code")
        print()
        return 1

    if args.setup_only:
        print("Setup mode: Configure git remote for existing repository")
        repo_url = input("Enter your repository URL (e.g., https://github.com/user/feishu-tools.git): ")
        if not repo_url:
            print("Error: Repository URL is required")
            return 1

        success, message = setup_git_remote(repo_url)
        if success:
            print(f"✓ {message}")
            return 0
        else:
            print(f"✗ Error: {message}")
            return 1

    # Create repository
    print(f"Creating GitHub repository: feishu-tools...")
    success, result = create_github_repo(token, private=args.private)

    if success:
        print(f"✓ Repository created: {result['html_url']}")
        print()
        print("Setting up git remote...")

        # Setup remote and push
        repo_url = result['clone_url']
        success, message = setup_git_remote(repo_url)

        if success:
            print(f"✓ {message}")
            print()
            print("=" * 60)
            print("Repository Ready!")
            print("=" * 60)
            print()
            print(f"URL: {result['html_url']}")
            print(f"Clone: git clone {result['clone_url']}")
            print()
            print("Contact:")
            print("  Author: 龚子 (Gong Zi)")
            print("  Email: gxj1512@163.com")
            print()
            return 0
        else:
            print(f"✗ Failed to push: {message}")
            print()
            print("Manual push command:")
            print(f"  git remote add origin {repo_url}")
            print(f"  git push -u origin master")
            return 1
    else:
        error_msg = result.get('message', 'Unknown error')
        errors = result.get('errors', [])

        # Check if repository already exists
        if 'already exists' in error_msg.lower() or 'name already exists' in error_msg.lower() or (errors and any('already_exists' in str(e).lower() or 'name already exists' in str(e).lower() for e in errors)):
            print("ℹ Repository already exists on GitHub")
            print()
            print("Attempting to push to existing repository...")

            # Try to get existing repository info
            repo_url = "https://github.com/LGRY/feishu-tools.git"

            # Check if remote exists
            try:
                result = subprocess.run(
                    ["git", "remote", "get-url", "origin"],
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    # Remote exists, just push
                    success, message = setup_git_remote(None)
                    if success:
                        print(f"✓ {message}")
                        print()
                        print("=" * 60)
                        print("Repository Updated!")
                        print("=" * 60)
                        print()
                        print(f"URL: https://github.com/LGRY/feishu-tools")
                        print()
                        print("Contact:")
                        print("  Author: 龚子 (Gong Zi)")
                        print("  Email: gxj1512@163.com")
                        print()
                        return 0
                    else:
                        print(f"✗ Failed to push: {message}")
                        return 1
                else:
                    # Remote doesn't exist, add it
                    success, message = setup_git_remote(repo_url)
                    if success:
                        print(f"✓ {message}")
                        return 0
                    else:
                        print(f"✗ Failed: {message}")
                        return 1

            except Exception as e:
                print(f"✗ Error: {str(e)}")
                print()
                print("Manual setup:")
                print(f"  git remote add origin {repo_url}")
                print(f"  git push -u origin master")
                return 1
        else:
            print(f"✗ Failed to create repository")
            print(f"Error: {error_msg}")
            if errors:
                print(f"Details: {errors}")
            return 1


if __name__ == "__main__":
    sys.exit(main())
