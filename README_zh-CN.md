# Claude Agent SDK：分步教程

## 观看视频！

[![image](./thumbnail.png)](https://youtu.be/gP5iZ6DCrUI)

Claude Code 可能是你所知道的最令人印象深刻、最强大的 AI 代理。如果你能利用它来帮助你完成任何事情该多好... 现在你可以了！Claude Agent SDK 是一个高级框架，用于使用 Claude Code 作为核心代理构建自定义 AI 代理系统。

## 你将学到什么

- 创建能够自主读取、写入和编辑文件的 AI 代理
- 构建能够在多轮交互中记住上下文的对话式代理
- 通过模型上下文协议（MCP）集成强大的外部工具
- 设计处理复杂多步骤工作流的专业子代理
- 使用自定义系统提示和工具权限配置代理行为

## 前置条件

开始之前，请确保你已安装：

- **Python 3.13+** 安装在你的系统上
- **uv** 已安装 [安装说明](https://docs.astral.sh/uv/getting-started/installation/)
- **Claude Code** 已安装
`npm install -g @anthropic-ai/claude-code`
- **Chrome 浏览器**（模块 5-6 需要，用于 Playwright MCP 集成）
- **Node.js**（模块 5-6 需要，用于 Playwright MCP 集成）

可选（见下面的步骤 3）：
你可以使用 Anthropic API 密钥或使用 Claude Code 进行身份验证。如果使用 Claude Code 进行身份验证，则不需要设置 API 密钥。
- **Anthropic API 密钥**（在 [console.anthropic.com](https://console.anthropic.com) 获取）

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/kenneth-liao/claude-agent-sdk-intro
cd claude-agent-sdk-intro
```

### 2. 设置环境

创建虚拟环境并安装依赖项：

```bash
uv sync
```

### 3. 配置 API 密钥（可选）

如果你使用 Anthropic API 密钥（见上面的前置条件），

在项目根目录创建一个 `.env` 文件：

```bash
ANTHROPIC_API_KEY=your_api_key_here
```

### 4. 配置本地设置

**重要：** `.claude/settings.json` 文件包含系统特定的文件路径，需要根据你的本地环境更新。

编辑 `.claude/settings.json` 并更新声音文件路径以匹配你的系统。你可能还需要将 uv run 命令路径更新为 python 文件的绝对路径。

```json
{
  "outputStyle": "Personal Assistant",
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "afplay /System/Library/Sounds/Funk.aiff"
          },
          {
            "type": "command",
            "command": "uv run .claude/hooks/log_agent_actions.py"
          }
        ]
      }
    ],
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "afplay /System/Library/Sounds/Purr.aiff"
          }
        ]
      }
    ]
  }
}
```

**macOS 用户：** 默认路径应该可以直接使用。

**Linux/Windows 用户：** 将 `afplay` 命令替换为适当的替代方案：
- **Linux：** 使用 `aplay`、`paplay` 或 `play`（来自 sox）
- **Windows：** 使用 `powershell -c (New-Object Media.SoundPlayer "C:\Windows\Media\notify.wav").PlaySync()`

或者如果你不想要音频通知，可以直接删除声音命令。

### 5. 运行你的第一个模块

```bash
python 0_querying.py
```

## 模块概览

### 模块 0：查询基础
**文件：** `0_querying.py`

学习与 Claude 交互的两种基本方式：`query()` 用于一次性任务，`ClaudeSDKClient` 用于持续对话。理解何时使用每种方法以及如何配置基本的代理选项。

### 模块 1：消息处理
**文件：** `1_messages.py`

掌握从 SDK 解析和显示不同类型消息的技能。学习使用 Rich 创建干净的 CLI 界面，以获得更好的用户体验，包括格式化输出和状态指示器。

### 模块 2：自定义工具
**文件：** `2_tools.py`

通过创建产品搜索函数来构建你的第一个自定义工具。学习三步过程：定义工具、创建 MCP 服务器和配置代理。理解工具命名约定和集成模式。

### 模块 3：代理选项
**文件：** `3_options.py`

使用 `ClaudeAgentOptions` 配置代理行为。控制工具权限、设置自定义系统提示、选择模型和管理文件访问。尝试不同的选项组合，看看它们如何相互作用。

### 模块 4：对话循环
**文件：** `4_convo_loop.py`

构建一个持续的对话界面，用户可以与代理来回交谈。学习如何在多轮对话中维护上下文并创建自然的对话体验。

### 模块 5：模型上下文协议（MCP）
**文件：** `5_mcp.py` | **文档：** [module-5-mcp.md](docs/module-5-mcp.md)

通过 MCP 服务器集成外部工具。连接 Playwright 进行浏览器自动化，使你的代理能够导航网站、截屏和与网页交互。探索 MCP 生态系统，了解如何添加超越内置工具的强大功能。

**前置条件：** Node.js 和 Chrome 浏览器

### 模块 6：子代理
**文件：** `6_subagents.py` | **文档：** [module-6-subagents.md](docs/module-6-subagents.md)

创建独立处理特定任务的专业 AI 代理。学习将工作委托给具有隔离上下文和受限工具访问权限的专家子代理。构建能够并行研究主题、分析数据和协调复杂工作流的多代理系统。

**前置条件：** 模块 5（使用 MCP 工具）

## 运行模块

每个模块都可以独立运行：

```bash
# 使用默认的 Haiku 模型运行（快速、经济）
python <module_file>.py

# 使用 Sonnet 模型运行（平衡性能）
python <module_file>.py --model claude-sonnet-4-20250514

# 使用 Opus 模型运行（最大能力）
python <module_file>.py --model claude-opus-4-20250514
```

注意：模块 0-2 的模型是硬编码的。模块 3-6 接受 `--model` 参数。

## 项目结构

```
claude-agent-sdk-intro/
├── 0_querying.py           # 基本查询模式
├── 1_messages.py           # 消息解析和显示
├── 2_tools.py              # 自定义工具创建
├── 3_options.py            # 代理配置
├── 4_convo_loop.py         # 对话循环
├── 5_mcp.py                # MCP 集成
├── 6_subagents.py          # 多代理系统
├── cli_tools.py            # CLI 辅助函数
├── main.py                 # （可选）主入口点
├── db/                     # 工具的示例数据
├── docs/                   # 详细的模块文档
└── .claude/                # Claude 代理配置
```

## 其他资源

- [Agent SDK 文档（Python）](https://docs.claude.com/en/api/agent-sdk/python)
- [MCP 服务器目录](https://github.com/modelcontextprotocol/servers)
- [Anthropic API 文档](https://docs.anthropic.com)

## 学习建议

1. **按顺序学习** - 每个模块都建立在前一个模块的概念基础上
2. **动手实验** - 修改代码，尝试不同的提示，看看会发生什么
3. **阅读文档** - 模块 5 和 6 有详细的文档和示例
4. **从简单开始** - 使用 Haiku 进行测试，升级到 Sonnet 用于生产
5. **查看源代码** - `cli_tools.py` 中的辅助函数展示了有用的模式

## 常见问题

**导入错误：** 确保你已经运行了 `uv sync` 并激活了虚拟环境

**API 错误：** 验证你的 `ANTHROPIC_API_KEY` 在 `.env` 中设置正确

**模块 5-6 无法工作：** 确保已安装 Node.js 和 Chrome 以使用 Playwright

**声音/通知错误：** 更新 `.claude/settings.json` 中的文件路径以匹配你系统的声音文件，或者如果不需要的话删除声音命令

## 后续步骤

完成所有模块后：

- 为特定任务构建你自己的专业代理
- 探索 MCP 生态系统以获取更多工具
- 结合概念创建复杂的多代理工作流
- 与社区分享你的创作

祝构建愉快！🚀
