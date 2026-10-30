# Source review and API compatibility

Reviewed 2026-10-30, before implementation. `evidence/materials_manifest.json` records local source SHA-256 hashes, PDF page counts and notebook cell counts. Source materials remain outside this standalone repository.

| Required source | Reviewed copy | Application to C5 |
|---|---|---|
| [Assignment](https://drive.google.com/file/d/1l00NuDt1RDD4D5AE_E2jCSsI_kHdWVWN/view) | Connected Drive text and local `C5 - Agent Tools Ass.pdf`, 3 pages; re-read in full for final review | Authoritative 3 tools, framework pair, 300–400 words, 1–2 paragraphs and 5–7-minute video |
| [Chapter notes](https://drive.google.com/file/d/1G8VaupHhpmIsmgfkxzGEuxXDGibY529Q/view) | Local `C5 - Agent Tools-1.pdf`, 8 pages | Isolated functionality, minimal typed inputs, logging and predictable failures |
| [Lecture deck](https://drive.google.com/file/d/1GLwgrGdyuRSiEHl0rgSyc-Hj22fl5Q4V/view) | Local `C5 - Agent Tools - Deck.pdf`, 69 pages; extracted text plus rendered diagram-rich pp. 13,16,38,43,52,58,65 | Host/client/server separation; tool categories; direct SDK MCP support |
| [Trust/safety discussion](https://drive.google.com/file/d/1QV70Y4AeTDlHGKwA-QINU3v-rCsWIK4E/view) | Local `C5.1 - Would You Trust This Agent_ - Deck.pdf`, 10 pages | Duplicate-credit example motivated atomic database uniqueness; stock/capacity example motivated bounded claims about published facts |
| [Seven tutorials](https://drive.google.com/drive/folders/1YoOTZH0Z9wac4YcPV15j9xh0dxG_z8At) | All seven local notebooks, markdown and code cells reviewed | See specific observations below |
| [Hugging Face article](https://huggingface.co/blog/Kseniase/mcp) | Public article and its linked [Turing Post expansion](https://www.turingpost.com/p/mcp) | Integration motivation; architecture verified separately against primary protocol sources |
| [C3 business facts](https://github.com/Jiany-S/C3/blob/main/me/business_summary.txt) | Local summary plus GitHub connector read, blob SHA `021d921280118ddfb52d4ca103cd6ebb171d441a` | Three fictional service names, durations, prices, languages and operating boundaries only |

Tutorial observations:

1. **Requests and API Wrappers**: request parameters, timeouts, HTTP errors and environment credentials. Core C5 data is local so the demo does not depend on a weather/search service.
2. **OpenAI Function Calling**: definitions, model-selected arguments, local execution, returned observation and final answer. Its legacy `functions/function_call` example is conceptual background; C5 uses current Agents SDK MCP integration.
3. **Data Tools**: database/PDF/web retrieval and simulated dispatch. Its SQL string interpolation and arbitrary-query interface are not copied; C5 has a fixed read-only catalog lookup.
4. **Action Tools**: database/file/email state changes, validation and retry-safe behavior. C5 restricts the effect to one local parameterized insert; it does not send messages.
5. **Orchestration Tools**: ordered workflows with outputs feeding later steps. C5 stops on invalid service instead of continuing to the write after an error.
6. **MCP Filesystem and Fetch**: actual `MCPServerStdio`, tool discovery and `mcp_servers` integration. C5 keeps one Python server and avoids unrelated browser/filesystem tools.
7. **Building an MCP Server and Client with an Open Source LLM**: weather server decorators, stdio lifecycle and model/tool loop. C5 uses the required OpenAI Agents SDK instead of loading a quantized local model or copying its manual parser.

## Current primary implementation sources

- [FastMCP tools](https://gofastmcp.com/servers/tools): decorators, typed schemas, structured returns, annotations and error masking.
- [FastMCP server execution](https://gofastmcp.com/deployment/running-server): stdio subprocess use and stdout constraints. Streamable HTTP is available for future remote hosting; old SSE examples are not a reason to add networking here.
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) and [v2 client documentation](https://py.sdk.modelcontextprotocol.io/client/): async lifecycle, structured_content and is_error. The v1 maintenance README explicitly distinguishes v1 and current v2; C5 tests the resolved v2 types.
- [Official OpenAI integration guidance](https://developers.openai.com/api/docs/guides/agents/integrations-observability), [Agents SDK MCP guide](https://openai.github.io/openai-agents-python/mcp/) and [installed-version source](https://github.com/openai/openai-agents-python/blob/v0.24.0/src/agents/mcp/server.py): constructor, call_tool arguments, list discovery, managed stdio streams and cleanup. Signatures and SDK default child environment keys were also inspected locally after installation.
- [Fetch implementation at revision fb31aa5ad2852ac2cb272fc7de7225547e1ed870](https://github.com/modelcontextprotocol/servers/blob/fb31aa5ad2852ac2cb272fc7de7225547e1ed870/src/fetch/src/mcp_server_fetch/server.py): inspected `create_server`, `fetch_url`, robots checks and private-address handling. The summary critiques this revision specifically.

`pip index versions` and PyPI metadata were checked before resolving FastMCP 4.1.4, MCP 2.3.0 and Agents SDK 0.24.0. A fresh Python 3.11 virtual environment installed them together successfully. `pip check` reported no broken requirements. A complete freeze is included with a Windows marker for pywin32; direct requirements are pinned separately. Real subprocess and OpenAI runs verify compatibility more strongly than documentation snippets alone.

The lecture notes describe orchestration through agents-as-tools, while the assignment explicitly permits a tool coordinating Data and Action capabilities. The assignment is authoritative here. No subagent, extra tool or nested model is needed for this small workflow.
