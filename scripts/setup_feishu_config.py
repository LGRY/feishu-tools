#!/usr/bin/env python3
"""
Feishu Configuration Setup Script

This script helps you configure Feishu credentials for accessing private documents.

Usage:
    python setup_feishu_config.py
"""

import os
import sys
import json
import getpass
import requests
from pathlib import Path


class FeishuConfigSetup:
    """Setup Feishu credentials"""

    def __init__(self):
        self.config_dir = Path.home() / ".claude"
        self.config_file = self.config_dir / "config.json"
        self.base_url = "https://open.feishu.cn/open-apis"

    def run(self):
        """Run the setup process"""
        print("╔═══════════════════════════════════════════════════════════════╗")
        print("║        🚀 Feishu Skill - Credential Setup                    ║")
        print("╚═══════════════════════════════════════════════════════════════╝")
        print()
        print("This script will configure Feishu credentials for accessing")
        print("private documents. Public documents don't require setup.")
        print()
        print("📖 Setup Guide: references/APP_SETUP_GUIDE.md")
        print()

        # Get credentials
        app_id = self._get_input("Enter your Feishu App ID (cli_xxxxx): ")
        app_secret = self._get_secret("Enter your Feishu App Secret: ")

        if not app_id or not app_secret:
            print("❌ Error: App ID and App Secret are required")
            return 1

        # Validate credentials
        print()
        print("🔍 Validating credentials...")
        token = self._validate_credentials(app_id, app_secret)

        if not token:
            print("❌ Error: Invalid credentials. Please check:")
            print("   • App ID format (should start with 'cli_')")
            print("   • App Secret is copied correctly")
            print("   • App has proper permissions configured")
            return 1

        print("✅ Credentials validated successfully!")

        # Save config
        print()
        print("💾 Saving configuration...")
        self._save_config(app_id, app_secret, token)

        print("✅ Configuration saved to:", self.config_file)
        print()
        print("╔═══════════════════════════════════════════════════════════════╗")
        print("║  ✅ Setup complete! You can now access private documents.     ║")
        print("╚═══════════════════════════════════════════════════════════════╝")
        print()
        print("Next steps:")
        print("  • Read documents: python scripts/feishu_client.py get-info --doc-id XXX")
        print("  • Create documents: python scripts/feishu_client.py create-document --title 'My Doc'")
        print()

        return 0

    def _get_input(self, prompt: str) -> str:
        """Get user input"""
        try:
            return input(prompt).strip()
        except EOFError:
            return ""

    def _get_secret(self, prompt: str) -> str:
        """Get secret input (hidden)"""
        try:
            return getpass.getpass(prompt)
        except EOFError:
            return ""

    def _validate_credentials(self, app_id: str, app_secret: str) -> str:
        """Validate credentials and get tenant token"""
        try:
            url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
            response = requests.post(
                url,
                json={"app_id": app_id, "app_secret": app_secret},
                timeout=10
            )

            data = response.json()

            if data.get("code") == 0:
                return data.get("tenant_access_token")
            else:
                print(f"⚠️  API returned error: {data.get('msg', 'Unknown error')}")
                return None

        except Exception as e:
            print(f"⚠️  Connection error: {str(e)}")
            return None

    def _save_config(self, app_id: str, app_secret: str, token: str):
        """Save configuration to file"""
        # Create config directory if needed
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Load existing config or create new
        config = {}
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
            except Exception:
                pass

        # Add Feishu credentials
        config["feishu"] = {
            "app_id": app_id,
            "app_secret": app_secret,
            "tenant_access_token": token
        }

        # Save config
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)

        # Set restrictive permissions (Unix-like systems)
        try:
            os.chmod(self.config_file, 0o600)
        except Exception:
            pass


def show_help():
    """Show help information"""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║  📚 Feishu App Setup - Quick Reference                        ║
╚═══════════════════════════════════════════════════════════════╝

1. Create a Feishu App:
   • Visit: https://open.feishu.cn/
   • Click "Create App" → "Self-built App"
   • Enter app name (e.g., "Claude Feishu Reader")

2. Get Credentials:
   • Go to "Credentials & Basic Info"
   • Copy App ID (format: cli_xxxxx)
   • Copy App Secret (click "Show" to reveal)

3. Configure Permissions:
   • Go to "Permissions & Scopes"
   • Click "Batch Import" → Select "JSON"
   • Paste:
   {
     "scopes": {
       "tenant": [
         "docx:document",
         "wiki:wiki:readonly",
         "drive:drive:readonly"
       ]
     }
   }
   • Click "Import"

4. Publish App (for testing):
   • Go to "Debug Credentials"
   • Your app is ready for testing!

5. Run Setup:
   • Run this script again
   • Enter your App ID and App Secret

📖 Full Guide: references/APP_SETUP_GUIDE.md (bilingual)

💡 Tips:
   • Use Debug Mode for personal use (no review needed)
   • Public documents don't require any setup
   • Keep your App Secret secure (like a password)

""")


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help", "help"]:
        show_help()
        return 0

    setup = FeishuConfigSetup()
    try:
        return setup.run()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
