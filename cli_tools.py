"""
在终端中配合 Claude Agent SDK 使用的 CLI 工具与便捷函数集合。
"""

import os
import argparse
import json

from claude_agent_sdk import (
    AssistantMessage, 
    TextBlock, 
    ResultMessage, 
    ToolUseBlock, 
    ToolResultBlock, 
    ThinkingBlock, 
    UserMessage, 
    Message, 
    SystemMessage
)
from rich import print
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.console import Console
from rich.prompt import Prompt
from rich.syntax import Syntax
from dotenv import load_dotenv
from typing import Literal

load_dotenv()

ANTHROPIC_ENV_KEYS = [
    "ANTHROPIC_BASE_URL",
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_MODEL",
]

def print_anthropic_env(label: str) -> None:
    """打印 Anthropic 相关关键环境变量的值。"""
    print(f"{label}：")
    for key in ANTHROPIC_ENV_KEYS:
        value = os.getenv(key)
        if value is None:
            print(f"{key}=<未设置>")
        else:
            print(f"{key}={value}")


# --------------------------------
# 解析命令行运行参数
# --------------------------------

parser = argparse.ArgumentParser()
parser.add_argument("--stats", "-s", default="False", help="是否打印会话统计")
parser.add_argument("--model", "-m", default="haiku", help="要使用的模型名称")
parser.add_argument("--output-style", "-os", default="Personal Assistant", help="期望使用的输出风格")
parser.add_argument("--print-raw", "-pr", default="False", help="是否打印原始消息")


# --------------------------------
# 打印消息的辅助函数
# --------------------------------

def print_rich_message(
        type: Literal["user", "assistant", "tool_use", "tool_result", "system"],
        message: str,
        console: Console
        ):
    """
    根据消息类型，使用带标题与边框颜色的面板打印内容。
    """
    styles = {
        "user": {
            "message_style": "bold yellow",
            "panel_title": "User Prompt",
            "border_style": "yellow"
            },
        "assistant": {
            "message_style": "bold green",
            "panel_title": "Assistant",
            "border_style": "green"
            },
        "tool_use": {
            "message_style": "bold blue",
            "panel_title": "Tool Use",
            "border_style": "blue"
            },
        "tool_result": {
            "message_style": "bold magenta",
            "panel_title": "Tool Result",
            "border_style": "magenta"
            },
        "system": {
            "message_style": "bold cyan",
            "panel_title": "System Message",
            "border_style": "cyan"}
    }

    # 对工具结果尝试启用 JSON 语法高亮
    if type == "tool_result" and is_json_string(message):
        panel_content = Syntax(message, "json", theme="monokai", line_numbers=False)
    else:
        panel_content = Text(message, style=styles[type]["message_style"])

    if type == "system":
        panel=Panel.fit(
            panel_content,
            title=styles[type]["panel_title"],
            border_style=styles[type]["border_style"]
            )
    else:
        panel=Panel(
            panel_content,
            title=styles[type]["panel_title"],
            border_style=styles[type]["border_style"]
            )
    console.print(panel, end="\n\n")


def is_json_string(text: str) -> bool:
    """判断字符串是否为合法 JSON"""
    try:
        json.loads(text)
        return True
    except json.JSONDecodeError:
        return False


def format_tool_result(content) -> str:
    """
    对工具返回内容进行友好格式化，兼容嵌套的 JSON 字符串。
    """
    if isinstance(content, str):
        # 尝试按 JSON 解析并格式化
        try:
            parsed = json.loads(content)
            return json.dumps(parsed, indent=2)
        except json.JSONDecodeError:
            return content
    elif isinstance(content, list):
        # 处理内容块列表（常见结构）
        formatted_parts = []
        for item in content:
            if isinstance(item, dict) and "text" in item:
                # 解析 text 字段中的 JSON
                text_content = item["text"]
                try:
                    parsed_json = json.loads(text_content)
                    formatted_json = json.dumps(parsed_json, indent=2)
                    formatted_parts.append(formatted_json)
                except json.JSONDecodeError:
                    # 若非 JSON，则原样使用
                    formatted_parts.append(text_content)
            else:
                # 其它字典结构按 JSON 打印
                formatted_parts.append(json.dumps(item, indent=2))
        return "\n\n".join(formatted_parts)
    else:
        # 其他类型转 JSON 字符串
        return json.dumps(content, indent=2)


def get_user_input(console: Console) -> str:
    """
    获取用户输入并以面板形式展示，同时返回输入字符串。
    """
    user_input = Prompt.ask("\n[bold yellow]You[/bold yellow]", console=console)
    print()
    return user_input


def parse_and_print_message(
        message: Message, 
        console: Console,
        print_stats: bool = False
        ):
    """
    按消息类型解析并打印内容。
    """
    # 助手消息可能包含 TextBlock、ToolUseBlock、ThinkingBlock、ToolResultBlock
    # https://docs.claude.com/en/api/agent-sdk/python#content-block-types
    if isinstance(message, SystemMessage):
        if message.subtype == "compact_boundary":
            print_rich_message(
                "system", 
                f"压缩完成 \n压缩前令牌数: {message.data['compact_metadata']['pre_tokens']} \n触发来源: {message.data['compact_metadata']['trigger']}",
                console
                )
        else:
            print_rich_message("system", json.dumps(message.data, indent=2), console)
    elif isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                print_rich_message("assistant", block.text, console)
            elif isinstance(block, ToolUseBlock):
                print_rich_message("tool_use", f"Tool: <{block.name}> \n\n {block.input}", console)
            elif isinstance(block, ThinkingBlock):
                print_rich_message("assistant", "Thinking...", console)
    elif isinstance(message, UserMessage):
        for block in message.content:
            if isinstance(block, ToolResultBlock):
                formatted_content = format_tool_result(block.content)
                print_rich_message("tool_result", formatted_content, console)
    elif isinstance(message, ResultMessage):
        
        if print_stats:
            result = message.subtype
            session_id = message.session_id
            duration_s = message.duration_ms/1000
            cost_usd = message.total_cost_usd
            input_tokens = message.usage["input_tokens"]
            output_tokens = message.usage["output_tokens"]

            session_stats = {
                "Session ID": session_id,
                "Result": result,
                "Duration (s)": f"{duration_s:.2f}",
                "Cost (USD)": f"${cost_usd:.2f}" if cost_usd else "N/A",
                "Input Tokens": input_tokens,
                "Output Tokens": output_tokens
            }

            if session_stats:
                stats_table = Table(
                    title="Session Stats",
                    show_header=False,
                    title_style="bold blue"
                )
                stats_table.add_column(style="cyan", no_wrap=True)
                stats_table.add_column(style="yellow")

                for stat_name, stat_value in session_stats.items():
                    stats_table.add_row(stat_name, str(stat_value))

                console.print(stats_table, end="\n")
