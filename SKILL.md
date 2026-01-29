---
name: feishu-tools
description: "Feishu (Lark) document and Wiki integration for creating, reading, editing, and managing documents. Use when Claude needs to create new Feishu documents in folders or Wiki spaces, read document structure and content including blocks, edit documents with rich text formatting (text, code, headings, lists, images, equations, mermaid diagrams, tables, whiteboards), upload and manage images, search documents, manage folders and Wiki nodes, extract content from whiteboards with flowcharts and mind maps. Supports both tenant (app-level) and user (OAuth) authentication."
---

# Feishu Tools

## Quick Start

**For Public Documents**: No setup required! Simply provide the URL:
- `Read the document at: https://xxx.feishu.cn/wiki/NODE_TOKEN`
- `Read the document at: https://xxx.feishu.cn/docx/DOC_ID`

**For Private Documents**: Configure credentials when prompted (see Configuration below).

---

## Authentication Setup

### Public Documents (No Configuration)

Publicly accessible Feishu documents can be read immediately without any setup. Just provide the URL and the skill will attempt to read it.

### Private Documents (Configuration Required)

For private or restricted documents, you need to configure Feishu credentials.

```bash
FEISHU_APP_ID=cli_xxxxx           # Your Feishu application ID
FEISHU_APP_SECRET=xxxxx           # Your Feishu application secret
FEISHU_AUTH_TYPE=tenant           # 'tenant' for app-level, 'user' for OAuth
```

**Tenant authentication** (default): App-level access, no user login required.
**User authentication**: OAuth flow for user-specific permissions and multi-user support.

## API Communication Pattern

All Feishu API calls follow this pattern:

1. Get access token (tenant_access_token or user_access_token)
2. Call Feishu API endpoints at `https://open.feishu.cn/open-apis`
3. Handle token refresh and caching
4. Process responses and errors

**Base headers** for all requests:
```json
{
  "Authorization": "Bearer {access_token}",
  "Content-Type": "application/json"
}
```

## Document ID Format

Feishu documents have two formats:
- **Regular documents**: `docx/{document_id}` or direct document ID
- **Wiki documents**: `wiki/{space_id}/{node_token}`

Always extract the `documentId` (also called `obj_token` for Wiki nodes) for editing operations.

## Core Workflows

### 1. Create Document

**In a folder (Feishu Drive)**:
```bash
curl -X POST "https://open.feishu.cn/open-apis/docx/v1/documents/" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "folder_token": "{folder_token}",
    "title": "Document Title"
  }'
```

**In a Wiki space**:
```bash
curl -X POST "https://open.feishu.cn/open-apis/wiki/v2/spaces/{space_id}/nodes" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "parent_node_token": "{parent_token_or_null}",
    "obj_type": "document",
    "title": "Document Title"
  }'
```

Response includes:
- `node_token`: For Wiki hierarchy (parent-child relationships)
- `obj_token`: For document editing (same as documentId)

### 2. Read Document Structure

**Get document info** (validates existence and permissions):
```bash
curl -X GET "https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}" \
  -H "Authorization: Bearer {token}"
```

**Get document blocks** (returns complete tree):
```bash
curl -X GET "https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children" \
  -H "Authorization: Bearer {token}"
```

Start with `block_id` as the document root. The response includes all blocks with their types, positions, and relationships.

### 3. Create Content Blocks

**Single block creation**:
```bash
curl -X POST "https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/{parent_block_id}/children" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "children": [
      {
        "block_type": "text",
        "text": {
          "elements": [
            {
              "text_run": {
                "content": "Hello, world!"
              }
            }
          ]
        }
      }
    ],
    "index": -1  # Append to end
  }'
```

**Batch creation** (recommended for >50 blocks):
```bash
curl -X POST "https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/batch_create" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "requests": [
      {
        "parent_block_id": "{parent_id}",
        "children": [{...block...}],
        "index": -1
      }
    ]
  }'
```

### 4. Search Documents

```bash
curl -X POST "https://open.feishu.cn/open-apis/search/v2/message" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "query": "{search_keywords}",
    "search_type": "document"
  }'
```

## Block Types and Structure

### Text Block
```json
{
  "block_type": "text",
  "text": {
    "elements": [{
      "text_run": {
        "content": "Text content",
        "text_element_style": {
          "bold": true,
          "italic": false,
          "underline": false,
          "strikethrough": false,
          "inline_code": true
        }
      }
    }]
  }
}
```

### Code Block
```json
{
  "block_type": "code",
  "code": {
    "language": "python",
    "elements": [{
      "text_run": {
        "content": "print('Hello, World!')"
      }
    }]
  }
}
```

Supported languages: python, javascript, java, c, cpp, go, rust, typescript, php, ruby, swift, kotlin, scala, csharp, html, css, sql, bash, shell, powershell, json, yaml, xml, markdown, latex, r, matlab, and 50+ more.

### Heading Block
```json
{
  "block_type": "heading",
  "heading": {
    "level": 1,
    "elements": [{
      "text_run": {
        "content": "Heading 1"
      }
    }]
  }
}
```

Levels: 1-9 (h1-h9)

### List Block
```json
{
  "block_type": "bullet",
  "bullet": {
    "elements": [{
      "text_run": {
        "content": "List item"
      }
    }]
  }
}
```

Types: `bullet` (unordered), `ordered` (numbered)

### Image Block
```json
{
  "block_type": "image",
  "image": {
    "token": "{image_token}"
  }
}
```

First upload the image to get a token:
```bash
curl -X POST "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all" \
  -H "Authorization: Bearer {token}" \
  -F "file=@/path/to/image.png" \
  -F "file_type=image"
```

### Table Block
```json
{
  "block_type": "table",
  "table": {
    "rows": 2,
    "columns": 3,
    "table_block_id": "{table_id}"
  }
}
```

After creating the table, fill cells with block updates.

### Equation Block
```json
{
  "block_type": "equation",
  "equation": {
    "elements": [{
      "text_run": {
        "content": "E = mc^2"
      }
    }]
  }
}
```

### Whiteboard Block
```json
{
  "block_type": "canvas",
  "canvas": {
    "elements": []
  }
}
```

### Mermaid Diagram
Create a whiteboard block first, then fill with Mermaid content using the whiteboard API.

## Update Block Content

```bash
curl -X PATCH "https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "block_type": "text",
    "text": {
      "elements": [{
        "text_run": {
          "content": "Updated content"
        }
      }]
    }
  }'
```

## Delete Blocks

```bash
curl -X DELETE "https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}" \
  -H "Authorization: Bearer {token}"
```

## Folder and Wiki Management

### Get Root Folder and Wiki Spaces

```bash
curl -X GET "https://open.feishu.cn/open-apis/drive/v1/root_folder/meta" \
  -H "Authorization: Bearer {token}"

curl -X GET "https://open.feishu.cn/open-apis/wiki/v2/spaces" \
  -H "Authorization: Bearer {token}"
```

### List Folder Contents

```bash
curl -X GET "https://open.feishu.cn/open-apis/drive/v1/files/{folder_token}/children" \
  -H "Authorization: Bearer {token}"
```

For Wiki spaces:
```bash
curl -X GET "https://open.feishu.cn/open-apis/wiki/v2/spaces/{space_id}/nodes" \
  -H "Authorization: Bearer {token}"
```

### Create Folder

```bash
curl -X POST "https://open.feishu.cn/open-apis/drive/v1/files/{parent_folder_token}/children" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "type": "folder",
    "name": "New Folder"
  }'
```

## Whiteboard Content

Extract whiteboard content (flowcharts, mind maps):

```bash
curl -X GET "https://open.feishu.cn/open-apis/board/v1/whiteboards/{whiteboard_id}" \
  -H "Authorization: Bearer {token}"
```

Returns structured data about shapes, connections, and their properties.

## Token Management

### Tenant Access Token

```bash
curl -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -d '{
    "app_id": "{app_id}",
    "app_secret": "{app_secret}"
  }'
```

Cache the token (valid for 2 hours).

### User Access Token (OAuth)

1. Generate OAuth URL:
```bash
https://open.feishu.cn/open-apis/authen/v1/authorize?app_id={app_id}&redirect_uri={redirect_uri}&scope={scopes}&state={state}
```

2. User authorizes and is redirected to your callback

3. Exchange code for token:
```bash
curl -X POST "https://open.feishu.cn/open-apis/authen/v1/oidc/access_token" \
  -d '{
    "grant_type": "authorization_code",
    "code": "{code_from_callback}"
  }'
```

4. Refresh token:
```bash
curl -X POST "https://open.feishu.cn/open-apis/authen/v1/oidc/refresh_access_token" \
  -d '{
    "grant_type": "refresh_token",
    "refresh_token": "{refresh_token}"
  }'
```

## Error Handling

Common errors:
- **99991663**: Invalid document ID or no permission
- **99991401**: Token expired
- **99991400**: Missing required permissions
- **99991668**: Block not found

Always check error codes and provide clear guidance to users.

## Best Practices

1. **Batch operations**: Use `batch_create` for creating multiple blocks (>50)
2. **Token caching**: Cache tokens and refresh before expiration
3. **Wiki vs Drive**: Use Wiki for hierarchical knowledge bases, Drive for file management
4. **Index placement**: Use `index: -1` to append to end, or specific index for precise positioning
5. **Document validation**: Always call `get_document_info` first to validate access
6. **Error recovery**: Handle rate limiting (429) with exponential backoff

## Content Styling

Text colors:
- `gray`, `brown`, `orange`, `yellow`, `green`, `blue`, `purple`

Background colors: Same palette

Text styles: `bold`, `italic`, `underline`, `strikethrough`, `inline_code`

Example styled text:
```json
{
  "text_element_style": {
    "bold": true,
    "text_color": "blue",
    "background": "yellow"
  }
}
```

## Advanced Features

For detailed workflows and patterns, see:
- [WORKFLOWS.md](references/WORKFLOWS.md) - Complete workflow guides
- [API_REFERENCE.md](references/API_REFERENCE.md) - Full API endpoint documentation
- [EXAMPLES.md](references/EXAMPLES.md) - Common usage examples
- [APP_SETUP_GUIDE.md](references/APP_SETUP_GUIDE.md) - Bilingual (English/中文) app configuration guide

---

## Configuration Guide (Private Documents)

### Quick Setup

Run the interactive setup script:

```bash
python scripts/setup_feishu_config.py
```

The script will prompt for your App ID and App Secret, validate them, and save the configuration.

### Manual Configuration

Create or edit `~/.claude/config.json`:

```json
{
  "feishu": {
    "app_id": "cli_your_app_id_here",
    "app_secret": "your_app_secret_here",
    "tenant_access_token": ""
  }
}
```

### Environment Variables (Alternative)

```bash
# Windows PowerShell
$env:FEISHU_APP_ID="cli_your_app_id"
$env:FEISHU_APP_SECRET="your_app_secret"

# macOS/Linux
export FEISHU_APP_ID="cli_your_app_id"
export FEISHU_APP_SECRET="your_app_secret"
```

---

## Creating a Feishu App

### Step 1: Create App

1. Visit [https://open.feishu.cn/](https://open.feishu.cn/)
2. Click **"Create App"** → **"Self-built App"**
3. Enter name (e.g., "Claude Feishu Reader")

### Step 2: Get Credentials

1. Go to **"Credentials & Basic Info"**
2. Copy **App ID** (format: `cli_xxxxx`)
3. Copy **App Secret** (click "Show" to reveal)

### Step 3: Configure Permissions

Go to **"Permissions & Scopes"** → **"Batch Import"** → **"JSON"**:

```json
{
  "scopes": {
    "tenant": [
      "docx:document",
      "wiki:wiki:readonly",
      "drive:drive:readonly"
    ]
  }
}
```

### Step 4: Enable Debug Mode

Go to **"Debug Credentials"** - your app is ready for testing!

**Note**: For personal use, Debug Mode is sufficient (no review needed).

---

## Scripts

### fetch_public_feishu.py

Read publicly accessible Feishu documents:

```bash
# Read Wiki page
python scripts/fetch_public_feishu.py --url "https://xxx.feishu.cn/wiki/NODE_TOKEN"

# Read document
python scripts/fetch_public_feishu.py --url "https://xxx.feishu.cn/docx/DOC_ID"

# Output as JSON
python scripts/fetch_public_feishu.py --url "..." --json
```

### setup_feishu_config.py

Interactive credential setup:

```bash
python scripts/setup_feishu_config.py
```

### feishu_client.py

Full-featured API client (requires configured credentials):

```bash
# Create document
python scripts/feishu_client.py create-document --title "My Document"

# Get document info
python scripts/feishu_client.py get-info --doc-id "doxcnxxxxx"

# Get document blocks
python scripts/feishu_client.py get-blocks --doc-id "doxcnxxxxx"

# Search documents
python scripts/feishu_client.py search --query "keyword"

# List Wiki spaces
python scripts/feishu_client.py wiki-spaces

# List folder contents
python scripts/feishu_client.py folder-children --folder-token "folder_xxxxx"
```

### feishu_blocks.py

Content block factory for creating formatted content:

```python
from scripts.feishu_blocks import BlockFactory

factory = BlockFactory()
blocks = [
    factory.heading1("Title"),
    factory.text("This is a paragraph"),
    factory.code_python('print("Hello, World!")'),
    factory.table(3, 3)
]
```
