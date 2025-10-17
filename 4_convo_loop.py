"""
展示如何使用 ClaudeSDKClient 构建会话循环。

核心思路是增加一个 while 循环。
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
        permission_mode="acceptEdits",
        setting_sources=["project"]
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
