import argparse
import asyncio

from lra.agents import create_research_agent
from lra.tools import multi_tool_server, start


async def main(message: str, thread_id: str = "default"):
    tools = await multi_tool_server.get_tools()
    agent = create_research_agent(tools)
    response = await agent(message, thread_id=thread_id)
    return response


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('message', type=str, nargs="*", help='Message to send to the agent.')
    parser.add_argument('--thread', '-t', default="default", help='Conversation thread ID')
    parser.add_argument('--start-server', action='store_true')
    args = parser.parse_args()
    if args.start_server:
        start("pdf")
    elif args.message:
        response = asyncio.run(main(" ".join(args.message), args.thread))
        print(response)
    else:
        parser.print_help()


if __name__ == '__main__':
    cli()
