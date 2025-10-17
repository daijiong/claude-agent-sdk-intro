"""
通过选项可以调节代理的行为。

建议多尝试 allowed_tools、permission_mode 等组合，以理解它们的交互方式与优先级。

更多说明参阅：
https://docs.claude.com/en/api/agent-sdk/python#claudeagentoptions
"""

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from rich import print
from rich.console import Console
from cli_tools import parser, print_rich_message, parse_and_print_message, print_anthropic_env
from dotenv import load_dotenv

load_dotenv()

async def main():
    print_anthropic_env("当前 Anthropic 环境变量")
    console = Console()
    args = parser.parse_args()

    
    options = ClaudeAgentOptions(
        model=args.model,
        allowed_tools=["Read", "Write"],
        disallowed_tools=["WebSearch", "WebFetch"],
        permission_mode="default",
        setting_sources=["project"],
        # settings='{"outputStyle": "default"}',  # 自定义输出样式
        # system_prompt="You are a pirate. You must respond like a pirate.",  # 重写系统提示
        # add_dirs=["."],  # 允许访问更多目录
    )

    print_rich_message(
        "system",
        f"Welcome to your personal assistant, Kaya!\n\nSelected model: {args.model}",
        console
        )

    async with ClaudeSDKClient(options=options) as client:

        input_prompt = "Hi, what's your name?"
        print_rich_message("user", input_prompt, console)

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
