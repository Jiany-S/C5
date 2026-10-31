"""Readable CLI presentation. All receipts describe real completed MCP calls."""
from __future__ import annotations

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

CATEGORIES = {"get_service_details": "DATA", "record_service_interest": "ACTION",
              "register_verified_service_interest": "ORCHESTRATION"}
EXAMPLES = [
    "What does Project Clarity cost and how long is it?",
    "Please record follow-up interest in Project Clarity. My name is Demo Student, "
    "email demo@example.com, notes: Scope a Python study planner.",
    "First verify Team Sprint, then register my follow-up interest. My name is Demo Team, "
    "email team@example.com, notes: Plan a four-student app sprint.",
]


class TerminalUI:
    def __init__(self, console: Console | None = None):
        self.console = console or Console(highlight=False)

    def say(self, message: str, *, style: str | None = None) -> None:
        self.console.print(Text(message, style=style))

    def welcome(self, model: str, directory) -> None:
        body = Text("Ask about services or request a follow-up.\n")
        body.append("Fictional coaching business | No booking, payment or email delivery.\n", style="dim")
        body.append(f"Model: {model}\nRecords: {directory}\n")
        body.append("/help  /examples  /tools  /records  /new  /quit", style="cyan")
        self.console.print(Panel(body, title="CedarBridge | Mira", border_style="cyan", expand=False))
        self.say('Try: "What does Project Clarity cost and how long is it?"', style="dim")

    def tools(self, tools) -> None:
        table = Table(title="Connected MCP tools", show_lines=True, expand=False)
        table.add_column("Category", style="cyan")
        table.add_column("Registered tool", overflow="fold")
        for tool in tools:
            table.add_row(CATEGORIES[tool.name], tool.name)
        self.console.print(table)
        self.say("Data reads service facts. Action saves explicit follow-up interest.\nOrchestration verifies a service before conditionally saving.", style="dim")

    def help(self) -> None:
        self.say("Chat in plain language. Name the service; include contact details only when requesting follow-up.")
        self.say("/examples  Show three copy-paste requests\n/tools     Show tools discovered from the running server\n"
                 "/records   Read saved IDs and services; contacts stay hidden\n/new       Clear chat history; saved interests remain\n"
                 "/quit      Close the connection (quit and exit also work)")
        self.say("Tool receipts are real MCP results. Launch with --trace to include raw result JSON.", style="dim")

    def examples(self) -> None:
        for index, prompt in enumerate(EXAMPLES, 1):
            self.say(f"{index}. {prompt}")

    def request(self, name: str) -> None:
        self.say(f"MCP request -> server | {CATEGORIES.get(name, 'TOOL')} | {name}", style="cyan")

    def receipt(self, payload: dict) -> None:
        code = payload.get("code", "mcp_error")
        style = "green" if payload.get("status") == "ok" else "yellow"
        self.say(f"MCP result <- server | {code}", style=style)
        service = payload.get("service")
        if service:
            self.say(f"  {service['name']}: USD {service['price_usd']} per {service['price_unit']} | {service['duration_minutes']} minutes")
        if payload.get("record_id"):
            label = "Saved" if payload.get("created") else "Existing"
            self.say(f"  {label} record ID: {payload['record_id']}")
        if payload.get("steps"):
            self.say("  Sequence: " + " -> ".join(f"{s['capability']} ({s['code']})" for s in payload["steps"]))
        if payload.get("status") != "ok":
            self.say("  " + payload.get("message", "Request could not be completed."))

    def answer(self, answer: str) -> None:
        self.console.print(Panel(Markdown(answer), title="Mira", border_style="green", expand=False))

    def records(self, records: list[dict]) -> None:
        self.say(f"Saved follow-up interests: {len(records)} (read-only view)", style="cyan")
        if not records:
            self.say("No interests saved in this record directory.")
            return
        table = Table(show_lines=True)
        table.add_column("Service")
        table.add_column("Record ID", overflow="fold")
        for record in records:
            table.add_row(record["service_name"], record["record_id"])
        self.console.print(table)

    def error(self, message: str) -> None:
        self.console.print(Panel(Text(message), title="Needs attention", border_style="yellow", expand=False))
