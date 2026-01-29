#!/usr/bin/env python3
"""
Feishu Block Factory - Create formatted content blocks for Feishu documents

This script provides helper functions to create various types of content blocks
for Feishu documents, including text, code, headings, lists, images, tables, etc.

Usage:
    from feishu_blocks import BlockFactory

    factory = BlockFactory()
    blocks = [
        factory.heading1("Title"),
        factory.text("This is a paragraph"),
        factory.code_python("print('Hello, World!')")
    ]
"""

from typing import List, Dict, Any, Optional


class BlockFactory:
    """Factory for creating Feishu content blocks"""

    # Available colors
    COLORS = ["gray", "brown", "orange", "yellow", "green", "blue", "purple"]

    # Supported code languages
    CODE_LANGUAGES = [
        "python", "javascript", "java", "c", "cpp", "go", "rust",
        "typescript", "php", "ruby", "swift", "kotlin", "scala",
        "csharp", "fsharp", "vb", "html", "css", "sql", "bash",
        "shell", "powershell", "json", "yaml", "xml", "markdown",
        "latex", "r", "matlab", "perl", "lua", "dart", "elixir",
        "haskell", "julia", "ocaml", "scheme", "clojure", "groovy"
    ]

    @staticmethod
    def _text_element(
        content: str,
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
        strikethrough: bool = False,
        inline_code: bool = False,
        text_color: Optional[str] = None,
        background: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a text run element"""
        element = {"text_run": {"content": content}}

        styles = {}
        if bold:
            styles["bold"] = True
        if italic:
            styles["italic"] = True
        if underline:
            styles["underline"] = True
        if strikethrough:
            styles["strikethrough"] = True
        if inline_code:
            styles["inline_code"] = True
        if text_color:
            if text_color not in BlockFactory.COLORS:
                raise ValueError(f"Invalid color. Must be one of: {BlockFactory.COLORS}")
            styles["text_color"] = text_color
        if background:
            if background not in BlockFactory.COLORS:
                raise ValueError(f"Invalid color. Must be one of: {BlockFactory.COLORS}")
            styles["background"] = background

        if styles:
            element["text_run"]["text_element_style"] = styles

        return element

    @staticmethod
    def text(
        content: str,
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
        strikethrough: bool = False,
        inline_code: bool = False,
        text_color: Optional[str] = None,
        background: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a text block"""
        return {
            "block_type": "text",
            "text": {
                "elements": [
                    BlockFactory._text_element(
                        content, bold, italic, underline,
                        strikethrough, inline_code, text_color, background
                    )
                ]
            }
        }

    @staticmethod
    def text_multi(elements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a text block with multiple styled elements"""
        return {
            "block_type": "text",
            "text": {
                "elements": elements
            }
        }

    @staticmethod
    def heading(
        content: str,
        level: int = 1,
        bold: bool = True,
        text_color: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a heading block (level 1-9)"""
        if level < 1 or level > 9:
            raise ValueError("Heading level must be between 1 and 9")

        return {
            "block_type": "heading1",
            "heading": {
                "level": level,
                "elements": [
                    BlockFactory._text_element(content, bold=bold, text_color=text_color)
                ]
            }
        }

    @staticmethod
    def heading1(content: str, **kwargs) -> Dict[str, Any]:
        """Create a level 1 heading"""
        return BlockFactory.heading(content, 1, **kwargs)

    @staticmethod
    def heading2(content: str, **kwargs) -> Dict[str, Any]:
        """Create a level 2 heading"""
        return BlockFactory.heading(content, 2, **kwargs)

    @staticmethod
    def heading3(content: str, **kwargs) -> Dict[str, Any]:
        """Create a level 3 heading"""
        return BlockFactory.heading(content, 3, **kwargs)

    @staticmethod
    def bullet(content: str, **kwargs) -> Dict[str, Any]:
        """Create a bullet list item"""
        return {
            "block_type": "bullet",
            "bullet": {
                "elements": [
                    BlockFactory._text_element(content, **kwargs)
                ]
            }
        }

    @staticmethod
    def ordered(content: str, **kwargs) -> Dict[str, Any]:
        """Create an ordered list item"""
        return {
            "block_type": "ordered",
            "ordered": {
                "elements": [
                    BlockFactory._text_element(content, **kwargs)
                ]
            }
        }

    @staticmethod
    def code(
        content: str,
        language: str = "python"
    ) -> Dict[str, Any]:
        """Create a code block"""
        if language not in BlockFactory.CODE_LANGUAGES:
            raise ValueError(
                f"Unsupported language: {language}. "
                f"Must be one of: {', '.join(BlockFactory.CODE_LANGUAGES)}"
            )

        return {
            "block_type": "code",
            "code": {
                "language": language,
                "elements": [
                    {"text_run": {"content": content}}
                ]
            }
        }

    @staticmethod
    def code_python(content: str) -> Dict[str, Any]:
        """Create a Python code block"""
        return BlockFactory.code(content, "python")

    @staticmethod
    def code_javascript(content: str) -> Dict[str, Any]:
        """Create a JavaScript code block"""
        return BlockFactory.code(content, "javascript")

    @staticmethod
    def code_bash(content: str) -> Dict[str, Any]:
        """Create a Bash code block"""
        return BlockFactory.code(content, "bash")

    @staticmethod
    def code_sql(content: str) -> Dict[str, Any]:
        """Create a SQL code block"""
        return BlockFactory.code(content, "sql")

    @staticmethod
    def code_json(content: str) -> Dict[str, Any]:
        """Create a JSON code block"""
        return BlockFactory.code(content, "json")

    @staticmethod
    def code_yaml(content: str) -> Dict[str, Any]:
        """Create a YAML code block"""
        return BlockFactory.code(content, "yaml")

    @staticmethod
    def image(image_token: str) -> Dict[str, Any]:
        """Create an image block"""
        return {
            "block_type": "image",
            "image": {
                "token": image_token
            }
        }

    @staticmethod
    def equation(content: str) -> Dict[str, Any]:
        """Create an equation block (LaTeX)"""
        return {
            "block_type": "equation",
            "equation": {
                "elements": [
                    {"text_run": {"content": content}}
                ]
            }
        }

    @staticmethod
    def table(rows: int, columns: int) -> Dict[str, Any]:
        """Create a table structure"""
        if rows < 1 or columns < 1:
            raise ValueError("Rows and columns must be positive integers")

        return {
            "block_type": "table",
            "table": {
                "rows": rows,
                "columns": columns
            }
        }

    @staticmethod
    def table_cell(content: str, is_header: bool = False) -> Dict[str, Any]:
        """Create content for a table cell (use with update_block)"""
        block_type = "heading1" if is_header else "text"
        return {
            "block_type": block_type,
            block_type: {
                "elements": [
                    BlockFactory._text_element(content)
                ]
            }
        }

    @staticmethod
    def whiteboard() -> Dict[str, Any]:
        """Create an empty whiteboard block"""
        return {
            "block_type": "canvas",
            "canvas": {
                "elements": []
            }
        }

    @staticmethod
    def divider() -> Dict[str, Any]:
        """Create a divider/separator (using text with dashes)"""
        return BlockFactory.text("---")

    @staticmethod
    def quote(content: str) -> Dict[str, Any]:
        """Create a quote block (using styled text)"""
        return BlockFactory.text(f"> {content}", italic=True, text_color="gray")

    @staticmethod
    def link(text: str, url: str) -> Dict[str, Any]:
        """Create a link element (inline link in text)"""
        # Note: Feishu uses special format for links
        return BlockFactory.text_multi([
            BlockFactory._text_element(text, underline=True, text_color="blue")
        ])

    @staticmethod
    def mention(user_id: str) -> Dict[str, Any]:
        """Create a mention element"""
        return {
            "text_run": {
                "content": f"@{user_id}",
                "mention": {
                    "user_id": user_id,
                    "type": "user"
                }
            }
        }

    @staticmethod
    def callout(
        content: str,
        emoji: Optional[str] = None,
        background: str = "yellow"
    ) -> Dict[str, Any]:
        """Create a callout/alert block"""
        emoji_part = f"{emoji} " if emoji else ""
        return BlockFactory.text(
            f"{emoji_part}{content}",
            background=background
        )

    @staticmethod
    def todo(content: str, checked: bool = False) -> Dict[str, Any]:
        """Create a todo/checkbox item"""
        prefix = "[x] " if checked else "[ ] "
        return BlockFactory.bullet(prefix + content)

    @staticmethod
    def code_block_with_language(
        code: str,
        language: str = "python",
        caption: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Create a code block with optional caption"""
        blocks = [BlockFactory.code(code, language)]

        if caption:
            blocks.append(BlockFactory.text(caption, italic=True, text_color="gray"))

        return blocks

    @staticmethod
    def section(
        title: str,
        content_blocks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Create a section with heading and content"""
        return [BlockFactory.heading2(title)] + content_blocks

    @staticmethod
    def definition_list(
        items: Dict[str, str]
    ) -> List[Dict[str, Any]]:
        """Create a definition list (bold terms, regular definitions)"""
        blocks = []
        for term, definition in items.items():
            blocks.append(BlockFactory.text_multi([
                BlockFactory._text_element(term + ": ", bold=True),
                BlockFactory._text_element(definition)
            ]))
        return blocks

    @staticmethod
    def metadata_table(
        metadata: Dict[str, str]
    ) -> List[Dict[str, Any]]:
        """Create a metadata table (key-value pairs)"""
        blocks = [BlockFactory.heading3("Metadata")]

        for key, value in metadata.items():
            blocks.append(BlockFactory.text_multi([
                BlockFactory._text_element(key + ": ", bold=True),
                BlockFactory._text_element(str(value))
            ]))

        return blocks


# Helper functions for common patterns

def create_markdown_like_document(
    title: str,
    sections: List[tuple]
) -> List[Dict[str, Any]]:
    """
    Create a document with markdown-like structure

    Args:
        title: Document title
        sections: List of (heading_level, heading_text, content_blocks) tuples

    Returns:
        List of blocks ready for batch creation
    """
    factory = BlockFactory()
    blocks = [factory.heading1(title)]

    for level, heading, content in sections:
        if level == 1:
            blocks.append(factory.heading1(heading))
        elif level == 2:
            blocks.append(factory.heading2(heading))
        elif level == 3:
            blocks.append(factory.heading3(heading))
        else:
            blocks.append(factory.heading(heading, level))

        blocks.extend(content)

    return blocks


def create_api_endpoint_doc(
    method: str,
    path: str,
    description: str,
    parameters: Optional[Dict[str, str]] = None,
    example: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Create documentation for an API endpoint"""
    factory = BlockFactory()
    blocks = []

    # Method and path
    blocks.append(factory.heading3(f"{method.upper()} {path}"))

    # Description
    blocks.append(factory.text(description))

    # Parameters
    if parameters:
        blocks.append(factory.heading4("Parameters"))
        for param, desc in parameters.items():
            blocks.append(factory.code(param + ": " + desc, "bash"))

    # Example
    if example:
        blocks.append(factory.heading4("Example"))
        blocks.append(factory.code(example, "bash"))

    return blocks


if __name__ == "__main__":
    # Example usage
    factory = BlockFactory()

    blocks = [
        factory.heading1("My Document"),
        factory.text("This is a paragraph with ", bold=False),
        factory.text("bold text", bold=True),
        factory.text(" and ", bold=False),
        factory.text("italic text", italic=True),
        factory.heading2("Code Examples"),
        factory.code_python('print("Hello, World!")'),
        factory.heading2("List"),
        factory.bullet("First item"),
        factory.bullet("Second item"),
        factory.heading2("Table"),
        factory.table(3, 3),
        factory.heading2("Colors"),
        factory.text("Red text", text_color="red"),
        factory.text("Yellow highlight", background="yellow"),
    ]

    import json
    print(json.dumps(blocks, indent=2))
