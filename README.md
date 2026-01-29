# Feishu Tools

[English](#english) | [中文](#中文)

---

<a name="english"></a>
## English

### Overview

**Feishu Tools** is a Claude Code skill that integrates with Feishu (Lark) documents and Wiki. It enables AI agents to create, read, edit, and manage Feishu documents with rich text formatting support.

### Features

- ✅ **Public Document Access** - Read public Feishu documents without any setup
- ✅ **Private Document Access** - Secure access with tenant or OAuth authentication
- ✅ **Document Creation** - Create documents in folders or Wiki spaces
- ✅ **Rich Content Editing** - Text, code, headings, lists, images, equations, tables, whiteboards
- ✅ **Image Management** - Upload and manage images
- ✅ **Search** - Search across documents and Wiki
- ✅ **Folder Management** - Manage Feishu Drive folders
- ✅ **Wiki Integration** - Full Wiki space and node support
- ✅ **Whiteboard Support** - Extract flowcharts and mind maps

### Installation

1. Download `feishu-tools.skill`
2. Install to your Claude Code skills directory:
   ```
   ~/.claude/skills/feishu-tools/
   ```

### Quick Start

**For Public Documents** (No setup required):
```
Read the document at: https://xxx.feishu.cn/wiki/NODE_TOKEN
```

**For Private Documents**:
1. Create a Feishu app at [open.feishu.cn](https://open.feishu.cn/)
2. Configure permissions: `docx:document`, `wiki:wiki:readonly`
3. Run setup script:
   ```bash
   python scripts/setup_feishu_config.py
   ```

### Usage Examples

```bash
# Create a document
python scripts/feishu_client.py create-document --title "My Document"

# Read document blocks
python scripts/feishu_client.py get-blocks --doc-id "doxcnxxxxx"

# Search documents
python scripts/feishu_client.py search --query "keyword"
```

### Scripts

| Script | Description |
|--------|-------------|
| `fetch_public_feishu.py` | Read public documents |
| `setup_feishu_config.py` | Interactive credential setup |
| `feishu_client.py` | Full-featured API client |
| `feishu_blocks.py` | Content block factory |

### Documentation

- [SKILL.md](SKILL.md) - Main skill documentation
- [APP_SETUP_GUIDE.md](references/APP_SETUP_GUIDE.md) - App configuration guide (bilingual)
- [WORKFLOWS.md](references/WORKFLOWS.md) - Complete workflow guides
- [API_REFERENCE.md](references/API_REFERENCE.md) - API endpoint documentation
- [EXAMPLES.md](references/EXAMPLES.md) - Usage examples

### Requirements

- Python 3.7+
- Feishu App ID and Secret (for private documents)
- Dependencies: `requests`, `python-dotenv`

### Authentication

Supports two authentication modes:

- **Tenant Authentication** (default) - App-level access
- **User Authentication** (OAuth) - User-specific permissions

### License

MIT License

### Contact

- **Author**: 龚子 (Gong Zi)
- **Email**: gxj1512@163.com

---

<a name="中文"></a>
## 中文

### 概述

**Feishu Tools** 是一个 Claude Code 技能，集成了飞书文档和知识库功能。它可以让 AI 代理创建、读取、编辑和管理飞书文档，支持富文本格式。

### 功能特性

- ✅ **公开文档访问** - 无需配置即可读取公开飞书文档
- ✅ **私有文档访问** - 支持租户或 OAuth 认证的安全访问
- ✅ **文档创建** - 在文件夹或知识库空间中创建文档
- ✅ **富内容编辑** - 支持文本、代码、标题、列表、图片、公式、表格、白板
- ✅ **图片管理** - 上传和管理图片
- ✅ **搜索** - 跨文档和知识库搜索
- ✅ **文件夹管理** - 管理飞书云空间文件夹
- ✅ **知识库集成** - 完整支持知识库空间和节点
- ✅ **白板支持** - 提取流程图和思维导图

### 安装

1. 下载 `feishu-tools.skill`
2. 安装到 Claude Code 技能目录：
   ```
   ~/.claude/skills/feishu-tools/
   ```

### 快速开始

**公开文档**（无需配置）：
```
读取文档：https://xxx.feishu.cn/wiki/NODE_TOKEN
```

**私有文档**：
1. 在 [open.feishu.cn](https://open.feishu.cn/) 创建飞书应用
2. 配置权限：`docx:document`、`wiki:wiki:readonly`
3. 运行配置脚本：
   ```bash
   python scripts/setup_feishu_config.py
   ```

### 使用示例

```bash
# 创建文档
python scripts/feishu_client.py create-document --title "我的文档"

# 读取文档块
python scripts/feishu_client.py get-blocks --doc-id "doxcnxxxxx"

# 搜索文档
python scripts/feishu_client.py search --query "关键词"
```

### 脚本说明

| 脚本 | 描述 |
|------|------|
| `fetch_public_feishu.py` | 读取公开文档 |
| `setup_feishu_config.py` | 交互式凭证配置 |
| `feishu_client.py` | 功能完整的 API 客户端 |
| `feishu_blocks.py` | 内容块工厂 |

### 文档

- [SKILL.md](SKILL.md) - 主技能文档
- [APP_SETUP_GUIDE.md](references/APP_SETUP_GUIDE.md) - 应用配置指南（双语）
- [WORKFLOWS.md](references/WORKFLOWS.md) - 完整工作流指南
- [API_REFERENCE.md](references/API_REFERENCE.md) - API 端点文档
- [EXAMPLES.md](references/EXAMPLES.md) - 使用示例

### 系统要求

- Python 3.7+
- 飞书应用 ID 和密钥（私有文档需要）
- 依赖：`requests`、`python-dotenv`

### 认证方式

支持两种认证模式：

- **租户认证**（默认）- 应用级访问
- **用户认证**（OAuth）- 用户特定权限

### 许可证

MIT 许可证

### 联系方式

- **作者**：龚子
- **邮箱**：gxj1512@163.com

---

## Supported Content Types / 支持的内容类型

### Text Blocks / 文本块
- Plain text with styles (bold, italic, underline, colors)
- Headings (levels 1-9)
- Bullet and numbered lists
- Inline code

### Code Blocks / 代码块
- 70+ programming languages
- Syntax highlighting

### Media / 媒体
- Images (local files and URLs)
- Tables with styled cells
- Equations (LaTeX)
- Mermaid diagrams
- Whiteboards (flowcharts, mind maps)

---

## Roadmap / 路线图

- [ ] Batch document operations
- [ ] Advanced table editing
- [ ] Comment and mention support
- [ ] Version history integration
- [ ] Multi-language document support

---

## Contributing / 贡献

Contributions are welcome! Please feel free to submit a Pull Request.

欢迎贡献！请随时提交 Pull Request。

---

## License / 许可证

This project is licensed under the MIT License.

本项目采用 MIT 许可证。
