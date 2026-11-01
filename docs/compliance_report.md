# Submission compliance review

Re-reviewed 2026-11-01 against all three pages of the authoritative assignment and the current repository. Published requirements are separated from the user's additional engineering checks. This is a software review, not a professor-issued grade.

**Outcome:** source, written deliverables and execution evidence are prepared; the repository is verified public. The separate submission screencast export is verified at 1.12x and 6:57.633, meeting the 5-7-minute duration requirement. The overall handoff remains **PARTIAL** until the final video is reviewed, uploaded and its accessible sharing link is supplied. See [current handoff](submission.md) and [latest validation](submission_review.md).

## Published assignment requirements

| Requirement | Exact implementation location | Evidence/test | Status | Correction / next action |
|---|---|---|---|---|
| Read Hugging Face article | `docs/sources_review.md`; `docs/mcp_research_summary.md` | Public introduction and linked expansion reviewed; article scope disclosed | PASS | None |
| Inspect existing MCP server | `docs/mcp_research_summary.md`, reference 3 | Fetch source pinned to `fb31aa5ad2852ac2cb272fc7de7225547e1ed870`; actual handlers inspected | PASS | None |
| Summary 300–400 words | `docs/mcp_research_summary.md`, marked main body | 371 whitespace-delimited words; `evidence/history/security_audit.json` | PASS | Keep references outside counted body |
| Explain Host/Client/Server and MCP concepts | Summary paragraphs 1–3; `docs/architecture.md` | Describes discovery, typed definitions, invocation, outputs and host execution | PASS | None |
| Critique server using class principles | Summary paragraphs 4–5 | Focus, parameter bounds, errors, output modes, changing external data and untrusted content | PASS | None |
| Coherent original/inspired theme | `business_data/services.json` | CedarBridge facts match read-only C3 summary; no C3 application dependency | PASS | None |
| Exactly three distinct tools | `mcp_server.py` three `@mcp.tool` definitions | `test_start_connect_and_exact_schemas`; `evidence/protocol.json` actual discovery | PASS | Do not add helper decorators |
| One Data tool without state changes | `mcp_server.py:get_service_details`; `business.py:lookup_service` | `test_known_data_is_read_only`, all 3 services, no store creation/catalog changes | PASS | None |
| One Action tool with a real effect | `mcp_server.py:record_service_interest`; `business.py:record_interest` | `test_action_persists_and_duplicate_is_stable`; live record ID and row count | PASS | None |
| One Orchestration tool coordinates the other capabilities | `business.py:register_verified_interest` | `test_orchestration_real_lookup_then_action`; actual `steps`, server events and persisted row | PASS | Shared business functions are internal calls, not claimed as nested MCP calls |
| Clear descriptions, typed inputs and output | Decorated signatures; `business.py:Service`, `Step`, `ToolResult`; `docs/tool_design.md` | Discovered input/output schemas asserted over MCP | PASS | None |
| Focused single responsibility | `docs/tool_design.md`, tool table and boundary rationale | Separate read, write, verify-then-write contracts | PASS | Retry routing overlap is documented; do not portray routing as perfectly deterministic |
| Predictable failure for every tool | Business codes and FastMCP validation | Unknown Data lookup; invalid Action contact/storage; Orchestration lookup failure/consent gate | PASS | None |
| FastMCP server | `mcp_server.py`, `FastMCP(...)` and `run(transport="stdio")` | Actual server process used in all protocol and live tests | PASS | None |
| OpenAI Agents SDK host/client | `agent_client.py:make_server`, `make_agent`, `cli` | `Agent(mcp_servers=[server])`, `Runner.run`, actual SDK connection; no local function tools | PASS | None |
| Agent routes requests through MCP | `ObservableMCPServer.call_tool` awaits SDK super-method | Final live Data/Action/Orchestration cases selected distinct tools and returned actual results | PASS | None |
| Functional tests including failures | `tests/test_protocol.py`, `tests/test_agent.py`, `scripts/protocol_demo.py` | 49 passed, 1 opt-in live test skipped in ordinary suite; 7/7 separate real live cases | PASS | Skipped ordinary live test is not presented as an API execution |
| Configuration and README | `README.md`, `.env.example`, requirements files | Fresh isolated Python 3.11 installation; `pip check` passed | PASS | Windows tested; other OSes not claimed as executed |
| Written summary and source deliverables | Standalone C5 source, docs and ZIP | File inventory, ZIP integrity and extracted-copy MCP discovery/protocol verification | PASS | Rebuild ZIP after adding real submission links |
| Reflection, 1–2 paragraphs | `docs/reflection.md` | Two paragraphs; real observed decisions/challenges and next steps | PASS | Student should review and adapt to their own understanding |
| 5–7-minute screencast duration | Local `runtime/video-edit/C5_Submission_Video.mp4`; metadata in `evidence/submission_review.json` | Verified 6:57.633 at 1.12x; exact approved cut and ending retained | PASS | Review presentation content and upload separately |
| Video shows full live round trips | Recorded live demo and `evidence/live_agent.json` | Actual software round trips passed; final recording exists | PARTIAL | Owner final playback review and hosted link pending |
| Video explains challenges and solutions | Latest recording; `docs/reflection.md`; recording plan | Real duplicate/failure issues documented; latest recording replaces older takes | PARTIAL | Owner final playback review and hosted link pending |
| Repository and video links shared in submission | `docs/submission.md` | GitHub connector verified Jiany-S/C5 public on 2026-11-01 | PARTIAL | Add hosted video URL and verify viewer access |

## Additional engineering checks requested by the user

| Check | Exact location / evidence | Status | Correction / limit |
|---|---|---|---|
| Review notes, lecture, safety deck and 7 tutorials | `docs/sources_review.md`; `evidence/materials_manifest.json` | PASS | Source PDFs/notebooks deliberately not bundled |
| Requirements checklist created before code | `docs/requirements_checklist.md` | PASS | Final hosted-video link remains pending |
| Current compatible APIs verified | `docs/sources_review.md`; requirements lock; final real execution | PASS | Pins describe the tested date, not future latest releases |
| Separate standalone C5, C3/C4 untouched | New C5 `.git`; C3/C4 final `git status --short` empty | PASS | No C6 work performed |
| Async lifecycle and subprocess cleanup | `make_server` context; `test_connections_close_on_exception_and_release_store` | PASS | Explicit SQLite closure fixes the observed Windows leak |
| No unnecessary external APIs | Local JSON + SQLite; only host makes OpenAI calls | PASS | Live agent still requires OpenAI access |
| No API credential in source or child configuration | `evidence/submission_review.json`; explicit allowlist in `make_server` | PASS | Local `.env` is ignored and excluded from ZIP; pattern scan does not read its key |
| Persistent duplicate safety across concurrent processes | `test_concurrent_servers_and_restart_deduplicate` | PASS | One outstanding interest per normalized email/service; no update semantics |
| Meaningful temporary-store testing | `tests/conftest.py`; protocol demo temporary directory | PASS | Demo runtime stores are synthetic and ignored by Git |
| Cleanliness and package audit | `.gitignore`; `scripts/package_submission.py`; security evidence | PASS | No environments, caches, runtime databases or source course materials in submission |
| Paid model calls labeled separately from scripted responses | `tests/test_agent.py`; live report execution tag | PASS | Scripted tests verify plumbing, not genuine language reasoning |
| Tested video prompts and silent-caption option | `scripts/demo_cases.py`; final live report; recording plan | PASS | Narration not explicitly required by PDF; captions still need timing/readability review |
| Non-Windows environment execution | README portability notes | NOT TESTED | Optional future verification; Windows/Python 3.11 is the tested target |
| Arbitrary adversarial prompts / authenticated consent | Architecture limits | NOT TESTED | Server verifies Boolean intent, not user identity; do not expose publicly as a production service |

## Requested minimum testing matrix

| # | Required behavior | Exact test/evidence | Status |
|---|---|---|---|
| 1 | Server starts | `test_start_connect_and_exact_schemas` | PASS |
| 2 | Client connects | Same test and every subprocess fixture | PASS |
| 3 | Exactly three tools | Same test; `evidence/protocol.json:tools` | PASS |
| 4 | Correct names, descriptions and schemas | Same test checks categories, required fields, types, descriptions, output schema | PASS |
| 5 | Correct known Data results | `test_known_data_is_read_only`, 3 services | PASS |
| 6 | Unknown Data service | `test_unknown_service_and_recovery` | PASS |
| 7 | Genuine persistence | `test_action_persists_and_duplicate_is_stable`; direct SQLite row comparison | PASS |
| 8 | Invalid emails / required fields rejected | Domain, schema and missing-field parameterized tests | PASS |
| 9 | Orchestration performs lookup then action | `test_orchestration_real_lookup_then_action`; ordered steps and saved UUID | PASS |
| 10 | Failed lookup prevents write | `test_failed_lookup_stops_action`; directory not created | PASS |
| 11 | Agent invokes each through MCP | 3 scripted SDK cases plus 3 real live categories | PASS |
| 12 | Agent correctly uses returned facts, IDs and failures | Scripted result forwarding checks and final live cases/answers | PASS for specified cases |
| 13 | Information-only question does not write | Data read-only tests; live `data` and `information_with_contact` | PASS |
| 14 | Repeated requests safe | Concurrent/restart test plus live `repeat`, same ID and row count | PASS |
| 15 | Safe errors without credential exposure | Storage failure/recovery test, masked framework errors, host safe error handler and exact-key audit | PASS within tested local scope |

## Evidence interpretation and corrections made

`evidence/pytest.xml` contains the fresh 2026-11-01 run: 49 passed / 1 skipped. Only its machine hostname attribute was removed for privacy; outcomes, timings and test names are unchanged. The skip is the explicitly opt-in paid test. `evidence/live_agent.json` separately records a real `gpt-4.1-mini` run with seven passed scenarios. `evidence/protocol.json` records seven real MCP calls without a model and successful connection closure. Initial live JSON reports remain available and are not counted as final passes. The dated `security_audit.json` and `archive_reproduction.json` describe the initial 2026-10-30 build; `review_validation.md` records the additional 2026-10-31 checks without rewriting those historical snapshots.

Early runs exposed a wrong FastMCP environment value, a test helper's `name` collision, and an unclosed SQLite handle on Windows. The first two were corrected; explicit `closing(...)` and a regression test resolved the handle issue. Early live responses overstated the staff response target or omitted the duplicate UUID. Instructions now require bounded wording, and the repeat prompt explicitly requests the ID. Repeated requests sometimes select orchestration even when the shorter Action route would suffice. That route is semantically safe, so the retry evaluation accepts either while requiring the same existing ID and unchanged count; it does not relax the dedicated tool-category scenarios.

## Strict academic assessment

The implementation is strong for this assignment: real interoperable transport, minimal local dependencies beyond the required frameworks, clear business boundaries, meaningful concurrency/failure tests, traceable research and honest evidence. The principal design cost is overlap between recording and verified recording. Explaining that tradeoff is preferable to claiming perfect model routing. The local Boolean consent gate and conservative email syntax are appropriate demonstration constraints, but they are not production authorization or identity verification.

The independent reviewer found no new implementation blocker and assessed technical/written quality at approximately 95/100 unofficially. This is not a professor rubric or a final assignment grade. The remaining handoff work is the final video playback review, upload and accessible sharing link.


## Independent review and interface refinements (2026-10-31)

A separate subagent re-read the actual assignment, reviewed the implementation and CLI, and independently ran focused checks. Its final technical/written assessment was approximately **95/100 unofficially**, with no remaining code blocker; this historical assessment does not grade the current recording or invent a professor rubric. See `independent_review.md` for findings and resolutions.

Corrections added a clear welcome and commands, compact actual MCP receipts, optional schemas/raw tracing, safe categorized errors and per-turn recovery. Shared configuration fixes inspector directory mismatches. Domain labels longer than 63 characters are rejected. Live evidence now uses atomic per-run snapshots and preserves failure/cancellation instead of leaving stale success. Evaluation rejects contradictory external-effect claims and incorrect price substrings, and checks persisted/retry IDs. The final suite contains 49 passes and one opt-in paid skip; the separate fresh real OpenAI demo passed seven scenarios.

The first revised live run was 5/7 because model answers omitted two IDs despite correct writes and visible receipts. That report remains unchanged. Making IDs explicit in both the Action message and final-answer instruction yielded the subsequent 7/7 run. Primary review of all seven final answers confirmed facts, IDs and failure wording; automated prose checks remain heuristics. The actual multi-turn CLI check also succeeded at state/persistence behavior, though its initial route-specific probe expected Action and observed the semantically valid Orchestration route; both facts are retained in `evidence/history/interactive_cli.json`.

| Revised check | Evidence | Status |
|---|---|---|
| CLI onboarding, commands, recovery and safe errors | `tests/test_cli.py`; `docs/interface_review.md` | PASS |
| Inspector shell/.env/project-relative consistency | `test_inspector_uses_dotenv_and_project_relative_paths` | PASS |
| 63/64-character email domain boundary | `tests/test_protocol.py` | PASS |
| No stale passing evidence after failure/cancellation | `tests/test_demo.py` | PASS |
| Contradictory prose / $150 versus $15 rejected | `tests/test_demo.py`; `scripts/demo_checks.py` | PASS for specified counterexamples |
| Fresh live model and real MCP with final code | `evidence/history/live_agent_review_final.json` | PASS, 7/7 |
| 60- and 80-column terminal layout | `docs/images/terminal-60.png`, `terminal-80.png` | PASS, visual exports reviewed |

The repository is now public and the screencast is recorded. Overall submission remains PARTIAL until the final video is reviewed, uploaded and linked. Current export metadata and package checks are documented in `submission_review.md`.
