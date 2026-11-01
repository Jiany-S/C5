# Submission review - 2026-11-01

The complete C5 source, tests, written deliverables, configuration and packaging were reviewed against the three-page assignment. A separate reviewer independently inspected the repository and exercised the actual MCP connection. No new implementation blocker was found.

## Current validation

- Fresh ordinary pytest: **49 passed, 1 skipped** in 122.33 seconds. The skip is the explicitly opt-in paid API test. `evidence/pytest.xml` has only the machine hostname attribute removed; results and timings are preserved.
- Dependency consistency: `pip check` reports no broken requirements.
- The independent probe discovered exactly three tools with the expected required fields, rejection of extra arguments and typed object output schemas. It verified real persistence, stable duplicate IDs, failed-lookup short circuiting and omission of contact details from results.
- The canonical real OpenAI report remains the completed **7/7** run dated 2026-10-31 in `evidence/live_agent.json`. No new paid calls were needed for documentation and media cleanup. Scripted-model tests are not presented as live-model evidence.
- Research summary: **371 words**, with references excluded. Reflection: **two paragraphs**. Their substantive text is unchanged.
- The public repository URL and visibility were verified through the GitHub connector. The final hosted-video URL remains pending.

The final source archive is allowlisted and checked for integrity, matching file contents and operation from an extracted copy outside the project directory. This reproduction reuses the tested dependency environment; it does not claim a second clean dependency installation. Machine-readable results and limitations are in [submission_review.json](../evidence/submission_review.json).

## Cleanup

The README now leads with the project, setup commands, deliverables and actual MCP behavior. The handoff no longer incorrectly claims that no repository or recording exists. Historical review documents are explicitly dated snapshots, with a pointer to current status.

Current test/protocol/live evidence is easy to identify through the [evidence index](../evidence/README.md). Earlier failed and intermediate JSON reports moved unchanged into `evidence/history/`; their failures were not rewritten as successes. Course source materials remain referenced rather than redistributed.

Three original MKV recordings and the installation log were preserved under ignored `runtime/recordings/` and `runtime/install/`. Existing edited MP4s retain their paths. Media ignore rules protect recordings and editing assets against accidental staging. The source package excludes `.env`, runtime databases, environments, caches, raw media and model files. A credential-pattern scan checks the deliverable files without reading the local key; it is not an exact-value secret scan or a dependency vulnerability audit.

## Independent assessment and remaining work

The reviewer assessed technical/written quality at approximately **95/100 unofficially**, with no code blocker. This is not a professor-issued rubric or a grade for the recorded presentation. Its submission notes led to the current status corrections, recording protection and JUnit hostname removal.

The latest normal-speed cut is 7:47.716. At the user's direction, a separate pitch-preserving **1.12x** submission export brings it to about **6:57.6**, retaining the exact cut and ending. Its verified duration and local filename are recorded in the [submission handoff](submission.md). The recording owner should watch the final export, upload it, verify viewer access and add its real URL before course submission. No upload or course submission is claimed.
