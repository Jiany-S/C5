# Tool design and contract v1.0

All registered interfaces are in `mcp_server.py`; all business capabilities and result models are in `business.py`. No C3 application module is imported. Prices and service facts derive from C3's fictional business summary, reviewed read-only.

| Category / signature | Responsibility | Predictable outcomes |
|---|---|---|
| Data: `get_service_details(service_name: str) -> ToolResult` | Read one published service | `service_found`, `unknown_service` |
| Action: `record_service_interest(name: str, email: str, service_name: str, notes: str, follow_up_requested: bool) -> ToolResult` | Persist explicit interest in an already selected service | `interest_recorded`, `already_recorded`, `invalid_input`, `unknown_service`, `consent_required`, `storage_error` |
| Orchestration: `register_verified_service_interest(name: str, email: str, service_name: str, notes: str, follow_up_requested: bool) -> ToolResult` | Coordinate lookup followed by conditional persistence | Lookup failure stops the sequence; no consent skips recording; otherwise return the Action outcome with ordered `steps` |

The Action tool's service-membership check is a write invariant, not a second full service-information response. The Orchestration tool provides the higher-level lookup-then-register contract and returns the service information plus the sequence. This small overlap protects direct Action callers while keeping three understandable entry points. Instructions distinguish already-chosen recording from verify-then-register requests. No tool mixes a menu of unrelated operations into an `action` string.

## Inputs

All fields are required. Service name is 1–100 characters, matched case-insensitively with collapsed whitespace. Name is 1–100 characters; notes are 1–1000 characters, nonempty after stripping. Email is 3–254 characters, normalized to lowercase and checked using a documented conservative ASCII pattern: one `@`, dotted domain, alphabetic suffix, no consecutive dots. This is syntax validation, not proof of ownership or deliverability; internationalized or unusual valid addresses may be rejected. Consent must be a JSON Boolean; strings such as `"yes"` must fail schema validation. Missing/incorrect types or length violations produce MCP validation errors before business code executes.

## Output

`ToolResult` is a Pydantic model, so FastMCP advertises an output schema and returns structured data. Every domain result includes:

- `schema_version`: `"1.0"`.
- `status`: `"ok"`, `"error"` or `"skipped"`; `code` and human-readable `message` explain it.
- `service`: typed published facts or null; `context`: fictional business boundaries and hours for successful Data lookup.
- `record_id`: persisted ID or null; `created`: true only after the new record transaction commits.
- `steps`: actual ordered capability/outcome pairs for orchestration; an empty list for standalone tools.
- `available_services`: choices on failed Data lookup, otherwise empty.

Domain failure is valid structured output, so it does not set the protocol's `is_error` flag. Framework validation/unknown-tool failures do. Clients must handle both. The CLI observer deliberately hides unstructured framework error text; a raw MCP caller can receive framework validation details. Never put secrets in tool arguments.

## Logging, determinism and tests

The catalog gives deterministic lookup results. Action semantics are predictable but IDs/timestamps are intentionally new on first insert. SQLite commits before success is returned; write exceptions yield a generic failure without file paths or raw error text. If a transport fails after commit, retrying the same email/service safely retrieves the prior ID.

`tests/test_protocol.py` verifies the real server and wire-discovered schemas, read-only behavior, persistence, failures, consent and cross-process concurrency. `tests/test_agent.py` uses a clearly labeled scripted model inside the real Agents SDK loop, while `scripts/live_demo.py` separately checks real OpenAI tool selection and result interpretation. No scripted-model outcome is evidence of real model selection.

Annotations advertise read-only/idempotent/closed-world behavior but are hints; actual validation and database constraints enforce behavior. No resource is needed because the required Data interface is itself a callable MCP tool.
