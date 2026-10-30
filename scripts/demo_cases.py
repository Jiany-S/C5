"""Fictional prompts shared by the live demonstration and its checks."""
CASES = [
    {"id": "data", "prompt": "What does Project Clarity cost, how long is it, and how is it delivered? I only want information.",
     "tool": "get_service_details", "code": "service_found", "count": 0},
    {"id": "action", "prompt": "I have already chosen Project Clarity. Please record my interest for follow-up. My name is Demo Student, email demo@example.com, and my project notes are: Scope a Python study planner.",
     "tool": "record_service_interest", "code": "interest_recorded", "count": 1},
    {"id": "orchestration", "prompt": "First verify that Team Sprint is a published service, then register my interest for follow-up in that service. My name is Demo Team, email team@example.com, notes: Plan a four-student campus app sprint.",
     "tool": "register_verified_service_interest", "code": "interest_recorded", "count": 2},
    {"id": "unknown", "prompt": "First verify that Moon Camp is a published service, then register my follow-up interest only if it exists. My name is Demo Moon, email moon@example.com, notes: Explore a space-themed project.",
     "tool": "register_verified_service_interest", "code": "unknown_service", "count": 2},
    {"id": "repeat", "prompt": "I have already chosen Project Clarity. Please record my interest for follow-up again. My name is Demo Student, email demo@example.com, notes: Scope a Python study planner. If already recorded, tell me the existing record ID.",
     "tool": "record_service_interest", "code": "already_recorded", "count": 2},
    {"id": "information_with_contact", "prompt": "My name is Info Only and my email is info@example.com. How much is Prototype Clinic? This is only an informational question; do not record my details or request follow-up.",
     "tool": "get_service_details", "code": "service_found", "count": 2},
    {"id": "invalid_email", "prompt": "Please record follow-up interest in Project Clarity. My name is Invalid Demo, email not-an-email, notes: Plan my project. Do not guess or correct my email.",
     "tool": None, "code": None, "count": 2},
]
