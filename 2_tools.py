"""
工具调用通过 ClaudeAgentOptions 管理。

添加自定义工具通常分三步：
1. 定义工具函数
2. 使用该工具创建 SDK MCP 服务器
3. 在代理配置中接入本地 MCP 服务器

工具命名约定为 `mcp__<server_name>__<tool_name>`。

更多说明参阅：
https://docs.claude.com/en/api/agent-sdk/custom-tools
"""

import json
import os

from claude_agent_sdk import tool, create_sdk_mcp_server, ClaudeSDKClient, ClaudeAgentOptions
from rich import print
from rich.console import Console
from cli_tools import parser, print_rich_message, parse_and_print_message, print_anthropic_env
from typing import Any
from dotenv import load_dotenv

load_dotenv(override=True)

# ----------------------------
# 1. 定义自定义工具
# ----------------------------
@tool("search_products", "Search for products in the space toys catalog", {"query": str})
async def search_products(args: dict[str, Any]) -> dict[str, Any]:
    # 从 JSON 文件加载商品数据
    products_file = os.path.join("db", "products.json")

    try:
        with open(products_file, 'r') as f:
            products = json.load(f)
    except FileNotFoundError:
        return {
            "content": [{
                "type": "text",
                "text": "Products catalog not found."
            }]
        }

    query = args['query'].lower()
    query_words = query.split()

    # 简单检索：根据商品名称或分类中是否包含关键词匹配商品
    matching_products = []
    for product in products:
        if any(word in product['name'].lower() for word in query_words) or any(word in product['category'].lower() for word in query_words):
            matching_products.append(product)

    if not matching_products:
        return {
            "content": [{
                "type": "text",
                "text": f"No products found matching '{args['query']}'"
            }]
        }

    # 返回最相关的商品（此处直接取首个匹配项）
    best_match = matching_products[0]
    stock_status = "In Stock" if best_match['in_stock'] else "Out of Stock"

    return {
        "content": [{
            "type": "text",
            "text": f"Product: {best_match['name']}\nCategory: {best_match['category']}\nPrice: ${best_match['price']}\nStock: {stock_status}"
        }]
    }

# ----------------------------
# 2. 创建 SDK MCP 服务器
# ----------------------------
products_server = create_sdk_mcp_server(
    name="products",
    version="1.0.0",
    tools=[search_products]
)

async def main():

    print_anthropic_env("当前 Anthropic 环境变量")

    console = Console()
    args = parser.parse_args()
    print(args)

    # ----------------------------
    # 3. 在代理中配置本地 MCP 服务器
    # ----------------------------
    options = ClaudeAgentOptions(
        model=args.model,
        mcp_servers={"products": products_server},
        # 查看所有默认可用的工具：
        # https://docs.claude.com/en/api/agent-sdk/python#tool-input%2Foutput-types
        allowed_tools=["Read", "Write", "mcp__products__search_products"],
        disallowed_tools=["WebSearch", "WebFetch"]
    )

    print_rich_message(
        "system",
        f"Welcome to your Space Toys Store Assistant!\n\nSelected model: {args.model}",
        console
    )

    async with ClaudeSDKClient(options=options) as client:

        input_prompt = "Find me a telescope for kids"
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
