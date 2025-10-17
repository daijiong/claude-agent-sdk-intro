# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

这是一个 Claude Agent SDK 的分步教程项目，展示如何使用 Claude Agent SDK 构建自定义 AI 代理系统。项目包含 7 个递进式模块（0-6），每个模块演示一个核心概念。

## 项目管理

- **Python 包管理**: 总是使用 `uv` 而非 `pip` 来管理 Python 项目
- **Node 包管理**: 总是使用 `bun` 而非 `npm` 来管理 Node 项目
- **Python 版本**: 需要 Python 3.13+
- **依赖安装**: 使用 `uv sync` 安装所有依赖

## 常用命令

### 运行模块
```bash
# 运行基础模块（0-2）- 模型已硬编码
python 0_querying.py
python 1_messages.py
python 2_tools.py

# 运行高级模块（3-6）- 支持 --model 参数
python 3_options.py --model claude-sonnet-4-20250514
python 4_convo_loop.py --model claude-sonnet-4-20250514
python 5_mcp.py --model claude-sonnet-4-20250514
python 6_subagents.py --model claude-sonnet-4-20250514

# 可用的模型选项
# - claude-haiku-4-20250611 (快速、经济)
# - claude-sonnet-4-20250514 (平衡性能)
# - claude-opus-4-20250514 (最强能力)
```

### 其他命令行参数
```bash
# 显示会话统计信息
python <module>.py --stats True

# 打印原始消息（用于调试）
python <module>.py --print-raw True

# 指定输出风格
python <module>.py --output-style "Personal Assistant"
```

## 核心架构

### 1. 两种查询模式
- **一次性查询 (`query()`)**: 用于单次任务，不需要维护对话历史
- **持续对话 (`ClaudeSDKClient`)**: 用于多轮对话，保持上下文状态

### 2. 消息处理流程
SDK 返回多种消息类型，通过 `cli_tools.py` 中的 `parse_and_print_message()` 函数统一处理：
- `AssistantMessage`: 包含 `TextBlock`, `ToolUseBlock`, `ThinkingBlock`
- `UserMessage`: 包含 `ToolResultBlock`
- `SystemMessage`: 包含压缩边界和系统事件
- `ResultMessage`: 包含会话统计信息

### 3. 自定义工具（Custom Tools）
创建自定义工具需要三个步骤：
1. 使用 `@tool` 装饰器定义工具函数
2. 使用 `create_sdk_mcp_server()` 创建 MCP 服务器
3. 在 `ClaudeAgentOptions` 中配置 `mcp_servers`

**工具命名约定**: `mcp__<server_name>__<tool_name>`

### 4. Agent 配置（ClaudeAgentOptions）
关键配置选项：
- `model`: 选择使用的 Claude 模型
- `allowed_tools`: 允许使用的工具列表
- `disallowed_tools`: 禁止使用的工具列表
- `mcp_servers`: MCP 服务器配置字典
- `agents`: 子代理定义字典
- `permission_mode`: 权限模式（如 "acceptEdits"）
- `setting_sources`: 设置来源（如 ["project"]）
- `system_prompt`: 自定义系统提示

### 5. 子代理（Subagents）
子代理通过 `AgentDefinition` 定义，提供：
- **上下文隔离**: 子代理有自己的独立上下文
- **工具隔离**: 可以为子代理指定特定的工具集
- **并行化**: 子代理可以并行运行以提高性能

**关键要求**:
- 主代理必须包含 `Task` 工具才能使用子代理
- 子代理通过 `ClaudeAgentOptions.agents` 字典定义

### 6. MCP 集成
MCP (Model Context Protocol) 允许集成外部工具服务器。配置格式：
```python
mcp_servers={
    "ServerName": {
        "command": "executable",  # 如 "npx"
        "args": ["arg1", "arg2"]  # 如 ["-y", "@playwright/mcp@latest"]
    }
}
```

**Playwright MCP 要求**:
- 需要安装 Node.js
- 需要安装 Chrome 浏览器
- 首次运行需要网络连接以下载包

## 项目结构说明

```
├── 0_querying.py        # 基础查询模式：query() vs ClaudeSDKClient
├── 1_messages.py        # 消息解析和 Rich 格式化输出
├── 2_tools.py           # 自定义工具：产品搜索工具示例
├── 3_options.py         # Agent 配置：权限、工具、模型选择
├── 4_convo_loop.py      # 对话循环：多轮交互
├── 5_mcp.py             # MCP 集成：Playwright 浏览器自动化
├── 6_subagents.py       # 子代理系统：youtube-analyst 和 researcher
├── cli_tools.py         # CLI 工具库：消息解析、Rich 输出、参数处理
├── db/products.json     # 示例数据：空间玩具产品目录
├── docs/                # 详细文档：模块 5 和 6 的深度指南
└── .claude/             # Claude 配置：settings.json, hooks, output_styles
```

## 重要文件

### cli_tools.py
提供核心 CLI 功能：
- `print_rich_message()`: 使用 Rich 格式化输出不同类型的消息
- `parse_and_print_message()`: 解析并显示 SDK 消息
- `format_tool_result()`: 格式化工具结果（JSON 高亮）
- `get_user_input()`: 获取用户输入并显示
- `parser`: 命令行参数解析器

### .claude/settings.json
包含 Claude Code 的项目配置：
- `outputStyle`: 输出风格（默认 "Personal Assistant"）
- `hooks`: 事件钩子（Stop 和 Notification 事件）

**注意**: hooks 中的文件路径是系统特定的，需要根据操作系统调整：
- macOS: `afplay /System/Library/Sounds/*.aiff`
- Linux: `aplay`, `paplay`, 或 `play` (sox)
- Windows: PowerShell 命令

## 模块依赖关系

- 模块 0-4: 只需要 Python 和 `uv`
- 模块 5-6: 额外需要 Node.js 和 Chrome（用于 Playwright MCP）
- 模块 6 依赖模块 5 的 MCP 概念

## 开发建议

1. **按顺序学习**: 模块按复杂度递增设计，建议从 0 开始
2. **先用 Haiku 测试**: 开发时使用 Haiku 模型降低成本
3. **理解消息流**: 使用 `--print-raw True` 查看原始消息结构
4. **异步处理**: 所有模块都使用 `asyncio` 和 `nest_asyncio`
5. **并行子代理**: 子代理可以并行执行，充分利用这一特性

## API 密钥配置

项目支持两种认证方式：
1. **Anthropic API Key**: 在 `.env` 文件中设置 `ANTHROPIC_API_KEY`
2. **Claude Code 认证**: 使用 Claude Code 的内置认证，无需 API Key

## 子代理定义

项目包含两个预定义子代理（在 [6_subagents.py](6_subagents.py) 中）：

### youtube-analyst
- **功能**: 分析用户的 YouTube 频道表现
- **工具**: Playwright 浏览器工具 + 文件系统工具
- **输出**: 在 `/docs` 目录生成 markdown 报告

### researcher
- **功能**: 深度研究主题并生成报告
- **工具**: WebSearch, WebFetch, 文件系统工具, TodoWrite
- **输出**: 在 `/docs` 目录生成带引用的 markdown 报告
- **限制**: 明确禁止使用除指定工具外的其他工具

## 故障排除

**导入错误**: 确保运行了 `uv sync` 并激活了虚拟环境

**API 错误**: 检查 `.env` 文件中的 `ANTHROPIC_API_KEY` 设置

**模块 5-6 问题**: 确保已安装 Node.js 和 Chrome

**声音/通知错误**: 更新 `.claude/settings.json` 中的文件路径或删除声音命令

**MCP 连接失败**: 检查网络连接，验证 MCP 包名正确，手动运行 npx 命令测试
