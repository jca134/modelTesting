"""Prompt variants. Each is a TypeSafe-style question; p_sensitive() maps the answer
distribution {option: probability} to one probability that the file is sensitive."""

SENSITIVE_DESC = (
    "Contains private information about an identifiable person or organization: medical or "
    "mental-health details, student records or grades, Social Security / passport / ID numbers, "
    "bank or card numbers, salaries, passwords or API keys, legal, HR, disciplinary or "
    "immigration matters."
)
NOT_SENSITIVE_DESC = (
    "General, public, or educational content: course material, announcements, recipes, code, "
    "aggregate statistics, blank forms, fiction, placeholder or redacted data, or public "
    "directory information. Nothing private about a specific real person."
)

PROMPTS = {
    "p1_bare_yesno": {
        "type": "noul",
        "instructions": "Does this file contain sensitive information?",
    },
    "p2_defined_choice": {
        "type": "choice",
        "instructions": "Classify this file for a data-privacy scan of a university Google Drive.",
        "criteria": {"sensitive": SENSITIVE_DESC, "not_sensitive": NOT_SENSITIVE_DESC},
    },
    "p3_category": {
        "type": "choice",
        "instructions": "What is the most sensitive kind of information in this file?",
        "criteria": {
            "medical": "Health, medical, or mental-health details about a specific person",
            "student_records": "Grades, conduct, advising, accommodations, or other FERPA records about a named student",
            "id_numbers": "Social Security, passport, driver's license, visa, or other ID numbers",
            "financial": "Bank accounts, card numbers, salaries, income, or payroll for a specific person",
            "credentials": "Real passwords, API keys, private keys, or login secrets",
            "legal_hr": "Legal, HR, disciplinary, harassment, criminal, or immigration matters about a person",
            "none": "None of these: general, public, aggregate, fictional, redacted, or placeholder content",
        },
    },
    "p4_risk_scale": {
        "type": "choice",
        "instructions": "How much harm could result if this file were shared publicly by mistake?",
        "criteria": {
            "public": "No harm: public or general information",
            "internal": "Minor: internal but impersonal (plans, budgets, schedules)",
            "personal": "Moderate: private details about an identifiable person",
            "severe": "Severe: health, ID numbers, financial accounts, credentials, or legal records",
        },
    },
    "p5_privacy_officer": {
        "type": "choice",
        "instructions": (
            "You are a university privacy officer. If this file were accidentally shared with "
            "'anyone with the link', would it expose a real person's private data or secrets in a "
            "way that violates FERPA, HIPAA, or basic privacy?"
        ),
        "criteria": {
            "yes": "Yes: it exposes a real person's private data, or working credentials",
            "no": "No: nothing private or secret about a real person would be exposed",
        },
    },
}

SENSITIVE_OPTIONS = {
    "p1_bare_yesno": {"yes"},
    "p2_defined_choice": {"sensitive"},
    "p3_category": {"medical", "student_records", "id_numbers", "financial", "credentials", "legal_hr"},
    "p4_risk_scale": {"personal", "severe"},
    "p5_privacy_officer": {"yes"},
}


def p_sensitive(prompt_name, dist):
    return float(sum(p for k, p in dist.items() if k in SENSITIVE_OPTIONS[prompt_name]))
