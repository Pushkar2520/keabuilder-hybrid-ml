from app.schemas import LeadInput


def calculate_rule_score(lead: LeadInput) -> float:
    """
    Deterministic scoring layer.

    This captures explicit business signals such as budget, urgency,
    acquisition source, and clarity of the submitted goal.
    """

    score = 0.0

    goal = lead.goal.lower()
    business_type = lead.business_type.lower()
    timeline = (lead.timeline or "").lower()
    source = (lead.source or "").lower()

    high_intent_terms = [
        "urgent",
        "immediately",
        "as soon as possible",
        "book calls",
        "generate leads",
        "sales funnel",
        "automation",
        "crm",
        "paid ads",
        "conversion",
        "demo",
        "pricing"
    ]

    if any(term in goal for term in high_intent_terms):
        score += 25

    if business_type in [
        "real estate",
        "coaching",
        "agency",
        "saas",
        "ecommerce",
        "education"
    ]:
        score += 15

    if lead.budget is not None:
        if lead.budget >= 50000:
            score += 25
        elif lead.budget >= 20000:
            score += 18
        elif lead.budget >= 5000:
            score += 10

    if any(term in timeline for term in ["urgent", "today", "this week", "immediate"]):
        score += 20
    elif any(term in timeline for term in ["this month", "soon", "next week"]):
        score += 12

    if source in ["google ads", "facebook ads", "linkedin ads", "referral"]:
        score += 10
    elif source in ["organic", "website", "social media"]:
        score += 6

    if lead.message and len(lead.message.split()) >= 8:
        score += 5

    return min(score, 100.0)