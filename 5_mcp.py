"""
可以通过代码定义 MCP，或从 .mcp.json 文件加载。

更多说明参阅：https://docs.claude.com/en/api/agent-sdk/mcp
"""

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
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
        allowed_tools=[
            'Read',
            'Write',
            'Edit',
            'MultiEdit',
            'Grep',
            'Glob',
            # 注意：必须显式允许 MCP 工具，否则默认无法使用。
            # 'mcp__Playwright__browser_navigate'
        ],
        permission_mode="acceptEdits",
        setting_sources=["project"],
        # 提示：Playwright 需提前安装 Node.js 和 Chrome！
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
