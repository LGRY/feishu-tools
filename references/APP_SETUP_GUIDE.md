# Feishu App Setup Guide

This guide walks you through creating and configuring a Feishu (Lark) application for reading documents via the Feishu Open API.

---

## Table of Contents

1. [Overview](#overview)
2. [Creating Your Feishu App](#creating-your-feishu-app)
3. [Obtaining App Credentials](#obtaining-app-credentials)
4. [Configuring Permissions](#configuring-permissions)
5. [Publishing Your App](#publishing-your-app)
6. [Setting Up Credentials in Claude](#setting-up-credentials-in-claude)
7. [Troubleshooting](#troubleshooting)
8. [Permission Reference](#permission-reference)
9. [Best Practices](#best-practices)

---

## Overview

To use the Feishu Reader skill with private documents, you need to:

1. Create a self-built application on the Feishu Open Platform
2. Configure the required API permissions
3. Obtain your App credentials (App ID and App Secret)
4. Configure the credentials in your Claude environment

**Note**: Public documents don't require any setup. You can read them immediately without creating an app.

---

## Creating Your Feishu App

### Step 1: Access the Feishu Open Platform

1. Visit [https://open.feishu.cn/](https://open.feishu.cn/)
2. Sign in with your Feishu account
3. If you don't have an account, click "Register" to create one

### Step 2: Create a New Application

1. Click the **"Create App"** button in the top-right corner
2. Select **"Self-built App"** from the options
3. Fill in the application details:
   - **App Name**: Enter a descriptive name, e.g., "Claude Feishu Reader"
   - **App Description**: Briefly describe the purpose, e.g., "Document reader for Claude AI assistant"
   - **App Icon**: Optionally upload an icon (not required)
4. Click **"Create"** to create your application

### Step 3: Navigate to App Management

After creation, you'll be redirected to your app's management dashboard. This is where you'll configure credentials and permissions.

---

## Obtaining App Credentials

### Step 1: Access Credentials Page

1. In the left sidebar, click **"Credentials & Basic Info"** (凭证与基础信息)
2. This page displays your app's authentication credentials

### Step 2: Copy Your Credentials

You'll need two values:

1. **App ID** (Application ID)
   - Displayed on the credentials page
   - Format: `cli_xxxxxxxxxxxxxxxxx`
   - Click to copy

2. **App Secret** (Application Secret)
   - Hidden by default for security
   - Click **"View"** or **"Show"** to reveal
   - Format: A long alphanumeric string
   - Copy and store securely - you'll need it later

**Important Security Note**:
- Never share your App Secret publicly
- Never commit it to version control
- Treat it like a password

---

## Configuring Permissions

### Understanding Permission Types

Feishu uses tenant-level permissions for apps. The permissions you need depend on what you want to access:

| Feature | Required Permission | Status |
|---------|---------------------|--------|
| Read documents | `docx:document` | Required |
| Read Wiki pages | `wiki:wiki:readonly` | Optional |
| Read Drive files | `drive:drive:readonly` | Optional |
| Search content | `search:search:readonly` | Optional |

### Step 1: Access Permissions Management

1. In the left sidebar, click **"Permissions & Scopes"** (权限管理)
2. You'll see two tabs: "Tenant Permissions" and "User Permissions"
3. Stay on the **"Tenant Permissions"** tab

### Step 2: Add Required Permissions

#### Method A: Manual Configuration (Individual Permissions)

1. Click **"Add Permission"** or **"Configure"**
2. Find and enable each permission:
   - Search for "document" and enable `docx:document`
   - Search for "wiki" and enable `wiki:wiki:readonly`
   - Search for "drive" and enable `drive:drive:readonly`
3. Click **"Save"** after enabling each permission

#### Method B: Batch Import (JSON Configuration) - Recommended

For faster setup, use the batch import feature:

1. In the **"Permissions & Scopes"** page, find and click **"Batch Import"** (批量导入)
2. Select **"JSON Configuration"** mode
3. Paste the following JSON configuration:

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

4. Click **"Import"** or **"Apply"**
5. All specified permissions will be enabled at once

### Step 3: Verify Permissions

After adding permissions, verify they appear in your tenant permissions list:
- ✅ `docx:document` - Get and access documents
- ✅ `wiki:wiki:readonly` - Read Wiki pages
- ✅ `drive:drive:readonly` - Read Drive files

---

## Publishing Your App

### Understanding Publishing Options

Feishu offers two modes for app usage:

1. **Debug Mode** - For development and testing
2. **Production Mode** - For production use

### Option A: Debug Mode (Immediate Access)

Debug mode allows you to use the app immediately without review.

**Steps:**
1. In the left sidebar, click **"Debug Credentials"** (调试凭证)
2. Your app is now ready for testing
3. Use the App ID and App Secret from the credentials page
4. No approval needed

**Limitations:**
- Only accessible to you (the app creator)
- Limited to testing purposes
- Cannot be shared with other users

### Option B: Production Mode (Multi-User Access)

For production use or sharing with others, you need to publish your app.

**Steps:**
1. In the left sidebar, click **"Publish & Review"** (发布管理)
2. Click **"Create Version"** (创建版本)
3. Fill in version information:
   - **Version Number**: e.g., `1.0.0`
   - **Update Log**: Describe what's new
   - **Version Description**: Explain the app's purpose
4. Click **"Submit for Review"** (提交审核)
5. Wait for approval (typically 1-3 business days)

**After Approval:**
- Your app can access documents in any tenant
- You can share the app with other users
- Full production access granted

**Note**: For personal use with your own documents, Debug Mode is sufficient.

---

## Setting Up Credentials in Claude

### Option A: Interactive Setup Script (Recommended)

The skill includes an automated setup script:

1. Open your terminal or command prompt
2. Navigate to your skill directory
3. Run the setup script:

```bash
python scripts/setup_feishu_config.py
```

4. When prompted, enter:
   - **App ID**: Paste your App ID (e.g., `cli_a1b2c3d4e5f6g7h8`)
   - **App Secret**: Paste your App Secret

5. The script will:
   - Validate your credentials
   - Fetch a tenant access token from Feishu API
   - Save everything to `~/.claude/config.json`

### Option B: Manual Configuration

Alternatively, manually create the configuration file:

1. Locate or create the global config file:
   - **Windows**: `C:\Users\YourName\.claude\config.json`
   - **macOS/Linux**: `~/.claude/config.json`

2. Add the following JSON structure:

```json
{
  "feishu": {
    "app_id": "cli_your_app_id_here",
    "app_secret": "your_app_secret_here",
    "tenant_access_token": ""
  }
}
```

3. Save the file
4. The tenant_access_token will be fetched automatically on first use

### Environment Variable Option (Advanced)

For advanced users, you can set environment variables instead:

```bash
# Windows PowerShell
$env:FEISHU_APP_ID="cli_your_app_id"
$env:FEISHU_APP_SECRET="your_app_secret"

# macOS/Linux
export FEISHU_APP_ID="cli_your_app_id"
export FEISHU_APP_SECRET="your_app_secret"
```

Environment variables take precedence over the config file.

---

## Troubleshooting

### Error 99991404: Permission Denied

**Problem**: The app doesn't have permission to access the requested resource.

**Solutions**:
1. Verify all required permissions are enabled in "Permissions & Scopes"
2. Check that permissions are under "Tenant Permissions" (not "User Permissions")
3. After adding permissions, wait 2-3 minutes for changes to take effect
4. For production apps, ensure the app has been approved and published
5. Verify the document is shared with your app or is publicly accessible

**Verification Steps**:
```
1. Go to Feishu Open Platform → Your App → Permissions & Scopes
2. Check these permissions are enabled:
   - docx:document
   - wiki:wiki:readonly (if accessing Wikis)
   - drive:drive:readonly (if accessing Drive files)
3. If permissions are missing, add them and save
```

### Error 99991003: Invalid Token

**Problem**: The tenant access token has expired.

**Context**: Tenant access tokens expire after 2 hours for security reasons.

**Solution**:
```bash
# Re-run the setup script to get a fresh token
python scripts/setup_feishu_config.py
```

The script will automatically fetch a new token and update your config.

**Automatic Token Refresh**: The skill attempts to refresh tokens automatically. If it fails, manual setup is required.

### Error 99991663 or 99991401: Document Not Found

**Problem**: The document doesn't exist or isn't accessible.

**Possible Causes**:
1. Incorrect document ID or URL
2. Document has been deleted
3. Document isn't shared with your app
4. Document is in a different tenant (for multi-tenant apps)

**Solutions**:
1. Verify the document URL is correct
2. Open the document in a browser to confirm it exists
3. For private documents, ensure they're shared with your Feishu app
4. Check that your App ID matches the one granted access

### Error 99990100: Invalid App Credentials

**Problem**: App ID or App Secret is incorrect.

**Solutions**:
1. Double-check your App ID and App Secret in the Feishu Open Platform
2. Ensure no extra spaces when copying credentials
3. Verify you're using the correct app (if you have multiple apps)
4. Re-run the setup script with corrected credentials

### Public Document Access Issues

**Problem**: Unable to read a publicly accessible document.

**Solutions**:
1. Verify the document is actually public by opening in incognito/private browser mode
2. Check if the document URL format is correct:
   - Wiki: `https://xxx.feishu.cn/wiki/NODE_TOKEN`
   - Document: `https://xxx.feishu.cn/docx/DOC_ID`
3. Try accessing via browser first to confirm availability
4. If public access fails but browser works, the document structure may have changed

---

## Permission Reference

### Complete Permission List

| Permission Scope | Permission Name | Required | Use Case |
|-----------------|-----------------|----------|----------|
| `docx:document` | Get Documents | ✅ Yes | Read and access document content, blocks, and metadata |
| `wiki:wiki:readonly` | Get Wiki | ❌ Optional | Read Wiki pages and node content |
| `drive:drive:readonly` | Get Drive Files | ❌ Optional | Read files stored in Feishu Drive |
| `search:search:readonly` | Search | ❌ Optional | Search across documents and content |

### Permission Scopes Explained

**Tenant Permissions (App-Level)**:
- Apply to the entire application
- Don't require user authorization
- Used by this skill

**User Permissions (User-Level)**:
- Require each user to authorize
- Used for user-specific actions
- Not needed for this skill

### Minimum Required Configuration

For basic document reading functionality, you only need:
```json
{
  "scopes": {
    "tenant": [
      "docx:document"
    ]
  }
}
```

---

## Best Practices

### Security Best Practices

1. **Never Commit Credentials**
   - Add `~/.claude/config.json` to `.gitignore`
   - Never include App Secrets in code or documentation

2. **Rotate Secrets Regularly**
   - Periodically regenerate your App Secret in the Feishu console
   - Update your config after rotation

3. **Use Principle of Least Privilege**
   - Only enable permissions you actually need
   - Disable unused permissions

4. **Monitor App Usage**
   - Check Feishu Open Platform analytics
   - Review API call logs periodically

### Development Best Practices

1. **Start with Debug Mode**
   - Use Debug Credentials for initial testing
   - Switch to Production only when ready

2. **Test with Public Documents First**
   - Verify basic functionality before configuring credentials
   - Public documents don't require any setup

3. **Handle Token Expiration Gracefully**
   - The skill attempts auto-refresh
   - Re-run setup script if manual refresh is needed

4. **Keep App Information Updated**
   - Maintain accurate app description
   - Update version notes when making changes

### Production Deployment

1. **For Personal Use**:
   - Debug mode is sufficient
   - No app review needed

2. **For Team/Organization Use**:
   - Publish app and submit for review
   - Share App ID/Secret securely with team
   - Each team member runs setup script

3. **For Public Distribution**:
   - Submit app for Feishu marketplace review
   - Provide comprehensive documentation
   - Implement proper error handling

---

## Additional Resources

### Official Documentation

- [Feishu Open Platform](https://open.feishu.cn/)
- [API Reference](https://open.feishu.cn/document/server-docs/api-reference)
- [Authentication Guide](https://open.feishu.cn/document/server-docs/authentication-management/access-token/tenant_access_token)
- [Permission Management](https://open.feishu.cn/document/home/ugn-7105708426972368898)

### Skill Documentation

- [Configuration Guide](configuration.md) - Advanced configuration options
- [Error Codes Reference](error-codes.md) - Complete API error code list
- [Batch Operations](batch-operations.md) - Processing multiple documents

### Community Resources

- [Feishu Developer Community](https://open.feishu.cn/community)
- [Feishu GitHub](https://github.com/larksuite)

---

## Quick Setup Checklist

Use this checklist to ensure you've completed all steps:

### Pre-Setup

- [ ] Have a Feishu account
- [ ] Determined if you need app setup (public documents don't need it)
- [ ] Decided on Debug vs Production mode

### App Creation

- [ ] Created self-built app on Feishu Open Platform
- [ ] Copied App ID
- [ ] Copied App Secret
- [ ] Stored credentials securely

### Permission Configuration

- [ ] Added `docx:document` permission
- [ ] Added `wiki:wiki:readonly` permission (if needed)
- [ ] Added `drive:drive:readonly` permission (if needed)
- [ ] Saved permission changes

### Publishing

- [ ] For testing: Located Debug Credentials
- [ ] For production: Created version and submitted for review

### Claude Configuration

- [ ] Ran setup script (`python scripts/setup_feishu_config.py`)
- [ ] Entered App ID and App Secret
- [ ] Verified config saved to `~/.claude/config.json`
- [ ] Successfully read a test document

---

## Support

If you encounter issues not covered in this guide:

1. **Check Error Messages**: Look up the error code in [error-codes.md](error-codes.md)
2. **Verify Permissions**: Ensure all required permissions are enabled
3. **Test Credentials**: Re-run the setup script to validate credentials
4. **Consult Documentation**: Refer to official Feishu API documentation
5. **Community Support**: Visit the [Feishu Developer Community](https://open.feishu.cn/community)

---

**Last Updated**: 2025-01-29

---

# 飞书应用配置指南

本指南将详细介绍如何创建和配置飞书应用，以便通过飞书开放 API 读取文档。

---

## 目录

1. [概述](#概述)
2. [创建飞书应用](#创建飞书应用)
3. [获取应用凭证](#获取应用凭证)
4. [配置权限](#配置权限)
5. [发布应用](#发布应用)
6. [在 Claude 中配置凭证](#在-claude-中配置凭证)
7. [故障排查](#故障排查)
8. [权限参考](#权限参考)
9. [最佳实践](#最佳实践)

---

## 概述

要使用飞书阅读器技能访问私有文档，您需要完成以下步骤：

1. 在飞书开放平台创建自建应用
2. 配置所需的 API 权限
3. 获取应用凭证（App ID 和 App Secret）
4. 在 Claude 环境中配置凭证

**注意**：公开文档无需任何配置，可以直接读取，无需创建应用。

---

## 创建飞书应用

### 第一步：访问飞书开放平台

1. 访问 [https://open.feishu.cn/](https://open.feishu.cn/)
2. 使用您的飞书账号登录
3. 如果没有账号，点击"注册"创建新账号

### 第二步：创建新应用

1. 点击页面右上角的 **"创建应用"** 按钮
2. 从选项中选择 **"自建应用"**
3. 填写应用详情：
   - **应用名称**：输入一个描述性名称，例如"Claude 飞书阅读器"
   - **应用描述**：简要说明用途，例如"Claude AI 助手的文档阅读工具"
   - **应用图标**：可选上传图标（非必需）
4. 点击 **"创建"** 完成应用创建

### 第三步：进入应用管理

创建完成后，系统会自动跳转到应用管理控制台。在这里您可以配置凭证和权限。

---

## 获取应用凭证

### 第一步：访问凭证页面

1. 在左侧菜单栏中，点击 **"凭证与基础信息"**
2. 此页面显示您的应用身份验证凭证

### 第二步：复制凭证信息

您需要获取两个关键值：

1. **App ID**（应用 ID）
   - 直接显示在凭证页面上
   - 格式：`cli_xxxxxxxxxxxxxxxxx`
   - 点击即可复制

2. **App Secret**（应用密钥）
   - 默认隐藏以保证安全
   - 点击 **"查看"** 或 **"显示"** 按钮来查看
   - 格式：一长串字母数字组合
   - 复制并妥善保管 - 后续配置需要使用

**重要安全提示**：
- 绝不要公开分享您的 App Secret
- 绝不要将其提交到版本控制系统
- 将其视为密码一样处理

---

## 配置权限

### 理解权限类型

飞书应用使用租户级权限。根据您要访问的内容，需要配置不同的权限：

| 功能 | 所需权限 | 状态 |
|---------|---------------------|--------|
| 读取文档 | `docx:document` | 必需 |
| 读取 Wiki 页面 | `wiki:wiki:readonly` | 可选 |
| 读取云空间文件 | `drive:drive:readonly` | 可选 |
| 搜索内容 | `search:search:readonly` | 可选 |

### 第一步：访问权限管理

1. 在左侧菜单栏中，点击 **"权限管理"**
2. 您会看到两个标签页："租户权限"和"用户权限"
3. 确保停留在 **"租户权限"** 标签页

### 第二步：添加所需权限

#### 方法 A：手动配置（逐个添加权限）

1. 点击 **"添加权限"** 或 **"配置"** 按钮
2. 搜索并启用每个权限：
   - 搜索"document"并启用 `docx:document`
   - 搜索"wiki"并启用 `wiki:wiki:readonly`
   - 搜索"drive"并启用 `drive:drive:readonly`
3. 启用每个权限后点击 **"保存"**

#### 方法 B：批量导入（JSON 配置）- 推荐

使用批量导入功能可快速完成配置：

1. 在 **"权限管理"** 页面中，找到并点击 **"批量导入"** 按钮
2. 选择 **"JSON 配置"** 模式
3. 粘贴以下 JSON 配置：

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

4. 点击 **"导入"** 或 **"应用"** 按钮
5. 所有指定的权限将一次性启用

### 第三步：验证权限

添加权限后，验证它们已出现在租户权限列表中：
- ✅ `docx:document` - 获取和访问文档
- ✅ `wiki:wiki:readonly` - 读取 Wiki 页面
- ✅ `drive:drive:readonly` - 读取云空间文件

---

## 发布应用

### 理解发布选项

飞书提供两种应用使用模式：

1. **调试模式** - 用于开发和测试
2. **生产模式** - 用于正式使用

### 选项 A：调试模式（立即可用）

调试模式允许您立即使用应用，无需审核。

**步骤**：
1. 在左侧菜单栏中，点击 **"调试凭证"**
2. 您的应用现在已可用于测试
3. 使用凭证页面中的 App ID 和 App Secret
4. 无需审批

**限制**：
- 仅您（应用创建者）可以访问
- 仅用于测试目的
- 无法与其他用户共享

### 选项 B：生产模式（多用户访问）

如需正式使用或与他人共享，需要发布应用。

**步骤**：
1. 在左侧菜单栏中，点击 **"发布管理"**
2. 点击 **"创建版本"** 按钮
3. 填写版本信息：
   - **版本号**：例如 `1.0.0`
   - **更新日志**：说明更新内容
   - **版本描述**：解释应用用途
4. 点击 **"提交审核"** 按钮
5. 等待审批（通常需要 1-3 个工作日）

**审批通过后**：
- 您的应用可以访问任何租户的文档
- 您可以与其他用户共享应用
- 获得完整的生产访问权限

**注意**：个人使用自己的文档时，调试模式已足够。

---

## 在 Claude 中配置凭证

### 选项 A：交互式设置脚本（推荐）

该技能包含自动化设置脚本：

1. 打开终端或命令提示符
2. 导航到技能目录
3. 运行设置脚本：

```bash
python scripts/setup_feishu_config.py
```

4. 根据提示输入：
   - **App ID**：粘贴您的 App ID（例如 `cli_a1b2c3d4e5f6g7h8`）
   - **App Secret**：粘贴您的 App Secret

5. 脚本将自动：
   - 验证您的凭证
   - 从飞书 API 获取租户访问令牌
   - 将所有信息保存到 `~/.claude/config.json`

### 选项 B：手动配置

您也可以手动创建配置文件：

1. 找到或创建全局配置文件：
   - **Windows**：`C:\Users\您的用户名\.claude\config.json`
   - **macOS/Linux**：`~/.claude/config.json`

2. 添加以下 JSON 结构：

```json
{
  "feishu": {
    "app_id": "cli_您的app_id",
    "app_secret": "您的app_secret",
    "tenant_access_token": ""
  }
}
```

3. 保存文件
4. tenant_access_token 将在首次使用时自动获取

### 选项 C：环境变量（高级用户）

对于高级用户，可以设置环境变量：

```bash
# Windows PowerShell
$env:FEISHU_APP_ID="cli_您的app_id"
$env:FEISHU_APP_SECRET="您的app_secret"

# macOS/Linux
export FEISHU_APP_ID="cli_您的app_id"
export FEISHU_APP_SECRET="您的app_secret"
```

环境变量的优先级高于配置文件。

---

## 故障排查

### 错误 99991404：权限不足

**问题**：应用无权访问请求的资源。

**解决方案**：
1. 验证"权限管理"中已启用所有必需的权限
2. 检查权限位于"租户权限"下（而非"用户权限"）
3. 添加权限后等待 2-3 分钟使更改生效
4. 对于生产应用，确保应用已通过审核并发布
5. 验证文档已与您的应用共享或是公开可访问的

**验证步骤**：
```
1. 访问飞书开放平台 → 您的应用 → 权限管理
2. 检查以下权限是否已启用：
   - docx:document
   - wiki:wiki:readonly（如访问 Wiki）
   - drive:drive:readonly（如访问云空间文件）
3. 如权限缺失，添加并保存
```

### 错误 99991003：令牌无效

**问题**：租户访问令牌已过期。

**背景**：出于安全考虑，租户访问令牌的有效期为 2 小时。

**解决方案**：
```bash
# 重新运行设置脚本以获取新令牌
python scripts/setup_feishu_config.py
```

脚本将自动获取新令牌并更新您的配置。

**自动令牌刷新**：该技能会尝试自动刷新令牌。如果失败，需要手动运行设置脚本。

### 错误 99991663 或 99991401：文档未找到

**问题**：文档不存在或无法访问。

**可能原因**：
1. 文档 ID 或 URL 不正确
2. 文档已被删除
3. 文档未与您的应用共享
4. 文档位于不同的租户（对于多租户应用）

**解决方案**：
1. 验证文档 URL 是否正确
2. 在浏览器中打开文档以确认其存在
3. 对于私有文档，确保已与您的飞书应用共享
4. 检查您的 App ID 是否与被授予访问权限的应用匹配

### 错误 99990100：应用凭证无效

**问题**：App ID 或 App Secret 不正确。

**解决方案**：
1. 在飞书开放平台再次检查您的 App ID 和 App Secret
2. 确保复制凭证时没有多余空格
3. 验证您使用的是正确的应用（如有多个应用）
4. 使用更正后的凭证重新运行设置脚本

### 公开文档访问问题

**问题**：无法读取公开可访问的文档。

**解决方案**：
1. 通过在浏览器的隐私/无痕模式下打开来验证文档确实是公开的
2. 检查文档 URL 格式是否正确：
   - Wiki：`https://xxx.feishu.cn/wiki/NODE_TOKEN`
   - 文档：`https://xxx.feishu.cn/docx/DOC_ID`
3. 先尝试在浏览器中访问以确认可用性
4. 如果公开访问失败但浏览器可以打开，文档结构可能已变更

---

## 权限参考

### 完整权限列表

| 权限范围 | 权限名称 | 是否必需 | 用途 |
|---------|-----------------|---------|---------|
| `docx:document` | 获取文档 | ✅ 是 | 读取和访问文档内容、块和元数据 |
| `wiki:wiki:readonly` | 获取 Wiki | ❌ 可选 | 读取 Wiki 页面和节点内容 |
| `drive:drive:readonly` | 获取云空间文件 | ❌ 可选 | 读取存储在飞书云空间的文件 |
| `search:search:readonly` | 搜索 | ❌ 可选 | 搜索文档和内容 |

### 权限范围说明

**租户权限（应用级）**：
- 应用于整个应用程序
- 不需要用户授权
- 本技能使用此类型权限

**用户权限（用户级）**：
- 需要每个用户单独授权
- 用于用户特定的操作
- 本技能不需要此类型权限

### 最低所需配置

仅实现基本文档读取功能，您只需要：
```json
{
  "scopes": {
    "tenant": [
      "docx:document"
    ]
  }
}
```

---

## 最佳实践

### 安全最佳实践

1. **绝不提交凭证**
   - 将 `~/.claude/config.json` 添加到 `.gitignore`
   - 绝不在代码或文档中包含 App Secret

2. **定期轮换密钥**
   - 定期在飞书控制台重新生成 App Secret
   - 轮换后更新配置

3. **遵循最小权限原则**
   - 仅启用您实际需要的权限
   - 禁用未使用的权限

4. **监控应用使用情况**
   - 检查飞书开放平台的分析数据
   - 定期审查 API 调用日志

### 开发最佳实践

1. **从调试模式开始**
   - 使用调试凭证进行初始测试
   - 仅在准备好时切换到生产模式

2. **先用公开文档测试**
   - 配置凭证前先验证基本功能
   - 公开文档无需任何设置

3. **优雅处理令牌过期**
   - 技能会尝试自动刷新
   - 如需手动刷新，重新运行设置脚本

4. **保持应用信息更新**
   - 维护准确的应用描述
   - 进行更改时更新版本说明

### 生产部署

1. **个人使用**：
   - 调试模式已足够
   - 无需应用审核

2. **团队/组织使用**：
   - 发布应用并提交审核
   - 安全地与团队共享 App ID/Secret
   - 每个团队成员运行设置脚本

3. **公开分发**：
   - 提交应用到飞书应用市场审核
   - 提供全面的文档
   - 实现适当的错误处理

---

## 其他资源

### 官方文档

- [飞书开放平台](https://open.feishu.cn/)
- [API 参考](https://open.feishu.cn/document/server-docs/api-reference)
- [身份验证指南](https://open.feishu.cn/document/server-docs/authentication-management/access-token/tenant_access_token)
- [权限管理](https://open.feishu.cn/document/home/ugn-7105708426972368898)

### 技能文档

- [配置指南](configuration.md) - 高级配置选项
- [错误代码参考](error-codes.md) - 完整的 API 错误代码列表
- [批量操作](batch-operations.md) - 处理多个文档

### 社区资源

- [飞书开发者社区](https://open.feishu.cn/community)
- [飞书 GitHub](https://github.com/larksuite)

---

## 快速设置清单

使用此清单确保您已完成所有步骤：

### 设置前准备

- [ ] 拥有飞书账号
- [ ] 确定是否需要应用设置（公开文档不需要）
- [ ] 决定使用调试模式还是生产模式

### 应用创建

- [ ] 在飞书开放平台创建自建应用
- [ ] 复制 App ID
- [ ] 复制 App Secret
- [ ] 安全存储凭证

### 权限配置

- [ ] 添加 `docx:document` 权限
- [ ] 添加 `wiki:wiki:readonly` 权限（如需要）
- [ ] 添加 `drive:drive:readonly` 权限（如需要）
- [ ] 保存权限更改

### 发布应用

- [ ] 用于测试：定位到调试凭证
- [ ] 用于生产：创建版本并提交审核

### Claude 配置

- [ ] 运行设置脚本（`python scripts/setup_feishu_config.py`）
- [ ] 输入 App ID 和 App Secret
- [ ] 验证配置已保存到 `~/.claude/config.json`
- [ ] 成功读取测试文档

---

## 支持

如果遇到本指南未涵盖的问题：

1. **检查错误信息**：在 [error-codes.md](error-codes.md) 中查找错误代码
2. **验证权限**：确保已启用所有必需的权限
3. **测试凭证**：重新运行设置脚本以验证凭证
4. **查阅文档**：参考飞书官方 API 文档
5. **社区支持**：访问[飞书开发者社区](https://open.feishu.cn/community)

---

**最后更新**：2025-01-29
