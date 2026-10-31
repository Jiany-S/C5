# Recording plan: target 6 minutes 20 seconds

The actual screencast remains to be recorded. This plan uses seven scenarios successfully run with `gpt-4.1-mini` through the actual OpenAI Agents SDK and FastMCP subprocess; see `evidence/live_agent.json`. Responses and UUIDs may vary on a new run. Never replace a failed live round trip with fabricated terminal output.

The assignment requires a 5–7-minute screencast and does not explicitly require spoken narration. A silent recording with readable on-screen captions can convey each specified point. `demo_captions.srt` provides a caption draft matching this timeline; align its timing to the actual recording. This is a reading of the assignment, not a statement that the instructor has approved this format.

## Prepare before recording

1. Configure a local C5 `.env` key or the shell's `OPENAI_API_KEY`; do not show its contents. The implementation-time key was read into memory from an authorized existing local file and was not copied into C5.
2. Install the locked environment and verify `python -m pytest -q` using the venv interpreter. The saved evidence is 49 passed, 1 opt-in live test skipped; the live demo is tested separately.
3. Obtain approval before publishing the standalone repository. Insert its real verified URL into `docs/submission.md`. No repository URL is claimed yet.
4. Use a 1080p recording, readable terminal font, word wrap, and a split view of terminal plus README/architecture/code. Hide notifications. Keep only invented names and example.com contacts visible.
5. Open `README.md`, `docs/architecture.md`, `mcp_server.py`, `business.py`, `evidence/pytest.xml`, and `docs/reflection.md`. Keep the caption draft available in the recording editor or on-screen notes.
6. Use the actual live script, not the protocol-only script, for the required agent demonstration:

```powershell
cd 'C:\Users\jijos\Desktop\EECE 503P\C5'
.venv\Scripts\python.exe -m scripts.live_demo --step
```

The script starts the server, discovers the three tools, and pauses before every numbered scenario. Press Enter to run it, or q to stop; EOF also cancels safely. Each scenario uses an independent conversation, so all prompts below are also suitable for separate CLI chats. The fresh store prevents prior rehearsals from changing the success cases into duplicates. There is no destructive reset command. Each run prints its unique runtime/demo-.../live_report.json path and preserves completed/partial execution atomically. Add --trace for raw JSON and server capability events as well as the default real MCP receipts.

## Exact screen sequence

| Time | Screen action | Concise caption / point to establish |
|---|---|---|
| 0:00–0:25 | Show README title and tool table | “CedarBridge C5: a standalone fictional coaching toolkit. Data reads; Action records; Orchestration verifies then records.” |
| 0:25–1:05 | Show architecture diagram and `make_agent` / `make_server` | “Host: Agents SDK application. Client: SDK MCP connection. Server: separate FastMCP Python process over stdio.” Explain discovered tools become model inputs. |
| 1:05–1:30 | Show exactly three decorators in `mcp_server.py`; run live command | Point to actual discovered tool names. Server is launched by client; stdout is protocol-only and capability logs use stderr. |
| 1:30–2:00 | Press Enter for `data` | Highlight selected Data tool, actual result, $15 / 30 minutes / online, and record count zero. |
| 2:00–2:45 | Press Enter for `action` | Highlight real Action call, “Saved record ID,” UUID in both receipt and model answer, and persisted row count one. Add `--trace` to show raw `created=true`. No booking/email. |
| 2:45–3:35 | Press Enter for `orchestration` | Highlight one outer MCP invocation, the actual ordered Sequence line, verified service and second persisted ID. Add `--trace` for server-side capability events and raw `steps`. Explain internal capability calls are not extra MCP round trips. |
| 3:35–4:10 | Press Enter for `unknown` | Unknown Moon Camp returns `unknown_service`; only lookup appears in steps. Count remains two. |
| 4:10–4:45 | Press Enter for `repeat` | Compare original Project Clarity ID with returned ID. `already_recorded`, `created=false`, count two. Either write interface may be selected safely. |
| 4:45–5:20 | Press Enter for `information_with_contact`, then `invalid_email` | Contact details alone do not authorize writing. Invalid email triggers clarification in the observed run. No third row. |
| 5:20–6:00 | Show saved pytest result, SQLite unique constraint/explicit close, reflection | “49 tests passed; live API checks are separate.” Explain duplicate safety, Windows connection closure and precise result interpretation as observed challenges. |
| 6:00–6:20 | Show actual published repository URL and docs | Explain one future improvement: authenticated consent, retention, or structured final answers. End with real repository link and reflection. |

Keep the finished video between **5:00 and 7:00**. Aim for 6:20; preserve actual execution and enough reading time. If API latency exceeds a section, shorten code explanation or pauses. Re-record when an error prevents demonstrating required behavior; do not silently splice in old output as a live result. Verify the exported video's duration and caption readability before submitting.

## Tested copy-paste prompts, in order

These exact strings live in `scripts/demo_cases.py`; the final live report contains each prompt and observed answer.

**1 — Data**

```text
What does Project Clarity cost, how long is it, and how is it delivered? I only want information.
```

**2 — Action**

```text
I have already chosen Project Clarity. Please record my interest for follow-up. My name is Demo Student, email demo@example.com, and my project notes are: Scope a Python study planner.
```

**3 — Orchestration**

```text
First verify that Team Sprint is a published service, then register my interest for follow-up in that service. My name is Demo Team, email team@example.com, notes: Plan a four-student campus app sprint.
```

**4 — Failed lookup**

```text
First verify that Moon Camp is a published service, then register my follow-up interest only if it exists. My name is Demo Moon, email moon@example.com, notes: Explore a space-themed project.
```

**5 — Retry without duplication**

```text
I have already chosen Project Clarity. Please record my interest for follow-up again. My name is Demo Student, email demo@example.com, notes: Scope a Python study planner. If already recorded, tell me the existing record ID.
```

**6 — Information with contact details**

```text
My name is Info Only and my email is info@example.com. How much is Prototype Clinic? This is only an informational question; do not record my details or request follow-up.
```

**7 — Invalid email**

```text
Please record follow-up interest in Project Clarity. My name is Invalid Demo, email not-an-email, notes: Plan my project. Do not guess or correct my email.
```

The last case produced no tool call in the final live run: the agent requested a valid address. Actual server rejection of invalid email is separately proved by protocol tests and the protocol demo. Say which behavior is being shown.

## Persistence proof after the recording

Use the exact directory printed by that run, replacing the example suffix below:

```powershell
.venv\Scripts\python.exe -m scripts.inspect_records --data-dir runtime/demo-REPLACE_WITH_PRINTED_ID
```

The script's per-case proof already queries the actual database in read-only mode and omits contacts. No external database viewer or additional MCP tool is needed. After recording, upload the video where the professor can access it, verify the sharing link, and fill in `docs/submission.md`. Do not commit runtime records or the video file to Git.
