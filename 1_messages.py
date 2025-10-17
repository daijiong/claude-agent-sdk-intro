"""
演示如何解析并打印 SDK 返回的消息。

为简化示例，我们从 cli_tools.py 导入了若干辅助函数，用以将打印/日志逻辑与主程序分离，便于理解整体流程。
"""

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from rich import print
from rich.console import Console
from cli_tools import print_rich_message, parse_and_print_message, print_anthropic_env
from dotenv import load_dotenv

load_dotenv(override=True)

MODEL = "haiku"

async def main():
    
    print_anthropic_env("当前 Anthropic 环境变量")
    
    # 初始化本次会话要使用的 Console
    console = Console()

    options = ClaudeAgentOptions(
        model=MODEL
    )

    # 启动提示信息
    print_rich_message(
        type="system", 
        message=f"Welcome to your Claude Personal Assistant!\n\nSelected model: {MODEL}",
        console=console
    )

    async with ClaudeSDKClient(options=options) as client:

        input_prompt = "你好，请介绍一下你自己"
        print_rich_message("user", input_prompt, console)
        await client.query(input_prompt)
        async for message in client.receive_response():
            # 如需调试可取消注释以打印原始消息
            # print(message)
            parse_and_print_message(message, console)


if __name__ == "__main__":
    import asyncio
    # 在 Jupyter notebook/交互式环境中运行 asyncio 时需要此设置
    import nest_asyncio
    nest_asyncio.apply()

    asyncio.run(main())
