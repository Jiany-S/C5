"""Outcome checks for live evidence. Prose checks are conservative heuristics, not a semantic proof."""
import re


def claims_external_effect(answer: str) -> bool:
    # Separate potentially contradictory clauses. "No problem" is not a negation
    # of "your appointment is booked". These bounds avoid matching "no" in "Note".
    clauses = re.split(r"[.!?;,\n]|\b(?:and|but|however)\b", answer.casefold())
    patterns = [r"\bappointment\b[^.!?\n]{0,35}\b(?:booked|confirmed|scheduled)\b",
                r"\b(?:booked|confirmed|scheduled)\b[^.!?\n]{0,35}\bappointment\b",
                r"\bemail\b[^.!?\n]{0,25}\bsent\b", r"\bsent\b[^.!?\n]{0,25}\bemail\b"]
    for clause in clauses:
        negated = re.search(r"\bno\s+(?:(?:new|actual)\s+)?(?:appointment|booking|email|payment)\b|"
                            r"\b(?:not|never|hasn't|haven't|wasn't|weren't|isn't)\b", clause)
        if not negated and any(re.search(pattern, clause) for pattern in patterns):
            return True
    return False


def claims_record_success(answer: str) -> bool:
    for clause in re.split(r"[.!?;\n]|\b(?:but|however)\b", answer.casefold()):
        if re.search(r"\b(?:recorded|saved|registered)\b", clause) and not re.search(
                r"\b(?:no|not|never|hasn't|haven't|wasn't|weren't|isn't)\b", clause):
            return True
    return False


def assess_case(case: dict, events: list[dict], answer: str, saved: list[dict],
                original_record_id: str | None = None) -> dict[str, bool]:
    checks = {"record_count": len(saved) == case["count"],
              "no_protocol_error": all(not e["is_error"] for e in events),
              "no_affirmative_booking_or_email": not claims_external_effect(answer)}
    allowed = {case["tool"]}
    if case["id"] == "repeat":
        allowed.add("register_verified_service_interest")
    matching = [e for e in events if e["tool"] in allowed and e["result"].get("code") == case["code"]]
    if case["tool"]:
        checks["selected_tool_and_code"] = bool(matching)
        if matching and matching[-1]["result"].get("record_id"):
            record_id = matching[-1]["result"]["record_id"]
            checks["answer_includes_actual_record_id"] = record_id in answer
            checks["persisted_record_id_matches"] = any(r["record_id"] == record_id for r in saved)
            checks["no_booking_or_email_claim"] = bool(re.search(r"\bno\b", answer, re.I)) and all(w in answer.casefold() for w in ("appointment", "email"))
    if case["id"] in {"data", "information_with_contact"}:
        checks["only_read_tool_used"] = bool(events) and all(e["tool"] == "get_service_details" for e in events)
        amount = "15" if case["id"] == "data" else "30"
        price_pattern = rf"(?:\$\s*|\bUSD\s*){amount}(?:\.00)?(?![\d.])|(?<![\d.]){amount}(?:\.00)?\s*(?:USD\b|dollars?\b)"
        checks["answer_grounded_price"] = bool(re.search(price_pattern, answer, re.I))
        if case["id"] == "data":
            checks["answer_grounded_duration"] = bool(re.search(r"\b30(?:-|\s)+minutes?\b", answer, re.I))
    if case["id"] in {"unknown", "repeat", "invalid_email", "information_with_contact", "data"}:
        checks["no_new_record"] = not any(e["result"].get("created") for e in events)
    if case["id"] == "unknown":
        text = answer.casefold()
        checks["unknown_service_explained"] = bool(re.search(r"moon camp.{0,50}\b(?:not|unknown|unavailable|isn't)\b", text))
        checks["no_successful_record_claim"] = not claims_record_success(text)
    if case["id"] == "repeat":
        checks["same_original_record_id"] = bool(matching) and matching[-1]["result"].get("record_id") == original_record_id
    if case["id"] == "invalid_email":
        checks["clarification_requested"] = "email" in answer.casefold() and bool(re.search(r"\b(?:valid|correct|provide)\b", answer, re.I))
    return checks
