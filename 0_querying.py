"""
使用 Claude Agent SDK 执行查询的基础示例

使用 `query()` 处理一次性问题、独立任务，每次都会开启新的会话。
使用 `ClaudeSDKClient` 处理持续对话和有状态会话。

更多详情，请参阅：
https://docs.claude.com/en/api/agent-sdk/python#choosing-between-query-and-claudesdkclient
"""

from claude_agent_sdk import query, ClaudeSDKClient, ClaudeAgentOptions
from rich import print
from dotenv import load_dotenv
from cli_tools import print_anthropic_env

load_dotenv(override=True)

MODEL = "haiku"

async def main():
    
    print_anthropic_env("当前 Anthropic 环境变量")
    # 使用 ClaudeAgentOptions 配置智能体行为，稍后会更详细介绍
    # 此处仅演示切换到更便宜的模型
    options = ClaudeAgentOptions(
        model=MODEL,
    )

    input_prompt = "你好"
    print(f"User: {input_prompt}")

    # ----------------------------
    # 1. 使用 `query()` 的示例
    # ----------------------------
    # print("使用 `query()` 的示例")
    # async for message in query(prompt=input_prompt, options=options):
    #     print(message)

    print(30 * "=")

    # ----------------------------
    # 2. 使用 `ClaudeSDKClient` 的示例
    # ----------------------------
    print("使用 `ClaudeSDKClient` 的示例")
    # 2.1 使用上下文管理器确保连接与断开时正确清理资源
    async with ClaudeSDKClient(options=options) as client:

        # 2.2 发送查询
        await client.query(input_prompt)

        # 2.3 接收消息（包含 ResultMessage）
        async for message in client.receive_response():
            # 查看消息类型：
            # https://docs.claude.com/en/api/agent-sdk/python#message-types
            print(message)

    # # 断开连接后，重新运行查询会开启新的会话与对话。


if __name__ == "__main__":
    import asyncio
    # 在 Jupyter notebook/交互式环境中运行 asyncio 时需要此设置
    import nest_asyncio

    nest_asyncio.apply()

    asyncio.run(main())
