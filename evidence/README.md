# Evidence index

## Current evidence

| File | What it proves |
|---|---|
| [pytest.xml](pytest.xml) | Latest ordinary suite; the paid API case is explicitly skipped |
| [protocol.json](protocol.json) | Real MCP discovery, seven credential-free calls, persistence counts and connection cleanup; no model |
| [live_agent.json](live_agent.json) | Completed real OpenAI + Agents SDK + MCP run, seven passed scenarios, answers and persistence checks |
| [materials_manifest.json](materials_manifest.json) | Hashes and page/cell counts of reviewed course sources, which are not redistributed |
| [submission_review.json](submission_review.json) | Current cleanup, package, security and reproduction checks, with explicit limitations |

The live run is dated in its JSON. Cleanup does not turn it into a new model execution. All demo contacts are fictional example.com addresses. Scripted-model tests verify transport and result forwarding, not model reasoning. Only the machine `hostname` attribute is removed from the current JUnit XML for privacy; test names, counts, timings and outcomes are preserved.

## Historical reports

`history/` preserves earlier successful, failed and intermediate runs without changing their results. Some deliberately have `passed=false`. The 2026-10-30 security and archive reports describe that earlier build; use the current submission review for the cleaned package. `history/live_agent_review_final.json` is the original saved report promoted to `live_agent.json` after manual review.

Execution evidence does not prove that a video has been uploaded or the professor has accepted the submission.
