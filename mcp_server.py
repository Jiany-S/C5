"""Exactly three MCP tools. stdout is reserved for protocol messages."""
import logging
import sys
from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field

from business import ToolResult, lookup_service, record_interest, register_verified_interest

mcp = FastMCP("CedarBridge C5", mask_error_details=True)
ServiceName = Annotated[str, Field(min_length=1, max_length=100, description="Published service: Project Clarity, Prototype Clinic, or Team Sprint; case-insensitive.")]
Name = Annotated[str, Field(min_length=1, max_length=100, description="Customer-supplied name; use fictional data in demos.")]
Email = Annotated[str, Field(min_length=3, max_length=254, description="Customer-supplied ASCII contact email; no deliverability verification.")]
Notes = Annotated[str, Field(min_length=1, max_length=1000, description="Customer-supplied project context; do not include sensitive data.")]
Consent = Annotated[bool, Field(strict=True, description="True only when the user explicitly requests follow-up; informational questions are false.")]


@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False})
def get_service_details(service_name: ServiceName) -> ToolResult:
    """DATA: Read published CedarBridge service facts. Returns service_found or unknown_service; never saves records."""
    return lookup_service(service_name)


@mcp.tool(annotations={"readOnlyHint": False, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False})
def record_service_interest(name: Name, email: Email, service_name: ServiceName, notes: Notes,
                            follow_up_requested: Consent) -> ToolResult:
    """ACTION: Save explicit follow-up interest locally for an already selected service. Requires consent. Repeated email/service returns the existing record ID without updating. Never books or sends email."""
    return record_interest(name, email, service_name, notes, follow_up_requested)


@mcp.tool(annotations={"readOnlyHint": False, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False})
def register_verified_service_interest(name: Name, email: Email, service_name: ServiceName, notes: Notes,
                                      follow_up_requested: Consent) -> ToolResult:
    """ORCHESTRATION: Verify a service with the Data capability, then use the Action capability only with explicit follow-up consent. Returns actual ordered steps and stops before saving on lookup failure. Use for verify-then-register requests."""
    return register_verified_interest(name, email, service_name, notes, follow_up_requested)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stderr, format="%(message)s")
    mcp.run(transport="stdio", show_banner=False)
