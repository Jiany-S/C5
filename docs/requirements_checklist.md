# C5 requirements checklist (created before implementation)

Authority: C5 assignment PDF, pp. 1–3, reviewed 2026-10-30. Additional engineering checks below come from the user's request, not an invented grading rubric.

## Published assignment requirements

- [x] Read the Hugging Face MCP article and inspect an existing open-source MCP server.
- [x] Write a 300–400-word summary of MCP architecture and critique the inspected server using Chapter 5 principles.
- [x] Choose one coherent theme: CedarBridge Learning Studio, independent of C3.
- [x] Register exactly three tools: one Data, one Action, one Orchestration.
- [x] Give each tool a description, typed arguments, typed/documented output and focused responsibility.
- [x] Handle predictable failures clearly.
- [x] Use FastMCP for the server and OpenAI Agents SDK for the host/client.
- [x] Route agent requests through real MCP communication.
- [x] Supply tests or scripts proving functionality and failures.
- [x] Supply configuration and README setup instructions.
- [x] Write a 1–2-paragraph reflection on boundaries, tool count and future work.
- [x] Record and export a 5–7-minute screencast: final local export is 6:57.633; owner final playback review remains before upload.
- [ ] Submit the public repository link and final hosted-video link. Repository verified; video upload/link pending.

## Additional requested verification

- [x] Read notes, lecture deck, trust/safety deck and all seven tutorials before code.
- [x] Verify current APIs and install compatible current released packages; pin tested versions.
- [x] Test startup, connection, exact tool names/descriptions/schemas, success and failure over MCP.
- [x] Test persistence, validation, no-consent/no-lookup writes and duplicate/concurrent requests.
- [x] Exercise Agents SDK with labeled scripted model responses and separately with real OpenAI calls.
- [x] Test result interpretation and informational requests that must not write.
- [x] Use temporary test stores; keep secrets, runtime data, caches and environments out of Git.
- [x] Prepare tested demo prompts, recording sequence, architecture and tool-design documentation.
- [x] Re-read the assignment, audit every requirement and fix reasonable findings.

Current completion and evidence locations are recorded in `compliance_report.md` and `submission_review.md`. A recording plan does not satisfy the actual video deliverable.
