"""Export a terminal preview from real MCP calls, without any model/API key."""
import argparse
import asyncio
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

from rich.console import Console
from agents import set_tracing_disabled

from agent_client import ROOT, discover, make_server
from scripts.inspect_records import read_records
from terminal_ui import TerminalUI


async def preview(width: int, output: Path):
    set_tracing_disabled(True)
    console = Console(file=StringIO(), record=True, width=width, color_system="truecolor")
    ui = TerminalUI(console)
    with TemporaryDirectory(prefix="cedarbridge-ui-") as temp:
        async with make_server(temp, verbose=False, ui=ui) as server:
            tools = await discover(server)
            ui.welcome("Preview | real MCP, no model call", "runtime/preview (temporary store)")
            ui.tools(tools)
            ui.say("\nYou: What does Project Clarity cost and how long is it?")
            await server.call_tool("get_service_details", {"service_name":"Project Clarity"})
            ui.say("\nYou: Verify Team Sprint, then record my explicit follow-up request.\nDemo Team | team@example.com | Plan a student app sprint")
            await server.call_tool("register_verified_service_interest", dict(
                name="Demo Team",email="team@example.com",service_name="Team Sprint",
                notes="Plan a student app sprint",follow_up_requested=True))
            ui.records(read_records(Path(temp)))
            ui.say("\n/help shows commands. /new clears chat history; saved records remain.", style="dim")
            ui.say("Interface preview: actual MCP receipts. No OpenAI model answer is simulated.", style="dim")
    output.mkdir(parents=True, exist_ok=True)
    console.save_html(str(output / f"terminal-{width}.html"), clear=False)
    console.save_svg(str(output / f"terminal-{width}.svg"), title="CedarBridge MCP | Terminal preview")
    print(f"Exported real-MCP terminal preview at {width} columns to {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--width", type=int, choices=(60, 80, 100), default=80)
    parser.add_argument("--output", type=Path, default=ROOT / "runtime/ui-preview")
    args = parser.parse_args()
    asyncio.run(preview(args.width, args.output))
