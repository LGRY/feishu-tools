# Feishu Workflows - Complete Guides

This document provides detailed workflows for common Feishu document operations.

## Table of Contents
1. [Document Creation Workflow](#document-creation-workflow)
2. [Document Reading Workflow](#document-reading-workflow)
3. [Content Editing Workflow](#content-editing-workflow)
4. [Image Upload Workflow](#image-upload-workflow)
5. [Table Creation Workflow](#table-creation-workflow)
6. [Wiki Node Management Workflow](#wiki-node-management-workflow)
7. [Document Search Workflow](#document-search-workflow)
8. [Whiteboard Diagram Workflow](#whiteboard-diagram-workflow)
9. [Batch Operations Workflow](#batch-operations-workflow)
10. [Error Recovery Workflow](#error-recovery-workflow)

---

## Document Creation Workflow

### Create Document in Folder

**Use case**: Creating a new document in a specific Feishu Drive folder.

**Steps**:
1. Verify you have the `folder_token`
2. Create the document with title
3. Extract `document_id` from response
4. Use `document_id` for subsequent operations

**Request**:
```bash
curl -X POST "https://open.feishu.cn/open-apis/docx/v1/documents/" \
  -H "Authorization: Bearer $FEISHU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "folder_token": "folder_xxxxxxxxx",
    "title": "My New Document"
  }'
```

**Response**:
```json
{
  "code": 0,
  "data": {
    "document": {
      "document_id": "doxcnxxxxxxxxxxxxxx"
    }
  }
}
```

### Create Wiki Node

**Use case**: Creating a document as a node in a Wiki space.

**Steps**:
1. Identify the `space_id` of the Wiki space
2. Determine `parent_node_token` (use `null` for root level)
3. Create the node
4. Extract both `node_token` and `obj_token`

**Request**:
```bash
curl -X POST "https://open.feishu.cn/open-apis/wiki/v2/spaces/wiki_xxxxxx/nodes" \
  -H "Authorization: Bearer $FEISHU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "parent_node_token": null,
    "obj_type": "document",
    "title": "Wiki Page Title"
  }'
```

**Response**:
```json
{
  "code": 0,
  "data": {
    "node": {
      "node_token": "nodexxxxxxxxx",
      "obj_token": "doxcnxxxxxxxxxxxxxx"
    }
  }
}
```

**Important**:
- `node_token`: Use for parent-child relationships in Wiki
- `obj_token`: Use for document editing operations (same as `document_id`)

---

## Document Reading Workflow

### Get Document Info

**Use case**: Verify document exists, check permissions, get basic metadata.

**Request**:
```bash
curl -X GET "https://open.feishu.cn/open-apis/docx/v1/documents/doxcnxxxxxxxxxxxxxx" \
  -H "Authorization: Bearer $FEISHU_TOKEN"
```

**Response**:
```json
{
  "code": 0,
  "data": {
    "document": {
      "document_id": "doxcnxxxxxxxxxxxxxx",
      "revision_id": 123,
      "title": "Document Title",
      "creator": "ou_xxxxxxxxx"
    }
  }
}
```

### Get Document Blocks (Tree Structure)

**Use case**: Read the complete document structure and content.

**Steps**:
1. Start with the document root block (same as document_id)
2. Get children recursively
3. Build the complete block tree

**Request**:
```bash
curl -X GET "https://open.feishu.cn/open-apis/docx/v1/documents/doxcnxxxxxxxxxxxxxx/blocks/doxcnxxxxxxxxxxxxxx/children" \
  -H "Authorization: Bearer $FEISHU_TOKEN" \
  -G \
  --data-urlencode "page_size=100" \
  --data-urlencode "document_revision_id=-1"
```

**Response**:
```json
{
  "code": 0,
  "data": {
    "items": [
      {
        "block_id": "doxcnxxxxxxxxxxxxxx",
        "block_type": "page",
        "children": [
          {
            "block_id": "blockxxxxxxxx1",
            "block_type": "heading1",
            "heading": {
              "level": 1,
              "elements": [{"text_run": {"content": "Title"}}]
            }
          },
          {
            "block_id": "blockxxxxxxxx2",
            "block_type": "text",
            "text": {
              "elements": [{"text_run": {"content": "Content"}}]
            }
          }
        ]
      }
    ],
    "page_token": "next_page_token_if_more"
  }
}
```

**Pagination**: Use `page_token` to get subsequent pages if data exceeds page_size.

### Recursive Block Reading

For complete document content, recursively read all nested blocks:

```python
def get_all_blocks(document_id, block_id=None, token=None):
    if block_id is None:
        block_id = document_id

    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children"
    params = {"page_size": 100, "document_revision_id": -1}
    if token:
        params["page_token"] = token

    response = requests.get(url, headers=headers, params=params)
    data = response.json()["data"]

    blocks = data["items"]
    if "page_token" in data:
        blocks.extend(get_all_blocks(document_id, block_id, data["page_token"]))

    return blocks
```

---

## Content Editing Workflow

### Add Single Block

**Use case**: Add a single block at the end of a parent block.

**Request**:
```bash
curl -X POST "https://open.feishu.cn/open-apis/docx/v1/documents/doxcnxxxxxxxxxxxxxx/blocks/doxcnxxxxxxxxxxxxxx/children" \
  -H "Authorization: Bearer $FEISHU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "children": [
      {
        "block_type": "text",
        "text": {
          "elements": [
            {
              "text_run": {
                "content": "This is a new paragraph with ",
                "text_element_style": {}
              }
            },
            {
              "text_run": {
                "content": "bold text",
                "text_element_style": {
                  "bold": true
                }
              }
            }
          ]
        }
      }
    ],
    "index": -1
  }'
```

### Batch Create Blocks

**Use case**: Create multiple blocks efficiently (recommended for >50 blocks).

**Benefits**:
- Single API call for multiple blocks
- Up to 50 blocks per request
- Reduces latency by up to 90%

**Request**:
```bash
curl -X POST "https://open.feishu.cn/open-apis/docx/v1/documents/doxcnxxxxxxxxxxxxxx/blocks/batch_create" \
  -H "Authorization: Bearer $FEISHU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "requests": [
      {
        "parent_block_id": "doxcnxxxxxxxxxxxxxx",
        "children": [
          {
            "block_type": "heading1",
            "heading": {
              "level": 1,
              "elements": [{"text_run": {"content": "Section 1"}}]
            }
          },
          {
            "block_type": "text",
            "text": {
              "elements": [{"text_run": {"content": "Content for section 1"}}]
            }
          }
        ],
        "index": -1
      },
      {
        "parent_block_id": "doxcnxxxxxxxxxxxxxx",
        "children": [
          {
            "block_type": "heading1",
            "heading": {
              "level": 1,
              "elements": [{"text_run": {"content": "Section 2"}}]
            }
          }
        ],
        "index": -1
      }
    ]
  }'
```

**Auto-batching**: For creating >50 blocks, split into multiple batch_create requests automatically.

### Update Block Content

**Use case**: Modify existing block content while preserving block type.

**Request**:
```bash
curl -X PATCH "https://open.feishu.cn/open-apis/docx/v1/documents/doxcnxxxxxxxxxxxxxx/blocks/blockxxxxxxxx1" \
  -H "Authorization: Bearer $FEISHU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "block_type": "text",
    "text": {
      "elements": [
        {
          "text_run": {
            "content": "Updated content",
            "text_element_style": {
              "bold": true,
              "text_color": "blue"
            }
          }
        }
      ]
    }
  }'
```

### Delete Blocks

**Use case**: Remove one or more blocks from the document.

**Request**:
```bash
curl -X DELETE "https://open.feishu.cn/open-apis/docx/v1/documents/doxcnxxxxxxxxxxxxxx/blocks/blockxxxxxxxx1" \
  -H "Authorization: Bearer $FEISHU_TOKEN"
```

---

## Image Upload Workflow

### Upload Image

**Steps**:
1. Upload image file to get token
2. Create image block with the token

**Upload Request**:
```bash
curl -X POST "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all" \
  -H "Authorization: Bearer $FEISHU_TOKEN" \
  -F "file=@/path/to/image.png" \
  -F "file_type=image" \
  -F "file_name=screenshot.png"
```

**Response**:
```json
{
  "code": 0,
  "data": {
    "file_token": "img_v2_xxxxxxxxx"
  }
}
```

### Create Image Block

**Request**:
```bash
curl -X POST "https://open.feishu.cn/open-apis/docx/v1/documents/doxcnxxxxxxxxxxxxxx/blocks/parent_block_id/children" \
  -H "Authorization: Bearer $FEISHU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "children": [
      {
        "block_type": "image",
        "image": {
          "token": "img_v2_xxxxxxxxx"
        }
      }
    ],
    "index": -1
  }'
```

### Upload from URL

```python
def upload_image_from_url(image_url, token):
    # Download image
    response = requests.get(image_url)
    image_data = response.content

    # Upload to Feishu
    files = {
        'file': ('image.png', image_data, 'image/png')
    }
    data = {
        'file_type': 'image',
        'file_name': 'image.png'
    }
    upload_response = requests.post(
        "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all",
        headers={"Authorization": f"Bearer {token}"},
        files=files,
        data=data
    )
    return upload_response.json()['data']['file_token']
```

---

## Table Creation Workflow

### Create Table Structure

**Request**:
```bash
curl -X POST "https://open.feishu.cn/open-apis/docx/v1/documents/doxcnxxxxxxxxxxxxxx/blocks/parent_block_id/children" \
  -H "Authorization: Bearer $FEISHU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "children": [
      {
        "block_type": "table",
        "table": {
          "rows": 3,
          "columns": 4,
          "table_block_id": "table_xxxxxxxxx"
        }
      }
    ],
    "index": -1
  }'
```

### Fill Table Cells

After creating the table, fill cells by updating individual cell blocks:

```python
def fill_table_cell(document_id, table_id, row, col, content):
    cell_block_id = f"{table_id}_{row}_{col}"

    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/{cell_block_id}"
    data = {
        "block_type": "table_cell",
        "table_cell": {
            "style": {},
            "blocks": [
                {
                    "block_type": "text",
                    "text": {
                        "elements": [{"text_run": {"content": content}}]
                    }
                }
            ]
        }
    }

    return requests.patch(url, headers=headers, json=data)
```

---

## Wiki Node Management Workflow

### Get Wiki Spaces List

**Request**:
```bash
curl -X GET "https://open.feishu.cn/open-apis/wiki/v2/spaces" \
  -H "Authorization: Bearer $FEISHU_TOKEN" \
  -G \
  --data-urlencode "page_size=50"
```

### Get Wiki Node Children

**Request**:
```bash
curl -X GET "https://open.feishu.cn/open-apis/wiki/v2/spaces/wiki_xxxxxx/nodes" \
  -H "Authorization: Bearer $FEISHU_TOKEN" \
  -G \
  --data-urlencode "parent_node_token=nodexxxxxxxxx" \
  --data-urlencode "page_size=50"
```

### Create Wiki Sub-page

**Request**:
```bash
curl -X POST "https://open.feishu.cn/open-apis/wiki/v2/spaces/wiki_xxxxxx/nodes" \
  -H "Authorization: Bearer $FEISHU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "parent_node_token": "nodexxxxxxxxx",
    "obj_type": "document",
    "title": "Sub-page Title"
  }'
```

---

## Document Search Workflow

### Search Documents

**Request**:
```bash
curl -X POST "https://open.feishu.cn/open-apis/search/v2/message" \
  -H "Authorization: Bearer $FEISHU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "search keywords",
    "search_type": "document",
    "filter": {
      "document_formats": ["docx", "wiki"]
    }
  }'
```

**Response**:
```json
{
  "code": 0,
  "data": {
    "items": [
      {
        "title": "Matching Document",
        "doc_type": "document",
        "document_id": "doxcnxxxxxxxxxxxxxx",
        "url": "https://..."
      }
    ]
  }
}
```

---

## Whiteboard Diagram Workflow

### Create Whiteboard Block

**Request**:
```bash
curl -X POST "https://open.feishu.cn/open-apis/docx/v1/documents/doxcnxxxxxxxxxxxxxx/blocks/parent_block_id/children" \
  -H "Authorization: Bearer $FEISHU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "children": [
      {
        "block_type": "canvas",
        "canvas": {
          "elements": []
        }
      }
    ],
    "index": -1
  }'
```

### Extract Whiteboard ID

From the response, extract the whiteboard_id from the canvas block.

### Fill with Mermaid Diagram

```bash
curl -X POST "https://open.feishu.cn/open-apis/board/v1/whiteboards/whiteboard_xxxxxxxxx/elements" \
  -H "Authorization: Bearer $FEISHU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "elements": [
      {
        "type": "mindmap",
        "content": "mindmap\n  root[Root]\n    branch1\n    branch2"
      }
    ]
  }'
```

### Get Whiteboard Content

**Request**:
```bash
curl -X GET "https://open.feishu.cn/open-apis/board/v1/whiteboards/whiteboard_xxxxxxxxx" \
  -H "Authorization: Bearer $FEISHU_TOKEN"
```

---

## Batch Operations Workflow

### Auto-batching Strategy

When creating many blocks (>50), automatically split into batches:

```python
def batch_create_blocks(document_id, parent_id, blocks, batch_size=50):
    """Auto-batch blocks into multiple requests"""
    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/batch_create"

    for i in range(0, len(blocks), batch_size):
        batch = blocks[i:i + batch_size]
        data = {
            "requests": [
                {
                    "parent_block_id": parent_id,
                    "children": batch,
                    "index": -1
                }
            ]
        }
        response = requests.post(url, headers=headers, json=data)
        # Handle response
```

### Consecutive Position Insertion

For inserting at specific positions, use the `index` parameter:

```python
def insert_at_positions(document_id, parent_id, blocks_with_positions):
    """Insert blocks at specific positions"""
    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/batch_create"

    requests_data = []
    for block, position in blocks_with_positions:
        requests_data.append({
            "parent_block_id": parent_id,
            "children": [block],
            "index": position
        })

    data = {"requests": requests_data}
    return requests.post(url, headers=headers, json=data)
```

---

## Error Recovery Workflow

### Handle Token Expiration

**Error**: `99991401` - Token expired

**Solution**: Refresh token and retry request

```python
def call_with_refresh(url, headers, data):
    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    if result.get("code") == 99991401:
        # Refresh token
        new_token = refresh_token()
        headers["Authorization"] = f"Bearer {new_token}"
        # Retry request
        response = requests.post(url, headers=headers, json=data)

    return response.json()
```

### Handle Rate Limiting

**Error**: `429` - Too many requests

**Solution**: Exponential backoff

```python
import time

def call_with_backoff(url, headers, data, max_retries=5):
    for attempt in range(max_retries):
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 429:
            wait_time = 2 ** attempt
            time.sleep(wait_time)
            continue

        return response.json()

    raise Exception("Max retries exceeded")
```

### Handle Missing Permissions

**Error**: `99991400` - Missing required permission

**Solution**: Report missing scope to user

```python
MISSING_PERMISSIONS = {
    "docs:document": "Document access permission",
    "docs:document:readonly": "Document read-only permission",
    "drive:drive": "Drive access permission",
    "wiki:wiki:readonly": "Wiki read-only permission",
    "wiki:wiki:write": "Wiki write permission"
}

def handle_permission_error(error_msg):
    for scope, description in MISSING_PERMISSIONS.items():
        if scope in error_msg:
            return f"Missing permission: {description} (scope: {scope})"
    return error_msg
```

### Validate Document Access

Before editing, always validate:

```python
def validate_document(document_id, token):
    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}"
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})

    if response.json().get("code") == 99991663:
        raise Exception(f"No access to document: {document_id}")

    return True
```

---

## Complete Example: Create Document with Content

```python
def create_document_with_content(title, content_blocks):
    # 1. Create document
    create_url = "https://open.feishu.cn/open-apis/docx/v1/documents/"
    create_data = {"title": title}
    response = requests.post(create_url, headers=headers, json=create_data)
    document_id = response.json()["data"]["document"]["document_id"]

    # 2. Batch create content blocks
    blocks_url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/batch_create"

    # Convert content to block format
    blocks = []
    for item in content_blocks:
        if item["type"] == "heading":
            blocks.append({
                "block_type": "heading1",
                "heading": {
                    "level": 1,
                    "elements": [{"text_run": {"content": item["content"]}}]
                }
            })
        elif item["type"] == "text":
            blocks.append({
                "block_type": "text",
                "text": {
                    "elements": [{"text_run": {"content": item["content"]}}]
                }
            })

    # Batch create
    batch_data = {
        "requests": [
            {
                "parent_block_id": document_id,
                "children": blocks,
                "index": -1
            }
        ]
    }

    requests.post(blocks_url, headers=headers, json=batch_data)

    return document_id
```
