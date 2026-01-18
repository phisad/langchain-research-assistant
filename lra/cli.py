import argparse
import asyncio

from rich.console import Console
from rich.markdown import Markdown

from lra.agents import create_research_agent
from lra.tools import multi_tool_server, start

console = Console()


async def run_repl():
    console.print("[bold blue]resi[/bold blue] - Research Assistant")
    console.print("Type [bold]/help[/bold] for commands, [bold]/quit[/bold] to exit.\n")

    tools = await multi_tool_server.get_tools()
    agent = create_research_agent(tools)

    while True:
        try:
            user_input: str = console.input("[bold green]> [/bold green]").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.startswith("/"):
            cmd = user_input.lower().split()[0]
            if cmd in ("/quit", "/exit", "/q"):
                console.print("Goodbye!")
                break
            elif cmd == "/clear":
                console.clear()
            elif cmd == "/help":
                console.print("[bold]Commands:[/bold]")
                console.print("  /help   Show this help")
                console.print("  /quit   Exit the assistant")
                console.print("  /clear  Clear the screen")
            else:
                console.print(f"[yellow]Unknown command: {cmd}[/yellow]")
            continue

        try:
            with console.status("[bold cyan]Thinking...[/bold cyan]"):
                response = await agent(user_input)
            console.print()
            console.print(Markdown(response))
            console.print()
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


def cli():
    parser = argparse.ArgumentParser(description="Research Assistant CLI")
    parser.add_argument('--start-server', action='store_true', help='Start the MCP PDF server')
    args = parser.parse_args()

    if args.start_server:
        start("pdf")
    else:
        asyncio.run(run_repl())


if __name__ == '__main__':
    cli()
