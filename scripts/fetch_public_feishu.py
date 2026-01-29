#!/usr/bin/env python3
"""
Feishu Public Document Fetcher - Reads publicly accessible Feishu documents

This script reads Feishu documents that are publicly accessible without
requiring API credentials. It supports both Wiki pages and regular documents.

For private documents, the script will prompt you to configure credentials.

Usage:
    python fetch_public_feishu.py --url "https://xxx.feishu.cn/wiki/NODE_TOKEN"
    python fetch_public_feishu.py --url "https://xxx.feishu.cn/docx/DOC_ID"
    python fetch_public_feishu.py --doc-id "doxcnxxxxx" --type "wiki"
"""

import os
import sys
import json
import argparse
import re
import requests
from typing import Optional, Dict, Any, List
from urllib.parse import urlparse, parse_qs


class FeishuPublicFetcher:
    """Fetch publicly accessible Feishu documents"""

    def __init__(self):
        self.base_url = "https://open.feishu.cn/open-apis"

    def parse_url(self, url: str) -> Dict[str, str]:
        """Parse Feishu URL to extract document type and ID"""
        # Support multiple URL formats
        patterns = [
            r'https://\w+\.feishu\.cn/wiki/([^/?]+)',  # Wiki URL
            r'https://\w+\.feishu\.cn/docx/([^/?]+)',  # Document URL
            r'https://\w+\.larksuite\.com/wiki/([^/?]+)',  # Lark Wiki
            r'https://\w+\.larksuite\.com/docx/([^/?]+)',  # Lark Document
        ]

        for pattern in patterns:
            match = re.match(pattern, url)
            if match:
                doc_id = match.group(1)
                doc_type = "wiki" if "wiki" in url else "document"
                return {"type": doc_type, "id": doc_id}

        raise ValueError(f"Invalid Feishu URL format: {url}")

    def fetch_public_wiki(self, node_token: str) -> Dict[str, Any]:
        """Fetch public Wiki page using public API"""
        # Try public access first
        try:
            # Public Wiki access via share link
            url = f"https://open.feishu.cn/open-apis/wiki/v2/publics/get_node"
            params = {
                "node_token": node_token,
                "language": "zh_cn"
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 0:
                    return {
                        "success": True,
                        "type": "wiki",
                        "data": data.get("data", {})
                    }

                # Permission denied
                if data.get("code") in [99991404, 99991663]:
                    return {
                        "success": False,
                        "error": "permission_denied",
                        "message": "This document requires authentication. Please configure credentials."
                    }

        except Exception as e:
            return {
                "success": False,
                "error": "fetch_failed",
                "message": f"Failed to fetch: {str(e)}"
            }

        # Fallback: Try with tenant token if configured
        return self._fetch_with_credentials("wiki", node_token)

    def fetch_public_document(self, document_id: str) -> Dict[str, Any]:
        """Fetch public document using public API"""
        try:
            # Try public access
            url = f"https://open.feishu.cn/open-apis/docx/v1/publics/get_document"
            params = {
                "document_id": document_id,
                "language": "zh_cn"
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 0:
                    return {
                        "success": True,
                        "type": "document",
                        "data": data.get("data", {})
                    }

                # Permission denied
                if data.get("code") in [99991404, 99991663]:
                    return {
                        "success": False,
                        "error": "permission_denied",
                        "message": "This document requires authentication. Please configure credentials."
                    }

        except Exception as e:
            return {
                "success": False,
                "error": "fetch_failed",
                "message": f"Failed to fetch: {str(e)}"
            }

        # Fallback: Try with credentials
        return self._fetch_with_credentials("document", document_id)

    def _fetch_with_credentials(self, doc_type: str, doc_id: str) -> Dict[str, Any]:
        """Try to fetch using configured credentials"""
        config = self._load_config()

        if not config or not config.get("app_id") or not config.get("app_secret"):
            return {
                "success": False,
                "error": "no_credentials",
                "message": self._get_config_instructions()
            }

        try:
            # Get tenant token
            token = self._get_tenant_token(config["app_id"], config["app_secret"])

            # Fetch with token
            if doc_type == "wiki":
                return self._fetch_wiki_with_token(doc_id, token)
            else:
                return self._fetch_document_with_token(doc_id, token)

        except Exception as e:
            return {
                "success": False,
                "error": "auth_failed",
                "message": f"Authentication failed: {str(e)}\n\n{self._get_config_instructions()}"
            }

    def _load_config(self) -> Optional[Dict[str, str]]:
        """Load Feishu credentials from config file"""
        config_paths = [
            os.path.expanduser("~/.claude/config.json"),
            os.path.join(os.path.dirname(__file__), "../config.json")
        ]

        for config_path in config_paths:
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                        return config.get("feishu", {})
                except Exception:
                    pass

        # Check environment variables
        return {
            "app_id": os.getenv("FEISHU_APP_ID"),
            "app_secret": os.getenv("FEISHU_APP_SECRET")
        }

    def _get_tenant_token(self, app_id: str, app_secret: str) -> str:
        """Get tenant access token"""
        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        response = requests.post(url, json={"app_id": app_id, "app_secret": app_secret})
        data = response.json()

        if data.get("code") != 0:
            raise Exception(f"Failed to get token: {data.get('msg')}")

        return data["tenant_access_token"]

    def _fetch_wiki_with_token(self, node_token: str, token: str) -> Dict[str, Any]:
        """Fetch Wiki with authentication"""
        # Get space ID first (required for authenticated Wiki access)
        # For now, return error with instructions
        return {
            "success": False,
            "error": "wiki_auth_not_supported",
            "message": "Wiki access with credentials requires space ID. Please use the full feishu_client.py script."
        }

    def _fetch_document_with_token(self, document_id: str, token: str) -> Dict[str, Any]:
        """Fetch document with authentication"""
        url = f"{self.base_url}/docx/v1/documents/{document_id}"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)
        data = response.json()

        if data.get("code") != 0:
            return {
                "success": False,
                "error": "api_error",
                "message": f"API error: {data.get('msg')}"
            }

        # Get blocks
        blocks_url = f"{self.base_url}/docx/v1/documents/{document_id}/blocks/{document_id}/children"
        blocks_response = requests.get(blocks_url, headers=headers, params={"page_size": 100})
        blocks_data = blocks_response.json()

        return {
            "success": True,
            "type": "document",
            "data": {
                "document": data.get("data", {}).get("document", {}),
                "blocks": blocks_data.get("data", {}).get("items", [])
            }
        }

    def _get_config_instructions(self) -> str:
        """Get configuration instructions"""
        return """
╔═══════════════════════════════════════════════════════════════╗
║  🔐 This document requires authentication                      ║
╚═══════════════════════════════════════════════════════════════╝

To access private Feishu documents, you need to configure credentials:

📋 Quick Setup:

1. Create a Feishu app:
   • Visit: https://open.feishu.cn/
   • Create a "Self-built App"
   • Copy App ID and App Secret

2. Configure permissions:
   • Go to "Permissions & Scopes"
   • Add: docx:document (required)
   • Add: wiki:wiki:readonly (optional, for Wiki)
   • Add: drive:drive:readonly (optional, for Drive)

3. Run setup script:
   python scripts/setup_feishu_config.py

4. Enter your App ID and App Secret when prompted

📖 Detailed Guide:
   See: references/APP_SETUP_GUIDE.md (bilingual English/中文)

💡 Tip: For public documents, no setup is required!
"""

    def format_output(self, result: Dict[str, Any]) -> str:
        """Format fetch result for display"""
        if not result.get("success"):
            return result.get("message", "Unknown error")

        data = result.get("data", {})
        output = []

        if result["type"] == "wiki":
            output.append("# Wiki Page")
            if "node" in data:
                node = data["node"]
                output.append(f"Title: {node.get('title', 'N/A')}")
                output.append(f"Node Token: {node.get('node_token', 'N/A')}")

        elif result["type"] == "document":
            doc = data.get("document", {})
            output.append("# Document")
            output.append(f"Title: {doc.get('title', 'N/A')}")
            output.append(f"Document ID: {doc.get('document_id', 'N/A')}")

            # Display blocks
            blocks = data.get("blocks", [])
            output.append(f"\n## Content ({len(blocks)} blocks)")

            for block in blocks:
                block_type = block.get("block_type", "unknown")
                output.append(f"\n[{block_type}]")

                # Extract text content
                if "text" in block:
                    elements = block["text"].get("elements", [])
                    for elem in elements:
                        text_run = elem.get("text_run", {})
                        content = text_run.get("content", "")
                        style = text_run.get("text_element_style", {})
                        if style.get("bold"):
                            content = f"**{content}**"
                        if style.get("italic"):
                            content = f"*{content}*"
                        output.append(content)

                elif "heading" in block:
                    level = block["heading"].get("level", 1)
                    elements = block["heading"].get("elements", [])
                    for elem in elements:
                        content = elem.get("text_run", {}).get("content", "")
                        output.append(f"{'#' * level} {content}")

                elif "code" in block:
                    lang = block["code"].get("language", "")
                    elements = block["code"].get("elements", [])
                    for elem in elements:
                        content = elem.get("text_run", {}).get("content", "")
                        output.append(f"```{lang}")
                        output.append(content)
                        output.append("```")

        return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch publicly accessible Feishu documents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fetch Wiki page
  python fetch_public_feishu.py --url "https://xxx.feishu.cn/wiki/NODE_TOKEN"

  # Fetch document
  python fetch_public_feishu.py --url "https://xxx.feishu.cn/docx/DOC_ID"

  # With explicit document ID
  python fetch_public_feishu.py --doc-id "doxcnxxxxx" --type "document"

For private documents, the script will prompt you to configure credentials.
        """
    )

    parser.add_argument("--url", help="Feishu document URL")
    parser.add_argument("--doc-id", help="Document ID (alternative to --url)")
    parser.add_argument("--type", choices=["wiki", "document"], help="Document type")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    # Determine document type and ID
    if args.url:
        try:
            fetcher = FeishuPublicFetcher()
            parsed = fetcher.parse_url(args.url)
            doc_type = parsed["type"]
            doc_id = parsed["id"]
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    elif args.doc_id and args.type:
        doc_type = args.type
        doc_id = args.doc_id
    else:
        parser.print_help()
        return 1

    # Fetch document
    fetcher = FeishuPublicFetcher()

    if doc_type == "wiki":
        result = fetcher.fetch_public_wiki(doc_id)
    else:
        result = fetcher.fetch_public_document(doc_id)

    # Output result
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(fetcher.format_output(result))

    return 0 if result.get("success") else 1


if __name__ == "__main__":
    sys.exit(main())
