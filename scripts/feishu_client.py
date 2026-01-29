#!/usr/bin/env python3
"""
Feishu API Client - Utility script for Feishu/Lark API operations

This script provides a Python client for interacting with Feishu documents,
Wiki spaces, and folders. It handles authentication, token management, and
common API operations.

Usage:
    python feishu_client.py create-document --title "My Document"
    python feishu_client.py get-blocks --doc-id "doxcnxxxxx"
    python feishu_client.py search --query "keyword"
"""

import os
import sys
import json
import argparse
import requests
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any


class FeishuClient:
    """Client for Feishu API operations"""

    def __init__(
        self,
        app_id: Optional[str] = None,
        app_secret: Optional[str] = None,
        base_url: str = "https://open.feishu.cn/open-apis"
    ):
        self.app_id = app_id or os.getenv("FEISHU_APP_ID")
        self.app_secret = app_secret or os.getenv("FEISHU_APP_SECRET")
        self.base_url = base_url
        self._tenant_token = None
        self._token_expires_at = None

        if not self.app_id or not self.app_secret:
            raise ValueError(
                "FEISHU_APP_ID and FEISHU_APP_SECRET must be provided "
                "as arguments or environment variables"
            )

    def get_tenant_token(self) -> str:
        """Get or refresh tenant access token"""
        if self._tenant_token and self._token_expires_at:
            if datetime.now() < self._token_expires_at:
                return self._tenant_token

        # Fetch new token
        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        response = requests.post(
            url,
            json={"app_id": self.app_id, "app_secret": self.app_secret}
        )
        result = response.json()

        if result.get("code") != 0:
            raise Exception(f"Failed to get token: {result.get('msg')}")

        self._tenant_token = result["tenant_access_token"]
        # Set expiry 60 seconds before actual expiry
        expires_in = result.get("expire", 7200)
        self._token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)

        return self._tenant_token

    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Make authenticated request to Feishu API"""
        url = f"{self.base_url}{endpoint}"
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self.get_tenant_token()}"

        response = requests.request(method, url, headers=headers, **kwargs)
        result = response.json()

        # Handle token refresh
        if result.get("code") == 99991401:
            headers["Authorization"] = f"Bearer {self.get_tenant_token()}"
            response = requests.request(method, url, headers=headers, **kwargs)
            result = response.json()

        if result.get("code") != 0:
            raise Exception(f"API error {result.get('code')}: {result.get('msg')}")

        return result.get("data", {})

    # Document Operations

    def create_document(
        self,
        title: str,
        folder_token: Optional[str] = None
    ) -> str:
        """Create a new document"""
        data = {"title": title}
        if folder_token:
            data["folder_token"] = folder_token

        result = self._request("POST", "/docx/v1/documents/", json=data)
        return result["document"]["document_id"]

    def get_document_info(self, document_id: str) -> Dict[str, Any]:
        """Get document information"""
        return self._request("GET", f"/docx/v1/documents/{document_id}")

    def get_document_blocks(
        self,
        document_id: str,
        block_id: Optional[str] = None,
        page_size: int = 100
    ) -> List[Dict[str, Any]]:
        """Get all blocks from a document"""
        if block_id is None:
            block_id = document_id

        all_blocks = []
        page_token = ""

        while True:
            params = {
                "document_revision_id": -1,
                "page_size": page_size
            }
            if page_token:
                params["page_token"] = page_token

            result = self._request(
                "GET",
                f"/docx/v1/documents/{document_id}/blocks/{block_id}/children",
                params=params
            )

            all_blocks.extend(result.get("items", []))

            if "page_token" not in result:
                break

            page_token = result["page_token"]

        return all_blocks

    def search_documents(
        self,
        query: str,
        doc_type: Optional[str] = None,
        count: int = 20
    ) -> List[Dict[str, Any]]:
        """Search for documents"""
        data = {
            "query": query,
            "search_type": "document",
            "count": count
        }

        if doc_type:
            data["filter"] = {"document_formats": [doc_type]}

        result = self._request("POST", "/search/v2/message", json=data)
        return result.get("items", [])

    # Block Operations

    def create_block(
        self,
        document_id: str,
        parent_block_id: str,
        block: Dict[str, Any],
        index: int = -1
    ) -> str:
        """Create a single block"""
        data = {"children": [block], "index": index}
        result = self._request(
            "POST",
            f"/docx/v1/documents/{document_id}/blocks/{parent_block_id}/children",
            json=data
        )
        return result["blocks"][0]["block_id"]

    def batch_create_blocks(
        self,
        document_id: str,
        parent_block_id: str,
        blocks: List[Dict[str, Any]],
        index: int = -1
    ) -> List[str]:
        """Create multiple blocks in batch (up to 50)"""
        data = {"requests": [{"parent_block_id": parent_block_id, "children": blocks, "index": index}]}
        result = self._request(
            "POST",
            f"/docx/v1/documents/{document_id}/blocks/batch_create",
            json=data
        )
        return [b["block_id"] for b in result["blocks"]]

    def update_block(
        self,
        document_id: str,
        block_id: str,
        block: Dict[str, Any]
    ) -> bool:
        """Update a block"""
        self._request(
            "PATCH",
            f"/docx/v1/documents/{document_id}/blocks/{block_id}",
            json=block
        )
        return True

    def delete_block(self, document_id: str, block_id: str) -> bool:
        """Delete a block"""
        self._request(
            "DELETE",
            f"/docx/v1/documents/{document_id}/blocks/{block_id}"
        )
        return True

    # Wiki Operations

    def get_wiki_spaces(self, page_size: int = 50) -> List[Dict[str, Any]]:
        """Get all Wiki spaces"""
        all_spaces = []
        page_token = ""

        while True:
            params = {"page_size": page_size}
            if page_token:
                params["page_token"] = page_token

            result = self._request("GET", "/wiki/v2/spaces", params=params)
            all_spaces.extend(result.get("items", []))

            if "page_token" not in result:
                break

            page_token = result["page_token"]

        return all_spaces

    def create_wiki_node(
        self,
        space_id: str,
        title: str,
        parent_node_token: Optional[str] = None
    ) -> Dict[str, str]:
        """Create a new Wiki node"""
        data = {
            "obj_type": "document",
            "title": title
        }
        if parent_node_token:
            data["parent_node_token"] = parent_node_token

        result = self._request(
            "POST",
            f"/wiki/v2/spaces/{space_id}/nodes",
            json=data
        )
        node = result["node"]
        return {
            "node_token": node["node_token"],
            "document_id": node["obj_token"]
        }

    def get_wiki_children(
        self,
        space_id: str,
        parent_node_token: Optional[str] = None,
        page_size: int = 50
    ) -> List[Dict[str, Any]]:
        """Get Wiki node children"""
        params = {"page_size": page_size}
        if parent_node_token:
            params["parent_node_token"] = parent_node_token

        result = self._request("GET", f"/wiki/v2/spaces/{space_id}/nodes", params=params)
        return result.get("items", [])

    # Folder Operations

    def get_root_folder(self) -> Dict[str, Any]:
        """Get root folder info"""
        return self._request("GET", "/drive/v1/root_folder/meta")

    def get_folder_children(
        self,
        folder_token: str,
        page_size: int = 50
    ) -> List[Dict[str, Any]]:
        """Get folder children"""
        all_items = []
        page_token = ""

        while True:
            params = {"page_size": page_size}
            if page_token:
                params["page_token"] = page_token

            result = self._request(
                "GET",
                f"/drive/v1/files/{folder_token}/children",
                params=params
            )
            all_items.extend(result.get("items", []))

            if "page_token" not in result:
                break

            page_token = result["page_token"]

        return all_items

    def create_folder(
        self,
        parent_folder_token: str,
        name: str
    ) -> str:
        """Create a new folder"""
        data = {"type": "folder", "name": name}
        result = self._request(
            "POST",
            f"/drive/v1/files/{parent_folder_token}/children",
            json=data
        )
        return result["file"]["token"]

    # Image Operations

    def upload_image(
        self,
        image_path: str,
        file_name: Optional[str] = None
    ) -> str:
        """Upload an image and return its token"""
        if file_name is None:
            file_name = os.path.basename(image_path)

        with open(image_path, "rb") as f:
            files = {"file": (file_name, f, "image/png")}
            data = {"file_type": "image", "file_name": file_name}

            result = self._request(
                "POST",
                "/drive/v1/medias/upload_all",
                files=files,
                data=data
            )

        return result["file_token"]


# CLI Interface

def main():
    parser = argparse.ArgumentParser(description="Feishu API Client")
    parser.add_argument("--app-id", help="Feishu App ID")
    parser.add_argument("--app-secret", help="Feishu App Secret")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Create document
    create_doc_parser = subparsers.add_parser("create-document", help="Create a new document")
    create_doc_parser.add_argument("--title", required=True, help="Document title")
    create_doc_parser.add_argument("--folder", help="Folder token")

    # Get document info
    get_info_parser = subparsers.add_parser("get-info", help="Get document info")
    get_info_parser.add_argument("--doc-id", required=True, help="Document ID")

    # Get blocks
    get_blocks_parser = subparsers.add_parser("get-blocks", help="Get document blocks")
    get_blocks_parser.add_argument("--doc-id", required=True, help="Document ID")

    # Search
    search_parser = subparsers.add_parser("search", help="Search documents")
    search_parser.add_argument("--query", required=True, help="Search query")
    search_parser.add_argument("--type", help="Document type (document/wiki)")

    # Wiki spaces
    subparsers.add_parser("wiki-spaces", help="List Wiki spaces")

    # Wiki children
    wiki_children_parser = subparsers.add_parser("wiki-children", help="Get Wiki children")
    wiki_children_parser.add_argument("--space-id", required=True, help="Wiki space ID")
    wiki_children_parser.add_argument("--parent", help="Parent node token")

    # Folder children
    folder_children_parser = subparsers.add_parser("folder-children", help="Get folder children")
    folder_children_parser.add_argument("--folder-token", required=True, help="Folder token")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        client = FeishuClient(app_id=args.app_id, app_secret=args.app_secret)

        if args.command == "create-document":
            doc_id = client.create_document(args.title, args.folder)
            print(f"Created document: {doc_id}")

        elif args.command == "get-info":
            info = client.get_document_info(args.doc_id)
            print(json.dumps(info, indent=2))

        elif args.command == "get-blocks":
            blocks = client.get_document_blocks(args.doc_id)
            print(json.dumps(blocks, indent=2))

        elif args.command == "search":
            results = client.search_documents(args.query, args.type)
            print(f"Found {len(results)} results:")
            for item in results:
                print(f"  - {item.get('title')} ({item.get('document_id')})")

        elif args.command == "wiki-spaces":
            spaces = client.get_wiki_spaces()
            print(f"Found {len(spaces)} Wiki spaces:")
            for space in spaces:
                print(f"  - {space.get('name')} ({space.get('space_id')})")

        elif args.command == "wiki-children":
            children = client.get_wiki_children(args.space_id, args.parent)
            print(f"Found {len(children)} children:")
            for child in children:
                print(f"  - {child.get('title')} ({child.get('node_token')})")

        elif args.command == "folder-children":
            children = client.get_folder_children(args.folder_token)
            print(f"Found {len(children)} items:")
            for item in children:
                print(f"  - {item.get('name')} ({item.get('type')})")

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
