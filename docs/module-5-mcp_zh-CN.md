# 模块 5：模型上下文协议（MCP）

> [!IMPORTANT]
> 由 RAIA 创建！

## 概述

本模块演示如何将 **模型上下文协议（MCP）服务器** 与 Claude Agent SDK 集成。MCP 允许 Claude 与外部工具和服务交互，极大地扩展了其超越内置 SDK 工具的能力。

在本示例中，我们集成了 Playwright MCP 服务器，它使 Claude 能够控制 Web 浏览器、截屏、填写表单并与网页进行交互。

## 什么是 MCP？

模型上下文协议（MCP）是一个开放协议，它标准化了 AI 应用程序连接外部数据源和工具的方式。可以把它想象成一个通用适配器，让 Claude 能够与各种服务、数据库、API 和工具进行通信。

**主要优势：**
- 访问 SDK 内置能力之外的外部工具
- 工具集成的标准化协议
- 社区驱动的 MCP 服务器生态系统
- 根据需要轻松添加或移除工具

📚 **了解更多：** [MCP 官方文档](https://docs.claude.com/en/api/agent-sdk/mcp)

## 代码详解

### 1. 使用 MCP 服务器进行配置

```python
options = ClaudeAgentOptions(
    model=args.model,
    allowed_tools=[
        'Read',
        'Write',
        'Edit',
        'MultiEdit',
        'Grep',
        'Glob'
    ],
    permission_mode="acceptEdits",
    setting_sources=["project"],
    # Note: Playwright requires Node.js and Chrome to be installed!
    mcp_servers={
        "Playwright": {
            "command": "npx",
            "args": [
                "-y",
                "@playwright/mcp@latest"
            ]
        }
    }
)
```

`mcp_servers` 参数接受一个字典，其中：
- **键**：MCP 服务器的名称（例如 "Playwright"）
- **值**：配置对象，包含：
  - `command`：启动 MCP 服务器的可执行命令
  - `args`：传递给命令的参数列表

在本示例中：
- `npx` 运行 Node Package Runner
- `-y` 自动确认包安装
- `@playwright/mcp@latest` 指定 Playwright MCP 包

### 2. Playwright MCP 的前置条件

⚠️ **重要提示：** Playwright MCP 服务器需要：
1. 系统上安装 **Node.js**
2. 安装 **Chrome 浏览器**
3. 互联网连接（首次运行时下载 Playwright 包）

### 3. 工作原理

配置完成后，Playwright MCP 工具会自动对 Claude 可用：

1. SDK 初始化与 MCP 服务器的连接
2. MCP 服务器向 Claude 暴露其工具
3. Claude 现在可以调用 Playwright 工具，例如：
   - `browser_navigate` - 导航到 URL
   - `browser_snapshot` - 捕获页面可访问性快照
   - `browser_click` - 点击元素
   - `browser_type` - 填写表单
   - `browser_take_screenshot` - 截屏
   - 以及更多工具！

其余代码遵循与之前模块相同的模式 - 使用 SDK 客户端的查询/响应循环。

## 可用的 MCP 服务器

以下是一些您可以集成的流行 MCP 服务器：

| MCP 服务器 | 描述 | 使用场景 |
|------------|-------------|-----------|
| **Playwright** | 浏览器自动化 | 网页抓取、测试、截屏 |
| **Filesystem** | 文件操作 | 增强的文件管理 |
| **GitHub** | GitHub API 访问 | 仓库管理、问题跟踪 |
| **PostgreSQL** | 数据库访问 | 查询数据库、管理数据 |
| **Google Drive** | Drive 集成 | 访问文档、表格 |
| **Brave Search** | 网页搜索 | 研究、事实核查 |

📚 **探索更多：** [MCP 服务器目录](https://github.com/modelcontextprotocol/servers)

## 运行模块

```bash
python 5_mcp.py --model claude-sonnet-4-20250514
```

### 示例交互

尝试这些提示来查看 MCP 的实际应用：

1. **网页导航：**
   ```
   Go to anthropic.com and take a screenshot
   ```

2. **网页研究：**
   ```
   Visit wikipedia.org and search for "Model Context Protocol"
   ```

3. **表单交互：**
   ```
   Navigate to example.com/contact and show me the form fields
   ```

## 与之前模块的主要区别

| 方面 | 之前的模块 | 本模块 |
|--------|-----------------|-------------|
| 工具 | 仅内置 SDK 工具 | SDK 工具 + MCP 工具 |
| 能力 | 文件操作、代码编辑 | + 浏览器控制、网页交互 |
| 配置 | 简单的工具列表 | 需要 MCP 服务器配置 |
| 依赖 | 仅 Python 包 | + Node.js、Chrome |

## 添加您自己的 MCP 服务器

要添加另一个 MCP 服务器：

1. 找到您想要的 MCP 服务器（例如，从 MCP 服务器目录中）
2. 将其添加到 `mcp_servers` 字典：

```python
mcp_servers={
    "Playwright": {
        "command": "npx",
        "args": ["-y", "@playwright/mcp@latest"]
    },
    "GitHub": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"]
    }
}
```

3. 确保满足所有前置条件（API 密钥、安装等）
4. 运行您的代理 - 新工具将自动可用！

## 故障排除

### 常见问题

**错误："Cannot find npx"**
- 解决方案：从 [nodejs.org](https://nodejs.org) 安装 Node.js

**错误："Browser not installed"**
- 解决方案：安装 Chrome 浏览器

**MCP 服务器连接失败**
- 检查您的互联网连接
- 验证 MCP 包名称是否正确
- 查看控制台日志以获取详细的错误消息

**工具未显示**
- 确保 MCP 服务器成功启动（检查控制台输出）
- 验证命令和参数是否正确
- 尝试手动运行 npx 命令进行测试

## 其他资源

- 📖 [Claude Agent SDK - MCP 集成](https://docs.claude.com/en/api/agent-sdk/mcp)
- 🛠️ [MCP 服务器注册表](https://github.com/modelcontextprotocol/servers)
- 🌐 [Playwright MCP 文档](https://www.npmjs.com/package/@playwright/mcp)
- 📚 [构建自定义 MCP 服务器](https://modelcontextprotocol.io/docs/building-mcp-servers)
- 🎯 [Agent SDK Python 参考](https://docs.claude.com/en/api/agent-sdk/python)

## 下一步

在掌握了 MCP 集成之后，您可以：

1. **组合多个 MCP 服务器** 以实现复杂的工作流程
2. **构建自定义 MCP 服务器** 以满足您的特定需求
3. **跨不同 MCP 服务器链式调用工具**
4. **探索 MCP 生态系统** 以获取专业化工具

---

💡 **专业提示：** 从一个 MCP 服务器开始，在添加多个服务器之前先理解它的工作原理。这会让调试变得容易得多！
