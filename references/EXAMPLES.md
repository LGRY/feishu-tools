# Feishu Skill Examples

Common usage examples and patterns for Feishu integration.

## Table of Contents
1. [Basic Document Operations](#basic-document-operations)
2. [Content Creation Examples](#content-creation-examples)
3. [Rich Text Formatting](#rich-text-formatting)
4. [Code Blocks Examples](#code-blocks-examples)
5. [Image Handling](#image-handling)
6. [Table Creation](#table-creation)
7. [Wiki Integration](#wiki-integration)
8. [Search Examples](#search-examples)
9. [Batch Operations](#batch-operations)
10. [Complete Workflows](#complete-workflows)

---

## Basic Document Operations

### Example 1: Create a Simple Document

```python
import requests

# Configuration
APP_ID = "cli_xxxxxxxxx"
APP_SECRET = "xxxxxxxxxxxxxxxx"
BASE_URL = "https://open.feishu.cn/open-apis"

# Get tenant token
token_response = requests.post(
    f"{BASE_URL}/auth/v3/tenant_access_token/internal",
    json={"app_id": APP_ID, "app_secret": APP_SECRET}
)
token = token_response.json()["tenant_access_token"]

# Create document
doc_response = requests.post(
    f"{BASE_URL}/docx/v1/documents/",
    headers={"Authorization": f"Bearer {token}"},
    json={"title": "My First Document"}
)
document_id = doc_response.json()["data"]["document"]["document_id"]
print(f"Created document: {document_id}")
```

### Example 2: Read Document Content

```python
# Get document info
info_response = requests.get(
    f"{BASE_URL}/docx/v1/documents/{document_id}",
    headers={"Authorization": f"Bearer {token}"}
)
doc_info = info_response.json()["data"]["document"]
print(f"Title: {doc_info['title']}")

# Get all blocks
blocks_response = requests.get(
    f"{BASE_URL}/docx/v1/documents/{document_id}/blocks/{document_id}/children",
    headers={"Authorization": f"Bearer {token}"},
    params={"page_size": 100}
)
blocks = blocks_response.json()["data"]["items"]

for block in blocks:
    print(f"Block type: {block['block_type']}")
```

---

## Content Creation Examples

### Example 3: Create Document with Headings and Text

```python
# Create document
document_id = create_document("Project Documentation")

# Define content structure
content = [
    {"type": "heading", "level": 1, "content": "Project Overview"},
    {"type": "text", "content": "This is the introduction to the project."},
    {"type": "heading", "level": 2, "content": "Features"},
    {"type": "bullet", "content": "Feature 1: User authentication"},
    {"type": "bullet", "content": "Feature 2: Real-time updates"},
    {"type": "heading", "level": 2, "content": "Installation"},
    {"type": "text", "content": "Run: pip install my-package"},
]

# Convert to block format and create
blocks = []
for item in content:
    if item["type"] == "heading":
        blocks.append({
            "block_type": "heading1",
            "heading": {
                "level": item["level"],
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
    elif item["type"] == "bullet":
        blocks.append({
            "block_type": "bullet",
            "bullet": {
                "elements": [{"text_run": {"content": item["content"]}}]
            }
        })

# Batch create
requests.post(
    f"{BASE_URL}/docx/v1/documents/{document_id}/blocks/batch_create",
    headers={"Authorization": f"Bearer {token}"},
    json={"requests": [{"parent_block_id": document_id, "children": blocks, "index": -1}]}
)
```

### Example 4: Create Ordered List

```python
# Create numbered list
blocks = [
    {
        "block_type": "ordered",
        "ordered": {
            "elements": [{"text_run": {"content": "First item"}}]
        }
    },
    {
        "block_type": "ordered",
        "ordered": {
            "elements": [{"text_run": {"content": "Second item"}}]
        }
    },
    {
        "block_type": "ordered",
        "ordered": {
            "elements": [{"text_run": {"content": "Third item"}}]
        }
    }
]

requests.post(
    f"{BASE_URL}/docx/v1/documents/{document_id}/blocks/{document_id}/children",
    headers={"Authorization": f"Bearer {token}"},
    json={"children": blocks, "index": -1}
)
```

---

## Rich Text Formatting

### Example 5: Styled Text

```python
# Text with multiple styles
styled_block = {
    "block_type": "text",
    "text": {
        "elements": [
            {
                "text_run": {
                    "content": "This is ",
                    "text_element_style": {}
                }
            },
            {
                "text_run": {
                    "content": "bold",
                    "text_element_style": {"bold": True}
                }
            },
            {
                "text_run": {
                    "content": ", ",
                    "text_element_style": {}
                }
            },
            {
                "text_run": {
                    "content": "italic",
                    "text_element_style": {"italic": True}
                }
            },
            {
                "text_run": {
                    "content": ", and ",
                    "text_element_style": {}
                }
            },
            {
                "text_run": {
                    "content": "bold red text",
                    "text_element_style": {
                        "bold": True,
                        "text_color": "red"
                    }
                }
            }
        ]
    }
}
```

### Example 6: Colored Text

```python
# Available colors: gray, brown, orange, yellow, green, blue, purple

colored_block = {
    "block_type": "text",
    "text": {
        "elements": [
            {
                "text_run": {
                    "content": "Blue text with ",
                    "text_element_style": {"text_color": "blue"}
                }
            },
            {
                "text_run": {
                    "content": "yellow highlight",
                    "text_element_style": {
                        "text_color": "blue",
                        "background": "yellow"
                    }
                }
            }
        ]
    }
}
```

### Example 7: Inline Code

```python
inline_code_block = {
    "block_type": "text",
    "text": {
        "elements": [
            {
                "text_run": {
                    "content": "Use the "
                }
            },
            {
                "text_run": {
                    "content": "pip install",
                    "text_element_style": {"inline_code": True}
                }
            },
            {
                "text_run": {
                    "content": " command to install."
                }
            }
        ]
    }
}
```

---

## Code Blocks Examples

### Example 8: Python Code Block

```python
code_block = {
    "block_type": "code",
    "code": {
        "language": "python",
        "elements": [
            {
                "text_run": {
                    "content": """def hello_world():
    print("Hello, World!")
    return True

hello_world()"""
                }
            }
        ]
    }
}
```

### Example 9: JavaScript Code Block

```javascript
// Supported languages: python, javascript, java, c, cpp, go, rust,
// typescript, php, ruby, swift, kotlin, scala, csharp, html, css,
// sql, bash, shell, powershell, json, yaml, xml, markdown, latex, r

const codeBlock = {
    "block_type": "code",
    "code": {
        "language": "javascript",
        "elements": [{
            "text_run": {
                "content": `function greet(name) {
    return \`Hello, \${name}!\`;
}

console.log(greet("World"));`
            }
        }]
    }
};
```

### Example 10: SQL Code Block

```python
sql_block = {
    "block_type": "code",
    "code": {
        "language": "sql",
        "elements": [{
            "text_run": {
                "content": """SELECT u.name, o.order_date
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.status = 'completed'
ORDER BY o.order_date DESC;"""
            }
        }]
    }
}
```

---

## Image Handling

### Example 11: Upload and Insert Image

```python
def upload_and_insert_image(document_id, image_path):
    # Upload image
    with open(image_path, 'rb') as f:
        files = {'file': ('image.png', f, 'image/png')}
        data = {
            'file_type': 'image',
            'file_name': 'image.png'
        }
        upload_response = requests.post(
            f"{BASE_URL}/drive/v1/medias/upload_all",
            headers={"Authorization": f"Bearer {token}"},
            files=files,
            data=data
        )
    image_token = upload_response.json()["data"]["file_token"]

    # Create image block
    image_block = {
        "block_type": "image",
        "image": {
            "token": image_token
        }
    }

    requests.post(
        f"{BASE_URL}/docx/v1/documents/{document_id}/blocks/{document_id}/children",
        headers={"Authorization": f"Bearer {token}"},
        json={"children": [image_block], "index": -1}
    )

    return image_token
```

### Example 12: Insert Image from URL

```python
def insert_image_from_url(document_id, image_url):
    # Download image
    response = requests.get(image_url)
    image_data = response.content

    # Upload to Feishu
    files = {'file': ('image.png', image_data, 'image/png')}
    data = {'file_type': 'image', 'file_name': 'image.png'}

    upload_response = requests.post(
        f"{BASE_URL}/drive/v1/medias/upload_all",
        headers={"Authorization": f"Bearer {token}"},
        files=files,
        data=data
    )
    image_token = upload_response.json()["data"]["file_token"]

    # Insert into document
    # (same as Example 11)
```

---

## Table Creation

### Example 13: Create Simple Table

```python
# Create table structure
table_block = {
    "block_type": "table",
    "table": {
        "rows": 3,
        "columns": 3
    }
}

response = requests.post(
    f"{BASE_URL}/docx/v1/documents/{document_id}/blocks/{document_id}/children",
    headers={"Authorization": f"Bearer {token}"},
    json={"children": [table_block], "index": -1}
)

table_id = response.json()["data"]["blocks"][0]["block_id"]
```

### Example 14: Fill Table with Data

```python
def fill_table_cell(document_id, table_id, row, col, content, is_header=False):
    cell_block_id = f"{table_id}_{row}_{col}"

    block_type = "heading1" if is_header else "text"

    cell_data = {
        "block_type": block_type,
        block_type: {
            "elements": [{"text_run": {"content": content}}]
        }
    }

    requests.patch(
        f"{BASE_URL}/docx/v1/documents/{document_id}/blocks/{cell_block_id}",
        headers={"Authorization": f"Bearer {token}"},
        json=cell_data
    )

# Fill table
fill_table_cell(document_id, table_id, 0, 0, "Name", is_header=True)
fill_table_cell(document_id, table_id, 0, 1, "Age", is_header=True)
fill_table_cell(document_id, table_id, 0, 2, "City", is_header=True)
fill_table_cell(document_id, table_id, 1, 0, "Alice")
fill_table_cell(document_id, table_id, 1, 1, "30")
fill_table_cell(document_id, table_id, 1, 2, "New York")
```

---

## Wiki Integration

### Example 15: Create Wiki Page

```python
def create_wiki_page(space_id, parent_node_token, title):
    response = requests.post(
        f"{BASE_URL}/wiki/v2/spaces/{space_id}/nodes",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "parent_node_token": parent_node_token,  # null for root
            "obj_type": "document",
            "title": title
        }
    )

    data = response.json()["data"]["node"]
    return {
        "node_token": data["node_token"],
        "document_id": data["obj_token"]  # Use this for editing
    }

# Usage
result = create_wiki_page("wiki_xxxxxx", None, "Home Page")
document_id = result["document_id"]
```

### Example 16: List Wiki Spaces

```python
def list_wiki_spaces():
    spaces = []
    page_token = ""

    while True:
        response = requests.get(
            f"{BASE_URL}/wiki/v2/spaces",
            headers={"Authorization": f"Bearer {token}"},
            params={"page_size": 50, "page_token": page_token}
        )

        data = response.json()["data"]
        spaces.extend(data["items"])

        if "page_token" not in data:
            break

        page_token = data["page_token"]

    return spaces

spaces = list_wiki_spaces()
for space in spaces:
    print(f"Space: {space['name']} (ID: {space['space_id']})")
```

### Example 17: Get Wiki Children

```python
def get_wiki_children(space_id, parent_node_token=None):
    response = requests.get(
        f"{BASE_URL}/wiki/v2/spaces/{space_id}/nodes",
        headers={"Authorization": f"Bearer {token}"},
        params={"parent_node_token": parent_node_token, "page_size": 50}
    )

    return response.json()["data"]["items"]

# Get root level pages
children = get_wiki_children("wiki_xxxxxx")
for child in children:
    print(f"Page: {child['title']} (Node: {child['node_token']})")
```

---

## Search Examples

### Example 18: Search Documents

```python
def search_documents(query):
    response = requests.post(
        f"{BASE_URL}/search/v2/message",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "query": query,
            "search_type": "document",
            "count": 20
        }
    )

    return response.json()["data"]["items"]

results = search_documents("project documentation")
for item in results:
    print(f"Found: {item['title']} (ID: {item.get('document_id')})")
```

### Example 19: Search by Type

```python
def search_by_type(query, doc_type):
    """
    doc_type: "document" for regular docs, "wiki" for wiki pages
    """
    response = requests.post(
        f"{BASE_URL}/search/v2/message",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "query": query,
            "search_type": "document",
            "filter": {
                "document_formats": [doc_type]
            }
        }
    )

    return response.json()["data"]["items"]

# Search only wiki pages
wiki_results = search_by_type("API", "wiki")
```

---

## Batch Operations

### Example 20: Batch Create Many Blocks

```python
def batch_create_blocks(document_id, blocks, batch_size=50):
    """Efficiently create many blocks using batch API"""
    url = f"{BASE_URL}/docx/v1/documents/{document_id}/blocks/batch_create"

    for i in range(0, len(blocks), batch_size):
        batch = blocks[i:i + batch_size]
        data = {
            "requests": [
                {
                    "parent_block_id": document_id,
                    "children": batch,
                    "index": -1
                }
            ]
        }

        response = requests.post(
            url,
            headers={"Authorization": f"Bearer {token}"},
            json=data
        )

        print(f"Created batch {i//batch_size + 1}: {len(batch)} blocks")

    return True

# Create 200 text blocks
blocks = [
    {
        "block_type": "text",
        "text": {
            "elements": [{"text_run": {"content": f"Item {i}"}}]
        }
    }
    for i in range(1, 201)
]

batch_create_blocks(document_id, blocks)
```

### Example 21: Insert at Specific Positions

```python
def insert_at_positions(document_id, parent_id, blocks_with_positions):
    """
    blocks_with_positions: list of (block, position) tuples
    """
    url = f"{BASE_URL}/docx/v1/documents/{document_id}/blocks/batch_create"

    requests_data = [
        {
            "parent_block_id": parent_id,
            "children": [block],
            "index": position
        }
        for block, position in blocks_with_positions
    ]

    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {token}"},
        json={"requests": requests_data}
    )

    return response.json()

# Insert blocks at specific positions
items = [
    ({"block_type": "text", "text": {"elements": [{"text_run": {"content": "First"}}]}}, 0),
    ({"block_type": "text", "text": {"elements": [{"text_run": {"content": "Second"}}]}}, 1),
    ({"block_type": "text", "text": {"elements": [{"text_run": {"content": "Third"}}]}}, 2),
]

insert_at_positions(document_id, document_id, items)
```

---

## Complete Workflows

### Example 22: Create API Documentation

```python
def create_api_documentation():
    # Create document
    doc_response = requests.post(
        f"{BASE_URL}/docx/v1/documents/",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "API Documentation"}
    )
    document_id = doc_response.json()["data"]["document"]["document_id"]

    # Define documentation structure
    content = [
        {
            "type": "heading",
            "level": 1,
            "content": "REST API Documentation"
        },
        {
            "type": "text",
            "content": "This document describes the API endpoints for our service."
        },
        {
            "type": "heading",
            "level": 2,
            "content": "Authentication"
        },
        {
            "type": "text",
            "content": "All requests require a Bearer token in the Authorization header."
        },
        {
            "type": "heading",
            "level": 2,
            "content": "Endpoints"
        },
        {
            "type": "heading",
            "level": 3,
            "content": "GET /api/users"
        },
        {
            "type": "text",
            "content": "Returns a list of all users."
        },
        {
            "type": "code",
            "language": "bash",
            "content": "curl -H \"Authorization: Bearer $TOKEN\" https://api.example.com/users"
        },
        {
            "type": "heading",
            "level": 3,
            "content": "POST /api/users"
        },
        {
            "type": "text",
            "content": "Creates a new user."
        },
        {
            "type": "code",
            "language": "bash",
            "content": 'curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d \'{"name":"John"}\' https://api.example.com/users'
        },
    ]

    # Convert to blocks
    blocks = []
    for item in content:
        if item["type"] == "heading":
            blocks.append({
                "block_type": "heading1",
                "heading": {
                    "level": item["level"],
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
        elif item["type"] == "code":
            blocks.append({
                "block_type": "code",
                "code": {
                    "language": item["language"],
                    "elements": [{"text_run": {"content": item["content"]}}]
                }
            })

    # Batch create
    requests.post(
        f"{BASE_URL}/docx/v1/documents/{document_id}/blocks/batch_create",
        headers={"Authorization": f"Bearer {token}"},
        json={"requests": [{"parent_block_id": document_id, "children": blocks, "index": -1}]}
    )

    return document_id
```

### Example 23: Create Meeting Notes

```python
def create_meeting_notes(title, attendees, agenda_items, action_items):
    """Create a structured meeting notes document"""
    # Create document
    doc_response = requests.post(
        f"{BASE_URL}/docx/v1/documents/",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": f"Meeting Notes: {title}"}
    )
    document_id = doc_response.json()["data"]["document"]["document_id"]

    blocks = []

    # Title
    blocks.append({
        "block_type": "heading1",
        "heading": {
            "level": 1,
            "elements": [{"text_run": {"content": title}}]
        }
    })

    # Attendees
    blocks.append({
        "block_type": "heading2",
        "heading": {
            "level": 2,
            "elements": [{"text_run": {"content": "Attendees"}}]
        }
    })
    for attendee in attendees:
        blocks.append({
            "block_type": "bullet",
            "bullet": {
                "elements": [{"text_run": {"content": attendee}}]
            }
        })

    # Agenda
    blocks.append({
        "block_type": "heading2",
        "heading": {
            "level": 2,
            "elements": [{"text_run": {"content": "Agenda"}}]
        }
    })
    for i, item in enumerate(agenda_items, 1):
        blocks.append({
            "block_type": "ordered",
            "ordered": {
                "elements": [{"text_run": {"content": item}}]
            }
        })

    # Action Items
    blocks.append({
        "block_type": "heading2",
        "heading": {
            "level": 2,
            "elements": [{"text_run": {"content": "Action Items"}}]
        }
    })
    for item in action_items:
        blocks.append({
            "block_type": "bullet",
            "bullet": {
                "elements": [{"text_run": {"content": item}}]
            }
        })

    # Create all blocks
    requests.post(
        f"{BASE_URL}/docx/v1/documents/{document_id}/blocks/batch_create",
        headers={"Authorization": f"Bearer {token}"},
        json={"requests": [{"parent_block_id": document_id, "children": blocks, "index": -1}]}
    )

    return document_id

# Usage
meeting_doc = create_meeting_notes(
    title="Weekly Standup",
    attendees=["Alice", "Bob", "Charlie"],
    agenda_items=[
        "Review last week's progress",
        "Discuss blockers",
        "Plan next week's work"
    ],
    action_items=[
        "[Alice] Fix login bug",
        "[Bob] Update documentation",
        "[Charlie] Prepare demo"
    ]
)
```

### Example 24: Create Report with Table

```python
def create_report_with_table(title, data):
    """Create a report document with a data table"""
    # Create document
    doc_response = requests.post(
        f"{BASE_URL}/docx/v1/documents/",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": title}
    )
    document_id = doc_response.json()["data"]["document"]["document_id"]

    blocks = []

    # Title
    blocks.append({
        "block_type": "heading1",
        "heading": {
            "level": 1,
            "elements": [{"text_run": {"content": title}}]
        }
    })

    # Description
    blocks.append({
        "block_type": "text",
        "text": {
            "elements": [{"text_run": {"content": "This report summarizes the key metrics."}}]
        }
    })

    # Table
    blocks.append({
        "block_type": "table",
        "table": {
            "rows": len(data) + 1,  # +1 for header
            "columns": len(data[0])
        }
    })

    # Create blocks
    response = requests.post(
        f"{BASE_URL}/docx/v1/documents/{document_id}/blocks/batch_create",
        headers={"Authorization": f"Bearer {token}"},
        json={"requests": [{"parent_block_id": document_id, "children": blocks, "index": -1}]}
    )

    # Get table ID
    table_id = response.json()["data"]["blocks"][2]["block_id"]

    # Fill table
    for row_idx, row_data in enumerate(data):
        for col_idx, cell_value in enumerate(row_data.values()):
            is_header = (row_idx == 0)
            fill_table_cell(document_id, table_id, row_idx, col_idx, str(cell_value), is_header)

    return document_id

# Usage
report_data = [
    {"Metric": "Users", "Value": "1,234"},
    {"Metric": "Revenue", "Value": "$56,789"},
    {"Metric": "Growth", "Value": "+15%"}
]

report_doc = create_report_with_table("Monthly Report", report_data)
```

---

## Tips and Patterns

### Pattern 1: Markdown to Feishu Blocks

```python
def markdown_to_blocks(markdown_text):
    """Convert simple markdown to Feishu blocks"""
    lines = markdown_text.strip().split('\n')
    blocks = []

    for line in lines:
        if line.startswith('# '):
            blocks.append({
                "block_type": "heading1",
                "heading": {
                    "level": 1,
                    "elements": [{"text_run": {"content": line[2:]}}]
                }
            })
        elif line.startswith('## '):
            blocks.append({
                "block_type": "heading2",
                "heading": {
                    "level": 2,
                    "elements": [{"text_run": {"content": line[3:]}}]
                }
            })
        elif line.startswith('- '):
            blocks.append({
                "block_type": "bullet",
                "bullet": {
                    "elements": [{"text_run": {"content": line[2:]}}]
                }
            })
        elif line:
            blocks.append({
                "block_type": "text",
                "text": {
                    "elements": [{"text_run": {"content": line}}]
                }
            })

    return blocks
```

### Pattern 2: Error Handling

```python
def feishu_request(method, url, **kwargs):
    """Wrapper with automatic token refresh and error handling"""
    global token

    response = requests.request(
        method,
        url,
        headers={"Authorization": f"Bearer {token}"},
        **kwargs
    )

    result = response.json()

    # Token expired - refresh and retry
    if result.get("code") == 99991401:
        token = refresh_token()
        response = requests.request(
            method,
            url,
            headers={"Authorization": f"Bearer {token}"},
            **kwargs
        )
        result = response.json()

    # Check for errors
    if result.get("code") != 0:
        raise Exception(f"Feishu API error: {result.get('msg')}")

    return result["data"]
```

### Pattern 3: Pagination Helper

```python
def paginate_request(url, params=None):
    """Handle paginated responses automatically"""
    all_items = []
    page_token = ""

    while True:
        response_params = params.copy() if params else {}
        if page_token:
            response_params["page_token"] = page_token

        response = requests.get(
            url,
            headers={"Authorization": f"Bearer {token}"},
            params=response_params
        )

        data = response.json()["data"]
        all_items.extend(data["items"])

        if "page_token" not in data:
            break

        page_token = data["page_token"]

    return all_items
```
