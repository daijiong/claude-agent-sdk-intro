"""
子代理用于将任务委派给专门的智能体。

优势包括：
- 上下文隔离：子代理拥有独立上下文，不与主代理共享。
- 工具隔离：子代理可配置独立工具集合，更利于安全与管理。
- 并行执行：子代理可并发运行，从而提升效率。

更多说明参阅：https://docs.claude.com/en/api/agent-sdk/subagents
"""

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AgentDefinition
from rich import print
from rich.console import Console
from cli_tools import parser, print_rich_message, parse_and_print_message, get_user_input, print_anthropic_env
from dotenv import load_dotenv
load_dotenv()


async def main():
    print_anthropic_env("当前 Anthropic 环境变量")
    console = Console()
    args = parser.parse_args()
    
    options = ClaudeAgentOptions(
        model=args.model,
        permission_mode="acceptEdits",
        setting_sources=["project"],
        allowed_tools=[
            'Read',
            'Write',
            'Edit',
            'MultiEdit',
            'Grep',
            'Glob',
            # 使用子代理必须启用 Task 工具！
            'Task',
            'TodoWrite',
            'WebSearch',
            'WebFetch',
            'mcp__Playwright__browser_close',
            'mcp__Playwright__browser_resize',
            'mcp__Playwright__browser_console_messages',
            'mcp__Playwright__browser_handle_dialog',
            'mcp__Playwright__browser_evaluate',
            'mcp__Playwright__browser_file_upload',
            'mcp__Playwright__browser_fill_form',
            'mcp__Playwright__browser_install',
            'mcp__Playwright__browser_press_key',
            'mcp__Playwright__browser_type',
            'mcp__Playwright__browser_navigate',
            'mcp__Playwright__browser_navigate_back',
            'mcp__Playwright__browser_network_requests',
            'mcp__Playwright__browser_take_screenshot',
            'mcp__Playwright__browser_snapshot',
            'mcp__Playwright__browser_click',
            'mcp__Playwright__browser_drag',
            'mcp__Playwright__browser_hover',
            'mcp__Playwright__browser_select_option',
            'mcp__Playwright__browser_tabs',
            'mcp__Playwright__browser_wait_for',
        ],
        # 亦可为子代理单独限定可用工具；默认会继承全部（含 MCP 工具）。
        agents={
            "youtube-analyst": AgentDefinition(
                description="An expert at analyzing a user's Youtube channel performance. The analyst will produce a markdown report in the /docs directory.",
                prompt="You are an expert at analyzing YouTube data and helping the user understand their performance. You can use the Playwright browser tools to access the user's Youtube Studio. Generate a markdown report in the /docs directory.",
                model="sonnet",
                tools=[
                    'Read',
                    'Write',
                    'Edit',
                    'MultiEdit',
                    'Grep',
                    'Glob',
                    'TodoWrite',
                    'mcp__Playwright__browser_close',
                    'mcp__Playwright__browser_resize',
                    'mcp__Playwright__browser_console_messages',
                    'mcp__Playwright__browser_handle_dialog',
                    'mcp__Playwright__browser_evaluate',
                    'mcp__Playwright__browser_file_upload',
                    'mcp__Playwright__browser_fill_form',
                    'mcp__Playwright__browser_install',
                    'mcp__Playwright__browser_press_key',
                    'mcp__Playwright__browser_type',
                    'mcp__Playwright__browser_navigate',
                    'mcp__Playwright__browser_navigate_back',
                    'mcp__Playwright__browser_network_requests',
                    'mcp__Playwright__browser_take_screenshot',
                    'mcp__Playwright__browser_snapshot',
                    'mcp__Playwright__browser_click',
                    'mcp__Playwright__browser_drag',
                    'mcp__Playwright__browser_hover',
                    'mcp__Playwright__browser_select_option',
                    'mcp__Playwright__browser_tabs',
                    'mcp__Playwright__browser_wait_for',
                ]
            ),
            "researcher": AgentDefinition(
                description="An expert researcher and documentation writer. The agent will perform deep research of a topic and generate a report or documentation in the /docs directory.",
                prompt="You are an expert researcher and report/documentation writer. Use the WebSearch and WebFetch tools to perform research. You can research multiple subtopics/angles to get a holistic understanding of the topic. You can use filesystem tools to track findings and data in the /docs directory. For longer reports, you can break the work into multiple tasks or write sections at a time. But the final output should be a single markdown report. The final report **MUST** include a citations section with links to all sources used. Review the full report, identify any areas for improvement in readability, cohorerence, and relevancy, and make any necessary edits before declaring the task complete. Clean up any extraneous files and only leave the final report in the /docs directory when you are done. You are only permitted to use these specific tools: Read, Write, Edit, MultiEdit, Grep, Glob, TodoWrite, WebSearch, WebFetch. All other tools are prohibited.",
                model="sonnet",
                tools=[
                    'Read',
                    'Write',
                    'Edit',
                    'MultiEdit',
                    'Grep',
                    'Glob',
                    'TodoWrite',
                    'WebSearch',
                    'WebFetch',
                ]
            )
        },
        # 提示：Playwright 需提前安装 Node.js 与 Chrome！
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

    print_rich_message(
        "system",
        f"Welcome to your personal assistant, Kaya!\n\nSelected model: {args.model}",
        console
        )

    async with ClaudeSDKClient(options=options) as client:

        while True:
            input_prompt = get_user_input(console)
            if input_prompt == "exit":
                break

            await client.query(input_prompt)

            async for message in client.receive_response():
                # 如需调试可取消注释打印原始消息
                # print(message)
                parse_and_print_message(message, console)


if __name__ == "__main__":
    import asyncio
    import nest_asyncio
    nest_asyncio.apply()

    asyncio.run(main())
