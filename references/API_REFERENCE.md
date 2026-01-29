# Feishu API Reference

Complete API endpoint reference for Feishu (Lark) integration.

## Table of Contents
1. [Authentication APIs](#authentication-apis)
2. [Document APIs](#document-apis)
3. [Block APIs](#block-apis)
4. [Wiki APIs](#wiki-apis)
5. [Drive/Folder APIs](#drivefolder-apis)
6. [Search APIs](#search-apis)
7. [Media/Image APIs](#mediaimage-apis)
8. [Whiteboard APIs](#whiteboard-apis)
9. [Common Response Format](#common-response-format)
10. [Error Codes](#error-codes)

---

## Authentication APIs

### Get Tenant Access Token

App-level authentication for server operations.

**Endpoint**: `POST /auth/v3/tenant_access_token/internal`

**Request**:
```json
{
  "app_id": "cli_xxxxxxxxx",
  "app_secret": "xxxxxxxxxxxxxxxxxxxx"
}
```

**Response**:
```json
{
  "code": 0,
  "tenant_access_token": "t-xxxxxxxxxxxxxxxx",
  "expire": 7200
}
```

**Token validity**: 2 hours (7200 seconds)

### OAuth Authorization URL

Generate URL for user authentication.

**Endpoint**: `GET /authen/v1/authorize`

**Query Parameters**:
- `app_id`: Your Feishu app ID
- `redirect_uri`: OAuth callback URL
- `scope`: Comma-separated permission scopes
- `state`: Random string for CSRF protection

**Example URL**:
```
https://open.feishu.cn/open-apis/authen/v1/authorize?app_id=cli_xxxx&redirect_uri=http://localhost:3333/callback&scope=docs:document:write&state=random123
```

### Exchange Code for User Token

**Endpoint**: `POST /authen/v1/oidc/access_token`

**Request**:
```json
{
  "grant_type": "authorization_code",
  "code": "code_from_callback",
  "redirect_uri": "http://localhost:3333/callback"
}
```

**Response**:
```json
{
  "code": 0,
  "access_token": "u-xxxxxxxxxxxxxxxx",
  "refresh_token": "r-xxxxxxxxxxxxxxxx",
  "expires_in": 7200
}
```

### Refresh User Token

**Endpoint**: `POST /authen/v1/oidc/refresh_access_token`

**Request**:
```json
{
  "grant_type": "refresh_token",
  "refresh_token": "r-xxxxxxxxxxxxxxxx"
}
```

---

## Document APIs

### Create Document

**Endpoint**: `POST /docx/v1/documents/`

**Request**:
```json
{
  "folder_token": "folder_xxxxxxxxx",  // Optional, for folder placement
  "title": "Document Title"
}
```

**Response**:
```json
{
  "code": 0,
  "data": {
    "document": {
      "document_id": "doxcnxxxxxxxxxxxxxx",
      "revision_id": 123
    }
  }
}
```

### Get Document Info

**Endpoint**: `GET /docx/v1/documents/{document_id}`

**Response**:
```json
{
  "code": 0,
  "data": {
    "document": {
      "document_id": "doxcnxxxxxxxxxxxxxx",
      "revision_id": 123,
      "title": "Document Title",
      "creator": "ou_xxxxxxxxx",
      "create_time": 1234567890,
      "update_time": 1234567890
    }
  }
}
```

### Get Document Blocks

**Endpoint**: `GET /docx/v1/documents/{document_id}/blocks/{block_id}/children`

**Query Parameters**:
- `page_size`: Number of blocks per page (max: 100, default: 20)
- `page_token`: Token for next page
- `document_revision_id`: Document revision (-1 for latest)

**Response**:
```json
{
  "code": 0,
  "data": {
    "items": [
      {
        "block_id": "doxcnxxxxxxxxxxxxxx",
        "block_type": "page",
        "parent_id": "",
        "children": [...]
      }
    ],
    "page_token": "next_page_token"
  }
}
```

---

## Block APIs

### Create Block

**Endpoint**: `POST /docx/v1/documents/{document_id}/blocks/{parent_block_id}/children`

**Request**:
```json
{
  "children": [
    {
      "block_type": "text",
      "text": {
        "elements": [
          {
            "text_run": {
              "content": "Text content",
              "text_element_style": {
                "bold": false,
                "italic": false,
                "underline": false,
                "strikethrough": false,
                "inline_code": false
              }
            }
          }
        ]
      }
    }
  ],
  "index": -1  // -1 to append, or specific position
}
```

### Batch Create Blocks

**Endpoint**: `POST /docx/v1/documents/{document_id}/blocks/batch_create`

**Request**:
```json
{
  "requests": [
    {
      "parent_block_id": "doxcnxxxxxxxxxxxxxx",
      "children": [...],
      "index": -1
    }
  ]
}
```

**Limits**: Up to 50 blocks per request

### Update Block

**Endpoint**: `PATCH /docx/v1/documents/{document_id}/blocks/{block_id}`

**Request**:
```json
{
  "block_type": "text",
  "text": {
    "elements": [
      {
        "text_run": {
          "content": "Updated content"
        }
      }
    ]
  }
}
```

### Delete Block

**Endpoint**: `DELETE /docx/v1/documents/{document_id}/blocks/{block_id}`

**Response**:
```json
{
  "code": 0
}
```

---

## Wiki APIs

### Get Wiki Spaces

**Endpoint**: `GET /wiki/v2/spaces`

**Query Parameters**:
- `page_size`: Number of spaces per page (max: 50)
- `page_token`: Token for next page

**Response**:
```json
{
  "code": 0,
  "data": {
    "items": [
      {
        "space_id": "wiki_xxxxxxxxx",
        "name": "Space Name",
        "description": "Space description"
      }
    ],
    "page_token": "next_page_token"
  }
}
```

### Get Wiki Node

**Endpoint**: `GET /wiki/v2/spaces/{space_id}/nodes/{node_token}`

**Response**:
```json
{
  "code": 0,
  "data": {
    "node": {
      "node_token": "nodexxxxxxxxx",
      "obj_type": "document",
      "obj_token": "doxcnxxxxxxxxxxxxxx",
      "title": "Node Title",
      "parent_node_token": "parentxxxxxxxx"
    }
  }
}
```

### Get Wiki Node Children

**Endpoint**: `GET /wiki/v2/spaces/{space_id}/nodes`

**Query Parameters**:
- `parent_node_token`: Parent node token (null for root)
- `page_size`: Number of nodes per page
- `page_token`: Token for next page

**Response**:
```json
{
  "code": 0,
  "data": {
    "items": [
      {
        "node_token": "nodexxxxxxxxx",
        "obj_type": "document",
        "title": "Child Page"
      }
    ]
  }
}
```

### Create Wiki Node

**Endpoint**: `POST /wiki/v2/spaces/{space_id}/nodes`

**Request**:
```json
{
  "parent_node_token": "parentxxxxxxxx",  // null for root
  "obj_type": "document",
  "title": "New Wiki Page"
}
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

---

## Drive/Folder APIs

### Get Root Folder

**Endpoint**: `GET /drive/v1/root_folder/meta`

**Response**:
```json
{
  "code": 0,
  "data": {
    "folder_token": "folder_xxxxxxxxx",
    "name": "My Library"
  }
}
```

### Get Folder Children

**Endpoint**: `GET /drive/v1/files/{folder_token}/children`

**Query Parameters**:
- `page_size`: Number of items per page
- `page_token`: Token for next page
- `type`: Filter by type ("file", "folder", "all")

**Response**:
```json
{
  "code": 0,
  "data": {
    "items": [
      {
        "token": "file_xxxxxxxxx",
        "type": "file",
        "name": "Document.docx",
        "create_time": 1234567890
      }
    ],
    "page_token": "next_page_token"
  }
}
```

### Create Folder

**Endpoint**: `POST /drive/v1/files/{parent_folder_token}/children`

**Request**:
```json
{
  "type": "folder",
  "name": "New Folder"
}
```

---

## Search APIs

### Search Documents

**Endpoint**: `POST /search/v2/message`

**Request**:
```json
{
  "query": "search keywords",
  "search_type": "document",
  "filter": {
    "document_formats": ["docx", "wiki"]
  },
  "count": 20,
  "page_token": ""
}
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

## Media/Image APIs

### Upload Image

**Endpoint**: `POST /drive/v1/medias/upload_all`

**Content-Type**: `multipart/form-data`

**Form Data**:
- `file`: Image file binary
- `file_type`: "image"
- `file_name`: Image filename

**Response**:
```json
{
  "code": 0,
  "data": {
    "file_token": "img_v2_xxxxxxxxx"
  }
}
```

### Get Image Resource

**Endpoint**: `GET /drive/v1/medias/{file_token}/download`

Returns image binary data.

---

## Whiteboard APIs

### Get Whiteboard Content

**Endpoint**: `GET /board/v1/whiteboards/{whiteboard_id}`

**Response**:
```json
{
  "code": 0,
  "data": {
    "whiteboard": {
      "whiteboard_id": "whiteboard_xxxxxxxxx",
      "elements": [
        {
          "type": "shape",
          "id": "shape_xxx",
          "text": "Shape text",
          "position": {...}
        }
      ]
    }
  }
}
```

### Create Whiteboard Elements

**Endpoint**: `POST /board/v1/whiteboards/{whiteboard_id}/elements`

**Request**:
```json
{
  "elements": [
    {
      "type": "text",
      "text": "Hello",
      "position": {"x": 100, "y": 100}
    }
  ]
}
```

---

## Common Response Format

All API responses follow this format:

```json
{
  "code": 0,           // 0 for success, non-zero for error
  "msg": "success",    // Human-readable message
  "data": {...}        // Response data (if successful)
}
```

---

## Error Codes

| Code | Message | Description |
|------|---------|-------------|
| 0 | success | Request successful |
| 99991663 | document not found | Invalid document ID or no permission |
| 99991401 | access_token expired | Token expired, refresh required |
| 99991400 | insufficient permissions | Missing required scope/permission |
| 99991668 | block not found | Invalid block ID |
| 99991402 | invalid request | Malformed request parameters |
| 99991602 | parameter invalid | Invalid parameter value |
| 429 | rate limit exceeded | Too many requests, use backoff |

### Common Error Messages

**"document has no permission to access"**
- Cause: App not added as collaborator
- Solution: Add app to document collaborators or use group permissions

**"scope check failed"**
- Cause: Missing required permission scope
- Solution: Add required scope to app permissions

**"token is expired"**
- Cause: Access token expired
- Solution: Refresh token and retry

---

## Permission Scopes

### Required Scopes by Operation

| Operation | Required Scopes |
|-----------|-----------------|
| Create document | `docs:document:write` |
| Read document | `docs:document:readonly` |
| Edit document | `docs:document:write` |
| Delete document | `docs:document:manage` |
| Access folders | `drive:drive` |
| Access Wiki | `wiki:wiki:readonly` |
| Edit Wiki | `wiki:wiki:write` |
| Search | `search:docs:read` |
| Upload images | `drive:drive:readonly` |

### Tenant vs User Scopes

**Tenant authentication** (app-level):
- `docs:document:readonly`
- `docs:document:write`
- `drive:drive:readonly`
- `wiki:wiki:readonly`
- `wiki:wiki:write`

**User authentication** (OAuth):
- All tenant scopes plus:
- `search:docs:read`
- `offline_access` (for refresh tokens)
- User-specific permissions

---

## Base URL

**Default**: `https://open.feishu.cn/open-apis`

Can be configured via environment variable:
```bash
FEISHU_BASE_URL=https://open.feishu.cn/open-apis
```

---

## Rate Limits

- **Tenant tokens**: 10,000 requests per minute
- **User tokens**: 1,000 requests per minute
- **Batch operations**: 50 blocks per request

When rate limited (HTTP 429), implement exponential backoff.

---

## Best Practices

1. **Token caching**: Cache tokens and refresh 60 seconds before expiration
2. **Batch operations**: Use `batch_create` for multiple blocks
3. **Error handling**: Always check `code` field in responses
4. **Pagination**: Handle `page_token` for large result sets
5. **Validation**: Validate document access before editing
6. **Retry logic**: Implement retry with backoff for rate limits
